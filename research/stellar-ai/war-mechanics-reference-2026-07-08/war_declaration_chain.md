# Stellaris 4.4.x AI war declaration chain

**Purpose.** This document maps the chain from “an AI might want war” to “a war declaration actually happens” for a coding/modding agent. It is intentionally war-specific and assumes the reader already understands broad Stellaris AI layers such as economic plans, budgets, scripted weights, and events.

**Version and evidence note.** Values and object names marked “public mirror” come from a public `HildoYe/game_files` mirror at commit `e6d53157737d29324a41c6598a384af3b4091df1`. Treat these as a strong guide to PC 4.4.x script surfaces, but verify against the local 4.4.4 installation before shipping a mod. Paradox Wiki pages are cited for gameplay behavior, but the AI personalities page currently states it was verified for PC 4.2, so wiki-only claims are labelled as older wiki knowledge. The game rules file itself warns that several rules remain hard-coded in addition to script rules, so any “exact” chain necessarily includes hardcoded pieces. Public mirror HildoYe/game_files@e6d531, common/game_rules/00_rules.txt: can_add_claim rules and hardcoded caveat, fileciteturn49file0L3-L7 and fileciteturn49file0L29-L135

## Executive chain

An AI declaration is best modeled as a sequence of gates. Passing an early desire gate does not synthesize the later legal gates.

```text
active AI empire
  -> valid/current personality and diplomacy state
  -> war desire/target scan: aggressiveness, bravery, attitude, distance, relative power
  -> legal hostility path: claim OR non-claim CB OR total-war/special CB
  -> usable war goal tied to that CB and legal under policy/federation/subject/emperor rules
  -> action_declare_war possible/vote passes, plus hardcoded diplomatic validity
  -> AI war-preparation window and fleet positioning
  -> declaration fires
  -> separate military AI decides whether fleets attack, defend, invade, or stall
```

The most common modding error is raising `aggressiveness` or ship spending without ensuring that claims, CBs, war goals, policy flags, and action validity still exist.

## Gate 0 — Actor and global war eligibility

**Required definitions and files.** The actor must be a country type that can use the relevant CB, war goal, and diplomacy action. Regular, fallen, and awakened empires are referenced by many vanilla war surfaces; individual CBs often narrow this further. The public mirror also exposes `NO_WARS_FLAG = "ai_no_wars"`, a hard stop used by AI/scripted control surfaces. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: NO_WARS_FLAG/NO_LEAVE_FED_FLAG, fileciteturn9file0L59-L60

**Relevant paths.**

- `common/defines/00_defines.txt`: `NO_WARS_FLAG`, declaration and war-AI defines.
- `common/casus_belli/00_casus_belli.txt`: per-CB `potential`, `is_valid`, `destroy_if`.
- `common/war_goals/00_war_goals.txt`: per-wargoal `potential`, `possible`, `ai_weight`, effects.
- `common/diplomatic_actions/00_actions.txt`: `action_declare_war`.
- `common/game_rules/00_rules.txt`: claim/rival rules and explicit warning that hardcoded rules also apply.

**Consumed by.** Engine diplomacy, AI country strategy, and war-declaration candidate scanning.

**Modding control.** Modders can override script definitions and set/clear flags through events/effects, but cannot fully replace the engine’s candidate scan or all diplomatic hardcoded rules from script alone.

**In-game failure.** No declaration occurs; player-facing UI may show missing diplomatic action, hidden/greyed war goal, “no casus belli”, failed claim tooltip, or no obvious UI if the blocked actor is an AI.

## Gate 1 — Active personality creates war pressure, not war legality

Personality comments in `common/personalities/00_personalities.txt` define the direct war-relevant fields. `aggressiveness` affects declaration chance, insult chance, and fleet power committed to offense; `bravery` affects willingness to pick rivals and war targets of similar strength; `military_spending` affects navy/army resource budgets; `claims_modifier` affects the opinion penalty from claims, not claim creation desire. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50

