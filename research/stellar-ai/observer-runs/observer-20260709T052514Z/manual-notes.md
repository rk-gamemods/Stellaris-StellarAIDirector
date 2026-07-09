# Manual Notes For observer-20260709T052514Z

## Setup

- Launch surface: launcher-resolved `dlc_load.json` plus direct Stellaris executable if Irony UI automation is not available.
- Irony collection/playset: `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`; Irony Mod Manager process was already running before T30 setup.
- Stellar AI Director included: yes, verified in T28 by `dlc_load.json` containing `mod/StellarAIDirector.mod`.
- Game version: Stellaris 4.4.5 stable/current local install.
- Galaxy size: Tiny / smallest available galaxy.
- AI empire count: smallest practical Tiny-galaxy AI count visible in setup; record exact value after launch.
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
