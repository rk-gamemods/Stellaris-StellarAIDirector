# AI Use Of High-Powered Modded Systems

## Direct answer

Public sources support three claims at different confidence levels:

1. **Some mod authors expose or claim AI support.** Gigas advertises AI use of its megastructure systems through its feature scope [S001]. Stellar AI claims a coherent research-first no-hidden-bonus AI [S033]. StarNet claims improved economy, research, military, and fleet use [S035]. Yagisan's Better Stellaris claims job-placement support including mod-added jobs [S040].
2. **Compatibility patches can be version-stale.** The public Starnet for NSC3 patch says it is for 3.12 and should not be used with other game versions [S036].
3. **Community evidence does not prove full-stack mastery.** Players question whether AI can keep up with Gigas scaling [S038] and report AI ineffectiveness against Blokkats [S039].

Therefore the correct project answer is: use public AI claims as route hints, but do not rely on them. Stellar AI Director needs explicit high-scale mod routes and observer proof.

## What the AI can plausibly use

| System | Public evidence | Confidence | Practical conclusion |
|---|---|---:|---|
| Vanilla economy/jobs | AI mods claim broad economy and job handling [S033][S035][S040] | medium | Use as baseline, but local observer runs decide truth. |
| Gigas megastructures | Gigas feature scope includes AI use claims [S001] | medium | Preserve parent AI where complete; add route pressure where absent. |
| Gigas crises | Player reports suggest AI is weak/useless versus Blokkats [S039] | medium | AI needs scripted crisis-counter assistance. |
| NSC3 hulls | NSC3 provides classes; stale StarNet patch exists for old versions [S025][S036] | low-medium | Validate current tech/ship-design graph before assuming AI designs work. |
| ESC components | ESC component tree exists but old AI patches/comments show conflict symptoms [S028][S037] | low-medium | AI global designs need source-backed component templates. |
| Starbase Extended | Page says it supports NSC/ACOT and adds starbase levels [S041] | medium | AI weights may need Director support for correct static-defense buildout. |
| PD/Guilli | GPM claims compatibility; PD/Exotic submods add jobs/deposits [S056][S057] | medium | AI should value modifiers/deposits, not only vanilla planet class. |
| URP/UIOD | Maintainer pages solve visibility/UI issues [S047][S051] | high | Required for human diagnosis and active-stack usability. |

## AI failure modes documented by sources

### 1. The AI may have hooks but wrong strategic goal

A parent mod can define AI weights for a megastructure, but that does not prove the AI is selecting the right route at the right year. In high-powered Gigas, a “reasonable” vanilla weight can still be wrong if the crisis curve requires a specific sequence.

### 2. The AI may research the wrong technology branch

Old Starnet/NSC comments describe ship tech progression staying vanilla or broken when patches conflict [S037]. This is directly relevant to NSC3 + ESC NEXT because engineering tech decks can be crowded with hulls, sections, reactors, weapons, and Gigas unlocks.

### 3. The AI may build resources it cannot see/use correctly

URP visibility problems and requests for missing strategic resources show that added resources can be invisible or unsupported until patched [S051][S052]. Hidden resource bottlenecks make it easy to misdiagnose AI failures.

### 4. The AI may not execute crisis mechanics

Katzen and Blokkat counterplay requires event/interface/research mechanics, not only fleet movement [S004][S006][S007][S039]. Generic fleet AI will not discover those routes unless the parent mod explicitly handles them and the AI actually reaches the conditions.

## Existing AI mods and patches worth knowing

| Mod/patch | Status for this stack | Reason |
|---|---|---|
| Stellar AI | Relevant reference, possible parent or comparison mod | Research-first no-hidden-bonus posture matches high-powered scaling need [S033]. |
| StarNet AI | Conceptual AI-aggression/economy reference | Current 4.4 compatibility must be checked; page claims stronger fleet use [S035]. |
| StarNet for NSC3 | Do not use directly for 4.4 | Explicitly says 3.12 only [S036]. |
| Yagisan's Better Stellaris | Watchlist/reference | Claims mod-added job placement, but not proven for this stack [S040]. |
| Stellar AI Director | Project-local route override layer | Should remain the integration point because external evidence does not prove full-stack mastery. |

## Implementation answer for Stellar AI Director

1. **Keep route names.** AI policy should be expressed as named routes: research unlock, Mega Engineering, Gigas economy, Gigas special resource, NSC hull, ESC component, starbase defense, fleet throughput, crisis counter.
2. **Preserve parent support only when complete.** If Gigas or NSC already has a good AI weight for an object, keep it. If it is absent, wrong-goal, or partial, add Director support.
3. **Use negative gating.** Do not let the AI build prestige megastructures during survival/recovery/deficit states.
4. **Build an observer proof loop.** Public sources cannot prove AI behavior. Use 2250/2300/2325/2350 checkpoints to record tech, science, alloys, naval capacity, fleet power, megastructure count, and Gigas special resources.
5. **Test crisis mechanics explicitly.** Katzen resistance, Blokkat knowledge/counterstructures, Aeternum celestial ships, and Compound event gates need separate proof.
