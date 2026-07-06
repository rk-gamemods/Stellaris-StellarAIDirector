# Stellar AI Director

Late-loading deterministic AI policy patch for the active Irony playset.

This mod is a deterministic, full-power AI replacement policy for the current
4.4 high-scale playset. It does not try to preserve vanilla or Stellar AI
assumptions after the opening curve; it encodes explicit state gates,
priorities, and emergency exits for Gigastructural Engineering, NSC3, ESC NEXT,
Starbase Extended, and the active supporting mods.

## Required Parents

- Stellar AI
- Gigastructural Engineering & More (4.4)
- NSC3
- Extra Ship Components NEXT
- Starbase Extended 3.0
- !!!Universal Resource Patch [2.4+]

Detected selected collection: `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`.

Missing required Steam parents during generation: none.

## Scope

- Adds scripted decision-state triggers for survival, recovery, megastructure
  prep, safe commit, surplus-sink pressure, and shipyard payoff exploitation.
- Overrides Stellar AI's megastructure alloy budget object with explicit
  emergency exits and larger reserves for Gigas/NSC3-scale projects.
- Replaces the base economic plan with a mod-set-specific high-scale survival
  plan that forces research, alloy, trade, naval-cap, tall-scaling, and
  megastructure pressure on a mid-2300s crisis curve.
- Adds economic-plan targets for alloy reserves, Gigas special resources,
  and static-defense/starbase pressure when empires need to climb toward
  Gigas/NSC3/ESC-scale economy and fleet power.
- Adds trade-capacity recovery and reserve subplans so the Director preserves
  Stellaris 4.4 logistics/upkeep headroom instead of treating trade as a
  normal buy/sell commodity.
- Adds a monthly market cap-breaker for AI empires that are wasting large
  positive-income stockpiles, converting marketable overflow into trade
  currency instead of letting storage caps void the income.
- Adds a two-pulse stranded-fleet recovery guard that uses vanilla
  `set_mia = mia_return_home` only for idle, MIA-eligible AI fleets outside
  their owner's space while the homeland is under wartime pressure.
- Adds a fleet-throughput economic subplan so Mega Shipyard unlocks and strong
  surplus can become fleet power without ignoring energy/alloy/trade runway checks.
- Adds a planetary-capacity economic subplan plus direct research lab and
  habitat science district construction weights for safe mineral/energy-backed
  tall growth without broad job automation rewrites or trade logistics collapse.
- Adds mandatory unlock-research pressure so AI empires keep pushing
  engineering/research/unity toward Mega Engineering, Mega Shipyard,
  planetcraft/systemcraft chains, NSC hulls, and ESC component tiers.
- Adds a bounded V1 threat-response layer for observed classified aggression:
  opinion modifiers, timed relation/country flags, and a third-party defensive
  readiness economy subplan capped at alloys 7, energy 6, and naval cap 40.
- Keeps unknown or unclassified war goals inert and does not declare wars,
  join wars, add punitive casus belli, or override diplomatic actions.
- Adds full-object route overrides for Mega Engineering, Mega Shipyard, Gigas
  planetcraft/systemcraft unlocks, NSC3 hull unlocks, ESC high-tier component
  unlocks, AP/tradition pressure, economy megastructures, planetcraft, war moon,
  systemcraft, and ESC starbase reactor support.
- Leaves ESC internal component-template `key = ...` overrides and direct NSC3
  ship-design templates as manual-review blockers until the atlas models those
  loader surfaces safely.

## Load Order

Place Stellar AI Director after all required parents and after parent
compatibility patches that the Director must supersede. In the current selected
collection, the latest required parent is at load position
115.
The Director should be below Stellar AI so its megastructure alloy reserve
override wins intentionally.

## Load Proof

When a player-controlled country starts, the mod fires a one-time popup titled
`Stellar AI Director Loaded`. Seeing that popup proves Irony loaded the Director into
the active playset and the game executed the Director event/on_action surface.

## Surplus Sink Ordering

After survival and recovery gates, the Director treats strong alloy/energy
surplus, capped marketable resources, or under-curve research as signals that
the empire needs useful spending outlets. The v1 order is:

1. research sink;
2. fleet-production sink;
3. unity sink.

`source_has_ai_weight` in the ROI matrix only reports whether the parent mod
defined an upstream AI weight. The Director's own policy is expressed in the
separate `director_*` columns.

## Validation

Run:

```powershell
python tools/validate_stellar_ai_director_patch.py
python -m unittest discover -s tools/tests
```
