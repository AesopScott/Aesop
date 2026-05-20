# Cross-Boundary Registries

This directory contains registries of named boundaries in the Aesop AI Academy project. A **boundary** is anywhere two or more pieces of code, config, or infrastructure refer to the same name independently and can disagree.

## What's Here

- **`claude-models.md`** — Claude model versions (e.g., Haiku, Sonnet) and where they're used
- **`env-vars.md`** — Environment variables (API keys, config values) and where they're read/set
- **`pinecone-integration.md`** — Pinecone vector database index names and access points
- **`research-data-structures.md`** — Data structure contracts between research, recommendation, and planning modules (Task #1)

Each registry lists:
- **Producers** — where the name is written/set/defined
- **Consumers** — where the name is read/used/checked
- **Status** — whether producer and consumer are in sync (✓) or have gaps (⚠)
- **Audit Trail** — when the registry was last verified and what was checked

## Why Registries Matter

When two parts of code reference the same name independently, they can drift:
- A model name changes in one place but not another → wrong model called
- An env var name is misspelled in one consumer → missing config
- A data structure shape changes in producer but not consumer → runtime errors

Registries prevent this by making every name visible with every producer and consumer listed alongside it.

## Maintenance Rules

**Every PR that touches a cross-boundary name must update the relevant registry in the same commit.**

Examples:
- Adding a new Claude model? Update `claude-models.md`.
- Creating a new environment variable? Update `env-vars.md`.
- Changing the shape of `researchFindings`? Update `research-data-structures.md`.
- Adding a new Pinecone index? Update `pinecone-integration.md`.

**How to update a registry:**
1. Make your code change
2. Edit the relevant `.md` file
3. Add the new name or update the existing entry (producer/consumer locations, status)
4. Update the Audit Trail section with the current timestamp
5. Commit both the code change and the registry update together

**Running /cross-boundary-audit:**
Periodically (or before major releases), run `/cross-boundary-audit` to verify all registries still match the code. The audit will:
- Find every name across the codebase
- List every producer and consumer
- Flag any gaps (orphaned producers, orphaned consumers, shape mismatches)
- Update the Audit Trail in each registry with verification results

**Interpreting Status:**
- ✓ — Producer and consumer are in sync; at least one producer exists, at least one consumer exists, no obvious shape mismatches
- ⚠ orphan producer — Name is produced somewhere but never consumed
- ⚠ orphan consumer — Name is consumed/checked somewhere but never produced
- ⚠ shape mismatch — Producer and consumer disagree on the structure/fields
- ⚠ Planned — Name is planned (Task #N) but not yet in code

## Detected Boundaries (This Project)

These are the boundary kinds detected in the Aesop AI Academy project. As the codebase evolves, new kinds may emerge.

- **Claude Model Names** — e.g., `claude-haiku-4-5-20251001`, `claude-sonnet-4-20250514`
- **Environment Variables** — e.g., `AESOP_ANTHROPIC_API_KEY`, `PINECONE_API_KEY`
- **Pinecone Indexes** — e.g., `aesop-academy`
- **Research Data Structures** — e.g., `researchFindings`, `recommendations` (Task #1)

## Audit Trail Example

Each registry includes an Audit Trail section like this:

```
## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-20 19:45 UTC (by /cross-boundary-audit, Task #1 planning)

**Boundaries checked:** [what kinds were verified]

**Evidence recorded:**
- [N] entries with complete producer/consumer pairs ✓
- [M] entries with gaps (orphan producers/consumers) ⚠
- New identifiers introduced: [list or "none"]
- Registries match current code diff: [yes/no]

**Gaps identified:** [list of ⚠ findings, or "none"]

**Status:** Audit complete | Audit stale | Audit incomplete
```

This proves to reviewers and auditors that a human or automated process has verified the registry matches the code.

## Next Steps

Run `/cross-boundary-audit` before starting major implementation phases to validate that all boundaries are correctly named and that producers/consumers are in sync.
