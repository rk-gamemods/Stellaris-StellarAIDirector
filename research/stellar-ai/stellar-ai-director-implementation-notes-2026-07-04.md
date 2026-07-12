# Stellar AI Director Implementation Notes

Generated 2026-07-04 from copied source snapshots and the selected Irony collection.

## Decision Surfaces

| surface | file | risk | reason |
| --- | --- | --- | --- |
| state gates | `common/scripted_triggers/zzz_staid_decision_state_triggers.txt` | low | additive namespaced triggers |
| unlock-research policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive economic-plan subplan reimplements parity-reference research pressure into validated modded unlock gates |
| alloy and outpost budgets | `common/ai_budget/zzz_staid_alloys_budget.txt`, `common/ai_budget/zzz_staid_outpost_budgets.txt` | medium | Director owns ship-conversion gates, keeps generic megastructure reserves with the active parent, and keeps native alloy/food outpost lanes eligible beside colonization with factor-0.25 allocation dampening |
| Gigas special-resource reserves | `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` | medium | intentional full-object overrides of Gigas megastructure special-resource budgets |
| economy targets | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | high | intentional full-object replacement of `basic_economy_plan` with high-scale Gigas/NSC3/ESC survival targets |
| fleet-throughput policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | medium | replacement economic-plan subplan maps shipyard ROI into crisis-scale alloy/energy/naval-cap targets after anti-collapse gates |
| route unlock overrides | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | high | full-object copied source overrides add Director AI weights for Mega Engineering, Mega Shipyard, Gigas, NSC3, ESC, and starbase unlock chains |
| AP/tradition category/node route overrides | `common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt`, `common/tradition_categories/zzzz_staid_02_perks_traditions_tradition_categories.txt`, `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` | medium | full-object copied source overrides preserve parent selection logic and add bounded Director route pressure to perks, categories, and selectable nodes |
| megastructure route overrides | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | high | full-object copied source overrides add Director AI weights for economy multipliers, Mega Shipyard, planetcraft, war moon, and systemcraft starts; the Gigas habitat start uniquely preserves parent scoring and replaces only the global empty-habitat veto with a bounded colonization-plan penalty |
| starbase static-defense policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt`, `common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt` | medium | additive economy reserves plus copied ESC starbase reactor AI weight support when crisis pressure is safe |
| planetary-capacity policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive economic-plan subplan raises mineral/energy, pop, and empire-size targets without building/job IDs |
| trade-capacity policy | `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`, `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive triggers and economy targets preserve Stellaris 4.4 trade logistics for ship, colony, market, and imbalance pressure |
| cap-breaker market safety | `common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt`, `events/zzz_staid_market_and_fleet_safety_events.txt` | medium | additive monthly event sells large marketable positive-income overflow using Stellar AI market value script instead of allowing capped resources to void income |
| native fleet-control restoration | `common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt`, `events/zzz_staid_market_and_fleet_safety_events.txt` | medium | the former two-pulse scripted MIA exception is removed; native mission assignment, access, and MIA behavior own active-war and post-war fleet movement |
| ROI anchors | `common/script_values/zzz_staid_roi_values.txt` | low | additive namespaced values |
| threat-response values/triggers | `common/script_values/zzz_staid_threat_response_values.txt`, `common/scripted_triggers/zzz_staid_threat_response_triggers.txt` | low | additive `staid_tr_` namespace with unknown-war-goal inertness and foreign-affairs safety gates |
| threat-response opinions/events | `common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`, `common/on_actions/zzz_staid_threat_response_on_actions.txt`, `events/zzz_staid_threat_response_events.txt` | medium | event-dispatched opinion/readiness response gated by attacker leader, awareness, participant exclusion, and forbidden-effect validation |
| integration surface ledger | `research/stellar-ai-director-integration-surfaces-2026-07-04.csv` | low | parsed source-object evidence for P6-P11 minimum interventions |

## Selected Playset

- Collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity
- Mod count: 116
- Irony patch mod enabled: True

## Required Parent Detection

| mod | present | load position |
| --- | --- | ---: |
| Gigastructural Engineering & More (4.4) | True | 62 |
| NSC3 | True | 71 |
| Extra Ship Components NEXT | True | 70 |
| Starbase Extended 3.0 | True | 72 |

## Standalone Stellar AI Parity Reference

Stellar AI is no longer a required launch dependency. Its current local source remains private parity evidence for this standalone baseline; copied or reimplemented surfaces must keep provenance notes and should not be prepared for redistribution without a later permission or rewrite pass.

| reference mod | present | load position | role |
| --- | --- | ---: | --- |
| Stellar AI | False | None | private parity/reference source, not descriptor dependency |
| Spacefleet Tactica | False | None | private parity/reference source, not descriptor dependency |

