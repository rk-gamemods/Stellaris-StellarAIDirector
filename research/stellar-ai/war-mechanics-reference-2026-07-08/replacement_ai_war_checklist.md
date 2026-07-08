# Replacement AI war checklist

This checklist is intended for a coding agent implementing or auditing a replacement AI war system without direct forced-war events.

## A. Active surface validation

- [ ] Confirm the intended personality object wins selection for each empire class.
- [ ] Confirm no other mod overwrites the same personality key after your file loads.
- [ ] Confirm `aggressiveness`, `bravery`, `military_spending`, diplomacy acceptance fields, and `behaviour` flags are present with valid spelling.
- [ ] Confirm no unknown placeholder key such as personality-level `war_philosophy` is being relied on.
- [ ] Confirm the intended economic plan and AI budget can produce alloys, energy upkeep, naval cap, armies, and influence surplus.
- [ ] Confirm ship designs have valid components, roles, and nonzero real fleet power.

Sources: Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50; Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: honorbound/zealot/explorer examples, fileciteturn17file0L57-L85, fileciteturn17file0L127-L155, fileciteturn17file0L219-L247

## B. Policy and diplomatic posture

- [ ] Confirm `war_philosophy` policy option is legal for the empire ethics/civics.
- [ ] Confirm conqueror/subjugator/purger personalities select `unrestricted_wars` when intended.
- [ ] Confirm liberator/ideology personalities select `liberation_wars` when intended.
- [ ] Confirm `no_wars` is limited to intended pacifist cases.
- [ ] Confirm non-aggression, defensive pact, federation, commercial, research, and migration acceptance values do not unintentionally create a galaxy-wide peace web.
- [ ] Confirm rivalries can form if humiliation wars are expected.

Sources: Public mirror HildoYe/game_files@e6d531, common/policies/00_policies.txt: war_philosophy, unrestricted/liberation/no_wars, fileciteturn21file0L21-L48 and fileciteturn20file0L16-L68, fileciteturn20file0L71-L154; Public mirror HildoYe/game_files@e6d531, common/diplomatic_actions/00_actions.txt: action_make_rival, fileciteturn35file0L45-L167

## C. Claim behavior

- [ ] Confirm `can_add_claim` permits claims under the empire’s policy and target type.
- [ ] Confirm `MAX_CLAIM_DISTANCE` and `MAX_CLAIM_DISTANCE_SUBJECT` are appropriate for map scale.
- [ ] Confirm claim target scoring values prefer the systems you expect.
- [ ] Confirm influence income and claim costs allow actual purchases.
- [ ] Confirm `claims_modifier` is not being mistaken for claim desire.
- [ ] Confirm total-war empires do not need normal claims unless fighting same-species/exception cases.

Sources: Public mirror HildoYe/game_files@e6d531, common/game_rules/00_rules.txt: can_add_claim rules and hardcoded caveat, fileciteturn49file0L3-L7 and fileciteturn49file0L29-L135; Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI claim scoring defines, fileciteturn9file0L49-L57; Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50

## D. Casus belli coverage

For every desired war type, verify at least one legal CB path:

- [ ] Conquest: `cb_claim` exists after claims are bought.
- [ ] Humiliation: rivalry or qualifying Galactic Community resolution exists.
- [ ] Subjugation: relative power and target independence pass.
- [ ] Ideology: `liberation_wars`, non-gestalt target, and ethics mismatch pass.
- [ ] Despoliation/raid: civic path and target colony checks pass.
- [ ] Total war: genocidal/assimilator/colossus/containment conditions pass.
- [ ] Subject/secret-fealty/event wars: required flags, agreements, or origins exist.
- [ ] Modded CBs: `potential`, `is_valid`, script grants, and `destroy_if` are tested.

Sources: Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: CB schema comments, fileciteturn22file0L3-L11; Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184; Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: total-war and special CBs, fileciteturn22file0L186-L237 and fileciteturn23file0L18-L112; Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: despoliation/raid/counterattack/allegiance/payback, fileciteturn22file0L239-L253, fileciteturn23file0L1-L16, fileciteturn23file0L126-L183, fileciteturn23file0L242-L296

## E. War-goal coverage

- [ ] Every CB has at least one matching wargoal.
- [ ] Every wargoal has `potential` and `possible` triggers that pass in a controlled test.
- [ ] No target is fully claimed if using subjugation, ideology, humiliation, or plunder goals that block all-claimed targets.
- [ ] `ai_weight` is positive for the desired goals and not accidentally outcompeted by modded goals.
- [ ] Defender default/pairing behavior is defined where needed.
- [ ] Galactic Emperor, Custodian, declared-crisis, Pax Galactica, federation, and subject blockers are intentional.

