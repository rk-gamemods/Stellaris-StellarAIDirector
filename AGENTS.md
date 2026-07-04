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

## Stellaris Modding Defaults

- Prefer small, focused mods with clear compatibility boundaries.
- Document which vanilla files, scripted effects, defines, events, assets, or localization keys a mod touches.
- Use stable namespaces and prefixes for custom content to avoid collisions with other mods.
- Keep localization keys explicit and grouped by mod.
- Treat overwrite-style changes as high-risk. Prefer additive files and scoped patches when Stellaris supports them.
- Record game version and DLC assumptions before implementing or testing a mod.
- Before editing an existing mod, identify whether the work affects gameplay scripts, UI, localization, graphics, dependencies, or packaging.

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