`AI_AGGRESSIVENESS_BASE = 25` is the base chance the AI will declare a war, multiplied by personality aggressiveness. Boxed-in and no-colony multipliers can raise this pressure: `AI_AGGRESSIVENESS_PROPAGATOR_BOXED_IN_MULT = 10`, `AI_AGGRESSIVENESS_BOXED_IN_MULT = 4`, and `AI_AGGRESSIVENESS_NO_COLONY_TARGET_MULT = 2`. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI aggression defines, fileciteturn12file0L56-L61

**Important limit.** Aggressiveness does not grant claims, bypass policies, create CBs, or make impossible war goals possible. It only helps the AI choose to use a legal path that already exists.

**Target-strength interaction.** Script comments say bravery controls picking rivals and war targets of similar strength. The Paradox Wiki adds older-version thresholds: at 0.5 and below, an empire cannot declare war on Equivalent empires; at 1.5 and above it can declare war on Superior empires; at 2.5 and above it can declare war on Overwhelming empires. Treat the exact thresholds as older wiki knowledge unless verified against local 4.4.4 code. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50; Paradox Wiki AI personalities page, verified for PC 4.2, behavior modifier descriptions and bravery thresholds, citeturn509366view0

**In-game failure.** AI may build fleets and sit at peace because the desire gate is low, because the AI lacks negative attitude/target score, or because a later legality gate fails.

## Gate 2 — Diplomatic attitude, rivalry, and target scoring

Aggressiveness is applied to enemies the AI is willing to consider. The wiki states aggressiveness affects declaring wars against empires with negative Attitude; that statement is useful but comes from a page verified for PC 4.2, so validate any exact behavior in 4.4.4. Paradox Wiki AI personalities page, verified for PC 4.2, behavior modifier descriptions and bravery thresholds, citeturn509366view0

Rivalry matters because `cb_humiliation` requires rivalry or qualifying Galactic Community resolution/denouncement conditions. The script action `action_make_rival` is auto-accepted but has diplomatic prerequisites such as purifier/swarm/terminator/inward-perfection restrictions and a relation/supremacist/harming-relations requirement; on accept it calls `check_casus_belli_valid` for `cb_humiliation`. Public mirror HildoYe/game_files@e6d531, common/diplomatic_actions/00_actions.txt: action_make_rival, fileciteturn35file0L45-L167

The `is_valid_rival` game rule constrains regular rival validity by relative power: target relative power must be at least inferior and no more than superior unless the rivaling country has the animosity diplomatic stance; the file also states hardcoded rules can still apply. Public mirror HildoYe/game_files@e6d531, common/game_rules/00_rules.txt: is_valid_rival, fileciteturn49file0L8-L27

**Distance gate.** Declaration candidates are distance-capped and distance-multiplied by defines: `WAR_DECLARATION_MAX_DISTANCE = 50`, `WAR_DECLARATION_MALUS_DISTANCE = 25`, `WAR_DECLARATION_MALUS = 0.05`, and `WAR_DECLARATION_MINIMUM_SCORE = 0.5`. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: war declaration distance/score defines, fileciteturn9file0L99-L103

**In-game failure.** AI is aggressive on paper but never selects distant or diplomatically friendly targets; an apparent target may be outside max distance or below the post-distance score floor.

## Gate 3 — Claim path must exist for conquest wars

For ordinary conquest, the AI needs claims or claims on a target subject. `cb_claim` is valid only if the attacker has a claim on the target or on a target subject, has no total-war CB, is not overlord to the target, and is not blocked by subject/overlord restrictions. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184

The claim system has both **legal claim rules** and **AI claim scoring**:

