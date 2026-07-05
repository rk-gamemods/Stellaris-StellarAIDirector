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
| error.log | True | False | 42113555 | 16 | 4 | 0 | 12 |
| game.log | True | False | 2551 | 2 | 0 | 0 | 2 |

## Director Line Samples

### error.log

- `expected_intentional_override: [13:04:46][game_singleobjectdatabase.h:170]: Object with key: alloys_expenditure_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_alloys_budget.txt line: 5`
- `expected_intentional_override: [13:04:46][game_singleobjectdatabase.h:170]: Object with key: sentient_metal_expenditure_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_gigas_resource_budgets.txt line: 6`
- `expected_intentional_override: [13:04:46][game_singleobjectdatabase.h:170]: Object with key: negative_mass_expenditure_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_gigas_resource_budgets.txt line: 24`
- `expected_intentional_override: [13:04:46][game_singleobjectdatabase.h:170]: Object with key: supertensiles_upkeep_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_gigas_resource_budgets.txt line: 42`
- `unclassified: [13:05:30][trigger.cpp:338]: Expected "using_war_goal = {", but got "using_war_goal = wg_conquest" at  common/scripted_triggers/zzz_staid_threat_response_triggers.txt:5 @ in scripted trigger staid_tr_is_conquest_war_goal at file: events/zzz`
- `unclassified: [13:05:30][trigger.cpp:338]: Expected "using_war_goal = {", but got "using_war_goal = wg_humiliation" at  common/scripted_triggers/zzz_staid_threat_response_triggers.txt:13 @ in scripted trigger staid_tr_is_humiliation_war_goal at file: eve`
- `unclassified: [13:05:31][trigger.cpp:338]: Expected "using_war_goal = {", but got "using_war_goal = wg_subjugation" at  common/scripted_triggers/zzz_staid_threat_response_triggers.txt:9 @ in scripted trigger staid_tr_is_subjugation_war_goal at file: even`
- `unclassified: [13:05:31][trigger.cpp:338]: Expected "using_war_goal = {", but got "using_war_goal = wg_humiliation" at  common/scripted_triggers/zzz_staid_threat_response_triggers.txt:13 @ in scripted trigger staid_tr_is_humiliation_war_goal at common/sc`
- `unclassified: [13:05:31][trigger.cpp:338]: Expected "using_war_goal = {", but got "using_war_goal = wg_subjugation" at  common/scripted_triggers/zzz_staid_threat_response_triggers.txt:9 @ in scripted trigger staid_tr_is_subjugation_war_goal at common/scr`
- `unclassified: [13:05:31][trigger.cpp:338]: Expected "using_war_goal = {", but got "using_war_goal = wg_conquest" at  common/scripted_triggers/zzz_staid_threat_response_triggers.txt:5 @ in scripted trigger staid_tr_is_conquest_war_goal at common/scripted_`

### game.log

- `unclassified: [14:21:00][effect_impl.cpp:21978]: [2200.1.1] Log effect, file: events/zzz_staid_load_proof_events.txt line: 17. STELLAR_AI_DIRECTOR_LOAD_PROOF: Stellar AI Director v1 loaded for United Cevantian Nation`
- `unclassified: [14:24:36][eventcommands.cpp:88]: Event staid_load_proof.1 added info about event selection. selectedOption 0, human 1, playerEventId 3`
