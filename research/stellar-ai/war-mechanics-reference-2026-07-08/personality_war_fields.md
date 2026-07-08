# Personality war fields reference

**Scope.** Vanilla personality objects are in `common/personalities/00_personalities.txt`. The public mirror uses the British spelling `behaviour = { ... }`. Some older docs and human descriptions say “behavior”; for a mod file, use the spelling used by the target vanilla file unless you have tested alias support.

**Version note.** Script comments and examples below come from the public 4.4.x mirror; wiki-only details such as exact bravery thresholds are older wiki knowledge because the AI personalities page states it was verified for PC 4.2. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50; Paradox Wiki AI personalities page, verified for PC 4.2, behavior modifier descriptions and bravery thresholds, citeturn509366view0

## Field summary table

| Field | Vanilla examples | Direct effect | Increasing | Decreasing | Zero or missing | War-declaration role | Limits |
|---|---:|---|---|---|---|---|---|
| `aggressiveness` | Honorbound 1.75; Zealot 1.25; Erudite 0.75 | War-declaration chance, insult chance, offensive fleet allotment | More target attempts and more offensive fleet commitment | Fewer declarations and less offensive commitment | Missing defaults to norm per wiki table; at 0, script comment says 50% fleet power still committed to offense, but war-declaration multiplier likely collapses normal desire | Direct desire and fleet stance | Does not create claims/CBs/wargoals or bypass policy. |
| `bravery` | Honorbound 1.5; Zealot 1.0; Erudite 0.75 | Rival/war target strength tolerance | Will consider stronger targets | Picks weaker targets only | Very low values avoid Equivalent+ targets; exact thresholds from 4.2 wiki | Target selection | Does not increase fleet power or legal access. |
| `combat_bravery` | Honorbound 2.0; Zealot 1.0 | Retreat willingness in combat | Fewer retreats | More retreats | Low/0 likely extremely cautious; exact curve hardcoded | Combat behavior | Does not affect declaration desire. |
| `military_spending` | Honorbound 1.2; Zealot 1.1; Erudite 0.9 | Mineral/energy budget for navies and armies | Builds/maintains more ships and armies if economy supports it | Underbuilds forces | Missing defaults to norm; 0 risks no military budget | Indirect fleet confidence | Does not force war or claims. |
| `claims_modifier` | Honorbound 2.0; Zealot 1.5; Erudite 1.0 | Opinion penalty from claims | More negative reaction to others’ claims | Less claim-driven opinion friction | 0 suppresses this opinion penalty | Indirect relations/attitude | Does not make AI place claims. |
| `threat_modifier` | Honorbound 0.75; Zealot 0.9; Erudite 1.2 | Threat concern/opinion scaling | More threat reaction | Less threat reaction | 0 suppresses threat concern | Indirect target/cooperation | Does not create CB. |
| `friction_modifier` | Honorbound 1.0; Zealot 1.2; Erudite 0.5 | Border friction opinion | More negative border friction | Less friction | 0 suppresses border-friction penalty | Indirect attitude/relations | Needs borders and opinion systems. |
| `trade_willingness` | Honorbound 0.7; Zealot 0.75; Erudite 0.9 | Trade acceptance fairness | More willing to trade | Less willing | Low values reduce deals | Indirect: pacts, trust, resources | Not war-specific. |
| `federation_acceptance` | Honorbound 0; Erudite 0 | Federation proposal acceptance modifier | More alliance/federation formation | Less | 0 neutral | Indirect: federations can block/route wars through votes | Does not by itself choose targets. |
| `nap_acceptance` | Honorbound -100; Erudite 5 | Non-aggression pact acceptance | More NAPs, fewer possible wars | Fewer NAPs | 0 neutral | Indirect hard block via NAPs | Needs action validity. |
| `defensive_pact_acceptance` | Honorbound 20; Erudite 5 | Defensive pact acceptance | More mutual defense webs | Fewer pacts | 0 neutral | Indirect: makes targets riskier/protected | Does not affect own declaration desire except via diplomacy. |
| `weapon_preferences` | Strike craft / kinetic / energy | Ship design preference | More of preferred weapon if valid | N/A | Missing uses AI design defaults | Combat effectiveness | Ignored/adapted against extreme enemy designs per wiki. |
| `armor_ratio`, `shields_ratio`, `hull_ratio` | Honorbound 0.4/0.4/0.2; Erudite 0.3/0.7/0.0 | Utility slot distribution | More of that defense | Less of that defense | 0 means none targeted for that layer | Combat survivability | Does not choose wars. |
| `behaviour.conqueror` | Honorbound yes; Zealot yes; Erudite yes | Personality intent flag | Enables conquest-favoring policy/logic | Less conquest | no/absent disables that behavior | Indirect through policies/wargoal preferences | Does not grant CB. |
| `behaviour.subjugator` | Honorbound yes; Erudite yes | Subjugation preference | More subjugation path | Less | no/absent disables | Indirect policy/wargoal preference | Needs `cb_subjugation`. |
| `behaviour.liberator` | Often no in examples | Liberation preference | More ideology/liberation weights | Less | no/absent disables | Indirect via `liberation_wars` AI_weight | Needs policy + `cb_ideology`. |
| `behaviour.opportunist` | Zealot yes; Erudite yes | Preference for targets already at war | More opportunistic targets | Less | no/absent disables | Target scoring | Does not bypass strength/legal checks. |
| `behaviour.propagator` | Commented as boxed-in aggressor behavior | Boxed-in warlike personality multiplier | Very aggressive once boxed in | Less | no/absent no special multiplier | Desire multiplier via define | Needs legal targets. |
| `war_philosophy` | Not found as a personality key in public mirror | Policy group, not personality field | See policies | See policies | N/A | Legal claim/CB path | Do not add as personality key expecting effect. |

