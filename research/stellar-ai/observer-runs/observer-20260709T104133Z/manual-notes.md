# Manual Notes For observer-20260709T104133Z

## Setup

- Launch surface: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\StellarAIDirector.mod` points to `C:/Users/Admin/Documents/GIT/GameMods/StellarisMods/mods/StellarAIDirector`.
- `dlc_load.json`: includes `mod/StellarAIDirector.mod` as the final enabled mod entry when checked before run setup.
- Irony collection/playset: launch through current Irony/launcher-resolved playset; record exact selected playset in screenshot or note at launch.
- Stellar AI Director included: yes, by launcher descriptor and `dlc_load.json`; runtime startup modal must still confirm load.
- Game version: repo target is 4.4.5; prior runtime displayed Pegasus v4.4.4 (26b7), so recheck main menu during this run.
- Galaxy size: Tiny / 200 stars.
- AI empire count: 6.
- Difficulty: Ensign.
- Scaling: off.
- Advanced AI starts: off.
- Player/AI hidden bonuses: off; no DAAM/player/hidden AI economic bonuses.
- Tech/logistics setup: match prior constrained benchmark if using 0.5x tech cost, 0.5x logistics fleet upkeep, 0.5x planetary deficit logistics, and fast transfers; record exact UI labels.
- Crisis settings: not the primary proof surface for this capped 2350 research run; record if changed.
- Seed save: none yet; create fresh constrained observer start after confirming mod load.
- Baseline commit: `e684f3e Boost research-designated world construction`.
- Previous failed run: `observer-20260709T080545Z`, no AI reached 3,000 monthly research by 2350; top was 1018.93.
- Current patch hypothesis: source-backed `has_designation` multipliers on generated research labs, research institutes/supercomputers/archaeostudies, and habitat science districts should convert research-designated worlds into actual research jobs while retaining support-economy gates.
- Command harness status before setup: absent / `managed_observer_schedule=false` when checked with `python tools\manage_stellaris_commands_at_date.py status --json`.

## Console Verification

Record exact `help <command>` results before relying on commands.

| command | help verified | result or alternative |
| --- | --- | --- |
| `human_ai` | no | |
| `observe` | no | |
| `game_speed 5` | no | |
| `fast_forward <days> 1` | no | |

## Checkpoint Notes

### 2250

### 2300

### 2325

### 2350

## Qualitative Behavior

- Strong AI behavior:
- Bad economy behavior:
- Bad fleet/war behavior:
- Missing modded asset usage:
- Deficit or collapse cases:

## Patch Hypotheses

Each hypothesis must cite evidence from this run, source files, logs, saves, screenshots, or current research.

| hypothesis | evidence | expected effect | patch status | result |
| --- | --- | --- | --- | --- |
