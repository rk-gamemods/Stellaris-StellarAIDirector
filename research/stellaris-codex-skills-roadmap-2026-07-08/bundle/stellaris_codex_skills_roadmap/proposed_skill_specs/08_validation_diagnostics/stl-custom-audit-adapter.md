---
skill_id: stl-custom-audit-adapter
category: 08_validation_diagnostics
topic: "Custom audit adapter"
priority: should-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-custom-audit-adapter

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Design small local Python/Codex helper scripts to emit mods.json, overwritten_paths, object inventories, load_order, and validation inputs.

## Trigger

Existing tools leave gaps in playset, freshness, conflict, or ID inventory workflows.

## Do not use when

A one-off manual check is sufficient.

## Likely source references or evidence types

- modding_tools_matrix.csv
- launcher files
- descriptors
- Steam Workshop folders
- Irony output
- CWTools output

## Related skills commonly chained

- `stl-active-playset-inventory`
- `stl-object-id-inventory`
- `stl-regression-reporting`

## Priority

should-have

## Scope-control notes

Tool adapter only; do not bake gameplay rules into scripts.
