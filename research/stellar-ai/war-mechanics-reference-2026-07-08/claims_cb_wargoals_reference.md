# Claims, casus belli, and war-goal reference

## Key model

A legal war path is:

```text
claim or special condition
  -> casus_belli object valid or script-granted
  -> war_goal object references that CB
  -> war_goal potential and possible pass
  -> action_declare_war and hardcoded diplomacy pass
```

The gameplay wiki states the high-level rule: an empire needs a Casus Belli to start a war, and each CB grants access to one or more wargoals. Paradox Wiki Warfare page, CB/wargoal/claims overview and AI pre-war warning, citeturn609891view0 and citeturn609891view1

## Claims

### Legal claim rules

`common/game_rules/00_rules.txt` exposes `can_add_claim`. The file starts with a crucial caveat: tooltips are generated from these rules, but multiple hardcoded rules still apply; a true script rule does not guarantee the action is available, and a false script rule makes it unavailable. Public mirror HildoYe/game_files@e6d531, common/game_rules/00_rules.txt: can_add_claim rules and hardcoded caveat, fileciteturn49file0L3-L7 and fileciteturn49file0L29-L135

`can_add_claim` allows claims when at least one of the following is true:

- the claimer has `unrestricted_wars` policy;
- the system owner is gestalt;
- the owner is in a war where the owner is attacker and the claimer is defender.

It then blocks claims on invalid country types and several special cases, including normal empires claiming genocidal/assimilator threats and genocidal/assimilator empires claiming in incompatible ways. Public mirror HildoYe/game_files@e6d531, common/game_rules/00_rules.txt: can_add_claim rules and hardcoded caveat, fileciteturn49file0L3-L7 and fileciteturn49file0L29-L135

### AI claim scoring

The AI claim-scoring defines in the public mirror are:

| Define | Value | Meaning |
|---|---:|---|
| `MAX_CLAIM_DISTANCE` | 4 | Maximum jumps away AI will make claims on. |
| `MAX_CLAIM_DISTANCE_SUBJECT` | 2 | Subject claim range. |
| `CLAIM_BASE_VALUE` | 100 | Base claim target value. |
| `CLAIM_RESOURCE_FACTOR` | 2 | Resource-rich system factor. |
| `CLAIM_BYPASS_FACTOR` | 10 | Bypass value factor. |
| `CLAIM_RELATIONS_FACTOR` | -0.1 | Opinion/relations factor. |
| `CLAIM_COST_FACTOR` | -0.2 | Cost penalty; the vanilla comment appears copy-pasted, so trust the define name more than the comment. |
| `CLAIM_COLONY_FACTOR` | 25 | Colony value factor. |
| `CLAIM_BORDERING_FACTOR` | 100 | Bordering system value. |

Source: Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI claim scoring defines, fileciteturn9file0L49-L57

### Influence budget and claim starvation

Confirmed source-backed facts: claim scoring has defines, claim legality has game rules, and `claims_modifier` affects opinion penalty from claims rather than claim creation. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI claim scoring defines, fileciteturn9file0L49-L57; Public mirror HildoYe/game_files@e6d531, common/game_rules/00_rules.txt: can_add_claim rules and hardcoded caveat, fileciteturn49file0L3-L7 and fileciteturn49file0L29-L135; Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50

Inference: the AI’s ability to actually buy claims is also constrained by influence income, claim costs, other influence spending, budget priority, and hardcoded AI claim-purchase logic. In the researched script surfaces, there is no simple `personality.claim_desire` key equivalent to `military_spending`.

### What happens if AI wants war but has no claim or CB

It cannot use `wg_conquest` because `cb_claim` will not exist. It may still use humiliation, subjugation, ideology, despoliation, total-war, subject, secret-fealty, crisis, or event CBs if their separate prerequisites pass. If none pass, the desire gate stalls.

## Casus belli objects

The CB file schema comments define:

- `potential`: country-type/structural availability, scoped with attacker as `this` and defender as `from`;
- `is_valid`: evaluated daily for automatic CB creation/destruction and scoped attacker/root vs defender/from;
- `destroy_if`: removes script-granted CBs early;
- `show_notification`: notification behavior.

Source: Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: CB schema comments, fileciteturn22file0L3-L11

### Vanilla CB reference

