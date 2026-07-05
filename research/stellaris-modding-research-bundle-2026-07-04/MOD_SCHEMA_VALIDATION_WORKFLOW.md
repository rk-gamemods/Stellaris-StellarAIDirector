# Mod schema and validation workflow

## Objective

Prevent Codex or human contributors from shipping PDXScript that looks plausible but is not recognized by Stellaris.

## Required validation sources

1. Current vanilla game files for the exact target version.
2. CWTools VS Code diagnostics. `[S007] [S013]`
3. CWTools CLI/cwtools-action if using CI. `[S014]`
4. In-game generated `trigger_docs`/script documentation where available. `[S009]`
5. Runtime `error.log`. `[S007]`
6. Irony conflict solver for load-order/override analysis. `[S011] [S012]`

## Pre-generation phase

Before writing code, collect:

```text
TARGET_VERSION=4.4.4
MOD_PREFIX=my_mod
TOUCHED_FOLDERS=common/pop_jobs,events,localisation
VANILLA_REFERENCES=<copy of relevant vanilla files>
REQUIRED_COMPAT_MODS=<list>
```

## Generation phase

Codex should produce:

- Minimal files.
- Unique object keys.
- Localisation keys.
- Comments documenting any vanilla override.
- Debug logs behind a flag or temporary notes.
- Test plan.

## Static validation phase

- Open mod root in VS Code.
- Select vanilla folder for CWTools.
- Wait for scan and fix diagnostics.
- Search for raw unprefixed keys.
- Search for copied vanilla filenames.
- Check localisation encoding.

## Conflict validation phase

- Load playset in Irony.
- Inspect conflicts involving touched folders.
- Export/record conflicts.
- Build patch mod if needed.
- Re-run with patch lower than source mods unless Irony indicates FIOS behavior.

## Runtime validation phase

Launch flags:

```text
-script_debug -debug_mode -debugtooltip -logall
```

Runtime steps:

1. New game, only mod.
2. New game, target playset.
3. Save/load cycle.
4. Trigger each event manually if possible.
5. Check `error.log` and `game.log` after each run.
6. Profile recurring scripts with `script_profiler` if performance changes.

## Release gate

Do not release if:

- New `error.log` lines are unexplained.
- A copied UI file differs from current vanilla without manual review.
- 4.5 pop/faction/ethics code was changed but no 4.5 test was run.
- Irony reports unresolved conflicts in core folders touched by the mod.
- Localisation keys appear raw in-game.
