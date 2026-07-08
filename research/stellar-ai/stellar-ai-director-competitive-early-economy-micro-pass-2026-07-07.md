# Stellar AI Director Competitive Early Economy Micro Pass

Date: 2026-07-07
Scope: first 50-75 years, before megastructure/modded exponential scaling dominates
Target: turn competitive human early-game habits into AI-observable behavior and patch hypotheses.

## Why This Exists

The previous research pass under-covered the user's actual request. It identified Research Cooperative and research pacts, but it did not dig deeply enough into the small early-game decisions competitive players use to make a strong empire foundation before 2250-2275.

This pass is about the smaller compounding wins: market timing, pop/job handling, capital specialization, colony timing, science-ship routing, starbase economics, policy choices, expansion selectivity, and when fleet spending is an investment rather than waste.

## Sources Checked

- Reddit, Montu tournament meta summary: https://www.reddit.com/r/Stellaris/comments/1pisidx/a_quick_summary_on_meta_builds_from_the_last/
- Reddit, "Guide to Hitting 3k+ Science by 2250": https://www.reddit.com/r/Stellaris/comments/vckh36/guide_to_hitting_3k_science_by_2250/
- Reddit, "4.0 cold start economy basic advice?": https://www.reddit.com/r/Stellaris/comments/1kg79dg/40_cold_start_economy_basic_advice/
- Reddit, "What is a good early build order?": https://www.reddit.com/r/Stellaris/comments/kn9ddn/what_is_a_good_early_build_order/
- Steam, multiplayer newbie guide: https://steamcommunity.com/sharedfiles/filedetails/?id=2309611439
- Steam, economy guide discussion: https://steamcommunity.com/app/281990/discussions/0/596284732212418039/
- Steam, early capital/colony order discussion: https://steamcommunity.com/app/281990/discussions/0/599666256597186436/
- Stellaris Wiki, Technology: https://stellaris.paradoxwikis.com/Technology

Version caution: some detailed build-order posts are older than 4.4.4 and should not be copied literally. The stable lessons are the resource-flow and decision-policy patterns: early pops, early colonies, market bridging, capital research concentration, avoid idle jobs, use fleet only for payoff, and keep tech-card prerequisites moving.

## Competitive Benchmarks Found

The aggressive 3k-science guide gives a useful human benchmark curve:

- 2210: 200+ science and at least 3 colonies, preferably 4-5.
- 2220: 500+ science.
- 2230: 1000+ science.
- 2240: 2000+ science.
- 2250: 3000+ science and roughly 200 pops without conquest.

This is not automatically the AI benchmark for every empire in the active mod stack, but it proves the user's point: 1000 research around 2270-2280 is not a high bar for a top snowball empire. The top AI should be earlier than that if it is going to matter against 25x crisis scaling.

## Small Wins And AI Translation

### 1. Day-1 Market Mineral Buy

Human trick: buy minerals immediately, often around 30-40/month, to accelerate buildings, districts, and colony setup before natural mineral income catches up.

Why it works: early minerals are time. Every delayed lab, district, colony support building, or blocker clear compounds downward.

AI translation:

- Add or strengthen early market-buy behavior for minerals when energy income/stockpile can support it.
- Treat early mineral shortage as a build-tempo emergency, not a passive deficit to wait out.
- Avoid selling minerals early unless capped or in emergency.

Observer metrics:

- Monthly mineral buy/sell if parseable from market logs.
- Mineral stockpile and income at 2205/2210/2220.
- Number of queued/blocked buildings waiting on minerals.

### 2. Dynamic Consumer Goods Bridging

Human trick: run research beyond natural CG production and buy CG temporarily, then build/shift civilian production when the deficit gets too large.

Why it works: being perfectly CG-positive at all times can mean under-staffing researchers. A small managed CG deficit or market-supported lab surge is often stronger than waiting.

AI translation:

- Permit early CG market support for research builds with energy runway.
- Do not let CG deficits spiral into job collapse; use thresholds.
- Prioritize civilian industry only when labs are bottlenecked by CG, not by habit.

Observer metrics:

- CG income/stockpile and researcher count.
- Labs built but unstaffed due CG.
- Researcher job count vs artisan/fabricator job count.

### 3. Capital As First Research World

Human trick: put early labs on the capital because it starts with the most pops and building slots; move basic production pressure to colonies as they mature.

Why it works: research jobs need pops now, not empty future slots. Capital has the earliest staffing density and can stack bonuses.

AI translation:

- Capital early plan should aggressively favor labs/research districts/zones when CG and amenities allow.
- New colonies should take basic resource, CG, or alloy roles to let the capital keep researchers.
- When a colony gains a production building, replace low-value capital production with research if stability/upkeep allow.

