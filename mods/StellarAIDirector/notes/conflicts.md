# Stellar AI Director Conflict Notes

## Intentional Conflicts

- `common/ai_budget/zzz_staid_alloys_budget.txt` does not replace upstream `alloys_expenditure_megastructures`; the active parent retains generic reserve ownership while Director object weights rank specific legal projects.
- `common/ai_budget/zzz_staid_outpost_budgets.txt` intentionally replaces vanilla `alloys_expenditure_starbases_expand` and `food_expenditure_starbases_expand`. It preserves native expansion-plan, threat, influence, biological-ship, wilderness-terraform, weight, and desired-min behavior; only colonization-plan eligibility becomes a factor-0.25 weight preference, and the alloy object's ambiguous multi-statement `NOT` becomes the explicit `NOR` used by its food analogue.
- `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` intentionally replaces upstream Gigas special-resource megastructure budget objects: `sentient_metal_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, and `supertensiles_upkeep_megastructures`.
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt` intentionally replaces `basic_economy_plan` with Director high-scale survival economy, mandatory modded unlock research, trade-capacity, fleet-throughput, static-defense, and planetary-capacity targets; despite the historical filename, conflict review must treat it as a Director-owned economic-plan surface.
- `common/technology/zzzz_staid_01_unlock_technology_technology.txt` intentionally replaces copied vanilla/Gigas/NSC3/ESC/Starbase Extended technology objects with Director route AI weights.
- `common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt`, `common/tradition_categories/zzzz_staid_02_perks_traditions_tradition_categories.txt`, and `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` intentionally replace copied AP/category/selectable-node objects with bounded Director route AI weights; automatic adoption/finish rewards are not overridden.
- `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` intentionally replaces copied Gigas/vanilla-compatible megastructure starts for economy multipliers, Mega Shipyard, planetcraft, war moon, and systemcraft priority.
- `common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt` intentionally replaces copied ESC starbase reactor support with Director crisis-starbase pressure.
- `common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt` narrowly replaces More Arcologies `building_navel_base` and `building_navel_command` so AI naval-capacity construction requires strategic readiness and cannot consume research-world slots.

## Expected Additive Surfaces

- `common/economic_plans/zzzz_staid_21_strategic_resource_deficit_recovery.txt` (three unique optional, non-scaling, actual-deficit-only +1 subplans; no strategic-resource object override)
- `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`
- `common/script_values/zzz_staid_roi_values.txt`
- `common/scripted_triggers/zzz_staid_threat_response_triggers.txt`
- `common/script_values/zzz_staid_threat_response_values.txt`
- `common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt`
- `events/zzz_staid_market_and_fleet_safety_events.txt`
- `common/on_actions/zzzz_staid_boss_defeat_escalation_on_actions.txt`
- `events/zzzz_staid_boss_defeat_escalation_events.txt`
- `common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`
- `common/on_actions/zzz_staid_threat_response_on_actions.txt`
- `events/zzz_staid_threat_response_events.txt`
- `localisation/english/staid_threat_response_l_english.yml`

## Threat-Response Boundaries

- V1 threat response is diplomacy/readiness pressure only.
- Unknown or unclassified war goals are inert until manually classified and tested.
- Generated threat-response files must not declare wars, join wars, add casus belli, or override diplomatic actions.
- Third-party readiness economy pressure must remain behind `staid_tr_foreign_affairs_safe`.

## NSC3/ESC Design Policy

- NSC3 and ESC unlock technologies now have copied source-object route AI weights.
- Fleet-throughput economy gates provide the current ship-use path without guessing direct ship-design templates.
- The residual ESC readiness subplan is optional and non-scaling and does not target volatile motes, exotic gases, or rare crystals; those resources use separate actual-deficit-only +1 subplans.
- Vanilla and parent mods retain producer eligibility and ordinary strategic-resource object ownership.
- ESC internal component-template `key = ...` overrides and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.

## Strategic V2 Compatibility Reviews

- Starbase Extended review: Director-owned starbase defense pressure is limited to copied safe module/building surfaces and generated economy gates. Parent-owned Waystation sections, ship sizes, component templates, and related starbase/ship loader surfaces remain out of scope because the active conflict matrix shows high-risk parent conflicts there.
- Planetary Diversity / More Arcologies review: `building_navel_base` and `building_navel_command` use narrow hard AI eligibility, not dataset weight pressure. `building_pd_rogue_council`, More Arcologies zones, and broad colony/designation rewrites remain blocked until their AI, UI, and load-order semantics are proven.
- Nomad/Arkship review: Director has one additive targeted opening route for Arkship research and otherwise keeps high-scale pressure normal-empire-only. It does not override Nomad colony types, Arkship ship sizes, Arkship component templates, Waystation sections, Waylines, Contracts, or Operational Reserve objects.

## Review Rules

- Any new full-object override must include an ownership note naming the parent surface and reason.
- Optional-mod references must be omitted or guarded unless the generator proves the referenced object exists.
- Irony conflict results should be classified as intentional Director wins, parent wins required, harmless additive duplicates, unexpected gameplay conflicts, or false positives.

## Irony Analyze Only Review

- Reviewed in Irony Conflict Solver Analyze Only for collection `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`.
- Existing collection order was preserved; `Stellar AI Director` is the only added local mod and is last after `!!!Universal Resource Patch [2.4+]`.
- Reviewed `common\ai_budget` conflicts: `negative_mass_expenditure_megastructures`, `sentient_metal_expenditure_megastructures`, and `supertensiles_upkeep_megastructures`.
- Each reviewed object resolves to `Stellar AI Director ... (LIOS)` as an intentional Director win.
- No unexplained Director gameplay conflicts were observed in the reviewed Director conflict set.
- Fresh Irony UI review has not yet been repeated for the strategic v2 starbase and Planetary Diversity surfaces; current classifications are based on generated audits and indexed active conflict-matrix evidence.
