# Stellar AI Director V2 Packet Manifest

Generated: 2026-07-08
Packet: Stellar AI Director Strategic V2 Roadmap Packet
Target: Stellaris PC 4.4.5 stable/current, backwards compatible with 4.4.4 where source-backed


## Packet Purpose

This packet replaces the prior shallow handoff with a strategic, evidence-gated development plan for Codex. It does not implement code. It gives Codex a product goal, technical contracts, phase roadmap, independent task slices, behavior model, validation plan, research backlog, evidence map, decision matrix, user-decision list, and read order.

## Produced Files

| File | Purpose | How Codex should use it |
| --- | --- | --- |
| `PRD.md` | Defines V2 product goals, non-goals, target version, compatibility frame, priorities, and success metrics. | Read first to understand why V2 is not just more AI weights. |
| `TECHNICAL_CONTRACTS.md` | Hard rules for script surfaces, generator ownership, validation, compatibility, unsafe surfaces, docs, and status reporting. | Keep open while editing. Violating it requires explicit task-gate evidence. |
| `IMPLEMENTATION_ROADMAP.md` | Strategic phased plan from current standalone state to stronger AI behavior and optional observer proof. | Use to choose the next phase and avoid unsafe ordering. |
| `CODEX_TASK_SLICES.md` | Commit-sized task cards with objectives, inputs, files, checks, acceptance criteria, dependencies, and artifacts. | Pick one card per implementation slice. |
| `AI_BEHAVIOR_DESIGN.md` | Defines observable AI behavior goals across economy, research, growth, fleets, war, defense, megastructures, colonies, crisis, and compatibility. | Use to judge whether code changes serve actual behavior goals. |
| `VALIDATION_AND_TEST_PLAN.md` | Static-first validation plan, existing tools, new validators/tests, runtime observer approval gate, and readiness gates. | Use before reporting ready-to-commit, ready-to-push, live-launch, or observer status. |
| `RESEARCH_QUESTIONS.md` | Technical unknowns with source-of-truth, method, priority, and decisions unlocked. | Use before touching risky surfaces. |
| `EVIDENCE_MAP.csv` | Evidence catalog mapping bundle artifacts to claims, confidence, limitations, and Codex use. | Use as source routing table; inspect rows/files with JDocMunch/JDataMunch/JCodeMunch before relying on details. |
| `DECISION_MATRIX.csv` | Strategic option comparison by cost, risk, validation difficulty, impact, prerequisites, and priority. | Use for prioritization and tradeoff discussions. |
| `OPEN_QUESTIONS_FOR_USER.md` | User preference/approval questions only. | Ask/resolve only when a task needs user preference or runtime/live/commit/push approval. |
| `PACKET_MANIFEST.md` | This file. Lists packet purpose, contents, and recommended read order. | Start here when receiving the packet. |

## Recommended Read Order For Codex

1. `PACKET_MANIFEST.md`
2. `PRD.md`
3. `TECHNICAL_CONTRACTS.md`
4. `VALIDATION_AND_TEST_PLAN.md`
5. `IMPLEMENTATION_ROADMAP.md`
6. `CODEX_TASK_SLICES.md`
7. `AI_BEHAVIOR_DESIGN.md`
8. `EVIDENCE_MAP.csv`
9. `DECISION_MATRIX.csv`
10. `RESEARCH_QUESTIONS.md`
11. `OPEN_QUESTIONS_FOR_USER.md`

## Implementation Rule

Codex should not implement from the roadmap directly. It should choose a task card from `CODEX_TASK_SLICES.md`, verify inputs, execute only that slice, validate, update docs/evidence, and report live/commit/push status separately.

## Source And Evidence Warning

Large CSVs and evidence tables are catalogs. This packet cites their purpose and claims they appear to support, but Codex must use JDataMunch/JDocMunch/JCodeMunch or local file inspection for row-level conclusions.

Historical observer runs and 4.4.4 runtime evidence are useful provenance but are not current 4.4.5 standalone proof unless revalidated.

## ZIP Contents

The ZIP should contain exactly these 11 files and no generated mod code.
