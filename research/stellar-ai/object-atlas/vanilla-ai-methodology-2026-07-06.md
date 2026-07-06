# Stellar AI Director Vanilla AI Methodology Notes

Generated during the 2026-07-06 object-atlas foundation pass. This note records the vanilla AI patterns the Director should copy before adding modded policy.

## Source Files Inspected

- `C:\Steam\steamapps\common\Stellaris\common\economic_plans\01_base.txt`
- `C:\Steam\steamapps\common\Stellaris\common\economic_plans\03_advanced.txt`
- `C:\Steam\steamapps\common\Stellaris\common\economic_plans\05_endgame.txt`
- `C:\Steam\steamapps\common\Stellaris\common\policies\00_policies.txt`
- `C:\Steam\steamapps\common\Stellaris\common\strategic_resources\00_strategic_resources.txt`
- `C:\Steam\steamapps\common\Stellaris\common\inline_scripts\ai\ai_strategic_resources.txt`
- `C:\Steam\steamapps\common\Stellaris\common\buildings\00_example.txt`

## Methodology Summary

Vanilla AI is not expressed as one universal "make economy bigger" knob. It layers local object eligibility and weights with broad economic-plan pressure. The Director should follow that pattern: route policy should create prerequisites, resources, and strategic state, then object-specific weights should be added only where the atlas says parent AI support is absent, partial, or pointed at the wrong goal.

Economic plans are the primary economy steering surface. Vanilla has base, advanced, and endgame economic-plan files, and the building example warns that building `ai_weight` is no longer the normal building-control path when economic plans are active. For the Director, this means broad economy changes belong in economic plans and budgets, while direct building/district overrides should be treated as narrower policy exceptions.

Selectable object surfaces still use local AI weights where the game expects local choices. Vanilla policies and strategic resources contain `ai_weight` blocks, and technology/AP/ship/component/modded objects often expose analogous local weight surfaces. The atlas therefore records `source_has_ai_weight` separately from route policy: an AI block is evidence of parent support, but not proof that the parent support pursues high-scale Gigas/NSC3/ESC routes.

Vanilla object definitions express prerequisites, unlocks, gates, costs, upkeep, and produced resources in the object blocks themselves. The Director's dependency graph should preserve those facts as edges rather than flattening them into score-only tuning. This is especially important for Mega Engineering, Mega Shipyard, planetcraft, war moons, systemcraft, ESC high-tier components, and special-resource economies.

Strategic resources have explicit AI handling and reusable AI inline scripts. The Director should treat modded resources such as sentient metal, negative mass, megaconstruction, supertensiles, dark matter, and ESC resource chains as first-class stockpile/income constraints, not as generic alloy or energy estimates.

Events and scripted triggers/effects are gate surfaces, not optional flavor. Vanilla and parent mods can hide unlocks, flags, and country state in events or reusable scripts. Parser gaps and unresolved gates must remain visible in the atlas and route reports until a source-backed edge or manual annotation resolves them.

## Director Rules Derived From Vanilla

- Use economic plans and AI budgets for broad economy posture.
- Use object-specific weights only after a policy row names the object, route, timing, safety gates, and parent-AI strategy.
- Preserve parent AI support when it already handles the object and only supply missing prerequisites/resources.
- Classify AI support as complete, partial, wrong-goal, absent, or unknown before overriding.
- Keep trade, strategic resources, and special modded resources as distinct bottlenecks.
- Keep unresolved event/script gates as manual-review blockers instead of guessing.
