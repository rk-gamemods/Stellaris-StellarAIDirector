> Snapshot commit: `27aa7547b610e2876d897771a804656453f948ee` | Branch: `master` | Working tree: `dirty` | Generated: `2026-07-08T15:18:04-04:00`

# Project Control And Guidance

Read these files before interpreting mod source, research packets, generated evidence, or validation claims.

## .gitignore

```text
# Local/editor state
.vscode/
.idea/
*.swp
*.tmp
Thumbs.db
Desktop.ini

# Codex/runtime scratch
.codex/
tmp/
temp/
__pycache__/
*.py[cod]

# Stellaris/generated packaging outputs
*.zip
*.7z
*.rar
dist/
build/
exports/

# Large or local-only reference drops
vanilla-dumps/
local/
*.local.*

# Stellaris observer-run bulky artifacts
# Keep small run metadata/checkpoints/summaries trackable, but do not make Git
# account for copied raw logs, savegames, screenshots, or extracted save dumps.
research/stellar-ai/observer-runs/**/logs/*.log
research/stellar-ai/observer-runs/**/saves/*.sav
research/stellar-ai/observer-runs/**/screenshots/*.png
research/stellar-ai/observer-runs/**/screenshots/*.jpg
research/stellar-ai/observer-runs/**/screenshots/*.jpeg
research/stellar-ai/observer-runs/**/exports/
```

## AGENTS.md

```markdown
# Stellaris Modding Instructions

This folder is for Stellaris modding, mod preparation, experiments, and supporting research.

## Working Rules

- Keep each mod in its own folder under `mods/`.
- Keep reusable notes, compatibility research, and source references under `research/`.
- Keep images, icons, generated art, and source asset files under `assets/`.
- Keep one-off scripts or repeatable helper tools under `tools/`.
- Keep planning notes and rough design notes under `notes/`.
- Do not mix live game installation files with source project files.
- Preserve original references and vanilla file excerpts when they are used to justify a change.

## Project Memory And Tooling Continuity

- Treat Open Brain as a first-class project history for this repository. At the start of any non-trivial Stellaris task, search relevant Open Brain memories for this project, the current mod or tool, prior user corrections, and known failure modes before planning or editing.
- At every meaningful completion, milestone, correction, blocker, or handoff, save an Open Brain memory summary. The summary must answer who asked, what was requested, what was done, where it was done, when it happened, why it mattered, how it was implemented or verified, files or tools touched, validation results, remaining risks, and next recommended action.
- Do not leave important project history only in chat. If a prior part of the current conversation produced useful decisions, corrections, tools, research, generated files, validation, or unresolved risks without a memory, backfill concise Open Brain memories before continuing.
- If Open Brain MCP capture is unavailable, emit a `memory_candidate` with the same who/what/where/when/why/how fields so it can be captured later. Do not claim that memory was saved unless `capture_thought` succeeded.
- Prefer a few retrieval-friendly paragraphs per completed work slice over forcing future agents to reconstruct intent from large chat histories, raw logs, or generated artifacts alone.

## Munch Tooling Requirements

- JDocMunch, JCodeMunch, and JDataMunch are first-class tools for this project. Use them for documentation, code, and data navigation when relevant; do not silently replace them with broad file reads or ad hoc shell searches.
- Route by artifact type before searching: use JDocMunch for prose documentation, Markdown plans, guide sections, and research notes; use JCodeMunch for source code, scripts, generated code, symbols, and code references; use JDataMunch for CSV, TSV, Excel, Parquet, JSONL/NDJSON, and any row/column dataset. Do not use JDocMunch as the primary inspection surface for CSV or other tabular data.
- For tabular research artifacts, call `jdatamunch_guide`, then `list_datasets`. If the needed file is missing or stale, run `index_local` with a stable project-specific dataset name, then use `describe_dataset`, `sample_rows`, `get_rows`, joins, aggregates, or SQL-style JDataMunch tools instead of reading the file into chat. Validate important refreshed datasets with `validate_index` before relying on them for conclusions.
- JDocMunch may be used to locate prose that references a CSV or to navigate a Markdown companion document, but it is not a substitute for JDataMunch row/column inspection. If JDataMunch fails and a temporary fallback is unavoidable, record the exact JDataMunch tool attempted, the error or remount requirement, and the fallback scope before continuing.
- Before non-trivial Stellaris work, obey the global Munch MCP startup gate: exact guide discovery, active-thread guide calls, and `C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1`. Do not continue Munch-dependent project work when active-thread guide calls fail, even if CLI fallbacks work.
- For JDocMunch specifically, partial lazy-loaded tool discovery is not proof of unavailability. Before using a CLI fallback or reporting missing tools, run exact discovery for the canonical tools: `jdocmunch_guide`, `search_sections`, `get_section`, `get_sections`, `list_docs`, `get_doc`, `get_toc`, `verify_index`, and `index_local`.
- For JDataMunch specifically, partial lazy-loaded tool discovery is not proof of unavailability. Before using a CLI fallback or reporting missing data tools, run exact discovery for the canonical tools needed by the guide, including `jdatamunch_guide`, `list_datasets`, `index_local`, `validate_index`, `describe_dataset`, `sample_rows`, `get_rows`, and any needed analysis or join tool.
- Start JDocMunch work by calling `jdocmunch_guide` when the MCP tool is exposed. If exact discovery exposes tools but an MCP call fails with `Transport closed`, classify the cause as a tool-surface problem such as stale active-session handle, remount requirement, config/version issue, or process failure. Do not phrase it as "JDocMunch is unavailable" without that diagnosis.
- When JDocMunch MCP fails but the installed CLI works, use the CLI only as a temporary fallback while recording the exact blocker and likely recovery path. Save the conclusion in Open Brain before finishing the task.
- Do not launch nested Codex sessions as a routine Munch preflight. Multiple live Munch MCP server processes are diagnostic in Codex Desktop stdio sessions, not by themselves a reason to kill processes or block work when active-thread guide calls return content. If guide calls return `Transport closed`, treat the active thread as stale/remount-required and follow the global Munch gate.
- Tested recovery for stale Munch handles in this project: fork the current Codex thread into the same directory, then rerun exact guide discovery, all three mounted guide calls, and the patched preflight. The same-directory fork reset `Transport closed` without closing Codex; do not rely on process killing as the reset mechanism.
- For local Stellaris project indexing, keep JDocMunch embeddings disabled unless the user explicitly asks to enable them. Prefer `use_embeddings=false` or `JDOCMUNCH_EMBEDDING_PROVIDER=none` for index refreshes.

## Stellaris Modding Defaults

- Target Stellaris PC 4.4.5 stable/current local install unless the task explicitly says 4.4.4 rollback, 4.5 beta, or another version.
- Use `supported_version="v4.4.*"` for stable 4.4 descriptors, including 4.4.5, but remember this is launcher-facing metadata only and does not determine whether script code loads.
- Treat 4.4.4 notes and generated evidence as historical/rollback references unless revalidated against current 4.4.5 vanilla files, active-stack inventories, conflicts, and runtime logs. Treat 4.5 as a separate porting branch, especially for pop, faction, ethic, job, species, workforce, UI, and AI-economy changes.
- Prefer small, focused mods with clear compatibility boundaries.
- Document which vanilla files, scripted effects, defines, events, assets, or localization keys a mod touches.
- Use stable namespaces and prefixes for custom content to avoid collisions with other mods.
- Keep localization keys explicit and grouped by mod.
- Treat overwrite-style changes as high-risk. Prefer additive files and scoped patches when Stellaris supports them.
- Record game version and DLC assumptions before implementing or testing a mod.
- Before editing an existing mod, identify whether the work affects gameplay scripts, UI, localization, graphics, dependencies, or packaging.
- Do not invent triggers, effects, modifiers, scopes, folder names, or loader behavior. Verify unfamiliar surfaces against current vanilla files, generated docs, CWTools, Irony, or runtime logs.
- Treat Nomads, Arkships, Waystations, Waylines, Contracts, and the 4.4 Situation Log as required compatibility cases when a mod touches relevant economy, colony, planet, war, diplomacy, UI, starbase, automation, AI, or modifier behavior.

## Local Stellaris Tooling

- Treat Irony Mod Manager as a project-local Stellaris tool, not a global Codex tool.
- Irony Mod Manager is installed at `C:\Users\Admin\AppData\Local\Programs\Irony Mod Manager`.
- Irony executable: `C:\Users\Admin\AppData\Local\Programs\Irony Mod Manager\IronyModManager.exe`.
- Irony stores user data under `C:\Users\Admin\AppData\Roaming\Mario`.
- Use Irony for Stellaris mod dependency, conflict, and load-order investigation when building or reviewing mod lists.
- Local Steam Stellaris install: `C:\Steam\steamapps\common\Stellaris`.
- Local Steam Workshop Stellaris content: `C:\Steam\steamapps\workshop\content\281990`.
- Local Paradox Stellaris user folder: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris`.
- Local Paradox launcher mod folder: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod`.
- Current integrated modding guide: `research/stellaris-modding-guide-2026-07-04.md`.
- Full attached research bundle: `research/stellaris-modding-research-bundle-2026-07-04/`.
- Stellaris reads `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\commands_at_date.txt` as live game-control input. Treat this file as a temporary observer-run harness only, never as a persistent project artifact. Do not copy or edit it by hand. Use `python tools\manage_stellaris_commands_at_date.py status|enable|disable`; enable only for an explicitly user-approved AI observer/testing run, disable it before normal play or handoff, and report the status.
- For explicitly approved observer simulations, `game_speed 5` is intentional. It unlocks the dev-only faster speed displayed by the UI as `GAME_SPEED_6`; do not downgrade observer harnesses or instructions to `game_speed 4` based on help text or old notes.

## Delivery Status Reporting

Every final or substantive status answer for Stellaris mod work must end with an
explicit, current status block covering all three surfaces below. This is a
reporting requirement, not a requirement that every task must be committed,
pushed, or live-installed.

- Live mod launch status: state whether the actual mod that Stellaris will load
  on the next game launch is updated. Check and report the relevant launcher
  descriptor under `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod`,
  the descriptor `path=...`, and whether `dlc_load.json` or the active launcher
  surface includes the mod when that is relevant. If the live-launch surface was
  not checked, say `not checked`; do not imply live readiness from project files
  alone.
- Commit status: state the current Git branch, whether the worktree is clean,
  whether relevant changes are uncommitted, staged, or committed, and the latest
  commit SHA/message when committed. Do not use words such as "done",
  "complete", "ready", or "good to go" without this status.
- Push status: state whether the current commit is pushed to the remote, the
  remote/branch checked, and the exact relationship such as
  `master...origin/master`, `ahead`, `behind`, or matching SHA. If no push was
  performed or remote status was not checked, say so explicitly.

Use a concise block like:

```text
Status:
- Live mod: updated / not updated / not checked. Evidence: ...
- Commit: committed <sha> / uncommitted changes / staged only / clean at <sha>.
- Push: pushed to <remote>/<branch> at <sha> / not pushed / not checked.
```

## User Mod Preferences

- Do not recommend Real Space by default. The user dislikes its UI/readability impact and finds it makes ships harder to see.
- Do not prioritize Star Wars themed total conversions or mod sets by default.
- Prioritize compatibility research for Gigastructural Engineering, NSC3, ship/component expansion mods, UI dependencies, smarter AI mods, and performance optimizers.
- For AI mods, specifically check whether the AI can use advanced systems added by major mods such as Gigastructural Engineering, NSC3, and ship/component expansions.
- For performance optimizers, verify what gameplay behavior they change and whether they introduce compatibility risks before treating them as safe QoL.
- Also prioritize strong space station, starbase defense, planetary defense, planetary weapon, and orbital-bombardment-resistance mods when they are current and compatible.
- Prioritize extra trait, leader-trait, origin, civic, ethic, tradition, ascension, and empire-creation options when building or recommending playsets.
- The user likes being able to create very strong or thematic empires, including immortal or long-lived leader concepts such as elf-like empires whose leaders do not die of old age.
- When researching trait and empire-creation mods, check whether options can appear for AI-controlled empires as well as player-designed empires.
- For Workshop collection recommendations, pre-filter aggressively for quality before content matching: current target game version, recent maintenance, meaningful ratings/favorites/subscribers/downloads, visible load-order guidance, active creator maintenance, and no obvious "not enough ratings", stale, waiting-for-update, removed, incompatible, or reported-problem signals.
- Prefer a smaller high-confidence maintained collection plus manual additions over a giant low-signal collection that happens to contain many matching keywords.
- When modifying a collection, distinguish low-risk visual flavor such as shipsets, portraits, flags, namelists, rooms, clothing, and simple graphics from heavy scripted gameplay systems, AI changes, event packs, performance-sensitive battle visuals, and large overhauls. Do not remove simple visual/theme mods merely because their theme is not a priority; focus caution on systems that affect scripts, balance, performance, dependencies, or load-order patches.

## Suggested Mod Folder Shape

```text
mods/<ModName>/
  README.md
  descriptor.mod
  common/
  events/
  gfx/
  interface/
  localisation/
  notes/
```

Only create folders a mod actually needs.

## Validation Expectations

- Check file paths and names against current Stellaris mod loading conventions before packaging.
- Verify syntax for edited game data files before considering a mod ready.
- Use CWTools diagnostics for PDXScript syntax/schema feedback when available.
- Use Irony Mod Manager for dependency, conflict, and load-order investigation on real playsets.
- Do not assume Stellaris is universally "last mod wins"; validate actual element-level conflict behavior.
- Do not launch Stellaris, run observer games, or run scenario simulations by default. Only do runtime/game validation when the user explicitly asks for it. Default validation is static: generated file surfaces, parser/load-safety, unresolved placeholders, and references to Stellaris/mod objects that must exist in vanilla, parent-mod, or generated inventories.
- Before and after any explicitly approved observer run that uses dated console commands, check `python tools\manage_stellaris_commands_at_date.py status`. The live `commands_at_date.txt` must be absent outside that active run. If it exists unexpectedly, disable it with `python tools\manage_stellaris_commands_at_date.py disable` and record the cleanup.
- Observer command schedules must use `game_speed 5` for the dev-only speed shown in-game as `GAME_SPEED_6`; static tests should catch accidental regressions to `game_speed 4`.
- Keep automated tests for fast universal safety checks only: valid generated files, parseable PDXScript/localization surfaces, known override targets, and valid referenced technologies, resources, scripted triggers, scripted values, or other game/mod entities. Do not encode fast-moving AI strategy, target numbers, decision behavior, launch proof, or observer outcomes as required tests; document that intent in code comments and notes instead.
- Record known conflicts, required DLC, and tested game version in the mod README.

## Research Expectations

For any non-trivial mod, create a note in `research/` or the mod's own `notes/` folder that captures:

- target Stellaris version;
- relevant vanilla files inspected;
- likely compatibility conflicts;
- DLC assumptions;
- test steps;
- open questions.
```

## README.md

