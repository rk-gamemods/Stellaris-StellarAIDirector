---
skill_id: stl-compat-patch-authoring
category: 10_packaging_release
topic: "Compatibility patch authoring"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-compat-patch-authoring

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Create minimal patch-mod plans that override only necessary objects and document load-order assumptions.

## Trigger

Two or more mods conflict and a patch is required.

## Do not use when

Simple load-order change solves the issue or conflict winner is unknown.

## Likely source references or evidence types

- Irony conflict map
- mod maintainer instructions
- vanilla/mod files
- descriptors

## Related skills commonly chained

- `stl-irony-conflict-map`
- `stl-load-order-rules`
- `relevant compatibility skill`

## Priority

must-have

## Scope-control notes

Patch only the conflict; avoid bundled broad fixes.
