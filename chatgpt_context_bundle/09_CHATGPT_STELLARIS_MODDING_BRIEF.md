> Snapshot commit: `27aa7547b610e2876d897771a804656453f948ee` | Branch: `master` | Working tree: `dirty` | Generated: `2026-07-08T15:18:04-04:00`

# ChatGPT Stellaris Modding Brief

Use this source bundle as a point-in-time context pack for the StellarisMods project. The project covers Stellaris modding, mod preparation, compatibility research, generated validation evidence, and source mods under `mods/`, with special emphasis on Stellar AI Director and compatibility with major mods such as Gigastructural Engineering, NSC3, Extra Ship Components NEXT, Starbase Extended, Planetary Diversity, UI dependencies, and AI/performance-related mods.

## Operating Rules For Online ChatGPT

1. Treat the uploaded bundle as context, not live truth. Ask for a refresh when current game version, Workshop state, active playset, runtime logs, or generated evidence matters.
2. Default to Stellaris PC 4.4.5 stable/current local install unless the user names another target.
3. Follow `AGENTS.md` and the modding guide source order: current user instruction, repo guidance, local vanilla files, current mod source, source-bundle evidence, Irony, CWTools, runtime logs, then inference.
4. Do not invent Stellaris triggers, effects, modifiers, scopes, folder names, or loader behavior. Ask Codex to verify unfamiliar surfaces against vanilla files, generated docs, CWTools, Irony, or runtime logs.
5. Treat raw mod-source snapshots, large CSVs, and observer-run artifacts as local evidence surfaces. In Codex, use JDocMunch for prose, JCodeMunch for scripts/source, and JDataMunch for row/column datasets.
6. Keep live launcher state separate from source files. A source mod being updated does not mean the mod that Stellaris will load on next launch is updated.
7. Runtime/game launches and observer simulations require explicit user approval. Default validation is static: file shape, parser/load safety, generated references, descriptors, and evidence reports.
8. For recommendations, respect user preferences: do not recommend Real Space or Star Wars total conversions by default; prioritize maintained compatibility with Gigastructures, NSC3, ship/component expansions, AI mods, station/defense mods, and empire-creation options.
9. For Stellar AI Director, distinguish design intent, generated PDXScript, validation reports, active playset conflicts, and observer outcomes. Do not treat one surface as proof for another without explicit evidence.

## Best Starting Files

1. `02_PROJECT_CONTROL_AND_GUIDANCE.md` for repo rules, final-status reporting, source order, and user preferences.
2. `03_MOD_SOURCE_AND_DESCRIPTORS.md` for current source mod files under `mods/`.
3. `04_STELLAR_AI_DIRECTOR_CONTEXT.md` for the active AI/economy/compatibility mod lane.
4. `05_RESEARCH_AND_EVIDENCE_GUIDES.md` for synthesized guides and external research packets.
5. `06_DATASETS_AND_VALIDATION_REPORTS.md` for dataset catalog and narrative audit/validation reports.
6. `08_SOURCE_FILE_MANIFEST_AND_UPLOAD_REVIEW.md` for coverage, omissions, and the full candidate manifest.
