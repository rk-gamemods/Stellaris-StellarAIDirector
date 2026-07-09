# Planetary Diversity And Guilli Strategy Findings

## Direct answer

Planetary Diversity and Guilli’s Planet Modifiers should be valued by **planet role evidence**, not planet names. Planetary Diversity’s main page says it uses events to change existing planets after game start and lists current submods such as Unique Worlds, More Arcologies, Gaia Worlds, Exotic Worlds, and Vanilla Replacements [S054]. PD submods can be gameplay-heavy: Exotic Worlds adds archetypes, world classes, districts, jobs, buildings, deposits, and terraforming paths [S056]. Guilli’s Planet Modifiers and Features adds hundreds of planetary modifiers and content that interacts with them, with compatibility claimed for Planetary Diversity and Gigastructures [S057]. The wiki baseline is that planet modifiers can be positive, negative, or mixed and affect colonies [S059].

## Strongest world-priority logic

### Research worlds

Prioritize worlds with:

- direct research job output modifiers;
- rare research deposits/features;
- PD/Gaia/relic-style lab buildings;
- high building-slot density;
- low habitability penalties after species/class matching;
- synergy with scientist/governor/council modifiers.

**AI rule:** if a world has strong research modifiers and safe upkeep, lock research designation and lab/zone buildout before generic urban/trade development.

### Alloy/industrial worlds

Prioritize worlds with:

- mineral/industrial district support;
- alloy/foundry output modifiers;
- high stability/habitability;
- nearby logistics/defense;
- low rare-resource bottlenecks;
- forge designation potential.

**AI rule:** only convert to heavy alloy when mineral/energy/strategic-resource support is safe. In 25x/Gigas, alloy worlds become mandatory during conversion phase.

### Energy/mineral worlds

Prioritize worlds with:

- district-count advantages;
- energy/mineral modifiers;
- strategic location near shipyards/megastructures;
- ability to support researcher/foundry upkeep.

**AI rule:** energy/mineral worlds are support worlds. Their job is to fund labs, shipyards, and megastructures, not to maximize raw local prestige.

### Rare-resource and strategic worlds

Prioritize worlds with:

- exotic gas/rare crystal/volatile motes deposits;
- Gigas/ESC/PD/Guilli special-resource deposits;
- building slots to exploit rare-resource chains;
- low devastation/defense risk.

**AI rule:** rare-resource worlds can outrank nominal research/alloy worlds when they unlock bottleneck upkeep for labs, components, or megastructures.

### Trade/unity worlds

Prioritize only when:

- empire has trade-policy support;
- piracy and route protection are safe;
- unity unlocks ascension/perk routes faster than more labs;
- world has strong direct trade/unity modifiers.

**AI rule:** in high-threat games, trade/unity must justify itself against research/alloy/crisis readiness.

## Crowded high-threat galaxy priorities

1. Colonize or capture worlds with strong research/alloy/rare-resource modifiers first.
2. Treat habitability/class as a gate, not a goal; modifiers decide role.
3. Do not over-colonize marginal worlds if they delay labs or alloy conversion.
4. Use planetary modifiers to route jobs/buildings early, because bad early designation wastes the snowball.
5. In AI logic, keep PD/Guilli modifiers as first-class valuation inputs.

## Compatibility and load order

- Use UIOD+Planetary Diversity when UIOD and PD are both active; the patch page provides load order: PD -> UIOD -> UIOD+PD [S049].
- Guilli claims special compatibility with PD and Gigas [S057], so a separate PD+GPM patch is not automatically required; verify active Workshop pages/source before adding old patches [S058].
- PD submods are not all harmless visuals. Exotic Worlds adds mechanics; More Arcologies/Gaia Worlds/Unique Worlds likely need separate AI valuation [S054][S056].

## AI valuation outputs to generate later

- `planet_role_research_score`
- `planet_role_alloy_score`
- `planet_role_energy_score`
- `planet_role_minerals_score`
- `planet_role_rare_resource_score`
- `planet_role_trade_score`
- `planet_role_growth_score`
- `planet_role_defense_score`
- `planet_role_megastructure_support_score`

These should read active-stack modifiers/deposits/classes from local source and generated object atlas. The research answer is the strategy and evidence hierarchy; exact IDs are local implementation data.
