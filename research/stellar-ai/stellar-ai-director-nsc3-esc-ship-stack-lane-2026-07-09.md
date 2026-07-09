# Stellar AI Director NSC3/ESC Ship Stack Lane Evidence Graph

Date: 2026-07-09

Task card: T15 - NSC3/ESC lane evidence graph

## Scope

This report maps the current NSC3, ESC NEXT, and adjacent ship-stack evidence
before any direct Stellar AI Director handling of ship templates, component
templates, component sets, ship sizes, sections, ship behaviors, or global ship
designs. The current safe implementation lane remains technology route pressure.

Target baseline: Stellaris PC 4.4.5 active stack evidence from the 2026-07-08
packet datasets.

Runtime status: not run for this task. Ship designer visibility, AI design use,
SAVEFAIL behavior, and combat behavior remain runtime/smoke-test claims.

## Active Stack Identity

Validated dataset: `stellaris_packet_active_source_roots_20260708` passed with
121 rows.

| Load | Mod | Steam ID | Version | Common | Descriptor |
| --- | --- | --- | --- | --- | --- |
| 70 | Extra Ship Components NEXT | 2648658105 | v4.4.* | True | True |
| 71 | NSC3 | 683230077 | v4.4.* | True | True |
| 73 | ESC NEXT: Overwrites: Component Progression | 2653789292 | v4.4.* | True | True |
| 74 | ESC NEXT: Overwrites: Global Ship Designs | 2653699311 | v4.4.* | True | True |
| 75 | ESC NEXT: Overwrites: Special Weapon Types Patch | 2663957444 | v4.4.* | True | True |
| 76 | ASB Addon: ESC NEXT | 2769917594 | 4.*.* | False | True |
| 116 | Spacefleet Tactica | 3696204283 | v4.4.* | True | True |

This order satisfies the captured ESC guidance that base ESC NEXT must load
before NSC3. The ESC add-ons intentionally load after NSC3 and therefore need
object-winner proof, not assumption.

## Maintainer Guidance Anchors

Validated dataset:
`stellaris_packet_followup_mod_maintainer_guidance_matrix_20260708` passed with
13 rows.

- ESC NEXT guidance retrieved 2026-07-08 says ESC has built-in NSC3
  compatibility, must load before NSC3, add-ons touch component progression,
  global ship designs, and weapon types, and AI can use new components.
- NSC3 guidance retrieved 2026-07-08 says NSC3 moved ship classes to
  `nsc_ship_sizes`, still overwrites vanilla `00_ship_sizes`, added
  `is_nsc_activated`, recommends Spacefleet Tactica, and fixed a bioship design
  missing a combat computer.
- NSC3 troubleshooting guidance says bad load-order symptoms include missing
  sections/classes, wrong starbase slots, and SAVEFAIL empty component spots.
  That is smoke-test guidance, not static proof.
- Spacefleet Tactica guidance says it changes ship behavior AI, adds sections,
  improves design AI, and expects compatible mods above it with add-ons below.

## Director Lane

Validated dataset: `stellar_ai_director_route_overrides_20260706` passed with
125 rows.

Current Stellar AI Director route pressure covers only technology objects for
this ship stack:

- `nsc3_capital_hull_route`: `tech_Carrier_1`, `tech_Dreadnought_1`,
  `tech_Flagship_1`, `tech_heavycarrier_1`, and `tech_supercarrier_1`; all are
  load winners with `validation_status = ok`.
- `esc_component_route`: `esc_tech_dark_matter_power_core_2`,
  `esc_tech_strikecraft_5`, and `esc_tech_dreadnought_computer`; all are load
  winners with `validation_status = ok`.

Generated technology evidence is present in
`mods/StellarAIDirector/common/technology/zzzz_staid_01_unlock_technology_technology.txt`
at the route object definitions around lines 2245, 2303, 2361, 2433, 2501,
2570, 2652, and 2707.

## Final Winner Graph

Validated dataset: `stellaris_packet_winning_objects_20260708` passed with
10,276 rows.

Representative final winners for the active ship stack:

