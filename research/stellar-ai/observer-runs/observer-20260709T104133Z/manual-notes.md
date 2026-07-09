# Manual Notes For observer-20260709T104133Z

## Setup

- Launch surface: `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod\StellarAIDirector.mod` points to `C:/Users/Admin/Documents/GIT/GameMods/StellarisMods/mods/StellarAIDirector`.
- `dlc_load.json`: includes `mod/StellarAIDirector.mod` as the final enabled mod entry when checked before run setup.
- Irony collection/playset: launch through current Irony/launcher-resolved playset; record exact selected playset in screenshot or note at launch.
- Stellar AI Director included: yes, by launcher descriptor and `dlc_load.json`; runtime startup modal must still confirm load.
- Game version: runtime main menu screenshot `screenshots/startup-after-70s.png` displayed Pegasus v4.4.4 (7d82); repo target remains 4.4.5, so runtime-version mismatch remains a risk.
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
- Current patch hypothesis at launch: source-backed `has_designation` multipliers on generated research labs, research institutes/supercomputers/archaeostudies, and habitat science districts should convert research-designated worlds into actual research jobs while retaining support-economy gates.
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

- Screenshot: `screenshots/checkpoint-2250-screen.png`.
- Save: `saves/observer-20260709T104133Z-2250.01.01.sav`.
- Extractor: `python tools\extract_stellar_ai_checkpoint.py --save ... --checkpoint-year 2250 --append`.
- Result: 7 eligible regular AI rows. Top regular AI research was 276.136/month (`Galactic %ADJECTIVE% Somcuedovian Union`, country 3); top-three by research were 276.136, 165.923, and 165.771.

### 2300

- Screenshot: `screenshots/checkpoint-2300-screen-final.png`.
- Save: `saves/observer-20260709T104133Z-2300.01.01.sav`.
- Result: 7 eligible regular AI rows. Top regular AI research was 1079.421/month (`Galactic %ADJECTIVE% Somcuedovian Union`, country 3); second was 632.376. This was late but still potentially salvageable for a 3,000-by-2350 target, so the run continued.

### 2325

- Screenshot: `screenshots/checkpoint-2325-screen-paused.png`.
- Save: `saves/observer-20260709T104133Z-2325.01.01.sav`.
- Result: 7 eligible regular AI rows. Top included regular AI research was only 860.299/month (`Tranquil %ADJECTIVE% Gricretoid Cooperative`, country 16777222), below the 2300 leader and far below the curve required for 3,000 by 2350.
- Additional diagnostic nuance: direct save inspection found country 3 at about 1507.57 research/month at 2325, but that country was excluded by the regular-AI extractor filter at this checkpoint; even counting it, the slope is still too shallow for the benchmark.
- Decision: stop early per runbook evidence-to-patch rule. The run did not continue to 2350 because 2325 evidence already disproved the current patch hypothesis.

### 2350

- Not run for this attempt. User success criteria were not met; 2325 evidence required another implementation patch before burning more runtime.

## Qualitative Behavior

- Strong AI behavior:
- Bad economy behavior: high positive energy/alloy/mineral income existed by 2300/2325, but research throughput did not compound enough; generated economic-plan targets were high, so construction execution/weight pressure was the likely bottleneck.
- Bad fleet/war behavior:
- Missing modded asset usage: mega counts existed in checkpoint rows, but research did not scale proportionally; evidence suggests many investments were not turning into science output fast enough.
- Deficit or collapse cases:

## Patch Hypotheses

Each hypothesis must cite evidence from this run, source files, logs, saves, screenshots, or current research.

| hypothesis | evidence | expected effect | patch status | result |
| --- | --- | --- | --- | --- |
| Research construction weights are still too polite after the designation-only patch; under-curve empires with safe economies need labs and habitat science districts to overpower generic construction. | 2325 checkpoint top included regular AI only 860.299 research/month; 2300/2325 JData rows show positive energy/alloy/mineral/CG income and no deficits; generated economic plans already target high research. | Raise lab/science district construction priority on under-curve and midgame empires, including non-designated developed colonies, while preserving collapse/runway gates. | Implemented after stopping this run: stronger `research_throughput_infrastructure` weights in `tools/stellar_ai_director_lib.py`, regenerated research building/district overrides, tests and validator passed. | Pending rerun. |