Sources: Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50; Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: honorbound/zealot/explorer examples, fileciteturn17file0L57-L85, fileciteturn17file0L127-L155, fileciteturn17file0L219-L247; Public mirror HildoYe/game_files@e6d531, common/policies/00_policies.txt: war_philosophy, unrestricted/liberation/no_wars, fileciteturn21file0L21-L48 and fileciteturn20file0L16-L68, fileciteturn20file0L71-L154

## `aggressiveness`

The vanilla comment is unusually explicit: aggressiveness affects war declaration chance, insult chance, and the percentage of fleet power committed to offense. It states that at 0, 50% is committed; at 1, roughly 75%; at 2, 100%; higher values continue to count for war declaration and insults. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50

`AI_AGGRESSIVENESS_BASE = 25` is multiplied by personality aggressiveness. Game-setting multipliers and boxed-in multipliers then modify the pressure. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI aggression defines, fileciteturn12file0L56-L61

**Increase effect.** More frequent war/insult attempts and larger offensive fleet allocation. Use with valid claims/CBs/wargoals or it will only produce frustrated desire.

**Decrease effect.** Fewer offensive decisions and more fleet kept defensive. This can be desirable for builder, isolationist, or crisis-fighter behavior.

**Zero effect.** The file comment says offense allocation does not drop below 50% at 0, but war-declaration desire is likely minimal because base chance is multiplied by aggressiveness. Treat “zero aggression still may fight defensive/special wars” as inference because engine behavior can bypass the normal desire loop.

**Cannot do.** It cannot generate claims, choose a war goal with `ai_weight = 0`, ignore truce/federation votes, or override `no_wars` policy.

## `bravery`

The vanilla comment says bravery affects rival and war-target strength selection. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50 The wiki adds exact thresholds: 0.5 and below cannot declare war on Equivalent empires, 1.5 and above can declare war on Superior empires, and 2.5 and above can declare war on Overwhelming empires; because the wiki page is verified for PC 4.2, validate those thresholds in 4.4.4 before using them as a hard balance promise. Paradox Wiki AI personalities page, verified for PC 4.2, behavior modifier descriptions and bravery thresholds, citeturn509366view0

**Increase effect.** AI accepts more even or unfavorable relative-power wars, so distant/strong targets are less filtered by risk.

**Decrease effect.** AI picks on inferior targets and avoids peer wars.

**Cannot do.** Bravery is not fleet power. If ship building, economy, or naval cap is broken, bravery only makes the AI willing to choose fights it cannot prosecute.

## `combat_bravery`

`combat_bravery` appears in vanilla personalities but is not listed in the top modifier comments except by example; the wiki describes combat bravery as retreat behavior and says at 1.0 an empire attempts retreat after losing 50% of its fleet. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: honorbound/zealot/explorer examples, fileciteturn17file0L57-L85, fileciteturn17file0L127-L155, fileciteturn17file0L219-L247; Paradox Wiki AI personalities page, verified for PC 4.2, behavior modifier descriptions and bravery thresholds, citeturn509366view0

**Role.** Combat behavior after fleets engage, not declaration.

**Risk.** Raising it can make AI fleets die instead of disengaging; lowering it can make AI abandon fights and stall offensives.

## `military_spending`

The script comment says this affects mineral and energy budget allocated to navies and armies. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50

**Increase effect.** More ships/armies if the economic plan can produce alloys, energy, naval cap, shipyards, and upkeep.

**Decrease effect.** Smaller fleets and lower army readiness, which indirectly lowers war confidence.

**Zero/missing.** Missing defaults to normal per the wiki’s personality table rule; zero risks starving fleets/armies even with high aggression. Paradox Wiki AI personalities page, verified for PC 4.2, behavior modifier descriptions and bravery thresholds, citeturn509366view0

**Cannot do.** It does not declare war. It merely changes resources available for later fleet-confidence and invasion checks.

## `claims_modifier`

