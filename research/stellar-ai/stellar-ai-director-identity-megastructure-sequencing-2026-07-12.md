# Identity-aware megastructure sequencing

Target: Stellaris Pegasus 4.4.4 active stack. Gigastructural Engineering & More (4.4), Steam ID 1121692237, is active before the launcher-linked Director. The validated 2026-07-08 Gigas AI-hook dataset contains 810 megastructure objects; this slice changes only existing Director-owned, final-winner route objects.

## Start-stage sequencing boundary

Identity preferences apply only to fifteen exact new-start objects with no top-level `upgrade_from`:

- Research: `macro_test_site_0`, `atmosphere_shredder_0`, `think_tank_0`, `planetary_computer_0`.
- Gestalt Growth: `ring_world_1`, `interstellar_habitat_0`, `stellar_ring_habitat_0`.
- Conquest and Extermination: `mega_shipyard_0`, `planetcraft_printer_0`, `war_moon_0`, `war_system_0`.
- Megacorp economy: `dyson_sphere_0`, `orbital_arc_furnace_1`, `asteroid_manufactory_0`, `matrioshka_brain_0_g_star`.
- Inward Perfection: the two interstellar/stellar-ring habitat starts.
- Barbaric Despoiler: the four military starts.

Resolved primary factors are at most 1.15, lead-secondary factors are 1.05, and defining-identity factors are 1.10. Same-vector primary/secondary roles remain mutually exclusive, while a deliberately blended cross-vector military identity can combine one primary, the other vector's secondary, and Barbaric Despoiler. The conservative static ceiling is therefore 1.15 x 1.05 x 1.10 = 1.32825, below 1.33. Every modifier uses the route generator's source-proven `from` country scope and requires the existing route build gate, eligible conflict-free identity, safe basic-economy runway, and no survival, recovery, catastrophic-collapse, or core-deficit short-runway state.

All continuation stages remain identity-neutral. Their increasing Director base weights and `staid_megastructure_continuation_priority_ready` remain responsible for finishing committed projects. Storage-cap Kugelblitz, apex O-star/scarce-site starts, `habitat_central_complex`, Nomad/Arkship/Waystation/Wayline objects, budgets, costs, placement, prerequisites, resources, effects, and upgrade chains are unchanged.

## Top five risks and controls

1. **Upgrade leakage:** identity preference on continuation stages could delay completion or flatten parent sequencing. Control: exact fifteen-start allowlist plus regression checks proving every other owned megastructure remains free of identity modifiers.
2. **Constructor-queue monopoly:** already-large route weights could crowd out other legal projects. Control: factors are bounded, existing affordability/route gates remain factor-zero authoritative, and recovery/deficit states disable identity tie-breakers.
3. **Mixed-vector stacking:** civic, primary, and cross-vector secondary identity can compound. Control: same-vector primary/secondary exclusion remains in the classifier; individual factors are at most 1.15; and a structural regression check fixes the conservative cumulative ceiling at 1.32825, below 1.33.
4. **Gigas full-object drift:** copied objects could lose placement, upgrade, resource, or scripted behavior. Control: the existing shared route renderer reconstructs active source objects, preserves non-`ai_weight` content, uses active object inventory for optional references, and must match every generated group.
5. **Special-site or Nomad damage:** scarce stars, special habitat controllers, or mobile infrastructure could receive inappropriate priorities. Control: explicit exclusion tests cover apex targets and Habitat Central Complex; no Nomad/Arkship/Waystation route is in the allowlist.

## Static/runtime boundary and rollback

Static proof covers final generated objects, exact start allowlist, country scope, bounded factors, route/recovery gates, continuation and special-site exclusions, source reconstruction, parser/reference validity, and absence of state mutation. It cannot prove site availability, constructor assignment, actual start order, build completion, or economic payoff.

Runtime acceptance records identity vectors, candidate starts, existing unfinished megastructures, site legality, resource budget/runway, constructor/build queue, chosen start, continuation timing, and completion over multiple years. No game launch or save mutation was performed.

Rollback is one fine-grained commit removing the identity megastructure modifier helper and megastructure file from the focused archetype overlay allowlist while retaining all parent route weights and prior identity consumers.
