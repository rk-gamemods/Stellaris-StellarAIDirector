# Stellaris 4.4.x AI / Colony / Zone / Ship Surface Follow-up Report

**Retrieved:** 2026-07-08
**Target:** Stellaris 4.4.x, prioritizing exact 4.4.4 versus 4.4.5 differences.
**Local baseline supplied by user:** Pegasus v4.4.5 (2f57), active IronyModManager playset with 120 enabled mods, and local vanilla documentation for economic plans/on_actions.

## Executive findings

| Finding | Confidence | Practical consequence |
|---|---:|---|
| Public CWTools Stellaris config provides exact current `.cwt` definitions for the requested folders, but I did **not** find a public CWTools ref explicitly labelled 4.4.4 or 4.4.5. | Medium-High | Treat the matrix as **current public CWTools**, not as a proven 4.4.4/4.4.5 split. |
| For the requested AI/planet surfaces (`economic_plans`, `ai_budget`, `colony.cwt`, `districts.cwt`, `zones.cwt`), current public CWTools file hashes matched the last public version-labelled `4.3.7` commit I checked. | Medium | No public evidence of a 4.4.4-to-4.4.5 schema change for these surfaces; actual vanilla depot diff is still required. |
| Public CWTools on_actions validation is deliberately stripped down. The disabled old file says full scoped validation is impractical because scripted on_actions can be made/fired from script. | High | CWTools will not answer exact nested on_action duplicate merge semantics. |
| No public CWTools or Paradox source found here specifies duplicate nested `events` or `random_events` event-ID merge behavior. | Medium | Local README plus runtime tests are the best next authority. |
| The only public schema delta observed after the last version-labelled CWTools commit was `component_template.prerequisites` accepting `OR` blocks. | Medium | Relevant for NSC/ESC/SFT component validation, but not proven to map specifically to 4.4.4 versus 4.4.5. |
| For machine-readable CWTools outside VS Code, the strongest public route found is `cwtools/cwtools-action`, which writes `output.json`. | Medium | Use CI/action output as the reproducible diagnostic artifact unless a local CLI is separately installed/verified. |

## CWTools schema answers

The public CWTools Stellaris repository describes itself as the Stellaris `.cwt` rules source and documents stable/latest behavior. The current public config folder contains the relevant files: `00_small_types_consolidated.cwt`, `colony.cwt`, `districts.cwt`, `zones.cwt`, `on_actions.cwt`, `section_templates.cwt`, `ship_sizes.cwt`, `components_consolidated.cwt`, `ship_behaviors.cwt`, and `global_ship_designs.cwt`. See `cwtools_schema_surface_matrix.csv` for the field-by-field matrix.

### Exact current public CWT paths

| Surface | Public CWT path | Current public object type |
|---|---|---|
| `common/ai_budget` | `config/common/00_small_types_consolidated.cwt` | `ai_budget` |
| `common/economic_plans` | `config/common/00_small_types_consolidated.cwt` | `economic_plan` |
| `common/on_actions` | `config/common/on_actions.cwt` | `on_action` |
| `common/colony_types` | `config/common/colony.cwt` | `colony_type` |
| `common/colony_automation` | `config/common/colony.cwt` | `colony_automation` |
| `common/colony_automation_exception` | `config/common/colony.cwt` | type path only found; body unresolved |
| `common/districts` | `config/common/districts.cwt` | `district` |
| `common/zones` | `config/common/zones.cwt` | `zones` |
| `common/zone_slots` | `config/common/zones.cwt` | `zone_slots` |
| ship sections/components/designs | `ship_sizes.cwt`, `section_templates.cwt`, `components_consolidated.cwt`, `ship_behaviors.cwt`, `global_ship_designs.cwt` | `ship_size`, `section_template`, `component_slot_template`, `component_set`, `component_template`, `ship_behavior`, `global_ship_design` |

### Key schema snippets

`config/common/00_small_types_consolidated.cwt`:

```cwt
type[ai_budget] = { path = "game/common/ai_budget" }
type[economic_plan] = { path = "game/common/economic_plans" }
```

