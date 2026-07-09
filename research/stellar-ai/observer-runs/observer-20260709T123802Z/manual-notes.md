# Manual Notes For observer-20260709T123802Z

## Setup

- Launch surface: verify `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\StellarAIDirector.mod` still points to `C:/Users/Admin/Documents/GIT/GameMods/StellarisMods/mods/StellarAIDirector` before launch.
- Irony collection/playset: current launcher-resolved Stellaris playset; verify `dlc_load.json` still includes `mod/StellarAIDirector.mod`.
- Stellar AI Director included: expected yes by descriptor and `dlc_load.json`; runtime startup proof modal must confirm.
- Game version: repo target is 4.4.5; previous live run displayed Pegasus v4.4.4 (7d82), so recheck main menu.
- Galaxy size: Tiny / 200 stars.
- AI empire count: 6.
- Difficulty: Ensign.
- Scaling: off.
- Advanced AI starts: off.
- Player/AI hidden bonuses: off; no DAAM/player/hidden AI economic bonuses.
- Gigastructural Engineering preset: Arcade unless startup modal records otherwise.
- Crisis settings:
- Seed save: none yet; create fresh constrained observer start after confirming mod load.
- Baseline commit: `8807310 Boost under-curve research construction`.
- Previous failed run: `observer-20260709T104133Z` stopped at 2325; top included regular AI reached only 860.299 monthly research and direct save inspection found an excluded country at about 1507.57, still below the needed 3,000-by-2350 curve.
- Current patch hypothesis: emergency under-curve research construction weights should make labs, institutes, supercomputers, archaeostudies, and habitat science districts overpower generic construction choices when an empire is economically safe but below the research curve.
- Command harness status before setup: must be absent / `managed_observer_schedule=false` before enabling this run.

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
| Stronger under-curve research construction weights will convert safe midgame economies into sustained research growth. | `observer-20260709T104133Z` 2325 checkpoint: top included regular AI only 860.299 research/month despite positive energy/alloy/mineral/CG income and no deficits; generated economic plans already targeted high research. | At least one regular AI should exceed the prior 2300/2325 slope, remain above 1,000 by 2300, continue compounding by 2325, and reach 3,000+ monthly research before 2350. | Implemented in commit `8807310`; static generator, validator, focused test, and full unit suite passed. | Pending live rerun. |
