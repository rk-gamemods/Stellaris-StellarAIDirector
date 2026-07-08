# Passive galaxy failure modes

This guide diagnoses the common “AI builds fleets but does not fight” outcome in replacement AI mods.

## First principle

Fleet construction, war desire, legal CB/wargoal access, diplomacy action validity, and post-war fleet missions are separate gates. Raising one gate cannot repair another.

## Fast diagnostic flow

1. **Is the intended personality active?** Check that the highest-weight `common/personalities` object is the one you think it is.
2. **Can the empire legally place claims?** Check `can_add_claim`, war philosophy, target owner type, influence, and claim range/value.
3. **Does the target produce a CB?** Check `has_casus_belli` or use UI/player control to inspect.
4. **Does at least one wargoal appear and pass `possible`?** Inspect target fail text.
5. **Can `action_declare_war` pass?** Check federation vote law, subject/overlord cases, and hardcoded restrictions.
6. **Does declaration score survive distance and power checks?** Inspect war declaration distance, bravery, and relative power.
7. **After war starts, can fleets get missions?** Check `MIN_FLEET_FOR_OPERATIONS`, `ENEMY_FLEET_POWER_MULT`, pathing, access, transports, and target priorities.

Sources for the distinct gates: Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50; Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: war declaration distance/score defines, fileciteturn9file0L99-L103; Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: CB schema comments, fileciteturn22file0L3-L11; Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: conquest/humiliation wargoals, fileciteturn29file0L143-L291; Public mirror HildoYe/game_files@e6d531, common/diplomatic_actions/00_actions.txt: action_declare_war object, fileciteturn45file0L108-L144; Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: fleet confidence/mission defines, fileciteturn9file0L17-L19 and fileciteturn14file0L87-L106

## Failure-mode catalog

| Failure mode | Why it makes the galaxy passive | Confirmed surfaces | Diagnosis | Safer fix | Confidence |
|---|---|---|---|---|---|
| High aggression but no claims | `aggressiveness` raises desire but `cb_claim` needs actual claims | Personality comments; `cb_claim`; claim rules | Check target has claims by AI | Raise influence/claim range/value; keep `unrestricted_wars`; test claim purchase | High |
| High aggression but `no_wars` or `liberation_wars` | Policy blocks normal conquest/claims | `war_philosophy` policy and `can_add_claim` | Inspect policy flags | Adjust policy AI weights or allowed options | High |
| High fleet budget but no CB path | Ships do not create legal war reason | CB/wargoal files | Player-control empire and inspect Declare War UI | Add valid CB/wargoal chain | High |
| Personality overwrite replaced by another mod | Your war fields are not active | Personality selection by weight; mod load order | Log/console active personality | Use additive files, unique keys, compatibility patches | High |
| Economic plan hoards alloys or starves influence | AI cannot buy claims or ships despite desire | Inference plus claim/fleet surfaces | Inspect stockpiles and claim count | Reduce competing influence/alloy sinks; adjust budgets | Medium |
| Starbase spending crowds out ships | Naval defense grows but mobile power stays low | General AI economy; fleet confidence defines | Compare fleet power vs starbase/naval cap | Cap starbase spending during war-prep tests | Medium |
| Claim budget starved | AI values targets but never purchases claims | Claim scoring defines; influence economy inferred | Watch influence and claims over 5 years | Lower claim costs; increase influence; raise claim factors | Medium |
| War goal invalid under policy | CB may exist but selected wargoal fails | War goals + policies | Inspect `possible` fail text | Align policy flag and wargoal `potential` | High |
| AI can build ships but auto-design invalid | Fleet power/effectiveness low; confidence fails | Personality ship prefs; fleet confidence defines | Inspect designs, component roles, fleet power | Fix auto-design weights and components | Medium |
| War declaration score blocked by distance | Candidate below score floor or beyond max distance | War declaration defines | Put empires adjacent in test | Increase max distance carefully or lower malus | High |
| War declaration score blocked by bravery/relative power | AI avoids peer/superior targets | Personality bravery + wiki thresholds | Test target at inferior/equivalent/superior | Raise bravery or improve fleet/economy | Medium-high |
| All multipliers multiply a base of zero | Zero `aggressiveness`, zero AI weight, or zero policy weight kills output | Script comments and weights | Check base weights first | Keep nonzero base values, use additive modifiers | High |
| Active AI overhaul replaces surface | Your files not loaded or overwritten | Mod load order | Diff final loaded game files | Compatibility patch after overhaul | High |
| Federation vote law blocks war | War requires unanimous/majority/leader vote | Federation law file changes `action_declare_war` settings | Inspect federation law | Adjust laws or AI vote weights | High |
| Target is protected by subject/overlord relation | CB/action possible checks block target or redirect war | CBs, action_declare_war | Inspect subject agreement and overlord | Use correct subject CB or agreement terms | High |
| Non-aggression/defensive pact web | Legal target is diplomatically blocked or too risky | Diplomatic actions and acceptance fields | Map pacts/truces | Lower pact acceptance or add break behavior | Medium |
| Truces after broken deals | AI cannot immediately re-attack | Diplomatic action comments and hardcoded diplomacy | Inspect truce timers | Avoid forced pact churn; shorten only with care | Medium |
| Total-war CB suppresses normal CBs | `has_total_war_cb` makes normal CBs false | CB files | Check total-war flags | Scope total-war conditions narrowly | High |
| Wargoal `ai_weight` too low | AI picks another goal or none if all invalid | Wargoal `ai_weight` | Compare all possible wargoals | Keep positive weights and avoid zeroing conquest/humiliation accidentally | High |
| Target all claimed, non-conquest goal blocked | Many wargoals require at least one unclaimed colony system | Wargoal possible blocks | Check `has_claimed_all_systems` fail text | Avoid overclaiming if using subjugation/ideology/plunder | High |
| AI declares but never attacks | Post-war military mission confidence fails | Fleet operation defines | Check fleets assigned missions | Tune `ENEMY_FLEET_POWER_MULT`, transports, target priorities | High |
| AI attacks fleets but never invades | Army threshold/transport logic fails | `ENEMY_ARMY_POWER_MULT`, transport defines | Inspect transport count and army power | Build armies and lower threshold cautiously | High |
| AI retreats constantly | Damaged thresholds/combat bravery too cautious | Fleet damaged thresholds; combat bravery | Observe retreat/repair loops | Adjust damaged thresholds/combat bravery | Medium |
| Large galaxy passive edges | Distance malus and claim max distance too restrictive | Claim/declaration distance defines | Measure hyperlane distance | Scale distances with galaxy size, but avoid cross-galaxy wars | High |
| Large galaxy endless wars | Distance too permissive creates unreachable targets | Same | Watch pathing and travel times | Increase target locality or path constraints | High |

## Minimal reproducible passive-galaxy test

Use one small map and three target pairs:

- Adjacent conquest pair: force `unrestricted_wars`, give influence, require one claim.
- Rivalry pair: bad relations and valid `action_make_rival`; no claims.
- Total-war pair: purifier/swarm/terminator or containment target.

The pair that fails identifies the broken gate. If all three pass on a small map but fail on a large map, inspect distance and economy scaling before touching personalities.