`ai_budget` is country-scoped in current public CWT and supports `resource`, `type = expenditure|upkeep`, `category`, `potential`, `weight`, `desired_max`, and `desired_min` blocks. `economic_plan` supports top-level `income`, `focus`, `subplan`, `pops`, `empire_size`, `naval_cap`, and `ai_weight`; each `subplan` supports country-scoped `potential`, `income`, `focus`, `pops`, `empire_size`, `naval_cap`, `set_name`, `scaling`, and `optional`.

`config/common/on_actions.cwt`:

```cwt
on_action = {
  events = { <event> }
  random_events = { int = 0 int = <event> }
}
```

`config/common/on_actions old.txt` explains why the older scoped definition is disabled: scripted on_actions make validation unreliable. This is a schema limitation, not a semantics statement.

`config/common/colony.cwt` declares `colony_automation` with `push_scope = planet` and `path_strict = yes`. The public body includes `category`, `available`, `prio_districts`, `prio_zones`, and `buildings` entries. `colony_type` includes AI resource conversion/current conversion, planet modifiers, and weighting.

`config/common/districts.cwt` declares `district` with `push_scope = planet`; key 4.4-relevant fields include `zone_slots`, `exempt_from_ai_planet_specialization`, `ai_weight`, `ai_resource_production`, `additional_ai_weight`, and `ai_weight_coefficient`.

`config/common/zones.cwt` declares both `zones` and `zone_slots`. `zones` includes `zone_sets`, `include`, `included_building_sets`, `excluded_building_sets`, `convert_to`, `ai_priority`, and `ai_weight_coefficient`. `zone_slots` includes `start`, `included_zone_sets`, `include`, `exclude`, `potential`, and `unlock`.

## 4.4.4 versus 4.4.5 status

I did not find a public CWTools ref or Paradox schema document labelled specifically as Stellaris 4.4.4 or Stellaris 4.4.5 for the requested surfaces. The public CWTools commit history checked still had a last explicit version-labelled commit of `4.3.7`; the later June 2026 commits were generic schema corrections, including adding `OR` to component-template prerequisites and a scope fix unrelated to the requested AI/planet surfaces.

**Observed public schema comparison against CWTools `4.3.7` commit:**

| File | Current-vs-4.3.7 public observation | Interpretation |
|---|---|---|
| `00_small_types_consolidated.cwt` | Same file hash in checked refs | No public AI-budget/economic-plan CWT delta observed. |
| `colony.cwt` | Same file hash in checked refs | No public colony-type/automation CWT delta observed. |
| `districts.cwt` | Same file hash in checked refs | No public district CWT delta observed. |
| `zones.cwt` | Same file hash in checked refs | No public zone/zone-slot CWT delta observed. |
| `section_templates.cwt` | Same file hash in checked refs | No public section-template CWT delta observed. |
| `ship_sizes.cwt` | Same file hash in checked refs | No public ship-size CWT delta observed. |
| `global_ship_designs.cwt` | Same file hash in checked refs | No public global-design CWT delta observed. |
| `components_consolidated.cwt` | Current differs from checked 4.3.7 file | Current public CWT adds `OR` in `component_template.prerequisites`; not mapped to 4.4.4/4.4.5 without depot validation. |

**Conclusion:** the exact 4.4.4-to-4.4.5 answer remains unresolved from public CWTools alone. A verified 4.4.4 depot or full vanilla snapshot is required.

## on_actions nested merge semantics

Public CWTools does **not** specify nested merge semantics for duplicate event IDs. It validates the shape of `events` and `random_events`, but it does not document how duplicate nested values are merged, appended, de-duplicated, or overwritten. The older on_actions schema was disabled because scripted on_actions make scope validation impractical.

Public Paradox documentation found during this pass did not provide an exact rule for duplicate event IDs inside `events` or `random_events`. Therefore:

- `events` duplicate IDs: unresolved from public documentation.
- `random_events` duplicate weighted IDs: unresolved from public documentation.
- Recommended validation: a minimal runtime test mod with duplicate events across multiple files/mods and deterministic log side effects.

