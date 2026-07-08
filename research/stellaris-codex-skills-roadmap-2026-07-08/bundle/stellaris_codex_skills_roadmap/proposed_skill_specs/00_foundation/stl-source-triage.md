---
skill_id: stl-source-triage
category: 00_foundation
topic: "Evidence hierarchy"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-source-triage

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Choose which evidence types should decide the task: vanilla files, CWTools, generated docs, Irony, logs, runtime tests, mod pages, or old examples.

## Trigger

Sources conflict, syntax is uncertain, a mod page disagrees with local files, or the task asks for research-backed work.

## Do not use when

The user explicitly names the authoritative source and no ambiguity remains.

## Likely source references or evidence types

- source_inventory.csv
- source_index.json
- modding_tools_matrix.csv
- vanilla files
- CWTools schema
- runtime logs
- Irony merged output

## Related skills commonly chained

- `stl-cwtools-schema-lookup`
- `stl-error-log-review`
- `stl-irony-conflict-map`

## Priority

must-have

## Scope-control notes

Produce a source plan only; do not implement or decide balance.
