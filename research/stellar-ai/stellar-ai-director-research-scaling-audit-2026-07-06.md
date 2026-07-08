# Stellar AI Director Research Scaling Audit - 2026-07-06

## Scope

The user reported that the strongest AI empire is still only reaching about 2,000 monthly research and about 20,000 total researched tech by year 2400. This audit checks an unverified strategy note against local Stellaris 4.4.4 and installed mod files, with emphasis on early compounding levers that could move the AI toward Gigastructural Engineering endgame routes sooner.

Source priority used here:

- Stellaris 4.4.4 vanilla files under `C:\Steam\steamapps\common\Stellaris`.
- Gigastructural Engineering workshop files under `C:\Steam\steamapps\workshop\content\281990\1121692237`.
- Current JDataMunch datasets `stellar_ai_object_atlas_20260706` and `stellar_ai_route_overrides_20260706`.
- Current launcher surface `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\dlc_load.json`.

## High Confidence Findings

### 1. Endgame megastructures are not the first bottleneck

Matrioshka Brain remains a valid late-game research source, but it is not a practical first target for the current failure mode. The current run is far below the tech velocity needed to reach that route on time. Treat Matrioshka as an eventual payoff, not the missing early multiplier.

The current route overrides include `matrioshka_brain_0_g_star`, but they do not solve the early research deficit by themselves.

### 2. Pop assembly is a real early snowball gap

Vanilla pop assembly buildings are exactly the kind of compounding lever the pasted note was pointing at, but the current object atlas shows weak Director treatment:

| Object | Atlas action | Atlas concern |
| --- | --- | --- |
| `building_robot_assembly_plant` | build | `needs_route_policy`, no source AI weight |
| `building_robot_assembly_complex` | build | `needs_route_policy`, no source AI weight |
| `building_machine_assembly_plant` | build | `needs_route_policy`, no source AI weight |
| `building_machine_assembly_complex` | build | `needs_route_policy`, no source AI weight |
| `building_clone_vats` | observe | no source AI weight, currently under-prioritized |
| `building_spawning_pool` | observe | no source AI weight, currently under-prioritized |
| `building_offspring_nest` | observe | no source AI weight, currently under-prioritized |

The likely next implementation should add a dedicated pop-growth/pop-assembly route family and promote eligible assembly buildings from passive observation into active build pressure, with empire-type gates so the AI does not try invalid assembly systems.

### 3. Research labs are weighted, but not as an explicit Director build command

The route override dataset gives high weights to `building_research_lab_1`, `building_research_lab_2`, `building_research_lab_3`, `building_institute`, `building_supercomputer`, and `building_archaeostudies_faculty`, but these are `director_action=observe`.

That may be safe if Stellar AI's copied parent building files are doing the build work. It is not enough if the observed problem is that empires are underbuilding research jobs. The next implementation should audit whether the generated Director layer can apply stronger build pressure to research buildings and research districts without fighting Stellar AI's own planet automation.

### 4. Gigas science kilostructures are promising pre-endgame stepping stones

Two tier-3 Gigas science routes are source-backed and much earlier than Matrioshka:

| Route | Tech | Structure IDs | Evidence |
| --- | --- | --- | --- |
| Engineering science kilo | `giga_tech_engineering_test_site` | `macro_test_site_0` through `macro_test_site_3` | tier 3 engineering tech; starter build time 360; first cost uses `@science_kilo_cost_1 = 500`; adds engineering deposits across science-candidate systems |
| Physics science kilo | `giga_tech_macro_scale_weather_manipulation` | `atmosphere_shredder_0` through `atmosphere_shredder_3` | tier 3 physics tech; starter build time 360; first cost uses `@science_kilo_cost_1 = 500`; adds physics deposits across science-candidate systems |

The current route override only explicitly includes `giga_tech_macro_scale_weather_manipulation`, not `giga_tech_engineering_test_site`, `macro_test_site_*`, or `atmosphere_shredder_*`. The atlas sees those objects as generic `mega_engineering_core`, not as a research snowball route. This is likely a real missed multiplier.

### 5. Planetary Computer is probably a major midgame ladder rung, but its districts are the critical part

`giga_tech_planetary_computer` is tier 5 and rare, with prerequisites including `tech_ecological_adaptation`, `tech_self_aware_logic`, `tech_power_plant_3`, and `giga_tech_macro_scale_weather_manipulation`.

`planetary_computer_0` has Gigas AI weight, but `district_giga_pcc_science` has no source AI weight in the atlas and is currently `director_action=observe`. The source decision `decision_giga_pcc_science_district` exists and has `ai_weight = "base = 1000"`, but the district itself is not a Director build target.

