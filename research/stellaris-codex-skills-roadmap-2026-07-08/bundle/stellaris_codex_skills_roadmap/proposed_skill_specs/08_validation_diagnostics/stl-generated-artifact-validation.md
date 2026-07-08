---
skill_id: stl-generated-artifact-validation
category: 08_validation_diagnostics
topic: "Generator artifact validation"
priority: should-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-generated-artifact-validation

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Validate deterministic generator outputs, expected files, diff cleanliness, static checks, and known manual-runtime questions.

## Trigger

Codex modifies generators or generated Stellaris mod artifacts.

## Do not use when

Hand-edited small file with no generator.

## Likely source references or evidence types

- git diff
- generator logs
- unit tests
- static validator
- implementation-plan acceptance criteria

## Related skills commonly chained

- `stl-regression-reporting`
- `stl-cwtools-diagnostics`
- `stl-vanilla-overrides-audit`

## Priority

should-have

## Scope-control notes

Generated artifact checks only; no gameplay design.
