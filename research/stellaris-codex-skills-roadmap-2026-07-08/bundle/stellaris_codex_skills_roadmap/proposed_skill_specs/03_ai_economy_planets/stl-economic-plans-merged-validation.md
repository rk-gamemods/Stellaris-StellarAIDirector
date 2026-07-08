---
skill_id: stl-economic-plans-merged-validation
category: 03_ai_economy_planets
topic: "Merged economic-plan validation"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-economic-plans-merged-validation

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Reconstruct active economic plans/subplans and identify final winners, duplicate subplan overwrites, and load-order-dependent behavior.

## Trigger

A heavy playset or AI overhaul makes plan behavior unclear.

## Do not use when

Single clean local mod with no external plan overrides.

## Likely source references or evidence types

- Irony merged output
- launcher order
- economic_plan docs
- active playset
- runtime AI logs

## Related skills commonly chained

- `stl-irony-conflict-map`
- `stl-active-playset-inventory`
- `stl-merge-semantics-research`

## Priority

must-have

## Scope-control notes

Report winners and conflicts only; do not retune values.
