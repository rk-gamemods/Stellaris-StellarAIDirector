---
skill_id: stl-error-log-review
category: 08_validation_diagnostics
topic: "Runtime log review"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-error-log-review

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Read error.log, game.log, script.log, localization logs, and crash folders to map runtime errors to script surfaces.

## Trigger

Game launches but content fails, missing loc appears, events do not fire, UI errors occur, or parser errors appear.

## Do not use when

Static pre-launch validation only.

## Likely source references or evidence types

- Stellaris logs
- crash folders
- CWTools output
- runtime test notes

## Related skills commonly chained

- `stl-events-validation`
- `stl-localization`
- `stl-runtime-smoke-test`

## Priority

must-have

## Scope-control notes

Log-to-cause mapping only; avoid redesign unless chained.
