---
skill_id: stl-compat-planetary-diversity
category: 09_compatibility
topic: "Planetary Diversity compatibility"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-compat-planetary-diversity

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Check planet classes, startup events, zones, zone slots, districts, colony types, deposits, and UIOD/planet-view patch interactions.

## Trigger

PD is active or planet/zones/UI/planet class files are touched.

## Do not use when

No PD or planet-class changes.

## Likely source references or evidence types

- PD files/pages
- UIOD patches
- Irony diff
- runtime planet-view tests

## Related skills commonly chained

- `stl-zones-zone-slots`
- `stl-interface-gui`
- `stl-ui-smoke-checklist`

## Priority

must-have

## Scope-control notes

PD compatibility only; do not design new planet classes broadly.
