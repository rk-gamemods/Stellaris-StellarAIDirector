# Stellar AI Director Observer Test Log

Selected collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity

## Repeatable Setup

- Galaxy size: Tiny Irony-launched smoke save.
- AI count: inferred from save country count (66 initialized countries).
- Difficulty: Cadet smoke setup from launch run notes.
- Crisis settings: inherited selected playset defaults for the smoke save.
- Mod order evidence: required parents are recorded in `notes/load-order.md`; save mod list contains 117 mods.

## Historical Smoke Checkpoints

- Early economy stability: short-smoke pass from `stellar-ai-director-observer-smoke-save-summary-2026-07-04.md`.
- Deficit spiral check: no early deficit collapse observed in parsed 2202.01.01 save metrics.

## Strategic V2 Observer Checkpoints

- First Mega Engineering unlock: not yet proven in the current strategic v2 branch.
- First high-ROI megastructure start: not yet proven in the current strategic v2 branch.
- First economy multiplier completion: not yet proven in the current strategic v2 branch.
- Shipyard/fleet payoff behavior: not yet proven in the current strategic v2 branch.
- War interruption behavior: not yet proven in the current strategic v2 branch.
- Starbase defense investment: not yet proven in the current strategic v2 branch.
- At least one AI empire reaching 3,000+ total monthly research before 2350: not yet proven in the current strategic v2 branch.

## Threat-Response Checkpoints

- Classified aggressive war deterministic contract: covered by generated tests and validator.
- Threat-response generated files emitted after 2026-07-05 implementation: covered by file audit and validator.
- Unknown/modded war goal inertness: covered by classification data, tests, and validator.
- No forced wars, join-war behavior, or punitive CBs: covered by forbidden-effect tests and validator.
- Runtime launch observation: required only after non-runtime gates are complete and runtime evidence is the final remaining blocker.

## Results

Short Irony-launched save summary: `stellar-ai-director-observer-smoke-save-summary-2026-07-04.md`.

- Save date: 2202.07.01.
- Director listed in save mod list: True.
- Short smoke passes: True.
- Player metrics: `{"economy_power": 540.44128, "empire_size": 51.0, "fleet_size": 15.0, "navy_coverage": 0.58823, "num_sapient_pops": 5276.0, "tech_power": 277.5, "used_naval_capacity": 15.0}`.
- Player monthly income: `{"alloys": 15.2, "consumer_goods": 62.602, "energy": 166.524, "engineering_research": 16.728, "food": 119.737, "influence": 4.176, "minerals": 68.246, "physics_research": 21.228, "society_research": 16.728, "trade": 152.165, "unity": 43.527}`.
- High-ROI path observed: False.

This short-smoke evidence is retained as historical context only. Generated
artifacts, tests, validators, and indexed evidence are the non-runtime gates for
the strategic v2 packet; they do not replace the final constrained observer run
required to prove long-run AI efficacy and the 3,000+ total-research-per-month
before 2350 target.
