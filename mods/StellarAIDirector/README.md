# Stellar AI Director

Late-loading deterministic AI policy patch for the active Irony playset.

This mod does not add runtime self-adjusting behavior. It encodes explicit
state gates, priorities, and emergency exits around Stellar AI and the major
late-game mods in the current 4.4 playset.

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
- Adds economic-plan subplans for alloy reserves, Gigas special resources,
  and static-defense/starbase pressure when defensive or threatened empires
  have safe income and stockpiles.
- Adds a fleet-throughput economic subplan so Mega Shipyard unlocks and strong
  surplus can become fleet power without ignoring energy/alloy runway checks.
- Adds a planetary-capacity economic subplan for safe mineral/energy-backed
  pop and empire-size growth without direct building/job overrides.
- Adds an unlock-research economic subplan so surplus empires keep pushing
  engineering/research/unity until core Mega Engineering and Mega Shipyard
  unlocks are present.
- Adds a bounded V1 threat-response layer for observed classified aggression:
  opinion modifiers, timed relation/country flags, and a third-party defensive
  readiness economy subplan capped at alloys 7, energy 6, and naval cap 40.
- Keeps unknown or unclassified war goals inert and does not declare wars,
  join wars, add punitive casus belli, or override diplomatic actions.
- Leaves NSC3/ESC ship and component design weights untouched in v1 unless
  observer evidence proves parent AI cannot use them.

## Load Order

Place Stellar AI Director after all required parents and after parent
compatibility patches that the Director must supersede. In the current selected
collection, the latest required parent is at load position
114.
The Director should be below Stellar AI so its megastructure alloy reserve
override wins intentionally.

## Load Proof

When a player-controlled country starts, the mod fires a one-time popup titled
`Stellar AI Director Loaded`. Seeing that popup proves Irony loaded the Director into
the active playset and the game executed the Director event/on_action surface.

## Surplus Sink Ordering

After survival and recovery gates, the Director treats strong alloy/energy
surplus plus a large alloy stockpile as a signal that the empire needs useful
spending outlets. The v1 order is:

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
