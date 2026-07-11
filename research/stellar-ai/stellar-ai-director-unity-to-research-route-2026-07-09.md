# Stellar AI Director Unity-To-Research Route Pass - 2026-07-09

## Scope

Strategic v2 task T10 weights traditions and ascension perks that convert unity spending into research tempo, megastructure progression, or modded high-scale research paths. The pass avoids generic unity hoarding and targets source-backed objects with concrete research or progression payoff.

## 2026-07-11 Correction

The T10 objective remains valid, but its original tradition implementation used the wrong native surface. `tr_discovery_adopt`, `tr_discovery_finish`, and `tr_diplomacy_finish` are automatic category rewards, not tree-selection choices. The same defect also affected the older `tr_supremacy_adopt`, `tr_prosperity_adopt`, `tr_adaptability_adopt`, and `tr_mercantile_adopt` route targets. Giving those reward objects Director-owned `ai_weight` blocks attached unsupported choice weights from 65,000 to 170,000 and hard-zero route exclusions, creating a candidate-pollution risk; exact engine candidate-pool behavior remains runtime-unproven.

The corrected implementation preserves the original outcomes by steering the six native tradition categories and the ten selectable Discovery/Diplomacy nodes instead:

- `tradition_discovery` and `tradition_diplomacy` for `research_diplomacy_core`;
- `tradition_supremacy` for `conquest_escape_route`;
- `tradition_prosperity` for `economy_megastructure_core`;
- `tradition_adaptability` and `tradition_mercantile` for `crowded_tall_route`.

Each copied category preserves the complete vanilla `potential`, base factor, ethic/personality modifiers, AP-pending suppression, and selectable-node graph. Each selectable Discovery/Diplomacy node preserves its native base factor, `possible` gates, swaps, modifiers, and effects. Director adds only a bounded factor-4 modifier while the research/diplomacy route is active. It adds no factor-zero off-route gate, survival gate, recovery penalty, time multiplier, unity budget multiplier, or unity reserve. Automatic adoption/finish rewards and their effects remain untouched.

## Source Evidence

- Active Stellaris 4.4.4 build 5505 `common/traditions/00_discovery.txt`:
  - `tr_discovery_adopt` improves anomaly research speed.
  - `tr_discovery_finish` grants `all_technology_research_speed` and an ascension perk.
- Active Stellaris 4.4.4 build 5505 `common/traditions/00_diplomacy.txt`:
  - `tr_diplomacy_finish` grants an ascension perk and diplomatic capacity that supports research federation paths.
- Current vanilla `common/tradition_categories/99_README_TRADITION_CATEGORIES.txt`:
  - adoption and finish bonuses are added automatically;
  - a finish bonus cannot have a cost;
  - the category's `ai_weight` is the native tree-selection surface.
- Current vanilla category files preserve positive tree weights and all normal eligibility/personality logic for Discovery, Diplomacy, Supremacy, Prosperity, Adaptability, and Mercantile.
- Active Stellaris 4.4.4 build 5505 `common/ascension_perks/00_ascension_perks.txt`:
  - `ap_technological_ascendancy` improves rare-tech draw.
  - `ap_master_builders` improves megastructure speed and build cap.
  - `ap_galactic_wonders` adds key megastructure research options.
- Existing generated Gigas route pressure already covers `ap_gigastructural_constructs` and `ap_celestial_printing` for modded mega/planetcraft progression.

## Original Implementation (Superseded)

- Added `ap_technological_ascendancy`, `tr_discovery_adopt`, `tr_discovery_finish`, and `tr_diplomacy_finish` to `research_diplomacy_core`.
- Added `ap_master_builders` and `ap_galactic_wonders` to `economy_megastructure_core`.
- Preserved existing source object bodies and generated Director-owned `ai_weight` comments so route rationale remains visible in generated files.
- Updated tuning notes to make the non-generic unity policy explicit.

Commit history confirms the intent rather than changing it: `20e62915` introduced the four older route-adoption targets, `539a8b09` made generic route weights hard-zero off-route, and `3b834f77` added the three T10 research/diplomacy targets. The 2026-07-11 correction moves those same route mappings to native category and selectable-node selection and retains the legitimate ascension-perk, federation, technology, budget, and megastructure surfaces.

## Validation Plan

- Regenerate Stellar AI Director generated files.
- Parse generated ascension-perk, tradition-category, and selectable-tradition files.
- Prove every generated category and selectable node equals its active vanilla parent after removing only the inserted route lines.
- Prove no route target points at an automatic tradition adoption or finish reward.
- Prove no Director output overrides `unity_expenditure_traditions` or changes its vanilla `weight = 0.8` policy.
- Validate generated references and dependency gates.
- Compile the generator and validator.
- Run focused unity-to-research tests and the full `tools/tests` suite.
- Refresh affected JData/JDoc/JCode indexes before relying on generated evidence.

## Runtime Evidence Gap

Static save evidence proves the affected AI held the same partial Discovery state for at least 29.5 years while unity rose from roughly 190,000 to 436,610. The country owns `cfl_trophy`, reducing its displayed next-tradition cost to 1 unity with 0 months remaining; affordability and reserve pressure are therefore ruled out. Static source evidence identifies the unsupported reward-object weights as the strongest Director-specific cause, but exact candidate-pool semantics and runtime recovery after reload remain unproven until an explicitly approved observer run.
