# Stellar AI Director Snowball Checkpoints

Date: 2026-07-06
Target stack when written: Stellaris 4.4.4 stable with Gigastructural Engineering & More, NSC3, ESC NEXT, Starbase Extended, and Stellar AI Director. Current target as of 2026-07-08 is Stellaris 4.4.5 stable/current local install.

## Decision Model

The Director needs a deterministic snowball ladder, not one generic "prefer megastructures" profile. Each profile should have an entry condition, an accomplishment condition, and an emergency exit for war, naval collapse, core-resource deficits, or short stockpile runway.

The core loop is:

1. Keep a survival floor: enough navy and starbase choke defense to avoid dying.
2. Convert early minerals/alloys into research and build surface.
3. Unlock the first high-leverage kilostructures and megastructures.
4. Use each completed payoff to unlock and fund the next tier.
5. Convert the larger economy into fleet power after major economic/research completions.

## Recommended Checkpoint Ladder

### 1. Opening Compression

Goal: reach stable research/alloy growth without overbuying early fleets.

Priority surfaces:

- vanilla and Stellar AI research lab/district weights;
- alloy and consumer-goods stability;
- early starbase choke defense;
- ESC strategic-resource prerequisites only when needed for the next component tier;
- NSC3/heavy-hull tech path setup without suppressing survival ships too hard.

Exit when the empire has stable core income, no immediate deficit spiral, and a live path toward Mega-Engineering or boxed-in tall expansion.

### 2. Boxed-In Escape Profile

Trigger when the empire has roughly one to three colony planets and no cheap expansion path.

Priority order:

1. If a weak neighbor or vassalization target exists, consider conquest escape.
2. If conquest is unsafe or blocked, pivot to tall build surface.
3. Weight habitats and habitat-support buildings as expansion infrastructure, not flavor.

Evidence:

- `habitat_central_complex`, `interstellar_habitat_0`, and `stellar_ring_habitat_0` are high-priority `crowded_tall_route` entries in the policy matrix.
- `interstellar_habitat_0` requires `giga_tech_interstellar_habitat`; `stellar_ring_habitat_0` requires `giga_tech_stellar_ring_habitat`.
- Gigas habitat stages already have continuation `ai_weight`, but the current generated route override CSV has no explicit habitat rows.

Implementation need: add a boxed-in phase gate that pushes habitat techs, habitat build starts, and tall-scaling buildings when colony surface is low.

### 3. Early Kilo Economy Profile

Goal: create the income slope that makes full megastructure spending realistic.

Candidate stepping stones:

- Orbital Arc Furnace: low first-stage costs relative to later megas, mineral/alloy economy support, continuation weights present.
- Asteroid Manufactory: AI-specific branches for consumer goods, alloys, food, energy, and supertensiles; the energy branch uses `value:giga_ai_output|RESOURCE|energy|AMOUNT|5000|MIN|0.5|`.
- Atmospheric Storm Observatory: research/science kilostructure candidate gated by `giga_tech_macro_scale_weather_manipulation`; source uses custom-tooltip country modifiers, so exact payoff needs localization or runtime confirmation before hard numeric ranking.

Implementation need: classify these as early kilo/economy accelerators with affordability gates, not as equal peers of Science Nexus or Matrioshka Brain.

### 4. Science Nexus / Think Tank Profile

Goal: buy a direct research jump before late Gigas escalation.

Evidence from Gigas `zz_e_science_nexus.txt`:

- `think_tank_0` requires `tech_science_nexus`, costs 5,000 alloys plus unity, and has startup `ai_weight`.
- `think_tank_1` costs 15,000 alloys plus unity, produces 100 physics/society/engineering research, and adds 5% research speed.
- `think_tank_2` produces 200 of each research and adds 10% research speed.
- `think_tank_3` produces 300 of each research and adds 15% research speed.
- Continuation stages use `value:giga_ai_base_continue`.

Current gap: the policy matrix marks `tech_science_nexus` and `think_tank_0..3`, but the current route override CSV has no explicit `think_tank_*` rows.

Implementation need: add a research-megastructure profile that pushes `tech_science_nexus` and `think_tank_0..3` when the empire has Mega-Engineering/Galactic Wonders path access, enough alloy runway, and no emergency military/resource state.

### 5. Ring World / Build-Surface Profile

Goal: expand research and economic capacity after the empire can pay megastructure costs and has population growth or migration to exploit the surface.

Evidence from Gigas `zz_e_ring_world.txt`:

- `ring_world_1` requires `tech_ring_world`, costs 5,000 alloys, and starts the chain.
- `ring_world_2_intermediate` costs 10,000 alloys and uses continuation `ai_weight`.
- `ring_world_3_intermediate` costs 10,000 alloys plus bulk matter and uses continuation `ai_weight`.