| CB | File | Main prerequisites | Consumed by | Modding note |
|---|---|---|---|---|
| `cb_claim` | `common/casus_belli/00_casus_belli.txt` | Claim on target or target subject; no total-war CB; not in federation; not overlord-to-target; subject restrictions | `wg_conquest` | Main conquest path; claims are separate. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184 |
| `cb_subjugation` | same | Actor default/awakened; not in federation; actor not subject; target not subject; relative power above Equivalent unless awakened | `wg_subjugation`, `wg_tribute`, corporate variants | Relative power can destroy non-awakened CB if too weak. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184 |
| `cb_humiliation` | same | Rivalry or qualifying GC condition; not liberation-wars except gestalt target; no total-war CB; standard restrictions | `wg_humiliation` | Rivalry action refreshes this CB. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184 |
| `cb_ideology` | same | `liberation_wars`; non-gestalt; target default; ethics mismatch; no total-war CB | `wg_force_ideology` | Policy enabling/disabling refreshes validity. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184 |
| `cb_despoliation` | same | Barbaric Despoilers; no total-war CB; standard restrictions | `wg_plunder` | Wargoal has extra target colony/unclaimed-system checks. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: despoliation/raid/counterattack/allegiance/payback, fileciteturn22file0L239-L253, fileciteturn23file0L1-L16, fileciteturn23file0L126-L183, fileciteturn23file0L242-L296 |
| `cb_pirate_raid` | same | Corporate crusader spirit; no total-war CB; standard restrictions | `wg_plunder_raid` | Similar to despoliation. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: despoliation/raid/counterattack/allegiance/payback, fileciteturn22file0L239-L253, fileciteturn23file0L1-L16, fileciteturn23file0L126-L183, fileciteturn23file0L242-L296 |
| `cb_purification` | same | Berserk machine/Fanatic Purifier/Determined Exterminator; total-war CB present | `wg_cleansing` | Total war. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: total-war and special CBs, fileciteturn22file0L186-L237 and fileciteturn23file0L18-L112 |
| `cb_hunger` | same | Devouring Swarm; total-war CB present | `wg_absorption` | Total war. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: total-war and special CBs, fileciteturn22file0L186-L237 and fileciteturn23file0L18-L112 |
| `cb_sublimation` | same | Driven Assimilator; total-war CB present | `wg_assimilation` | Total war. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: total-war and special CBs, fileciteturn22file0L186-L237 and fileciteturn23file0L18-L112 |
| `cb_containment` | same | Target is awakened FE/Synth Queen/genocidal/assimilator threat; attacker default and not itself genocidal/assimilator; total-war CB present | `wg_end_threat*` | Defensive anti-threat total war. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: total-war and special CBs, fileciteturn22file0L186-L237 and fileciteturn23file0L18-L112 |
| `cb_colossus` | same | Actor has `tech_colossus`, `unrestricted_wars`, default country, target not federation, actor controls colossus, no total-war CB | `wg_colossus` | Requires actual colossus fleet. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: total-war and special CBs, fileciteturn22file0L186-L237 and fileciteturn23file0L18-L112 |
| `cb_stop_colossus` | same | Target has colossus; actor does not; no total-war CB | `wg_end_threat_colossus` | Anti-colossus total war. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: total-war and special CBs, fileciteturn22file0L186-L237 and fileciteturn23file0L18-L112 |
| `cb_subject` | same | Actor is subject, target is overlord | `wg_independence` | Subject path; paired wargoal. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: despoliation/raid/counterattack/allegiance/payback, fileciteturn22file0L239-L253, fileciteturn23file0L1-L16, fileciteturn23file0L126-L183, fileciteturn23file0L242-L296; Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: independence wargoal, fileciteturn24file0L5-L102 |
| `cb_allegiance` | same | Secret fealty from target subject; actor independent; not in target federation | Allegiance wargoals | Special Overlord path. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: despoliation/raid/counterattack/allegiance/payback, fileciteturn22file0L239-L253, fileciteturn23file0L1-L16, fileciteturn23file0L126-L183, fileciteturn23file0L242-L296 |
| `cb_counterattack`, `cb_renegade_containment` | same | Galactic Community resolutions and target war/membership conditions | Counterattack/containment wargoals | Resolution-dependent. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: despoliation/raid/counterattack/allegiance/payback, fileciteturn22file0L239-L253, fileciteturn23file0L1-L16, fileciteturn23file0L126-L183, fileciteturn23file0L242-L296 |

## War goals

A war goal references exactly one CB by object key and then adds additional availability and outcome logic.

### Common war-goal prerequisite chains

#### Conquest / claim war

```text
can_add_claim passes -> AI buys claim -> cb_claim valid -> wg_conquest possible -> action_declare_war passes
```

`wg_conquest` references `cb_claim`, blocks total-war CBs and some Galactic Emperor/Pax cases, allows status quo/surrender/demand surrender, and has AI weight 2. Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: conquest/humiliation wargoals, fileciteturn29file0L143-L291

**Failure modes.** Claim cannot be placed, claim range/value too low, influence unavailable, `cb_claim` blocked by total-war CB, target is federation ally/subject path, or wargoal blocked by Galactic Emperor/Pax rules.

#### Humiliation

```text
rivalry or GC condition -> cb_humiliation valid -> wg_humiliation possible -> action_declare_war
```

`wg_humiliation` references `cb_humiliation`, is a defender default, blocks all-claimed-target cases, emperor/Pax cases, and total war. AI weight is 1. Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: conquest/humiliation wargoals, fileciteturn29file0L143-L291

**Failure modes.** No valid rivalry, opinion too high to rival, target has no unclaimed colony system, or liberation-wars policy suppresses normal humiliation path.

#### Subjugation

```text
actor strong enough and target independent -> cb_subjugation -> wg_subjugation/tribute/corporate variant -> action_declare_war
```

