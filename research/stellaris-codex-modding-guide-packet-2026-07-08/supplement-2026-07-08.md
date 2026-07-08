# Stellaris Codex Modding Guide Packet Supplement (2026-07-08)

## Scope And Authority

This supplement verifies the attached `stellaris_coding_agent_packet.zip` against the local game and active playset on 2026-07-08. It is source-provenance documentation only; it did not edit live game, Workshop, or mod source files.

Important correction: the local install is `Pegasus v4.4.4 (5505)` with `rawVersion=v4.4.4` and `modsCompatibilityVersion=4.4` from `C:\Steam\steamapps\common\Stellaris\launcher-settings.json`. The request and packet refer to 4.4.4, but the current inspected source files are 4.4.5. Treat these findings as stable 4.4.x evidence and re-check against a true 4.4.4 rollback before making 4.4.4-only claims.

Live playset evidence:
- `dlc_load.json` enabled mods: 120.
- Active launcher playset: `IronyModManager` from `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\launcher-v2.sqlite`.
- Launcher enabled mods: 120.
- `dlc_load.json` and launcher active playset differ by: dlc-minus-launcher=0, launcher-minus-dlc=0.

## Requested Open Questions

| Topic | Verified Finding | Evidence | Residual Risk |
|---|---|---|---|
| `common/economic_plans` | Correct the packet: economic plans are not simple full-object last-winner objects. Vanilla `00_example.txt` says economic plans are additive and multiple instances of a plan are mashed together; duplicate subplan names overwrite the existing subplan. | `C:/Steam/steamapps/common/Stellaris/common/economic_plans/00_example.txt`; see `surface-summary-2026-07-08.csv` and conflict matrix. | Static report does not resolve nested subplan wins; inspect subplan names before patching. |
| `common/ai_budget` | Folder exists in 4.4.5 with 20 vanilla files plus modded definitions. Vanilla docs show `potential` gates entries; budget categories must have `use_for_ai_budget = yes`; multiple entries with the same category and resource are allowed. | `C:/Steam/steamapps/common/Stellaris/common/ai_budget/documentation.txt` and `00_alloys_budget.txt`; Gigas active source has additional special-resource budgets. | No local source proves top-level same-ID budget entries merge like economic plans; treat duplicate top-level budget IDs as conflict risk. |
| `common/ai_planet_specialization` | Correct the packet: this folder is absent in the current local 4.4.5 install. Related current surfaces are `common/colony_types`, `common/colony_automation*`, `common/districts`, `common/zones`, and `common/zone_slots`. | Filesystem check against `C:/Steam/steamapps/common/Stellaris/common`; surface summary has zero folder roots for `ai_planet_specialization`. | The term still appears as district flags such as `exempt_from_ai_planet_specialization`; do not create a same-named folder without schema proof. |
| `common/on_actions` merge behavior | Treat as additive/merge-like, not simple last-winner. Vanilla economic-plan docs explicitly compare economic-plan additive overwriting to on_actions; the on_actions README defines `events` and `random_events` blocks and custom on_actions. | `C:/Steam/steamapps/common/Stellaris/common/economic_plans/00_example.txt`; `C:/Steam/steamapps/common/Stellaris/common/on_actions/99_README_ON_ACTIONS.txt`. | Nested duplicate event entries still need object-level review; static matrix labels duplicate on_actions as `merge_expected`. |
| Gigas megastructure AI hooks | Gigas active source contributes megastructure definitions, AI-weighted megastructures, and multiple AI budget files for special resources such as negative mass, sentient metal, and supertensiles. | `surface-source-provenance-2026-07-08.csv`, `winning-objects-2026-07-08.csv`, Gigas JDoc index, and active source root at load position 62. | Static source proves hooks exist, not that AI reaches the tech/economy state to use them. Runtime observer proof is still required. |
| Starbase Extended starbase scopes | Starbase Extended active source defines starbase modules/buildings with `ai_weight`; static report records nested `from`/`owner` usage counts for scope-sensitive review. | Load position 72 source root; `starbase-extended-scope-report-2026-07-08.csv`. | CWTools schema was not available locally, so scope diagnostics are parser/provenance only. |
| NSC3/ESC ship/component/section validity | NSC3 and ESC parse across requested ship/component surfaces. The generated ship reference check reports missing references separately for global designs/section templates. | `ship-design-reference-checks-2026-07-08.csv`; active load positions 70-71 plus NSC3 shipset patches at 42-48 and 77-80. | Static parser is not a full game schema engine; CWTools or launch logs should confirm unresolved missing rows. |
| Planetary Diversity zones/districts | Planetary Diversity family is active at positions 64-67 plus UI patch at 107. Current 4.4.5 uses `zones` and `zone_slots`; generated report checks PD district/zone references against active winners. | `planetary-diversity-zone-district-report-2026-07-08.csv`. | Some references are not simple object IDs; rows marked `not_checked_or_missing` need CWTools/runtime log confirmation before treating them as broken. |

