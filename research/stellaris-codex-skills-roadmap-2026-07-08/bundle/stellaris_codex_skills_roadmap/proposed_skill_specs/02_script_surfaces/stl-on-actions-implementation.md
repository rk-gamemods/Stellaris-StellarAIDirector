---
skill_id: stl-on-actions-implementation
category: 02_script_surfaces
topic: "on_actions implementation"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-on-actions-implementation

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Attach events/effects to game hooks and pulses with minimal frequency, correct scope assumptions, and safe registration.

## Trigger

Startup, monthly/yearly hooks, pulse events, or hook-based compatibility logic is needed.

## Do not use when

The event is manual/debug-only and does not need automatic triggering.

## Likely source references or evidence types

- vanilla on_actions
- CWTools on_actions CWT
- generated docs
- existing validation notes

## Related skills commonly chained

- `stl-events-implementation`
- `stl-pulse-performance`
- `stl-on-actions-validation`

## Priority

must-have

## Scope-control notes

Hook selection and structure only; event body design is separate.
