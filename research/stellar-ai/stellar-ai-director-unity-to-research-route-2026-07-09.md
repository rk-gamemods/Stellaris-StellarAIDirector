# Stellar AI Director Unity-To-Research Route Pass - 2026-07-09

## Scope

Strategic v2 task T10 weights traditions and ascension perks that convert unity spending into research tempo, megastructure progression, or modded high-scale research paths. The pass avoids generic unity hoarding and targets source-backed objects with concrete research or progression payoff.

## Source Evidence

- Current Stellaris 4.4.5 vanilla `common/traditions/00_discovery.txt`:
  - `tr_discovery_adopt` improves anomaly research speed.
  - `tr_discovery_finish` grants `all_technology_research_speed` and an ascension perk.
- Current Stellaris 4.4.5 vanilla `common/traditions/00_diplomacy.txt`:
  - `tr_diplomacy_finish` grants an ascension perk and diplomatic capacity that supports research federation paths.
- Current Stellaris 4.4.5 vanilla `common/ascension_perks/00_ascension_perks.txt`:
  - `ap_technological_ascendancy` improves rare-tech draw.
  - `ap_master_builders` improves megastructure speed and build cap.
  - `ap_galactic_wonders` adds key megastructure research options.
- Existing generated Gigas route pressure already covers `ap_gigastructural_constructs` and `ap_celestial_printing` for modded mega/planetcraft progression.

## Implementation

- Added `ap_technological_ascendancy`, `tr_discovery_adopt`, `tr_discovery_finish`, and `tr_diplomacy_finish` to `research_diplomacy_core`.
- Added `ap_master_builders` and `ap_galactic_wonders` to `economy_megastructure_core`.
- Preserved existing source object bodies and generated Director-owned `ai_weight` comments so route rationale remains visible in generated files.
- Updated tuning notes to make the non-generic unity policy explicit.

## Validation Plan

- Regenerate Stellar AI Director generated files.
- Parse generated ascension perk and tradition files.
- Validate generated references and dependency gates.
- Compile the generator and validator.
- Run focused unity-to-research tests and the full `tools/tests` suite.
- Refresh affected JData/JDoc/JCode indexes before relying on generated evidence.

## Runtime Evidence Gap

This is a static implementation slice. Runtime unity prioritization remains unproven until the approved observer run phase after all non-runtime packet work is complete.
