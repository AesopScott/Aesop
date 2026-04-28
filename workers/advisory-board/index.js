/**
 * AESOP Advisory Board Worker
 *
 * Handles form submissions and member deletions without exposing
 * any credentials to the browser.
 *
 * Secrets (set via Cloudflare dashboard or wrangler secret put):
 *   GITHUB_PAT      — fine-grained PAT, Contents R/W on AesopScott/Aesop
 *   ADMIN_PASSWORD  — password for the admin delete page
 */

const REPO    = 'AesopScott/Aesop';
const PATH    = 'about/advisory-board-members.json';
const GH_API  = `https://api.github.com/repos/${REPO}/contents/${PATH}`;

const ALLOWED_ORIGINS = [
  'https://aesopacademy.org',
  'https://www.aesopacademy.org',
  'http://localhost',
  'http://127.0.0.1',
];

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allowed = ALLOWED_ORIGINS.some(o => origin.startsWith(o));

    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(allowed ? origin : ALLOWED_ORIGINS[0]),
      });
    }

    const url = new URL(request.url);
    let response;

    if (url.pathname === '/add'    && request.method === 'POST') response = await handleAdd(request, env);
    else if (url.pathname === '/remove' && request.method === 'POST') response = await handleRemove(request, env);
    else if (url.pathname === '/list'   && request.method === 'GET')  response = await handleList(env);
    else response = json({ error: 'Not found' }, 404);

    // Attach CORS headers to every response
    const h = new Headers(response.headers);
    for (const [k, v] of Object.entries(corsHeaders(allowed ? origin : ALLOWED_ORIGINS[0]))) {
      h.set(k, v);
    }
    return new Response(response.body, { status: response.status, headers: h });
  },
};

// ── ADD MEMBER ──────────────────────────────────────────────────
async function handleAdd(request, env) {
  let member;
  try { member = await request.json(); }
  catch { return json({ error: 'Invalid JSON' }, 400); }

  const missing = ['name', 'title', 'organization', 'linkedin', 'bio']
    .filter(f => !member[f] || !String(member[f]).trim());
  if (missing.length) return json({ error: `Missing: ${missing.join(', ')}` }, 400);

  // Extract photo before writing JSON — stored as a separate GitHub file
  const photoData = member.photo || null;
  delete member.photo;

  // Match key: normalize the LinkedIn URL so trivial differences
  // (trailing slash, tracking query string, casing) don't create
  // duplicates. LinkedIn is required by the form, so this is reliable.
  const linkKey = (m) => (m.linkedin || '')
    .toLowerCase()
    .trim()
    .replace(/\/+$/, '')   // drop trailing slash
    .split('?')[0];        // drop query string (utm_*, etc.)

  member.addedAt = member.addedAt || new Date().toISOString();

  // We may need the photo upload to know the member's id, but for an
  // UPSERT we want to reuse the existing member's id rather than mint
  // a new one. Resolve match first, then mint id if it's a new member,
  // then upload the photo against the final id.
  let isUpdate = false;
  let resolvedId = member.id || null;

  // Pull the file once up front to look for an existing entry by
  // LinkedIn match. updateFile() below will fetch again — extra GET is
  // cheap compared to dealing with race conditions across two writes.
  let preexisting;
  try {
    const { data } = await ghGet(env.GITHUB_PAT);
    const incomingKey = linkKey(member);
    if (incomingKey) {
      preexisting = (data.members || [])
        .find(m => linkKey(m) === incomingKey);
    }
  } catch (err) {
    // Non-fatal: fall through and let updateFile() report the GitHub
    // error in the normal path.
    console.error('Pre-check ghGet failed (non-fatal):', err);
  }
  if (preexisting) {
    isUpdate   = true;
    resolvedId = preexisting.id;
  } else if (!resolvedId) {
    resolvedId = member.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')
                 + '-' + Date.now();
  }
  member.id = resolvedId;

  // Upload photo to GitHub (non-fatal if it fails)
  if (photoData) {
    try {
      await writePhoto(env.GITHUB_PAT, member.id, photoData);
      member.hasPhoto = true;
    } catch (err) {
      console.error('Photo write failed (non-fatal):', err);
    }
  }

  return updateFile(env, data => {
    data.members = data.members || [];
    const incomingKey = linkKey(member);
    const idx = incomingKey
      ? data.members.findIndex(m => linkKey(m) === incomingKey)
      : -1;
    if (idx >= 0) {
      // UPDATE: preserve the existing entry's identity and curator-set
      // fields (board membership, addedAt) while taking everything
      // else from the new submission.
      const existing = data.members[idx];
      data.members[idx] = {
        ...existing,
        ...member,
        id:       existing.id,                     // never reassign id
        addedAt:  existing.addedAt || member.addedAt,
        // Curator-controlled fields: only fall through to incoming
        // value if the existing entry didn't have one.
        board:    existing.board   ?? member.board,
        boards:   existing.boards  ?? member.boards,
        hasPhoto: (member.hasPhoto !== undefined)
                    ? member.hasPhoto
                    : existing.hasPhoto,
      };
    } else {
      data.members.push(member);
    }
    return data;
  }, isUpdate
       ? `Update advisory board member: ${member.name}`
       : `Add advisory board member: ${member.name}`);
}

