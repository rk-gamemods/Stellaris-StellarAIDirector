# Stellar AI Observer Loop Runbook

This runbook owns the repeatable observer-simulation workflow for improving Stellar AI Director. The goal is to make at least one or two top AI empires plausibly competitive by 2350 against 25x endgame-crisis pressure without hidden AI/player economic bonuses.

For this goal, "crisis competitive" is a very high bar. A 2350 empire with only hundreds of monthly research is a failed benchmark even if its economy, alloys, or parsed naval usage improved. Treat roughly 6000+ monthly research by 2350 as the minimum research-scale target, and treat 25x crisis fleet preparation as requiring eventual fleet power on the order of tens of millions. Parsed fleet/naval usage in checkpoint CSVs is diagnostic, not success by itself.

## Authority

Source order:

1. Current user instruction and active goal objective.
2. Repository `AGENTS.md`.
3. Open Brain memories for Stellar AI Director observer setup, Irony validation, economy coverage, and crash work.
4. Current Irony/Stellaris state, launcher descriptors, `dlc_load.json`, logs, saves, screenshots, and observer artifacts.
5. Current vanilla and active mod files.
6. Current external research.
7. Model judgment after the above evidence.

Do not claim runtime success without observer artifacts. Do not claim the AI is fixed from static validation alone.

## Standard Artifact Layout

Create runs under:

```text
research/stellar-ai/observer-runs/<run-id>/
  README.md
  metadata.json
  manual-notes.md
  checkpoints.csv
  metrics.json
  summary.json
  summary.md
  logs/
  saves/
  screenshots/
  exports/
```

Use `python tools/new_stellar_ai_observer_run.py` to create a new run folder. Use `python tools/summarize_stellar_ai_observer_run.py` after adding notes, checkpoint rows, logs, saves, or screenshots.

## Baseline Setup

Default baseline unless the user changes it:

- Stellaris PC 4.4.5 stable/current local install.
- Launch through Irony Mod Manager or an Irony-equivalent launcher-resolved playset.
- Verify the selected playset includes `Stellar AI Director`.
- Small galaxy baseline.
- Ensign, no scaling, no advanced AI starts, no player bonuses, and no hidden economic bonuses.
- Use a fixed 2200.01.01 seed save for comparable tuning unless testing galaxy generation, empire generation, starts, origins, civics, or initial conditions.

Record exact UI labels when they differ from these names.

## Launch And Console Procedure

### `commands_at_date.txt` lifecycle

The live user-folder command schedule is a temporary observer-test harness, not
a mod setting. It must never be left at
`C:\Users\Admin\Documents\Paradox Interactive\Stellaris\commands_at_date.txt`
after an observer run or checkpoint capture.

Use the manager script only when the user explicitly approves an AI observer
run:

```powershell
python tools\manage_stellaris_commands_at_date.py status
python tools\manage_stellaris_commands_at_date.py enable
python tools\manage_stellaris_commands_at_date.py disable
```

Before normal play or before ending an observer task, run `disable` and verify
that `status` reports `exists: False`. Do not copy an observer
`commands_at_date.txt` artifact into the live Stellaris user folder by hand.

Before starting a long observer run, prove the control path end to end. Do not
accept "Fastest" UI speed as sufficient when console acceleration is available.
Do not start a long run if the agent cannot reliably open the console, pause and
unpause with the keyboard, issue the faster-than-fastest command, and recover
the game to galaxy view with the observer panel visible.

Use `game_speed 5`, not `game_speed 4`, for approved observer schedules. Local
user-provided visual proof shows this unlocks the dev-only higher speed that
the Stellaris UI displays as `GAME_SPEED_6`. Treat older notes, help text, or
templates that imply `game_speed 4` is the maximum as superseded for observer
automation.

Candidate command sequence from prior memory:

- `human_ai`
- `observe`
- `game_speed 5`
- `ticks_per_turn <amount>` for faster-than-fastest simulation when available and verified
- `fast_forward <days> 1` when available and verified

If a command is unavailable, record the exact help result and use the closest verified alternative.

The benchmark loop should be automated rather than manually driven:

- open console and verify `help ticks_per_turn`;
- set the accelerated tick rate for run legs;
- pause at checkpoint dates;
- capture the screenshot, save, logs, and checkpoint CSV automatically;
- restore galaxy view with the observer country list visible;
- resume only after artifacts are verified.

If this automation cannot be proven, switch to supervised/manual operation with
the user steering rather than pretending the agent-run loop is efficient.

## Checkpoints

Capture benchmark evidence around:

- 2250
- 2300
- 2325
- 2350

For each checkpoint, inspect multiple AI empires, not only the leader. At minimum record leader, top 3 average, top 25% average, median surviving empire, bottom 25%, collapsed/stagnant empires, and chronic-deficit empires.

Record where visible:

- fleet power;
- naval capacity used and available;
- research output;
- alloys, consumer goods, energy, minerals, food, and strategic-resource income/stockpile;
- colonies, pops, systems, habitats, megastructures, and kilostructures;
- wars, subjects, unemployment/jobs, buildings/districts, and policies;
- qualitative behavior mistakes.

If no empire is plausibly on track by 2300 or 2325, stop early, preserve artifacts, diagnose the bottleneck, patch, validate, and rerun. "On track" must be judged primarily by research snowball toward the 6000+ by 2350 target, then by economy, alloys, megastructure use, and actual war/crisis preparation. Do not call a run a partial success merely because it improves fleet/naval usage while research remains far below the target.

Early research benchmarks matter. A strong run should be approaching or above
roughly 1000 monthly research around 2270-2280, then compounding rapidly toward
5000-6000+ by 2350. If the 2270-2300 slope is too shallow, diagnose research
buildings, jobs, policies, tech weights, pop growth, habitats/kilostructures,
megastructure unlocks, and empire-type strategy before tuning fleet.

Fleet is only useful when it buys strategic advantage. Treat fleet spending as
waste unless it supports defense or aggressive conquest, vassalization,
territorial expansion, political wins, or economy capture. Militarist empires
may justify heavier fleet investment, but they must also have lower war
thresholds and more aggressive neighbor exploitation. Non-militarist empires
should bias toward research/economy/diplomacy and only maintain defensive fleet
unless their situation clearly rewards expansion.

Federation behavior matters. Avoid steering high-research/economy empires into
non-research federations when the benchmark depends on a research snowball.

## Evidence To Patch Rule

Every patch hypothesis must cite at least one concrete source:

- observer-run checkpoint row;
- save summary or parsed save evidence;
- Stellaris log or crash artifact;
- vanilla or active mod file;
- generated Director audit artifact;
- external research source;
- screenshot or manual note captured in the run folder.

Keep changes scoped and reversible. Regenerate generated files, run static validation, and document expected effect before the next run.

## Validation

For helper changes:

```powershell
python -m unittest tools.tests.test_stellar_ai_observer_loop
```

For observer command-schedule lifecycle checks:

```powershell
python tools\manage_stellaris_commands_at_date.py status
```

The live status must be absent outside an explicitly active observer run.

For Stellar AI Director patches:

```powershell
python tools\generate_stellar_ai_director_patch.py
python tools\validate_stellar_ai_director_patch.py
python -m unittest discover -s tools\tests
```

For documentation changes, refresh and verify the JDocMunch index before relying on new sections.

## Reporting

Each milestone report should state:

- run ID or why no runtime run happened;
- what was observed;
- bottleneck diagnosed;
- patch or artifact changed;
- validation commands and results;
- next highest-leverage experiment.

End every substantive Stellaris mod status report with the required live mod, commit, and push status block from `AGENTS.md`.
