# Manual Notes For observer-20260707T105756Z

## Setup

- Launch surface: Irony Mod Manager
- Irony collection/playset: `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`
- Stellar AI Director included: yes; project descriptor path points to this workspace mod
- Game version: Stellaris 4.4.4 stable target
- Galaxy size: Tiny, 200 stars
- AI empire count: 12
- Difficulty: Ensign
- Scaling: off
- Advanced AI starts: off
- Player/AI hidden bonuses: off; difficulty-adjusted AI modifiers off
- Crisis settings: random crisis, 25x crisis
- Benchmark bar: 25x-crisis readiness is not satisfied by hundreds of monthly research or ordinary fleet/naval usage. Treat roughly 6000+ monthly research by 2350 as the minimum research-scale target, and treat tens-of-millions fleet power as the eventual crisis-relevance scale.
- Seed save: fresh random empire launch, Cidnuran Consciousness; observer mode active by 2200.01.02
- Setup proof: `screenshots/setup-advanced-settings.png`
- Mod load proof: `screenshots/stellar-ai-director-loaded.png`
- Observer proof: `screenshots/observer-mode-2200-01-02.png`

## Console Verification

Record exact `help <command>` results before relying on commands.

| command | help verified | result or alternative |
| --- | --- | --- |
| `human_ai` | no | |
| `observe` | no | |
| `game_speed 4` | no | scheduled for 2200.01.01 and fallback 2200.01.02 through `commands_at_date.txt` |
| `fast_forward <days> 1` | no | |

The scheduled `human_ai`/`observe` commands appear to have fired by 2200.01.02:
the player resource bar and capacity values were zeroed, the outliner no longer
showed normal controlled empire assets, and the simulation advanced at fastest
speed after startup dialogs were dismissed.

## Checkpoint Notes

### 2250

- Checkpoint reached by scheduled pause at visible date 2250.01.02; evidence save copied from `autosave_2250.01.01.sav`.
- Extractor appended 12 ranked regular-AI rows from 13 eligible regular countries.
- JDataMunch dataset `stellar_ai_observer_20260707T105756Z_checkpoints` validated `ok` for 12 rows and 25 columns.
- 2250 aggregate: average economy 1340.2345, average fleet/naval used 84.3333, average alloys income 57.0839, average research 247.7058.
- Top three average: economy 1995.3977, fleet/naval used 110.6667, alloys income 75.3, research 306.03.
- Top empire: Divine %ADJECTIVE% Maganir Council, economy 2309.683, fleet/naval used 170, alloys income 85.784, research 350.643.
- Early read: no ranked empire has crossed the patched >100 monthly alloy payoff threshold yet, so this checkpoint is baseline evidence rather than a shipyard-payoff verdict.

### 2300

- Checkpoint reached by scheduled pause at visible date 2300.01.02; evidence save copied from `autosave_2300.01.01.sav`.
- Extractor appended 12 ranked regular-AI rows from 13 eligible regular countries.
- JDataMunch dataset `stellar_ai_observer_20260707T105756Z_checkpoints` validated `ok` for 24 rows and 25 columns across 2250 and 2300.
- 2300 aggregate: average economy 2394.419, average fleet/naval used 164.6667, average alloys income 119.8210, average research 394.8492.
- Top three average: economy 3966.9433, fleet/naval used 318.6667, alloys income 213.2940, research 682.4107.
- Top empire: Vazuran Hegemony, economy 4205.262, fleet/naval used 595, alloys income 263.561, research 256.865, colonies 10, megastructures 17.
- Patch signal: several empires now exceed the patched >100 monthly alloy payoff threshold. Fleet conversion is mixed: Vazuran converts strongly, while Luo-xu-li State has economy 3884.111, research 1064.519, alloys 151.385, and only 89 fleet/naval used. Continue to 2325 before drawing a result.

### 2325

- Checkpoint reached by scheduled pause at visible date 2325.01.02; evidence save copied from `autosave_2325.01.01.sav`.
- Extractor appended 12 ranked regular-AI rows from 13 eligible regular countries.
- JDataMunch dataset `stellar_ai_observer_20260707T105756Z_checkpoints` validated `ok` for 36 rows and 25 columns across 2250, 2300, and 2325.
- Corrected benchmark read: this is a failed run by the 25x-crisis target. Best 2325 research is Luo-xu-li State at 1463.190, while the top economy empire Vazuran Hegemony has only 561.619 research. The run is not plausibly on track for roughly 6000+ monthly research by 2350.
- 2325 aggregate: average economy 2886.4058, average fleet/naval used 149.0833, average alloys income 137.3621, average research 447.2296.
- Top three by economy average: economy 4996.6013, fleet/naval used 302.0, alloys income 278.3053, research 589.7430.
- Stop decision: preserve 2325 artifacts and diagnose research snowball failure before any further fleet-focused tuning. The prior wording that treated 2350 research around 800 as a partial success was wrong for this 25x crisis goal.

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
| Lowering `staid_shipyard_payoff_ready` from >150 to >100 monthly alloys will convert more mid-tier surplus-alloy empires into shipyard/fleet payoff before 2350. | Prior run `observer-20260707T090209Z` had Albrotan at 2350 with +109.213 alloys, +636.966 energy, and fleet/naval used 48; the previous >150 gate excluded that case while the existing under-cap lane already uses >100. | More non-collapsed mid-tier empires should build fleet/naval usage once alloy income is above 100, without waiting for elite-economy income. | applied before launch; generated mod files and validator/tests passed sequentially | pending rerun |
