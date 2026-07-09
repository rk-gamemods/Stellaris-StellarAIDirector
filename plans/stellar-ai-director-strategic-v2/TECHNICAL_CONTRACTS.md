# Stellar AI Director V2 Technical Contracts

Generated: 2026-07-08
Packet: Stellar AI Director Strategic V2 Roadmap Packet
Target: Stellaris PC 4.4.5 stable/current, backwards compatible with 4.4.4 where source-backed


## Contract Purpose

This document tells Codex what must be preserved while implementing the next phase. It is intentionally stricter than a normal roadmap because Stellaris AI modding can silently fail through wrong scopes, missing objects, load-order assumptions, stale parent objects, or validator blind spots.

## Source-Of-Truth Hierarchy

Codex must use sources in this order:

1. Current user instruction.
2. This V2 packet.
3. `02_PROJECT_CONTROL_AND_GUIDANCE.md` and `AGENTS.md` guidance embedded there.
4. Current local vanilla files from the target Stellaris install.
5. Current `mods/StellarAIDirector` source files.
6. Current generated artifacts and datasets in `research/stellar-ai/`.
7. Irony conflict/load-order evidence for the actual playset.
8. CWTools/generated script docs/runtime logs.
9. Inference, only when no stronger source exists and clearly labeled.

Do not use old observer runs, 4.4.4 reports, or archived launch notes as current proof unless the task explicitly revalidates them against 4.4.5 and current live descriptor/load state.

## Script-Surface Contracts

| Surface | Contract | Risk if violated |
| --- | --- | --- |
| `common/ai_budget` | Full-object overrides must identify source object, parent mod, and reason. Existing Director wins for megastructure/Gigas resource budgets must remain intentional and documented. | Silent budget conflicts or resource starvation. |
| `common/economic_plans` | Director-owned high-scale plan must keep survival, recovery, deficit, research, construction, trade-capacity, fleet-throughput, static-defense, and special-resource gates distinct. | AI may overbuild, collapse, or hoard unusable resources. |
| `common/buildings` / `common/districts` | Generated weights must preserve source-local variables and prerequisites. Use `ai_resource_production`/verified weight surfaces only. | Parser errors, invalid objects, or job spam. |
| `common/technology` | Route weights must target verified vanilla/mod technology IDs and preserve prerequisites. | AI may chase nonexistent or disconnected techs. |
| `common/traditions` / `common/ascension_perks` | Use route rationale and source-object provenance for every override. | AP/tradition drift away from research/economy/fleet payoff. |
| `common/federation_types` | Existing research federation override is allowed only because it is static-validated and avoids unsafe diplomacy/personality folders. | Diplomatic behavior can become unsafe if extended blindly. |
| `common/policies` / `common/edicts` | Preserve route-gated policy/edict weights; do not force player policies; do not invent policy options. | Invalid policy options or hidden behavior forcing. |
| `common/starbase_modules` / `common/starbase_buildings` | Starbase Extended and vanilla scopes must be verified; duplicate `potential` merges must remain handled by the generator. | Load errors or broken starbase AI. |
| `common/megastructures` | Keep verified route-copy overrides; broad Gigas rewrites require source/parser/conflict proof and queue-continuation evidence. | Stalled construction, broken Gigas scripts, or conflicts with parent settings. |
| `events` / `on_actions` | Events are for load proof, market/fleet safety, threat response, or verified hysteresis/cooldown only. No scenario forcing without approved design. | Event spam, forced behavior, performance issues. |
| `common/scripted_triggers` / `common/script_values` | Computed strategic state is preferred. Persistent flags/variables require verified need and cleanup. | Stale state, performance pulses, or scope errors. |
| `localisation` | Visible content must have localization; generated localization must validate header/keys. | Missing text, broken launcher/game UI. |

## Forbidden Or Gated Surfaces

These are not banned forever, but they are blocked until a task card explicitly completes its research gate.

| Surface | Default status | Gate to unblock |
| --- | --- | --- |
| `common/diplomatic_actions` | Do not generate. | Exact local winning object, AI acceptance mechanics, prerequisite chain, active-stack conflicts, and safe negative tests. |
| `common/personalities` | Do not generate broad rewrites. | Active-stack winning personality map, field-by-field merge plan, Irony conflict proof, runtime-safe acceptance strategy. |
| Direct NSC3 ship designs | Do not generate. | Source-verified ship-size/section/component graph and loader semantics. |
| ESC component-template `key = ...` handling | Do not generate direct overrides. | Atlas must model loader surface safely; component-template row extraction and reference checks pass. |
| Section templates and ship sizes | Do not generate. | Winning-object graph and conflict analysis prove safe scope. |
| Broad Gigas object rewrites | Do not generate beyond verified route copies. | Parser proof, conflict proof, route edge proof, and queue/continuation plan. |
| Forced wars / join wars / punitive CBs | Do not generate in V2 core. | Separate war-chain plan, direct-threat/capability/proximity/cooldown gates, negative tests, explicit user approval if behavior changes gameplay aggressively. |
| Hidden AI bonuses | Do not generate. | Separate balance-mode decision from user. |

## Threat-Response Contract

The current V1 threat-response layer remains bounded:

- Unknown or unclassified war goals are inert until manually classified and tested.
- Generated files must not declare wars, join wars, add casus belli, override diplomatic actions, or force `wg_*` dispatch.
- Third-party defensive readiness economy pressure must remain behind `staid_tr_foreign_affairs_safe` or its verified successor.
- Any parser issue around `using_war_goal` syntax must be treated as a validator failure and fixed by source-backed syntax, not guessed.

## Generator Contracts

Codex must keep the generator as the owner of generated outputs.

