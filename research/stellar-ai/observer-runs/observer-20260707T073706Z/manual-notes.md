# Manual Notes For observer-20260707T073706Z

## Setup

- Launch surface: Irony Mod Manager
- Irony collection/playset: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity
- Stellar AI Director included: yes, via live launcher descriptor path to project mod folder
- Game version: Stellaris 4.4.4 stable target
- Galaxy size: Tiny (200 Stars)
- AI empire count: 12
- Difficulty: Ensign
- Scaling: off
- Advanced AI starts: off
- Player/AI hidden bonuses: off
- Crisis settings: 25x, Random
- Seed save: fresh patched rerun; prior baseline rerun `observer-20260707T050444Z` is the comparison packet
- Player empire: random built-in empire generated as Zacan Hierarchy; the initially selected custom Alarian Kernel design was invalid under the active DLC/playset surface
- Gigastructures setup: Giga-Experience selected after default Forgotten Empires options
- Gulli's Planet Modifiers setup: default/recommended options accepted

## Console Verification

Record exact `help <command>` results before relying on commands.

| command | help verified | result or alternative |
| --- | --- | --- |
| `human_ai` | no | scheduled through user-dir `commands_at_date.txt`; prior run confirmed observer-like blank-empire state |
| `observe` | no | scheduled through user-dir `commands_at_date.txt`; prior run confirmed observer-like blank-empire state |
| `game_speed 5` | no | using `game_speed 4`, which prior run displayed as Fastest |
| `fast_forward <days> 1` | no | not used by default |

Copied schedule evidence: `exports/commands_at_date.txt`.
Runtime proof:

- `screenshots/2200-stellar-ai-director-loaded-proof.jpg` captures the Stellar AI Director startup proof event in-game.
- `screenshots/2200-observer-mode-fastest-proof.jpg` captures the run after scheduled commands fired: date 2200.09.27, Fastest speed, zero-resource observer-like state, and no hidden bonuses configured.
- Live launch log check after observer proof: 0 hits for `Stellar AI Director`, 0 hits for `Unexpected token: ai_weight`, 0 hits for `using_war_goal trigger: invalid target`, and 1 nested scripted-trigger warning mentioning the `zzz_staid` chain. Treat that warning as a follow-up candidate, not as a current blocker.

## Checkpoint Notes

### 2250

- Paused at 2250.01.02 from the scheduled checkpoint command; proof saved as `screenshots/2250-pause-proof.jpg`.
- Preserved save: `exports/saves/autosave_2250.01.01.sav`.
- Extracted 12 ranked rows from 13 eligible regular countries and appended them to `checkpoints.csv`.
- Top economy at 2250: Werdo Accord, economy 1836.813, research 391.033, alloys +133.992, fleet/naval used 35/35.
- Top fleet/naval used at 2250 among extracted rows: SPEC_Alari Kernel, fleet/naval used 122/122, economy 1470.221, research 310.149, alloys +113.089.
- Aggregate 2250 comparison versus `observer-20260707T050444Z`: current run average economy 1266.789 vs previous 1373.551, average research 244.018 vs 259.056, average fleet 74.0 vs 98.083, average naval used 74.5 vs 98.25, average alloys +59.474 vs +51.827. Early signal is not yet improved fleet conversion, but current alloy income is higher; continue to 2300 before judging the patch.

### 2300

- Paused at 2300.01.02 from the scheduled checkpoint command; proof saved as `screenshots/2300-pause-proof.jpg`.
- Preserved save: `exports/saves/autosave_2300.01.01.sav`.
- Extracted 9 ranked rows from 9 eligible regular countries and appended them to `checkpoints.csv`.
- Top economy at 2300: Werdo Accord, economy 4352.829, tech 4965.0, research 726.866, alloys +298.454, energy +1106.701, fleet/naval used 250/250.
- Top research at 2300: Nintidarite %ADJ% Divine Empire, research 853.846, economy 3824.239, tech 4815.0, alloys +114.429, fleet/naval used 194/186.
- Aggregate 2300 comparison versus `observer-20260707T050444Z`: current run average economy 1846.915 vs previous 2401.006, average research 388.207 vs 454.168, average fleet 104.778 vs 140.0, average naval used 106.333 vs 140.0, average alloys +81.227 vs +88.620, average energy +487.297 vs +642.594. The current field average trails the prior run and only 9 regular empires remain eligible, but the top empire is ahead of the prior run's 2300 leader in economy, tech, fleet/naval use, alloys, and comparable energy. Continue to 2325 to test whether the top one or two empires compound enough to justify the fleet-gate patch.

