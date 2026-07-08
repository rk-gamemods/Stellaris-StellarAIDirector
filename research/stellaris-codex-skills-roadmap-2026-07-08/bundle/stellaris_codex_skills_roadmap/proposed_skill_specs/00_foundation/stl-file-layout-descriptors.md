---
skill_id: stl-file-layout-descriptors
category: 00_foundation
topic: "Mod folder and descriptors"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-file-layout-descriptors

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Verify mod folder layout, outer .mod, inner descriptor.mod, path, supported_version, tags, thumbnail, and package-sensitive metadata.

## Trigger

The mod does not appear in the launcher, is being packaged, moved, published, or version-bumped.

## Do not use when

Gameplay script, AI logic, UI layout, or balance is the main task.

## Likely source references or evidence types

- Stellaris modding tutorial
- local descriptors
- launcher mod files
- Workshop metadata
- repo packaging scripts

## Related skills commonly chained

- `stl-packaging-descriptor-release`
- `stl-steam-workshop-update`
- `stl-version-vanilla-baseline`

## Priority

must-have

## Scope-control notes

Stay limited to file placement and metadata; do not inspect game object definitions unless descriptor paths are wrong.
