# Validation caveats and open questions

## What is high confidence

- Historical bundle anchor: 4.4.4 stable patch status and checksum 5505. `[S002]` Current work should use 4.4.5 unless explicitly targeting rollback.
- 4.4.5 open beta exists on `stellaris_test`. `[S003] [S004]`
- 4.5 pop/faction/ethics refactor is breaking and save-incompatible according to official notes. `[S004]`
- Local mod descriptor pair and Windows placement. `[S007]`
- `supported_version` is launcher-facing only. `[S007]`
- Mod folder mirrors install folder. `[S007]`
- Localisation UTF-8 BOM, filename, header, and no-fallback rules. `[S008]`
- Scope error behavior and need for `exists` checks. `[S009]`

## What requires target-environment validation

1. Exact command list on 4.4.x.
   - The console page used was verified for PC 4.2. Use in-game `help` on 4.4.x. `[S010]`

2. Full folder-by-folder override semantics.
   - Sources confirm FIOS/LIOS exists and Irony understands it, but this bundle does not contain a complete current Stellaris folder-rule table. Use Irony, current vanilla files, and CWTools full cache. `[S011] [S012] [S014]`

3. `replace_path` behavior in current Stellaris.
   - Clausewitz descriptor `replace_path` is known in Paradox modding but was not strongly verified from an accessible current official Stellaris page during this run. Treat as dangerous and validate before use.

4. Public LLM project quality.
   - GitHub READMEs establish claimed architecture, not runtime quality. Run code in a sandbox before relying on it. `[S015] [S016] [S017]`

5. macOS local mod path.
   - The path came from the Stellaris Mods wiki snippet, but the full page was blocked by a client challenge. Verify on the target machine if the launcher cannot see the mod. `[S019]`

## Open research questions for a follow-up pass with local game files

- Build a complete FIOS/LIOS folder rule table for 4.4.4 by inspecting Irony game definitions and vanilla loader behavior.
- Generate current `trigger_docs`, effects docs, modifiers docs, and scopes logs from a 4.4.4 installation.
- Diff current 4.4.5 vanilla files against any 4.4.4-derived assumptions for all folders touched by the target mod.
- Diff 4.4.4 vs 4.5 beta for pop/faction/ethics/job code.
- Run Galactic Conclave / Overmind / Companion in a disposable environment and record actual capabilities.
