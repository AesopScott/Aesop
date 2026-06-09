# theladder-shared

Reusable, catalog-agnostic engines extracted from the Concepts ladder
(`theladder/ladder-app.js`) so that other pathways — products
(`theladder-products/products-app.js`) and use cases
(`theladder-use-cases/use-cases-app.js`) — can run the same placement and
certification logic without copy-pasting it.

These are **framework-free vanilla ES modules** (no Firebase, no DOM, no app
state). They match the module style of `ladder-app.js`, which is loaded via
`<script type="module" src="/theladder/ladder-app.js">`. The product and
use-case apps are also loaded with `<script type="module">`, so they import
these engines directly:

```js
import { createPlacementEngine } from '/theladder-shared/placement-engine.js';
import { createCertificationEngine } from '/theladder-shared/certification-engine.js';
```

The original `theladder/ladder-app.js` is **not modified** — the Concepts
ladder keeps its own inline copy and stays live. These modules generalize that
logic; adopting them inside `ladder-app.js` is a separate, optional follow-up.

---

## placement-engine.js

A catalog-agnostic placement assessment engine. The caller supplies a
**catalog descriptor** (items + grouping + grant/assignment rules) and gets
back a placement system-prompt builder, the completion-signal regex + parser,
a normalizer, and a grant/assignment resolver.

### Public API surface

- `createPlacementEngine(descriptor)` — bind an engine to one catalog.
- `engine.PLACEMENT_REGEX` — the completion-signal RegExp.
- `engine.buildSystemPrompt({ languageLabel })` — placement assessor prompt.
- `engine.placementOpener()` — first assistant message.
- `engine.parsePlacementResponse(rawText)` → `{ placement, visibleText }`.
- `engine.normalizePlacementSignals(raw)` → normalized placement (the
  grant/assignment resolver: clamps scores, filters tags, resolves granted
  groups + assigned item ids).
- `engine.resolveGrantedGroups(scores)` → group ids placed out of.
- `engine.resolveAssignedItemIds(grantedGroupIds, tags)` → assigned item ids.
- `engine.shouldApplyPlacement(placement, learnerTurnCount)` → boolean gate.
- Exports: `PLACEMENT_REGEX`, `DEFAULT_INTEREST_TAGS`,
  `DEFAULT_INTEREST_KEYWORDS`, `clampInt`, `normalizeTags`.

The descriptor shape and every field are documented in the header comment of
`placement-engine.js`.

### Generalized from `theladder/ladder-app.js`

| Concept | ladder-app.js source | Notes |
|---|---|---|
| `PLACEMENT_REGEX` | line 12 | Marker contract kept identical. |
| `normalizePlacementSignals` | lines 540–557 | Generalized; `assignedTopicIds` now resolved from descriptor items, not `LADDER_TIERS`. |
| `grantRules` | lines 479–498 | Lifted out as caller-supplied `descriptor.grantRules(scores)`; the Concepts ladder's hard-coded tier thresholds become one descriptor's rules. |
| `assignedTopicsForPlacement` | lines 526–538 | Generalized to `resolveAssignedItemIds`; "core topic" (order ≤ 4 or readiness check) → `isCoreItem` / `coreItemsPerGroup`. |
| `topicMatchesInterest` | lines 500–515 | Generalized to `itemMatchesInterest`; keyword map is `DEFAULT_INTEREST_KEYWORDS`, overridable per catalog. |
| `normalizeTags` | lines 569–574 | Exported; allowed-tag list is now a descriptor option. |
| `clampInt` | lines 576–580 | Exported helper. |
| `interestText` | lines 455–458 | Folded into each item's `interestText` field. |
| `parsePlacementResponse` | lines 896–906 | Same strip-marker + parse + normalize flow. |
| `placementSystemPrompt` | lines 1331–1362 | Generalized to `buildSystemPrompt`; dimensions/role/opener are descriptor `assessment` options with AI-fluency defaults. |
| `placementOpener` | lines 1364–1366 | Default opener in `assessment.opener`. |
| 5-reply apply gate | line 1443 (`userAssessmentTurns() >= 5`) | Generalized to `shouldApplyPlacement` + `minLearnerTurns`. |

---

## certification-engine.js

A catalog-agnostic certification engine that preserves the doc-16 guarantees
(`G:/My Drive/Obsidian/Aesop_Build/16-Ladder-Certification-Architecture.md`):
an AI examiner proposes a result; an **independent second-model validator**
must confirm both the learner side (sufficient evidence) and the examiner side
(fair, scoped, on-blueprint) before any credential is recorded; **no credential
without validation**; a failed validation is logged but not credentialed.

### Public API surface

- `createCertificationEngine({ proxyUrl, validatorModel, rubricDimensions, fetchImpl })`.
- Regexes: `engine.CERTIFICATION_RESULT_REGEX`, `engine.CERTIFICATION_VALIDATION_REGEX`.
- `engine.buildExaminerSystemPrompt(blueprint)` — examiner prompt parameterized
  by item / education tier / certification tier / depth / standards; discloses
  the 7 rubric dimensions to the learner.
