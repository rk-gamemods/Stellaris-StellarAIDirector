# Stellar AI Director 2241-2299 Runtime Regression Investigation

Date: 2026-07-11

## Scope and Baseline

This pass investigates five reports from the `unitedcevantiannation24_1055935931` campaign: three recognized-but-uncolonized orbital habitats, a Gigas Rogue Planetwide AI devastation loop, adjacent unclaimed systems left idle, a multi-decade unity/tradition stall, and possible collisions with other colony-automation exceptions.

The active game/save baseline is Stellaris 4.4.4 build 5505. The Director descriptor remains `supported_version="v4.4.*"`; all copied parent objects must be rechecked against the installed 4.4.5 stable files before a 4.4.5 runtime claim. Relevant active dependencies are Gigastructural Engineering 1121692237, More Events Mod 727000451, and Starbase Extended 3250900527. No observer run or game launch was authorized in this pass.

The newest autosave was copied before inspection. Source and copy SHA-256 are both `E11C25F4F4859F9BD4D6FB3CD657443D50DC89E8127ED81FD24E055C141F6179`. Evidence copies include:

- `C:\Users\Admin\AppData\Local\Temp\autosave_2299.07.01-20260711-131316-895.sav`;
- `C:\Users\Admin\AppData\Local\Temp\codex-stellaris-save-copies\autosave_2299.07.01-20260711-131339-expansion-diagnosis.sav`.

The live save was never modified.

The earlier habitat report was also inspected only through a copy: `C:\Users\Admin\AppData\Local\Temp\codex-stellaris-save-copies\test_2241.02.27-20260711-142751-orbital-habitat-diagnosis.sav`. Its source and copy SHA-256 are both `5C986D86EABE0E8B1E7CDF5802F16019C4D04C42E7FBD1B7977891BB8F4C05B4`.

## Gigas Rogue Planetwide AI

Gigas applies `giga_rogue_ai_computer`, corrupt-code/relay blockers, and periodic attacks while the modifier remains. The attack event makes 20 independent 70-percent army-spawn attempts, so an attack averages 14 and can reach 20 `pcc_rogue_ai_army` units. A rogue victory adds 75 devastation and restores blockers, recreating the observed cleanup/devastation loop.

Gigas already ships the correct colony-automation exception: `giga_rogue_ai_planet` requests `building_stronghold`. Director loaded later and replaced `building_stronghold.allow` with economic-readiness and strategic-placement gates, unintentionally vetoing that parent handler.

The correction embeds the exact vetted Gigas exception object and adds a narrow rogue-computer branch to the Director's stronghold/fortress legality. The branch remains inside the parent cap of fewer than two strongholds and fewer than two fortresses. Normal fortress readiness and placement behavior is unchanged. The generated handler is tested against both the vetted snapshot and the currently installed Workshop copy; the test fails if Gigas changes upstream. Director defines no folder `replace_path` and owns no other colony-automation exception.

No event-created armies, free resources, forced fleet orders, or scripted 50-army garrison were added. Gigas's native handler is the authoritative solution; static evidence does not establish a simple native surface for parking an exact army count indefinitely.

## Adjacent-System Expansion

Save evidence rules out affordability, survey, access, constructor availability, and current hostiles for the reported targets. Iota Aquarii 14 and Golovia 107 are unowned, unrestricted, surveyed, and directly adjacent to country 0; Gamma Draconis 156 is the second hop beyond Golovia. Country 0 has roughly 575 influence, 169,000 alloys, and four idle constructors, including one beside Golovia.

The Director's former `staid_economy_safety.5` monthly watchdog counted every `build_orbital_station_order`, canceled it after 12 pulses, and then canceled reissued orders during a 360-day retry backoff. The active outpost has a 360-day base build time before travel. The watchdog therefore interpreted valid long-duration construction as failure. The save contains its tracking state, including an idle constructor with 180 days of backoff remaining.

The generic watchdog, variables, monthly dispatch, and `clear_orders` behavior are removed. Unknown expansion failures return to the native planner instead of a scripted order interceptor.

The original feature also intended to protect the More Events Mod Surveyor home system temporarily. That intent is retained on the native `starbase_outpost.possible_construction` surface, but its release condition is corrected. The old gate waited for `mem_surveyor_found_alkree_homeworld`; active MEM event 303 requires `mem_surveyor_studied_ruins`, for which the active mod contains no setter. It could therefore abandon the system permanently. MEM event 300 does set the permanent planet modifier `mem_surveyor_alkree_homeworld` on the already flagged Alkree carrier planet when the ruins anomaly resolves and then schedules the research-station chain. The corrected gate blocks AI outposts only until that exact carrier-flag-plus-modifier state exists, while player construction and all other systems remain unchanged.

## Orbital Habitats

The 2241 save contains three unowned size-6 `pc_habitat` worlds in country 0's controlled systems: Procyon planet 2206, Sirius 2207, and Tahlin 2208. Native AI state already contains three type-1 colonization strategies targeting exactly those planets with species 87 and value 80. That species is allowed to colonize, and the empire owns a valid colonizer design, but it has zero colony ships. The failure is therefore after native target recognition and before colony-ship funding or production, not habitat eligibility.