Observer metrics:

- Capital researcher jobs and lab count by 2210/2220/2230.
- Ratio of capital research jobs to capital basic worker jobs.
- Colony support role coverage: CG world, energy/mineral world, alloy world.

### 4. Avoid Clerks And Empty Jobs

Human trick: avoid employing low-value clerks and avoid building districts/buildings too early when pops cannot work them.

Why it works: early pops are the true scarce resource. A pop in a weak job or an empty job slot is lost compounding.

AI translation:

- Lower clerk/trade-job priority for non-trade builds.
- Prefer buildings/districts that immediately employ available pops or solve the next bottleneck.
- Penalize overbuilding empty districts and buildings unless a pop-growth/assembly burst is imminent.

Observer metrics:

- Clerk count, unemployed pops, and empty specialist jobs.
- Built lab slots vs staffed researcher jobs.
- District/building count with no corresponding pop demand.

### 5. Early Colony Count And Pop Acquisition

Human trick: colonize guaranteed worlds very early, use migration treaties for more habitability coverage, and treat primitive/conquered worlds as pop injections.

Why it works: more planets means more pop growth streams; conquered planets skip the slow "new colony has no pops" problem.

AI translation:

- Push guaranteed colonies immediately when resource runway exists.
- Prefer early migration pacts or species access when it opens otherwise weak worlds.
- For aggressive empires, early wars should prioritize populated planets, not low-value systems.
- Consider explicit primitive-world invasion/evaluation where legal and personality-appropriate.

Observer metrics:

- Colonies by 2210/2220/2230.
- Pops by 2220/2230/2250.
- Conquered/primitive pops gained.
- Colonizable planets known but uncolonized.

### 6. Science Ships: Explore First, Survey Deliberately

Human trick: build multiple science ships and use Explore to reveal habitables, neighbors, choke points, and contacts before fully surveying everything.

Why it works: the first strategic need is knowing where colonies, threats, and expansion races are. Full survey of irrelevant systems can waste early scientist time.

AI translation:

- Increase early science-ship count for economy/research empires.
- Prioritize discovery of guaranteed habitables, nearby colonies, hostile neighbors, and chokepoints.
- Assign the last/extra early science ship to assist research once the local strategic map is known.

Observer metrics:

- Science ships built by 2205/2210.
- Known colonizable planets by 2210.
- First-contact count and influence income.
- Assist-research assignment on capital when exploration wave is complete.

### 7. Hydroponics Bays And Starbase Economy

Human trick: max early starbases for hydroponics bays, sell surplus food, and use that liquidity to keep mineral/CG/alloy buys going.

Why it works: starbase food can free pops from farmer jobs and convert into market liquidity. It is an indirect research accelerator because pops can become miners/artisans/researchers instead.

AI translation:

- Increase hydroponics bay priority where food-using empire can use or sell food.
- Treat early starbase cap as an economy multiplier, not only defense.
- Use food surplus market conversion carefully above a reserve.

Observer metrics:

- Starbase count vs cap.
- Hydroponics bays by 2210/2220.
- Farmer jobs avoided/reduced.
- Food surplus sold or stockpiled uselessly.

### 8. Expansion ROI And "Planets Over Systems"

Human trick: do not blindly claim every system. Spend influence/alloys on systems that lead to planets, chokepoints, bridges, or high resource value. In war, claim planets, not low-value space.

Why it works: early outposts compete with colony ships, starbases, science ships, and fleet. Low-ROI systems slow the foundation.

AI translation:

- Raise system-claim value for habitables, chokepoints, bridge systems, and high mineral/energy value.
- Lower value for isolated low-yield systems unless needed for route control.
- For conquest AI, war claims should target capital/world systems first.

Observer metrics:

- Outposts built with no colony/resource/chokepoint payoff.
- Influence spent per colony secured.
- War claims: planet systems vs non-planet systems.

### 9. Policy And Rights Setup

Human trick: set policies/species rights immediately for the intended opening: Academic Privilege for research, Proactive first contact for contacts/influence, Civilian Economy for CG-heavy lab rush, refugee/migration openness for pops, then swap later when the strategic need changes.

Why it works: policies are small percentage or flow changes that affect every early month.

AI translation:

- Add opening policy weights by empire role: research/economy/diplomacy vs militarist/conquest.
- Research/economy empires should bias toward science/CG/pop-access policies; militarists toward alloy/fleet once the attack window is chosen.
- Re-evaluate policy after 2210/2220 rather than sticking to day-1 settings forever.

Observer metrics:

- Policies at 2200/2210/2220.
- Specialist output modifiers active.
- CG/alloy policy match to build strategy.