- Legal claim rules live in `common/game_rules/00_rules.txt` under `can_add_claim`. Claims generally require unrestricted wars, claiming a gestalt owner, or a defensive-war exception; the rule also blocks invalid country types and several genocidal/assimilator cases. Public mirror HildoYe/game_files@e6d531, common/game_rules/00_rules.txt: can_add_claim rules and hardcoded caveat, fileciteturn49file0L3-L7 and fileciteturn49file0L29-L135
- AI claim scoring has defines: max claim distance 4 jumps for normal empires and 2 for subjects, plus base/resource/bypass/relation/cost/colony/bordering factors. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI claim scoring defines, fileciteturn9file0L49-L57
- Gameplay cost rules are summarized on the warfare wiki: claims have a base influence cost and distance/starbase/colony/offensive-war/rival modifiers; that page is gameplay-facing, so verify exact costs if your mod changes claim costs. Paradox Wiki Warfare page, CB/wargoal/claims overview and AI pre-war warning, citeturn609891view0 and citeturn609891view1

**What modders can safely tune.** You can tune claim scoring distance/value through defines and reduce claim costs or increase influence availability. You should not expect `claims_modifier` to make the AI place more claims; the script comment says it affects opinion penalty from claims. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50

**In-game failure.** AI has high aggression and fleets but no `cb_claim`; the diplomacy UI says no CB, conquest war goal is not available, or AI keeps spending influence elsewhere and never claims.

## Gate 4 — Casus belli must be valid

`common/casus_belli/00_casus_belli.txt` provides the CB schema. `potential` limits country types; `is_valid` is evaluated daily to create or destroy automatic CBs and is scoped as attacker/root versus defender/from; `destroy_if` is for script-granted CB cleanup. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: CB schema comments, fileciteturn22file0L3-L11

Core vanilla chains:

| War family | CB object | Key prerequisites | Notes |
|---|---|---|---|
| Conquest | `cb_claim` | Existing claim on target or target subject; no total-war CB; not in federation with target; subject/overlord restrictions | Used by `wg_conquest`. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184 |
| Subjugation | `cb_subjugation` | Actor default/awakened; not federation with target; actor not subject; target not subject; relative power above Equivalent unless awakened FE | If power falls below Superior, non-awakened CB can be destroyed. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184 |
| Humiliation | `cb_humiliation` | Rivalry or qualifying GC resolution; no total-war CB; not liberation-wars except gestalt target path | Rivalry action refreshes this CB. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184; Public mirror HildoYe/game_files@e6d531, common/diplomatic_actions/00_actions.txt: action_make_rival, fileciteturn35file0L45-L167 |
| Ideology | `cb_ideology` | `liberation_wars` policy, non-gestalt attacker/target, ethics mismatch, no total-war CB | Policy enabling/disabling calls `check_casus_belli_valid`. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184; Public mirror HildoYe/game_files@e6d531, common/policies/00_policies.txt: war_philosophy, unrestricted/liberation/no_wars, fileciteturn21file0L21-L48 and fileciteturn20file0L16-L68, fileciteturn20file0L71-L154 |
| Despoliation / raid | `cb_despoliation`, `cb_pirate_raid` | Barbaric Despoilers or corporate crusader civic; no total war; standard subject/overlord restrictions | War goals also require target has at least one unclaimed colony system. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: despoliation/raid/counterattack/allegiance/payback, fileciteturn22file0L239-L253, fileciteturn23file0L1-L16, fileciteturn23file0L126-L183, fileciteturn23file0L242-L296; Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: plunder/subjugation/ideology wargoals, fileciteturn25file0L189-L258, fileciteturn26file0L135-L202, fileciteturn28file0L240-L298 |
| Total-war threats | `cb_purification`, `cb_hunger`, `cb_sublimation`, `cb_containment`, `cb_colossus`, `cb_stop_colossus` | Genocidal/assimilator/colossus/containment conditions; often require `has_total_war_cb` yes/no appropriately | Total-war CBs suppress many normal CBs. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: total-war and special CBs, fileciteturn22file0L186-L237 and fileciteturn23file0L18-L112 |
| Subject / secret fealty / events | `cb_subject`, `cb_allegiance`, `cb_payback`, event CBs | Subject-overlord, secret fealty, origin, event flags | Often paired or event-driven. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: despoliation/raid/counterattack/allegiance/payback, fileciteturn22file0L239-L253, fileciteturn23file0L1-L16, fileciteturn23file0L126-L183, fileciteturn23file0L242-L296; Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: independence wargoal, fileciteturn24file0L5-L102 |

