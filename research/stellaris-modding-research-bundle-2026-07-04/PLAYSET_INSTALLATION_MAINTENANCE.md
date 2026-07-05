# Playset, installation, and maintenance guide

## Local development installation

1. Put `<mod>.mod` in the user mod directory.
2. Put the mod root folder beside it.
3. Ensure the outer `.mod` file points to the root folder.
4. Enable in Paradox Launcher or Irony.
5. Do not subscribe to the same mod's Workshop version while developing the local copy. `[S007]`

## Workshop/user installation notes

- Users normally subscribe through Steam Workshop or Paradox Mods, then enable the mod in a launcher playset.
- The launcher creates/imports descriptors and local paths.
- If mods do not appear, rebuild launcher state by removing stale launcher/cache descriptors only after backing up playsets.

## Recommended user load order explanation

Tell users:

```text
Load the base mod above any submods.
Load compatibility patches below all mods they patch.
Load UI patches after UI mods.
Use Irony Mod Manager if running a large playset.
```

Do not promise universal load-order behavior because FIOS/LIOS rules can make some earlier definitions win. `[S011] [S012]`

## Version support statement template

```text
Supported Stellaris version: 4.4.* stable.
Tested on: 4.4.4 checksum 5505.
Not tested on: 4.4.5 beta unless noted.
4.5 status: not supported until the pop/faction/ethics refactor is ported.
Save compatibility: new save recommended after major mod updates.
```

## Maintenance cadence

After every Stellaris update:

1. Read patch notes.
2. Search for `Modding` section.
3. Diff vanilla folders touched by the mod.
4. Run CWTools.
5. Run clean new-game test.
6. Run target playset with Irony.
7. Update README support line.

## User bug report template

```text
Game version/checksum:
DLC list:
Mod version:
Full playset order:
Is this a new game or old save?
Reproduction steps:
Expected result:
Actual result:
error.log attached:
game.log attached:
Screenshots/video:
```
