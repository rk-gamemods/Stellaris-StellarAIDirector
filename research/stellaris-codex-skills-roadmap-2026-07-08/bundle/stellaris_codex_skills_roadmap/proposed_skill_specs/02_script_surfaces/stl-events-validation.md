---
skill_id: stl-events-validation
category: 02_script_surfaces
topic: "Events validation"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-events-validation

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Validate event IDs, namespaces, is_triggered_only, scope transitions, options, localization, and runtime errors.

## Trigger

Reviewing generated or patched events, logs mention events, or an event fires incorrectly.

## Do not use when

The task is pure event concept design without files.

## Likely source references or evidence types

- CWTools diagnostics
- error.log
- script.log
- game.log
- console-fired test event

## Related skills commonly chained

- `stl-cwtools-diagnostics`
- `stl-error-log-review`
- `stl-runtime-smoke-test`

## Priority

must-have

## Scope-control notes

Do not redesign event content unless validation identifies the failure.
