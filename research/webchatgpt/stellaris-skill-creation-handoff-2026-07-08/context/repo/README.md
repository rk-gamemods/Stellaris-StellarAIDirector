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
