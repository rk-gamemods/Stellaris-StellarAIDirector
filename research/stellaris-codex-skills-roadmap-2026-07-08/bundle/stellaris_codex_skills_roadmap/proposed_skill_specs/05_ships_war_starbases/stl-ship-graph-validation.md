---
skill_id: stl-ship-graph-validation
category: 05_ships_war_starbases
topic: "Ship graph validation"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-ship-graph-validation

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Run a static graph validation of ship sizes, sections, component slots, component sets, behaviors, global designs, and required components.

## Trigger

Multiple ship/component mods are active or a ship designer/save failure is suspected.

## Do not use when

A single vanilla component stat is changed.

## Likely source references or evidence types

- Irony merged files
- CWTools
- custom graph checker
- ship designer smoke tests
- error.log

## Related skills commonly chained

- `stl-compat-ship-stack`
- `stl-runtime-smoke-test`
- `stl-global-ship-designs`

## Priority

must-have

## Scope-control notes

Validation graph only; do not retune ship balance.
