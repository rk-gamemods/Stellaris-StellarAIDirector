# Stellar AI Director 4.4.5 Nomad/Arkship Compatibility Audit

Date: 2026-07-09

Task: T26 - 4.4.5 Nomad/Arkship compatibility audit

## Scope

This audit classifies Stellar AI Director strategic v2 surfaces touched through T25 against Stellaris 4.4.5 Nomads, Arkships, Waystations, Waylines, Contracts, and Operational Reserves. It is a static compatibility audit only; no runtime observer claim is made here.

## Sources

- `stellaris_packet_object_definitions_20260708`
- `stellaris_packet_active_load_order_conflicts_20260708`
- `stellar_ai_director_generated_file_audit_20260704`
- `stellar_ai_director_generated_reference_audit_20260704`
- `stellar_ai_director_generated_conflicts_20260704`
- Current generated files under `mods/StellarAIDirector/common`
- Local vanilla Stellaris 4.4.5 files under `C:\Steam\steamapps\common\Stellaris\common`

## Vanilla And Active-Stack Nomad Surface

Indexed object definitions show a broad 4.4 Nomad surface:

| Surface | Matching objects |
| --- | ---: |
| `ai_budget` | 9 |
| `colony_types` | 19 |
| `component_sets` | 27 |
| `component_templates` | 35 |
| `districts` | 1 |
| `global_ship_designs` | 2 |
| `megastructures` | 8 |
| `on_actions` | 35 |
| `section_templates` | 32 |
| `ship_sizes` | 16 |
| `starbase_buildings` | 59 |
| `starbase_modules` | 136 |
| `zones` | 1 |

Key vanilla anchors checked:

- Vanilla economic plans split mineral/energy subplans by `is_nomadic = no` and `is_nomadic = yes`.
- Vanilla colony automation includes `col_nomad_city`, `col_nomad_hive`, `col_nomad_nexus`, and `zone_ark_waystation_trade`.
- Vanilla Arkship ship sizes use `carries_colony = pc_ark`, are `shipclass_starbase`, can be disabled, and collect stockpiles from waystations or logistic ships.

Active conflict evidence shows adjacent Nomad risks are owned by parent mods, not Director:

| Surface | Object | Active winner | Risk |
| --- | --- | --- | --- |
| `ai_budget` | `alloys_expenditure_megastructures_arkships` | Stellar AI | override_conflict |
| `ai_budget` | `alloys_expenditure_megastructures_waystations` | Stellar AI | override_conflict |
| `component_templates` | `COMBAT_COMPUTER_ARKSHIP` | Extra Ship Components NEXT | override_conflict |
| `megastructures` | `arkship_ruined` | Gigastructural Engineering & More (4.4) | override_conflict |
| `megastructures` | `civilian_arkship_megastructure` | Gigastructural Engineering & More (4.4) | override_conflict |
| `megastructures` | `military_arkship_megastructure` | Gigastructural Engineering & More (4.4) | override_conflict |
| `megastructures` | `science_arkship_megastructure` | Gigastructural Engineering & More (4.4) | override_conflict |
| `megastructures` | `waystation_megastructure` | Gigastructural Engineering & More (4.4) | override_conflict |
| `section_templates` | `CLOAKING_WAYSTATION_SECTION` | Starbase Extended 3.0 | override_conflict |

## Director Generated Surface

Generated file audit covers 42 files and 1,019 top-level generated objects with zero unresolved placeholders. Generated reference audit contains 3,818 references, all `ok`.

Generated conflict audit contains only one Director-owned Nomad-named object:

| Object type | Object | File | Classification |
| --- | --- | --- | --- |
| `scripted_trigger` | `staid_opening_nomad_arkship_research` | `common/scripted_triggers/zzzz_staid_10_opening_strategy_triggers.txt` | additive Director object |

This means Director does not directly override vanilla or parent Nomad colony types, Arkship ship sizes, Arkship component templates, Waystation sections, Wayline mechanics, or Contract on_actions.

## Surface Classification

