# localStorage Keys Registry

Every localStorage key used in this project. For each: producers (setItem), consumers (getItem), and status. Update whenever a key is added, removed, or its value format changes. Archive/ and admin/ files excluded from this registry (they manage their own internal keys).

---

## `aesop-learner-id`

Primary learner identity key. UUID v4 or `AESOP-XXXX` short code depending on entry point. Shared across assessment, students page, and transcript.

**Value format:** `string` — either full UUID (from `firebase-helpers.js`) or `AESOP-XXXX` short code (from `students.html` / `transcript.html`)

**Producers**
- `ai-academy/students.html:100` — `setItem` on new account creation (short code `AESOP-XXXX`)
- `ai-academy/students.html:122` — `setItem` on ID lookup / login
- `ai-academy/students.html:163` — `setItem` inside `onRecovered` callback (hardcoded string, not using `LS_ID` constant — minor inconsistency)
- `ai-academy/js/firebase-helpers.js:406` — `setItem` via `getOrCreateLearnerId()` (UUID v4)
- `ai-academy/js/qr-recovery.js:47` — `setItem` on successful QR recovery (UUID v4)

**Consumers**
- `ai-academy/students.html:88` — `getItem` on page load (drives welcome gate vs hub)
- `ai-academy/js/firebase-helpers.js:401` — `getItem` via `getOrCreateLearnerId()`

**Shape note:** Two ID formats coexist: short codes (`AESOP-XXXX`) created by `students.html` / `transcript.html`, and UUID v4 created by `firebase-helpers.js` for assessment. A student who created their account via the Student Hub will have a short code; if they then take the assessment, `getOrCreateLearnerId()` will reuse that short code as the Firestore document ID. The assessment and progress records will be stored under different IDs if the student uses different entry points on different devices.

**Status:** ⚠ two ID formats (short code vs UUID) depending on entry point — functionally separate learner records if device differs

---

## `aesop-assessment-complete`

Boolean flag marking whether the learner has completed the assessment. Drives homepage CTA and student page pathway display.

**Value format:** `string` — exactly `'1'` when set; absence or any other value treated as false.

**Producers**
- `ai-academy/js/pathway-display.js:145` — `setItem('aesop-assessment-complete', '1')` via `markAssessmentComplete()`

**Consumers**
- `ai-academy/js/pathway-display.js:133` — `getItem` via `hasCompletedAssessment()` (returns boolean)
- `ai-academy/index.html:3137` — `getItem` directly to decide CTA variant (Take Assessment vs View Pathway)

**Status:** ✓ one producer, two consumers, value format consistent

---

## `aesop_firebase_offline_queue`

Write-ahead queue for Firestore operations that failed due to network unavailability.

**Value format:** `JSON string` — serialized `Array<{operation: string, data: object, timestamp: string}>`

**Producers**
- `ai-academy/js/firebase-helpers.js:317` — `setItem` via `queueOfflineWrite()` (appends)
- `ai-academy/js/firebase-helpers.js:368` — `setItem('[]')` via `processOfflineQueue()` (clears after sync)

**Consumers**
- `ai-academy/js/firebase-helpers.js:311` — `getItem` via `queueOfflineWrite()` (reads before append)
- `ai-academy/js/firebase-helpers.js:329` — `getItem` via `processOfflineQueue()` (reads queue to process)

**Status:** ✓ producer and consumer in same module

---

## `aesop-streak`

Daily study streak counter.

**Value format:** `JSON string` — `{count: number, last: "YYYY-MM-DD"}`

**Producers**
- `ai-academy/students.html:74` — `setItem` via `updateStreak()`

**Consumers**
- `ai-academy/students.html:68` — `getItem` via `updateStreak()`

**Status:** ✓ producer and consumer in same file

---

## `aesop-course-progress`

Course-level module progress written by course pages, read by students.html.

**Value format:** `JSON string` — `{ [courseId]: { [moduleId]: {...} } }`

**Producers**
- Individual course/module HTML files (not enumerated here — convention documented in `AESOP-MODULE-BUILD-STANDARDS.md`)

**Consumers**
- `ai-academy/students.html:174` — `getItem` to merge into Firestore-loaded progress

**Status:** ✓ convention-based; individual module files are producers

---

## `aesop-hub-progress`

