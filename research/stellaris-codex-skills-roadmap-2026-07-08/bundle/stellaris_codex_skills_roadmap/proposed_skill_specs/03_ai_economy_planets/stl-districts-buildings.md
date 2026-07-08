---
skill_id: stl-districts-buildings
category: 03_ai_economy_planets
topic: "Districts and buildings"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-districts-buildings

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Add or repair districts/buildings, resources, potential/allow, upgrades, on_queued/on_built hooks, AI weights, and zone metadata.

## Trigger

District/building definitions, upgrades, build restrictions, or job-producing structures are edited.

## Do not use when

Only jobs, resource categories, or UI layout change.

## Likely source references or evidence types

- vanilla districts/buildings
- CWTools districts/buildings CWT
- Building modding docs
- Irony merged output
- error.log

## Related skills commonly chained

- `stl-jobs-pop-economy`
- `stl-zones-zone-slots`
- `stl-resources-modifiers`

## Priority

must-have

## Scope-control notes

One object family per task; avoid economic-plan tuning here.