```markdown
# Stellaris Mods

Starter workspace for Stellaris modding and mod preparation.

## Folder Map

| Path | Purpose |
| --- | --- |
| `mods/` | Source folders for individual Stellaris mods. |
| `research/` | Vanilla file notes, compatibility findings, game-version research, and modding references. |
| `assets/` | Source art, icons, image exports, generated visuals, and other reusable assets. |
| `tools/` | Local scripts or helpers used for validation, packaging, or analysis. |
| `plans/` | Durable implementation plans and remaining-work trackers. |
| `notes/` | Early ideas, task notes, and rough planning that has not become mod-specific yet. |

## Current Modding Baseline

- Default target is Stellaris PC 4.4.5 stable/current local install unless a task explicitly says 4.4.4 rollback, 4.5 beta, or another version.
- Use `supported_version="v4.4.*"` for stable 4.4 descriptors, including 4.4.5, while remembering this is launcher-facing metadata only.
- Treat 4.5 as a separate porting branch for pop, faction, ethic, job, species, workforce, UI, and AI-economy work.
- Treat Nomads, Arkships, Waystations, Waylines, Contracts, and the 4.4 Situation Log as required compatibility cases when touched by a mod.

Start with `research/stellaris-modding-guide-2026-07-04.md` for the operational guide. The full evidence bundle is preserved under `research/stellaris-modding-research-bundle-2026-07-04/`.

## Starting A Mod

1. Create `mods/<ModName>/`.
2. Add a short `README.md` describing the idea, target Stellaris version, expected DLC assumptions, and known compatibility risks.
3. Choose a unique mod prefix and use it for files, object IDs, event namespaces, localisation keys, flags, variables, and scripted triggers/effects.
4. Add only the Stellaris folders the mod needs, such as `common/`, `events/`, `gfx/`, `interface/`, or `localisation/`.
5. Keep research evidence in `research/` or `mods/<ModName>/notes/`.
6. Validate paths, syntax, conflicts, and in-game behavior before calling the mod ready.

## Validation Shortlist

- Check current vanilla files before using unfamiliar triggers, effects, modifiers, scopes, or folder paths.
- Use CWTools diagnostics for syntax/schema feedback when editing PDXScript.
- Use Irony Mod Manager for dependency, conflict, and load-order investigation on real playsets.
- For explicitly approved runtime validation, launch-test with only the mod, then with the target playset.
- Record `error.log`, `game.log`, known conflicts, required DLC, and tested game version in the mod README.

## Current Status

No specific Stellaris mod has been created yet. This project now includes dated 2026-07-04 research for mod structure, version hazards, conflict handling, validation, debugging, playset maintenance, and LLM-adjacent external tooling.
```

## mods/README.md

```markdown
# Mods

Create one folder per Stellaris mod here.

Default to Stellaris PC 4.4.5 stable/current local install unless the mod README says otherwise. Use `supported_version="v4.4.*"` for stable 4.4 descriptors, including 4.4.5.

Each mod should include its own `README.md` with:

- mod purpose;
- target Stellaris version;
- required or assumed DLC;
- touched vanilla systems;
- mod prefix;
- object keys added or overridden;
- localisation keys added or overridden;
- compatibility notes;
- test checklist.

## Mod Folder Rules

- Use unique, prefixed filenames instead of vanilla-like names such as `00_civics.txt`.
- Add only folders the mod actually needs.
- Keep source project files here, not in the live Stellaris launcher mod directory.
- When preparing a playable local copy, use the descriptor pair described in `research/stellaris-modding-guide-2026-07-04.md`.
- Treat overwrites, copied vanilla files, UI files, and `replace_path` as high-risk until validated against current vanilla files and Irony conflict results.

The attached research bundle includes a starter skeleton at `research/stellaris-modding-research-bundle-2026-07-04/templates/stellaris_mod_skeleton/`.

## Local 4.4 Replacements

- `StellarAIDirector/` - AI budget/priority patch for the Irony playset.
- `RKImmortalLeadersTrait/` - local 4.4 replacement for the old Immortal Leaders Trait mod.
- `RKCheatTraits44/` - local 4.4 replacement for udk Cheat Traits; use this for effectively unlimited custom empire trait points/picks.
- `RKGodlyTraitsRedux44/` - local 4.4 compatibility copy of Godly Traits Redux 4.0 with powerful species and leader traits.
- `RKMoreTraitPoints/` - local 4.4 replacement for More Trait Points; do not stack with other species-archetype trait-point mods.
- `RKMilitusExtraTraitPicks/` - local 4.4 replacement for Militus' Extra Trait Points; do not stack with other species-archetype trait-point mods.
- `RKThreeCivicMoreTraitPointsPicks/` - local 4.4 replacement for 3 Civic Points + More Trait Points/Picks; do not stack with other species-archetype trait-point mods.
```

## research/README.md

```markdown
# Research

Use this folder for Stellaris modding references, vanilla file notes, compatibility findings, and game-version research.

Keep notes source-backed when possible. Include file paths, game version, DLC assumptions, and date checked.

## Primary Guides

| Path | Use |
| --- | --- |
| `stellaris-modding-guide-2026-07-04.md` | Fast-start operational guide for Stellaris 4.4.x mod work. |
| `stellaris-modding-research-bundle-2026-07-04/` | Full attached research bundle with source IDs, reports, matrices, templates, and validation notes. |
| `stellaris-codex-modding-guide-packet-2026-07-08/` | Versioned supplement for the attached Codex modding guide packet, verified against local Stellaris 4.4.5 vanilla files and the active 120-mod playset. |
| `stellaris-codex-skills-roadmap-2026-07-08/` | Preserved consolidated roadmap bundle and indexed source package for creating small, topic-based Stellaris Codex skills. |
| `stellar-ai/war-mechanics-reference-2026-07-08/` | Focused external AI war-mechanics packet for claims, CBs, war goals, declaration gates, personality war fields, war defines, fleet-use separation, and passive-galaxy diagnosis. Use as a research reference, then verify against local vanilla and active-stack files before code changes. |
| `local-stellaris-environment-2026-07-04.md` | Local install, Workshop, launcher, and Irony paths verified on this machine. |
| `stellaris-30-day-research-2026-07-04.md` | Recent modding and game-state research rollup. |
| `stellaris-preferred-collections-2026-07-04.md` | User-preferred collection and compatibility research notes. |
| `stellaris-traits-collection-research-2026-07-04.md` | Updated collection research after adding trait, empire-creation, and immortal-leader preferences. |
| `stellaris-collection-2473560875-instructions-2026-07-04.md` | Deep dive on the recommended collection's author instructions, intended use, optional modules, and modification risks. |
| `stellar-ai/` | Focused research project for Stellar AI as the baseline AI mod and likely center for compatibility adjustments. |
| `steam-collection-2473560875-irony-mod-list-2026-07-04.txt` | Raw Irony clipboard list copied from the collection author's Steam discussion, updated there on 2026-07-02. |
| `steam-collection-2473560875-irony-remoteid-filters-2026-07-04.txt` | Generated remote-ID filter chunks for bulk-selecting collection mods in Irony's Installed Mods panel. |
| `irony-import-workflow-collection-2473560875-2026-07-04.md` | Corrected workflow for using Irony with already-subscribed Steam collection mods; explains ZIP import versus clipboard order import. |
| `stellaris-webchatgpt-reconciliation-2026-07-04.md` | Reconciliation notes for external research packets. |

## Source Bundle Use

The source bundle's Markdown reports cite sources with IDs such as `[S007]`. Resolve those IDs through:

- `stellaris-modding-research-bundle-2026-07-04/source_index.csv`
- `stellaris-modding-research-bundle-2026-07-04/source_index.json`
- `stellaris-modding-research-bundle-2026-07-04/RESEARCH_EVIDENCE_NOTES.md`

For implementation, start with the synthesized guide and then open the specific bundle file for the surface being changed:

- version and porting: `CURRENT_VERSION_AND_STRUCTURAL_CHANGES.md`
- structure and descriptors: `MOD_STRUCTURE_AND_SETUP.md`
- conflicts and load order: `LOAD_ORDER_OVERRIDES_AND_CONFLICTS.md`
- validation: `MOD_SCHEMA_VALIDATION_WORKFLOW.md`
- debugging: `TROUBLESHOOTING_DEBUGGING_AI.md`
- playset maintenance: `PLAYSET_INSTALLATION_MAINTENANCE.md`
- LLM/external bridge design: `AI_LLM_ARCHITECTURE_SPEC.md`
```

## notes/README.md

```markdown
# Notes

Use this folder for early ideas, task notes, and rough planning before a specific mod folder exists.

Move durable mod-specific notes into that mod's own folder once the mod takes shape.

```

## plans/README.md

```markdown
# Plans

Durable implementation plans live here.

Use this directory for written, updateable plans that need to survive beyond a
single chat turn. Keep rough ideas in `notes/`, evidence and source research in
`research/`, generated or hand-authored mod source in `mods/`, and repeatable
automation in `tools/`.

## Current Plans

- [Stellar AI Director V1 Remaining Work](stellar-ai-director-v1-remaining-plan.md)
- [Stellar AI Director Threat Response Source Plan](stellar-ai-director-threat-response-plan.md)
- [Stellar AI Director Threat Response Focused Plan Set](stellar-ai-director-threat-response/README.md)

## Update Rules

- Update the plan status when a task moves from planned to in progress, done,
  deferred, or replaced.
- Keep status entries evidence-backed with file paths, commands, or manual test
  notes.
- Do not leave major decisions only in chat. Summarize them in the relevant
  plan and capture durable milestones in Open Brain.
- Do not use Mermaid diagrams in these plans unless the user explicitly asks
  for them; keep the documents readable as plain Markdown.
```

## plans/stellar-ai-director-threat-response-plan.md

```markdown
# Stellar AI Director Threat Response Full Implementation Plan

Status: planning document only. No implementation has been performed from this plan yet.
Target game version: Stellaris PC 4.4.4 stable.
Captured: 2026-07-05.

Review annotation, 2026-07-05: this file is now the source brief for the focused plan set in `plans/stellar-ai-director-threat-response/`. Use that folder for implementation handoff, testing, risk mitigation, runtime interaction clarifications, and expanded acceptance gates. Preserve this document as the original integrated plan unless a later design decision intentionally replaces it.

## Summary

Implement a bounded, personality-weighted galactic threat-response layer for Stellar AI Director. This layer reacts to aggressive wars that other empires can observe, but it does not replace vanilla survival logic, Stellar AI economic logic, or Director recovery/deficit gates.

The concepts `moral_outrage`, `regional_fear`, `shared_threat_cooperation`, `conquest_respect`, `punitive_pressure`, `defensive_readiness`, and `opportunism` are not native Stellaris concepts. They are Director-owned design axes stored in the Python generator, compiled into concrete PDXScript artifacts that Stellaris can execute.

V1 outputs only:

- tiered opinion toward the aggressor;
- tiered shared-threat opinion toward victims/other threatened observers;
- timed country/relation flags;
- one small defensive-readiness economy pressure path;
- validation/reporting for unclassified war goals.

V1 explicitly does not force wars, join wars, add punitive CBs, overwrite diplomatic actions, or bypass survival/recovery/deficit gates.

## Verified Stellaris Primitives

Use only primitives verified in the local Stellaris 4.4.4 install:

- `on_war_beginning`
- `is_war_participant`
- `any_attacker`
- `any_defender`
- `random_attacker`
- `random_defender`
- `is_war_leader`
- `using_war_goal`
- event `scopes = { from = ... fromfrom = ... }`
- `script_values` with arithmetic, `min`, `max`, and `value:...`
- `check_variable_arithmetic`
- `set_timed_country_flag`
- `set_timed_relation_flag`
- `has_relation_flag`
- `add_opinion_modifier`
- `remove_opinion_modifier`
- opinion `modifier = { ... }`
- opinion `decay`
- opinion `accumulative`
- existing Director gates:
  - `staid_core_deficit_short_runway`
  - `staid_survival_mode`
  - `staid_recovery_mode`
  - `staid_fleet_buildup_economy_safe`
  - `staid_starbase_defense_economy_safe`

## Generated Files And Isolation

Extend the existing generator-driven Director system rather than hand-writing scattered logic.

Add/extend Python surfaces:

- `tools/stellar_ai_director_lib.py`
  - threat vector tables
  - war-goal classification table
  - score/tier generation helpers
  - threat-response validation helpers
- `tools/generate_stellar_ai_director_patch.py`
  - emits the new threat-response files
- `tools/validate_stellar_ai_director_patch.py`
  - fails on threat-response contract violations
- `tools/tests/test_stellar_ai_director.py`
  - owns deterministic tests for all non-game-launch behavior

Generate new PDXScript files:

- `mods/StellarAIDirector/common/script_values/zzz_staid_threat_response_values.txt`
- `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_threat_response_triggers.txt`
- `mods/StellarAIDirector/common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`
- `mods/StellarAIDirector/common/on_actions/zzz_staid_threat_response_on_actions.txt`
- `mods/StellarAIDirector/events/zzz_staid_threat_response_events.txt`
- `mods/StellarAIDirector/localisation/english/staid_threat_response_l_english.yml`

Update durable docs/artifacts:

- `plans/stellar-ai-director-threat-response-plan.md`
- `research/stellar-ai/stellar-ai-director-threat-response-feasibility-2026-07-05.md`
- `research/stellar-ai/stellar-ai-director-threat-response-war-goal-classification-2026-07-05.csv`
- `mods/StellarAIDirector/notes/tuning-notes.md`

The threat-response layer remains isolated. It must not modify:

- `staid_survival_mode`
- `staid_recovery_mode`
- `staid_core_deficit_short_runway`
- vanilla or generated `common/diplomatic_actions`
- v1 war declaration / join-war / CB behavior

## Generator-Owned Data Model

Add generator constants:

```python
THREAT_RESPONSE_AXES = (
    "moral_outrage",
    "regional_fear",
    "shared_threat_cooperation",
    "conquest_respect",
    "punitive_pressure",
    "defensive_readiness",
    "opportunism",
)

THREAT_SCORE_LIMITS = {
    "anti_aggressor_score": (0, 100),
    "alignment_with_aggressor_score": (0, 60),
    "defensive_readiness_score": (0, 50),
}

THREAT_ECONOMY_RATIO_CAP = 0.20
THREAT_RELATION_FLAG_DAYS = 7200
```

The generator emits PDXScript values/triggers/objects. Stellaris runtime does not need to know what a design axis means; it only consumes emitted script values, tier triggers, flags, and opinion modifiers.

Runtime state is named and bounded:

- `staid_tr_anti_aggressor_low`
- `staid_tr_anti_aggressor_medium`
- `staid_tr_anti_aggressor_high`
- `staid_tr_anti_aggressor_severe`
- `staid_tr_alignment_low`
- `staid_tr_alignment_medium`
- `staid_tr_alignment_high`
- `staid_tr_defensive_readiness_low`
- `staid_tr_defensive_readiness_high`

Pairwise observer-to-aggressor state uses timed relation flags. Economy readiness uses timed country flags.

## Personality Vectors

Normal ethic contribution is `W`. Fanatic contribution is exactly `3W`.

Normal ethic table:

| Ethic | Outrage | Fear | Cooperation | Respect | Punitive | Defense | Opportunism |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pacifist | +3 | +1 | +2 | -2 | +1 | +2 | 0 |
| Egalitarian | +2 | +1 | +2 | -1 | +1 | +1 | 0 |
| Xenophile | +1 | +1 | +3 | -1 | +1 | +1 | 0 |
| Militarist | -1 | +2 | 0 | +2 | +1 | +2 | +1 |
| Authoritarian | -1 | +1 | -1 | +2 | 0 | +1 | +2 |
| Xenophobe | 0 | +3 | -2 | +1 | +2 | +2 | +1 |
| Materialist | 0 | +2 | +1 | 0 | +1 | +1 | +1 |
| Spiritualist | +1 | +1 | +1 | 0 | +1 | +1 | 0 |

Fanatic examples:

- pacifist outrage `+3` becomes fanatic pacifist outrage `+9`
- authoritarian respect `+2` becomes fanatic authoritarian respect `+6`
- xenophile cooperation `+3` becomes fanatic xenophile cooperation `+9`

Gestalt vectors are separate and do not use moral ethics by default:

| Type | Outrage | Fear | Cooperation | Respect | Punitive | Defense | Opportunism |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hive/machine | 0 | +2 | 0 | 0 | +1 | +2 | 0 |
| Empath/servitor-like | +2 | +2 | +2 | 0 | +1 | +2 | 0 |
| Purifier/devouring/exterminator | 0 | +2 | -3 | +3 | 0 | +2 | +2 |

Civic/personality additions are bounded:

- normal civic contribution max `+1` per axis;
- total civic contribution max `+2` normal-equivalent per axis;
- no civic can bypass caps;
- homicidal/genocidal civics use the special gestalt/homicidal path, not normal moral outrage.

## Score Math

Emit script values equivalent to:

```text
anti_aggressor_score =
  clamp(0, 100,
    severity * 10
    + moral_outrage * 5
    + regional_fear * 5
    + shared_threat_cooperation * 4
    + punitive_pressure * 6
    - conquest_respect * 5
    - opportunism * 3
  )

