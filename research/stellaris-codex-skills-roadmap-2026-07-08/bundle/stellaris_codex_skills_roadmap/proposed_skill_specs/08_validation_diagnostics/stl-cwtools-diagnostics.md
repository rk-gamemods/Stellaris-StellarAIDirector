---
skill_id: stl-cwtools-diagnostics
category: 08_validation_diagnostics
topic: "CWTools diagnostics"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-cwtools-diagnostics

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Run/read CWTools diagnostics and map warnings/errors to files, object families, and likely follow-up skills.

## Trigger

Static validation is requested or code generation has produced Stellaris script.

## Do not use when

Runtime-only bug with clean static diagnostics.

## Likely source references or evidence types

- CWTools VS Code output
- cwtools-action output.json
- Problems list
- logs

## Related skills commonly chained

- `stl-cwtools-schema-lookup`
- `stl-error-log-review`
- `stl-regression-reporting`

## Priority

must-have

## Scope-control notes

Diagnostics triage only; no broad refactor.
