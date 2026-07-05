# Stellar AI Director Launch Validation Evidence

Game executable exists: True
Game executable: `C:\Steam\steamapps\common\Stellaris\stellaris.exe`
Launcher descriptor exists: True
Launcher descriptor points to source: True
Enabled in dlc_load.json: True
Generated runtime files: 10
Launch evidence status: stale_or_missing_logs
Main menu proven: True
Main menu evidence: manual main-menu proof markers recorded for baseline_without_director, with_director

## Log Review

| log | exists | newer than generated files | bytes | Director lines | expected override lines | Director problem lines | unclassified lines |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| error.log | True | False | 41990928 | 4 | 4 | 0 | 0 |
| game.log | True | False | 3810 | 2 | 0 | 0 | 2 |

## Director Line Samples

### error.log

- `expected_intentional_override: [21:36:50][game_singleobjectdatabase.h:170]: Object with key: alloys_expenditure_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_alloys_budget.txt line: 5`
- `expected_intentional_override: [21:36:50][game_singleobjectdatabase.h:170]: Object with key: sentient_metal_expenditure_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_gigas_resource_budgets.txt line: 6`
- `expected_intentional_override: [21:36:50][game_singleobjectdatabase.h:170]: Object with key: negative_mass_expenditure_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_gigas_resource_budgets.txt line: 24`
- `expected_intentional_override: [21:36:50][game_singleobjectdatabase.h:170]: Object with key: supertensiles_upkeep_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_gigas_resource_budgets.txt line: 42`

### game.log

- `unclassified: [21:41:08][effect_impl.cpp:21978]: [2200.1.1] Log effect, file: events/zzz_staid_load_proof_events.txt line: 17. STELLAR_AI_DIRECTOR_LOAD_PROOF: Stellar AI Director v1 loaded for United Nations of Earth`
- `unclassified: [21:48:16][eventcommands.cpp:88]: Event staid_load_proof.1 added info about event selection. selectedOption 0, human 1, playerEventId 3`