Baseline absorbed/reimplemented surfaces: AI budgets, `basic_economy_plan`, construction pressure, research/economy/fleet conversion, market/runway safety, claim/war support reserves, and high-scale modded progression hooks.

Deferred non-baseline surfaces: diplomatic-action overrides, direct ship-design/component/section handling for NSC3/ESC, executable target-specific reachability internals, and runtime observer proof. Complete 4.4.4 personality objects and native war-support budgets are now implemented.

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

Surplus is no longer treated as the only time the AI may climb. In this playset, capped marketable resources and under-curve research are strategic failures even when alloy reserves are not yet high. The replacement economic plan forces research, alloy, trade, naval-cap, and megastructure pressure on time gates, while still using survival/recovery gates to prevent immediate deficit death spirals.

## Trade-Capacity Policy

Stellaris 4.4 treats `trade` as a standard advanced resource and the market resource, but local vanilla ship-size files also use `logistics = { trade = ... }` and vanilla economic plans target trade income through intermediate, mature, and endgame stages. The Director therefore models trade as logistics/capacity headroom: it is not converted through market ROI pricing, and fleet, planet, defense, surplus, and megastructure gates require explicit trade income floors before adding more upkeep pressure.

## Market Cap-Breaker Policy

The Stellar AI parity-reference monthly market script sells only a small bounded number of surplus batches. The Director adds a late-loading monthly safety event for large positive-income overflow in resources with both a finite stockpile maximum and verified market tradability: minerals, food, consumer goods, volatile motes, exotic gases, rare crystals, Zro, dark matter, and Gigas sentient metal. Nanites, alloys, energy, unity, negative mass, and ambiguous non-market Gigas construction resources are intentionally excluded from direct forced selling.

## Stranded-Fleet Recovery Policy

The Director does not issue fleet orders. The former two-pulse `set_mia = mia_return_home` exception was intended for post-war access pockets, but its foreign-space test also matched active enemy territory and could recall an offensive fleet during homeland pressure. The exception is removed; native pathfinding, access, and MIA handling own recovery.

## Unlock-Research Policy

The Director treats modded unlock research as mandatory survival pressure. Core targets include Mega Engineering, Mega Shipyard, Gigas planetcraft/systemcraft chains, NSC3 large hull infrastructure, ESC high-tier components, and the economy techs needed to feed them. Full-object copied source overrides now add direct AI weights for those route unlocks and bounded pressure on selected AP/tradition categories and selectable nodes.

## Static-Defense Policy

Defensive starbase investment is expressed as additive `basic_economy_plan` subplans plus a copied ESC starbase reactor override. The v1 policy requires no recovery mode, no short-runway core deficit, safe alloy/energy income and stockpiles, then either defensive ethics without an aggressive under-cap fleet push or high threat pressure.

## Planetary-Capacity Policy

Expanded planet and building capacity is covered through safe country-level economic-plan demand. Research demand is enabled only behind consumer-goods, energy, and deficit runway gates; vanilla research-zone eligibility remains the hard construction boundary. More Arcologies naval buildings use explicit AI eligibility that excludes research-designated worlds.

## NSC3/ESC Design Policy

NSC3 and ESC unlock usage now has direct technology AI-weight overrides plus fleet-throughput economy pressure. ESC internal component-template `key = ...` entries and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.

## Threat-Response Policy

The V1 threat-response feature adds observer opinion, timed flags, and a capped third-party defensive-readiness economy subplan for classified observed aggression. `wg_conquest`, `wg_subjugation`, and `wg_humiliation` are the initial allowlist; unknown war goals stay inert until evidence, severity, output expectations, tests, and validator coverage are added. The generated event path must not declare wars, join wars, add casus belli, force `wg_*` dispatch, or override diplomatic actions.

`source_has_ai_weight` records whether the parent mod file had an upstream AI weight. It does not mean the Director has no policy. Director policy is recorded separately as `director_strategy_role`, `director_weight_basis`, `director_build_gate`, `director_surplus_sink_role`, and `director_surplus_sink_priority` in the ROI matrix.

## v1 Boundaries

- Direct technology/AP/tradition category/node object overrides are emitted from copied source objects for the supported high-scale route families; automatic adoption/finish rewards remain untouched.
- Direct Mega Shipyard, economy megastructure, planetcraft, war moon, and systemcraft object weights are emitted from copied source objects and paired with economy/reserve gates.
- Direct starbase support includes copied ESC starbase reactor AI weight plus country-level static-defense economy targets.
- Research infrastructure uses safe economic-plan demand plus vanilla research-zone eligibility; inactive building `ai_weight` is not treated as the primary construction planner.
- ESC internal component-template `key = ...` overrides and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.
- Exotic Gigas superprojects remain outside the main decision path until the core reserve/commit/payoff loop is observer-tested, but their special-resource budget objects are gated by Director survival/recovery state.