The original wartime colony-budget feature was meant to let wealthy, safe empires continue expanding during persistent wars while deferring only under tight or existential pressure. Putting `staid_wartime_colony_expansion_safe` inside `alloys_expenditure_colonies_expand` added a second Director veto after `ai_colonize_plans` had already selected legal targets. That could starve valid habitats indefinitely. Commit `64698897` already removed only those extra war/midgame/Director vetoes while preserving the parent `ai_colonize_plans`, nomad, species-economy, affordability, weight, and desired-min/max logic. Scale-aware runway and existential protections remain on their appropriate economy surfaces.

The audit also found a recurrence risk in the Director's copied Gigas `habitat_central_complex` object. Replacing its entire `ai_weight` dropped Gigas's native recent-build cooldown, uncolonized-habitat backlog veto, and starport requirement. The correction retains the boxed-in/crowded-tall positive route—habitats remain an intended escape route—but preserves all three parent factor-zero safeguards so construction cannot outrun colonization again.

## Unity and Traditions

Country 0 held the exact same partial Discovery state from 2270.01 through 2299.07 while unity rose from approximately 190,000 to 436,610. It was a regular AI, below the category cap, economically healthy, not in survival/collapse mode, and had eligible positive-weight Discovery nodes. Other AIs continued buying traditions. The UI showed the next tradition cost as 1 unity and 0 months because the country owns the `cfl_trophy` relic, while its stockpile was 436,610. Affordability is therefore ruled out: vanilla `unity_expenditure_traditions` remains the sole active budget winner and is deliberately not overridden.

The original Director policy was deliberate: convert unity into research tempo, economy/megastructure progression, conquest capacity, and crowded-tall development. The implementation used the wrong objects. Director attached unsupported choice weights of 65,000 to 170,000 to seven automatic adoption/finish reward objects, creating a candidate-pollution risk. Vanilla's category documentation states that adoption/finish rewards are added automatically and the finish bonus has no cost; normal tree selection belongs to `tradition_<tree>.ai_weight`. The old atlas also reported nested generic `weight` blocks as AI support, which made some adoption objects look like native choice surfaces when they were not. The atlas now treats a tradition as AI-selectable only when it has a top-level `ai_weight`.

The correction preserves the route intent by replacing all seven reward-object targets with native category and selectable-node targets:

- Discovery and Diplomacy -> research/diplomacy;
- Supremacy -> conquest escape;
- Prosperity -> economy/megastructures;
- Adaptability and Mercantile -> crowded tall.

Each category is a full active-parent copy with one factor-4 route modifier inserted into its existing `ai_weight`. The five selectable Discovery nodes and five selectable Diplomacy nodes receive the same bounded modifier in their existing native `ai_weight`; automatic adoption and finish rewards remain untouched. Vanilla base weights, `possible` gates, swaps, potential, ethics, personality, AP-pending suppression, and effects remain identical after removing the inserted route lines. There are no factor-zero exclusions, survival/recovery gates, timing multipliers, or unity reserve changes. This is the strongest Director-controlled correction for candidate pollution, but exact engine candidate-pool behavior and recovery remain runtime-unproven. Legitimate ascension-perk, federation, claim-budget, technology, and megastructure pressure remains in place.

## Colony-Automation Exception Audit

The final active exception map contains 24 unique objects: 22 vanilla objects, Gigas's housing override, the Gigas frameworld exception, and the Gigas rogue-AI exception. Gigas's housing override preserves the full vanilla object and appends only Gigas districts. Director's generated full-object building/district overrides intersect 12 requested objects; tests prove their `potential`, `allow`, and `possible` children remain identical to their parent winners. The only non-dataset intersections are `building_medical_2` and `building_stronghold`; medical legality is preserved, and stronghold has the explicit rogue-AI compatibility branch described above. No other analogous exception collision was found.

## Evidence and Knowledge-Base Boundary

The local Stellaris knowledge base was healthy and useful for version-attested object identity and locating vanilla budget/building surfaces. It did not contain decisive runtime semantics for automatic tradition finishers, constructor order progress, Gigas attacks, or MEM's event-chain defect. The save copies, installed vanilla/mod sources, generated trigger documentation, active-stack conflict inventory, git/Open Brain history, and current runtime logs were therefore decisive. This usefulness boundary should be retained in Open Brain rather than treating the knowledge base as either globally sufficient or globally useless.

## Static Validation and Remaining Risk

Required static checks cover PDX parsing, exact Gigas handler parity, active-Workshop drift, stronghold cap nesting, exception overlap legality, absence of the generic outpost watchdog, reachable MEM release state, active Starbase Extended parent parity, tradition category/node parent parity, absence of tradition reward overrides, preservation of Gigas habitat safety rules, generated file/conflict/reference audits, Python compilation, and diff whitespace.

Static validation can prove load shape and source preservation, not runtime recovery. After a normal game reload, focused observation should verify that the rogue planet builds defenses and completes cleanup, constructors retain valid outpost orders, the MEM home system releases after anomaly resolution, country 0 builds colony ships for its existing native habitat plans, and country 0 purchases a legal tradition. That runtime work requires explicit authorization.
