---
skill_id: stl-scripted-effects
category: 02_script_surfaces
topic: "Scripted effects"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-scripted-effects

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Create or review reusable effects with safe scope guards, clear side effects, cleanup, and namespaced IDs.

## Trigger

Repeated effect logic, setup/cleanup actions, catch-up scripts, or compatibility repairs are needed.

## Do not use when

The task only needs a boolean condition or numeric formula.

## Likely source references or evidence types

- vanilla scripted_effects
- generated effect docs
- CWTools schema
- runtime logs

## Related skills commonly chained

- `stl-events-implementation`
- `stl-savegame-safety`
- `stl-flags-variables-state`

## Priority

must-have

## Scope-control notes

Require explicit scope and side-effect boundary; do not design whole event chains.
