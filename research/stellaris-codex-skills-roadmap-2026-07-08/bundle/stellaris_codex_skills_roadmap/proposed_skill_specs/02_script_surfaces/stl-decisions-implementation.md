---
skill_id: stl-decisions-implementation
category: 02_script_surfaces
topic: "Planet/empire decisions"
priority: should-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-decisions-implementation

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Implement and validate decisions with cost, allow/potential, effects, AI weights, cooldowns, localization, and save-safety notes.

## Trigger

A task adds planet or country decisions, edict-like buttons, or manual player/AI actions.

## Do not use when

The task is a policy/edict or event-only feature.

## Likely source references or evidence types

- vanilla decisions
- CWTools schema
- localization
- generated docs
- error.log

## Related skills commonly chained

- `stl-events-implementation`
- `stl-localization`
- `stl-savegame-safety`

## Priority

should-have

## Scope-control notes

Decisions only; do not include policies, edicts, or situations.
