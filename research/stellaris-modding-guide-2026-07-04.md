# Stellaris Modding Guide

Date integrated: 2026-07-04

Primary source bundle: `research/stellaris-modding-research-bundle-2026-07-04/`

Use this guide as the fast-start operational layer for Codex and human work. The source bundle remains the evidence layer; source IDs such as `[S007]` resolve through `source_index.csv` and `source_index.json` in that bundle.

## Default Target

- Target Stellaris PC 4.4.4 stable unless the task explicitly says 4.4.5 beta, 4.5 beta, or another version.
- Use `supported_version="v4.4.*"` for stable 4.4 mods.
- Treat `supported_version` as launcher-facing metadata only; it does not determine whether game script loads.
- Treat 4.4.5 as a beta branch, especially for situation, automation, starbase module, and Arkship-equivalent additions.
- Treat 4.5 as a separate porting branch. Do not casually version-bump mods touching pops, factions, ethics, jobs, species, workforce, UI, or AI economy.

See:

- `CURRENT_VERSION_AND_STRUCTURAL_CHANGES.md`
- `PORTING_AND_REGRESSION_CHECKLISTS.md`
- `VALIDATION_CAVEATS_AND_OPEN_QUESTIONS.md`

## Source Order For Mod Work

1. Current user request.
2. Project `AGENTS.md` and this guide.
3. Current local vanilla files under `C:\Steam\steamapps\common\Stellaris`.
4. Current mod source files under `mods/`.
5. Source bundle evidence and matrices.
6. Irony Mod Manager conflict results.
7. CWTools diagnostics, generated script docs, and runtime logs.
8. Model inference only when no stronger source exists.

Do not invent triggers, effects, modifiers, scopes, folder names, or loader behavior. Verify them against current vanilla files, generated docs, CWTools, Irony, or runtime logs.

## Mod Structure Defaults

Keep project source under `mods/<ModName>/`. Do not mix source files with live launcher installation files.

A local playable mod needs a descriptor pair in the actual Stellaris user mod directory:

```text
C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\<mod_id>.mod
C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\<mod_id>\descriptor.mod
```

Rules:

- The outer `.mod` file includes `path`.
- The inner `descriptor.mod` does not include `path`.
- Mod folders mirror recognized Stellaris install folders such as `common/`, `events/`, `localisation/`, `localisation_synced/`, `gfx/`, and `interface/`.
- Use `localisation`, not `localization`.
- English localisation files go under `localisation/english/`, end in `_l_english.yml`, start with `l_english:`, and must be UTF-8 with BOM.

See:

- `MOD_STRUCTURE_AND_SETUP.md`
- `templates/stellaris_mod_skeleton/`
- `tables/file_structure_requirements.csv`

## Naming And Collision Rules

Pick a unique mod prefix before creating files. Prefix:

- object IDs;
- event namespaces and event IDs;
- localisation keys;
- files;
- scripted triggers and effects;
- flags and variables;
- asset paths where practical.

Avoid vanilla-like names such as `00_civics.txt` and generic keys such as `civic_example`. Additive unique-key content is safest. If overriding vanilla or another mod, isolate the key, document the source version, and record the conflict/test plan in the mod README.

## 4.4 Compatibility Cases

For mods touching economy, colonies, planets, wars, diplomacy, UI, starbases, automation, AI, or modifiers, explicitly test:

- a normal settled empire;
- a Nomadic Empire;
- Arkship colonies and modifier application;
- countries without normal colonies or capitals;
- Waystation UI;
- Wayline modifier stacking;
- Contract creation/cancellation;
- Nomad total-war ownership transfer;
- Situation Log and fleet automation UI when interface files are touched.

These are first-class compatibility cases for Stellaris 4.4.x, not edge curiosities.

## Conflict And Load Order Rules

Do not assume Stellaris is universally "last mod wins." Some content behaves like last-in-order-served, some behaves like first-in-order-served, and element-level behavior matters more than filename collisions.

Use this workflow for compatibility work:

1. Identify every vanilla key overridden.
2. Identify every other-mod key overridden.
3. Run Irony Mod Manager conflict analysis for real playsets.
4. Create a small compatibility patch for merged duplicate definitions.
5. Load the patch after source mods unless Irony or current loader evidence says otherwise.
6. Record unresolved conflicts and required load order.

See:

- `LOAD_ORDER_OVERRIDES_AND_CONFLICTS.md`
- `tables/override_conflict_matrix.csv`

## Validation Workflow

Before code generation, collect:

```text
TARGET_VERSION=4.4.4
MOD_PREFIX=<prefix>
TOUCHED_FOLDERS=<folders>
VANILLA_REFERENCES=<current vanilla files>
REQUIRED_COMPAT_MODS=<mods>
```

Static validation:

- Open the mod with CWTools configured against the current vanilla folder.
- Fix diagnostics rather than explaining them away.
- Search for unprefixed keys and copied vanilla filenames.
- Check localisation file name, header, and UTF-8 BOM.

Conflict validation:

- Use Irony Mod Manager for playset dependency, conflict, and load-order investigation.
- Document conflicts in the mod README or compatibility patch README.

Runtime validation:

- Launch a new game with only the mod.
- Launch a new game with the target playset.
- Test save/load.
- Read `error.log` first, then `game.log`.
- Use `-script_debug -debug_mode -debugtooltip -logall` when needed.
- Use `script_profiler` for recurring scripts or performance-sensitive changes.

Do not call a gameplay or UI mod ready until meaningful runtime validation has been recorded.

See:

- `MOD_SCHEMA_VALIDATION_WORKFLOW.md`
- `TROUBLESHOOTING_DEBUGGING_AI.md`
- `tables/debug_commands_and_tools.csv`

## Debug Packet For Codex

When asking Codex to debug a Stellaris mod, provide or generate:

```text
game version and checksum
active playset order
full mod tree
all changed files
vanilla reference files for touched paths
error.log
game.log
steps to reproduce
expected behavior
actual behavior
Ironman status
```

Codex should classify each error, identify wrong scopes, missing localisation, duplicate keys, invalid folders, stale overrides, and likely load-order conflicts, then return a minimal patch and test plan.

## LLM And External Bridge Boundary

No supported native in-engine LLM API was identified. Public LLM-adjacent projects use external save parsing, advisors, MCP relays, or console command-file bridges.

For any LLM bridge:

- treat saves as untrusted input;
- keep API keys out of the repo;
- use a whitelisted action schema;
- require human approval for destructive actions;
- audit every recommendation or action;
- never run arbitrary LLM-generated console commands.

See:

- `LLM_AI_PROJECTS_INVENTORY.md`
- `AI_LLM_ARCHITECTURE_SPEC.md`
- `templates/llm_bridge/action_schema.json`
