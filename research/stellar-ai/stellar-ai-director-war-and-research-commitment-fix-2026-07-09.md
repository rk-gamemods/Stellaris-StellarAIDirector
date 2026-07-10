# Stellar AI Director war pressure and research commitment fix

Date: 2026-07-09  
Runtime baseline: Stellaris 4.4.4, forward target 4.4.5, descriptor `v4.4.*`  
Target mod: `mods/StellarAIDirector`

## Runtime evidence

The 2228.01 observer save showed a systemic pre-declaration failure. United Cevantian Nation had about 7,016 military power, hostile bordering empires with roughly 89 and 125 military power, unrestricted wars, claims, subjugation casus belli, and no active war. Its `prepare_war_date_start`, `prepare_war_date`, and target remained at their empty sentinel values. The save contained zero wars globally. This placed the failure before fleet execution: the built-in planner never entered war preparation.

The same empire owned seven colonies but had no research designation: capital, factory, two generic Urban, two Mining, and a Forge designation in the 2228.01 autosave. Vanilla `col_research` weighting is reactive to research zones/buildings/modifiers, so an empty colony can select generic Urban before a research signal exists. The selected designation then reinforces its own construction affinity.

## Removed dependency evidence

Stellar AI 0.10 for Stellaris 4.4.4 does not call `declare_war`, `create_war`, add claims, add casus belli, or override war-aggression defines. It replaces vanilla personalities and raises the `aggressiveness` scalar for 20 shared personality IDs. For example, `ruthless_capitalists` rises from vanilla 1.0 to 3.0; purifiers and exterminators rise to 4.5. Removing Stellar AI therefore removed a material input to the engine war planner that the Director's define-only tuning did not replace.

Stellar AI also maintained persistent `stellarai_research_plan_claimed` flags and used them to make research designations eligible while preventing claimed worlds from falling back to Urban. Removing that runtime dependency removed the colony commitment mechanism even though the Director retained research economic targets.

Sources inspected:

- `C:/Steam/steamapps/common/Stellaris/common/personalities/00_personalities.txt`
- `C:/Steam/steamapps/common/Stellaris/common/colony_types/00_colony_types.txt`
- `C:/Steam/steamapps/workshop/content/281990/3610149307/common/personalities/00_personalities.txt`
- `C:/Steam/steamapps/workshop/content/281990/3610149307/common/scripted_variables/stellarai_scripted_variables.txt`
- `C:/Steam/steamapps/workshop/content/281990/3610149307/events/111_stellarai_commitment_events.txt`
- `C:/Steam/steamapps/workshop/content/281990/3610149307/common/colony_types/~stellarai_colony_types.txt`
- Steam Workshop primary page: `https://steamcommunity.com/workshop/filedetails/?id=3610149307`

## Implemented policy

The Director now generates current-vanilla full-object overrides for the 20 shared personalities and changes only `aggressiveness` to the verified Stellar AI 4.4.4 value. Vanilla diplomacy, behavior flags, bravery, military spending, and colony spending are preserved. Normal wars still use the engine planner, legal casus belli, and war goals. `ENEMY_FLEET_POWER_MULT` remains 0.55, while the existing boss/ultra-boss readiness values remain separate. The local-war distance cap and distance malus remain in place.

Research specialization is now a persistent colony build-out plan rather than a loose building-weight preference:

- fewer than 3 colonies: no forced non-capital research claim;
- 3-4 colonies: 1 research claim;
- 5 colonies: 2 claims;
- 6 colonies: 3 claims;
- from 5 colonies onward: target `floor(owned colonies / 2)`.

The first role is reserved at three colonies. Additional claims require `staid_research_construction_priority_ready`, which enforces consumer-goods and energy runway. When that gate fails, new claims pause but existing commitments remain. Candidate selection strongly prefers research bonuses and generic Urban worlds, avoids consuming industrial/rural specializations when better candidates exist, and heavily avoids Fortress worlds. Claimed normal worlds cannot select `col_city`; only `col_research` remains eligible for that plan lane. Human designation access remains vanilla.

No military-archetype exception is active in this slice. Any lower research ratio for purifiers, exterminators, or another specialized economy should be introduced only as a separately evidenced policy; the current high-power mod stack makes technology a first-class requirement even for military empires.

## Validation

- Generator completed successfully.
- All 88 `tools.tests.test_stellar_ai_director` tests passed.
- `tools/validate_stellar_ai_director_patch.py` passed.
- Generated personality blocks are byte-equivalent to current vanilla after removing the single aggressiveness line.
- Generated PDXScript files parse with the repository parser.
- No Stellaris launch or observer simulation was run for this slice. Runtime proof requires the next user playtest/relaunch.

## Remaining runtime questions

- Whether the restored personality aggression enters war preparation within the first few monthly planner cycles in the 2228 test case.
- Whether the 50% research-plan ratio remains economically sustainable across machine, hive, catalytic, bio-ship, and total-war economies under the active stack.
- Whether habitats, ring worlds, and other special district sets need their own persistent research-plan claims; this slice guarantees normal-planet research roles and preserves existing special research designations in the count.
