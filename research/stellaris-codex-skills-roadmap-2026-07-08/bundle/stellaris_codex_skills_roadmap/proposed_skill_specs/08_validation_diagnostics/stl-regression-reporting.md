---
skill_id: stl-regression-reporting
category: 08_validation_diagnostics
topic: "Regression reporting"
priority: should-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-regression-reporting

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Produce a compact before/after report listing files touched, diagnostics run, runtime results, unresolved questions, and next test.

## Trigger

Finishing a coding pass, patch, port, or compatibility investigation.

## Do not use when

User only asks for a code snippet or a quick answer.

## Likely source references or evidence types

- test notes
- CWTools output
- logs
- Irony conflicts
- git diff

## Related skills commonly chained

- `stl-cwtools-diagnostics`
- `stl-error-log-review`
- `stl-runtime-smoke-test`

## Priority

should-have

## Scope-control notes

Report only; do not perform new investigation.
