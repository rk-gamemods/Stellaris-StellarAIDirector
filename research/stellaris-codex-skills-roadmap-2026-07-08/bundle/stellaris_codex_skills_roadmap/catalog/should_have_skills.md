# should-have skills

Generated: 2026-07-08

| Skill ID | Category | Topic | Purpose |
|---|---|---|---|
| `stl-scripted-content-classifier` | 00_foundation | Task-to-surface classifier | Map a requested change to the smallest relevant Stellaris file surface and likely validation chain. |
| `stl-source-inventory-maintenance` | 00_foundation | Source inventory upkeep | Keep source lists, retrieval dates, confidence, caveats, and stale/dynamic-source warnings current for Codex handoffs. |
| `stl-cwtools-limitations` | 01_schema_and_research | CWTools limitation handling | Identify when CWTools can validate shape but cannot prove load-order winners, nested merge behavior, runtime scope semantics, or active-stack behavior. |
| `stl-generated-script-docs` | 01_schema_and_research | Generated docs inventory | Locate, generate, or refresh local trigger/effect/modifier/script documentation and record what version it represents. |
| `stl-object-id-inventory` | 01_schema_and_research | Object ID inventory | Build a narrow inventory of IDs for one object family across vanilla and enabled mods. |
| `stl-decisions-implementation` | 02_script_surfaces | Planet/empire decisions | Implement and validate decisions with cost, allow/potential, effects, AI weights, cooldowns, localization, and save-safety notes. |
| `stl-flags-variables-state` | 02_script_surfaces | Flags, variables, and state | Manage persistent state using flags, variables, event targets, cooldowns, and cleanup rules. |
| `stl-scripted-values` | 02_script_surfaces | Scripted values | Design reusable numeric formulas, constants, and AI weights without embedding large logic in other objects. |
| `stl-situations-scripted-actions` | 02_script_surfaces | Situations and scripted actions | Implement or validate situations, situation stages/approaches, scripted actions, automation blocks, and version-gated 4.4/4.5 syntax. |
| `stl-ai-catchup-construction-events` | 03_ai_economy_planets | AI catch-up construction events | Plan AI-only emergency catch-up events for severe unemployment/housing/job deficits when normal planning is too slow, with save-safety and semantic tests. |
| `stl-ai-construction-defines` | 03_ai_economy_planets | AI construction defines | Tune global AI construction thresholds, free-job caps, scoring multipliers, target expiry, and underdeveloped-planet knobs cautiously. |
| `stl-ai-personalities` | 03_ai_economy_planets | AI personalities | Tune AI personalities, aggression, diplomacy, expansion, research/military tendencies, and compatibility with strategy routes. |
| `stl-colony-automation` | 03_ai_economy_planets | Colony automation | Review colony automation categories, priority districts/zones, buildings, availability, and AI planet behavior hooks. |
| `stl-civics-origins-governments` | 04_gameplay_domains | Civics, origins, authorities, governments | Implement empire setup content including civics, origins, authorities, governments, start effects, and scripted gates. |
| `stl-diplomacy-subjects-federations` | 04_gameplay_domains | Diplomacy, subjects, federations | Tune diplomatic actions, subject contracts, federations, pacts, war joining, and coalition logic. |
| `stl-nomads-arkships-waylines` | 04_gameplay_domains | Nomads, Arkships, Waylines | Handle 4.4 Nomad/Arkship/Wayline assumptions around colonies, carriers, contracts, resources, UI panels, and war/diplomacy interactions. |
| `stl-policies-edicts` | 04_gameplay_domains | Policies and edicts | Implement policies/edicts with availability, AI weights, resources, cooldowns, and safe effects. |
| `stl-tech-ai-weights` | 04_gameplay_domains | Technology AI weights | Tune AI research choices, prerequisite paths, doctrine lanes, and avoiding incoherent sidegrades. |
| `stl-traditions-ascension-perks` | 04_gameplay_domains | Traditions and ascension perks | Add or patch traditions, ascension perks, adoption/finish effects, unlocks, and UI-safe localization. |
| `stl-fleet-doctrine-ai` | 05_ships_war_starbases | Fleet doctrine AI | Tie ship designs, tech weights, budget pressure, aggression, threat response, and doctrine specialization into coherent AI fleet behavior. |
| `stl-ship-behaviors-computers` | 05_ships_war_starbases | Ship behaviors and combat computers | Implement or validate combat computers, ship behaviors, ranges, class restrictions, and AI-use metadata. |
| `stl-megastructure-ai-planning` | 06_megastructures | AI megastructure planning | Make AI recognize, afford, prioritize, and sequence megastructures through tech, economy, budgets, and events. |
| `stl-megastructures-implementation` | 06_megastructures | Megastructures | Add or patch megastructure stages, placement rules, build/upgrade logic, resources, events, and localization. |
| `stl-icons-sprites-gfx` | 07_ui_localization_assets | Icons, sprites, and GFX | Add spriteTypes, icons, DDS/TGA assets, atlas paths, and icon references for resources, components, techs, and UI. |
| `stl-custom-audit-adapter` | 08_validation_diagnostics | Custom audit adapter | Design small local Python/Codex helper scripts to emit mods.json, overwritten_paths, object inventories, load_order, and validation inputs. |
| `stl-generated-artifact-validation` | 08_validation_diagnostics | Generator artifact validation | Validate deterministic generator outputs, expected files, diff cleanliness, static checks, and known manual-runtime questions. |
| `stl-performance-telemetry` | 08_validation_diagnostics | Performance telemetry | Define counters/logging for pulses, queues, economy, unemployment, fleets, script cost, and observer-run performance. |
| `stl-regression-reporting` | 08_validation_diagnostics | Regression reporting | Produce a compact before/after report listing files touched, diagnostics run, runtime results, unresolved questions, and next test. |
| `stl-ui-smoke-checklist` | 08_validation_diagnostics | UI smoke checklist | Define a minimal UI panel checklist for planet view, ship designer, topbar, outliner, diplomacy, situations, and save/reload checks. |
| `stl-compat-esc-next` | 09_compatibility | ESC NEXT compatibility | Check ESC components, reactors, weapon progression, global designs, techs, icons, and NSC3 ordering assumptions. |
| `stl-release-test-matrix` | 10_packaging_release | Release test matrix | Define clean/active-stack/beta save tests, UI checks, static validation, and pass/fail criteria for release readiness. |
| `stl-steam-workshop-update` | 10_packaging_release | Steam Workshop update | Plan Workshop upload/update metadata, description, thumbnail, visibility, dependencies, tags, and change-note discipline. |