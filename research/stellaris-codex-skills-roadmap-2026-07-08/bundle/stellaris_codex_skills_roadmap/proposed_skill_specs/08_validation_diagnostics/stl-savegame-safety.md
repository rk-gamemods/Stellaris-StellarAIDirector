---
skill_id: stl-savegame-safety
category: 08_validation_diagnostics
topic: "Savegame safety"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-savegame-safety

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Assess whether a change is save-safe, new-game-only, copied-save-only, or requires migration/cleanup.

## Trigger

Events, buildings, megastructures, ship classes, defines, or patches affect existing saves.

## Do not use when

Pure documentation or typo fix.

## Likely source references or evidence types

- patch notes
- mod pages
- existing saves
- runtime tests
- logs

## Related skills commonly chained

- `stl-runtime-smoke-test`
- `stl-packaging-descriptor-release`
- `stl-porting-version-bump`

## Priority

must-have

## Scope-control notes

Risk classification only; no implementation.
