---
skill_id: stl-fleet-manager-reinforcement
category: 05_ships_war_starbases
topic: "Fleet manager and reinforcement"
priority: later
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-fleet-manager-reinforcement

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Assess fleet manager templates, reinforcement behavior, transport/fleet creation, and AI replenishment issues.

## Trigger

Fleets fail to reinforce, templates are invalid, or AI cannot maintain intended ship classes.

## Do not use when

Ship designer definitions are invalid before fleet manager is reached.

## Likely source references or evidence types

- vanilla fleet manager behavior
- global ship designs
- runtime logs
- observer telemetry

## Related skills commonly chained

- `stl-global-ship-designs`
- `stl-fleet-doctrine-ai`

## Priority

later

## Scope-control notes

Reinforcement behavior only; no component graph validation unless chained.
