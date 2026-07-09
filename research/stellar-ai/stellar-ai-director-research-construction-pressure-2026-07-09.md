# Stellar AI Director Research Construction Pressure Pass - 2026-07-09

## Scope

Strategic v2 task T07 strengthens research-world construction pressure without allowing unconditional lab spam. The pass targets generated research infrastructure building and district weights while preserving the support-economy runway gates that prevent consumer goods, energy, and minerals collapse.

## Source Evidence

- JDataMunch dataset `stellar_ai_director_economic_valuation_20260707` was inspected for `building_research_lab_1`, `building_research_lab_2`, `building_research_lab_3`, `building_institute`, `building_supercomputer`, `building_archaeostudies_faculty`, `district_hab_science`, and `district_giga_pcc_science`.
- Generated policy-matrix rows place these surfaces in `research_throughput_infrastructure` and tall/crowded route families with `no_core_deficit` and resolved route prerequisite safety gates.
- Current generated strategy triggers already provide `staid_research_input_runway_safe`, `staid_research_under_curve`, `staid_opening_route_research_priority`, `staid_surplus_sink_pressure`, and `staid_planetary_capacity_growth_ready`.

## Implementation

- Research infrastructure buildings retain the hard zero gate unless `staid_research_input_runway_safe = yes`.
- Once safe, those buildings now receive extra construction pressure for:
  - `staid_research_under_curve`
  - `staid_opening_route_research_priority`
  - `staid_surplus_sink_pressure`
- Habitat science districts retain the tall-capacity hard zero gate and now receive extra pressure when the empire is under the research curve.
- `mods/StellarAIDirector/notes/tuning-notes.md` records the operational intent so later runtime evidence can be compared against the hypothesis.

## Validation Plan

- Regenerate Stellar AI Director generated files.
- Validate generated references and dependency gates.
- Compile the generator and validator.
- Run the full `tools/tests` suite.
- Refresh affected JData/JDoc indexes before relying on generated evidence.

## Runtime Evidence Gap

This is a static implementation slice. Runtime efficacy remains unproven until the approved observer run phase after all non-runtime packet work is complete.
