---
skill_id: stl-ai-catchup-construction-events
category: 03_ai_economy_planets
topic: "AI catch-up construction events"
priority: should-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-ai-catchup-construction-events

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Plan AI-only emergency catch-up events for severe unemployment/housing/job deficits when normal planning is too slow, with save-safety and semantic tests.

## Trigger

Late-game AI colonies have large unemployment/stockpiles and vanilla plan/budget tuning cannot clear the backlog.

## Do not use when

Normal economic plans/budgets/zone metadata have not been tried or the goal is vanilla-pure AI behavior.

## Likely source references or evidence types

- AI construction throttle packet
- open_questions.md
- generated effect docs
- runtime copied-save tests
- error.log

## Related skills commonly chained

- `stl-scripted-effects`
- `stl-events-implementation`
- `stl-savegame-safety`
- `stl-runtime-smoke-test`

## Priority

should-have

## Scope-control notes

Emergency intervention only; do not replace normal AI economy or assume add_building semantics without tests.
