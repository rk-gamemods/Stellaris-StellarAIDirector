# Stellar AI Director Launch Comparison

Generated from preserved baseline and Director-enabled launch logs.

Launch surface: direct_executable_probe
Director delta status: expected_only
Main menu proven: True
Main menu evidence: manual main-menu proof markers recorded for baseline_without_director, with_director

## Summary

| probe | Director matches | expected override lines | problem lines | unclassified lines |
| --- | ---: | ---: | ---: | ---: |
| baseline without Director | 0 | 0 | 0 | 0 |
| with Director | 4 | 4 | 0 | 0 |

## Baseline Logs

| log | exists | bytes | Director lines |
| --- | --- | ---: | ---: |
| `C:\Users\Admin\Documents\GIT\GameMods\StellarisMods\research\stellar-ai\baseline-without-director-error-2026-07-04.log` | True | 41973687 | 0 |
| `C:\Users\Admin\Documents\GIT\GameMods\StellarisMods\research\stellar-ai\baseline-without-director-game-2026-07-04.log` | True | 177 | 0 |

## Director-Enabled Logs

| log | exists | bytes | Director lines | expected override lines | problem lines | unclassified lines |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `C:\Users\Admin\Documents\GIT\GameMods\StellarisMods\research\stellar-ai\with-director-error-2026-07-04.log` | True | 41971038 | 4 | 4 | 0 | 0 |
| `C:\Users\Admin\Documents\GIT\GameMods\StellarisMods\research\stellar-ai\with-director-game-2026-07-04.log` | True | 177 | 0 | 0 | 0 | 0 |

## Director Line Samples

### with-director-error-2026-07-04.log

- `expected_intentional_override: [20:31:28][game_singleobjectdatabase.h:170]: Object with key: alloys_expenditure_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_alloys_budget.txt line: 5`
- `expected_intentional_override: [20:31:28][game_singleobjectdatabase.h:170]: Object with key: sentient_metal_expenditure_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_gigas_resource_budgets.txt line: 6`
- `expected_intentional_override: [20:31:28][game_singleobjectdatabase.h:170]: Object with key: negative_mass_expenditure_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_gigas_resource_budgets.txt line: 24`
- `expected_intentional_override: [20:31:28][game_singleobjectdatabase.h:170]: Object with key: supertensiles_upkeep_megastructures already exists, using the one at  file: common/ai_budget/zzz_staid_gigas_resource_budgets.txt line: 42`

### with-director-game-2026-07-04.log

No Director-specific lines found in this log.


## Current Conclusion

The comparison shows main-menu proof markers and an expected-only Director log delta, but the recorded launch surface is `direct_executable_probe`, not an Irony or launcher-resolved playset launch.

Next validation must launch the actual parent playset through Irony or another launcher-resolved playset surface before P14 can be marked complete.
