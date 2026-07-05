# Stellar AI Director Load Order

Selected collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity
Required parent maximum load position: 115

## Required Position

- Load after Stellar AI.
- Load after Gigastructural Engineering & More (4.4).
- Load after NSC3.
- Load after Extra Ship Components NEXT.
- Load after Starbase Extended 3.0.
- Load after !!!Universal Resource Patch [2.4+].
- Load after parent compatibility patches whose AI/economy behavior the Director intentionally coordinates.
- Load before any future local patch that intentionally overrides the Director.

## Required Parent Evidence

| mod | present | load position |
| --- | --- | ---: |
| Stellar AI | True | 115 |
| Gigastructural Engineering & More (4.4) | True | 62 |
| NSC3 | True | 71 |
| Extra Ship Components NEXT | True | 70 |
| Starbase Extended 3.0 | True | 72 |

## Current Intentional Supersession

- `common/ai_budget/zzz_staid_alloys_budget.txt` intentionally overrides Stellar AI's `alloys_expenditure_megastructures` budget.
- `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` intentionally overrides Gigas `sentient_metal_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, and `supertensiles_upkeep_megastructures` budgets.
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt` intentionally adds/overrides `basic_economy_plan` subplans with Director late-game economy, trade-capacity, fleet-throughput, static-defense, and planetary-capacity targets.
- Additive scripted triggers, script values, and economic-plan subplans use the `staid_` namespace and should not conflict with parent object IDs.
