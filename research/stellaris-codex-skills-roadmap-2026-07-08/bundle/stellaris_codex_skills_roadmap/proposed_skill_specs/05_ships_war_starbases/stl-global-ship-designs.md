---
skill_id: stl-global-ship-designs
category: 05_ships_war_starbases
topic: "Global ship designs"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-global-ship-designs

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Check AI/default/global designs against sections, slots, required components, tech availability, and save/design validity.

## Trigger

AI ship designs fail, designs have empty slots, or modded ship classes need defaults.

## Do not use when

Player-only cosmetic shipset changes.

## Likely source references or evidence types

- common/global_ship_designs
- NSC/ESC/SFT files
- ship designer tests
- SAVEFAIL logs

## Related skills commonly chained

- `stl-components-slots-sets`
- `stl-ship-behaviors-computers`
- `stl-ship-graph-validation`

## Priority

must-have

## Scope-control notes

Validation-heavy; implement only direct global design fixes.
