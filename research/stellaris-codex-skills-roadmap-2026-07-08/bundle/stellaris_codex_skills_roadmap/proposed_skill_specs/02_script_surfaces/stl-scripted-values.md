---
skill_id: stl-scripted-values
category: 02_script_surfaces
topic: "Scripted values"
priority: should-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-scripted-values

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Design reusable numeric formulas, constants, and AI weights without embedding large logic in other objects.

## Trigger

Costs, scores, scaling factors, AI weights, or thresholds repeat.

## Do not use when

Static literals are clearer or boolean logic is needed.

## Likely source references or evidence types

- vanilla scripted_values
- CWTools schema
- economic plan examples
- AI weight files

## Related skills commonly chained

- `stl-tech-ai-weights`
- `stl-economic-plans-implementation`
- `stl-resources-modifiers`

## Priority

should-have

## Scope-control notes

Numeric expressions only; no event bodies or triggers beyond formula guards.