Lesson-level progress including completed lessons and passed tests, written by module hub, read by students.html.

**Value format:** `JSON string` — `{completedLessons: {...}, passedTests: {...}}`

**Consumers**
- `ai-academy/students.html:183` — `getItem` to build per-course progress display

**Producers**
- Module hub pages (not enumerated here — same convention as `aesop-course-progress`)

**Status:** ✓ convention-based

---

## `aesop-cert-fdn`

Certification foundation course completion count (integer). Drives certification card display on student hub.

**Value format:** `string` — integer stringified (read via `parseInt`)

**Producers**
- Certification tracking logic in course/module pages (not enumerated here)

**Consumers**
- `ai-academy/students.html:628` — `getItem` to determine certification level

**Status:** ✓ consumed; producer location conventional

---

## `aesop-cert-mpts`

Certification module points total. Drives certification card display.

**Value format:** `string` — integer stringified (read via `parseInt`)

**Producers**
- Certification tracking logic in course/module pages

**Consumers**
- `ai-academy/students.html:629` — `getItem` to determine certification level

**Status:** ✓ consumed; producer location conventional

---

## `aesop-theme`

Dark mode preference.

**Value format:** `string` — `'dark'` or `'light'`

**Producers**
- Theme toggle scripts in various pages (pattern: `localStorage.setItem(KEY, 'dark'/'light')`)

**Consumers**
- Theme initialization scripts in various pages (pattern: `localStorage.getItem(KEY) === 'dark'`)

**Status:** ✓ standard convention across all pages

---

## `aesop-product-course-requests-v1`

Local fallback queue for product training requests from `/theladder-products/` when Firestore does not accept the write. This is not the primary approval system; it exists so the learner gets a recoverable record instead of losing the request.

**Value format:** `JSON string` - array of product request objects matching the `productCourseRequests` shape, plus `id`, `localOnly`, and `error` fields.

**Producers**
- `theladder-products/products-app.js` - `setItem` when Firestore `addDoc` fails

**Consumers**
- `theladder-products/products-admin.js` - `getItem` to show same-browser fallback requests on the admin queue

**Status:** ⚠ same-browser fallback only; production approval should use Firestore `productCourseRequests`

---

## Summary

| Key | Format | Producers | Consumers | Status |
|-----|--------|-----------|-----------|--------|
| `aesop-learner-id` | string (UUID or short code) | students.html, firebase-helpers.js, qr-recovery.js | students.html, firebase-helpers.js | ⚠ two ID formats |
| `aesop-assessment-complete` | `'1'` | pathway-display.js | pathway-display.js, index.html | ✓ |
| `aesop_firebase_offline_queue` | JSON array | firebase-helpers.js | firebase-helpers.js | ✓ |
| `aesop-streak` | JSON object | students.html | students.html | ✓ |
| `aesop-course-progress` | JSON object | module pages | students.html | ✓ |
| `aesop-hub-progress` | JSON object | module hub | students.html | ✓ |
| `aesop-cert-fdn` | integer string | cert tracking | students.html | ✓ |
| `aesop-cert-mpts` | integer string | cert tracking | students.html | ✓ |
| `aesop-theme` | `'dark'\|'light'` | theme toggles | theme init scripts | ✓ |
| `aesop-product-course-requests-v1` | JSON array | products-app.js | products-admin.js | ⚠ local fallback only |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-23T00:00:00Z (by /cross-boundary-audit, Task #6 branch)

**Boundaries checked:** localStorage keys across ai-academy/js/, ai-academy/students.html, ai-academy/index.html, ai-academy/assessment.html (archive/ excluded)

**Evidence recorded:**
- 8 entries with complete or convention-based producer/consumer pairs ✓
- 1 entry with format inconsistency (`aesop-learner-id` — two ID formats)
- 1 inline hardcoded string instead of constant (`students.html:163`)
- New identifiers introduced on this task: `aesop-assessment-complete`, `aesop_firebase_offline_queue` (Task #6)
- Registries match current code diff: yes

**Gaps identified:**
- `aesop-learner-id`: two ID formats (UUID vs short code) depending on entry point — students who create account on Student Hub then take assessment may accumulate two separate Firestore records
- `students.html:163` uses hardcoded `'aesop-learner-id'` string instead of `LS_ID` constant

**Status:** Audit complete
