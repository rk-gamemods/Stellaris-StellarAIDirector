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

This remains an explicit mapping for the ordinary-resource lane. The strategic
lane evaluates the exact, deliberately narrow trigger subset used by the twelve
restored Stellar AI recovery subplans: source-derived `years_passed` windows,
resource availability, `has_deficit`, monthly-income floors, and stockpile
floors. It does not claim to be a general PDX interpreter. Every selected or
evaluated subplan name must exist in the current generated PDX or the diagnostic
stops with an error.

The scenario CSV supplies starting incomes, stockpiles, marginal investment
increments, duration, and state labels. Each abstract investment is assigned to
the largest proportional shortfall against the active PDX targets, with the
existing research/resource urgency multipliers retained only as a simplified
planner response. Those multipliers do not change the PDX targets being tested.

## Strategic-resource extension

Strategic-resource construction is a separate delayed lane; it is never routed
through the legacy instant-investment allocator. For volatile motes, exotic
gases, and rare crystals the model tracks gross production, upkeep, optional
monthly upkeep growth, live net income, raw and visible stockpiles, project
starts, pending output, completion month, total producer capacity, mineral
construction cost, and post-completion energy upkeep.

The deterministic monthly order is:

1. apply projects due at the start of the month and their completion vectors;
2. apply strategic upkeep growth and recompute live net income;
3. evaluate the single source-derived recovery band for the current year;
4. queue feasible projects, counting pending output only for duplicate
   prevention and never as live income;
5. debit construction minerals;
6. update `raw_stockpile += live_net`, clamp the visible stockpile at zero, and
   record the maximum external bridge needed.

A project started in month 1 with the vanilla 480-day/16-month construction
delay completes at the start of month 17. Total capacity counts both pending and
completed projects and cannot be reused as fictitious concurrent slots.

## Prevention and shock-repair contracts

The model intentionally distinguishes two outcomes:

- A gradual shortage must activate at the positive income floor and complete
  production before the raw stockpile reaches zero. This is the prevention
  contract.
- A sudden captured-pop or upkeep shock may require market purchases while
  construction is pending. The model reports eventual production recovery,
  construction-only survival, bridge quantity, and bridge affordability as
  separate results; it never injects free resources into the trace.

The 2290.07.01 copied-save calibration has 209.341 gross gas, 348.608 upkeep,
-139.267 net income, and 721.753 stockpiled gas. Nine existing refineries imply
12.699444 gas per refinery-equivalent. The endgame +16 target therefore needs
13 additional projects. They cost 6,500 minerals and add 39 energy upkeep,
complete in month 17, and need a 1,506.519 gas bridge. The zero-growth exact
case reaches +25.825778 gas income; a separately labeled +0.034 upkeep-growth
sensitivity needs a 1,511.143 bridge and still ends at +19.705778.

The copied save also contains 476,959.614 market currency (`trade`). Vanilla
4.4.4 defines strategic resources as 10 units per 100 trade at base price. At
the +400 maximum price fluctuation and the 30% base market fee, the model uses a
conservative 65 trade per gas. The exact shock bridge therefore costs at most
97,923.735 trade under that bound and is affordable from the saved reserve.
This proves financing capacity, not that the opaque engine will buy a specific
amount; the restored native `ai_wants` object remains responsible for demand.

The prevention case begins at +9 gas with +0.034 monthly upkeep growth. The
source-derived endgame floor activates at month 30 while income is still
positive, starts one project, completes it at month 46, and never depletes the
initial stockpile. This is the primary acceptance condition.

## Initial PDX-derived failure

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

These failures were evidence about the generated targets under the stated
scenario mapping. They replace the earlier abstract-model result, which passed
because Python itself imposed the desired 2:1 ratio and low food floor. That
earlier method could not serve as a test of the mod and has been removed.

The first immediately visible PDX cause is the base plan's `food = 60`. Every
normal scenario that starts below it is pulled above the desired normal ceiling.
The wartime cases also activate a large alloy/energy military reserve without a
matching research target, allowing the research ratio to fall far below 2:1.
The implementation pass subsequently changed those PDX values.

## Corrected PDX-derived result

The generator now sets the normal base food target to +10. The militarist
reserve was reduced from crisis-scale flat targets to an operational reserve
(`alloys 600`, `energy 350`, `minerals 250`, `unity 100`, `trade 80`) and now
adds 710 total research target across the three research fields.

| Scenario | Final research / ordinary | Support safe | Final food | Result |
|---|---:|:---:|---:|---|
| Early balanced | 3.2803 | Yes | 12 | Pass |
| Early expansion | 3.2057 | Yes | 20 | Pass |
| CG constrained | 3.1065 | Yes | 20 | Pass |
| Energy constrained | 3.1059 | Yes | 20 | Pass |
| Food surplus trap | 2.2886 | Yes | 775 | Pass: no additional food pressure |
| Food deficit recovery | 3.1039 | Yes | 13 | Pass |
| Midgame fleet pivot | 2.1679 | Yes | 15 | Pass |
| Rich wartime research | 2.0324 | Yes | 50 | Pass |
| Late research scale | 3.4970 | Yes | 30 | Pass |
| Bio-ship burden | 2.9452 | Yes | 20 | Pass |

The opt-in PDX diagnostic now exits successfully: every modeled scenario keeps
support safe and finishes at or above the 2:1 research ratio, while normal food
does not receive new pressure above +50.

## Artifacts

- `stellar-ai-economic-model-scenarios-2026-07-11.csv`: scenario inputs.
- `stellar-ai-strategic-resource-model-scenarios-2026-07-11.csv`: copied-save,
  prevention, sensitivity, isolated-shortage, and compound-shortage inputs.
- `stellar-ai-economic-model-timeline-2026-07-11.csv`: monthly PDX-driven trace.
- `stellar-ai-economic-model-summary-2026-07-11.csv`: final result per scenario,
  including the PDX source path.
- `tools/simulate_stellar_ai_economy.py`: PDX parser and deterministic model.
- `tools/manual_checks/check_stellar_ai_economy_model.py`: opt-in doctrine check.
- `tools/manual_checks/test_stellar_ai_economy_model.py`: exact legacy hashes,
  trigger boundaries, build delay, bridge, cost, capacity, and sibling-isolation
  regression tests.

## Limitations and next step

This is not Stellaris engine emulation. It does not model individual pops,
workforce assignment, exact planet-slot selection, dynamic market purchasing
decisions, price movement caused by each trade, designation choice, or competing
active-stack economic plans. Build time, capacity, construction/upkeep vectors,
the relevant recovery triggers, and conservative bridge affordability are now
modeled explicitly. The abstract planner remains comparative proof of policy
logic, not proof of opaque runtime execution.

The next design pass should change the generator's PDX economic bands, rerun
this opt-in diagnostic, and compare the generated timeline. Only after the
PDX-derived cases satisfy the intended doctrine should the change proceed to
merged-plan validation and a separately approved observer test.
