---
skill_id: stl-cwtools-limitations
category: 01_schema_and_research
topic: "CWTools limitation handling"
priority: should-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-cwtools-limitations

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Identify when CWTools can validate shape but cannot prove load-order winners, nested merge behavior, runtime scope semantics, or active-stack behavior.

## Trigger

CWTools passes but the bug persists, or a public schema is intentionally incomplete.

## Do not use when

A schema error already explains the issue.

## Likely source references or evidence types

- CWTools action output
- cwtools_schema_surface_matrix.csv
- remaining_open_questions.csv
- runtime logs
- Irony output

## Related skills commonly chained

- `stl-runtime-smoke-test`
- `stl-merge-semantics-research`
- `stl-irony-conflict-map`

## Priority

should-have

## Scope-control notes

Only decide what CWTools cannot answer; do not design the runtime test unless chained.
