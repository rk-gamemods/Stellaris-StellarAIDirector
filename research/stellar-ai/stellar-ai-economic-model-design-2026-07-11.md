# Stellar AI Director PDX-Driven Economic Model

Date: 2026-07-11  
Target: generated Stellar AI Director economic-plan PDX
Execution: opt-in troubleshooting/verbose diagnostic only

## Purpose

This harness tests the economic policy that the mod actually generates. It does
not maintain a second set of Python phase floors or resource targets. Its source
is:

`mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt`

The parser reads `basic_economy_plan`, its base `income`, and every named
`subplan` income directly from that PDX file. If the generator changes the PDX,
the next diagnostic run tests the changed values without manually synchronizing
Python constants.

## Execution boundary

The simulation is intentionally outside routine automatic test discovery. Run
it only while troubleshooting economics or during an explicitly verbose pass:

```text
python tools/manual_checks/check_stellar_ai_economy_model.py
```

The lower-level CSV generator is:

```text
python tools/simulate_stellar_ai_economy.py
```

No game, observer run, live descriptor, or gameplay state is touched.

## Policy being checked

The user-supplied doctrine is the diagnostic acceptance policy, not an input
used to steer the simulated AI:

- research income should be at least twice the sum of positive ordinary net
  income;
- energy and consumer goods must remain adequate;
- normal food production should remain near break-even and should not be pushed
  above +50;
- early expansion should give minerals relative priority;
- war and later phases may increase alloys without allowing research to collapse.

For reporting, the ratio denominator is positive energy, minerals, food,
consumer goods, alloys, unity, and trade. Physics, society, and engineering
targets from PDX are summed into `research`.

## How scenarios select PDX

All scenarios receive the base `basic_economy_plan` income. The model then adds
the PDX incomes for these named subplans, following the vanilla documentation
that active subplan goals are added to the base plan:

| Model phase/state | PDX subplans selected |
|---|---|
| Early | safe research baseline; early modded research rush |
| Mid | safe research baseline; midgame megastructure rush |
| Late | safe research baseline; crisis-scale giga rush |
| At war | phase subplans plus militarist conquest fleet reserve |

This is an explicit scenario mapping. The harness does not pretend to execute
arbitrary PDX triggers. Expanding trigger evaluation is future work; every
selected subplan name must exist in the current generated PDX or the diagnostic
stops with an error.

The scenario CSV supplies starting incomes, stockpiles, marginal investment
increments, duration, and state labels. Each abstract investment is assigned to
the largest proportional shortfall against the active PDX targets, with the
existing research/resource urgency multipliers retained only as a simplified
planner response. Those multipliers do not change the PDX targets being tested.

## Current PDX-derived result

The first PDX-driven run produced the following results:

| Scenario | Final research / ordinary | Support safe | Final food | Doctrine result |
|---|---:|:---:|---:|---|
| Early balanced | 3.0983 | Yes | 60 | Fail: normal food above +50 |
| Early expansion | 3.0317 | Yes | 68 | Fail: normal food above +50 |
| CG constrained | 3.0412 | Yes | 68 | Fail: normal food above +50 |
| Energy constrained | 3.0404 | Yes | 68 | Fail: normal food above +50 |
| Food surplus trap | 2.2886 | Yes | 775 | Existing surplus not increased |
| Food deficit recovery | 3.0383 | Yes | 61 | Fail: normal food above +50 |
| Midgame fleet pivot | 0.9347 | No | 15 | Fail: research below 2:1 |
| Rich wartime research | 0.5675 | No | 50 | Fail: research below 2:1 |
| Late research scale | 3.4719 | Yes | 66 | Fail: normal food above +50 |
| Bio-ship burden | 1.0871 | No | 60 | Fail: research below 2:1 |

These failures are evidence about the current generated targets under the stated
scenario mapping. They replace the earlier abstract-model result, which passed
because Python itself imposed the desired 2:1 ratio and low food floor. That
earlier method could not serve as a test of the mod and has been removed.

The first immediately visible PDX cause is the base plan's `food = 60`. Every
normal scenario that starts below it is pulled above the desired normal ceiling.
The wartime cases also activate a large alloy/energy military reserve without a
matching research target, allowing the research ratio to fall far below 2:1.
This diagnostic does not itself change those PDX values.

## Artifacts

- `stellar-ai-economic-model-scenarios-2026-07-11.csv`: scenario inputs.
- `stellar-ai-economic-model-timeline-2026-07-11.csv`: monthly PDX-driven trace.
- `stellar-ai-economic-model-summary-2026-07-11.csv`: final result per scenario,
  including the PDX source path.
- `tools/simulate_stellar_ai_economy.py`: PDX parser and deterministic model.
- `tools/manual_checks/check_stellar_ai_economy_model.py`: opt-in doctrine check.

## Limitations and next step

This is not Stellaris engine emulation. It does not model pops, jobs, planet
slots, build time, designation choice, market trades, reassignment, trigger
evaluation, or competing active-stack economic plans. The abstract allocation
response is useful for comparative planning, not runtime proof.

The next design pass should change the generator's PDX economic bands, rerun
this opt-in diagnostic, and compare the generated timeline. Only after the
PDX-derived cases satisfy the intended doctrine should the change proceed to
merged-plan validation and a separately approved observer test.
