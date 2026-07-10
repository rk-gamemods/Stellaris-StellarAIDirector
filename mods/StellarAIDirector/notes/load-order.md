# Stellar AI Director Load Order

Selected collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity
Required compatibility-mod maximum load position: 72

## Required Position

- Load after Gigastructural Engineering & More (4.4).
- Load after NSC3.
- Load after Extra Ship Components NEXT.
- Load after Starbase Extended 3.0.
- Load after Planetary Diversity and Planetary Diversity - More Arcologies when those collection surfaces are active.
- Load after !!!Universal Resource Patch [2.4+].
- Load after compatibility patches whose AI/economy behavior the Director intentionally coordinates.
- Stellar AI is not a required parent for the standalone baseline; keep it only as private parity/reference evidence when comparing behavior during development.
- Load before any future local patch that intentionally overrides the Director.

## Required Compatibility Evidence

| mod | present | load position |
| --- | --- | ---: |
| Gigastructural Engineering & More (4.4) | True | 62 |
| NSC3 | True | 71 |
| Extra Ship Components NEXT | True | 70 |
| Starbase Extended 3.0 | True | 72 |

## Stellar AI Standalone Parity

The Director descriptor intentionally omits Stellar AI. Current Stellar AI source is a private local parity reference only; its high-value AI budget, economic-plan, construction-pressure, research/economy/fleet conversion, and war-support surfaces are absorbed or reimplemented by Director-owned generated files.

| reference mod | present | load position | role |
| --- | --- | ---: | --- |
| Stellar AI | False | None | private parity/reference source, not descriptor dependency |
| Spacefleet Tactica | False | None | private parity/reference source, not descriptor dependency |

## Current Intentional Supersession

- `common/ai_budget/zzz_staid_alloys_budget.txt` intentionally defines the Director-owned `alloys_expenditure_megastructures` budget using Stellar AI parity evidence without requiring Stellar AI to load.
- `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` intentionally overrides Gigas `sentient_metal_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, and `supertensiles_upkeep_megastructures` budgets.
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt` intentionally replaces `basic_economy_plan` with Director high-scale survival economy, mandatory modded unlock research, trade-capacity, fleet-throughput, static-defense, and planetary-capacity targets.
- `common/buildings/zzzz_staid_13_dataset_job_pressure_buildings.txt` maps selected nonmilitary parent buildings to `ai_resource_production`; military-capacity objects are excluded from this generated pressure path.
- `common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt` narrowly overrides More Arcologies naval administration buildings with AI strategic-readiness and research-world exclusion gates.
- Additive scripted triggers, script values, and economic-plan subplans use the `staid_` namespace and should not conflict with parent object IDs.