The script comment says `claims_modifier` affects opinion penalty from claims. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50 It should be treated as **claim concern**, not claim placement desire.

**Increase effect.** AI becomes more angered by others’ claims, worsening relations and potentially creating negative attitude.

**Decrease/zero effect.** Claims stop mattering as much diplomatically; a galaxy can become friendlier even if claims exist.

**Cannot do.** It does not increase number of claims made, claim range, or influence budget.

## `threat_modifier`, `threat_others_modifier`, and `friction_modifier`

The personality file says `threat_modifier` affects how much threat is generated for this empire when others are conquered; `threat_others_modifier` affects how much threat is generated for others when this empire is conquered; `friction_modifier` affects border friction. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50 Define-level threat decay, distance, size, and NAP modifiers exist separately. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: threat defines, fileciteturn12file0L37-L55

**War role.** These fields alter opinion and attitude, which indirectly influence rivalry, pacts, target selection, and war desire.

**Failure mode.** Over-lowering all of them can make even militarist empires maintain neutral/good relations; high aggression then has no hostile diplomatic context to act on.

## Diplomacy acceptance fields

The personality file defines acceptance additions for federations, non-aggression pacts, commercial pacts, research agreements, migration pacts, defensive pacts, and loyalty. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50

**War role.** They are indirect but important:

- High `nap_acceptance` creates non-aggression pacts that block war until broken and any truce/cooldown resolves.
- High `defensive_pact_acceptance` creates defense webs that make targets stronger and can deter or redirect wars.
- High `federation_acceptance` pushes wars through federation vote laws rather than direct declarations.
- Research/commercial/migration pacts raise trust and relations, often making negative attitude less likely.

**Cannot do.** These fields do not directly choose war goals.

## `behaviour = { ... }` flags

The top-of-file comments list flags such as `conqueror`, `subjugator`, `liberator`, `opportunist`, `slaver`, `purger`, `propagator`, `crisis_fighter`, and `sneak_attacker`. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50

Key war interactions:

- `conqueror`, `subjugator`, and `purger` strongly boost AI weight for `unrestricted_wars`. Public mirror HildoYe/game_files@e6d531, common/policies/00_policies.txt: war_philosophy, unrestricted/liberation/no_wars, fileciteturn21file0L21-L48 and fileciteturn20file0L16-L68, fileciteturn20file0L71-L154
- `conqueror`, `subjugator`, and `liberator` boost AI weight for `liberation_wars`. Public mirror HildoYe/game_files@e6d531, common/policies/00_policies.txt: war_philosophy, unrestricted/liberation/no_wars, fileciteturn21file0L21-L48 and fileciteturn20file0L16-L68, fileciteturn20file0L71-L154
- `propagator` interacts with `AI_AGGRESSIVENESS_PROPAGATOR_BOXED_IN_MULT = 10`. Public mirror HildoYe/game_files@e6d531, common/defines/00_defines.txt: AI aggression defines, fileciteturn12file0L56-L61
- `wants_tribute` appears in wargoal AI weights for subjugation/tribute even though it is not listed in the top behavior comment block; verify the full local personality file if using it in a replacement personality set. Public mirror HildoYe/game_files@e6d531, common/war_goals/00_war_goals.txt: plunder/subjugation/ideology wargoals, fileciteturn25file0L189-L258, fileciteturn26file0L135-L202, fileciteturn28file0L240-L298

## Ship design fields

`weapon_preferences`, `armor_ratio`, `shields_ratio`, `hull_ratio`, and `ship_roles` influence ship design. Public mirror HildoYe/game_files@e6d531, common/personalities/00_personalities.txt: behavior/modifier comments, fileciteturn17file0L3-L50 The wiki states these preferences are ignored if the AI faces an enemy heavily focused on a weapon or defense type. Paradox Wiki AI personalities page, verified for PC 4.2, behavior modifier descriptions and bravery thresholds, citeturn509366view0

**War role.** They change actual combat performance, which can feed back into relative fleet confidence and outcomes. They do not affect declaration legality.

**Passive-galaxy risk.** Invalid or badly weighted designs can make the AI appear to build fleets while having low real combat value, causing bravery/fleet-confidence checks or post-war mission checks to fail.

## `war_philosophy` is not a personality key in this source set

A search of the public mirror located `war_philosophy` in policies/events/effects, not in `common/personalities/00_personalities.txt`. Treat it as a policy group in `common/policies/00_policies.txt`. Public mirror HildoYe/game_files@e6d531, common/policies/00_policies.txt: war_philosophy, unrestricted/liberation/no_wars, fileciteturn21file0L21-L48 and fileciteturn20file0L16-L68, fileciteturn20file0L71-L154

**Practical rule.** Do not add `war_philosophy = unrestricted_wars` inside a personality and expect it to work. Instead, alter policy AI weights or set policies via valid game effects.
