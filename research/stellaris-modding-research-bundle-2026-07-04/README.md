# Stellaris modding research bundle for Codex

Generated: 2026-07-04
Target game: Stellaris PC 4.4.x. This bundle was collected on 2026-07-04 when 4.4.4 was live and 4.4.5 was beta; as of 2026-07-08, treat 4.4.5 stable/current local install as the active target and keep 4.4.4 content as historical evidence.
Primary consumer: Codex / coding agent / mod developer.

## Contents

- `FULL_RESEARCH_REPORT.md` — full narrative research report with action rules, caveats, and source IDs.
- `CODEX_BRIEF.md` — compressed operational brief for a coding agent.
- `CURRENT_VERSION_AND_STRUCTURAL_CHANGES.md` — version matrix, 4.0/4.4/4.4.5/4.5 impact analysis.
- `MOD_STRUCTURE_AND_SETUP.md` — exact local directory layout, descriptors, metadata, folder mirroring, naming and localisation rules.
- `LOAD_ORDER_OVERRIDES_AND_CONFLICTS.md` — priority model, FIOS/LIOS caveats, conflict/patching strategy.
- `SCRIPTED_VS_NONSCRIPTED_MODS.md` — PDXScript vs content/UI/asset mods and external companion apps.
- `BEST_PRACTICES_TOOLS_RESOURCES.md` — toolchain and maintenance practices.
- `TROUBLESHOOTING_DEBUGGING_AI.md` — debug workflow, console/logging, AI-assisted debugging patterns, direct game-state inspection options.
- `LLM_AI_PROJECTS_INVENTORY.md` — inventory of LLM-adjacent projects and feasibility assessment for LLM-driven empire control.
- `PORTING_AND_REGRESSION_CHECKLISTS.md` — actionable checklists for 4.4.x and 4.5.
- `VALIDATION_CAVEATS_AND_OPEN_QUESTIONS.md` — what must be verified against the actual target game files, Irony, or runtime logs.
- `source_index.json` / `source_index.csv` — machine-readable source list.
- `tables/*.csv` — quick matrices for version changes, conflicts, debug commands, and LLM projects.
- `templates/stellaris_mod_skeleton/` — Codex-friendly starter mod skeleton with descriptors, events, scripted trigger/effect files, localisation, install notes, and checklist.

## Source notation

Markdown reports cite sources with IDs such as `[S007]`. Resolve those IDs in `source_index.json` or `source_index.csv`.

## High-confidence bottom line

For public 4.4 releases, develop against **Stellaris 4.4.5 stable/current local install** and declare `supported_version="v4.4.*"` unless intentionally targeting 4.4.4 rollback or 4.5 beta. The main 4.4 modding hazard is Nomads/Arkships/Waylines/Contracts: scripts and modifiers that assume normal settled colonies or normal starbase/planet relationships need explicit tests. The next major porting hazard is 4.5's pop-ethics/faction refactor, which Paradox explicitly describes as a breaking, save-incompatible change.
