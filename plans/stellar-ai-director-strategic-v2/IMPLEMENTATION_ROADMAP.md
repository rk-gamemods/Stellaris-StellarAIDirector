# Stellar AI Director V2 Implementation Roadmap

Generated: 2026-07-08
Packet: Stellar AI Director Strategic V2 Roadmap Packet
Target: Stellaris PC 4.4.5 stable/current, backwards compatible with 4.4.4 where source-backed


## Strategic Sequencing

The next phase must be staged so Codex does not jump from "AI is weak" to speculative high-risk overrides. The roadmap is ordered by leverage and safety:

1. Stabilize current 4.4.5 standalone baseline.
2. Harden evidence and validators.
3. Fix first-75-year compounding economy/research trajectory.
4. Improve diplomacy/unity/fleet payoff only through safe surfaces.
5. Build source-verified lanes for risky modded ship/war/Gigas behavior.
6. Package, document, and optionally observer-test with explicit approval.

## Phase 0 - Baseline Re-Orientation And Source Freshness

| Field | Plan |
| --- | --- |
| Purpose | Prevent Codex from implementing against stale 4.4.4 observer evidence, archived launch notes, or the old Stellar AI dependency frame. |
| Work type | Research / validation prep. |
| Expected files | `research/stellar-ai/stellar-ai-director-4-4-5-compatibility-triage-2026-07-08.md`, `standalone-baseline-cleanup`, `standalone-parity-inventory`, `mods/StellarAIDirector/README.md`, `notes/load-order.md`. |
| Key tasks | Verify target version wording, standalone dependency wording, required parents, active-source roots, Munch/JData/JDoc/JCode freshness, and current generated artifact list. |
| Risks | Treating historical observer runs as current proof; treating source mod as live mod; missing 4.4.5 patch-surface changes. |
| Validation | Stale wording search; descriptor check; generated artifact inventory; source-manifest refresh if repo changed. |
| Exit criteria | Codex can state current baseline, required parents, deferred gaps, and validation commands without guessing. |

## Phase 1 - Static Validation And Evidence Infrastructure

| Field | Plan |
| --- | --- |
| Purpose | Make it hard for future slices to silently break references, generated objects, conflict assumptions, or folder contracts. |
| Work type | Validation / tooling. |
| Expected files | `tools/stellar_ai_director_lib.py`, `tools/validate_stellar_ai_director_patch.py`, `tools/tests/test_stellar_ai_director.py`, generated file/reference/conflict/integration audits. |
| Key tasks | Expand validator coverage for forbidden folders, stale dependencies, generated source comments, 4.4.5 risk patterns, route object existence, and no direct ship template emission. |
| Risks | Overfitting tests to current tuning values; letting validator depend on runtime outcomes. |
| Validation | Generator, validator, py_compile, full unit suite, file/reference/conflict audit refresh, `git diff --check`. |
| Exit criteria | Validator fails on seeded broken contracts and passes on generated outputs. |

## Phase 2 - 4.4.5 Compatibility Hardening

| Field | Plan |
| --- | --- |
| Purpose | Address the current 4.4.5 risk posture before adding strategy complexity. |
| Work type | Research / validation / compatibility triage. |
| Expected files | New or updated `research/stellar-ai/stellar-ai-director-4-4-5-compatibility-triage-*.md`, log-risk classifier, optional active-stack issue matrix. |
| Key tasks | Classify remaining load-freeze/log patterns: Gigas orbital/frameworld references, ESC/ship-size deferred reads, invalid `uses_ship_category` scope, portrait `has_job`, Gigas GUI/asset warnings, and any Director-owned residual issues. |
| Risks | Confusing parent-mod warnings with Director-owned defects; applying patches to parent content without scope. |
| Validation | Static log summary parser; no generated zones resurrection; no unsupported economic-plan targets; starbase-module duplicate block tests; optional Irony Analyze Only. |
| Exit criteria | Codex knows which issues are Director-owned, parent-owned, compatibility-patch candidates, or runtime-only warnings. |

## Phase 3 - Opening Economy And Research Compounding V2

| Field | Plan |
| --- | --- |
| Purpose | Fix the highest-leverage failure: AI arrives too late to research, megastructure, and crisis-prep routes. |
| Work type | Implementation / validation. |
| Expected files | `common/scripted_triggers/zzzz_staid_10_opening_strategy_triggers.txt`, `common/economic_plans/zzzz_staid_additive_economic_plan.txt`, `common/buildings/*research*`, `common/districts/*research*`, `common/technology/*`, `common/policies/*`, `common/edicts/*`, generator/tests. |
| Key tasks | Refine route triggers; strengthen early research world and lab pressure; active pop assembly/growth pressure; preserve support economy; avoid unstaffed job spam; add validation for support-resource gates. |
| Risks | Overbuilding labs without CG/energy; starving alloy defenses; overriding parent automation too broadly; breaking Nomad/Arkship cases. |
| Validation | Unit tests for route triggers and generated weights; economic-plan parse; no invalid references; non-runtime metrics documented but not tested. |
| Exit criteria | Static artifacts show a coherent first-75-year economy/research book that is safe for regular, hive, machine, and relevant Nomad contexts. |