## Mod-maintainer guidance relevant to the requested surfaces

The companion `mod_maintainer_guidance_matrix.csv` contains exact row-level guidance. The most operationally important items are below.

### NSC3 + ESC NEXT + Spacefleet Tactica

**NSC3** has explicit 4.4 ship-surface notes: it moved NSC ship classes to `nsc_ship_sizes`, still overwrites vanilla `00_ship_sizes`, added `is_nsc_activated`, and fixed a save issue from a missing combat computer in a bioship design. Its troubleshooting guide tells users to test with only NSC3 and UI Overhaul Dynamic, start a new game, run `research_all_technologies`, and inspect NSC3. It lists bad-load-order symptoms directly relevant to this task: missing ship sections, invisible new ship classes, incorrect starbase slots, and `SAVEFAIL` from an empty component spot.

**ESC NEXT** publishes built-in NSC3 compatibility guidance and says ESC NEXT must load before NSC3. It also lists add-ons touching component progression, global ship designs, and weapon-type compatibility, and says the AI can use its new components.

**Spacefleet Tactica** says it changes ship behavior AI, adds ship sections, improves AI ship design, and AI empires use its sections. It says compatible mods should load above SFT, SFT add-ons should be directly below SFT, and NSC users should use the add-on that disables SFT ship sections.

**Recommended validation graph for this active combination:**

1. `ship_size.section_slots` must match `section_template.fits_on_slot` and `global_ship_design.section.slot`.
2. Every `section_template.component_slot.template` must exist in `common/component_slot_templates`.
3. Every global design component `slot` must match a section component slot or utility slot enum.
4. Every `component_template.component_set` must exist.
5. Every `ship_size.required_component_set` and `global_ship_design.required_component` must resolve.
6. Combat computers should be checked as utility `component_template` entries with valid `ship_behavior`, valid component set, valid class/size restriction, and AI-use metadata.
7. Run a new-game smoke test with all relevant tech unlocked and save at least one design per added ship class.

### Planetary Diversity and UIOD

Planetary Diversity public guidance confirms 4.4 support and says it changes existing planets through events rather than adding more planets. Its public page does not enumerate `common/zones`, `common/zone_slots`, or `common/districts` edits. Planetary Diversity - Planet View says it does not add building slots and is not compatible with UI Overhaul Dynamic or other planet-view mods; it recommends UIOD if using more building slots or a different UI. UIOD’s public guidance says it supports 4.4, has compatibility patches, includes a ship designer with room for more sections, and should usually be placed at the very bottom.

**Recommended PD validation:** diff enabled PD modules and UIOD patches for `common/zones`, `common/zone_slots`, `common/districts`, `common/colony_types`, planet-view interface files, and UIOD patch files. Then run a runtime UI check on vanilla and PD planet classes with zones visible.

### Gigastructural Engineering, Universal patches, Expanded Starbases, Stellar AI

Gigastructural Engineering publishes compatibility guidance noting AI use of megastructures, a scripted-trigger overwrite, topbar/resource-display caveats for new resources, and vanilla megastructure overwrites. This matters for `on_actions`, scripted triggers, resources, and compatibility patch ordering more than for the exact zone schema.

Universal Resource Patch is explicitly about displaying added strategic resources. Maintainer comments recommend bottom placement if there are issues and using Irony Mod Manager to resolve `interface/resource_groups` conflicts. Universal Modifier Patch is separate but relevant because Expanded Starbases requires it and it patches economy-category modifier availability.

For the user’s “Starbase Extended” item, the nearest public source found in this pass was **Expanded Starbases**. That page requires Universal Modifier Patch, UIOD, and Expanded Mods Base, and says it is incompatible with NSC or other mods that modify the starbase ship size file. Confirm the local workshop ID before applying this row to the active stack.