## Surface Summary

| Surface | Definitions | Unique Objects | Conflicts/Merges | Source Roots With Folder | AI Weight Definitions | Merge Model |
|---|---:|---:|---:|---:|---:|---|
| economic_plans | 15 | 7 | 4 | 5 | 12 | additive_object_merge |
| ai_budget | 294 | 245 | 45 | 4 | 0 | top_level_duplicate_unproven; category/resource duplicates allowed |
| ai_planet_specialization | 0 | 0 | 0 | 0 | 0 | folder_absent_in_local_4.4.5 |
| colony_types | 148 | 124 | 24 | 4 | 0 | last_definition_wins_by_object_id |
| on_actions | 1423 | 549 | 161 | 27 | 0 | additive_object_merge |
| megastructures | 1254 | 967 | 229 | 10 | 436 | last_definition_wins_by_object_id |
| starbase_modules | 253 | 187 | 58 | 7 | 252 | last_definition_wins_by_object_id |
| starbase_buildings | 236 | 207 | 24 | 11 | 230 | last_definition_wins_by_object_id |
| ship_sizes | 631 | 502 | 86 | 9 | 0 | last_definition_wins_by_object_id |
| section_templates | 1509 | 1342 | 154 | 18 | 474 | last_definition_wins_by_section_key |
| component_templates | 4967 | 3532 | 1072 | 14 | 3621 | last_definition_wins_by_object_id |
| component_sets | 1257 | 1253 | 4 | 12 | 0 | last_definition_wins_by_object_id |
| global_ship_designs | 843 | 659 | 183 | 8 | 0 | last_definition_wins_by_design_name |
| districts | 399 | 286 | 99 | 5 | 81 | last_definition_wins_by_object_id |
| zones | 361 | 261 | 100 | 8 | 0 | last_definition_wins_by_object_id |
| zone_slots | 103 | 103 | 0 | 4 | 0 | last_definition_wins_by_object_id |

## Focus Source Roots

| Load | Steam ID | Name | Required Version | Root |
|---:|---|---|---|---|
| 0 | vanilla | Stellaris vanilla | v4.4.4 | `C:\Steam\steamapps\common\Stellaris` |
| 62 | 1121692237 | Gigastructural Engineering & More (4.4) | v4.4.* | `c:\steam\steamapps\workshop\content\281990\1121692237` |
| 64 | 819148835 | Planetary Diversity | v4.4.* | `c:\steam\steamapps\workshop\content\281990\819148835` |
| 65 | 3173239930 | Planetary Diversity - Vanilla Replacements | v4.4.* | `c:\steam\steamapps\workshop\content\281990\3173239930` |
| 66 | 1732447147 | Planetary Diversity - More Arcologies | v4.4.* | `c:\steam\steamapps\workshop\content\281990\1732447147` |
| 67 | 2284514368 | Planetary Diversity - Gaia Worlds | v4.4.* | `c:\steam\steamapps\workshop\content\281990\2284514368` |
| 70 | 2648658105 | Extra Ship Components NEXT | v4.4.* | `c:\steam\steamapps\workshop\content\281990\2648658105` |
| 71 | 683230077 | NSC3 | v4.4.* | `c:\steam\steamapps\workshop\content\281990\683230077` |
| 72 | 3250900527 | Starbase Extended 3.0 | v4.**.* | `c:\steam\steamapps\workshop\content\281990\3250900527` |
| 115 | 3610149307 | Stellar AI | v4.4.4 | `c:\steam\steamapps\workshop\content\281990\3610149307` |
| 116 | 3696204283 | Spacefleet Tactica | v4.4.* | `c:\steam\steamapps\workshop\content\281990\3696204283` |
| 119 | 1595876588 | !!!Universal Resource Patch [2.4+] | v4.*.* | `c:\steam\steamapps\workshop\content\281990\1595876588` |
| 120 |  | Stellar AI Director | v4.4.* | `C:\Users\Admin\Documents\GIT\GameMods\StellarisMods\mods\StellarAIDirector` |

