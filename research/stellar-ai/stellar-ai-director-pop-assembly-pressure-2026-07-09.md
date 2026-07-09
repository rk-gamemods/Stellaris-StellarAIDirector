# Stellar AI Director Pop Assembly Pressure Pass - 2026-07-09

## Scope

Strategic v2 task T08 promotes safe pop assembly and growth infrastructure without allowing invalid empire paths. The pass targets generated `ai_weight` modifiers for vanilla pop assembly building overrides copied into Stellar AI Director.

## Source Evidence

- Current Stellaris 4.4.5 vanilla source inspected: `C:\Steam\steamapps\common\Stellaris\common\buildings\01_pop_assembly_buildings.txt`.
- Generated Director surface inspected: `mods/StellarAIDirector/common/buildings/zzzz_staid_07_pop_assembly_buildings.txt`.
- JDataMunch dataset `stellar_ai_director_economic_valuation_20260707` was inspected for robot assembly plants/complexes, machine assembly plants/complexes, clone vats, spawning pools, and offspring nests.
- JDataMunch dataset `stellar_ai_director_policy_matrix_20260706` places these objects in high-priority tall/pop assembly route families with `no_core_deficit;route_prerequisites_resolved` safety gates.

## Implementation

- All pop assembly objects retain the hard zero gate unless `staid_pop_assembly_snowball_ready = yes`.
- Robot assembly receives extra pressure for Mechanist/synthetic paths and materialist empires.
- Machine assembly receives extra pressure only for machine or individual-machine empires.
- Clone vats receive extra pressure for cloning technology/tradition and biological ascension pressure.
- Spawning pools receive hive pressure but hard-zero for progenitor hives, which should use offspring nests instead.
- Offspring nests receive progenitor-hive pressure.
- Vanilla-derived potential and destroy triggers remain in the copied objects so invalid empire paths are excluded by object availability as well as AI weight.

## Validation Plan

- Regenerate Stellar AI Director generated files.
- Validate generated references and dependency gates.
- Compile the generator and validator.
- Run focused generated-building tests and the full `tools/tests` suite.
- Refresh affected JData/JDoc/JCode indexes before relying on generated evidence.

## Runtime Evidence Gap

This is a static implementation slice. Runtime efficacy remains unproven until the approved observer run phase after all non-runtime packet work is complete.
