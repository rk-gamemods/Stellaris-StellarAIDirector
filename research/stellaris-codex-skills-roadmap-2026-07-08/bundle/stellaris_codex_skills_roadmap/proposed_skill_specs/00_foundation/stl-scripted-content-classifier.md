---
skill_id: stl-scripted-content-classifier
category: 00_foundation
topic: "Task-to-surface classifier"
priority: should-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-scripted-content-classifier

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Map a requested change to the smallest relevant Stellaris file surface and likely validation chain.

## Trigger

The user asks broadly to add/fix/change a feature and the agent must decide which skill or file family applies.

## Do not use when

The file path and surface are already explicit.

## Likely source references or evidence types

- repo tree
- vanilla folder map
- prior roadmap catalog
- CWTools path types
- source inventory

## Related skills commonly chained

- `stl-project-orientation`
- `stl-source-triage`
- `stl-cwtools-schema-lookup`

## Priority

should-have

## Scope-control notes

Classification only; do not inspect every possible folder.