// ── REMOVE MEMBER ───────────────────────────────────────────────
async function handleRemove(request, env) {
  let body;
  try { body = await request.json(); }
  catch { return json({ error: 'Invalid JSON' }, 400); }

  if (!body.password || body.password !== env.ADMIN_PASSWORD) {
    return json({ error: 'Unauthorized' }, 401);
  }
  if (!body.id) return json({ error: 'Missing member id' }, 400);

  return updateFile(env, data => {
    const before = (data.members || []).length;
    data.members = (data.members || []).filter(m => m.id !== body.id);
    if (data.members.length === before) throw Object.assign(new Error('Not found'), { status: 404 });
    return data;
  }, `Remove advisory board member: ${body.id}`);
}

// ── LIST MEMBERS (admin read) ────────────────────────────────────
async function handleList(env) {
  const { data } = await ghGet(env.GITHUB_PAT);
  return json({ members: data.members || [] });
}

// ── SHARED FILE UPDATE ──────────────────────────────────────────
async function updateFile(env, transform, message) {
  try {
    const { data, sha } = await ghGet(env.GITHUB_PAT);
    const updated = transform(data);
    await ghPut(env.GITHUB_PAT, updated, sha, message);
    return json({ success: true });
  } catch (err) {
    if (err.status === 404) return json({ error: 'Member not found' }, 404);
    console.error(err);
    return json({ error: err.message || 'GitHub write failed' }, 500);
  }
}

// ── WRITE MEMBER PHOTO ──────────────────────────────────────────
async function writePhoto(pat, id, dataUrl) {
  // Strip the data URL prefix ("data:image/jpeg;base64,")
  const base64   = dataUrl.replace(/^data:image\/[a-z]+;base64,/, '');
  const photoApi = `https://api.github.com/repos/${REPO}/contents/about/advisory-board-photos/${id}.jpg`;

  const r = await fetch(photoApi, {
    method: 'PUT',
    headers: {
      Authorization:  `token ${pat}`,
      'Content-Type': 'application/json',
      Accept:         'application/vnd.github.v3+json',
      'User-Agent':   'AESOP-Board-Worker/1.0',
    },
    body: JSON.stringify({
      message: `Add photo for advisory board member: ${id}`,
      content: base64,
    }),
  });

  if (!r.ok) {
    const text = await r.text();
    throw new Error(`GitHub photo PUT ${r.status}: ${text}`);
  }
}

// ── GITHUB API HELPERS ──────────────────────────────────────────
async function ghGet(pat) {
  const r = await fetch(GH_API, {
    headers: {
      Authorization: `token ${pat}`,
      Accept: 'application/vnd.github.v3+json',
      'User-Agent': 'AESOP-Board-Worker/1.0',
    },
  });
  if (!r.ok) throw Object.assign(new Error(`GitHub GET ${r.status}`), { status: r.status });
  const d = await r.json();
  return {
    data: JSON.parse(new TextDecoder().decode(base64Decode(d.content.replace(/\n/g, '')))),
    sha: d.sha,
  };
}

async function ghPut(pat, payload, sha, message) {
  const body   = JSON.stringify(payload, null, 2);
  const bytes  = new TextEncoder().encode(body);
  const encoded = base64Encode(bytes);
  const r = await fetch(GH_API, {
    method: 'PUT',
    headers: {
      Authorization: `token ${pat}`,
      'Content-Type': 'application/json',
      Accept: 'application/vnd.github.v3+json',
      'User-Agent': 'AESOP-Board-Worker/1.0',
    },
    body: JSON.stringify({ message, content: encoded, sha }),
  });
  if (!r.ok) {
    const text = await r.text();
    throw Object.assign(new Error(`GitHub PUT ${r.status}: ${text}`), { status: r.status });
  }
}

// ── UTILITIES ───────────────────────────────────────────────────
function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin':  origin,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age':       '86400',
  };
}

function base64Decode(str) {
  const bin = atob(str);
  const buf = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
  return buf;
}

function base64Encode(bytes) {
  let bin = '';
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin);
}