alignment_with_aggressor_score =
  clamp(0, 60,
    conquest_respect * 6
    + opportunism * 5
    - moral_outrage * 7
    - regional_fear * 3
  )

defensive_readiness_score =
  clamp(0, 50,
    severity * 5
    + regional_fear * 5
    + defensive_readiness * 5
  )
```

Tier cutoffs:

- `anti_aggressor_low`: `25+`
- `anti_aggressor_medium`: `45+`
- `anti_aggressor_high`: `65+`
- `anti_aggressor_severe`: `85+`
- `alignment_low`: `20+`
- `alignment_medium`: `35+`
- `alignment_high`: `50+`
- `defensive_readiness_low`: `25+`
- `defensive_readiness_high`: `40+`

If the emitted PDXScript cannot represent one formula cleanly in one object, the generator emits equivalent tier triggers. The generator remains the source of truth for the math.

## War-Goal Classification

Only explicitly classified war goals can create punitive threat response.

Initial allowlist:

| War Goal | Severity |
| --- | ---: |
| `wg_conquest` | 2 |
| `wg_subjugation` | 3 |
| `wg_humiliation` | 1 |

Context severity modifiers:

- repeated aggressive war within 20 years: `+2`
- observer adjacent to aggressor or victim: `+2`
- victim is federation ally / defensive pact / guaranteed: `+3`
- observer has claims or direct border with aggressor: `+1`
- aggressor is homicidal/genocidal: severe path, still bounded by caps

Unknown or modded war goals:

- severity `0`
- no punitive opinion
- no containment flag
- no defensive-readiness flag
- no CB
- no forced war
- recorded in the classification CSV for later manual review

## Runtime Event Flow

`on_war_beginning` calls one hidden event, `staid_tr.1`.

`staid_tr.1` processes only once per war, when `root` is the attacker-side war leader:

```text
from = {
  any_attacker = {
    is_same_value = root
    is_war_leader = yes
  }
}
```

This prevents duplicate galaxy-wide applications from every participant.

Event flow:

1. Verify attacker war leader.
2. Verify war goal is allowlisted.
3. Save attacker as aggressor.
4. Save representative defender with `random_defender`.
5. Dispatch observer evaluation to aware default countries.
6. Observer event receives:
   - `root` = observer
   - `from` = aggressor
   - `fromfrom` = defender/victim representative
7. Observer computes tier using generated triggers/script values.
8. Observer applies only allowed outputs:
   - timed relation flag toward aggressor;
   - timed country flag for defensive readiness if foreign-affairs safe;
   - opinion modifier toward aggressor;
   - shared-threat opinion toward victim/observers when applicable.

Awareness rule for v1:

- observer must be a default country;
- observer must not be the aggressor;
- observer must have communications or another verified relation/visibility path;
- no omniscient galaxy-wide reaction.

## Opinion Effects And Caps

Anti-aggressor opinion toward aggressor:

| Tier | Opinion |
| --- | ---: |
| Low | -30 |
| Medium | -60 |
| High | -120 |
| Severe | -200 |

Shared-threat cooperation:

| Tier | Opinion |
| --- | ---: |
| Low | +15 |
| Medium | +30 |
| High/Severe | +60 |

Conquest alignment / respect:

| Tier | Opinion |
| --- | ---: |
| Low | +10 |
| Medium | +25 |
| High | +40 |

Stacking rules:

- applying a higher tier removes lower tiers first;
- anti-aggressor high/severe cannot coexist with alignment for the same observer/aggressor pair;
- opinion modifiers decay;
- no opinion path exceeds its cap.

## Economy And Survival Guardrails

Add `staid_tr_foreign_affairs_safe`.

Required for any third-party threat economy response:

```text
NOT = { staid_core_deficit_short_runway = yes }
NOT = { staid_survival_mode = yes }
NOT = { staid_recovery_mode = yes }
is_at_war = no
```

Also require enough resources:

```text
has_monthly_income = { resource = alloys value > 120 }
has_monthly_income = { resource = energy value > 100 }
resource_stockpile_compare = { resource = alloys value > 8000 }
resource_stockpile_compare = { resource = energy value > 5000 }
```

Threat readiness is not used for direct self-defense. If the AI is the defender/victim, vanilla/Stellar AI/Director war and survival logic owns the existential response.

Third-party economy cap:

- existing Director fleet-throughput reserve is `alloys = 35`, `energy = 30`, `naval_cap = 200`;
- third-party threat economy ratio cap is `20%`;
- maximum v1 threat subplan:
  - `alloys <= 7`
  - `energy <= 6`
  - `naval_cap <= 40`

If survival/recovery/deficit/war gate is active, third-party threat economy contribution is exactly `0`.

## Forced-War Restrictions

V1 generated files must not contain:

- `declare_war`
- `join_war`
- `add_casus_belli`
- forced `wg_*` dispatch
- forced punitive event chain
- diplomatic-action override that effectively forces escalation

This is intentional. Event-style forced wars bypass AI intelligence too easily.

Future punitive-war/CB work, if added later, must be a separate phase with:

- direct-threat requirement;
- safe economy gate;
- military capability gate;
- distance/proximity gate;
- cooldown;
- no survival/recovery/deficit state;
- separate tests proving it cannot fire for weak, distant, struggling, unknown-war-goal, or already-at-war empires.

## Automated Test Matrix

Everything that does not require opening Stellaris must be tested.

### Generated Object Validity

- every generated `.txt` file parses with the local PDX parser;
- every generated common file has at least one top-level object;
- every generated object appears in the correct folder;
- no malformed braces;
- no placeholder tokens;
- no empty generated files.

### Name Validity

- every generated object name matches `^[a-z][a-z0-9_]*$`;
- every threat-response object starts with `staid_tr_`;
- event namespace is only `staid_tr`;
- event IDs are unique;
- localization keys exist for visible opinion modifiers;
- no duplicate generated top-level objects unless explicitly classified as an intentional override.

### Reference Validity

- every generated `value:...` script value reference exists;
- every generated scripted trigger reference exists;
- every generated opinion modifier used by events exists;
- every event referenced by on-actions exists;
- every generated localization key referenced by visible content exists;
- every allowlisted war goal exists in vanilla or indexed mod snapshots;
- every unknown/modded war goal remains inert until added to the allowlist;
- no generated reference is missing from `collect_generated_reference_rows`.

### Value Range Tests

- vector values remain within declared axis ranges;
- score values include explicit `min/max` or equivalent clamp;
- anti-aggressor score range is `0..100`;
- alignment score range is `0..60`;
- defensive readiness score range is `0..50`;
- opinion values stay within caps:
  - anti-aggressor `>= -200`
  - shared-threat `<= +60`
  - alignment `<= +40`
- relation/country flag duration equals `7200` days unless changed in one generator constant;
- economy subplan values stay within:
  - `alloys <= 7`
  - `energy <= 6`
  - `naval_cap <= 40`

### Ratio Tests

- every fanatic vector equals exactly `3x` the normal vector;
- every civic addition is within civic cap;
- total civic contribution per axis is within cap;
- third-party threat economy pressure is never above `20%` of the existing fleet-throughput reserve;
- third-party threat economy pressure is exactly `0` when foreign-affairs safety gates fail;
- alignment and anti-aggressor severe cannot both be active for the same pair.

### Survival And Deficit Gate Tests

Fail validation if any third-party threat economy trigger omits:

- `NOT = { staid_core_deficit_short_runway = yes }`
- `NOT = { staid_survival_mode = yes }`
- `NOT = { staid_recovery_mode = yes }`
- `is_at_war = no`

Fail validation if:

- `staid_survival_mode` references any `staid_tr_` trigger;
- `staid_recovery_mode` references any `staid_tr_` trigger;
- threat response modifies core survival/recovery/deficit triggers;
- threat response can produce economy pressure for a struggling third-party empire.

### Unknown War-Goal Tests

- war goal not in `WAR_GOAL_THREAT_CLASSES` has severity `0`;
- unknown war goal emits no punitive opinion;
- unknown war goal emits no readiness flag;
- unknown war goal emits no CB;
- unknown war goal emits no forced war effect;
- unknown war goal appears in the classification audit artifact.

### Forced-War Safety Tests

Fail validation if any generated v1 file contains:

- `declare_war`
- `join_war`
- `add_casus_belli`
- `attacker_war_goal`
- forced punitive `wg_*`
- generated `common/diplomatic_actions`

Also fail if an event path can call a future war/CB effect without:

- direct-threat classification;
- not survival;
- not recovery;
- not deficit;
- not already at war;
- capability gate;
- proximity gate;
- cooldown.

For v1, this path should not exist at all.

### Scenario Matrix Tests

Use generator-level expected-output tests for these profiles:

- pacifist egalitarian observer condemns conquest strongly;
- fanatic pacifist contribution is exactly triple normal pacifist before caps;
- militarist authoritarian observer can respect distant conquest;
- militarist authoritarian adjacent to repeated aggression shifts toward defensive concern;
- xenophobe reacts strongly to nearby aggression but weakly to distant unrelated wars;
- materialist reacts through risk/strategic stability rather than moral outrage;
- gestalt uses fear/survival logic, not moral outrage;
- purifier/devouring/exterminator does not join moral containment logic;
- struggling third-party empire gets opinion state only, no economy response;
- directly attacked empire is not routed through third-party foreign-affairs safety;
- unknown modded war goal produces no punitive state.

## Validation Commands

Required before any launch/observer-game test:

```powershell
python -m unittest tools.tests.test_stellar_ai_director
python tools/generate_stellar_ai_director_patch.py
python tools/validate_stellar_ai_director_patch.py
```

`validate_generated_patch` must include the threat-response checks, so a normal Director validation run catches broken names, objects, references, ranges, ratios, safety gates, and forbidden forced-war effects.

## Acceptance Criteria

- Threat response creates visible diplomatic consequences for aggression.
- Different ethics/civics/gestalts produce materially different reactions.
- Fanatic ethics preserve exact `3x` normal-weight ratios.
- Unknown modded war goals are inert until classified.
- Third-party struggling empires do not spend themselves into collapse.
- Threat economy pressure cannot exceed the declared ratio cap.
- Survival/recovery/deficit gates cannot be bypassed by personality logic.
- V1 cannot force wars, join wars, or add punitive CBs.
- All non-game-launch behavior is covered by deterministic tests and validator failures.
- Observer-game testing is only the final runtime smoke after automated validation passes.

## Assumptions

- Target game version is Stellaris PC 4.4.4 stable.
- V1 is diplomacy/readiness pressure only, not punitive-war automation.
- Direct self-defense remains owned by vanilla/Stellar AI/Director war and survival behavior.
- Major future escalation features require a separate plan and stricter tests.
```

## plans/stellar-ai-director-threat-response/00-annotated-review.md

```markdown
# Annotated Review

Source reviewed: [../stellar-ai-director-threat-response-plan.md](../stellar-ai-director-threat-response-plan.md).
Review date: 2026-07-05.

## Verdict

The source plan is directionally strong and captures the most important safety decisions: generator-owned design axes, no speculative Stellaris primitives, no forced wars in V1, unknown-war-goal inertness, opinion caps, economy caps, and protection for survival/recovery/deficit gates.

It was not yet implementation-ready because it combined design intent, implementation, tests, and acceptance criteria in one file without enough phase ownership, exact deliverables, risk treatment, runtime interaction clarifications, or handoff gates. This folder keeps the good core and expands the missing pieces into focused documents.

## Section Annotations

| Source section | Review status | Required expansion |
| --- | --- | --- |
| Summary | Good scope boundary. It correctly says V1 is diplomacy/readiness pressure and not war automation. | Add explicit deliverable IDs, non-goals, and a done definition so implementers can prove the scope is complete without expanding it. Covered in [01](01-goals-deliverables-and-acceptance.md). |
| Verified Stellaris Primitives | Good correction from prior planning. It avoids invented runtime support. | Require evidence maintenance for each primitive and define what happens if a primitive later fails launch/runtime validation. Covered in [07](07-research-and-evidence-maintenance.md). |
| Generated Files And Isolation | Good generator-first direction and clear generated output list. | Clarify owner surfaces in `tools/stellar_ai_director_lib.py`, generated-output audit coverage, and which existing file-audit folder sets must be extended. Covered in [02](02-main-implementation-plan.md). |
| Generator-Owned Data Model | Good distinction between design axes and runtime artifacts. | Add table/schema ownership, naming conventions, score limits, flag direction, and generated audit expectations. Covered in [02](02-main-implementation-plan.md) and [03](03-runtime-interaction-contract.md). |
| Personality Vectors | Good ratio requirement, especially fanatic exactly `3x`. | Add deterministic table validation, bounded civic merge rules, gestalt/homicidal routing, and scenario tests that prove caps do not hide ratio mistakes. Covered in [05](05-testing-and-validation-plan.md). |
| Score Math | Good math sketch and tier cutoffs. | Require generator-owned expected-output tests for formula equivalence, explicit clamps, tier exclusivity, and generated trigger fallback when direct script value math becomes awkward. Covered in [02](02-main-implementation-plan.md) and [05](05-testing-and-validation-plan.md). |
| War-Goal Classification | Good allowlist and unknown-war-goal inertness. | Add CSV schema, audit maintenance rules, runtime unknown behavior, source-corpus lookup order, and modded war-goal review loop. Covered in [07](07-research-and-evidence-maintenance.md). |
| Runtime Event Flow | Good single-dispatch intent and scope naming. | Clarify attacker/defender/observer roles, participants excluded from third-party observer flow, multi-attacker/multi-defender behavior, awareness rules, dedupe/cooldown flags, and performance bounds. Covered in [03](03-runtime-interaction-contract.md). |
| Opinion Effects And Caps | Good caps and mutual-exclusion intent. | Add exact modifier naming, remove-before-apply order, accumulator/decay requirements, exclusive pair state, and tests for repeated applications. Covered in [03](03-runtime-interaction-contract.md) and [05](05-testing-and-validation-plan.md). |
| Economy And Survival Guardrails | Good non-overridable survival/recovery/deficit rule. | Add third-party-only routing, `is_at_war = no` semantics, direct-victim exclusion, explicit zero-output rule, and validation for generated subplan caps. Covered in [03](03-runtime-interaction-contract.md), [04](04-risk-prevention-and-mitigation.md), and [05](05-testing-and-validation-plan.md). |
| Forced-War Restrictions | Strong safety boundary. | Convert forbidden effects into validator failures and define future punitive-war work as a separate plan with a new risk review. Covered in [04](04-risk-prevention-and-mitigation.md) and [05](05-testing-and-validation-plan.md). |
| Automated Test Matrix | Good categories. | Expand into test ownership, fixture shape, command cadence, negative-path cases, game-launch gate, and proof expectations. Covered in [05](05-testing-and-validation-plan.md). |
| Validation Commands | Correct high-level commands. | Add doc/index validation, generated artifact inspection, targeted test groups, and launch/observer prerequisites. Covered in [05](05-testing-and-validation-plan.md) and [06](06-implementation-slices-and-handoff.md). |
| Acceptance Criteria | Good user-facing outcomes. | Convert broad statements into testable deliverables with artifacts and pass/fail gates. Covered in [01](01-goals-deliverables-and-acceptance.md). |
| Assumptions | Correct, but too short for handoff. | Add source-of-truth hierarchy, compatibility assumptions, and stop conditions. Covered across [01](01-goals-deliverables-and-acceptance.md), [04](04-risk-prevention-and-mitigation.md), and [07](07-research-and-evidence-maintenance.md). |

## Missing Coverage Added

- Risk prevention and risk mitigation are separated from implementation tasks.
- Runtime interaction semantics are explicit enough to avoid accidental galaxy-wide or participant-side effects.
- The unknown-war-goal policy now includes both runtime inertness and research artifact maintenance.
- The event-flow plan now distinguishes observer state, victim state, aggressor state, country flags, and relation flags.
- The economy plan now states that third-party readiness pressure is exactly zero when safety gates fail.
- The testing plan now treats forbidden war effects, safety-gate omissions, invalid references, score ranges, fanatical ratios, and runtime-scope mistakes as validator/test failures.
- The plan now includes compatibility checks for Nomads, Arkships, Waystations, Waylines, Contracts, the 4.4 Situation Log, Gigastructural Engineering, NSC3, ship/component expansion mods, and heavy AI/economy mods when the touched surface is relevant.

## Open Design Points

These are not blockers to planning, but they must be resolved before implementation is called complete:

- The exact verified visibility/communications predicate for observer awareness must be selected from local Stellaris 4.4.4 sources before generation.
- If multi-defender handling expands beyond a representative defender, it must get a separate performance and interaction review.
- If shared-threat cooperation toward other observers is implemented, it must be bounded and tested; otherwise V1 should apply shared-threat opinion only toward the representative victim.
- If a future punitive-war or CB feature is desired, it must be a new phase with separate safety gates and cannot be smuggled into this V1 implementation.
```

