---
skill_id: stl-situations-scripted-actions
category: 02_script_surfaces
topic: "Situations and scripted actions"
priority: should-have
status: roadmap_spec_only
not_a_skill_file: true
---

# stl-situations-scripted-actions

> Roadmap card only. This is not a finished Codex skill and is not a `SKILL.md` body.

## Purpose

Implement or validate situations, situation stages/approaches, scripted actions, automation blocks, and version-gated 4.4/4.5 syntax.

## Trigger

A task touches situations, Situation Log UI, automation buttons, or scripted action menus.

## Do not use when

A simple event or edict can solve the problem without situation machinery.

## Likely source references or evidence types

- vanilla situations
- scripted_actions
- 4.4/4.5 patch notes
- CWTools
- UI logs

## Related skills commonly chained

- `stl-version-vanilla-baseline`
- `stl-interface-gui`
- `stl-runtime-smoke-test`

## Priority

should-have

## Scope-control notes

Keep situations/actions together only where they share UI automation; split if it grows.
