# API Endpoints Registry

Every HTTP endpoint served by this project's API layer. For each: request shape, response shape, producers (PHP handler), consumers (JS callers), and status. Update whenever an endpoint is added, changed, or removed.

---

## `POST /aesop-api/proxy.php`

Lab chat proxy. Forwards student chat messages to Anthropic API using `claude-haiku-4-5-20251001`. Used by all course module labs.

**Request shape (JSON body):**
```
{
  messages:      Array<{role: "user"|"assistant", content: string}>,  // required
  system_prompt: string,                                               // optional
  max_tokens:    number                                                // optional; capped at 1024
}
```

**Response shape (JSON):**
Anthropic API response passthrough:
```
{
  content: [{type: "text", text: string}],
  ...
}
```
On error: `{"error": "message string"}`

**Producer**
- `aesop-api/proxy.php:7` — handler; reads `system_prompt` (line 51), caps `max_tokens` at 1024, slices conversation to last 40 turns

**Consumers**
- All course module HTML files under `ai-academy/modules/` — `var PROXY_URL='/aesop-api/proxy.php'` convention
- `ai-academy/modules/admin-review.js:5` — `const PROXY='/aesop-api/proxy.php'`

**Status:** ✓ widely consumed; field names consistent

---

## `POST /aesop-api/assessment-proxy.php`

Assessment chat proxy. Forwards assessment conversation to Anthropic API using `claude-sonnet-4-6`. Separate from lab proxy to allow higher token cap and hardcoded system prompt.

**Request shape (JSON body):**
```
{
  messages:   Array<{role: "user"|"assistant", content: string}>,  // required; each ≤4000 chars; ≤20 turns
  max_tokens: number                                                // optional; capped at 800
}
```

Note: system prompt is **hardcoded server-side** (PHP nowdoc). Any `system_prompt` field sent by the client is silently ignored. Client cannot override the guardrail.

**Response shape (JSON):**
Anthropic API response passthrough on success:
```
{
  content: [{type: "text", text: string}],
  ...
}
```
On error: `{"error": "human-readable message"}` (no raw Anthropic body or internal details exposed)

**Rate limit:** 10 requests/minute per IP (atomic file lock)

**Producer**
- `aesop-api/assessment-proxy.php:26` — hardcoded `$SYSTEM_PROMPT` nowdoc; reads only `messages` + `max_tokens` from request; caps at 800 tokens / 20 turns; per-IP rate limit via `flock(LOCK_EX)` temp file

**Consumers**
- `ai-academy/js/assessment-chat.js:80` — `fetch(PROXY_URL, {messages, max_tokens})`; no `system_prompt` sent

**Status:** ✓ — system prompt server-side; client contract: `{messages, max_tokens}` only

---

## Summary

| Endpoint | Method | Model | Token cap | History cap | Status |
|----------|--------|-------|-----------|-------------|--------|
| `/aesop-api/proxy.php` | POST | claude-haiku-4-5-20251001 | 1024 | 40 turns | ✓ |
| `/aesop-api/assessment-proxy.php` | POST | claude-sonnet-4-6 | 800 | 20 turns | ✓ system prompt server-side |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-23T00:00:00Z (by /cross-boundary-audit, Task #6 branch); updated 2026-05-23 (Codex review remediation)

**Boundaries checked:** All PHP files in aesop-api/ serving HTTP responses; all JS fetch() calls in ai-academy/js/ and module HTML files

**Evidence recorded:**
- 1 endpoint with complete match ✓ (`proxy.php`)
- `assessment-proxy.php` client contract updated: `system_prompt` field removed (system prompt now hardcoded server-side, client sends only `{messages, max_tokens}`)

**Status:** Audit current
