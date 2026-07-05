# Stellar AI Director Implementation Notes

Generated 2026-07-04 from copied source snapshots and the selected Irony collection.

## Decision Surfaces

| surface | file | risk | reason |
| --- | --- | --- | --- |
| state gates | `common/scripted_triggers/zzz_staid_decision_state_triggers.txt` | low | additive namespaced triggers |
| unlock-research policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive economic-plan subplan extends Stellar AI research pressure into validated modded unlock gates |
| alloy reserves | `common/ai_budget/zzz_staid_alloys_budget.txt` | medium | intentional full-object override of Stellar AI megastructure budget |
| Gigas special-resource reserves | `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` | medium | intentional full-object overrides of Gigas megastructure special-resource budgets |
| economy targets | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | medium | intentional full-object override of `basic_economy_plan` with Director economy targets |
| fleet-throughput policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive economic-plan subplan maps shipyard ROI into alloy/energy/naval-cap targets after anti-collapse gates |
| starbase static-defense policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive economic-plan subplans reserve alloy/energy income when defensive strategy or crisis pressure is safe |
| planetary-capacity policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive economic-plan subplan raises mineral/energy, pop, and empire-size targets without building/job IDs |
| ROI anchors | `common/script_values/zzz_staid_roi_values.txt` | low | additive namespaced values |
| threat-response values/triggers | `common/script_values/zzz_staid_threat_response_values.txt`, `common/scripted_triggers/zzz_staid_threat_response_triggers.txt` | low | additive `staid_tr_` namespace with unknown-war-goal inertness and foreign-affairs safety gates |
| threat-response opinions/events | `common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`, `common/on_actions/zzz_staid_threat_response_on_actions.txt`, `events/zzz_staid_threat_response_events.txt` | medium | event-dispatched opinion/readiness response gated by attacker leader, awareness, participant exclusion, and forbidden-effect validation |
| integration surface ledger | `research/stellar-ai-director-integration-surfaces-2026-07-04.csv` | low | parsed source-object evidence for P6-P11 minimum interventions |

## Selected Playset

- Collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity
- Mod count: 119
- Irony patch mod enabled: True

## Required Parent Detection

| mod | present | load position |
| --- | --- | ---: |
| Stellar AI | True | 114 |
| Gigastructural Engineering & More (4.4) | True | 61 |
| NSC3 | True | 70 |
| Extra Ship Components NEXT | True | 69 |
| Starbase Extended 3.0 | True | 71 |

## Generated ROI Thresholds

These values are generated from rows where `data_quality = resolved` and `decision_eligible = yes`.

| threshold | value |
| --- | ---: |
| prep_stockpile_alloys | 15000 |
| prep_income_alloys | 130 |
| commit_stockpile_alloys | 27000 |
| desired_base_alloys | 25000 |
| desired_mega_engineering_add | 50000 |
| desired_prep_add | 75000 |
| desired_commit_add | 100000 |
| shipyard_stockpile_alloys | 12000 |
| shipyard_income_alloys | 150 |
| eligible_roi_rows | 140 |

## Surplus Sink Policy

When survival and recovery gates are clear, surplus pressure is approximated from strong monthly alloy/energy income plus a large alloy stockpile. The v1 scripted ordering is research sink first, fleet-production sink second, and unity sink third. Fleet-throughput policy now maps shipyard readiness into alloy, energy, and naval-cap economic-plan targets while blocking over-naval-cap upkeep spirals.

## Unlock-Research Policy

Research-heavy Stellar AI behavior is preserved and extended with a country-level economic-plan subplan for core modded unlocks. Direct technology/AP/tradition object overrides are deferred in v1; every emitted technology reference is checked by the generated reference audit.

## Static-Defense Policy

Defensive starbase investment is expressed as additive `basic_economy_plan` subplans because vanilla economic plans explicitly merge subplans safely. The v1 policy requires no recovery mode, no short-runway core deficit, safe alloy/energy income and stockpiles, then either defensive ethics without an aggressive under-cap fleet push or high threat pressure. Direct starbase module/building weights remain deferred until a safe parent surface can be proven for each object.

## Planetary-Capacity Policy

Expanded planet and building capacity is covered in v1 through a safe country-level economic-plan subplan, not direct building or job references. The policy raises mineral/energy, pop, and empire-size targets only when recovery and short-runway deficit gates are clear.

## NSC3/ESC Design Policy

Direct NSC3/ESC ship and component design overrides are deferred until observer evidence shows parent AI weights cannot use the new hulls or components. The P11 integration audit must have no failed rows; warning rows are tracked as parent-design gaps rather than automatic override targets.

## Threat-Response Policy

The V1 threat-response feature adds observer opinion, timed flags, and a capped third-party defensive-readiness economy subplan for classified observed aggression. `wg_conquest`, `wg_subjugation`, and `wg_humiliation` are the initial allowlist; unknown war goals stay inert until evidence, severity, output expectations, tests, and validator coverage are added. The generated event path must not declare wars, join wars, add casus belli, force `wg_*` dispatch, or override diplomatic actions.

`source_has_ai_weight` records whether the parent mod file had an upstream AI weight. It does not mean the Director has no policy. Director policy is recorded separately as `director_strategy_role`, `director_weight_basis`, `director_build_gate`, `director_surplus_sink_role`, and `director_surplus_sink_priority` in the ROI matrix.

## v1 Boundaries

- Direct technology/AP/tradition object overrides are deferred in v1. The unlock-research policy uses validated country-level economy-plan targets instead.
- Direct Mega Shipyard object weights remain deferred unless a safe parent object surface is proven; v1 maps the payoff through country-level economy-plan targets and source ROI evidence.
- Direct starbase module/building weights remain deferred; v1 uses a country-level static-defense economy target rather than overriding Starbase Extended objects.
- Direct planet building/job overrides are not emitted in v1; no generated building/job references are used.
- Direct NSC3/ESC ship and component design overrides are deferred until observer evidence proves parent AI cannot use the new hulls or components.
- Exotic Gigas superprojects remain outside the main decision path until the core reserve/commit/payoff loop is observer-tested, but their special-resource budget objects are gated by Director survival/recovery state.
