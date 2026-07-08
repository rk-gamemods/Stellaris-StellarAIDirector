---
skill_id: stl-merge-semantics-research
category: 01_schema_and_research
topic: "Merge/overwrite semantics"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-merge-semantics-research

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Investigate whether a specific surface merges, appends, replaces, de-duplicates, or has duplicate-ID ambiguity.

## Trigger

Duplicate object IDs, nested blocks, on_actions, economic subplans, localization replace behavior, or load-order surprises are suspected.

## Do not use when

A simple unique additive file is being created.

## Likely source references or evidence types

- vanilla docs
- CWTools schema
- Irony merged view
- remaining_open_questions.csv
- minimal runtime tests

## Related skills commonly chained

- `stl-irony-conflict-map`
- `stl-runtime-smoke-test`
- `stl-on-actions-validation`

## Priority

must-have

## Scope-control notes

One object type and one merge question per task.