| Director surface | Classification | Evidence | Risk |
| --- | --- | --- | --- |
| Opening research route | Nomad-aware targeted support | `staid_opening_nomad_arkship_research` requires `is_nomadic = yes`; `basic_economy_plan` includes it in the opening growth-to-research route. | Static only; runtime priority cadence unproven. |
| Economic plan | Partial Nomad support, normal-only for most high-scale pressure | Full `basic_economy_plan` override includes one Nomad opening lane, while many later construction, megastructure, starbase, fleet, and crisis gates require `is_nomadic = no`. | Does not replace vanilla's full Nomad mineral/energy ladder. |
| Technology unlocks | Nomad-aware where needed | Generated technology file includes Arkship/Waystation checks such as `tech_arkship_tier_3`, `tech_waystation_2`, `tech_waystation_3`, `is_waystation_starbase`, and `is_nomadic = yes` equivalents. | Static reference-safe only. |
| Megastructures | Normal/Waystation-safe, no Arkship ownership | Generated megastructure copies preserve `megastructures/system_ownership_or_waystation_check`; active Arkship/Waystation megastructure conflicts are owned by Gigas, not Director. | Gigas ownership is active-stack risk outside this slice. |
| Planet/PD decisions | Arkship-excluded | Generated PD outpost decisions include `NOT = { is_planet_class = pc_ark }` for Arkship carriers. | Correctly avoids applying planet outpost decisions to mobile Arkship colonies. |
| Buildings/districts | Source-preserving, not a Nomad colony-type rewrite | Generated building/district copies preserve parent nomadic cost switchers and `is_nomadic` conditions where present; T25 added only two More Arcologies buildings, not colony types. | Live AI construction cadence unproven. |
| Starbase modules/buildings | Normal-only static defense | Generated starbase defense modules/buildings use `is_nomadic = no`; active Waystation section ownership remains Starbase Extended/NSC3/vanilla. | No Director Waystation defense strategy. |
| War/fleet/fauna pressure | Normal-only | Generated threat, fleet, raiding, conquest, and hostile fauna gates use `is_nomadic = no` where colony/fleet assumptions could misfit Nomads. | Contracts are not directly tuned by Director. |
| Contracts and Operational Reserves | Not directly owned | Object definitions show vanilla contract on_actions and Nomad budget/reserve-like surfaces; generated conflict audit has no Director Contract or Operational Reserve object. | No Director-specific contract strategy or runtime proof. |
| Colony types/designations | Not directly owned | Generated file audit has no `colony_types` file; vanilla owns `col_nomad_*` designations and automation. | This is compatibility-by-noninterference, not new Nomad automation. |

## Findings

1. The current Director strategy is compatible with normal empires and conservative for Nomads: it gives Nomads an opening research lane, but blocks most high-scale normal-empire planet/starbase/megastructure pressure with `is_nomadic = no`.
2. The generated patch does not directly touch the highest-risk Nomad mechanics: Arkship ship sizes, Arkship component templates, Waystation sections, Waylines, Contract on_actions, or Nomad colony types.
3. T25's More Arcologies patch remains compatible with this stance because it adds two building job-pressure objects only and does not emit a colony/designation rewrite.
4. Active-stack risk exists around Gigas Arkship/Waystation megastructure dummy overrides, ESC Arkship component/computer overrides, and Starbase Extended's cloaking waystation section, but those are parent-mod conflicts outside Director's generated ownership.

## Acceptance

T26 acceptance is met for static audit scope: every touched economy, planet, war, and starbase surface is classified as normal-only, Nomad-aware targeted support, source-preserving, or not directly owned. No invented Nomad triggers, effects, modifiers, scopes, folders, Wayline behavior, Contract behavior, or Operational Reserve behavior were added.

## Remaining Risk

Runtime AI effectiveness for Nomads and Arkships is unproven. This audit does not prove that a live Nomad AI will reach the desired research/fleet/megastructure pace; it proves that strategic v2 generated surfaces avoid unsafe Nomad assumptions and preserve parent ownership for high-risk Nomad mechanics.
