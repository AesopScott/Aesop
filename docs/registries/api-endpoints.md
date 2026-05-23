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

Assessment chat proxy. Forwards assessment conversation to Anthropic API using `claude-sonnet-4-6`. Separate from lab proxy to allow higher token cap and different model.

**Request shape (JSON body):**
```
{
  messages:      Array<{role: "user"|"assistant", content: string}>,  // required
  system_prompt: string,                                               // optional — see gap note
  max_tokens:    number                                                // optional; capped at 800
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
- `aesop-api/assessment-proxy.php:11` — handler; reads `system_prompt` (line 54), caps `max_tokens` at 800, slices conversation to last 20 turns

**Consumers**
- `ai-academy/js/assessment-chat.js:80` — `fetch(PROXY_URL, ...)` where `PROXY_URL = '/aesop-api/assessment-proxy.php'`

**Bug fixed (Task #6 audit):** `assessment-chat.js` originally sent `system: ASSESSMENT_SYSTEM_PROMPT` but the proxy reads `$input['system_prompt']`. Fixed in same commit as this registry — key renamed to `system_prompt` in `assessment-chat.js:85`.

**Status:** ✓ (post-fix) — field name aligned

---

## Summary

| Endpoint | Method | Model | Token cap | History cap | Status |
|----------|--------|-------|-----------|-------------|--------|
| `/aesop-api/proxy.php` | POST | claude-haiku-4-5-20251001 | 1024 | 40 turns | ✓ |
| `/aesop-api/assessment-proxy.php` | POST | claude-sonnet-4-6 | 800 | 20 turns | ✓ (fixed) |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-23T00:00:00Z (by /cross-boundary-audit, Task #6 branch)

**Boundaries checked:** All PHP files in aesop-api/ serving HTTP responses; all JS fetch() calls in ai-academy/js/ and module HTML files

**Evidence recorded:**
- 1 endpoint with complete match ✓ (`proxy.php`)
- 1 endpoint with critical field name mismatch discovered and fixed (`assessment-proxy.php`)
- New identifiers introduced on this task: `/aesop-api/assessment-proxy.php` (Task #6)
- Registries match current code diff: yes (post-fix)

**Gaps identified:**
- `assessment-proxy.php` — consumer sent `system` key; proxy expected `system_prompt`. System prompt was silently dropped. Fixed: `assessment-chat.js:85` updated from `system:` to `system_prompt:`.

**Status:** Audit complete