| Contract | Rule |
| --- | --- |
| Generated files are reproducible | `python tools/generate_stellar_ai_director_patch.py` must recreate generated mod/research artifacts without hand edits. |
| Source-local variables preserved | Copied parent objects must include required `@variables` and inline scripts needed for parse context. |
| Provenance comments | New full-object overrides must identify parent object, source path, policy route, and why Director wins. |
| Optional-mod references guarded | A generated reference to an optional mod object must be omitted or guarded unless the generator proves it exists in vanilla, parent mod, or generated outputs. |
| Stable namespace | New Director-owned IDs use `staid_` or a more specific sub-prefix such as `staid_tr_`. |
| No hand-edited generated outputs | Fix generator code/data, not generated text files, unless doing an emergency local diagnosis that is reverted into generator ownership before commit. |
| Deterministic ordering | Generated object order should be stable to keep diffs reviewable. |
| Dataset updates | Large CSVs are catalogs; generated reports must state row counts and limitations. |

## Validation Contracts

Minimum local static gate for implementation slices:

```powershell
python tools\generate_stellar_ai_director_patch.py
python tools\validate_stellar_ai_director_patch.py
python -m py_compile tools\stellar_ai_director_lib.py tools\generate_stellar_ai_director_patch.py tools\validate_stellar_ai_director_patch.py
python -m unittest discover -s tools\tests
git diff --check
```

Add surface-specific checks as the task requires:

| Area | Required checks |
| --- | --- |
| Object atlas | `python tools/build_stellar_ai_director_object_atlas.py` when route/source coverage changes. |
| File/reference audits | Generated file, reference, conflict, integration, and route audits must update when generated surfaces change. |
| Irony conflicts | Classify conflicts as intentional Director wins, parent wins required, harmless additive duplicates, unexpected conflicts, or false positives. |
| CWTools | Use where available for syntax/schema feedback, especially new PDXScript folders. |
| Runtime logs | Runtime only with approval; inspect `error.log` before `game.log`. |
| Observer harness | `python tools\manage_stellaris_commands_at_date.py status` before/after any approved observer run. |

## Compatibility Contracts

| Mod/system | Contract |
| --- | --- |
| Gigastructural Engineering & More (4.4) | Preserve route, budget, and special-resource support. Do not claim queue optimization until save/observer evidence shows continuation and upgrade sequencing. |
| NSC3 | Current safe path is tech/resource/fleet-throughput support. Direct ship-design handling remains research-gated. |
| Extra Ship Components NEXT | Current safe path is technology/resource readiness. ESC internal component-template handling remains research-gated. |
| Starbase Extended 3.0 | Use verified starbase module/building scopes and Irony conflict results before expanding defense AI. |
| UI Overhaul Dynamic | Director should not introduce UI files unless a future user-approved UI task exists. Coordinate load-order notes only. |
| Universal Resource Patch | Keep after-parent load-order expectations and do not flatten unique resources into generic resources. |
| Planetary Diversity | Preserve targeted planet/outpost value support; broad designation rewrites require winning-object inventory. |
| Major AI/performance mods | Do not stack behavior assumptions. Research overlap, conflict winners, and performance throttles before recommending compatibility. |
| Nomads/Arkships/Waystations | Treat 4.4.x Nomad, Arkship, Wayline, Contract, Waystation, and Operational Reserve surfaces as required compatibility cases when touched. |

## Descriptor, Load Order, And Live Launcher Contracts

- `supported_version="v4.4.*"` remains launcher metadata for 4.4-line support.
- The source mod folder is not automatically the live launcher mod. Codex must report live descriptor path and `dlc_load.json` state separately when readiness is discussed.
- Stellar AI is not a required parent. Keep it only as private parity/reference evidence.
- Director should load after Gigastructural Engineering, NSC3, Extra Ship Components NEXT, Starbase Extended, Universal Resource Patch, and compatibility patches whose AI/economy behavior it coordinates.
- Director should load before any future local patch that intentionally overrides Director.

## README, Notes, And Release Contracts

Codex must update docs when behavior changes:

| File | Update when |
| --- | --- |
| `mods/StellarAIDirector/README.md` | New user-facing behavior, target version, dependencies, validation commands, or non-goals. |
| `mods/StellarAIDirector/notes/load-order.md` | Parent list, load position, Irony evidence, or standalone dependency wording changes. |
| `mods/StellarAIDirector/notes/conflicts.md` | New intentional overrides, conflict classifications, or parent-win requirements. |
| `mods/StellarAIDirector/notes/tuning-notes.md` | Strategy/tuning goals, runtime metrics, observer hypotheses, or balance decisions. |
| `mods/StellarAIDirector/notes/observer-test-log.md` | Only when runtime or save-inspection evidence is actually collected. |
| `research/stellar-ai/*.md` | Any durable evidence, gap, route, audit, or user-approved runtime result. |

## Stop Conditions

Stop the implementation slice and report clearly if any of the following occur:

- Required local source files or Munch indexes are stale or inaccessible.
- A proposed surface is not verified in vanilla/mod/generated docs.
- A generated object references missing triggers/effects/resources/techs/objects.
- A high-risk folder would be generated without an explicit gate.
- Validation fails after regeneration.
- Irony shows unexplained Director conflicts.
- Runtime logs show new repeated Director problem lines after an approved runtime check.
- `commands_at_date.txt` is unexpectedly present outside an approved observer run.

## Codex Status Reporting Contract

Every implementation handoff must explicitly report:

```text
Status:
- Live mod: updated / not updated / not checked. Evidence: ...
- Commit: committed <sha> / uncommitted changes / staged only / clean at <sha>.
- Push: pushed / not pushed / not checked. Evidence: ...
```

Do not imply source edits are live-launch ready unless the launcher descriptor and `dlc_load.json` were checked.
