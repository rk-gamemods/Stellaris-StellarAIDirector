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
- Before non-trivial Stellaris work, obey the global Munch MCP startup gate: exact guide discovery, active-thread guide calls, and `C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1`. Do not continue Munch-dependent project work when active-thread guide calls fail, even if CLI fallbacks work.
- For JDocMunch specifically, partial lazy-loaded tool discovery is not proof of unavailability. Before using a CLI fallback or reporting missing tools, run exact discovery for the canonical tools: `jdocmunch_guide`, `search_sections`, `get_section`, `get_sections`, `list_docs`, `get_doc`, `get_toc`, `verify_index`, and `index_local`.
- Start JDocMunch work by calling `jdocmunch_guide` when the MCP tool is exposed. If exact discovery exposes tools but an MCP call fails with `Transport closed`, classify the cause as a tool-surface problem such as stale active-session handle, remount requirement, config/version issue, or process failure. Do not phrase it as "JDocMunch is unavailable" without that diagnosis.
- When JDocMunch MCP fails but the installed CLI works, use the CLI only as a temporary fallback while recording the exact blocker and likely recovery path. Save the conclusion in Open Brain before finishing the task.
- Do not launch nested Codex sessions as a routine Munch preflight. Multiple live Munch MCP server processes are diagnostic in Codex Desktop stdio sessions, not by themselves a reason to kill processes or block work when active-thread guide calls return content. If guide calls return `Transport closed`, treat the active thread as stale/remount-required and follow the global Munch gate.
- Tested recovery for stale Munch handles in this project: fork the current Codex thread into the same directory, then rerun exact guide discovery, all three mounted guide calls, and the patched preflight. The same-directory fork reset `Transport closed` without closing Codex; do not rely on process killing as the reset mechanism.
- For local Stellaris project indexing, keep JDocMunch embeddings disabled unless the user explicitly asks to enable them. Prefer `use_embeddings=false` or `JDOCMUNCH_EMBEDDING_PROVIDER=none` for index refreshes.

## Stellaris Modding Defaults

- Target Stellaris PC 4.4.4 stable unless the task explicitly says 4.4.5 beta, 4.5 beta, or another version.
- Use `supported_version="v4.4.*"` for stable 4.4 descriptors, but remember this is launcher-facing metadata only and does not determine whether script code loads.
- Treat 4.4.5 as a beta branch and 4.5 as a separate porting branch, especially for pop, faction, ethic, job, species, workforce, UI, and AI-economy changes.
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
- Launch-test in Stellaris after meaningful gameplay or UI changes.
- Record known conflicts, required DLC, and tested game version in the mod README.

## Research Expectations

For any non-trivial mod, create a note in `research/` or the mod's own `notes/` folder that captures:

- target Stellaris version;
- relevant vanilla files inspected;
- likely compatibility conflicts;
- DLC assumptions;
- test steps;
- open questions.