## plans/stellar-ai-director-threat-response/01-goals-deliverables-and-acceptance.md

```markdown
# Goals, Deliverables, And Acceptance

## Objective

Implement a bounded Stellar AI Director V1 threat-response layer that reacts to observable aggressive wars through diplomatic opinion, timed flags, and tightly capped third-party defensive-readiness economy pressure.

## Current Gap

The existing Stellar AI Director work improves economic, megastructure, starbase, and fleet-throughput behavior, but it does not yet add a generator-owned threat-response layer for observed aggression. The source plan defines the desired behavior, but implementation needs testable deliverables, phase gates, risk controls, and runtime interaction rules.

## Non-Goals

V1 must not:

- declare wars;
- join wars;
- add punitive casus belli;
- overwrite diplomatic actions;
- force `wg_*` dispatch;
- make direct self-defense decisions for attacked empires;
- bypass `staid_core_deficit_short_runway`, `staid_survival_mode`, or `staid_recovery_mode`;
- apply punitive effects for unknown or unclassified war goals;
- treat generator-owned axes as native Stellaris runtime concepts.

## Source Of Truth

Use sources in this order:

1. Current user instruction and this plan set.
2. [../stellar-ai-director-threat-response-plan.md](../stellar-ai-director-threat-response-plan.md).
3. Current repo rules in `AGENTS.md`.
4. Existing Director generator and tests in `tools/stellar_ai_director_lib.py` and `tools/tests/test_stellar_ai_director.py`.
5. Current local Stellaris 4.4.4 files, source snapshots, generated research artifacts, CWTools/Irony output, and launch logs.
6. Open Brain memory only as advisory history.

## Deliverables

| ID | Deliverable | Expected output | Acceptance check |
| --- | --- | --- | --- |
| D1 | Generator-owned threat model | Constants/tables in `tools/stellar_ai_director_lib.py` for axes, ethics, gestalt paths, civic caps, score limits, tier cutoffs, flag durations, and economy caps. | Unit tests prove normal/fanatic ratios, range limits, civic caps, and stable exported table shape. |
| D2 | War-goal classification model | `WAR_GOAL_THREAT_CLASSES` table and `research/stellar-ai/stellar-ai-director-threat-response-war-goal-classification-2026-07-05.csv`. | Known allowlisted goals resolve to severity; unknown goals resolve to severity `0` and inert outputs; CSV records source/evidence/status. |
| D3 | Generated script values and triggers | `common/script_values/zzz_staid_threat_response_values.txt` and `common/scripted_triggers/zzz_staid_threat_response_triggers.txt`. | Generated files parse, names use `staid_tr_`, score ranges clamp correctly, and safety gates appear where required. |
| D4 | Generated opinion modifiers and localization | `common/opinion_modifiers/zzz_staid_threat_response_opinions.txt` and `localisation/english/staid_threat_response_l_english.yml`. | Opinion keys exist, modifiers have decay/cap behavior, lower tiers are removed before higher tiers, and visible keys localize. |
| D5 | Generated on-action and event flow | `common/on_actions/zzz_staid_threat_response_on_actions.txt` and `events/zzz_staid_threat_response_events.txt`. | Event namespace is `staid_tr`; dispatch is once per attacker war leader; participant and awareness gates are present; forbidden effects are absent. |
| D6 | Defensive-readiness economy pressure | A generated, capped third-party economy path integrated with existing Director economic-plan surfaces. | Economy pressure is exactly zero when foreign-affairs safety fails and never exceeds `20%` of existing fleet-throughput reserve values. |
| D7 | Validator extensions | `validate_generated_patch()` covers threat-response generated files, references, ranges, ratios, forbidden effects, safety gates, and audit artifacts. | `python tools/validate_stellar_ai_director_patch.py` fails on each seeded threat-response contract violation and passes on the generated patch. |
| D8 | Test coverage | Focused tests in `tools/tests/test_stellar_ai_director.py`. | `python -m unittest tools.tests.test_stellar_ai_director` covers D1-D7, including negative paths and scenario matrix cases. |
| D9 | Research and evidence artifacts | Feasibility note and classification CSV under `research/stellar-ai/`, plus tuning notes updates. | Artifacts state target game version, inspected sources, compatibility risks, test steps, open questions, and generated file ownership. |
| D10 | Documentation updates | `mods/StellarAIDirector/README.md`, `mods/StellarAIDirector/notes/tuning-notes.md`, and plan status docs updated as needed. | Docs describe the feature, generated files, known conflicts, tested game version, non-goals, and remaining runtime risks. |
| D11 | Runtime smoke evidence | Launch/main-menu proof first, then observer-game smoke after automated validation passes. | No new Director problem lines in logs, generated files load, and observer-game notes confirm no forced wars or economy collapse symptoms. |

## Acceptance Criteria

The implementation is acceptable only when all of these are true:

- Threat response produces diplomatic consequences for classified observed aggression.
- Different ethics, civics, and gestalt paths produce materially different generated decisions.
- Fanatic ethics preserve exact `3x` normal-weight ratios before caps.
- Unknown and unclassified war goals are inert until intentionally classified.
- Third-party struggling empires receive no threat economy pressure.
- Third-party threat economy pressure cannot exceed the declared ratio cap.
- Survival/recovery/deficit gates cannot be bypassed by personality logic.
- V1 generated files contain no forced-war, join-war, punitive-CB, or diplomatic-action override path.
- Automated tests and validator checks cover every non-game-launch behavior.
- Manual/runtime launch and observer checks are performed only after deterministic validation passes.

## Out Of Scope For This Plan Set

- Balancing final opinion values after long observer-game campaigns.
- Supporting Stellaris 4.4.5 beta, 4.5 beta, or later script changes.
- Making the AI start containment wars or issue punitive CBs.
- Building UI around threat state.
- Reworking the existing ROI, megastructure, starbase, or fleet-throughput Director model except where the new threat economy cap integrates with it.
```

## plans/stellar-ai-director-threat-response/02-main-implementation-plan.md

```markdown
# Main Implementation Plan

## Objective

Add the threat-response feature through the existing deterministic generator and validator pipeline. The durable behavior belongs in `tools/stellar_ai_director_lib.py`; wrappers remain thin command surfaces.

## Keep Unchanged

- Keep `tools/generate_stellar_ai_director_patch.py` as the simple `run_all()` wrapper.
- Keep `tools/validate_stellar_ai_director_patch.py` as the simple `validate_generated_patch()` wrapper.
- Preserve existing generated Director files unless a threat-response slice explicitly extends audit coverage or economy plans.
- Preserve existing survival/recovery/deficit trigger semantics.
- Preserve existing V1 main-menu, observer, Irony, and plan-status evidence flows.

## Owner Surfaces

Primary owner:

- `tools/stellar_ai_director_lib.py`

Required implementation consumers:

- `tools/tests/test_stellar_ai_director.py`
- `tools/generate_stellar_ai_director_patch.py`
- `tools/validate_stellar_ai_director_patch.py`

Generated outputs:

- `mods/StellarAIDirector/common/script_values/zzz_staid_threat_response_values.txt`
- `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_threat_response_triggers.txt`
- `mods/StellarAIDirector/common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`
- `mods/StellarAIDirector/common/on_actions/zzz_staid_threat_response_on_actions.txt`
- `mods/StellarAIDirector/events/zzz_staid_threat_response_events.txt`
- `mods/StellarAIDirector/localisation/english/staid_threat_response_l_english.yml`

Durable evidence outputs:

- `research/stellar-ai/stellar-ai-director-threat-response-feasibility-2026-07-05.md`
- `research/stellar-ai/stellar-ai-director-threat-response-war-goal-classification-2026-07-05.csv`
- `mods/StellarAIDirector/notes/tuning-notes.md`

## Implementation Steps

### I1 - Data Model

Add generator constants for:

- `THREAT_RESPONSE_AXES`
- normal ethic vector table;
- fanatic multiplier constant set to exactly `3`;
- gestalt/homicidal vector table;
- civic/personality additive cap table;
- score limits;
- tier cutoffs;
- opinion values and caps;
- relation/country flag durations;
- economy ratio cap;
- forbidden V1 effect strings.

Add helper functions that return plain serializable rows. Prefer deterministic rows over scattered literals so tests and CSVs can consume the same source.

### I2 - War-Goal Classification

Add `WAR_GOAL_THREAT_CLASSES` with initial entries:

- `wg_conquest`, severity `2`;
- `wg_subjugation`, severity `3`;
- `wg_humiliation`, severity `1`.

Each row must include:

- war goal key;
- severity;
- classification status;
- source evidence path or source label;
- notes;
- whether punitive outputs are allowed.

Unknown lookup must return severity `0`, punitive outputs disabled, readiness disabled, forced-war disabled, and audit status `unknown_inert`.

### I3 - Threat Score Generation

Generate script values or equivalent tier triggers for:

- anti-aggressor score range `0..100`;
- alignment score range `0..60`;
- defensive-readiness score range `0..50`.

If direct formula output is brittle in PDXScript, emit tier triggers that are equivalent to generator-owned score expectations. Do not let runtime PDXScript become the only source of the math.

### I4 - Runtime Trigger Generation

Generate `staid_tr_` scripted triggers for:

- classified war-goal checks;
- observer eligibility;
- awareness/communications gate;
- attacker war leader gate;
- observer not aggressor;
- observer not attacker-side participant;
- observer not defender-side participant;
- third-party foreign-affairs safety;
- anti-aggressor tier checks;
- alignment tier checks;
- defensive-readiness tier checks;
- modifier exclusivity checks.

The third-party economy trigger must include all existing Director safety gates and `is_at_war = no`.

### I5 - Opinion And Localization Generation

Generate opinion modifiers for:

- anti-aggressor low, medium, high, severe;
- shared-threat low, medium, high;
- conquest alignment low, medium, high.

Each visible modifier needs a localization key. Opinion generation must encode decay and stacking behavior consistently with the source plan. Event code must remove incompatible lower or opposite modifiers before applying a higher tier.

### I6 - Event And On-Action Generation

Generate an `on_war_beginning` hook that dispatches to a hidden `staid_tr` event chain.

The chain must:

1. run only for the attacker-side war leader;
2. classify the war goal;
3. stop immediately for unknown or inert war goals;
4. choose a representative defender only for V1 victim/shared-threat output;
5. evaluate only eligible observers;
6. apply only allowed opinion/flag/economy outputs;
7. never call forbidden war effects.

### I7 - Economy Integration

Add a narrow third-party threat readiness economy pressure path. It must:

- be capped at `20%` of existing fleet-throughput reserve values;
- produce at most `alloys <= 7`, `energy <= 6`, and `naval_cap <= 40`;
- be exactly zero when survival, recovery, deficit, or at-war gates fail;
- not route direct self-defense through third-party economy safety;
- remain subordinate to existing Director fleet/starbase economy gates.

### I8 - Validation And Audit Integration

Extend existing generated-file and reference audit coverage so the new folders are not invisible:

- `opinion_modifiers`;
- `on_actions`;
- `events`;
- `localisation/english`.

Add threat-response-specific validation that fails on:

- invalid names;
- missing references;
- missing localization;
- missing safety gates;
- out-of-range scores/opinions/economy values;
- broken fanatic ratios;
- unclassified allowlist entries;
- forbidden forced-war effects;
- missing classification CSV;
- generated output not matching generator tables.

## Contracts And Precedence

- Generator tables precede emitted PDXScript.
- Emitted PDXScript precedes manual notes.
- Validator failures block launch/observer testing.
- Runtime unknown-war-goal behavior must be inert even if research artifacts list unknown candidates for later review.
- Safety gates precede personality-driven outputs.
- Anti-aggressor high/severe opinion beats conquest alignment for the same observer/aggressor pair.

## Out Of Scope

- New diplomatic actions.
- New casus belli.
- War declaration automation.
- Multi-victim galaxy-wide opinion propagation beyond the bounded V1 representative defender behavior.
- Runtime UI or Situation Log integration.
```

## plans/stellar-ai-director-threat-response/03-runtime-interaction-contract.md

