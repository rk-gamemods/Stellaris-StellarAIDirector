---
skill_id: stl-scripted-triggers
category: 02_script_surfaces
topic: "Scripted triggers"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-scripted-triggers

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Create or review reusable boolean conditions with explicit scopes, safe exists checks, and namespaced IDs.

## Trigger

Conditions repeat across files, compatibility gates are needed, or trigger logic needs reuse.

## Do not use when

A one-off inline condition is clearer or numeric output is required.

## Likely source references or evidence types

- vanilla scripted_triggers
- generated trigger docs
- CWTools schema
- error.log

## Related skills commonly chained

- `stl-scope-script-basics`
- `stl-naming-namespace-hygiene`
- `stl-compat-patch-authoring`

## Priority

must-have

## Scope-control notes

Boolean conditions only; do not cover scripted effects or scripted values except references.
