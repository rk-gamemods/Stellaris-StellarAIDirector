# Manual Notes For observer-20260707T090209Z

## Setup

- Launch surface: Irony Mod Manager launched Stellaris from the active collection.
- Irony collection/playset: `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`.
- Stellar AI Director included: yes; Irony list showed `Stellar AI Director` enabled at load order 120, and the in-game startup proof event displayed `Stellar AI Director Loaded`.
- Game version: Pegasus v4.4.4 (e3ff) on the main menu.
- Galaxy size: Tiny (200 stars).
- AI empire count: 12.
- Difficulty: Ensign.
- Scaling: off.
- Advanced AI starts: off.
- Player/AI hidden bonuses: player bonuses off; difficulty-adjusted AI modifiers disabled.
- Crisis settings: Random crisis type, 25x crisis strength.
- Seed save: new random player empire, Democratic Fallatian Accord; custom Alarian Kernel was still blocked by design/DLC validation.

## Startup Proof

- Main menu/version proof: `screenshots/current-stellaris-state.jpg`.
- Irony playset proof: `screenshots/irony-selected-stellar-ai-director.jpg`.
- General settings proof: `screenshots/after-random-select.jpg`.
- Advanced settings proof: `screenshots/new-game-advanced-settings.jpg`.
- Stellar AI Director loaded proof: `screenshots/after-stellar-ai-confirm-gulli-start.jpg`.
- Startup mod choices: Forgotten Empires defaults advanced via `Begin`; Gigastructures `Giga-Experience`; Gulli defaults/start.
- Observer command proof: `screenshots/after-pause-click-advance.jpg` shows zeroed player resources, empty observer outline, date 2204.07.01, and Fastest speed after the scheduled `human_ai`, `observe`, and `game_speed 4` commands fired.

## Console Verification

Record exact `help <command>` results before relying on commands.

| command | help verified | result or alternative |
| --- | --- | --- |
| `human_ai` | scheduled `help human_ai` at 2200.01.01/2200.01.02 | Observer proof screenshot shows player resources zeroed after schedule fired. |
| `observe` | scheduled `help observe` at 2200.01.01/2200.01.02 | Observer proof screenshot shows empty observer outline after schedule fired. |
| `game_speed 5` | no; schedule uses `game_speed 4` | Observer proof screenshot shows Fastest speed after schedule fired. |
| `fast_forward <days> 1` | no | |

## Checkpoint Notes

### 2250

- Runtime state: scheduled pause reached at 2250.01.02; screenshot `screenshots/checkpoint-2250-exact-or-near.jpg`.
- Save captured: `saves/checkpoint-2250-autosave_2250.01.01.sav`.
- Parsed report: `exports/checkpoint-2250-save-report.md`.
- Parsed JSON: `exports/checkpoint-2250-save-summary.json`.
- JDataMunch dataset: `stellar_ai_observer_20260707T090209Z_checkpoints`, validated `ok` after indexing `checkpoints.csv`.
- Structured rows: 12 eligible regular AI rows from 71 countries in the save.
- Top regular rows by economy: rank 1 `NAME_The_Chosen` economy 2531.745, fleet 220, research 412.343, alloys 54.232, pops 23482; rank 2 `Ro-Adj State` economy 1809.128; rank 3 `EMPIRE_DESIGN_zeriphen1` economy 1427.659; rank 4 `SPEC_Alari Kernel` economy 1406.833 with the highest listed alloys income at 134.359.
- Note: several type 10 Forgotten Empires / special countries were excluded by the benchmark parser as special/outlier evidence, not regular AI benchmark rows.

### 2300

- Runtime state: scheduled pause reached at 2300.01.02; screenshot `screenshots/checkpoint-2300-exact-or-near.jpg`.
- Save captured: `saves/checkpoint-2300-autosave_2300.01.01.sav`.
- Parsed report: `exports/checkpoint-2300-save-report.md`.
- Parsed JSON: `exports/checkpoint-2300-save-summary.json`.
- Structured rows: 11 eligible regular AI rows from 68 countries in the save.
- Top regular rows by economy: rank 1 `Engineer Autocracy` economy 4382.409, fleet 348, research 666.105, alloys 220.391, pops 22610; rank 2 `Ro-Adj State` economy 4052.679; rank 3 `NAME_The_Chosen` economy 3892.869; rank 4 `Olmalgill Imperium` economy 2476.165; rank 5 `Albrotan %ADJ% Allied Nations` economy 2296.252.
- Note: naval capacity available remains blank because the live 4.4.4 save surface does not expose the simple field the parser knows how to read; naval capacity used/fleet size is populated.

### 2325

- Runtime state: scheduled pause reached at 2325.01.02; screenshot `screenshots/checkpoint-2325-exact-or-near.jpg`.
- Save captured: `saves/checkpoint-2325-autosave_2325.01.01.sav`.
- Parsed report: `exports/checkpoint-2325-save-report.md`.
- Parsed JSON: `exports/checkpoint-2325-save-summary.json`.
- Structured rows: 12 ranked regular AI rows emitted from 13 eligible regular AI countries and 65 total countries in the save.
- Top regular rows by economy: rank 1 `Engineer Autocracy` economy 5374.918, fleet 440, research 806.623, alloys 301.109, pops 27378; rank 2 `Ro-Adj State` economy 4583.283; rank 3 `Olmalgill Imperium` economy 3196.91; rank 4 `NAME_The_Chosen` economy 3065.644; rank 5 `Albrotan %ADJ% Allied Nations` economy 2516.818.
- Benchmark note: by 2325 the top regular AI crossed 300 monthly alloys and 800 research with 440 fleet size/naval capacity used, while the second economy crossed 4500 economy power and 700 research.