Sources: Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: conquest/humiliation wargoals, fileciteturn29file0L143-L291; Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: plunder/subjugation/ideology wargoals, fileciteturn25file0L189-L258, fileciteturn26file0L135-L202, fileciteturn28file0L240-L298; Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: total-war wargoals, fileciteturn24file0L105-L230 and fileciteturn25file0L48-L187; Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: independence wargoal, fileciteturn24file0L5-L102

## F. Diplomatic action and federation layer

- [ ] `action_declare_war` is not overwritten destructively by your mod or an overhaul.
- [ ] If patching `action_declare_war`, preserve vanilla `requires_alliance_vote`, independence comments, notification behavior, and possible blockers unless deliberately changing them.
- [ ] Federation declare-war law settings are compatible with desired behavior: unanimous, majority, or leader vote.
- [ ] AI federation law weights do not force pacifying vote structures everywhere.
- [ ] Subject agreement terms and overlord conflict rules are compatible with intended wars.
- [ ] Truces, non-aggression pacts, defensive pacts, and guarantees are tested in save-game scenarios.

Sources: Public mirror HildoYe/game_files@e6d531, common/diplomatic_actions/00_actions.txt: diplomatic-action schema comments, fileciteturn32file0L3-L26; Public mirror HildoYe/game_files@e6d531, common/diplomatic_actions/00_actions.txt: action_declare_war object, fileciteturn45file0L108-L144; Public mirror HildoYe/game_files@e6d531, common/federation_laws/08_declare_war_vote.txt: declare-war federation laws, fileciteturn46file0L5-L51, fileciteturn46file0L54-L105, fileciteturn46file0L160-L222, fileciteturn47file0L4-L17

## G. Declaration scoring

- [ ] `AI_AGGRESSIVENESS_BASE` and personality `aggressiveness` are nonzero for warlike personalities.
- [ ] Boxed-in and no-colony multipliers are sane.
- [ ] `bravery` is high enough for intended target strength bands.
- [ ] `WAR_DECLARATION_MAX_DISTANCE` and malus defines fit map size.
- [ ] `WAR_DECLARATION_MINIMUM_SCORE` is not so high that all candidates fail.
- [ ] Fleet/economic relative power is high enough for desired wars.

Sources: Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI aggression defines, fileciteturn12file0L56-L61; Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: war declaration distance/score defines, fileciteturn9file0L99-L103; Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50

## H. War preparation and fleet behavior

- [ ] `AI_WAR_PREPARATION_MIN_MONTHS` and `MAX_MONTHS` support the intended pacing.
- [ ] AI shipyards can reinforce before the declaration window ends.
- [ ] `ENEMY_FLEET_POWER_MULT` allows offensive missions at intended odds.
- [ ] `MIN_FLEET_FOR_OPERATIONS` is not above normal early-game fleet power.
- [ ] Army production and `ENEMY_ARMY_POWER_MULT` allow invasions.
- [ ] War target priorities value claims, planets, starbases, and hostile fleets as intended.
- [ ] Repair/damaged thresholds do not create endless retreat loops.

Sources: Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI war preparation and war target defines, fileciteturn14file0L32-L58; Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: fleet confidence/mission defines, fileciteturn9file0L17-L19 and fileciteturn14file0L87-L106

## I. Test matrix before release

Run each test with observer mode and with temporary player control of the AI empire.

| Test | Expected result | Fail means |
|---|---|---|
| Adjacent conquest | Claim bought, `cb_claim`, `wg_conquest`, declaration | claim/legal/wargoal gate broken |
| Rival humiliation | Rivalry, `cb_humiliation`, `wg_humiliation` | relation/rivalry gate broken |
| Subjugation | CB only when actor stronger and target independent | relative power/subject gate broken |
| Ideology | Only liberation-wars non-gestalt ethics mismatch | policy/ethic gate broken |
| Total war | Paired total-war wargoal and no surrender | total-war condition pairing broken |
| Federation member | Vote follows law | federation setting broken |
| Subject | Independence/overlord special cases work | subject agreement/hardcoded gate broken |
| Large galaxy | Local wars still occur | distance/claim/economy scaling broken |

## J. Release safety rules

- [ ] Prefer additive files with unique objects over wholesale replacement.
- [ ] Patch known vanilla keys only when necessary.
- [ ] Keep at least one normal conquest, humiliation, subjugation, ideology, and total-war path available unless intentionally removing it.
- [ ] Never tune only `aggressiveness`; pair it with claims, CBs, wargoals, and fleet economy tests.
- [ ] Maintain a compatibility patch for every AI overhaul that edits personalities, economic plans, budgets, diplomatic actions, CBs, or wargoals.
