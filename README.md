# Stellaris Mods

Starter workspace for Stellaris modding and mod preparation.

## Folder Map

| Path | Purpose |
| --- | --- |
| `mods/` | Source folders for individual Stellaris mods. |
| `research/` | Vanilla file notes, compatibility findings, game-version research, and modding references. |
| `assets/` | Source art, icons, image exports, generated visuals, and other reusable assets. |
| `tools/` | Local scripts or helpers used for validation, packaging, or analysis. |
| `notes/` | Early ideas, task notes, and rough planning that has not become mod-specific yet. |

## Starting A Mod

1. Create `mods/<ModName>/`.
2. Add a short `README.md` describing the idea, target Stellaris version, expected DLC assumptions, and known compatibility risks.
3. Add only the Stellaris folders the mod needs, such as `common/`, `events/`, `gfx/`, `interface/`, or `localisation/`.
4. Keep research evidence in `research/` or `mods/<ModName>/notes/`.
5. Validate paths, syntax, and in-game behavior before calling the mod ready.

## Current Status

No specific Stellaris mod has been created yet. This project is ready for mod prep, research, and the first mod folder.

