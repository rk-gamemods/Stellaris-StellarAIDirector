# Ranked Research Questions - Filled Answers

Each question below is answered directly. The ranking reflects value for future AI/modding work, not whether the answer is missing.

## Rank 1 - Q1: High-powered gameplay strategy

**Answer:** The best-supported player strategies are hard tech rush into alloy/naval conversion and early aggression/alloy conquest. A lower-bound year-50 line is roughly 500-800 science and 100 alloys [S018]. A high-end tech-rush benchmark is 2k+ science by 2240 and 3k+ by 2250 [S017]. For a Gigas/NSC/ESC 25x-crisis stack, target the high-end curve and treat the lower-bound line as a failure warning.

**Decision:** AI route kernel must lock a lane by 2210-2220 and enforce conversion by 2275-2300.

## Rank 2 - Q2: Gigas progression and crisis knowledge

**Answer:** Gigas progression is an escalation ladder: unlock research -> economy megas -> special resources -> construction throughput -> celestial ships -> crisis counters. Katzen is resistance/sabotage first [S006][S007]. Blokkats are knowledge/scrap/counter-research/systemcraft [S004][S005][S012]. Aeternum is full Gigas economy plus planetcraft/systemcraft [S009][S010][S011].

**Decision:** Implement named AI routes for each stage and crisis counter.

## Rank 3 - Q3: NSC3 + ESC NEXT + Spacefleet Tactica fleet design

**Answer:** NSC3 supplies classes/scale; ESC supplies advanced components; SFT supplies the behavior layer after NSC3 removed Advanced Ship Behaviors [S025][S027][S028]. Configure ESC reactors when using NSC3 because maintained collection guidance says ESC reactors are weaker and must be adjusted [S029].

**Decision:** Validate active section/component/computer/reactor graph before generating AI designs.

## Rank 4 - Q4: AI use of high-powered mods

**Answer:** Public sources show AI-support claims, not full-stack proof. Gigas claims AI megastructure use [S001], Stellar AI claims research-first no-hidden-bonus AI [S033], StarNet claims aggressive/economic AI [S035], but players still question Gigas AI scaling and report AI failure against Blokkats [S038][S039].

**Decision:** Do not rely on parent AI; use explicit route overrides plus observer proof.

## Rank 5 - Q7: Static defense strategy

**Answer:** Starbase Extended 3.0 is the correct defense pillar because it claims 4.**.*, Vanilla, NSC, and ACOT support [S041]. Expanded Starbases is rejected for this NSC3 stack because it says it is incompatible with NSC [S042]. Planetary cannon mods are stale/3.9-labeled and not 4.4-ready by public evidence [S043][S044].

**Decision:** Use Starbase Extended; consider Eternal Vigilance Redux only after economy/upkeep test [S045].

## Rank 6 - Q9: Modded resources and UI/resource visibility

**Answer:** URP displays added strategic resources from mods and has load-order sensitivity [S051][S052]. UIOD and topbar patches create the UI room needed for NSC/Gigas/PD/resource visibility [S047][S048][S049][S050].

**Decision:** Treat URP/UIOD patches as required infrastructure.

## Rank 7 - Q8: Planetary Diversity and Guilli strategy

**Answer:** PD changes planet variety and submods can add jobs/buildings/deposits/terraforming [S054][S056]. Guilli adds hundreds of planetary modifiers and claims compatibility with PD/Gigas [S057]. Planet role should be based on modifiers/deposits/jobs, not planet class name alone [S059].

**Decision:** Build AI planet valuation from current active modifiers/deposits.

## Rank 8 - Q5: Console commands and testing

**Answer:** Use Paradox Wiki plus in-game `help`; `debugtooltip`, selected-scope `effect`, deposits, traits, megastructure spawn, event firing, `observe`, and `human_ai` are the key test surfaces [S060][S061][S062][S064].

**Decision:** Use the included command templates and verify every modded ID locally.

## Rank 9 - Q6: Modding tools/resources

**Answer:** Use Paradox Wiki, CWTools, Irony, OldEnt generated docs, Steam/GitHub mod source/changelogs, and save/log tools [S065][S070][S071][S074][S076][S077][S078][S079][S080]. Exact syntax comes from vanilla/mod source + CWTools; exact conflicts come from Irony.

**Decision:** Make this the source order for future implementation.

## Rank 10 - Q10: 4.4.x and 4.5 hazards

**Answer:** 4.4.5 changes resource abundance and Nomad/Arkship/Waystation behavior [S081]. 4.5 is a breaking pop/faction/ethic beta and must be a separate branch [S083][S084].

**Decision:** Keep 4.4.5 stable; branch 4.5 separately.
