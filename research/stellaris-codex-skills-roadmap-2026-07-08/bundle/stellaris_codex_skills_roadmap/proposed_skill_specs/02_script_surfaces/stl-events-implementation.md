---
skill_id: stl-events-implementation
category: 02_script_surfaces
topic: "Events implementation"
priority: must-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-events-implementation

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Author country/planet/fleet/ship events with namespaces, triggers, immediate blocks, options, and localization hooks.

## Trigger

A feature needs an event chain, UI option, notification, cleanup, or scripted workflow.

## Do not use when

Only registering events in on_actions or only writing localization text.

## Likely source references or evidence types

- vanilla events
- scopes docs
- generated effect docs
- event namespace examples

## Related skills commonly chained

- `stl-events-validation`
- `stl-localization`
- `stl-scripted-effects`

## Priority

must-have

## Scope-control notes

One event namespace/workflow per use; delegate on_actions and validation.