### 10. Tech-Card Pathing

Human trick: prioritize technologies that unlock production multipliers, research alternatives, starbase economy, pop assembly/growth, and the chosen ascension/megastructure route.

Why it works: Stellaris research is card/weight gated. Missing prerequisite tiers and draw-weight enhancers delays the entire route.

AI translation:

- Weight early Computing, Industry, New Worlds, Statecraft, and Voidcraft route techs according to empire plan.
- Prioritize production multiplier buildings: civilian fabricators, energy grid/nexus, mineral purification, research output techs, hydroponics, starbase upgrades, pop assembly, capital upgrades.
- Prefer research alternatives where they improve chance to draw route techs.

Observer metrics:

- Key tech acquisition dates: hydroponics, capital upgrades, production buildings, research alternatives, pop assembly, Mega Engineering prerequisites.
- Number of research alternatives.
- Whether AI is picking cheap irrelevant techs over route-critical cards.

### 11. Unity First Can Be Tech First

Human/PvP finding: recent tournament summaries include multiple strong builds whose early strategy is unity rush, not direct lab-only tech rush. Examples from the Montu-summary Reddit post include Shroud-Forged tech rush with Prosperity/Psionic/Discovery/Supremacy, Lava Giant Virtual Cultist Machines with unity rush, and Death Cult/Fortune Seekers Megacorps with unity rush.

Why it works: ascension, traditions, planet ascension, and build-defining perks can create a stronger research base than adding a few early labs.

AI translation:

- Do not treat unity as anti-research. Define route types: direct tech rush, unity-to-tech rush, military-to-pops-to-tech rush.
- If an empire has strong ascension/tradition synergy, prioritize the unity path until the conversion point, then hard pivot into research/alloys.

Observer metrics:

- Traditions completed by 2220/2230/2250.
- Ascension path start date.
- Unity/month and unity buildings/jobs relative to research conversion.

### 12. Fleet As Investment, Not Decoration

Human competitive logic: early fleet is valid if it wins a capital, primitives, subjects, or safety. It is bad if it only consumes alloys/upkeep while the empire stays boxed and passive.

Why it works: conquest is the fastest way to add pops. A military rush that gains a capital can outperform a pure tech rush; idle fleet cannot.

AI translation:

- Militarist/conqueror AI should lower war thresholds when it has a timing edge and target populated systems.
- Non-militarists should build defensive minimum and use diplomacy/research/economy.
- Fleet buildup should be paired to an action gate: declare, vassalize, conquer, deter known threat, or stop building.

Observer metrics:

- Fleet built vs wars declared.
- Pops/colonies/subjects gained per alloy spent.
- Idle fleet upkeep years.
- War target quality and claims.

## AI Implementation Priority

P0 observer metrics before patching:

- Add first-75-years checkpoint fields: policies, colonies, pops, known colonizable planets, science ships, assist-research, capital lab/researcher count, clerk count, empty jobs, CG/market support, starbase/hydroponics count, tradition/ascension timing, federation type, research agreements, wars/claims/subjects/pops gained.

P0 economy tuning:

- Early mineral/CG/alloy market support with runway guards.
- Capital-first research concentration.
- Colony support specialization.
- Clerk suppression and empty-job avoidance.
- Colonization urgency for guaranteed and high-habitability worlds.

P0 military payoff tuning:

- For militarists/conquerors, connect fleet buildup to aggressive war/claim/subject behavior.
- For non-militarists, cap fleet at defensive sufficiency and redirect surplus into research/CG/unity/colonies.

P1 tech/tradition route tuning:

- Add role-specific first-50-years routes: direct tech, unity-to-tech, military-to-pops-to-tech.
- Weight production multiplier buildings/techs before flashy late techs.
- Track draw-enabler technologies and research alternatives.

P1 diplomacy tuning:

- Research pacts and Research Cooperative are part of the economy engine, not flavor.
- Push embassies/trust/Diplomatic Networking and research agreement acceptance for friendly non-genocidal empires.

## Immediate Hypothesis For Next Patch Slice

The current Director likely underperforms because it treats research as late scaling infrastructure and modded unlock weights, while competitive play treats the first 10-30 years as a tempo race:

1. Buy minerals early.
2. Staff capital researchers early.
3. Colonize early.
4. Use market CG to keep researchers active.
5. Avoid clerks and empty jobs.
6. Use starbase hydroponics and food sales as economic leverage.
7. Convert fleet into pops or stop buying fleet.
8. Use unity/ascension when it is the faster path to research, not as a separate goal.

The next patch should therefore not start with more megastructure weights. It should first make the AI's opening behave like a competitive build foundation, then let megastructure and modded scaling compound from a better base.
