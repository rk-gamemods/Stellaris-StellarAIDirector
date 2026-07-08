---
skill_id: stl-pulse-performance
category: 02_script_surfaces
topic: "Pulse performance"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-pulse-performance

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Prevent daily/monthly/yearly pulses and galaxy-wide loops from over-scanning or over-firing.

## Trigger

Any frequent on_action, pulse event, every_country/planet loop, or observer-run performance problem.

## Do not use when

Static data definitions with no runtime loops.

## Likely source references or evidence types

- vanilla pulse patterns
- performance telemetry
- observer logs
- script instrumentation

## Related skills commonly chained

- `stl-on-actions-implementation`
- `stl-performance-telemetry`
- `stl-observer-run-planning`

## Priority

must-have

## Scope-control notes

Performance guards/caps only; no balance tuning.