`cb_subjugation` requires target not subject and relative power above Equivalent unless awakened FE. `wg_subjugation` then blocks inward perfection, corporate attackers for that specific goal, Become-the-Crisis, total-war CBs, all-claimed-target cases, Galactic Custodian/Emperor/declared-crisis targets, and Pax Galactica. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184; Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: plunder/subjugation/ideology wargoals, fileciteturn25file0L189-L258, fileciteturn26file0L135-L202, fileciteturn28file0L240-L298

**Failure modes.** Fleet/economy relative power is too low; target is already a subject; claims would destroy target; policy or galactic institutions block.

#### Ideology

```text
policy = liberation_wars -> ethics mismatch -> cb_ideology -> wg_force_ideology -> action_declare_war
```

`cb_ideology` requires non-gestalt attacker/target, `liberation_wars`, default target, no total-war CB, and an ethics mismatch. `wg_force_ideology` repeats policy and target checks and blocks all-claimed-target/emperor/Pax cases. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: cb_claim/cb_subjugation/cb_humiliation/cb_ideology, fileciteturn22file0L14-L184; Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: plunder/subjugation/ideology wargoals, fileciteturn25file0L189-L258, fileciteturn26file0L135-L202, fileciteturn28file0L240-L298

**Failure modes.** Gestalt, no ethics mismatch, policy not liberation wars, target would be fully destroyed by existing claims.

#### Despoliation / raiding

```text
Barbaric Despoilers or corporate crusader -> CB -> plunder/raid wargoal -> action_declare_war
```

`wg_plunder` and `wg_plunder_raid` both require target default colonies with at least one unclaimed colony system, block emperor/Pax cases, and apply raiding/resource effects on accept. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: despoliation/raid/counterattack/allegiance/payback, fileciteturn22file0L239-L253, fileciteturn23file0L1-L16, fileciteturn23file0L126-L183, fileciteturn23file0L242-L296; Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: plunder/subjugation/ideology wargoals, fileciteturn25file0L189-L258, fileciteturn26file0L135-L202, fileciteturn28file0L240-L298

**Failure modes.** All target colonies are claimed, target is invalid country type, or a total-war path suppresses normal CBs.

#### Total war / genocidal / containment / colossus

Total-war CBs and wargoals use paired attacker/defender goals. They usually set `total_war = yes`, allow only status quo, and set `surrender_acceptance = -1000`. Total wars auto-transfer occupied systems under gameplay rules and do not use normal surrender. Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: total-war wargoals, fileciteturn24file0L105-L230 and fileciteturn25file0L48-L187; Paradox Wiki Warfare page, CB/wargoal/claims overview and AI pre-war warning, citeturn609891view0 and citeturn609891view1

**Failure modes.** Missing civic/technology/colossus, target not in threat class, `has_total_war_cb` condition mismatched, emperor/Pax rules, or containment actor itself is excluded.

#### Crisis or special event wars

Event/origin CBs such as `cb_payback`, `cb_revenge_for_eaten_star`, and Galactic Community counterattack/renegade containment depend on flags, origins, event chains, or active resolutions. Public mirror HildoYe/game_files@e6d531, common/casus_belli/00_casus_belli.txt: despoliation/raid/counterattack/allegiance/payback, fileciteturn22file0L239-L253, fileciteturn23file0L1-L16, fileciteturn23file0L126-L183, fileciteturn23file0L242-L296

**Modding rule.** Event CBs are valid only if the granting flags/conditions survive daily validity checks or are script-granted with correct destroy rules.

#### Modded CBs and war goals

Minimum safe pattern:

```text
common/casus_belli/my_cb.txt
  my_cb = { potential = { ... } is_valid = { ... } }

common/war_goals/my_wg.txt
  my_wg = { casus_belli = my_cb potential = { ... } possible = { ... } ai_weight = { weight = ... } }
```

Then ensure `action_declare_war` hardcoded legality can still fire. A custom CB with no wargoal produces no useful declaration path; a custom wargoal whose CB is never granted is also inert.

## Failure-mode matrix

| Situation | Root cause | Fix |
|---|---|---|
| CB exists but no usable war goal | Wargoal `potential`/`possible` false, missing `casus_belli` reference, all AI weights zero | Inspect `common/war_goals`; add fail-text probes; test with player UI. |
| War goal exists but CB never granted | `is_valid` false, no script grant, missing policy/claim/rivalry | Inspect `common/casus_belli`, policies, claims, and flags. |
| AI has claim but cannot declare | `cb_claim` suppressed by total-war CB, federation/overlord/subject restriction, Pax/Emperor rule | Check CB validity and wargoal possible. |
| AI has fleet but no legal target | No CB path or diplomatic action blocked | Build a test target with forced claim/CB. |
| AI is aggressive but blocked | Aggression only affects desire | Do not tune aggression until legal chain is green. |
| Modded total-war CB suppresses normal wars | `has_total_war_cb` true causes normal CBs to fail | Scope total-war CB narrowly or add compatible war goals. |
| Subject never wars | Subject diplomacy terms / hardcoded vassal-overlord special case / CB subject rules | Test independence and overlord-target cases separately. |