Current gap: the policy matrix marks ring-world stages, but current route overrides do not include them.

Implementation need: add a build-surface profile that prefers ring-world starts after the first research/economy payoff or when boxed-in tall pressure remains high.

### 6. Storage-Cap Profile

Goal: raise storage before very large late-game Gigas projects exceed default caps.

Evidence:

- Gigas `kugelblitz_0` requires `giga_tech_kugelblitz`; the tech depends on `tech_starbase_5` and `tech_zero_point_power` in the object atlas.
- `kugelblitz_1` adds `country_resource_max_add = 50000`.
- `kugelblitz_2` requires Mega-Engineering and adds `country_resource_max_add = 150000`.
- `kugelblitz_3` requires Tetradimensional Engineering and adds `country_resource_max_add = 500000`.
- The inspected Kugelblitz source shows energy costs/upkeep, not energy production. If the desired "storage plus energy income" target exists, it is not Kugelblitz in the inspected source.
- `building_giga_mega_storage` is a Gigas ring-world building, not a kilostructure; it requires `giga_tech_ringworld_buildings` and adds `country_resource_max_add = 1500 * value:giga_ring_world_building_size`.

Implementation need: route Kugelblitz as a storage-cap checkpoint, not an energy-income checkpoint. Separately route energy kilostructures such as Asteroid Manufactory energy branch or Dyson-line structures.

### 7. Matrioshka / Late Research Breakout Profile

Goal: move from strong research to runaway Gigas research.

Evidence:

- `matrioshka_brain_0_g_star` requires `giga_tech_matrioshka_brain_1`, costs 10,000 alloys plus giga unity, and uses Gigas AI savings/upkeep weights.
- Scripted variables show Matrioshka stages can reach much larger research output than Science Nexus, so this should follow Science Nexus/Kugelblitz/energy preparation rather than compete with them early.

Implementation need: add Matrioshka as a late research breakout after storage, energy, alloys, and prerequisite techs are secured.

### 8. Fleet Conversion Profile

Goal: convert the economic/research snowball into actual survival and conquest power.

Evidence:

- Vanilla ship sizes define AI demand through `ai_ship_data` fractions/min/max and expose `ship_roles` / `triggered_ship_roles`.
- Military ship sizes require component sets such as power core, FTL, thrusters, sensors, and combat computers.
- Global ship designs are static premade/event designs. Scripts can create/add static designs and a few events use `set_ship_design` for specific owned ships, but there is no inspected normal AI policy surface for "maintain empty reserve design and convert all ships on war."

Conclusion: do not make naked reserve fleets a V1 Director feature. Treat it as experimental only after a focused proof. The practical V1 route is:

- keep survival fleet floors;
- weight NSC3 heavy hull and ESC component unlocks;
- use strong starbase chokepoints to buy conversion time;
- trigger a post-megastructure fleet-conversion profile that prioritizes shipyards, strategic resources, heavy designs, and fleet rebuilding.

## Immediate Implementation Slices

1. Add explicit route overrides for missing high-leverage megastructure stages:
   - `think_tank_0..3`;
   - `ring_world_1`, `ring_world_2_intermediate`, `ring_world_3_intermediate`;
   - `kugelblitz_0..3`;
   - `habitat_central_complex`, `interstellar_habitat_0`, `stellar_ring_habitat_0`.
2. Add tech-route rows for:
   - `tech_science_nexus`;
   - `tech_ring_world`;
   - `giga_tech_kugelblitz`;
   - `giga_tech_interstellar_habitat`;
   - `giga_tech_stellar_ring_habitat`;
   - early kilo techs for Orbital Arc Furnace, Asteroid Manufactory, and Atmospheric Storm Observatory.
3. Add phase triggers:
   - boxed-in tall pressure;
   - research-megastructure target;
   - ring-world build-surface target;
   - storage-cap target;
   - post-payoff fleet conversion.
4. Add building-weight slice for tall and advanced unlocked buildings:
   - Gigas ring-world storage and housing/economic buildings;
   - Gigas habitat support buildings;
   - pop assembly and growth buildings when surface-limited;
   - advanced modded resource/research buildings where parent AI support is absent or partial.
5. Keep naked-fleet conversion out of normal generation until a separate feasibility proof shows safe design creation, assignment, upgrade, and war-trigger behavior.

## Validation Notes

- Use JDataMunch for route/policy/object CSV inspection.
- Use exact source reads for specific Gigas/vanilla files after JDataMunch identifies candidate objects.
- Do not encode observer-game targets as fast tests; use static validation for generated files, references, and object existence.
- Treat research milestones such as 5k-10k by 2300 and 20k-40k by 2350 as tuning notes, not brittle automated tests.
