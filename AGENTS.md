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

### Skill Issue Review Queue

- Whenever a skill file causes confusion, misrouting, missing context, weak guidance, bad defaults, stale evidence, validation friction, or any other rough edge, save an Open Brain memory for the Global Skill Reviewer before finishing the task.
- The memory must include the skill name/path, the user task, what went wrong or felt unclear, why it mattered, related files/paths/evidence, the workaround used, and the suggested review or improvement.
- Also tell the user that the skill issue was queued for Global Skill Reviewer attention, including the affected skill and short issue summary, so the user can decide whether it should be fixed immediately instead of waiting for the reviewer.
- If Open Brain capture is unavailable, emit a `memory_candidate` with the same review details and still notify the user.

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