| Surface | Winner | Winning objects |
| --- | --- | ---: |
| component_templates | Extra Ship Components NEXT | 1292 |
| component_templates | ESC NEXT: Overwrites: Component Progression | 603 |
| component_sets | Extra Ship Components NEXT | 591 |
| section_templates | NSC3 | 468 |
| component_templates | ESC NEXT: Overwrites: Special Weapon Types Patch | 265 |
| component_templates | Spacefleet Tactica | 227 |
| section_templates | Spacefleet Tactica | 220 |
| global_ship_designs | ESC NEXT: Overwrites: Global Ship Designs | 175 |
| component_templates | NSC3 | 153 |
| ship_sizes | NSC3 | 67 |
| component_sets | NSC3 | 47 |

Validated conflict dataset:
`stellaris_packet_active_load_order_conflicts_20260708` passed with 2,244 rows.
Conflict pressure is real on the same surfaces: component templates, global ship
designs, section templates, ship sizes, component sets, starbase modules, and
starbase buildings. The highest conflict clusters are ESC component progression
component templates (588), ESC special weapon component templates (265),
Spacefleet Tactica component templates (180), ESC global ship designs (175),
NSC3 section templates (127), and NSC3 ship sizes (64).

## Reference Graph

Validated dataset:
`stellaris_packet_ship_design_reference_checks_20260708` passed with 17,855
rows.

Reference status aggregate:

| Status | Reference key | Target surface | Rows |
| --- | --- | --- | ---: |
| ok | component.template | component_templates | 12636 |
| ok | required_component | component_templates | 2389 |
| ok | ship_size | ship_sizes | 1961 |
| ok | section.template | section_templates | 794 |
| missing | component.template | component_templates | 35 |
| missing | required_component | component_templates | 21 |
| missing | ship_size | ship_sizes | 13 |
| missing | section.template | section_templates | 6 |

Sample missing clusters:

- ESC NEXT global design overwrite references missing tier-6 bio/psychic-style
  components such as `ANTI_EVASION_GUN_6`, `ANTI_FIRE_RATE_GUN_6`,
  `HEALING_GUN_6`, `EVASION_GUN_6`, `FIRE_RATE_GUN_6`, and `CONFUSER_GUN_6`
  in `common/global_ship_designs/biogenesis_ship_designs.txt`.
- Gigas frameworld section templates reference missing
  `frameworld_defensive_station` and `frameworld_planetary_outpost` ship sizes.
- Gigas/ACOT-flavored global ship designs reference missing
  `BASE_COMBAT_COMPUTER_COLOSSUS_OE` and `OMEGA_PRECURSOR_COLOSSUS_*_SECTION`.

These rows are triage inputs, not proof that Stellar AI Director broke the ship
stack. They are sufficient to block direct generated ship templates until a
dedicated ship-stack validation/fix card proves exact winners and loader
semantics.

## Direct Override Block

Stellar AI Director currently generates no direct files in:

- `common/ship_sizes`
- `common/section_templates`
- `common/component_templates`
- `common/component_sets`
- `common/global_ship_designs`
- `common/ship_behaviors`
- `common/component_slot_templates`

Evidence:

- `rg --files mods\StellarAIDirector\common | rg "common/(ship_sizes|section_templates|component_templates|component_sets|global_ship_designs|ship_behaviors|component_slot_templates)"` returned no paths.
- JData `stellar_ai_director_generated_file_audit_20260704` validates with 42
  generated files and zero rows in those ship graph folders.

## Decision

Classification: `compatible_with_caveat` for the current technology-pressure
lane; `blocked_for_direct_templates` for ship-size, section-template,
component-template, component-set, behavior, and global-design overrides.

No gameplay patch is warranted in T15. Current Director support should remain
limited to source-backed technology route pressure for NSC3 hull techs and ESC
component techs. Direct ship graph work requires a separate implementation card
with exact final-winner proof, missing-reference triage, component/set checks,
and a narrow runtime smoke test before any claim that the AI can use the final
sections/components/designs safely.

## Validation

- JData `validate_index` passed for active source roots, maintainer guidance,
  active conflict matrix, winning objects, ship-design reference checks, route
  overrides, and generated file audit.
- JData server-side aggregation was used for conflict, winner, and reference
  counts.
- `python tools/validate_stellar_ai_director_patch.py` passed before this
  report was written.
- No runtime test was run and no runtime claim is made.