Stellar AI is directly relevant to AI surfaces. Its maintainer page says it is built on current 4.4 definitions and that shared buildings, jobs, zones, colony types, personalities, economic plans, strategic resources, and AI budgets retain current 4.4 mechanics. It recommends loading near the bottom unless another overlapping mod should win, and warns that AI overhauls or mods replacing the same economic/colony/job/building/zone definitions are incompatible.

## CWTools diagnostics outside VS Code on Windows

No maintained public standalone Windows CWTools CLI was verified in this pass. The current public machine-readable route found is `cwtools/cwtools-action`:

- It supports `game: stellaris`.
- It can accept `modPath`.
- It can use a custom `rules` repo and `rulesRef`.
- It can check all files with `changedFilesOnly: "0"`.
- It writes a full `output.json` diagnostic log that can be uploaded as an artifact.

**Recommended 2026 workflow:** use a temporary GitHub repository or private CI runner containing the mod stack or a generated merged/mod-root staging directory, then run `cwtools/cwtools-action` with `game=stellaris`, `changedFilesOnly=0`, and an explicit rules ref. For a local Windows workflow, reproducing the action through a compatible local runner/container is plausible, but it was not verified here as a maintained standalone CWTools CLI.

## Remaining validation priorities

See `remaining_open_questions.csv`. Highest-priority runtime tests:

1. Duplicate nested on_actions behavior.
2. NSC3/ESC/SFT ship designer save and component-slot coverage.
3. PD/UIOD zone-slot/planet-view visibility.
4. Active-stack economic_plan merged subplan winners.
5. Exact 4.4.4 depot diff against current v4.4.5.

## Source index

| Label | Source |
|---|---|
| CWTools Stellaris config README | https://github.com/cwtools/cwtools-stellaris-config#readme |
| CWTools common config folder | https://github.com/cwtools/cwtools-stellaris-config/tree/master/config/common |
| CWTools AI/economic plan CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/00_small_types_consolidated.cwt |
| CWTools on_actions CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/on_actions.cwt |
| CWTools old on_actions CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/on_actions%20old.txt |
| CWTools colony CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/colony.cwt |
| CWTools districts CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/districts.cwt |
| CWTools zones CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/zones.cwt |
| CWTools components CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/components_consolidated.cwt |
| CWTools section templates CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/section_templates.cwt |
| CWTools ship sizes CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/ship_sizes.cwt |
| CWTools ship behaviors CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/ship_behaviors.cwt |
| CWTools global ship designs CWT | https://github.com/cwtools/cwtools-stellaris-config/blob/master/config/common/global_ship_designs.cwt |
| CWTools Action README | https://github.com/cwtools/cwtools-action/blob/master/README.md |
| Gigastructural Engineering & More | https://steamcommunity.com/sharedfiles/filedetails/?id=1121692237 |
| NSC3 main page | https://steamcommunity.com/workshop/filedetails/?id=683230077 |
| NSC3 troubleshooting guide | https://steamcommunity.com/workshop/filedetails/discussion/683230077/759555096795282832/ |
| NSC3 public releases mirror | https://github.com/corsairmarks/nsc3-season-1/releases |
| ESC NEXT Steam page | https://steamcommunity.com/sharedfiles/filedetails/?id=2648658105 |
| ESC NEXT public repo | https://github.com/corsairmarks/Extra-Ship-Components-Next |
| Spacefleet Tactica | https://steamcommunity.com/sharedfiles/filedetails/?id=3696204283 |
| Planetary Diversity | https://steamcommunity.com/sharedfiles/filedetails/?id=819148835 |
| Planetary Diversity - Planet View | https://steamcommunity.com/sharedfiles/filedetails/?id=1866576239 |
| UI Overhaul Dynamic | https://steamcommunity.com/workshop/filedetails/?id=1623423360 |
| Universal Resource Patch | https://steamcommunity.com/sharedfiles/filedetails/?id=1595876588 |
| Universal Modifier Patch | https://steamcommunity.com/workshop/filedetails/?id=1688887083 |
| Expanded Starbases | https://steamcommunity.com/sharedfiles/filedetails/?id=1359700418 |
| Stellar AI | https://steamcommunity.com/workshop/filedetails/?id=3610149307 |