### 2325

- Paused at 2325.01.02 from the scheduled checkpoint command; proof saved as `screenshots/2325-pause-proof.jpg`.
- Preserved save: `exports/saves/autosave_2325.01.01.sav`.
- Extracted 10 ranked rows from 10 eligible regular countries and appended them to `checkpoints.csv`.
- Top economy/research at 2325: United Flusionian States, economy 4523.564, tech 9752.5, research 1200.589, alloys +305.609, energy +1193.056, fleet/naval used 250/523, colonies 2, megastructures 4.
- Next economy: Balajid Hive, economy 4099.236, tech 5787.5, research 877.304, alloys +127.029, energy +1289.432, fleet/naval used 134/134, colonies 7, megastructures 17.
- Aggregate 2325 comparison versus `observer-20260707T050444Z`: current run average economy 1775.915 vs previous 3477.501, average research 374.275 vs 728.360, average fleet 90.7 vs 211.917, average naval used 119.6 vs 203.583, average alloys +83.104 vs +128.221, average energy +518.052 vs +862.295. Previous 2325 max fleet/naval was 661/561; current max is 250/523. Since the prior run was still weak by 2350, this run is not on track. Stop this run at 2325, preserve artifacts, and patch the fleet income lane before rerunning.

### 2350

## Qualitative Behavior

- Strong AI behavior:
- Bad economy behavior:
- Bad fleet/war behavior:
- Missing modded asset usage:
- Deficit or collapse cases:

## Extraction Notes

- After the 2300 checkpoint, `tools/stellar_ai_observer_loop.py` was patched to populate country-local `colonies` from `controlled_colonies`/`owned_planets` and `megastructures` from `owned_megastructures`; existing 2250 and 2300 rows were regenerated from preserved saves.
- The live 4.4.4 save country blocks expose `used_naval_capacity`, `controlled_colonies`, `owned_planets`, and `owned_megastructures`, but did not expose a simple country-local total naval capacity, owned systems, or habitat classification field. Leave `naval_capacity_available`, `systems`, and `habitats` blank until a stronger cross-object parser is added.

## Patch Hypotheses

Each hypothesis must cite evidence from this run, source files, logs, saves, screenshots, or current research.

| hypothesis | evidence | expected effect | patch status | result |
| --- | --- | --- | --- | --- |
| Fresh rerun after fleet-gate patch should improve 2300/2325/2350 fleet conversion without hidden bonuses. | Previous full cutoff run `observer-20260707T050444Z` showed strong economy/research but weak fleets by 2350; `staid_shipyard_payoff_ready` and `staid_fleet_buildup_economy_safe` were patched to add under-95%-naval-cap monthly alloy/energy lanes while preserving stockpile lanes. | Top one or two regular AI empires should convert more of their economy into naval capacity usage and fleet power by the practical 2350 crisis-readiness cutoff. | Patched and statically validated on 2026-07-07 before this run. | Failed by the 2325 stop gate. Current averages trail the prior run by a wide margin, and the best current fleet/naval track is below the prior 2325 fleet leader. Do not continue this run to 2350; use it as evidence for the next threshold patch. |
| Lower the under-cap fleet income lane from +200 alloys/month to +100 alloys/month. | 2325 save probe shows only the top regular empire clears +200 alloys/month; plausible builders such as Balajid Hive and Feral Hesukaran Annihilators sit around +123 to +127 alloys/month, and the previous run's stronger 2325 field included multiple empires in the +100 to +176 alloy/month range. Source review also found `staid_fleet_buildup_economy_safe` still had a top-level +200 alloy gate, so the prior OR lane was globally blocked for mid-tier builders. | More midgame AIs that are under naval cap and economically solvent should enter fleet buildup before they accumulate giant stockpiles, without opening the lane for weak low-alloy economies. | Patched after 2325 stop: lowered the shipyard income lane and both fleet-buildup alloy gates from >200 to >100, regenerated the mod, and validated. | Pending fresh rerun; current live game was already loaded with the old generated script and should not be used as proof for this patch. |