```markdown
# Runtime Interaction Contract

## Objective

Define the exact logical interactions the generated PDXScript must implement so the feature behaves predictably in-game and remains bounded.

## Actors

- Aggressor: attacker-side war leader that began a classified aggressive war.
- Victim representative: one defender-side country selected for V1 shared-threat context.
- Observer: a default country that is neither the aggressor nor any war participant and can plausibly know about the war.
- Direct victim: any defender-side participant. Direct victims are owned by vanilla/Stellar AI/Director war and survival behavior, not the third-party observer economy path.

## Event Trigger

`on_war_beginning` dispatches to one hidden `staid_tr` event chain.

The first event must verify that `root` is the attacker-side war leader before any galaxy or observer iteration occurs. If that check fails, the chain stops with no output.

## Observer Eligibility

An observer must:

- be a default country;
- not be the aggressor;
- not be an attacker-side participant;
- not be a defender-side participant;
- not be a country type that should avoid normal diplomatic logic;
- pass the selected and verified awareness/communications predicate;
- pass any Nomad/Arkship/Waystation/Wayline/Contract compatibility exclusion required by inspected sources.

The awareness predicate must be selected from verified Stellaris 4.4.4 primitives. If only communications is confidently verified, V1 must use communications rather than an invented visibility model.

## War-Goal Classification

Classification precedes all outputs.

Allowed V1 classes:

| War goal | Severity | Runtime behavior |
| --- | ---: | --- |
| `wg_conquest` | 2 | May create opinion/flag/readiness outputs if observer gates pass. |
| `wg_subjugation` | 3 | May create stronger opinion/flag/readiness outputs if observer gates pass. |
| `wg_humiliation` | 1 | May create lower opinion outputs if observer gates pass. |

Unknown or unclassified goals:

- severity `0`;
- no punitive opinion;
- no shared-threat opinion;
- no alignment opinion;
- no readiness flag;
- no economy pressure;
- no CB;
- no forced war;
- audit row only.

## Severity Modifiers

Severity modifiers are allowed only after the base war goal is classified.

Allowed V1 modifiers:

- repeated aggressive war within 20 years: `+2`;
- observer adjacent to aggressor or victim: `+2`;
- victim is federation ally, defensive pact partner, or guaranteed country: `+3`;
- observer has claims or a direct border with aggressor: `+1`;
- aggressor is homicidal/genocidal: severe path, still capped.

Any modifier that cannot be expressed with verified primitives must stay generator-side as an unimplemented row with tests proving it does not appear in generated runtime script.

## State And Direction

Use separate state for separate meanings:

- observer-to-aggressor relation flags for anti-aggressor or alignment state;
- observer-to-victim relation flags for shared-threat state;
- observer country flags for defensive-readiness state;
- aggressor or observer cooldown flags only if needed for repeated-aggression detection or duplicate suppression.

Do not reuse one flag for both "this pair already reacted" and "this aggressor has repeated aggression." Those are different meanings and require different tests.

## Output Precedence

The generated event chain must apply outputs in this order:

1. Stop if root is not attacker war leader.
2. Stop if war goal is not classified.
3. Stop for non-observer countries and participants.
4. Stop if awareness gate fails.
5. Compute generator-owned score/tier outputs.
6. Remove incompatible lower-tier or opposite-polarity opinions.
7. Apply the highest valid anti-aggressor or alignment opinion.
8. Apply shared-threat opinion only to the victim representative unless a bounded multi-victim path is explicitly implemented.
9. Apply defensive-readiness country flag only if `staid_tr_foreign_affairs_safe` passes.
10. Apply economy pressure only from the generated economic-plan path and only while the readiness flag and all safety gates pass.

## Opinion Interactions

Anti-aggressor high/severe and conquest alignment must be mutually exclusive for the same observer/aggressor pair.

Higher anti-aggressor tiers remove lower anti-aggressor tiers before applying. Higher alignment tiers remove lower alignment tiers before applying. Anti-aggressor high/severe removes alignment for the same pair.

Opinion modifiers must decay. If accumulative behavior is used, generated values and removal order must prove the configured cap cannot be exceeded by repeated event applications.

## Economy Interactions

Threat-readiness economy pressure is third-party-only.

It is exactly zero when any of these are true:

- `staid_core_deficit_short_runway = yes`;
- `staid_survival_mode = yes`;
- `staid_recovery_mode = yes`;
- `is_at_war = yes`;
- required monthly income or stockpile checks fail.

If the country is directly attacked, this feature does not decide its direct war economy behavior. Existing vanilla/Stellar AI/Director self-defense and survival behavior owns that response.

## Shared-Threat Interactions

V1 should prefer a bounded observer-to-victim shared-threat opinion over observer-to-observer mesh behavior. A galaxy-wide observer mesh can become expensive and hard to reason about.

If observer-to-observer shared-threat cooperation is implemented later, it must have:

- an explicit cap on affected countries;
- duplicate suppression;
- performance tests or a bounded-loop proof;
- separate interaction tests for federations, defensive pacts, guarantees, vassals, and crisis actors.

## Compatibility Clarifications

Required compatibility cases when implementation touches relevant diplomacy, economy, colony, planet, war, UI, starbase, automation, AI, or modifier behavior:

- Nomads;
- Arkships;
- Waystations;
- Waylines;
- Contracts;
- Stellaris 4.4 Situation Log behavior;
- Gigastructural Engineering war goals, crises, and special country types;
- NSC3 and ship/component expansion scripted country or fleet behavior;
- smarter AI mods and performance optimizers in the active playset.

Compatibility checks do not mean V1 must implement special behavior for each case. They mean the plan must prove the feature either interacts safely or explicitly excludes the case.
```

## plans/stellar-ai-director-threat-response/04-risk-prevention-and-mitigation.md

```markdown
# Risk Prevention And Mitigation

## Risk Doctrine

Threat response is high-risk because it touches diplomacy, opinion modifiers, event dispatch, war context, and economy pressure. Prevent risk through generator-owned contracts and validator failures before relying on launch or observer-game smoke tests.

## Risk Register

| ID | Risk | Prevention | Mitigation | Proof |
| --- | --- | --- | --- | --- |
| R1 | Abstract design axes leak into runtime as unsupported Stellaris concepts. | Keep axes only in generator constants and emitted comments/docs. Runtime files consume script values, triggers, flags, and opinion modifiers only. | Remove leaked axis references from generated files and add validator checks for raw axis names in runtime-sensitive contexts. | Unit tests and validator scan generated files. |
| R2 | `on_war_beginning` fires multiple galaxy-wide reactions for one war. | First event verifies attacker-side war leader before observer iteration. | Add duplicate-suppression relation/country flag only if launch testing shows repeated application. | Event contract tests inspect attacker leader gate and event IDs. |
| R3 | Unknown modded war goals accidentally create punitive effects. | Classification lookup defaults to severity `0` and inert outputs. | Add unknown war goal to CSV for manual review; do not hot-classify without tests. | Unknown-war-goal tests and CSV audit. |
| R4 | Generated files accidentally add forced war behavior. | Validator forbids `declare_war`, `join_war`, `add_casus_belli`, forced punitive `wg_*`, and generated diplomatic-action overrides. | Revert the offending generated event path and split punitive-war work into a separate plan. | Forbidden-effect tests fail before launch. |
| R5 | Third-party observers spend into collapse. | `staid_tr_foreign_affairs_safe` requires no deficit, no survival, no recovery, not at war, high income, and high stockpiles. | Set threat economy output to zero and leave only opinion effects for struggling empires. | Safety-gate and economy-ratio tests. |
| R6 | Opinion modifiers stack beyond intended caps. | Remove lower and opposite modifiers before applying higher tiers; use decay and bounded values. | Add cleanup event path or stricter non-accumulative modifiers if runtime shows stacking drift. | Repeated-application tests and validator checks. |
| R7 | Event scopes point at the wrong country. | Document root/from/fromfrom contract and inspect generated event blocks. | Disable output application until scope is corrected; preserve classification tests. | Event-flow tests and launch log checks. |
| R8 | Observer loop creates performance problems. | Exclude participants, require awareness, prefer representative defender, and avoid observer-to-observer mesh in V1. | Reduce outputs to relation with aggressor only if observer-game smoke shows overhead. | Static loop inspection and observer smoke notes. |
| R9 | Compatibility cases behave strangely. | Check Nomads, Arkships, Waystations, Waylines, Contracts, 4.4 Situation Log, Gigas, NSC3, and active playset AI/economy mods where touched. | Add explicit exclusions for country types or situations that cannot safely participate. | Research note and runtime smoke checklist. |
| R10 | Generated output conflicts with existing override audits. | Extend file/reference/conflict audit coverage for opinion modifiers, on-actions, events, and localization. | Classify intentional overrides or rename files/objects to avoid collisions. | Generated conflict and reference audit artifacts. |
| R11 | Localization encoding or keys break load. | Generate only explicit localization keys and keep file under `localisation/english`. | Remove visible strings until localization passes. | Unit tests and validator localization checks. |
| R12 | Source corpus becomes stale before implementation. | Refresh JDocMunch/JCodeMunch indexes and local source snapshots when current sources are needed. | Pause classification expansion until fresh evidence exists. | Verify-index output and research note timestamp. |
| R13 | Score math becomes hard to represent in PDXScript. | Generator remains source of truth and may emit equivalent tier triggers. | Replace direct formula script values with generated tier triggers and keep expected-output tests. | Formula/tier equivalence tests. |
| R14 | Homicidal or crisis actors receive normal moral diplomacy. | Route homicidal/genocidal paths through special vectors and exclusions. | Make those actors inert or severe-only depending on verified country type behavior. | Scenario tests and source-evidence note. |

## Prevention Gates

Implementation must stop before runtime testing if any gate fails:

- Munch startup and relevant indexes are not healthy.
- Generated files do not parse.
- Validator reports missing references, missing localization, out-of-range values, or forbidden effects.
- Unit tests fail.
- Unknown war goals produce anything other than inert output.
- Economy pressure can be emitted while survival/recovery/deficit/at-war gates fail.

## Mitigation Boundaries

Allowed mitigations:

- Narrow outputs to opinion-only while preserving the classification model.
- Keep generated event files present but unhooked from `on_war_beginning` until tests pass.
- Exclude uncertain country types or compatibility cases from observer eligibility.
- Treat unknown or unverified war goals as inert.
- Reduce shared-threat behavior to observer-to-victim only.

Disallowed mitigations:

- Bypassing validator failures for launch testing.
- Hand-editing generated files as the durable fix.
- Adding a runtime forced-war path to compensate for weak opinion impact.
- Weakening survival/recovery/deficit gates.
- Treating a passing launch as proof that deterministic tests are unnecessary.

## Rollback Boundary

Rollback is source-driven:

- remove or revert the generator constants/functions;
- remove generated threat-response files through the generator;
- remove on-action hook before launch testing if event behavior is suspect;
- keep research/audit notes that explain why rollback happened.

Do not delete unrelated Stellar AI Director files or existing evidence artifacts when rolling back this feature.
```

## plans/stellar-ai-director-threat-response/05-testing-and-validation-plan.md

```markdown
# Testing And Validation Plan

## Objective

Prove every non-game-launch threat-response behavior with deterministic tests and validator checks before any Stellaris launch or observer smoke test.

## Required Commands

Run these after implementation changes:

```powershell
python -m unittest tools.tests.test_stellar_ai_director
python tools/generate_stellar_ai_director_patch.py
python tools/validate_stellar_ai_director_patch.py
```

Run these for documentation and repo hygiene after plan/docs changes:

```powershell
git diff --check -- plans
```

Refresh and verify the local docs index when generated docs or plans change:

```powershell
jdocmunch-mcp index-local C:\Users\Admin\Documents\GIT\GameMods\StellarisMods --name local/StellarisMods-docs --no-ai-summaries
jdocmunch-mcp verify-index --repo local/StellarisMods-docs
```

Use the active MCP tools when mounted; the CLI commands above are fallback/readback examples, not a replacement for the repo's Munch tool requirement.

## Unit Test Groups

### Data Model Tests

Test that:

- `THREAT_RESPONSE_AXES` contains only expected axis names;
- every normal ethic vector has every axis;
- every fanatic vector equals exactly `3x` the normal vector before caps;
- civic additions cannot exceed per-civic and total caps;
- gestalt and homicidal paths do not use normal moral outrage by default;
- score limits and tier cutoffs are stable and monotonic.

### War-Goal Classification Tests

Test that:

- `wg_conquest`, `wg_subjugation`, and `wg_humiliation` classify with expected severity;
- unknown war goals return severity `0`;
- unknown war goals produce no punitive, readiness, CB, or forced-war output;
- the classification CSV contains all allowlisted rows;
- allowlisted rows include source/evidence/status fields;
- every allowlisted goal is present in vanilla or indexed source snapshots.

### Generation Tests

Test that generated files:

- exist at the expected paths;
- parse with the local PDX parser where applicable;
- contain at least one top-level object where expected;
- use only `staid_tr_` object prefixes for threat response;
- use event namespace `staid_tr`;
- include localization for visible opinion modifiers;
- include no placeholder tokens or empty generated files.

### Reference Tests

Test that:

- every `value:...` reference resolves;
- every scripted trigger reference resolves;
- every opinion modifier used by events exists;
- every event referenced by on-actions exists;
- every localization key referenced by visible content exists;
- file/reference audit rows include the new generated folders.

### Range And Ratio Tests

Test that:

- anti-aggressor score range is `0..100`;
- alignment score range is `0..60`;
- defensive-readiness score range is `0..50`;
- anti-aggressor opinion is never below `-200`;
- shared-threat opinion is never above `+60`;
- alignment opinion is never above `+40`;
- relation/country flag duration equals the generator constant;
- third-party economy values are at most `alloys <= 7`, `energy <= 6`, and `naval_cap <= 40`;
- third-party economy pressure is never above `20%` of the existing fleet-throughput reserve.

### Safety-Gate Tests

Validator must fail if third-party threat economy output omits:

- `NOT = { staid_core_deficit_short_runway = yes }`;
- `NOT = { staid_survival_mode = yes }`;
- `NOT = { staid_recovery_mode = yes }`;
- `is_at_war = no`;
- required income and stockpile checks.

Validator must also fail if:

- `staid_survival_mode` references any `staid_tr_` trigger;
- `staid_recovery_mode` references any `staid_tr_` trigger;
- threat response modifies core survival/recovery/deficit triggers;
- threat response can produce economy pressure for a struggling third-party empire.

### Forbidden-Effect Tests

Fail validation if any generated V1 file contains:

- `declare_war`;
- `join_war`;
- `add_casus_belli`;
- `attacker_war_goal`;
- forced punitive `wg_*`;
- generated `common/diplomatic_actions`.

For V1, any future war/CB effect path should not exist at all.

### Runtime-Flow Contract Tests

Use static generated-text and parsed-object tests to prove:

- `on_war_beginning` hooks only the threat-response dispatcher;
- first event verifies attacker-side war leader;
- participants cannot become third-party observers;
- unknown war goals stop before opinion/economy application;
- awareness gate appears before output application;
- opinion removal happens before opinion application;
- anti-aggressor high/severe and alignment cannot coexist for the same pair;
- defensive-readiness flag can be set only after foreign-affairs safety passes.

## Scenario Matrix

Use generator-level expected-output tests for:

- pacifist egalitarian observer strongly condemns conquest;
- fanatic pacifist contribution is exactly triple normal pacifist before caps;
- militarist authoritarian observer can respect distant conquest;
- militarist authoritarian adjacent to repeated aggression shifts toward defensive concern;
- xenophobe reacts strongly to nearby aggression and weakly to distant unrelated wars;
- materialist reacts through risk/strategic stability rather than moral outrage;
- gestalt uses fear/survival logic, not moral outrage;
- purifier/devouring/exterminator does not join normal moral containment logic;
- struggling third-party empire gets opinion state only and no economy response;
- directly attacked empire is not routed through third-party foreign-affairs safety;
- unknown modded war goal produces no punitive state.

## Manual Runtime Validation

Manual/runtime validation happens only after deterministic checks pass.

Minimum runtime sequence:

1. Generate and validate the patch.
2. Confirm main-menu load proof with the parent playset and Director-enabled playset.
3. Run observer smoke with at least one classified aggressive war.
4. Inspect logs for new Director problem lines, missing localization, invalid references, or repeated event spam.
5. Confirm no forced wars, join-war behavior, or punitive CBs appeared.
6. Record evidence in `mods/StellarAIDirector/notes/observer-test-log.md` and `research/stellar-ai/`.

Runtime smoke is not a substitute for deterministic tests. It only proves that generated files load and basic event behavior does not immediately break in-game.
```

## plans/stellar-ai-director-threat-response/06-implementation-slices-and-handoff.md

```markdown
# Implementation Slices And Handoff

## Objective

Break implementation into small, reviewable slices with clear gates. Do not merge broad event/economy behavior before the data model and validator can prove the contracts.

## Slice Order

### S0 - Tooling And Source Readiness

Outputs:

- Munch guide calls return content.
- Munch startup assertion passes or records only expected duplicate-stdio warnings.
- Relevant JDocMunch/JCodeMunch indexes are fresh.
- Open Brain memory lookup is performed.

Gate:

- Do not implement while required tool surfaces are stale or failing.

### S1 - Evidence And Classification Prep

Outputs:

- feasibility note under `research/stellar-ai/`;
- initial war-goal classification CSV;
- source evidence for verified primitives and allowlisted war goals.

Gate:

- Unknown war goals must be explicitly inert before event generation starts.

### S2 - Generator Data Model

Outputs:

- constants and table helpers in `tools/stellar_ai_director_lib.py`;
- data model tests;
- no generated runtime hook yet.

Gate:

- Fanatic `3x` tests, civic cap tests, and table-shape tests pass.

### S3 - Generated Values And Triggers

Outputs:

- threat-response script values;
- threat-response scripted triggers;
- static validator checks for names, ranges, and safety gates.

Gate:

- Generated files parse and validator catches seeded broken names/ranges/gates.

### S4 - Opinion Modifiers And Localization

Outputs:

- opinion modifier file;
- localization file;
- tests for caps, decay, exclusivity, and keys.

Gate:

- Repeated-application and mutual-exclusion tests pass.

### S5 - Event And On-Action Flow

Outputs:

- hidden `staid_tr` event chain;
- `on_war_beginning` hook;
- runtime-flow contract tests.

Gate:

- Forbidden-effect tests pass.
- Unknown-war-goal stop-path tests pass.
- Participant exclusion and awareness-gate tests pass.

### S6 - Economy Integration

Outputs:

- capped third-party threat economy pressure path;
- safety gate tests;
- tuning notes update.

Gate:

- Economy pressure is exactly zero under survival/recovery/deficit/at-war failures.
- Economy values stay within cap.

### S7 - Full Validator And Audit Integration

Outputs:

- `validate_generated_patch()` covers all new surfaces;
- file/reference/conflict audits include new generated folders;
- docs and plan status artifacts updated.

Gate:

- `python tools/validate_stellar_ai_director_patch.py` passes.
- Seeded contract breaks fail in tests.

### S8 - Launch And Observer Smoke

Outputs:

- main-menu proof;
- observer smoke notes;
- logs and generated reports under `research/stellar-ai/`.

Gate:

- Run only after S7 passes.
- Stop on new Director problem lines, forced-war behavior, missing localization, or repeated event spam.

## Stop Conditions

Stop and repair before continuing if:

- active Munch guide calls fail;
- the local source corpus is stale for a primitive or war-goal claim;
- deterministic tests fail;
- validation fails;
- generated files require hand edits to pass;
- forbidden effects appear;
- unknown war goals produce output;
- runtime logs show repeated event spam or missing generated objects.

## Handoff Package

At handoff, include:

- files changed;
- generated artifacts;
- source evidence inspected;
- validation commands and results;
- failed commands and reruns;
- runtime evidence if performed;
- remaining risks;
- next recommended action.

Handoff should be saved in Open Brain with who/what/where/when/why/how context and should also be reflected in repo docs or research artifacts when it changes project state.
```

