# Annotated Review

Source reviewed: [../stellar-ai-director-threat-response-plan.md](../stellar-ai-director-threat-response-plan.md).
Review date: 2026-07-05.

## Verdict

The source plan is directionally strong and captures the most important safety decisions: generator-owned design axes, no speculative Stellaris primitives, no forced wars in V1, unknown-war-goal inertness, opinion caps, economy caps, and protection for survival/recovery/deficit gates.

It was not yet implementation-ready because it combined design intent, implementation, tests, and acceptance criteria in one file without enough phase ownership, exact deliverables, risk treatment, runtime interaction clarifications, or handoff gates. This folder keeps the good core and expands the missing pieces into focused documents.

## Section Annotations

| Source section | Review status | Required expansion |
| --- | --- | --- |
| Summary | Good scope boundary. It correctly says V1 is diplomacy/readiness pressure and not war automation. | Add explicit deliverable IDs, non-goals, and a done definition so implementers can prove the scope is complete without expanding it. Covered in [01](01-goals-deliverables-and-acceptance.md). |
| Verified Stellaris Primitives | Good correction from prior planning. It avoids invented runtime support. | Require evidence maintenance for each primitive and define what happens if a primitive later fails launch/runtime validation. Covered in [07](07-research-and-evidence-maintenance.md). |
| Generated Files And Isolation | Good generator-first direction and clear generated output list. | Clarify owner surfaces in `tools/stellar_ai_director_lib.py`, generated-output audit coverage, and which existing file-audit folder sets must be extended. Covered in [02](02-main-implementation-plan.md). |
| Generator-Owned Data Model | Good distinction between design axes and runtime artifacts. | Add table/schema ownership, naming conventions, score limits, flag direction, and generated audit expectations. Covered in [02](02-main-implementation-plan.md) and [03](03-runtime-interaction-contract.md). |
| Personality Vectors | Good ratio requirement, especially fanatic exactly `3x`. | Add deterministic table validation, bounded civic merge rules, gestalt/homicidal routing, and scenario tests that prove caps do not hide ratio mistakes. Covered in [05](05-testing-and-validation-plan.md). |
| Score Math | Good math sketch and tier cutoffs. | Require generator-owned expected-output tests for formula equivalence, explicit clamps, tier exclusivity, and generated trigger fallback when direct script value math becomes awkward. Covered in [02](02-main-implementation-plan.md) and [05](05-testing-and-validation-plan.md). |
| War-Goal Classification | Good allowlist and unknown-war-goal inertness. | Add CSV schema, audit maintenance rules, runtime unknown behavior, source-corpus lookup order, and modded war-goal review loop. Covered in [07](07-research-and-evidence-maintenance.md). |
| Runtime Event Flow | Good single-dispatch intent and scope naming. | Clarify attacker/defender/observer roles, participants excluded from third-party observer flow, multi-attacker/multi-defender behavior, awareness rules, dedupe/cooldown flags, and performance bounds. Covered in [03](03-runtime-interaction-contract.md). |
| Opinion Effects And Caps | Good caps and mutual-exclusion intent. | Add exact modifier naming, remove-before-apply order, accumulator/decay requirements, exclusive pair state, and tests for repeated applications. Covered in [03](03-runtime-interaction-contract.md) and [05](05-testing-and-validation-plan.md). |
| Economy And Survival Guardrails | Good non-overridable survival/recovery/deficit rule. | Add third-party-only routing, `is_at_war = no` semantics, direct-victim exclusion, explicit zero-output rule, and validation for generated subplan caps. Covered in [03](03-runtime-interaction-contract.md), [04](04-risk-prevention-and-mitigation.md), and [05](05-testing-and-validation-plan.md). |
| Forced-War Restrictions | Strong safety boundary. | Convert forbidden effects into validator failures and define future punitive-war work as a separate plan with a new risk review. Covered in [04](04-risk-prevention-and-mitigation.md) and [05](05-testing-and-validation-plan.md). |
| Automated Test Matrix | Good categories. | Expand into test ownership, fixture shape, command cadence, negative-path cases, game-launch gate, and proof expectations. Covered in [05](05-testing-and-validation-plan.md). |
| Validation Commands | Correct high-level commands. | Add doc/index validation, generated artifact inspection, targeted test groups, and launch/observer prerequisites. Covered in [05](05-testing-and-validation-plan.md) and [06](06-implementation-slices-and-handoff.md). |
| Acceptance Criteria | Good user-facing outcomes. | Convert broad statements into testable deliverables with artifacts and pass/fail gates. Covered in [01](01-goals-deliverables-and-acceptance.md). |
| Assumptions | Correct, but too short for handoff. | Add source-of-truth hierarchy, compatibility assumptions, and stop conditions. Covered across [01](01-goals-deliverables-and-acceptance.md), [04](04-risk-prevention-and-mitigation.md), and [07](07-research-and-evidence-maintenance.md). |

## Missing Coverage Added

- Risk prevention and risk mitigation are separated from implementation tasks.
- Runtime interaction semantics are explicit enough to avoid accidental galaxy-wide or participant-side effects.
- The unknown-war-goal policy now includes both runtime inertness and research artifact maintenance.
- The event-flow plan now distinguishes observer state, victim state, aggressor state, country flags, and relation flags.
- The economy plan now states that third-party readiness pressure is exactly zero when safety gates fail.
- The testing plan now treats forbidden war effects, safety-gate omissions, invalid references, score ranges, fanatical ratios, and runtime-scope mistakes as validator/test failures.
- The plan now includes compatibility checks for Nomads, Arkships, Waystations, Waylines, Contracts, the 4.4 Situation Log, Gigastructural Engineering, NSC3, ship/component expansion mods, and heavy AI/economy mods when the touched surface is relevant.

## Open Design Points

These are not blockers to planning, but they must be resolved before implementation is called complete:

- The exact verified visibility/communications predicate for observer awareness must be selected from local Stellaris 4.4.4 sources before generation.
- If multi-defender handling expands beyond a representative defender, it must get a separate performance and interaction review.
- If shared-threat cooperation toward other observers is implemented, it must be bounded and tested; otherwise V1 should apply shared-threat opinion only toward the representative victim.
- If a future punitive-war or CB feature is desired, it must be a new phase with separate safety gates and cannot be smuggled into this V1 implementation.