**In-game failure.** A target looks hostile, but no CB is generated. For AI debugging, check actual `has_casus_belli` state, not just personality or relations.

## Gate 5 — A usable war goal must exist and pass `potential` + `possible`

A CB is not enough. Each usable war goal in `common/war_goals/00_war_goals.txt` must reference the CB and pass its own `potential` and `possible` triggers. The warfare wiki summarizes this at gameplay level: a CB grants access to at least one wargoal, and the war is declared with a wargoal. Paradox Wiki Warfare page, CB/wargoal/claims overview and AI pre-war warning, citeturn609891view0 and citeturn609891view1

Examples:

- `wg_conquest` uses `casus_belli = cb_claim`, has `hide_if_no_cb = no`, blocks total-war CBs, blocks some Galactic Emperor cases, and blocks Pax Galactica. Its AI weight is only 2, so modded extra wargoals can easily outcompete it. Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: conquest/humiliation wargoals, fileciteturn29file0L143-L291
- `wg_humiliation` uses `cb_humiliation`, has `defender_default = yes`, rejects cases where the target has no unclaimed colony system, and has AI weight 1. Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: conquest/humiliation wargoals, fileciteturn29file0L143-L291
- `wg_force_ideology` uses `cb_ideology`, requires `liberation_wars`, blocks total-war and emperor/Pax cases, and has AI weight 5. Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: plunder/subjugation/ideology wargoals, fileciteturn25file0L189-L258, fileciteturn26file0L135-L202, fileciteturn28file0L240-L298
- `wg_subjugation` uses `cb_subjugation`, excludes inward perfection on either side, corporate attackers, become-the-crisis, total-war CBs, full-claim destruction cases, Galactic Custodian/Emperor/declared-crisis targets, and Pax Galactica. Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: plunder/subjugation/ideology wargoals, fileciteturn25file0L189-L258, fileciteturn26file0L135-L202, fileciteturn28file0L240-L298
- Total-war wargoals set `total_war = yes`, usually allow only status quo, and set `surrender_acceptance = -1000`. Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: total-war wargoals, fileciteturn24file0L105-L230 and fileciteturn25file0L48-L187

**Modding control.** Modders can add or override wargoals, but every new wargoal needs an existing or script-granted CB path, complete localization, sane `ai_weight`, and defensive/default behavior where relevant.

**In-game failure.** CB exists but Declare War has no usable wargoal; a wargoal appears hidden or greyed with fail text such as `has_claimed_all_systems`, `cannot_use_against_emperor`, or `pax_galactica_active`.

## Gate 6 — War philosophy and policy gates

`war_philosophy` is a policy group, not a personality key in the public 4.4.x personality file. It has `allow = { is_at_war = no }`, so empires cannot change it while already at war. Public mirror HildoYe/game_files@e6d531, common/policies/00_policies.txt: war_philosophy, unrestricted/liberation/no_wars, fileciteturn21file0L21-L48 and fileciteturn20file0L16-L68, fileciteturn20file0L71-L154

The three main options are:

- `unrestricted_wars`: gives `policy_flags = { unrestricted_wars }`; invalid for pacifists, fanatic pacifists, inward perfection, and crusader spirit. AI weight is strongly boosted for AI personalities with `conqueror`, `subjugator`, or `purger`, and for Become the Crisis; certain Rules of War resolutions reduce AI weight. Public mirror HildoYe/game_files@e6d531, common/policies/00_policies.txt: war_philosophy, unrestricted/liberation/no_wars, fileciteturn21file0L21-L48 and fileciteturn20file0L16-L68, fileciteturn20file0L71-L154
- `liberation_wars`: gives `policy_flags = { liberation_wars }`; invalid for fanatic pacifists and fanatic purifiers, non-gestalt only; enabling/disabling refreshes `cb_ideology`. Public mirror HildoYe/game_files@e6d531, common/policies/00_policies.txt: war_philosophy, unrestricted/liberation/no_wars, fileciteturn21file0L21-L48 and fileciteturn20file0L16-L68, fileciteturn20file0L71-L154
- `no_wars`: gives `policy_flags = { no_wars }`; invalid for fanatic militarists, fanatic purifiers, devouring swarms, machine terminators, and crusader spirit; AI weight is essentially fanatic-pacifist only. Public mirror HildoYe/game_files@e6d531, common/policies/00_policies.txt: war_philosophy, unrestricted/liberation/no_wars, fileciteturn21file0L21-L48 and fileciteturn20file0L16-L68, fileciteturn20file0L71-L154