## plans/stellar-ai-director-threat-response/07-research-and-evidence-maintenance.md

```markdown
# Research And Evidence Maintenance

## Objective

Keep threat-response implementation grounded in current local Stellaris 4.4.4 evidence, source snapshots, and generated audit artifacts.

## Required Research Artifacts

### Feasibility Note

Path:

- `research/stellar-ai/stellar-ai-director-threat-response-feasibility-2026-07-05.md`

Must include:

- target game version;
- local Stellaris install path inspected;
- vanilla files inspected;
- mod source snapshots inspected;
- verified primitives used by the plan;
- primitives intentionally not used;
- compatibility cases reviewed;
- test steps;
- open questions;
- final implementation recommendation.

### War-Goal Classification CSV

Path:

- `research/stellar-ai/stellar-ai-director-threat-response-war-goal-classification-2026-07-05.csv`

Required columns:

- `war_goal`;
- `source`;
- `source_path`;
- `mod_or_vanilla`;
- `classification`;
- `severity`;
- `punitive_outputs_allowed`;
- `readiness_outputs_allowed`;
- `forced_war_allowed`;
- `status`;
- `notes`.

Initial rows:

- `wg_conquest`;
- `wg_subjugation`;
- `wg_humiliation`.

Unknown rows discovered from vanilla or mod snapshots must use:

- `severity = 0`;
- `punitive_outputs_allowed = no`;
- `readiness_outputs_allowed = no`;
- `forced_war_allowed = no`;
- `status = unknown_inert` or `needs_review`.

## Source Freshness

Before relying on source claims:

- verify the local docs index for `local/StellarisMods-docs`;
- refresh it if changed docs or source snapshots are missing;
- verify the code index for `local/StellarisMods-223b92bc` before code navigation;
- refresh source snapshots if the active playset or target game version changes.

Do not use stale Munch results to justify primitives, war-goal support, or generated-file contracts.

## Evidence Rules

- Preserve original vanilla or mod excerpts when they justify a behavior.
- Distinguish vanilla war goals from modded war goals.
- Distinguish confirmed runtime primitives from generator-only design concepts.
- Record source path and date for every primitive or war-goal claim.
- If a primitive is unverified, do not emit it in generated files.
- If a compatibility case is uncertain, prefer explicit exclusion over speculative behavior.

## Review Loop

The classification CSV is a maintenance surface, not a runtime permission slip. A war goal becomes active only when:

1. source evidence is recorded;
2. severity is intentionally assigned;
3. expected outputs are defined;
4. unit tests cover the classification;
5. validator checks include the generated behavior;
6. runtime unknown-inert behavior remains covered.

## Compatibility Review Targets

Review when touched by implementation:

- Gigastructural Engineering war goals, crisis actors, special resources, and country types;
- NSC3 scripted country, fleet, starbase, and ship behavior;
- Extra Ship Components and other ship/component expansion mods;
- Starbase Extended and other starbase-defense mods;
- smarter AI mods;
- performance optimizer mods;
- Nomads;
- Arkships;
- Waystations;
- Waylines;
- Contracts;
- Stellaris 4.4 Situation Log behavior.

For each target, classify as:

- safe interaction;
- explicit exclusion;
- unknown inert;
- needs separate plan.
```

## plans/stellar-ai-director-threat-response/README.md

```markdown
# Stellar AI Director Threat Response Plan Set

Status: expanded planning package.
Source plan: [../stellar-ai-director-threat-response-plan.md](../stellar-ai-director-threat-response-plan.md).
Target game version: Stellaris PC 4.4.4 stable.
Created: 2026-07-05.

This folder splits the original threat-response plan into focused, implementation-ready documents. Treat the source plan as the design brief and this folder as the controlling handoff package for implementation, validation, and review.

## Documents

- [00 Annotated Review](00-annotated-review.md): section-by-section review of the source plan, including gaps that this plan set closes.
- [01 Goals, Deliverables, And Acceptance](01-goals-deliverables-and-acceptance.md): concrete outputs, non-goals, source-of-truth rules, and pass/fail completion criteria.
- [02 Main Implementation Plan](02-main-implementation-plan.md): generator, emitted file, validator, and documentation work to perform.
- [03 Runtime Interaction Contract](03-runtime-interaction-contract.md): event flow, scopes, observer rules, war-goal classification, output precedence, and logical interaction clarifications.
- [04 Risk Prevention And Mitigation](04-risk-prevention-and-mitigation.md): risk register, prevention gates, mitigation paths, rollback boundaries, and stop conditions.
- [05 Testing And Validation Plan](05-testing-and-validation-plan.md): deterministic tests, validator checks, scenario matrix, commands, and manual runtime validation.
- [06 Implementation Slices And Handoff](06-implementation-slices-and-handoff.md): execution order, slice gates, handoff evidence, and completion packaging.
- [07 Research And Evidence Maintenance](07-research-and-evidence-maintenance.md): feasibility note, war-goal classification CSV, source corpus refresh, and audit artifact rules.

## Controlling Rules

- The Python generator in `tools/stellar_ai_director_lib.py` is the source of truth for threat-response constants, tables, generated PDXScript, validation, and research artifacts.
- The generated mod files under `mods/StellarAIDirector/` are outputs. Do not hand-edit them as the durable source of behavior.
- V1 is diplomacy and defensive-readiness pressure only. It must not declare wars, join wars, add punitive CBs, overwrite diplomatic actions, or bypass existing Director survival/recovery/deficit gates.
- Design axes such as `moral_outrage` and `regional_fear` must stay generator-owned. Stellaris runtime artifacts must consume only emitted script values, triggers, flags, events, and opinion modifiers.
- Unknown or unclassified war goals are inert until intentionally classified.

## Done Definition

This plan set is complete enough for implementation only when:

- every deliverable in [01 Goals, Deliverables, And Acceptance](01-goals-deliverables-and-acceptance.md) has a named output and acceptance check;
- every runtime interaction in [03 Runtime Interaction Contract](03-runtime-interaction-contract.md) has a deterministic validation path or is explicitly marked manual/runtime-only;
- every high-risk failure mode in [04 Risk Prevention And Mitigation](04-risk-prevention-and-mitigation.md) has a prevention check and a mitigation path;
- the automated checks in [05 Testing And Validation Plan](05-testing-and-validation-plan.md) pass before any launch or observer-game smoke test;
- completion evidence is captured in the implementation handoff described in [06 Implementation Slices And Handoff](06-implementation-slices-and-handoff.md).
```

## plans/stellar-ai-director-v1-remaining-plan.md

```markdown
# Stellar AI Director V1 Remaining Work Plan

Last updated: 2026-07-04

Owner context: Stellaris modding workspace at `C:\Users\Admin\Documents\GIT\GameMods\StellarisMods`.

Primary target: a late-loading local mod named `Stellar AI Director` that
centralizes deterministic AI decision-tree overrides for the active Irony
playset.

This is a living implementation plan. Update it as work is completed, deferred,
or replaced by better evidence.

## Source Of Truth And Current Evidence

This plan is based on:

- Current user request: create a maximum-effort plan for finishing the AI mod
  patch and save it in a dedicated plan directory.
- Existing project rules in `AGENTS.md`.
- Existing generated mod skeleton under `mods/StellarAIDirector/`.
- Existing tools under `tools/`.
- Current validation commands run on 2026-07-04:
  - `python tools\validate_stellar_ai_director_patch.py`
  - `python -m unittest discover -s tools\tests`
- Current Munch gate result:
  - `jcodemunch_guide` works.
  - `jdatamunch_guide` works.
  - `jdocmunch_guide` returns `Transport closed`.
  - `C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1` fails because
    duplicate live Munch worker processes are present.

Important limitation: this plan does not claim a fresh JDocMunch-backed corpus
review. JDocMunch must be repaired or remounted before any source-corpus-heavy
implementation or final verification is treated as complete.

## Current Verified State

### Existing Mod Skeleton

`mods/StellarAIDirector/` exists and currently contains:

- `descriptor.mod`
- `README.md`
- `common/ai_budget/zzz_staid_alloys_budget.txt`
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt`
- `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`
- `common/script_values/zzz_staid_roi_values.txt`

### Existing Required Parents

`mods/StellarAIDirector/descriptor.mod` currently declares dependencies on:

- `Stellar AI`
- `Gigastructural Engineering & More (4.4)`
- `NSC3`
- `Extra Ship Components NEXT`
- `Starbase Extended 3.0`
- `!!!Universal Resource Patch [2.4+]`

These dependency names still need final launcher/Irony verification against the
actual local mod descriptors and loaded playset names.

### Existing Generated Policy Surface

The current generated patch appears to provide:

- State triggers for:
  - core deficit with short runway;
  - survival mode;
  - recovery mode;
  - megastructure prep readiness;
  - megastructure commit safety;
  - pausing new megastructure starts;
  - shipyard payoff readiness;
  - surplus sink pressure;
  - research sink priority readiness;
  - shipyard expansion readiness;
  - unity sink priority readiness.
- A full-object override of Stellar AI's `alloys_expenditure_megastructures`
  budget object.
- Additive subplans inside `basic_economy_plan` for:
  - mega alloy reserve;
  - Gigas special resource reserve;
  - payoff exploitation alloys.
- Numeric script values for generated ROI thresholds and documentation anchors.

### Existing Tools And Tests

Existing tools:

- `tools/build_active_playset_snapshot.py`
- `tools/build_ai_roi_matrix.py`
- `tools/build_mod_snapshot_inventory.py`
- `tools/generate_stellar_ai_director_patch.py`
- `tools/stellar_ai_director_lib.py`
- `tools/validate_stellar_ai_director_patch.py`

Existing tests:

- `tools/tests/test_stellar_ai_director.py`

Current validation result:

- `python tools\validate_stellar_ai_director_patch.py`: passed.
- `python -m unittest discover -s tools\tests`: 36 tests passed.

### What This Means

The project has a real prototype, not just notes. However, it is not yet a
campaign-ready V1 because it only touches a narrow set of AI surfaces. It still
needs a complete source-corpus-backed audit, broader generated policy surfaces,
load-order verification, conflict verification, Stellaris launch validation,
and later observer testing.

## Definition Of A Working V1

V1 is working when all of these are true:

- The mod loads after every required parent mod whose AI, economy,
  megastructure, tech, starbase, or shipyard logic it intentionally overrides.
- The descriptor and README clearly list hard dependencies and tested version
  assumptions.
- Every generated reference to resources, technologies, ascension perks,
  scripted triggers, scripted values, megastructures, starbase modules,
  buildings, ship sizes, components, events, and defines is verified against the
  active playset or vanilla sources.
- The generated PDXScript validates locally and does not reference disabled or
  missing mods.
- Irony shows only intentional conflicts, especially around AI policy surfaces.
- Stellaris reaches the main menu with the patch enabled.
- The first observer smoke test shows at least one AI empire can remain alive,
  pursue a high-ROI economy or shipyard path when eligible, and avoid obvious
  deficit spirals.
- The plan, README, generated artifacts, and validation outputs explain what
  V1 changes and what it intentionally leaves alone.

## V1 Non-Goals

V1 must not try to solve every possible AI weakness.

Out of scope for V1:

- Self-learning, adaptive, or LLM-style runtime behavior.
- Large UI changes.
- New player-facing content unrelated to AI decision weights.
- Full ship design rewrite unless evidence shows NSC3 or ESC AI design weights
  are unusable.
- Exotic Gigas superprojects as mainline choices unless they are explicitly
  proven safe by tests and source inspection.
- Performance-heavy scripted polling events unless no lighter Stellaris AI
  surface can express the needed decision.
- Blindly overriding large parent mod objects without an ownership note and a
  conflict reason.

## Load Order Target

The patch should be placed very late in the Irony mod list.

Required placement rule:

- `Stellar AI Director` loads after:
  - Stellar AI;
  - Gigastructural Engineering & More (4.4);
  - NSC3;
  - Extra Ship Components NEXT;
  - Starbase Extended 3.0;
  - Universal Resource Patch;
  - any compatibility patch that modifies those parents and is meant to be
    upstream of the Director.

Suggested Irony position:

- Near the bottom of the gameplay section.
- After AI, economy, megastructure, technology, ship/component, and starbase
  mods it coordinates.
- Before only those local or compatibility patches that are intentionally meant
  to override the Director.

Validation requirement:

- Use Irony conflict scan to confirm `Stellar AI Director` wins only the
  intended AI policy conflicts.
- Record every intentional winning conflict in the mod README or a dedicated
  conflict note.
- If another late patch must win over the Director, document the exception and
  why it is safe.

## Remaining Work Dashboard

Status values:

- `Done`: completed and verified.
- `Partial`: some implementation exists but is not enough for V1.
- `Needed`: not implemented yet.
- `Gate`: must pass before dependent work is trustworthy.
- `Deferred`: intentionally not part of V1.

| ID | Workstream | Status | V1 Required | Summary |
| --- | --- | --- | --- | --- |
| P0 | Munch/JDocMunch startup gate | Gate | Yes | Active JDocMunch MCP still fails; duplicate workers exist. |
| P1 | Source corpus freshness and indexes | Partial | Yes | Source snapshots exist, but JDocMunch-backed verification is not fresh. |
| P2 | Playset and dependency lock | Partial | Yes | Descriptor dependencies exist; names and load position need Irony verification. |
| P3 | ROI and market model | Partial | Yes | Strong tests exist; coverage must expand beyond current ROI targets. |
| P4 | Decision tree model | Partial | Yes | Offline tests exist; more scenarios and PDX mapping needed. |
| P5 | Generated PDXScript policy surfaces | Partial | Yes | Current patch touches budgets/plans/triggers only. |
| P6 | Tech, AP, tradition, and unlock prioritization | Needed | Yes | Must prioritize unlock chains for required mods. |
| P7 | Megastructure and gigastructure build priorities | Partial | Yes | ROI matrix exists; per-object AI weights still need generated overrides. |
| P8 | Shipyard, fleet throughput, and ship production sinks | Partial | Yes | Strategic shipyard math exists; policy needs in-game surface mapping. |
| P9 | Starbase and defensive economy logic | Needed | Yes | Required by user preference; no generated starbase policy yet. |
| P10 | Planetary/building capacity use | Needed | Should | Required if active mods expand planet capacity. |
| P11 | NSC3/ESC integration | Partial | Yes | V1 currently leaves design weights untouched; tech/use audit needed. |
| P12 | Validator hardening | Partial | Yes | Current validator passes; must cover more PDX surfaces and load-order checks. |
| P13 | Irony conflict and load-order validation | Needed | Yes | No recorded Irony conflict pass yet. |
| P14 | Stellaris launch validation | Needed | Yes | Main-menu launch not recorded. |
| P15 | Observer smoke test | Needed | Yes | Needed before calling campaign-ready. |
| P16 | Documentation and tuning loop | Partial | Yes | README exists; needs conflict notes, tuning knobs, and test log. |

