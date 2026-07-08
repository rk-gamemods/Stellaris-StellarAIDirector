---
skill_id: stl-object-id-inventory
category: 01_schema_and_research
topic: "Object ID inventory"
priority: should-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-object-id-inventory

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Build a narrow inventory of IDs for one object family across vanilla and enabled mods.

## Trigger

The agent must ensure IDs exist, avoid collisions, or validate references.

## Do not use when

The user gives exact IDs and only asks for formatting.

## Likely source references or evidence types

- vanilla files
- enabled mod folders
- Irony merged output
- grep/ripgrep output
- generated inventories

## Related skills commonly chained

- `stl-vanilla-overrides-audit`
- `stl-compat-patch-authoring`

## Priority

should-have

## Scope-control notes

Inventory only; do not resolve conflicts or change files.