## Conflict And Winner Notes

The complete active-load-order matrix is in `tables/active-load-order-conflict-matrix-2026-07-08.csv`; the complete winner table is in `tables/winning-objects-2026-07-08.csv`. The rows below are the first high-signal duplicate objects after sorting by surface and duplicate count.

| Surface | Object | Definitions | Winner | Risk |
|---|---|---:|---|---|
| ai_budget | `alloys_expenditure_megastructures` | 3 | 120:Stellar AI Director `common/ai_budget/zzz_staid_alloys_budget.txt` | override_conflict |
| ai_budget | `minerals_expenditure_planets_high` | 3 | 120:Stellar AI Director `common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt` | override_conflict |
| ai_budget | `minerals_expenditure_planets_low` | 3 | 120:Stellar AI Director `common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt` | override_conflict |
| ai_budget | `minerals_expenditure_planets_med` | 3 | 120:Stellar AI Director `common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_armies` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_armies_threatened` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_buffer` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_colonies_expand` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_colonies_infernal_expand` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_decisions` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_deposit_blockers` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_habitats` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_megastructures_arkships` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_megastructures_waystations` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_planets` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_ship_upgrades` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_ships` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_starbases` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_starbases_expand` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_expenditure_starbases_fallen_empires` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_upkeep_buffer` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_upkeep_planets` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `alloys_upkeep_ships` | 2 | 115:Stellar AI `common/ai_budget/00_alloys_budget.txt` | override_conflict |
| ai_budget | `influence_expenditure_claims` | 2 | 120:Stellar AI Director `common/ai_budget/zzzz_staid_08_site_limited_expansion_ai_budget.txt` | override_conflict |
| ai_budget | `influence_expenditure_claims_fanatic_militarist` | 2 | 120:Stellar AI Director `common/ai_budget/zzzz_staid_08_site_limited_expansion_ai_budget.txt` | override_conflict |

## Static Diagnostics

CWTools availability checks: where.exe cwtools=not_found_or_failed; where.exe cwtools-cli=not_found_or_failed; dotnet tool list -g=pass; VS Code/Cursor CWTools extension directories=not_found; PDX parser diagnostics for requested active-stack surfaces=pass.

PDX parser diagnostics for requested surfaces: 0 parse errors. See `tables/pdx-parse-diagnostics-2026-07-08.csv`.

Ship/section/component reference checks: 17855 rows, 75 missing-reference rows. See `tables/ship-design-reference-checks-2026-07-08.csv`.

Planetary Diversity zone/district checks: 537 rows, 0 not-checked-or-missing rows. See `tables/planetary-diversity-zone-district-report-2026-07-08.csv`.

## Safe Runtime Validation Plan

Do not run this automatically. Use it only after explicit user approval for runtime testing.

1. Before launch, run `python tools\manage_stellaris_commands_at_date.py status`; the live `commands_at_date.txt` must be absent unless the user approves an observer run.
2. Snapshot `dlc_load.json`, `mods_registry.json`, active `launcher-v2.sqlite` playset rows, and the generated conflict/winner tables from this supplement.
3. If the test is only load-safety, launch to main menu with the active playset and capture `error.log`, `game.log`, and `setup.log`; do not arm dated commands.
4. If the test is AI behavior, create a supervised observer-run folder, then enable the managed command schedule only through `python tools\manage_stellaris_commands_at_date.py enable`; use `game_speed 5` for approved observer schedules.
5. Capture checkpoints at 2250, 2300, 2325, and 2350 or stop early if research/economy slope makes the 2350 benchmark impossible.
6. Disable the live command schedule before handoff with `python tools\manage_stellaris_commands_at_date.py disable`, then verify `status` reports absent.
7. Treat runtime logs as the source of truth for CWTools-unchecked missing references, GUI layout, AI megastructure adoption, upkeep spirals, and starbase spending crowd-out.

## Generated Artifacts

- `tables/active-source-roots-2026-07-08.csv`
- `tables/surface-source-provenance-2026-07-08.csv`
- `tables/surface-summary-2026-07-08.csv`
- `tables/object-definitions-2026-07-08.csv`
- `tables/active-load-order-conflict-matrix-2026-07-08.csv`
- `tables/winning-objects-2026-07-08.csv`
- `tables/gigas-megastructure-ai-hooks-2026-07-08.csv`
- `tables/starbase-extended-scope-report-2026-07-08.csv`
- `tables/ship-design-reference-checks-2026-07-08.csv`
- `tables/planetary-diversity-zone-district-report-2026-07-08.csv`
- `tables/pdx-parse-diagnostics-2026-07-08.csv`
- `tables/cwtools-diagnostics-2026-07-08.csv`
- `webchatgpt-followup-2026-07-08/stellaris_44x_ai_surface_followup_report.md`
- `webchatgpt-followup-2026-07-08/cwtools_schema_surface_matrix.csv`
- `webchatgpt-followup-2026-07-08/mod_maintainer_guidance_matrix.csv`
- `webchatgpt-followup-2026-07-08/remaining_open_questions.csv`

## Web ChatGPT Follow-up Reconciliation

Returned follow-up files are preserved under `webchatgpt-followup-2026-07-08/`.
They refine the supplement but do not overturn the local-source findings.

| Topic | Follow-up result | Effect on this supplement |
|---|---|---|
| CWTools schema authority | Public CWTools is the current schema source found, but no public 4.4.4- or 4.4.5-labelled schema ref was found. | Keep local 4.4.5 files as the inspected source of truth; treat public CWTools as current schema guidance, not a proven 4.4.4/4.4.5 diff. |
| `economic_plans` and `ai_budget` | Public CWT exposes object paths and fields; local economic-plan docs still provide the strongest merge semantics found. | No change: economic plans are additive/merge-like locally; top-level `ai_budget` duplicate behavior still needs active-stack/runtime validation. |
| `on_actions` | Public CWT validates shape only; nested duplicate event-ID behavior is not specified. | No change: duplicate nested `events` and `random_events` semantics remain runtime-test questions. |
| 4.4.4 versus 4.4.5 | No public exact version split was found for the requested surfaces. | A verified 4.4.4 depot/snapshot is still required for exact rollback claims. |
| NSC3/ESC/SFT | Public guidance supports ESC before NSC3, Spacefleet Tactica ordering/add-ons, and ship-designer/runtime smoke tests. | Prioritize final graph validation for ship sizes, sections, component templates/sets, combat computers, and global ship designs. |
| Planetary Diversity/UIOD | Public guidance confirms 4.4 support and UIOD/planet-view compatibility concerns, but not exact zone/slot definitions. | Keep local PD zone/district table as source evidence; verify visible zones/planet UI in runtime only with approval. |
| Gigas/URP/UMP/starbases | Public guidance supports Gigas AI megastructure use and resource/UI patching concerns; Starbase Extended identity still needs exact local workshop-source confirmation. | Keep Gigas hooks as source-proven, and treat resource-group/topbar/starbase UI conflicts as active-stack validation items. |
| CWTools diagnostics | Strongest public machine-readable path found is `cwtools/cwtools-action` with `output.json`; no maintained standalone Windows CLI was verified. | Local CWTools diagnostics remain unavailable; CI/action-based diagnostics are the recommended next schema-validation route. |

## Remaining Open Questions

The current remaining questions are captured in `webchatgpt-followup-2026-07-08/remaining_open_questions.csv`. Highest-priority follow-up remains: exact 4.4.4 depot diff, duplicate nested `on_actions` runtime behavior, active-stack economic-plan merged subplan winners, NSC3/ESC/SFT ship graph validity, PD/UIOD runtime visibility, Starbase Extended identity, and machine-readable CWTools action diagnostics.