- `engine.rubricDisclosure()` — plain-language "BEFORE YOU BEGIN" text.
- `engine.parseExaminerResponse(rawText)` → `{ certificationResult, rubricDimensions, visibleText }`.
- `engine.parseRubricEvaluation(rawText)` → the 7-dimension rubric evaluation.
- `engine.buildValidationSystemPrompt()` / `engine.buildValidationMessages(...)`.
- `engine.parseValidationResponse` / `normalizeValidation` / `failedValidation`.
- `engine.validateCertification(context, result, conversationMessages)` — the
  second-model validator **call + decision** (proxy at `/aesop-api/proxy.php`).
- `engine.recordCertificationResult({ context, result, conversationMessages, hooks })`
  — the full no-credential-without-validation pipeline. Returns
  `{ outcome: 'validation_failed' | 'not_awarded' | 'awarded', validation, record? }`.
- `engine.buildEvidencePacket({ context, result, rubricDimensions, validation, extra })`
  — evidence packet matching doc-16 "Rubric And Evidence Packet Requirements".
- `engine.buildChallenge(...)` / `engine.resolveChallenge(...)` /
  `engine.CHALLENGE_OUTCOMES` — the challenge flow.
- Exports: `CERTIFICATION_VALIDATOR_MODEL`, `RUBRIC_DIMENSIONS`,
  `TRANSCRIPT_STATUS`, `CHALLENGE_OUTCOMES`, `PROXY_URL`.

The blueprint, hooks, and evidence-packet shapes are documented in the header
comment of `certification-engine.js`.

### Generalized from `theladder/ladder-app.js`

| Concept | ladder-app.js source | Notes |
|---|---|---|
| `CERTIFICATION_RESULT_REGEX` | line 13 | Marker contract kept identical. |
| `CERTIFICATION_VALIDATION_REGEX` | line 14 | Marker contract kept identical. |
| `CERTIFICATION_VALIDATOR_MODEL` | line 16 | Default validator model; overridable via options. |
| 7 rubric dimensions + `parseRubricEvaluation` | lines 2603–2641 | Generalized; dimension list is an option. |
| Rubric disclosure block | lines 2500–2508 | Lifted to `rubricDisclosure()`. |
| Examiner system prompt (`systemPromptFor` evaluation block) | lines 2480–2532 | Generalized to `buildExaminerSystemPrompt(blueprint)`; drops Concepts-only readiness/completion/teaching blocks and tier coupling. |
| `parseCertificationResponse` | lines 908–920 | → `parseExaminerResponse`. |
| `certificationValidationSystemPrompt` | lines 1152–1166 | → `buildValidationSystemPrompt`; "Ladder tier" wording generalized to "item under test". |
| `certificationValidationMessages` | lines 1169–1186 | → `buildValidationMessages`. |
| `parseCertificationValidationResponse` | lines 922–931 | → `parseValidationResponse`. |
| `normalizeCertificationValidation` | lines 1188–1215 | → `normalizeValidation`; accepts `itemId`/`itemLabel` with `ladderTierId` fallbacks. |
| `failedCertificationValidation` | lines 1217–1226 | → `failedValidation`. |
| `validateCertificationConversation` | lines 1234–1256 | → `validateCertification`; takes `conversationMessages` arg instead of reading app state. |
| `recordCertificationResult` | lines 1258–1329 | Generalized; the no-credential-without-validation invariant + transcript distinction preserved. App-state writes are pushed to caller `hooks` (`onValidation`, `onCredential`, `resolveItem`, `buildIdentityAssurance`). |
| `buildCertificationResult` | lines 2643–2658 | Subsumed by `buildEvidencePacket`, expanded to the full doc-16 field list. |
| Challenge outcomes / flow | doc-16 "Challenge Flow" + "Challenge Documentation" | New `buildChallenge` / `resolveChallenge` scaffolding (the Concepts ladder app does not yet implement the structured challenge packet). |

> Line refs are against `theladder/ladder-app.js` at extraction time
> (`orch/shared-engines` worktree). Re-grep if the file drifts.

---

## Invariants (do not break when merging)

1. **Placement signal contract.** The marker `<!--LADDER_PLACEMENT_COMPLETE:{...}-->`
   and its JSON keys (`capabilityScore`, `technicalScore`, `governanceScore`,
   `interestTags`, `reasoning`) are fixed across all pathways.

2. **Certification signal contract.** The markers
   `<!--LADDER_CERTIFICATION_RESULT:{...}-->` and
   `<!--LADDER_CERTIFICATION_VALIDATION:{...}-->` are fixed.

3. **No credential without second-model validation.** A credential record is
   only produced when an independent validator returns `valid === true`
   (both `learner_valid` and `examiner_valid`). `recordCertificationResult`
   enforces this; a failed or unreachable validator yields a logged-but-not-
   credentialed outcome. Do not call `onCredential` outside this pipeline.