**In-game failure.** AI is aggressive but has `no_wars` or `liberation_wars`; conquest claims and CBs fail, ideology may be the only legal normal path, or no legal war exists.

## Gate 7 — `action_declare_war` and federation/subject voting

The diplomacy action schema supports `potential`, `possible`, `proposable`, `ai_acceptance`, voting requirements, independence requirements, and action settings. Its comments explicitly warn that `ai_acceptance` does not overwrite hardcoded reasons. Public mirror HildoYe/game_files@e6d531, common/diplomatic_actions/00_actions.txt: diplomatic-action schema comments, fileciteturn32file0L3-L26

`action_declare_war` in the public mirror is script-light but important:

- usable by regular, fallen, and awakened empires;
- `requires_actor_independence = no`, with a comment that the vassal-overlord special case is handled in code;
- `requires_recipient_independence = no`;
- `requires_alliance_vote = yes`, `requires_unanimous_vote = yes` by default;
- `auto_accepted = yes` and `action_type = aggressive`;
- `possible` blocks declaring on a recipient subject of a federation ally and blocks Fallen Empire cases during Synth Queen state. Public mirror HildoYe/game_files@e6d531, common/diplomatic_actions/00_actions.txt: action_declare_war object, fileciteturn45file0L108-L144

Federation laws modify `action_declare_war` settings via `set_diplomacy_action_setting`: unanimous vote, majority vote, or leader vote, with law cooldowns, centralization requirements, and AI weights. Public mirror HildoYe/game_files@e6d531, common/federation_laws/08_declare_war_vote.txt: declare-war federation laws, fileciteturn46file0L5-L51, fileciteturn46file0L54-L105, fileciteturn46file0L160-L222, fileciteturn47file0L4-L17

**Hardcoded part.** The declare-war action does not contain the whole war legality chain. CB selection, wargoal selection, subject special cases, truce/non-aggression/defensive arrangements, active wars, and other diplomatic blockers are partly engine-handled. Do not assume that patching `action_declare_war.possible` is sufficient or safe.

**In-game failure.** AI has a CB/wargoal but cannot pass federation vote, cannot legally attack a subject/overlord arrangement, or is blocked by a hardcoded diplomatic restriction.

## Gate 8 — Preparation timer and declaration score

The public mirror defines `AI_WAR_PREPARATION_MIN_MONTHS = 12` and `AI_WAR_PREPARATION_MAX_MONTHS = 30`. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI war preparation and war target defines, fileciteturn14file0L32-L58

The warfare wiki says that when AI is about to declare war it first moves fleets toward the target border and targets with military intel may receive a warning; use this as gameplay-facing/older-wiki evidence, not a script guarantee. Paradox Wiki Warfare page, CB/wargoal/claims overview and AI pre-war warning, citeturn609891view0 and citeturn609891view1

Distance and score defines determine whether the declaration candidate remains viable after scoring. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: war declaration distance/score defines, fileciteturn9file0L99-L103

**In-game failure.** AI appears to posture at the border, then the target changes, a legality gate changes, a defensive pact/federation state changes, the fleet-confidence check fails, or the preparation window expires without a declaration.

## Gate 9 — Fleet use after war starts is separate from declaring war

Post-declaration military behavior is controlled by a different set of defines and hardcoded fleet assignment logic:

