# Strategy Findings: 25x Crisis And High-Powered Gigas/NSC3/ESC Endgames

## Answer in one paragraph

Experienced players do not describe 25x crisis readiness as “build a balanced empire.” They describe route discipline: either tech-rush hard enough to unlock repeatables/megastructures before pivoting to alloys, or attack early enough that conquest/pop acquisition doubles the economy before the crisis clock matters. A common lower-bound target is about 500-800 science and 100 alloys by year 50 [S018]. A much stronger tech-rush guide claims 2k+ science by 2240 and 3k+ by 2250 [S017]. For this mod stack, the lower-bound target is a warning line; the high-powered target should be the operating curve because Gigas crises and 25x crisis settings punish late conversion.

## Strategy families players recommend

### 1. Hard tech rush into alloy conversion

**What players recommend:** maximize research early, cover energy/consumer goods/minerals only as support, use diplomacy to avoid wars, and pivot to alloy/naval production when threats or crisis timing require it. The 3k-by-2250 guide states that 2k+ science by 2240 is the key checkpoint and that 3k by 2250 is conservative if the run is working [S017].

**Why it matters for Gigas/NSC3/ESC:** research unlocks Mega Engineering, Gigas prerequisites, NSC hulls, ESC component tiers, megastructure build options, and repeatables. Without early research, late alloy income arrives too late to matter.

**AI translation:** set early research pressure and route unlock priorities before alloy-stockpile vanity. Do not let the AI spend early minerals on low-ROI buildings while labs, research zones, pop assembly, and energy/CG support are behind curve.

### 2. Early aggression / alloy-conquest snowball

**What players recommend:** aggressive starts use alloys/influence to gain pops, planets, subjects, and claims rather than waiting for internal scaling. Recent 25x all-crisis discussions show conquest-heavy or build-specific paths can defeat extreme crisis settings earlier than normal empire curves [S016].

**Why it matters for Gigas/NSC3/ESC:** conquered pops and subject economies can fund the otherwise unrealistic alloy/research requirements for celestial ships, multiple shipyards, and Gigas crisis counters.

**AI translation:** only use this route when the AI has aggressive ethics/personality, nearby weak targets, and enough fleet/alloy runway. Failed aggression is worse than pure tech.

### 3. Crisis-specific counterbuilds

**What players recommend:** do not compare raw fleet power only. Counterfit the crisis. Players explicitly say crisis-specific counters can beat enemies with much higher fleet-power numbers [S019]. Anti-crisis build discussions recommend different designs for shield-heavy, armor/hull-heavy, and massive single-target threats [S020][S021].

**AI translation:** once a crisis type is known, switch ship design weights, weapon preferences, and defense priorities instead of continuing generic mixed fleets.

## Year-by-year / checkpoint benchmarks

These are player-advice benchmarks, not official balance math. Use them as AI route targets and warning thresholds.

| Date | Lower-bound strong-player line | High-powered stack target | Use in AI logic | Evidence |
|---|---:|---:|---|---|
| 2210 | Expansion or early war plan chosen; early labs/industry support started | Route locked: tech, conquest, or survival | Do not average between incompatible plans | [S016][S017] |
| 2220 | Basic economy stable, first specialization decisions | 300-500 science if tech lane; positive alloy income if conquest lane | Raise research/alloy weights if both are low | [S017][S023] |
| 2230 | 300 research can be “fine” in normal play, but not high-end | 800-1200 science on tech lane; conquest should have extra pops/subjects | If below curve, stop low-ROI spending | [S023] |
| 2240 | Normal runs may still be modest | 2k+ science on elite tech-rush line | Mega Engineering/Gigas unlock pressure should already be high | [S017] |
| 2250 | 500-800 science and 100 alloys is a common lower bound | 3k+ science or strong conquest economy; start planned alloy conversion | If below 500 science, emergency research. If below 100 alloys, emergency industry. | [S017][S018] |
| 2275 | First serious megastructure/shipyard goals should be visible | Mega Engineering path, economy megas, NSC/ESC tier pressure | Route to Mega Engineering, Mega Shipyard/Gigas shipyard, starbase defense | [S001][S025][S028] |
| 2300 | 1k+ science is expected for ordinary scaling; 150 alloys is low | 5k-10k+ science, strong alloy base, megastructure construction underway | Stop colonization sprawl that does not pay back before crisis | [S023] |
| 2325 | Conversion phase should be active | Multiple shipyards, naval-cap growth, crisis-counter research | Build fleet throughput, not just stockpile alloys | [S019][S021] |
| 2350 | Millions of fleet power and strong repeatables may be needed | Some players cite ~40k research and ~10k naval cap as a 25x line | Hard crisis readiness check; specialize fleets | [S022] |
| 2400+ | Late crisis settings become easier if scaling was exponential | Gigas celestial ships, systemcraft/planetcraft if Gigas crises enabled | Crisis-specific final conversion | [S009][S010][S012] |

## Economy and conversion guidance

**Research first is not research only.** The strong tech-rush line still needs energy/CG/mineral support and a planned alloy pivot [S017]. In the modded stack, that pivot must include shipyard throughput because massive alloy income is useless if the empire cannot convert it into hulls before a crisis window.

**Alloys without tech are also a trap.** Early conquest can work, but only if conquest produces additional pops and worlds. A stagnant empire with low tech and high alloy stockpiles will lose to Gigas/NSC/ESC technological scaling.

**Mega Engineering timing is a route milestone.** The AI should treat Mega Engineering and prerequisite engineering/research pathing as a named route, not as one tech among hundreds. NSC3/ESC/Gigas make engineering congestion more dangerous.

## Fleet design principles from player advice

1. **Counter the crisis.** Shield-heavy threats need different weapons than armor/hull-heavy threats [S020].
2. **Engage at maximum favorable range.** Older 25x success reports emphasize fighting crisis fleets one or two at a time and opening at long range [S006].
3. **Keep reinforcement throughput alive.** 25x/all-crisis runs require not just a first fleet, but the ability to replace losses [S021][S022].
4. **Screen capital fleets.** Gigas and crisis-scale fights still benefit from screens/pickets/corvettes/frigates so high-value capital ships can apply damage [S009][S021].

## Direct AI route conclusions

- If science < 500 by 2250, the AI is not on a high-powered survival curve.
- If science is strong but alloys/shipyards are weak by 2275-2300, force conversion.
- If both science and alloys are weak, trigger survival/recovery mode and stop prestige megastructures.
- If crisis type is known, switch to counterfit designs.
- If Gigas crises are enabled, require celestial-ship route readiness instead of vanilla crisis readiness.
