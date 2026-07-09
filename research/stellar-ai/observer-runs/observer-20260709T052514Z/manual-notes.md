# Manual Notes For observer-20260709T052514Z

## Setup

- Launch surface: launcher-resolved `dlc_load.json` plus direct Stellaris executable if Irony UI automation is not available.
- Irony collection/playset: `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`; Irony Mod Manager process was already running before T30 setup.
- Stellar AI Director included: yes, verified in T28 by `dlc_load.json` containing `mod/StellarAIDirector.mod`.
- Game version: local runtime displayed Stellaris 4.4.4 despite the project target/default being 4.4.5. Treat this as a runtime-version risk for final claims.
- Galaxy size: Tiny / smallest available galaxy.
- AI empire count: 6 regular AI empires on Tiny galaxy setup, with advanced starts off.
- Difficulty: Ensign or nearest no-hidden-bonus setting.
- Scaling: off.
- Advanced AI starts: off.
- Player/AI hidden bonuses: off.
- Crisis settings: leave collection/default unless the setup screen forces a choice; max benchmark year is 2350.
- Seed save: create fresh T30 run save if UI control succeeds.
- Computer Use: not mounted in this Codex thread. Exact tool discovery for Computer Use exposed no Computer Use tool, and plugin discovery did not list an install candidate. Runtime control will use script helpers, screenshots, and PowerShell process/UI control only where needed.

## Console Verification

Record exact `help <command>` results before relying on commands.

| command | help verified | result or alternative |
| --- | --- | --- |
| `human_ai` | no | |
| `observe` | no | |
| `game_speed 5` | no | |
| `fast_forward <days> 1` | no | |

## Runtime Boundary

- User condition for live testing is satisfied: non-runtime implementation, static validation, documentation/evidence, live launcher readiness, and final package gate are complete.
- `commands_at_date.txt` must be enabled only for the active observer attempt and disabled before handoff.
- Required checkpoint years: 2250, 2300, 2325, and 2350, with an early diagnostic stop allowed if the run is plainly below the research-snowball target.
- Explicit success gate from user: at least one AI empire reliably reaches 3,000+ total monthly research before 2350.
- Runbook stretch/diagnostic target: roughly 6,000+ total monthly research by 2350 for 25x-crisis relevance.

## Checkpoint Notes

### 2250

- Evidence: `screenshots/checkpoint-2250-reached-20260709T0738Z.png`, `saves/checkpoint-2250-autosave_2250.01.01.sav`, `exports/checkpoint-2250-benchmark.md`, and `checkpoints.csv`.
- Extractor result: 9 eligible regular AI countries, checkpoint date 2250.01.01.
- JDataMunch dataset `stellar_ai_observer_20260709T052514Z_checkpoints` validated after this checkpoint with 9 rows and 25 columns.
- Top research country was `Klumetan Berserkers` at 274.516 monthly research, 48.57 alloys income, 25 fleet power, 5 colonies, and 6 parsed megastructures.
- Error-log triage used safe Headroom compression on `logs/checkpoint-2250-20260709T0738Z-error.log`; compressed output highlighted active-stack/Gigas/asset noise and a Planetary Diversity ship-scope decision error, with no preserved `STELLAR_AI_DIRECTOR` marker.

### 2300

- Evidence: `screenshots/checkpoint-2300-reached-20260709T0731Z.png`, `saves/checkpoint-2300-autosave_2300.01.01.sav`, `exports/checkpoint-2300-benchmark.md`, and `checkpoints.csv`.
- Extractor result: 10 eligible regular AI countries, checkpoint date 2300.01.01.
- JDataMunch dataset `stellar_ai_observer_20260709T052514Z_checkpoints` validated after this checkpoint with 19 rows and 25 columns.
- Top research country was `Feral Hesukaran Annihilators` at 470.409 monthly research, 94.296 alloys income, 193 fleet power, 8 colonies, and 27 parsed megastructures.
- Research snowball status: concerning but not yet stopped; continue to 2325 as the decisive early-stop checkpoint. The run must bend sharply upward to remain plausible for the 3,000+ monthly research success gate by 2350.

### 2325

- Evidence: `screenshots/checkpoint-2325-reached-20260709T0743Z.png`, `saves/checkpoint-2325-autosave_2325.01.01.sav`, `exports/checkpoint-2325-benchmark.md`, and `checkpoints.csv`.
- Extractor result: 8 eligible regular AI countries, checkpoint date 2325.01.01.
- JDataMunch dataset `stellar_ai_observer_20260709T052514Z_checkpoints` validated after this checkpoint with 27 rows and 25 columns.
- Top research country was `NAME_The_Chosen` at 644.918 monthly research, 186.761 alloys income, 317 fleet power, 3 colonies, and 17 parsed megastructures.
- Second place was `Klumetan Berserkers` at 571.319 monthly research, 149.897 alloys income, 45 fleet power, 10 colonies, and 23 parsed megastructures.
- Early-stop result: failed research-snowball trajectory. The run is below the 3,000+ monthly research success gate and below the observer-loop diagnostic expectation of being near or above roughly 1,000 monthly research well before this point. Preserve evidence, stop the run, patch, and rerun rather than continuing to 2350 on this trajectory.

### 2350

- Deferred for this failed attempt. Do not claim 2350 success from this run.

## Qualitative Behavior

- Strong AI behavior:
- Bad economy behavior: research scaling remains much too weak; best parsed regular AI reached only 644.918 monthly research by 2325.
- Bad fleet/war behavior: several high-economy/high-pop countries had zero or near-zero parsed fleet power by 2300-2325, while research still did not snowball.
- Missing modded asset usage:
- Deficit or collapse cases:

## Patch Hypotheses

Each hypothesis must cite evidence from this run, source files, logs, saves, screenshots, or current research.

| hypothesis | evidence | expected effect | patch status | result |
| --- | --- | --- | --- | --- |
| Research snowball still lacks a high-pressure late-midgame accelerator for regular AI empires. | 2325 checkpoint leader at 644.918 research/month; second at 571.319 despite 17-23 parsed megastructures. | Add/retune Director plan pressure so qualifying AIs shift harder into research-job/building/habitat/megastructure compounding before 2300. | open | |
| Fleet/war pressure may be consuming alloys without enough conquest/economy payoff, or some empires are demilitarizing after expansion. | 2300-2325 rows show several empires with 0-50 parsed fleet power while others remain low-research; 2325 leader has only 317 fleet power. | Audit war/fleet/economy balance so aggression expands economy instead of stalling research. | open | |
