---
skill_id: stl-zones-zone-slots
category: 03_ai_economy_planets
topic: "Zones and zone slots"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-zones-zone-slots

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Implement or validate 4.x zones, zone sets, slot unlocks, building-set includes/excludes, conversion, AI priority, and UI visibility dependencies.

## Trigger

common/zones, common/zone_slots, planet view, or 4.x building-slot behavior is touched.

## Do not use when

Pre-4.x district-only logic or pure building stat edits.

## Likely source references or evidence types

- CWTools zones CWT
- cwtools_schema_surface_matrix.csv
- vanilla zone files
- PD/UIOD patches
- runtime UI checks

## Related skills commonly chained

- `stl-districts-buildings`
- `stl-interface-gui`
- `stl-compat-planetary-diversity`

## Priority

must-have

## Scope-control notes

Zones/slots only; do not cover all buildings or planet economy.