## Phase 4 - Research Diplomacy And Unity-To-Research

| Field | Plan |
| --- | --- |
| Purpose | Make non-genocidal research/economy AI more likely to convert diplomacy and unity into research tempo without unsafe diplomatic-action rewrites. |
| Work type | Research-first implementation. |
| Expected files | `common/federation_types/zzzz_staid_15_research_diplomacy_federation_types.txt`, traditions/AP files, policies, edicts, research notes. |
| Key tasks | Preserve Research Cooperative weighting; research safe prerequisites for research agreements; improve diplomacy tradition and compatible policy/edict routes; do not generate `common/diplomatic_actions` or `common/personalities` until proven. |
| Risks | Research agreements depend on trust/opinion/embassy/diplomacy gates; personality overrides are full-object conflict-heavy. |
| Validation | Tests confirm no unsafe diplomacy/personality folders; generated federation/tradition/AP weights parse; source note explains gated research-agreement status. |
| Exit criteria | Safe research diplomacy routes are implemented; unsafe agreement/personality work remains explicit research question. |

## Phase 5 - Modded Progression Route Mastery

| Field | Plan |
| --- | --- |
| Purpose | Ensure AI can pursue prerequisite chains for Mega Engineering, Mega Shipyard, Gigas economy megastructures, planetcraft, war moons, systemcraft, NSC3 hulls, and ESC component tiers. |
| Work type | Implementation / research. |
| Expected files | `common/technology/`, `common/ascension_perks/`, `common/traditions/`, `common/megastructures/`, route reports, object atlas. |
| Key tasks | Refresh route graph; identify missing prerequisites; treat special resources as first-class bottlenecks; add safe object-specific weights only where policy rows exist; preserve parent AI where complete. |
| Risks | Late-game weights cannot compensate for early deficits; event/script gates may hide prerequisites; Gigas settings can alter build caps/resources. |
| Validation | Object atlas, dependency edges, policy matrix, parent AI support map, route reports, generated reference audit. |
| Exit criteria | Static route graph explains how an AI gets from 2200 economy to high-scale modded objects and what blockers remain. |

## Phase 6 - Fleet Payoff And War-Support Behavior

| Field | Plan |
| --- | --- |
| Purpose | Convert fleet investment into useful outcomes while preserving survival/recovery/deficit safety. |
| Work type | Implementation / research. |
| Expected files | fleet-throughput economic plans, bombardment stance weights, threat-response files, war-mechanics research notes. |
| Key tasks | Strengthen militarist/conquest/raiding payoff routes; identify cheap hostile-fauna clearance targets; reserve fleet only when it buys territory/pops/subjects/survival/crisis readiness; keep non-militarists research/economy focused. |
| Risks | War declaration/CB/join-war surfaces are dangerous; fleet can starve economy; hostile fauna target difficulty may be unknown. |
| Validation | Forbidden-effect scan; threat-response tests; route tests; hostile-fauna inventory remains gated until fleet power/reward data exists. |
| Exit criteria | Fleet pressure is payoff-gated and no forced-war behavior exists in core V2. |

## Phase 7 - NSC3 / ESC Ship-Stack Research Lane

| Field | Plan |
| --- | --- |
| Purpose | Build the evidence needed before direct ship-design/component/section/ship-size handling. |
| Work type | Research / validation / report generation. |
| Expected files | New `research/stellar-ai/stellar-ai-director-nsc3-esc-ship-stack-lane-*.md`, possible CSV graph, `ship-design-reference-checks`, active winning objects. |
| Key tasks | Map ship sizes, sections, components, component sets, templates, prerequisites, resources, AI weights, and load winners for NSC3 + ESC NEXT. Identify what can be supported through tech/resource/economy only and what requires direct overrides. |
| Risks | Loader behavior for component-template `key = ...` and direct ship designs is not safely modeled; ship graph conflicts can be high. |
| Validation | JDataMunch/JCodeMunch graph checks; no generated direct overrides from the research task itself. |
| Exit criteria | Codex can propose a minimal safe ship-stack implementation or explicitly keep direct handling deferred. |

## Phase 8 - Gigas Queue Continuation And Megastructure Runtime-Proof Lane

| Field | Plan |
| --- | --- |
| Purpose | Move from static route weights to proof that AI queues, upgrades, and sequences high-value Gigas chains. |
| Work type | Research / optional runtime-support tooling. |
| Expected files | Gigas queue report, save-inspection helpers, route blocker report, tuning notes. |
| Key tasks | Identify build/upgrade chain blockers, site limits, settings-driven disable flags, special resource runway, megaconstruction/supertensiles behavior, and event/script gates. |
| Risks | Queue continuation is not provable by static weights alone; runtime/save evidence may be needed. |
| Validation | Static chain graph first; optional approved save/observer extraction later. |
| Exit criteria | Static blocker report exists; runtime optimization claims remain withheld until approved evidence. |

