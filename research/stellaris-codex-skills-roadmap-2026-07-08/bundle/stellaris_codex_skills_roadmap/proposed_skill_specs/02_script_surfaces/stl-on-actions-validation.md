---
skill_id: stl-on-actions-validation
category: 02_script_surfaces
topic: "on_actions validation"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-on-actions-validation

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Check duplicate IDs, nested event/random_event ambiguity, pulse frequency, merge winners, and runtime proof needs.

## Trigger

Existing on_action behavior is unclear, duplicates are present, or a mod stack changes on_actions.

## Do not use when

Writing a fresh event body before hook choice.

## Likely source references or evidence types

- CWTools diagnostics
- Irony merged output
- remaining_open_questions.csv
- error.log
- minimal runtime test mod

## Related skills commonly chained

- `stl-runtime-smoke-test`
- `stl-merge-semantics-research`
- `stl-pulse-performance`

## Priority

must-have

## Scope-control notes

Validation only; do not implement new gameplay here.
