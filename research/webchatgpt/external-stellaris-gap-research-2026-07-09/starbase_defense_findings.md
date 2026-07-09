# Starbase, Orbital Ring, And Planetary Defense Findings

## Direct answer

For the requested stack, **Starbase Extended 3.0 is the strongest current static-defense candidate** because its Workshop page says it supports Stellaris 4.**.*, Vanilla, NSC, and ACOT and adds starbase levels up to large module/building counts [S041]. **Expanded Starbases is not recommended for the NSC3 stack** because its page explicitly says it is not compatible with NSC or other mods that modify the starbase ship-size file [S042]. **Planetary-cannon mods are not currently high-confidence 4.4.x picks** because the At War original points to a takeover fork [S043] and the continuation page is labeled 3.9.* [S044]. **Eternal Vigilance Redux is a promising optional add-on** for automated defense platforms if its economy/upkeep behavior is acceptable [S045].

## Strong static defense strategy

### What static defense should do

- Protect shipyards, gateways, megastructure systems, and chokepoints.
- Buy time for fleet concentration and reinforcement.
- Force crisis/fallen/Gigas fleets into favorable engagements.
- Support mobile fleets; never replace them in 25x/Gigas crisis contexts.

### Starbase Extended role

Starbase Extended adds large starbase levels and many module/building slots [S041]. In a high-powered stack, that makes it useful for:

- bastion chokepoints;
- high-throughput shipyard systems;
- defensive anchor systems around Gigas megastructures;
- fortress/orbital-ring style hardpoints;
- AI defensive-pressure routes.

### Orbital rings and planetary defense

The public starbase-modding reference makes clear that starbases have GUI/building/module surfaces and ship-size/section/component surfaces [S046]. Mods that touch orbital rings, starbase levels, or ship sizes can conflict with NSC3 and Starbase Extended. Treat orbital-ring defense as part of the starbase conflict scan, not a separate harmless system.

## Compatibility findings

| Mod | Use / avoid | Reason | Source |
|---|---|---|---|
| Starbase Extended 3.0 | Use as primary defense pillar | Supports 4.**.*, Vanilla, NSC, ACOT; adds starbase levels/slots; new game recommended | [S041] |
| Expanded Starbases | Avoid with NSC3 stack | Explicitly incompatible with NSC and other starbase ship-size modifiers | [S042] |
| At War: Planetary Cannons original | Concept only | Old page points to takeover fork | [S043] |
| At War: Planetary Cannons 3.9.* | Avoid until proven | Labeled 3.9.*, not 4.4.x | [S044] |
| Eternal Vigilance Redux | Optional test | Automates defense-platform construction with policies and AI energy gates | [S045] |

## Common broken symptoms

- Starbase upgrade chain stops at vanilla level despite mod installed.
- Module/building slots display wrong counts.
- UI shows fewer slots than the mod provides.
- Ship designer or starbase designer has missing components/reactors.
- Defense platforms auto-build everywhere and crush energy economy.
- NSC3 or Starbase Extended starbase ship-size conflicts appear in Irony.

## AI Director decisions

1. Add starbase defense weights only behind energy/alloy income gates.
2. Use bastion chokepoint logic for static defense, not everywhere-spam.
3. Use shipyard megabase systems for fleet throughput once alloys/naval cap are ready.
4. Do not combine multiple starbase-level mods unless Irony proves a deliberate patch.
5. Treat planetary cannon mods as watchlist only until 4.4.x source proof exists.