## Phase 9 - Starbase, Defense, And Crisis Readiness

| Field | Plan |
| --- | --- |
| Purpose | Make AI defense investment useful against high-scale threats without turning wars into stagnant tower-defense or starving research. |
| Work type | Implementation / compatibility. |
| Expected files | Starbase module/building generated files, starbase scope report, policies/tech/economic plans, crisis response research. |
| Key tasks | Expand Starbase Extended AI support where verified; route static defense through threat/capacity/economy gates; research crisis detection surfaces; document planet-defense and bombardment-resistance interactions. |
| Risks | Starbase mods conflict through ship sizes/modules/buildings; overdefense can waste economy; crisis triggers may be hidden. |
| Validation | Starbase files parse; Irony conflicts classified; no unsupported scopes; optional runtime only after approval. |
| Exit criteria | Defense weights are source-backed and tied to risk, economy, and crisis posture. |

## Phase 10 - Colony, Planetary Diversity, And Designation Breadth

| Field | Plan |
| --- | --- |
| Purpose | Expand beyond targeted Planetary Diversity/outpost support only where evidence shows gaps. |
| Work type | Research-first implementation. |
| Expected files | PD profile, colony/designation inventory, building/district datasets, generated decision/building/district files. |
| Key tasks | Identify high-value PD worlds/buildings/districts; avoid broad designation rewrites; add targeted rules for clear ROI and safe support resources; include Nomad/Arkship cases when touched. |
| Risks | Broad colony/designation rewrites can fight vanilla automation and modded planet types. |
| Validation | Dataset row inspection, generated file audit, reference audit, route policy rationale. |
| Exit criteria | Any new planet logic is targeted, source-backed, and safe-gated. |

## Phase 11 - Packaging, Documentation, And Release Hygiene

| Field | Plan |
| --- | --- |
| Purpose | Make the mod understandable, launchable, and safely handoffable without confusing source, live launcher, commit, and push states. |
| Work type | Packaging / documentation / validation. |
| Expected files | README, descriptor, load-order notes, conflicts, tuning notes, observer log, research status, generated audits. |
| Key tasks | Refresh docs; verify live descriptor and `dlc_load.json`; verify observer harness status; update validation status; stage only coherent changes. |
| Risks | Untracked generated/research files pollute commit; live launcher state drifts; old docs imply Stellar AI dependency. |
| Validation | Standard static commands; live descriptor check; git status; remote status if pushing. |
| Exit criteria | Codex reports live mod/commit/push status separately. |

## Phase 12 - Optional User-Approved Observer Loop

| Field | Plan |
| --- | --- |
| Purpose | Measure whether V2 actually improves AI behavior over time. |
| Work type | Runtime / observer validation. |
| Expected files | New observer-run folder, metadata, manual notes, checkpoints, metrics, summary, log summaries, screenshots/saves if approved. |
| Key tasks | Confirm approval; status-check `commands_at_date.txt`; launch through Irony; record settings; collect 2250/2300/2325/2350 checkpoints; parse save metrics; compare to hypotheses; disable observer commands after run. |
| Risks | Runtime tests are slow, settings-sensitive, and not deterministic enough for unit tests. |
| Validation | Error log first, game log second, checkpoint CSVs, summary; stop conditions for crash/freeze/event spam/economy collapse. |
| Exit criteria | Observer evidence says what improved, what failed, and what next slice should address. |

## Strategic Phase Dependencies

```text
Phase 0 -> Phase 1 -> Phase 2 -> Phase 3
Phase 3 -> Phase 4, Phase 5, Phase 6
Phase 5 -> Phase 7, Phase 8
Phase 6 -> Phase 9
Phase 3/10 can iterate in parallel after validation gates
Phase 11 after any coherent implementation slice
Phase 12 only with explicit user approval after Phase 11 static readiness
```

## Biggest Strategic Risks

| Risk | Mitigation |
| --- | --- |
| The AI remains underpowered even after static improvements. | Observer targets are optional approval-gated metrics; use checkpoint deltas to guide next slice. |
| Codex implements unsafe overrides too early. | Hard gates for diplomacy/personality/ship/Gigas/war surfaces. |
| Parent mods change under 4.4.5. | Refresh source snapshots, active-stack inventories, and conflict reports before each risky slice. |
| More weights create worse economy. | Support-resource and unstaffed-job gates; separate tuning targets from tests. |
| Compatibility breaks with major mods. | Irony Analyze Only and generated audits before live claims. |
| Runtime proof is overstated. | Docs must distinguish static proof, launch proof, save proof, and observer proof. |