## Phase P0 - Tooling Gate And Shared Munch Direction

Objective: restore reliable tooling before corpus-heavy implementation.

Current defect:

- The active Codex thread still cannot call `jdocmunch_guide`.
- The startup checker reports duplicate `jcodemunch-mcp` and `jdatamunch-mcp`
  processes.
- Current Munch config uses per-client stdio commands, which cannot guarantee a
  single universal tool instance across Codex threads.

Keep unchanged:

- Do not enable JDocMunch embeddings unless explicitly requested.
- Do not treat CLI fallbacks as equivalent to active-thread MCP health.
- Do not launch nested Codex sessions as a normal preflight.

Tasks:

- [ ] Decide the immediate operational path:
  - close/restart Codex to clear duplicate worker processes; or
  - manually terminate orphaned Munch workers only after confirming they are not
    attached to active work; or
  - move directly to a shared service transport if available.
- [ ] Re-run:
  - `C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1`
- [ ] Confirm active-thread guide calls:
  - `jdocmunch_guide`
  - `jcodemunch_guide`
  - `jdatamunch_guide`
- [ ] Research whether current Munch MCP packages expose streamable HTTP or SSE
  transport.
- [ ] If they do not, create a separate plan to add a local singleton service
  wrapper or upstream transport support.
- [ ] Record final tooling state in Open Brain.

Acceptance criteria:

- The startup checker passes.
- Active-thread guide calls all return content.
- Future work can use JDocMunch for source/document navigation instead of raw
  full-file reads.
- There is a written next step for singleton service transport if the current
  packages remain stdio-only.

## Phase P1 - Source Corpus Freshness And Index Recovery

Objective: ensure the patch is based on current, indexed sources.

Current defect:

- Source snapshots exist under `research/mod-source-snapshots/2026-07-04/`.
- JDocMunch is not currently available in the active thread for documentation
  and section navigation.
- It is not yet proven that every gameplay-heavy source folder is indexed and
  queryable.

Tasks:

- [ ] Verify snapshot manifest freshness:
  - `research/mod-source-snapshots/2026-07-04/snapshot-manifest.csv`
  - `research/mod-source-snapshots/2026-07-04/descriptor-inventory.csv`
  - `research/mod-source-snapshots/2026-07-04/pdx-object-inventory.csv`
  - `research/mod-source-snapshots/2026-07-04/ai-surface-inventory.csv`
- [ ] Rebuild snapshot inventory from the active Irony playset.
- [ ] Use JDocMunch after P0 to index or verify documentation and text-heavy
  research surfaces.
- [ ] Use JCodeMunch for tools and generated Python code when code navigation is
  needed.
- [ ] Use JDataMunch for CSV matrices instead of manual CSV inspection once the
  relevant datasets are indexed.
- [ ] Create a short corpus status note with:
  - snapshot date;
  - active playset name;
  - required parent mods present;
  - optional gameplay mods detected;
  - files/folders omitted from indexing and why.

Acceptance criteria:

- Every required parent mod source root is present.
- Every required parent descriptor is mapped to a stable local snapshot path.
- Object inventory includes resources, technologies, APs, megastructures,
  starbase modules/buildings, ship sizes, components, scripted triggers,
  scripted values, events, and economic plans.
- Any missing or unparseable source surface is listed with exact examples and a
  follow-up task.

## Phase P2 - Playset And Dependency Lock

Objective: lock the exact playset and dependency contract for V1.

Current defect:

- Descriptor dependencies exist, but the exact launcher/Irony names and load
  ordering still need verification.

Tasks:

- [ ] Read the active Irony selected collection.
- [ ] Confirm all required parent mods are installed and enabled.
- [ ] Verify local descriptor names exactly match `descriptor.mod`
  dependency names.
- [ ] Add missing dependency aliases or correct names if Paradox launcher names
  differ from workshop names.
- [ ] Generate a load-order note under either:
  - `mods/StellarAIDirector/notes/load-order.md`; or
  - `research/stellar-ai/stellar-ai-director-load-order-2026-07-04.md`.
- [ ] Document the intended Irony placement:
  - after required parents;
  - after parent compatibility patches the Director must supersede;
  - before any local patch intentionally overriding the Director.
- [ ] Add a final mod-list entry or import helper only after Irony workflow is
  clear.

Acceptance criteria:

- The mod descriptor has verified dependency names.
- The README names the required load-order position.
- There is an explicit list of upstream mods whose AI behavior the Director
  intentionally coordinates.
- Irony can place the patch where it wins intended conflicts.

## Phase P3 - ROI And Market Model Hardening

Objective: make the ROI model good enough to drive generated priorities.

Current state:

- ROI extraction exists.
- Inline script and variable expansion tests exist.
- Dyson wrapper costs are no longer zero in tests.
- Market-aware conversion tests exist, including alloy base and ceiling price
  behavior and the mineral-to-alloy stress conversion concern.
- Current tests report at least 140 eligible ROI rows.

Remaining defects:

- The ROI model still needs broader coverage beyond current target names.
- Some resources are intentionally unpriced and must be handled as bottleneck
  gates rather than forced into a fake scalar value.
- Strategic utility values need explicit caps and scenario multipliers so a
  shipyard or defense structure is not judged only by income production.

Tasks:

- [ ] Expand ROI extraction coverage for all required parent mods:
  - vanilla megastructures;
  - Gigastructural Engineering megastructures/gigastructures;
  - NSC3 megastructures and shipyard structures;
  - Starbase Extended modules/buildings;
  - relevant ESC resource consumers/unlocks.
- [ ] Separate ROI categories:
  - direct economy producer;
  - bottleneck resource producer;
  - shipyard throughput multiplier;
  - naval cap multiplier;
  - defensive leverage structure;
  - research acceleration;
  - unity/tradition acceleration;
  - prerequisite unlock;
  - exotic/superproject.
- [ ] Preserve unpriced resources as named bottlenecks:
  - do not hide them inside a fake all-purpose value;
  - expose them as required-resource gates;
  - add scarcity and surplus columns.
- [ ] Add scenario-specific valuation columns:
  - base-market cost;
  - deficit-market cost;
  - surplus-liquidation payoff;
  - market-fee-aware cost;
  - resource-bottleneck relief;
  - shipyard throughput value;
  - defensive leverage value;
  - unlock-chain value.
- [ ] Add diminishing return handling:
  - research value before and after very high research income;
  - alloy value when alloy income is negative, adequate, high, or stockpile-capped;
  - energy/mineral/CG value under deficit and surplus;
  - rare resource value when needed by queued construction or ship components.
- [ ] Add per-resource runway columns:
  - `resource_deficit_runway_months`;
  - `stockpile_required_for_safe_commit`;
  - `required_surplus_income_before_start`;
  - `emergency_abort_threshold`.
- [ ] Add tests for specific named structures:
  - Gigas Dyson variants;
  - Matrioshka-style research structures;
  - Neutronium Gigaforge;
  - Nidavellir;
  - HRAE;
  - NSC3 mega shipyard stages;
  - vanilla Mega Shipyard;
  - Starbase Extended high-defense modules;
  - at least one special-resource bottleneck path.

Acceptance criteria:

- No decision-eligible row has zero cost unless the source truly defines no
  cost and the row explains why.
- No decision-eligible row has unresolved cost/upkeep/production without a
  visible `data_quality` reason.
- Every unpriced resource is preserved as a named bottleneck.
- Strategic objects that do not produce income still receive strategy roles.
- ROI rows are stable enough that generated thresholds do not swing wildly from
  parsing noise.

## Phase P4 - Decision Tree Model Hardening

Objective: finish the deterministic logic model before emitting broader script.

Current state:

- Offline `EmpireState` tests exist for survival, recovery, prep, commit,
  payoff exploitation, surplus research/fleet/unity sinks, war interruption,
  lost economy, and shipyard support.

Remaining defects:

- Offline model needs more scenarios.
- Offline model needs clearer mapping to actual Stellaris triggers.
- Emergency exits need deeper coverage for resource-specific collapse.

Tasks:

- [ ] Expand offline state model inputs:
  - at war;
  - war exhaustion;
  - lost war;
  - lost territory/economy fraction;
  - fleet power ratio if available;
  - used naval capacity;
  - fleet upkeep pressure;
  - starbase choke coverage;
  - alloy/energy/mineral/CG/food/special-resource income;
  - stockpile runway by resource;
  - active megastructure progress;
  - construction capacity;
  - research sink availability;
  - fleet sink availability;
  - unity sink availability;
  - personality posture.
- [ ] Define deterministic states:
  - `survival_mode`;
  - `recovery_mode`;
  - `normal_growth_mode`;
  - `investment_prep_mode`;
  - `investment_commit_mode`;
  - `payoff_exploitation_mode`;
  - `research_expansion_mode`;
  - `shipyard_expansion_mode`;
  - `unity_expansion_mode`;
  - `defensive_fortification_mode`;
  - `superproject_mode` gated or disabled for V1.
- [ ] Add escape hatch tests:
  - war starts during prep with weak fleet;
  - war starts near completion with safe runway;
  - half economy lost during commit;
  - energy deficit from fleet upkeep;
  - rare resource deficit from advanced components;
  - alloy stockpile capped with insufficient shipyard capacity;
  - massive energy surplus but alloy bottleneck;
  - defensive personality at chokepoint;
  - aggressive personality with sustainable fleet budget;
  - crisis or rival pressure forcing defense before long-payoff projects.
- [ ] Define exact state precedence:
  - survival always wins;
  - recovery beats new investment;
  - near-complete commit can continue only with safe runway;
  - payoff exploitation only after the relevant completed project exists;
  - surplus sinks only after economy safety gates pass.
- [ ] Document personality modifiers:
  - defensive empires prefer chokepoint starbases and lower idle fleet upkeep;
  - aggressive empires tolerate higher fleet spending if income supports it;
  - research-focused empires prioritize research sinks earlier;
  - isolationist/tall empires bias toward defensive and megastructure paths.

Acceptance criteria:

- Offline tests cover all state transitions and negative paths.
- Every PDXScript trigger has a corresponding offline model concept or a
  documented engine-only reason.
- The decision tree cannot choose new long-payoff investment during short
  resource runway survival cases.
- The decision tree can choose high-ROI investment when a stable empire is
  strong enough to survive the upfront cost.

## Phase P5 - Generated PDXScript Policy Surfaces

Objective: expand from prototype triggers/budget/plans to a coherent generated
patch.

Current state:

- Current generated PDX surfaces are narrow and mostly additive, except one
  intentional budget override.

Remaining defects:

- The patch does not yet centralize all relevant AI modifications.
- It does not yet emit tech/AP/tradition/starbase/megastructure priority
  overrides.
- It does not yet provide enough in-game weight surfaces to force the desired
  strategic behavior.

Tasks:

- [ ] Inventory all relevant AI-bearing PDX object types in required parents:
  - `common/ai_budget`;
  - `common/economic_plans`;
  - `common/megastructures`;
  - `common/technology`;
  - `common/ascension_perks`;
  - `common/traditions`;
  - `common/starbase_modules`;
  - `common/starbase_buildings`;
  - `common/buildings`;
  - `common/ship_sizes`;
  - `common/component_templates`;
  - scripted triggers/effects/values used by those objects.
- [ ] Categorize each target as:
  - additive new object;
  - full-object override;
  - no safe direct override;
  - defer to parent mod;
  - needs compatibility patch.
- [ ] For every full-object override:
  - add an ownership comment;
  - list parent source path;
  - list exact reason for override;
  - verify no unrelated behavior was dropped.
- [ ] Generate focused files by responsibility:
  - `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`;
  - `common/script_values/zzz_staid_roi_values.txt`;
  - `common/ai_budget/zzz_staid_alloys_budget.txt`;
  - `common/economic_plans/zzzz_staid_additive_economic_plan.txt`;
  - new tech weight file if safe;
  - new megastructure override file if required;
  - new starbase policy file if required;
  - new AP/tradition weight file if required.
- [ ] Avoid dumping every override into one giant file.
- [ ] Keep generated comments concise but enough for conflict review.

Acceptance criteria:

- Generated files are small enough to review by surface.
- Every generated reference is validated.
- Every broad override has an ownership note.
- No generated file references optional mods unless the generator proves they
  exist or guards them safely.

## Phase P6 - Technology, Ascension Perk, Tradition, And Unlock Priorities

Objective: make the AI actually unlock the paths needed for late-game power.

Current defect:

- Current prototype does not emit direct technology/AP/tradition prioritization.
- The AI may build a stronger economy but still fail to research or select the
  unlocks that make Gigas/NSC3/ESC scaling possible.

Tasks:

- [ ] Inventory all required unlock tech chains:
  - vanilla megastructure chain;
  - Gigas megastructure/gigastructure unlocks;
  - Gigas special resource unlocks;
  - NSC3 ship size and shipyard unlocks;
  - ESC advanced weapons/reactors/shields/armor/resource unlocks;
  - Starbase Extended defense unlocks.
- [ ] Identify AI weight surfaces for technologies.
- [ ] Add priority bands:
  - survival economy tech;
  - research economy tech;
  - mega-engineering prerequisites;
  - first high-ROI economy multiplier;
  - shipyard/fleet throughput;
  - advanced military component unlocks;
  - defensive starbase unlocks;
  - repeatables after core modded unlocks.
- [ ] Inventory ascension perks that unlock mega/giga progression.
- [ ] Add AP strategy:
  - prioritize required mega/giga APs when economy and tech prerequisites are
    ready;
  - avoid taking dead-end APs that block key build paths;
  - allow personality-specific variation only after core unlock path remains
    viable.
- [ ] Inventory tradition mods if active playset expands tradition count/options.
- [ ] Add tradition strategy only if active mods require it for the core loop.
- [ ] Add validation that every referenced tech/AP/tradition exists.

Acceptance criteria:

- AI can reach modded construction prerequisites, not only vanilla endgame.
- Research-heavy Stellar AI behavior is preserved but extended into modded
  unlocks.
- No tech/AP/tradition reference is emitted without validation.

## Phase P7 - Megastructure And Gigastructure Build Priority Overrides

Objective: convert ROI analysis into actual AI build priorities.

Current defect:

- ROI analysis identifies candidates, but generated PDX does not yet clearly
  alter individual megastructure/gigastructure build weights.

Tasks:

- [ ] For each decision-eligible structure, classify:
  - buildable by normal empire;
  - requires special origin/civic/path;
  - requires unique resource;
  - requires site/star/body type;
  - one-per-empire or limited count;
  - dangerous or exotic.
- [ ] Build priority tiers:
  - first economy multiplier;
  - first research multiplier;
  - special resource bottleneck;
  - shipyard throughput;
  - defensive leverage;
  - second bottleneck project;
  - optional/superproject.
- [ ] Add site-selection logic where the same structure has variants:
  - Dyson star variants;
  - Matrioshka star variants;
  - other Gigas wrapper variants.
- [ ] Generate AI weights with gates:
  - do not start if survival/recovery;
  - prefer high ROI when prep-ready;
  - continue near-complete projects when runway is safe;
  - pause new projects under war/fleet emergency;
  - bias to bottleneck relief based on resource deficits.
- [ ] Keep superprojects disabled or heavily gated:
  - require overwhelming economy;
  - require safe fleet/defense;
  - require completed core loop;
  - require no critical deficits.

Acceptance criteria:

