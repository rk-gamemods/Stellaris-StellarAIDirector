# must-have skills

Generated: 2026-07-08

| Skill ID | Category | Topic | Purpose |
|---|---|---|---|
| `stl-file-layout-descriptors` | 00_foundation | Mod folder and descriptors | Verify mod folder layout, outer .mod, inner descriptor.mod, path, supported_version, tags, thumbnail, and package-sensitive metadata. |
| `stl-naming-namespace-hygiene` | 00_foundation | IDs, namespaces, and prefixes | Define safe naming conventions for object IDs, event namespaces, localization keys, flags, variables, and generated files. |
| `stl-project-orientation` | 00_foundation | Repo/task orientation | Identify the target mod, repo layout, task type, deliverable, target Stellaris version, and evidence requirements before loading topic skills. |
| `stl-scope-script-basics` | 00_foundation | PDXScript scope basics | Provide minimal scope rules for ROOT/THIS/FROM/PREV, exists checks, trigger/effect placement, and common wrong-scope failure modes. |
| `stl-source-triage` | 00_foundation | Evidence hierarchy | Choose which evidence types should decide the task: vanilla files, CWTools, generated docs, Irony, logs, runtime tests, mod pages, or old examples. |
| `stl-version-vanilla-baseline` | 00_foundation | Target version and vanilla baseline | Determine target Stellaris version, vanilla snapshot, DLC/beta assumptions, and whether a vanilla diff is required. |
| `stl-cwtools-schema-lookup` | 01_schema_and_research | CWTools schema lookup | Find the relevant CWTools CWT rule path and summarize allowed shape, scope, and known schema gaps for one folder/object type. |
| `stl-merge-semantics-research` | 01_schema_and_research | Merge/overwrite semantics | Investigate whether a specific surface merges, appends, replaces, de-duplicates, or has duplicate-ID ambiguity. |
| `stl-trigger-effect-docs` | 01_schema_and_research | Trigger/effect docs lookup | Verify exact trigger/effect names, parameter forms, scope expectations, and generated-doc freshness before using them. |
| `stl-vanilla-docs-diff` | 01_schema_and_research | Vanilla file diff | Compare a modded or copied object against the target vanilla version to detect stale keys, deleted blocks, new requirements, and full-file override risk. |
| `stl-vanilla-overrides-audit` | 01_schema_and_research | Vanilla override audit | List full-file and object-level vanilla overrides in a mod and rank porting/compatibility risk. |
| `stl-events-implementation` | 02_script_surfaces | Events implementation | Author country/planet/fleet/ship events with namespaces, triggers, immediate blocks, options, and localization hooks. |
| `stl-events-validation` | 02_script_surfaces | Events validation | Validate event IDs, namespaces, is_triggered_only, scope transitions, options, localization, and runtime errors. |
| `stl-on-actions-implementation` | 02_script_surfaces | on_actions implementation | Attach events/effects to game hooks and pulses with minimal frequency, correct scope assumptions, and safe registration. |
| `stl-on-actions-validation` | 02_script_surfaces | on_actions validation | Check duplicate IDs, nested event/random_event ambiguity, pulse frequency, merge winners, and runtime proof needs. |
| `stl-pulse-performance` | 02_script_surfaces | Pulse performance | Prevent daily/monthly/yearly pulses and galaxy-wide loops from over-scanning or over-firing. |
| `stl-scripted-effects` | 02_script_surfaces | Scripted effects | Create or review reusable effects with safe scope guards, clear side effects, cleanup, and namespaced IDs. |
| `stl-scripted-triggers` | 02_script_surfaces | Scripted triggers | Create or review reusable boolean conditions with explicit scopes, safe exists checks, and namespaced IDs. |
| `stl-ai-budgets-implementation` | 03_ai_economy_planets | AI budgets | Adjust AI spending categories, desired min/max, upkeep/expenditure types, and resource partitioning. |
| `stl-colony-types-designations` | 03_ai_economy_planets | Colony types and designations | Add or validate colony type weights, designation modifiers, AI resource conversion, and specialization alignment. |
| `stl-districts-buildings` | 03_ai_economy_planets | Districts and buildings | Add or repair districts/buildings, resources, potential/allow, upgrades, on_queued/on_built hooks, AI weights, and zone metadata. |
| `stl-economic-plans-implementation` | 03_ai_economy_planets | Economic plans | Tune or add economic plans/subplans for AI income, focus, pops, empire size, naval cap, scaling, and phase-specific priorities. |
| `stl-economic-plans-merged-validation` | 03_ai_economy_planets | Merged economic-plan validation | Reconstruct active economic plans/subplans and identify final winners, duplicate subplan overwrites, and load-order-dependent behavior. |
| `stl-jobs-pop-economy` | 03_ai_economy_planets | Jobs and pop economy | Define jobs, strata/categories, resources, upkeep/output, modifiers, unemployment implications, and AI-visible job output. |
| `stl-pop-groups-workforce` | 03_ai_economy_planets | Pop groups and workforce | Handle 4.x pop groups, workforce assignment, job efficiency, pop-count assumptions, and compatibility with old scripts/UI. |
| `stl-resources-modifiers` | 03_ai_economy_planets | Resources and modifiers | Manage strategic resources, economic categories, modifier keys, AI recognition, resource groups, and universal-patch dependencies. |
| `stl-zones-zone-slots` | 03_ai_economy_planets | Zones and zone slots | Implement or validate 4.x zones, zone sets, slot unlocks, building-set includes/excludes, conversion, AI priority, and UI visibility dependencies. |
| `stl-technologies` | 04_gameplay_domains | Technologies | Implement technologies, prerequisites, categories, feature flags, unlocks, tiers, rare weights, and localization. |
| `stl-components-slots-sets` | 05_ships_war_starbases | Components, slots, and sets | Validate component templates, slot templates, component sets, prerequisites, restrictions, resources, and AI-use metadata. |
| `stl-global-ship-designs` | 05_ships_war_starbases | Global ship designs | Check AI/default/global designs against sections, slots, required components, tech availability, and save/design validity. |
| `stl-ship-graph-validation` | 05_ships_war_starbases | Ship graph validation | Run a static graph validation of ship sizes, sections, component slots, component sets, behaviors, global designs, and required components. |
| `stl-ship-sizes-sections` | 05_ships_war_starbases | Ship sizes and sections | Validate/edit ship sizes, section slots, fits_on_slot graph, class restrictions, ship designer assumptions, and section geometry references. |
| `stl-starbases-orbital-rings` | 05_ships_war_starbases | Starbases and orbital rings | Implement and validate starbase levels, modules, buildings, ship-size files, orbital rings, UI slots, and cooldown effects. |
| `stl-gigastructure-safety` | 06_megastructures | Gigastructure safety | Assess high-power megastructure effects, crises, menus, resources, scripted triggers, vanilla overwrites, and save/runtime risks. |
| `stl-interface-gui` | 07_ui_localization_assets | Interface GUI/GFX | Edit or validate .gui/.gfx layout files, panels, topbar, planet view, ship designer, outliner, and compatibility patch ordering. |
| `stl-localization` | 07_ui_localization_assets | Localization | Add, validate, and troubleshoot localization yml keys, language headers, encoding, missing loc, duplicate keys, and dynamic loc references. |
| `stl-resource-topbar-ui` | 07_ui_localization_assets | Resource topbar UI | Patch resource groups/topbar visibility and ordering for new strategic resources and universal resource patches. |
| `stl-active-playset-inventory` | 08_validation_diagnostics | Active playset inventory | Read/produce enabled mods, Workshop IDs, descriptors, paths, versions, and load order for the active playset. |
| `stl-cwtools-diagnostics` | 08_validation_diagnostics | CWTools diagnostics | Run/read CWTools diagnostics and map warnings/errors to files, object families, and likely follow-up skills. |
| `stl-error-log-review` | 08_validation_diagnostics | Runtime log review | Read error.log, game.log, script.log, localization logs, and crash folders to map runtime errors to script surfaces. |
| `stl-irony-conflict-map` | 08_validation_diagnostics | Irony conflict map | Use Irony merged/conflict output to identify file/object winners, FIOS/LIOS behavior, and candidate patch targets. |
| `stl-load-order-rules` | 08_validation_diagnostics | Load-order rules | Apply maintainer-stated ordering rules and general Stellaris overwrite expectations before or alongside Irony verification. |
| `stl-observer-run-planning` | 08_validation_diagnostics | Observer-run planning | Plan safe observer runs with metrics, interval checks, copied saves, stop criteria, and comparison notes. |
| `stl-runtime-smoke-test` | 08_validation_diagnostics | Runtime smoke test | Design minimal new-game/console/copied-save tests for one feature with pass/fail signals and log checks. |
| `stl-savegame-safety` | 08_validation_diagnostics | Savegame safety | Assess whether a change is save-safe, new-game-only, copied-save-only, or requires migration/cleanup. |
| `stl-compat-expanded-starbases` | 09_compatibility | Expanded/Starbase Extended compatibility | Confirm exact workshop identity, then check starbase ship size, levels, modules, UI slots, UMP/UIOD dependencies, and NSC incompatibilities. |
| `stl-compat-gigastructures` | 09_compatibility | Gigastructural Engineering compatibility | Check Gigas megastructures, resources, UI patches, crises, on_actions, scripted triggers, vanilla overwrites, and patch order. |
| `stl-compat-nsc3` | 09_compatibility | NSC3 compatibility | Check NSC3 ship sizes, section files, starbase interactions, bioships, global designs, UIOD dependency, and save warnings. |
| `stl-compat-planetary-diversity` | 09_compatibility | Planetary Diversity compatibility | Check planet classes, startup events, zones, zone slots, districts, colony types, deposits, and UIOD/planet-view patch interactions. |
| `stl-compat-ship-stack` | 09_compatibility | Composite ship-stack compatibility | Validate final merged NSC3 + ESC NEXT + Spacefleet Tactica graph for sizes, sections, slots, components, behaviors, and global designs. |
| `stl-compat-spacefleet-tactica` | 09_compatibility | Spacefleet Tactica compatibility | Check SFT ship behavior AI, sections, combat computers, NSC/ESC/Gigas add-on rules, and AI design effects. |
| `stl-compat-stellar-ai` | 09_compatibility | Stellar AI compatibility | Compare AI economy, research, budgets, jobs, buildings, zones, colony types, personalities, and load-order assumptions against Stellar AI. |
| `stl-compat-uiod` | 09_compatibility | UI Overhaul Dynamic compatibility | Check UIOD load order, compatibility patches, planet view, ship designer, topbar/resource groups, outliner, and final UI winners. |
| `stl-compat-universal-patches` | 09_compatibility | Universal Resource/Modifier Patch compatibility | Check Universal Resource Patch and Universal Modifier Patch interactions, resource topbar display, economy categories, and dependencies. |
| `stl-compat-patch-authoring` | 10_packaging_release | Compatibility patch authoring | Create minimal patch-mod plans that override only necessary objects and document load-order assumptions. |
| `stl-packaging-descriptor-release` | 10_packaging_release | Packaging and release | Prepare local release structure, descriptor metadata, supported version, changelog, artifacts, and release checklist. |
| `stl-porting-version-bump` | 10_packaging_release | Version porting | Build a porting checklist from vanilla diff, deprecated keys, patch notes, schema changes, save risk, and regression saves. |