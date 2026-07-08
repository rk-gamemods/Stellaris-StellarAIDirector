---
skill_id: stl-vanilla-overrides-audit
category: 01_schema_and_research
topic: "Vanilla override audit"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-vanilla-overrides-audit

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

List full-file and object-level vanilla overrides in a mod and rank porting/compatibility risk.

## Trigger

A mod copies vanilla files or fails after a patch, or release notes mention touched surfaces.

## Do not use when

The mod is purely additive with namespaced IDs.

## Likely source references or evidence types

- repo tree
- vanilla diff
- Irony conflicts
- source inventory
- porting notes

## Related skills commonly chained

- `stl-vanilla-docs-diff`
- `stl-porting-version-bump`
- `stl-compat-patch-authoring`

## Priority

must-have

## Scope-control notes

Audit only; do not implement fixes.