- The AI can select a first high-ROI economy megastructure.
- The AI can prefer better star/body variants when multiple options exist.
- Shipyard megastructures are valued as throughput sinks, not income producers.
- Exotic projects do not derail normal AI survival.

## Phase P8 - Shipyard, Fleet Throughput, And Surplus Sink Logic

Objective: let AI convert huge economy into military power without collapse.

Current state:

- ROI tests include strategic shipyard throughput for NSC3 mega shipyard stages.
- Decision tests include surplus fleet sink behavior.

Remaining defects:

- In-game PDX mapping for shipyard/fleet expansion is not complete.
- The AI must avoid building a massive shipyard before it has economy to use it.

Tasks:

- [ ] Define shipyard expansion prerequisites:
  - alloy income high enough;
  - energy income high enough;
  - stockpile near cap or unable to spend alloys;
  - fleet buildup desired;
  - current shipyard capacity inadequate or strategic war plan requires burst
    production.
- [ ] Define when shipyard expansion is bad:
  - low alloy income;
  - negative energy runway;
  - fleet upkeep already causing collapse;
  - no strategic need and better research sink exists.
- [ ] Map shipyard strategy to actual AI surfaces:
  - megastructure AI weight;
  - starbase shipyard modules if relevant;
  - naval cap budget;
  - fleet build budget;
  - economy plans for alloys/energy/special resources.
- [ ] Add tests:
  - alloy stockpile capped -> shipyard/fleet sink;
  - high economy but no tech -> prioritize unlock;
  - shipyard completed but alloy income too low -> recovery/economy first;
  - shipyard completed and economy strong -> fleet payoff exploitation.
- [ ] Decide whether NSC3/ESC ship design weights need V1 overrides:
  - audit first;
  - leave untouched if parent AI weights are adequate;
  - override only if evidence shows AI cannot use bigger ships/components.

Acceptance criteria:

- Mega Shipyard and NSC3 shipyard structures get strategic weight when the AI
  has excess economy.
- The AI does not overbuild ships into an energy/alloy upkeep death spiral.
- Research remains the first surplus sink when relevant unlocks are still
  available.

## Phase P9 - Starbase And Defensive Economy Logic

Objective: make defensive empires use static defenses and chokepoints better.

Current defect:

- No generated starbase policy exists yet.

Tasks:

- [ ] Inventory Starbase Extended modules/buildings and defensive modifiers.
- [ ] Inventory vanilla starbase defensive AI weights.
- [ ] Identify choke/defense triggers Stellaris exposes to AI weights.
- [ ] Define defensive strategy:
  - chokepoint starbases reduce required idle fleet spending;
  - defensive personalities bias toward starbases before oversized idle fleets;
  - aggressive empires still prefer fleet if they can use it offensively;
  - crisis/rival pressure increases defense priority.
- [ ] Add starbase ROI categories:
  - defensive leverage;
  - naval cap support;
  - shipyard support;
  - trade/economy support;
  - special module support.
- [ ] Generate starbase weights only where source supports safe overrides.
- [ ] Add tests:
  - defensive empire with choke and safe economy chooses starbase investment;
  - defensive empire with deficit does not overbuild;
  - aggressive empire with strong economy still prioritizes fleet expansion;
  - crisis pressure increases defensive priority.

Acceptance criteria:

- Defensive empires get a clearer static-defense path.
- Starbase investment does not replace survival/recovery gates.
- The plan records which starbase surfaces could not be safely controlled.

## Phase P10 - Planetary And Building Capacity Logic

Objective: ensure AI uses expanded planet capacity if active mods add it.

Current defect:

- No generated planet/building policy exists yet.
- It is not yet proven whether the active playset expands building slots,
  districts, planet classes, or special planet infrastructure in a way the AI
  ignores.

Tasks:

- [ ] Inventory active mods that change:
  - building slots;
  - districts;
  - planet classes;
  - special deposits;
  - jobs;
  - automation plans;
  - economic plans.
- [ ] Determine whether Stellar AI already covers those surfaces.
- [ ] Add economy-plan targets only for high-impact missing resource paths.
- [ ] Avoid broad planet automation rewrites in V1 unless evidence shows a major
  gap.
- [ ] Add tests or validation rows for any generated building/job references.

Acceptance criteria:

- V1 either covers expanded planet capacity or explicitly documents why the
  active playset does not need extra planet logic.
- No generated building/job reference is unverified.

## Phase P11 - NSC3 And ESC Integration

Objective: ensure AI can use bigger ships and stronger components without a
large risky ship-design rewrite.

Current state:

- V1 README says NSC3 and ESC ship/component design weights are left untouched.

Remaining defect:

- It is not yet proven that leaving them untouched is enough.

Tasks:

- [ ] Inventory NSC3 AI surfaces:
  - ship sizes;
  - section templates;
  - shipyards;
  - naval cap effects;
  - technologies;
  - AI weights.
- [ ] Inventory ESC AI surfaces:
  - component templates;
  - strategic resource requirements;
  - technologies;
  - AI weights.
- [ ] Determine the minimum V1 intervention:
  - tech unlock prioritization only;
  - resource economy support;
  - shipyard throughput support;
  - direct ship/component weights if required.
- [ ] Add special-resource gates so AI does not research/build components it
  cannot sustain.
- [ ] Add tests for referenced NSC3/ESC IDs.
- [ ] Document any parent AI weights deliberately preserved.

Acceptance criteria:

- AI is more likely to unlock NSC3/ESC power paths.
- AI has economy support for components that consume advanced resources.
- Direct ship/component overrides are either implemented with evidence or
  explicitly deferred with reasons.

## Phase P12 - Validator Hardening

Objective: make invalid generated patches fail before Stellaris launch.

Current state:

- `validate_generated_patch()` exists and passes.

Remaining defects:

- Validator must cover every new surface added after the prototype.
- It must detect broad override risk and missing load-order assumptions.

Tasks:

- [ ] Add validation categories:
  - required parent mod present;
  - descriptor dependency name matches local descriptor;
  - generated file path is valid for Stellaris;
  - generated object references exist;
  - scripted trigger references exist;
  - scripted value references exist;
  - resource references exist;
  - technology references exist;
  - AP/tradition references exist;
  - megastructure references exist;
  - starbase module/building references exist;
  - ship size/component references exist;
  - event references exist if used;
  - optional references are guarded or omitted;
  - no broad override without ownership note.
- [ ] Add syntax-level checks:
  - parser can parse generated PDX;
  - braces are balanced;
  - no accidental unresolved template placeholders;
  - no disabled-mod references.
- [ ] Add data-quality checks:
  - no decision-eligible zero-cost rows unless explained;
  - no unresolved decision-eligible rows;
  - all generated thresholds come from eligible rows;
  - market price inputs are present.
- [ ] Add load-order checks:
  - Director dependencies present;
  - Director should be after required parents;
  - conflict owner list generated.

Acceptance criteria:

- A missing tech/resource/megastructure ID fails validation.
- An unguarded optional mod reference fails validation.
- A full-object override without ownership note fails validation.
- The validator is the main pre-launch gate before Irony/Stellaris.

## Phase P13 - Irony Conflict And Load-Order Validation

Objective: prove the patch wins only intended conflicts.

Tasks:

- [ ] Install or expose `mods/StellarAIDirector` to the Paradox launcher local
  mod folder if not already visible.
- [ ] Add the mod to the active Irony playset.
- [ ] Move it near the bottom after required parent mods.
- [ ] Run Irony conflict scan.
- [ ] Export or record conflict results.
- [ ] Classify conflicts:
  - intentional Director wins;
  - parent wins required;
  - harmless duplicate/additive;
  - unexpected conflict requiring code change;
  - false positive or cosmetic only.
- [ ] Update README/conflict notes with intentional conflicts.
- [ ] Re-run generated validation after any conflict-driven change.

Acceptance criteria:

- Irony conflict scan has no unexplained AI/gameplay conflicts.
- Load-order position is documented.
- The patch descriptor and README match the actual playset.

## Phase P14 - Stellaris Launch Validation

Objective: prove the generated patch loads into the game.

Tasks:

- [ ] Launch Stellaris with only required parent mods plus Director if practical.
- [ ] Launch with the full active playset plus Director.
- [ ] Reach main menu.
- [ ] Inspect:
  - `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\error.log`
  - `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs\game.log`
- [ ] Record:
  - game version;
  - DLC state if known;
  - playset name;
  - mod order date;
  - errors/warnings relevant to Director files.
- [ ] Fix any missing reference, syntax, or load-order errors.

Acceptance criteria:

- Main menu loads.
- No Director-caused fatal errors.
- No missing generated object references in logs.
- Known unrelated warnings are documented separately.

## Phase P15 - Observer Smoke Test

Objective: verify the decision tree does something useful in a running game.

Tasks:

- [ ] Create a repeatable observer test setup:
  - galaxy size;
  - AI count;
  - difficulty;
  - crisis settings;
  - mod list hash or exported order;
  - test duration checkpoints.
- [ ] Add logging or manual tracking for:
  - AI economy growth;
  - first mega-engineering unlocks;
  - first high-ROI megastructure starts;
  - completion of first economy multiplier;
  - shipyard/fleet payoff behavior;
  - deficit spirals;
  - war interruptions;
  - starbase defense investment.
- [ ] Run first short observer test:
  - early to midgame checkpoint;
  - verify no immediate AI self-sabotage.
- [ ] Run first long observer test:
  - into late game;
  - verify at least one AI starts/completes/exploits a high-ROI path.
- [ ] Record outcomes in `mods/StellarAIDirector/notes/observer-test-log.md`.

Acceptance criteria:

- At least one AI empire reaches a modded high-ROI path.
- AI does not broadly collapse from Director-induced overspending.
- If behavior is wrong, tuning changes are recorded against exact observed
  symptoms.

## Phase P16 - Documentation, Tuning, And Maintenance Loop

Objective: make the mod easy to update after real gameplay feedback.

Tasks:

- [ ] Update `mods/StellarAIDirector/README.md` with:
  - exact hard dependencies;
  - load-order position;
  - validation commands;
  - intentional override list;
  - known limitations;
  - tuning workflow.
- [ ] Add `mods/StellarAIDirector/notes/` if it does not exist.
- [ ] Add notes:
  - `load-order.md`;
  - `conflicts.md`;
  - `observer-test-log.md`;
  - `tuning-notes.md`.
- [ ] Add a generated tuning report from ROI/decision outputs.
- [ ] Keep CSVs as analysis inputs, not runtime files:
  - document which CSV columns feed generation;
  - document which values are hand-tunable;
  - document how to regenerate after changing weights.
- [ ] Add tuning knobs to the generator:
  - prep stockpile multiplier;
  - commit reserve multiplier;
  - deficit runway months;
  - shipyard surplus threshold;
  - research/fleet/unity sink ordering;
  - defensive starbase personality multiplier;
  - superproject gate.
- [ ] Add tests that fail when tuning knobs produce unsafe thresholds.

Acceptance criteria:

- A future agent can change weights without reading the whole chat history.
- A player feedback note can be translated into a small generator/config change.
- Generated files remain reproducible from tools and source snapshots.

## Implementation Slice Order

Use this order unless a later discovery proves it wrong:

1. P0: Repair Munch gate enough for source-corpus work.
2. P1: Refresh source snapshots and indexes.
3. P2: Verify playset dependencies and load-order names.
4. P12: Harden validator before adding more generated surfaces.
5. P3: Expand ROI/data model coverage.
6. P4: Expand offline decision-tree scenarios.
7. P6: Add tech/AP/tradition unlock strategy.
8. P7: Add megastructure/gigastructure priority generation.
9. P8: Add shipyard/fleet throughput policy.
10. P9: Add starbase defensive policy.
11. P11: Audit NSC3/ESC and add only required minimal overrides.
12. P10: Add planet/building capacity policy only if active mods require it.
13. P13: Irony conflict validation.
14. P14: Stellaris main-menu validation.
15. P15: Observer smoke tests.
16. P16: Documentation and tuning loop.

## Risk Register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| JDocMunch remains unavailable in active threads | Source review becomes slow and error-prone | Treat P0 as first gate; do not claim corpus-complete verification without it. |
| Duplicate Munch workers hide stale handles | Agents believe tools work when active thread is broken | Startup checker fails on duplicates; move toward singleton service. |
| Wrong descriptor dependency names | Launcher does not enforce parent order | Verify names against local descriptors and Irony. |
| Full-object override drops parent behavior | Breaks parent mod AI or compatibility | Ownership notes, source diff review, validator rule. |
| Stellaris trigger/effect assumptions are wrong | Script loads with errors or silently fails | Verify against vanilla/current mod sources, CWTools, and logs. |
| ROI scalar hides resource scarcity | AI chooses bad projects during bottlenecks | Preserve per-resource columns and bottleneck gates. |
| Shipyard treated as income producer | AI undervalues throughput sink | Keep strategic shipyard valuation separate from income ROI. |
| AI overbuilds fleet after payoff | Energy/alloy upkeep death spiral | Add fleet upkeep and runway escape hatches. |
| Research sink over-prioritized forever | AI delays fleet/defense despite danger | State precedence and threat gates. |
| Starbase defense over-prioritized | Passive empires waste resources on static defense | Personality/threat/choke gates and negative tests. |
| Exotic Gigas projects destabilize AI | AI burns economy on unsafe superprojects | Disable or heavily gate superproject mode in V1. |
| Irony conflict scan reveals broad conflicts | Patch cannot safely load late as planned | Split overrides or defer unsafe surfaces. |
| Main-menu logs show missing IDs | Patch not ready for play | Validator expansion and log-driven fixes. |

## Exact Validation Commands

Run from `C:\Users\Admin\Documents\GIT\GameMods\StellarisMods`.

Tooling gate:

```powershell
& 'C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1'
```

Generator:

```powershell
python tools\generate_stellar_ai_director_patch.py
```

Patch validator:

```powershell
python tools\validate_stellar_ai_director_patch.py
```

Unit tests:

```powershell
python -m unittest discover -s tools\tests
```

Optional syntax and hygiene:

```powershell
git diff --check
```

Manual validation:

- Irony conflict scan.
- Stellaris main-menu launch.
- `error.log` and `game.log` review.
- Observer smoke test.

## Completion Checklist For V1

- [ ] P0 Munch gate passes.
- [ ] P1 source corpus/index status is current.
- [ ] P2 dependency names and load order are verified.
- [ ] P3 ROI matrix covers required parent surfaces.
- [ ] P4 decision tree tests cover emergency exits and surplus sinks.
- [ ] P5 generated PDX surfaces are expanded and documented.
- [ ] P6 tech/AP/tradition unlocks are prioritized or explicitly deferred.
- [ ] P7 megastructure/gigastructure weights are generated and validated.
- [ ] P8 shipyard/fleet throughput logic is generated and validated.
- [ ] P9 starbase defense logic is generated or explicitly deferred with reason.
- [ ] P10 planet/building expansion logic is covered or ruled out.
- [ ] P11 NSC3/ESC integration is audited and minimally patched if needed.
- [ ] P12 validator catches missing references and unsafe overrides.
- [ ] P13 Irony conflict scan is reviewed and documented.
- [ ] P14 Stellaris reaches main menu with the patch enabled.
- [ ] P15 observer smoke test confirms at least one useful high-ROI AI path.
- [ ] P16 README/notes/tuning docs are current.

## Current Best Estimate

Assuming P0 tooling is restored first:

- Minimal V1 that loads and has broader generated priorities: 4 to 8 focused
  hours.
- V1 with Irony conflict validation and main-menu launch: about 1 focused day.
- V1 that is trustworthy for a real campaign: 1 to 2 focused days plus observer
  test time.
- Tuned behavior that consistently challenges the player in late game: iterative
  work over multiple observer/play sessions.

The largest unknown is not writing files. The largest unknown is mapping the
right Stellaris AI surfaces without accidentally overriding too much parent mod
behavior.
```