### 2350

- Runtime state: scheduled pause reached at 2350.01.02; screenshot `screenshots/checkpoint-2350-exact-or-near.jpg`.
- Save captured: `saves/checkpoint-2350-autosave_2350.01.01.sav`.
- Parsed report: `exports/checkpoint-2350-save-report.md`.
- Parsed JSON: `exports/checkpoint-2350-save-summary.json`.
- Structured rows: 12 ranked regular AI rows emitted from 13 eligible regular AI countries and 67 total countries in the save.
- Top regular rows by economy: rank 1 `Engineer Autocracy` economy 6152.658, fleet 558, research 807.745, alloys 326.823, pops 33976; rank 2 `NAME_The_Chosen` economy 3660.409; rank 3 `EMPIRE_DESIGN_zeriphen1` economy 2728.307 with fleet 316 and alloys 140.795; rank 4 `Albrotan %ADJ% Allied Nations` economy 2612.943; rank 5 `Feral Hesukaran Annihilators` economy 2204.988.
- Benchmark note: one regular AI plausibly reached crisis-relevant economy/alloy scale by 2350 without hidden economic bonuses, but the second-ranked regular AI was materially behind and had only 61 fleet size/naval capacity used in the parsed save.

## Qualitative Behavior

- Strong AI behavior: `Engineer Autocracy` became the clear success case by 2350, rising from economy 4382.409 at 2300 to 6152.658 at 2350, with 326.823 alloys income, 807.745 research, 558 fleet size/naval capacity used, and 24 parsed megastructures.
- Bad economy behavior: `Ro-Adj State` was rank 2 at 2300 and 2325, then fell to rank 12 by 2350 with economy 448.979, 31.884 alloys income, one colony, and 4562 pops. Save inspection showed this was a conquest/subjugation case: by 2350 Ro-Adj had `overlord=28`, while country 28 (`Arann Horde`) owned 13 planets, had one subject, and used 3020 naval capacity.
- Bad fleet/war behavior: several high-economy regular AIs carried low parsed fleet size by 2350, including `NAME_The_Chosen` at economy 3660.409 with fleet 61 and `Albrotan %ADJ% Allied Nations` at economy 2612.943 with fleet 48. The earlier under-cap alloy gate patch improved at least one top empire, but the run still shows possible fleet spend/war survival gaps. `Albrotan %ADJ% Allied Nations` had +109.213 alloys and +636.966 energy in 2350, enough for the +100 under-cap fleet buildup gate but not for the old +150 top-level `staid_shipyard_payoff_ready` gate.
- Missing modded asset usage: parsed megastructure counts indicate top economies are using or owning megastructure-class assets (`Engineer Autocracy` 24 at 2350; `EMPIRE_DESIGN_zeriphen1` 22 at 2350), but the parser does not distinguish built/owned/ruined/inherited objects. Treat this as directional only until save sections are inspected.
- Deficit or collapse cases: no deficit flags were extracted by the current parser, but Ro-Adj's late collapse is the primary follow-up target. The next analysis step should inspect its 2325 and 2350 save country blocks and war/planet ownership context before making another patch.

## Patch Hypotheses

Each hypothesis must cite evidence from this run, source files, logs, saves, screenshots, or current research.

| hypothesis | evidence | expected effect | patch status | result |
| --- | --- | --- | --- | --- |
| Under-cap alloy/fleet gates were too restrictive before this run | Prior patch lowered key under-cap alloy thresholds from `>200` to `>100`; `Engineer Autocracy` reached 326.823 alloys income and 558 fleet size by 2350 without hidden bonuses. | At least one regular AI should build and spend enough alloy output to become crisis-relevant by 2350. | Applied before run | Partially supported: one clear success case, but several strong economies still had low fleet size. |
| Late-game fleet spend/survival still needs investigation | 2350 rows show `NAME_The_Chosen` economy 3660.409 with fleet 61 and `Albrotan %ADJ% Allied Nations` economy 2612.943 with fleet 48; `Ro-Adj State` collapsed from rank 2 at 2325 to rank 12 at 2350. | A follow-up patch may need to target fleet replenishment, war recovery, or collapse prevention rather than raw economy growth. | Analysis narrowed | Ro-Adj is not a clean economy defect because it became a subject of the Arann Horde after losing most planets. High-economy low-fleet regular AIs remain the cleaner signal. |
| Shipyard payoff gate still excluded +100 to +150 alloy under-cap empires | `Albrotan %ADJ% Allied Nations` had economy 2612.943, fleet 48, +109.213 alloys, and +636.966 energy at 2350. Source review found `staid_fleet_buildup_economy_safe` admitted +100 alloys but `staid_shipyard_payoff_ready` still had a top-level +150 alloy gate. | Mid-tier under-cap empires with stable +100 alloys should be allowed into shipyard/fleet payoff routes instead of waiting for +150 alloys or huge stockpiles. | Applied after this run; rerun pending | `tools/stellar_ai_director_lib.py` changed `staid_shipyard_payoff_ready` from alloys `>150` to `>100`; generated triggers refreshed; regression test now asserts the shipyard block has no +150 alloy gate. Validation: generator passed; `python tools\validate_stellar_ai_director_patch.py` passed; `python -m unittest tools.tests.test_stellar_ai_director tools.tests.test_stellar_ai_observer_loop` passed 34 OK; `python -m unittest discover -s tools\tests` passed 37 OK. |
