# First build order

Generated: 2026-07-08

Build these first because they create the minimum safe path from task routing → evidence selection → implementation → static/runtime validation.

1. **`stl-project-orientation`** — Every task needs a cheap entrypoint that identifies repo, target version, deliverable, and whether work is implementation, validation, or planning.
2. **`stl-active-playset-inventory`** — Compatibility work is impossible without enabled mods, descriptors, Workshop IDs, paths, and load order.
3. **`stl-irony-conflict-map`** — The active stack is large enough that merged winners matter more than intent in source files.
4. **`stl-cwtools-schema-lookup`** — Agents need fast schema lookup without loading a giant Stellaris reference.
5. **`stl-cwtools-diagnostics`** — Static diagnostics should be reusable after any implementation skill.
6. **`stl-error-log-review`** — Runtime logs catch wrong scopes, missing loc, parser errors, and UI/script failures schema lookup cannot settle.
7. **`stl-scope-script-basics`** — Most high-risk Stellaris script mistakes are scope mistakes.
8. **`stl-naming-namespace-hygiene`** — Safe IDs, event namespaces, loc keys, flags, and variables prevent avoidable collisions before code exists.
9. **`stl-scripted-triggers`** — Reusable compatibility gates and AI conditions are foundational and small.
10. **`stl-scripted-effects`** — Reusable setup/repair/cleanup logic needs separate scope and side-effect discipline.
11. **`stl-on-actions-implementation`** — on_actions are high-risk and common enough to keep hook design separate from events.
12. **`stl-on-actions-validation`** — Duplicate/nested behavior and pulse safety need validation that is separate from implementation.
13. **`stl-events-implementation`** — Events are the glue layer for scripted workflows, but should not include on_actions or validation.
14. **`stl-economic-plans-implementation`** — AI economy work is central and should load without ship/UI/megastructure context.
15. **`stl-zones-zone-slots`** — 4.x planet construction depends heavily on zones/slots/building sets and often interacts with PD/UIOD/Stellar AI.

## Next wave

After those, build `stl-compat-ship-stack`, `stl-compat-uiod`, `stl-compat-gigastructures`, `stl-compat-stellar-ai`, `stl-runtime-smoke-test`, `stl-savegame-safety`, and `stl-packaging-descriptor-release`.