- `ENEMY_FLEET_POWER_MULT = 1.2`: AI needs enemy fleet power multiplied by this to become offensive in an offensive war.
- `ENEMY_ARMY_POWER_MULT = 1.0`: army power threshold for landing armies.
- `MIN_FLEET_FOR_OPERATIONS = 500`: minimum fleet power to assign to attack/operation missions.
- `OFFENSE_VS_DEFENSE_STRATEGY_ALLOTMENT = 1.0`: how much fleet power a 1.0-aggressiveness country tries to commit to offense.
- War target priorities include borders, claims, planets, starbases, hostile fleets, and chokepoints. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: fleet confidence/mission defines, fileciteturn9file0L17-L19 and fileciteturn14file0L87-L106; Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI war preparation and war target defines, fileciteturn14file0L32-L58

This means “declares war” and “attacks effectively” are different systems. A mod can fix the first and still produce passive wars if fleet confidence, transport army logic, damaged thresholds, access paths, or target scoring are wrong.

## What modders can add, override, or only influence

| Surface | Can add? | Can override? | Usually only indirect? | Notes |
|---|---:|---:|---:|---|
| Personality objects | Yes | Yes | No | Highest-weight active personality wins; overwrite conflicts are common. |
| Personality fields | Limited to known keys | Yes | No | Unknown keys are ignored. `behaviour` is the vanilla spelling. |
| War philosophy policies | Yes, with care | Yes | No | Policy flags are consumed by CB/claim rules. |
| Claims scoring defines | No new define behavior | Yes | Partly | Claim budget/influence allocation remains partly AI/economy/hardcoded. |
| CB objects | Yes | Yes | No | Need `is_valid`/script grants and matching war goals. |
| War goals | Yes | Yes | No | Need matching CB, `possible`, `potential`, and sane `ai_weight`. |
| `action_declare_war` | Not as a new core action | Yes, high risk | Partly | The action is script-light; much is hardcoded. |
| Federation laws | Yes | Yes | No | They mutate `action_declare_war` vote settings. |
| Fleet operations | Defines/scripted weights partly | Yes | Mostly | Mission assignment remains engine AI. |

## In-game failure signatures by gate

| Gate | Typical symptom | Most likely file to inspect first |
|---|---|---|
| Actor/global | Empire never declares any wars | `defines/00_defines.txt`, flags/events, country type |
| Personality/desire | Only some personalities fight | `common/personalities/00_personalities.txt` active winning object |
| Attitude/rivalry | No humiliation CB; no insults/rivalries | `common/diplomatic_actions/00_actions.txt`, `common/game_rules/00_rules.txt` |
| Claims | No conquest CB despite claims-focused personality | `common/game_rules/00_rules.txt`, claim defines, influence economy |
| CB | “No casus belli” | `common/casus_belli/00_casus_belli.txt` |
| Wargoal | CB exists but war goal hidden/greyed | `common/war_goals/00_war_goals.txt` |
| Policy | Pacifist/liberation/no-wars passive behavior | `common/policies/00_policies.txt` |
| Federation/subject | Target legally protected or vote never passes | `common/federation_laws/08_declare_war_vote.txt`, `action_declare_war` |
| Scoring/distance | Far empires never attacked | declaration distance defines |
| Fleet confidence | War declared but no offensive movement | fleet confidence and target mission defines |

## Minimal test harness for a modded AI

Create three controlled empires in a small test galaxy:

1. **Conquest path:** militarist/conqueror AI, adjacent target, unrestricted wars, enough influence, one claim on a colonized target system, no pacts, no federation. Expected: `cb_claim` then `wg_conquest` then declaration after prep.
2. **Non-claim path:** rival target with bad relations and no claims. Expected: `cb_humiliation` then `wg_humiliation` if policy/target rules pass.
3. **Total-war path:** purifier/swarm/terminator/assimilator or containment target. Expected: paired total-war CB/wargoal and immediate ownership transfer on occupation after war start.

If any test fails, inspect the highest failed gate first; do not tune aggression until the legal path is confirmed.
