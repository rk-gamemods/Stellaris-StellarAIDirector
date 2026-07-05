# Goals, Deliverables, And Acceptance

## Objective

Implement a bounded Stellar AI Director V1 threat-response layer that reacts to observable aggressive wars through diplomatic opinion, timed flags, and tightly capped third-party defensive-readiness economy pressure.

## Current Gap

The existing Stellar AI Director work improves economic, megastructure, starbase, and fleet-throughput behavior, but it does not yet add a generator-owned threat-response layer for observed aggression. The source plan defines the desired behavior, but implementation needs testable deliverables, phase gates, risk controls, and runtime interaction rules.

## Non-Goals

V1 must not:

- declare wars;
- join wars;
- add punitive casus belli;
- overwrite diplomatic actions;
- force `wg_*` dispatch;
- make direct self-defense decisions for attacked empires;
- bypass `staid_core_deficit_short_runway`, `staid_survival_mode`, or `staid_recovery_mode`;
- apply punitive effects for unknown or unclassified war goals;
- treat generator-owned axes as native Stellaris runtime concepts.

## Source Of Truth

Use sources in this order:

1. Current user instruction and this plan set.
2. [../stellar-ai-director-threat-response-plan.md](../stellar-ai-director-threat-response-plan.md).
3. Current repo rules in `AGENTS.md`.
4. Existing Director generator and tests in `tools/stellar_ai_director_lib.py` and `tools/tests/test_stellar_ai_director.py`.
5. Current local Stellaris 4.4.4 files, source snapshots, generated research artifacts, CWTools/Irony output, and launch logs.
6. Open Brain memory only as advisory history.

## Deliverables

| ID | Deliverable | Expected output | Acceptance check |
| --- | --- | --- | --- |
| D1 | Generator-owned threat model | Constants/tables in `tools/stellar_ai_director_lib.py` for axes, ethics, gestalt paths, civic caps, score limits, tier cutoffs, flag durations, and economy caps. | Unit tests prove normal/fanatic ratios, range limits, civic caps, and stable exported table shape. |
| D2 | War-goal classification model | `WAR_GOAL_THREAT_CLASSES` table and `research/stellar-ai/stellar-ai-director-threat-response-war-goal-classification-2026-07-05.csv`. | Known allowlisted goals resolve to severity; unknown goals resolve to severity `0` and inert outputs; CSV records source/evidence/status. |
| D3 | Generated script values and triggers | `common/script_values/zzz_staid_threat_response_values.txt` and `common/scripted_triggers/zzz_staid_threat_response_triggers.txt`. | Generated files parse, names use `staid_tr_`, score ranges clamp correctly, and safety gates appear where required. |
| D4 | Generated opinion modifiers and localization | `common/opinion_modifiers/zzz_staid_threat_response_opinions.txt` and `localisation/english/staid_threat_response_l_english.yml`. | Opinion keys exist, modifiers have decay/cap behavior, lower tiers are removed before higher tiers, and visible keys localize. |
| D5 | Generated on-action and event flow | `common/on_actions/zzz_staid_threat_response_on_actions.txt` and `events/zzz_staid_threat_response_events.txt`. | Event namespace is `staid_tr`; dispatch is once per attacker war leader; participant and awareness gates are present; forbidden effects are absent. |
| D6 | Defensive-readiness economy pressure | A generated, capped third-party economy path integrated with existing Director economic-plan surfaces. | Economy pressure is exactly zero when foreign-affairs safety fails and never exceeds `20%` of existing fleet-throughput reserve values. |
| D7 | Validator extensions | `validate_generated_patch()` covers threat-response generated files, references, ranges, ratios, forbidden effects, safety gates, and audit artifacts. | `python tools/validate_stellar_ai_director_patch.py` fails on each seeded threat-response contract violation and passes on the generated patch. |
| D8 | Test coverage | Focused tests in `tools/tests/test_stellar_ai_director.py`. | `python -m unittest tools.tests.test_stellar_ai_director` covers D1-D7, including negative paths and scenario matrix cases. |
| D9 | Research and evidence artifacts | Feasibility note and classification CSV under `research/stellar-ai/`, plus tuning notes updates. | Artifacts state target game version, inspected sources, compatibility risks, test steps, open questions, and generated file ownership. |
| D10 | Documentation updates | `mods/StellarAIDirector/README.md`, `mods/StellarAIDirector/notes/tuning-notes.md`, and plan status docs updated as needed. | Docs describe the feature, generated files, known conflicts, tested game version, non-goals, and remaining runtime risks. |
| D11 | Runtime smoke evidence | Launch/main-menu proof first, then observer-game smoke after automated validation passes. | No new Director problem lines in logs, generated files load, and observer-game notes confirm no forced wars or economy collapse symptoms. |

## Acceptance Criteria

The implementation is acceptable only when all of these are true:

- Threat response produces diplomatic consequences for classified observed aggression.
- Different ethics, civics, and gestalt paths produce materially different generated decisions.
- Fanatic ethics preserve exact `3x` normal-weight ratios before caps.
- Unknown and unclassified war goals are inert until intentionally classified.
- Third-party struggling empires receive no threat economy pressure.
- Third-party threat economy pressure cannot exceed the declared ratio cap.
- Survival/recovery/deficit gates cannot be bypassed by personality logic.
- V1 generated files contain no forced-war, join-war, punitive-CB, or diplomatic-action override path.
- Automated tests and validator checks cover every non-game-launch behavior.
- Manual/runtime launch and observer checks are performed only after deterministic validation passes.

## Out Of Scope For This Plan Set

- Balancing final opinion values after long observer-game campaigns.
- Supporting Stellaris 4.4.5 beta, 4.5 beta, or later script changes.
- Making the AI start containment wars or issue punitive CBs.
- Building UI around threat state.
- Reworking the existing ROI, megastructure, starbase, or fleet-throughput Director model except where the new threat economy cap integrates with it.
