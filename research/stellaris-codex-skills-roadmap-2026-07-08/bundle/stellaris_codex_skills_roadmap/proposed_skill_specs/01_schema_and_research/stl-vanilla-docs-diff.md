---
skill_id: stl-vanilla-docs-diff
category: 01_schema_and_research
topic: "Vanilla file diff"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-vanilla-docs-diff

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Compare a modded or copied object against the target vanilla version to detect stale keys, deleted blocks, new requirements, and full-file override risk.

## Trigger

Porting, overriding vanilla objects, or troubleshooting after a Stellaris patch.

## Do not use when

The mod only adds unique new IDs and no vanilla object is copied or replaced.

## Likely source references or evidence types

- local vanilla files
- verified depot snapshots
- patch notes
- directory diff output
- source inventory

## Related skills commonly chained

- `stl-version-vanilla-baseline`
- `stl-vanilla-overrides-audit`
- `stl-porting-version-bump`

## Priority

must-have

## Scope-control notes

One folder or object family at a time; do not become a general patch-note review.