The next implementation should treat Planetary Computer as a midgame research-capacity checkpoint and ensure the AI both builds the complex and fills it with science districts.

### 6. The pasted "Encourage Free Thought" claim is wrong for vanilla 4.4.4

In local vanilla 4.4.4, `encourage_free_thought` is the "Encourage Political Thought" edict and modifies ethics shift, not research speed. The relevant ambition is `scientific_revolution`; for regular empires it gives researcher workforce output and a tech alternative, while the wilderness version gives +10% all technology research speed.

Do not implement an `encourage_free_thought` research strategy.

### 7. Research Cooperative and research agreements are real but too small to be the main fix

Research Cooperative has a confirmed +5% all-tech speed federation perk and crisis-only +10%/+10% research-speed perks. Research agreements are backed by `RESEARCH_AGREEMENT_SPEED_MULT = 0.25` in vanilla defines, but they are diplomatic, conditional, and influence-limited.

These are worthwhile opportunistic modifiers. They should not be treated as the core fix for a 2,000/month research ceiling.

### 8. ACOT is installed but not active in the checked launcher surface

ACOT workshop folders exist locally, including core `1419304439`, Override `1504307690`, and related add-ons. The checked `dlc_load.json` did not include those ACOT IDs; it included `2960574667` and `3245080043`, which are Vengeance Shipset and Kurogane 2.0, not ACOT.

The current object atlas has zero rows for known ACOT IDs. Do not spend implementation effort on ACOT-specific policy until the active playset confirms ACOT is enabled, or the atlas is regenerated with ACOT included.

## Claim Audit

| Pasted claim | Verdict | Notes |
| --- | --- | --- |
| "Pop Assembly is king" | Directionally true | Needs concrete Director route support for clone vats, spawning pools, robot/machine assembly plants, and upgrades. |
| "Vertical planet investment / tech worlds matter" | Likely true | Research designations exist for planets, habitats, ring worlds, ecumenopoleis, and nomads. Ascension amplification still needs a focused source pass before coding. |
| "Matryoshka Brain provides thousands of raw research" | True but too late | Correct as a payoff, not as the missing early snowball. |
| "Planet Craft Research Segments" | Probably mislabeled | Local evidence points to Planetary Computer science districts, not planetcraft. |
| "Science Nexus remains powerful" | True but insufficient alone | Useful stepping stone; not enough to fix a 2,000/month ceiling by itself. |
| "Research Cooperative grants massive base speed" | Overstated | Base all-tech speed observed at +5%; crisis perks can add +20% while crisis is present. |
| "Research agreements help" | True but conditional | Vanilla define shows 0.25 speed multiplier; requires diplomacy and influence. |
| "Encourage Free Thought gives +10% research speed" | False for checked 4.4.4 | It is an ethics-shift edict locally. Use Scientific Revolution instead. |

## Recommended Next Implementation Slices

1. Add a `pop_assembly_snowball_core` route for eligible assembly buildings and upgrades, with empire-type and tech gates.
2. Add a `science_kilo_snowball_core` route for `giga_tech_engineering_test_site`, `giga_tech_macro_scale_weather_manipulation`, `macro_test_site_*`, and `atmosphere_shredder_*`.
3. Add a `planetary_computer_research_core` route for `giga_tech_planetary_computer`, `planetary_computer_*`, `decision_giga_pcc_science_district`, and `district_giga_pcc_science`.
4. Audit research district/building actions that are currently `observe`; decide which can safely become active `build` pressure without fighting Stellar AI.
5. Add opportunistic, low-priority diplomacy/edict goals for research agreements, research federation membership, and Scientific Revolution only after the raw research and pop-growth routes are strengthened.
6. Do not add ACOT-specific routes until the active launcher surface or regenerated object atlas includes ACOT.

## Validation Performed

- Munch MCP guides returned content for JDocMunch, JCodeMunch, and JDataMunch.
- `C:\Users\Admin\.codex\scripts\assert-munch-mcp-startup.ps1` passed with expected duplicate stdio process warnings.
- Re-indexed `research\stellar-ai\stellar-ai-director-route-overrides-2026-07-06.csv` as `stellar_ai_route_overrides_20260706` after validation found a missing `index.json`.
- Verified `stellar_ai_route_overrides_20260706` and `stellar_ai_object_atlas_20260706` with JDataMunch.
- Checked active launcher IDs in `C:\Users\Admin\Documents\Paradox Interactive\Stellaris\dlc_load.json`.

## Remaining Uncertainty

- Planetary ascension mechanics should be inspected before implementing explicit ascension goals.
- Curator scientist claims were not fully verified in this pass and should not be treated as implementation-ready.
- Static source evidence cannot prove in-game year-2400 outcomes; observer validation remains a separate, user-authorized step.
