---
skill_id: stl-active-playset-inventory
category: 08_validation_diagnostics
topic: "Active playset inventory"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-active-playset-inventory

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Read/produce enabled mods, Workshop IDs, descriptors, paths, versions, and load order for the active playset.

## Trigger

Any compatibility, load-order, mod-stack, or active-save task begins.

## Do not use when

A single local mod is tested in a clean environment.

## Likely source references or evidence types

- launcher playset files
- descriptors
- Steam Workshop folders
- Irony profile/export
- mods.json

## Related skills commonly chained

- `stl-irony-conflict-map`
- `stl-load-order-rules`
- `stl-source-inventory-maintenance`

## Priority

must-have

## Scope-control notes

Inventory only; do not solve conflicts.
