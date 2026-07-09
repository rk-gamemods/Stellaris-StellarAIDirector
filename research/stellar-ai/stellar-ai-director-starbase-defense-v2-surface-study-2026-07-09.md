# Stellar AI Director Starbase Defense V2 Surface Study

Date: 2026-07-09
Task: T22 - Starbase Extended defense surface study
Target game version: Stellaris 4.4.5 stable, active packet playset evidence dated 2026-07-08
Scope: research only; no generated gameplay files changed

## Sources Used

- JData `stellaris_packet_active_source_roots_20260708`
- JData `stellaris_packet_starbase_extended_scope_20260708`
- JData `stellaris_packet_active_load_order_conflicts_20260708`
- JData `stellar_ai_director_generated_reference_audit_20260704`
- JData `stellar_ai_director_generated_conflicts_20260704`
- Local descriptor: `C:\Steam\steamapps\workshop\content\281990\3250900527\descriptor.mod`
- Existing Irony artifact: `research/stellar-ai/stellar-ai-director-irony-conflict-scan-2026-07-04.md`
- Irony executable probe: `C:\Users\Admin\AppData\Local\Programs\Irony Mod Manager\IronyModManager.exe --help`

## Identity Proof

The active starbase expansion mod is **Starbase Extended 3.0**, not an inferred
or similarly named Expanded Starbases variant.

Evidence:

- Active source-root row: load position 72, Steam ID `3250900527`, root
  `c:\steam\steamapps\workshop\content\281990\3250900527`, `common_exists=True`,
  `descriptor_exists=True`, required version `v4.**.*`.
- Descriptor fields: `name="Starbase Extended 3.0"`,
  `remote_file_id="3250900527"`, `supported_version="v4.**.*"`, and tags include
  `NSC`, `Starbase`, and `Starbases`.

## Dependency And Conflict Posture

Active dependency-relevant rows found:

- NSC3: present at load position 71, Steam ID `683230077`.
- Starbase Extended 3.0: present at load position 72, Steam ID `3250900527`.
- UI Overhaul Dynamic: present at load position 103, Steam ID `1623423360`.
- UIOD + Gigastructural Engineering: present at load position 106.
- Universal Resource Patch: present at load position 119, Steam ID `1595876588`.
- Universal Modifier Patch: not found by exact active-root display/Steam-ID query.
- Expanded Mods Base: not found by active-root display query.

This is `compatible_with_caveat`, not a clean compatibility claim. Starbase
Extended wins many NSC3/vanilla starbase ship-size and section-template rows in
the current conflict matrix. That may be intentional for the active playset, but
it means a future Director pass must not touch ship sizes, section templates,
component sets, component templates, GUI, or GFX without a narrower conflict map
and runtime/UI evidence.

## Starbase Extended Scope Summary

JData validation passed for the Starbase Extended scope report. It contains 50
objects from Steam ID `3250900527`:

| Surface | Objects | Objects with `potential` | Objects with `possible` | AI-weight blocks | Max nested `owner` refs |
| --- | ---: | ---: | ---: | ---: | ---: |
| `starbase_buildings` | 35 | 27 | 12 | 35 | 4 |
| `starbase_modules` | 15 | 12 | 1 | 15 | 4 |

The source report found no nested `from` or `root` references and only bounded
nested `owner` references. That makes AI-weight copying feasible for selected
module/building objects after object-by-object review, but not safe as a broad
automatic rewrite.

## Current Director Starbase Overrides

Current generated reference validation reports all starbase references as `ok`:

- `common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt`: 17/17 references ok.
- `common/starbase_modules/zzzz_staid_05_starbase_defense_starbase_modules.txt`: 44/44 references ok.

Current generated conflict audit classifies 14 starbase object outputs as
intentional Director overrides:

- Buildings: `adv_starbase_defenses`, `esc_starbase_reactor`,
  `reinforced_defenses`, `strategic_defenses`.
- Modules: `armor_module`, `gun_battery`, `hangar_bay`, `large_battery`,
  `missile_battery`, `orbital_ring_armor_module`,
  `orbital_ring_gun_battery`, `orbital_ring_hangar_bay`,
  `orbital_ring_large_gun_battery`, `orbital_ring_missile_battery`.

Active conflict rows show the Director is currently the final winner at load
position 120 for selected Starbase Extended defense modules/buildings. This is
acceptable only because those generated files declare full-object override
ownership and the reference audit passes.

## Safe Future Levers

Safe or potentially safe, with evidence requirements:

1. **Defensive module/building AI-weight refinements** for already copied
   Director-owned defense objects, preserving original Starbase Extended/NSC3
   `potential` and `possible` blocks and retaining `staid_` economy gates.
2. **Crisis and hostile-border pressure gates** using existing Director triggers
   such as static-defense readiness, crisis pressure, hostile-fauna safety, and
   fleet-buildup economy safety.
3. **Orbital-ring defensive module weights** for the already copied
   orbital-ring defense modules, but only when the Starbase Extended source
   object has a simple AI-weight scope and generated references remain ok.
4. **Economic-plan reserve support** for starbase defense spending, expressed in
   Director-owned `basic_economy_plan` subplans rather than new ship-size or UI
   rewrites.
5. **Research/unlock pressure** for Starbase Extended defense unlocks where the
   technology object is already modeled in the Director unlock pipeline and the
   reference audit can prove the object exists.

## Forbidden Or Deferred Paths

Do not generate these in a T22/T23 continuation without a separate object graph,
conflict review, and UI/runtime proof:

- `common/ship_sizes` starbase or orbital-ring objects.
- `common/section_templates` starbase or orbital-ring sections.
- `common/component_sets` or `common/component_templates` Starbase Extended or
  NSC3 starbase components.
- Starbase GUI/GFX slot patches such as starbase view or module icon layout.
- Broad Starbase Extended full-object rewrites outside the existing selected
  module/building set.
- Any assumption that Universal Resource Patch substitutes for Universal
  Modifier Patch or Expanded Mods Base.
- Any runtime claim that starbase UI slots, save/reload, or AI construction
  choices are correct without an approved launch artifact.

## Irony Check Status

Irony Mod Manager is installed and the executable reports version
`1.27.192.32361` / product version `1.27.192+7e69c2ddbd`. The previous project
artifact records an Irony Conflict Solver Analyze Only review for the active
collection, but that July 4 review only covered `common\ai_budget` Director
conflicts.

For this T22 slice, no fresh Irony UI Analyze Only export was produced because
Computer Use was not exposed in this thread and the Irony executable did not
surface a CLI help/analyze command. The active conflict matrix is therefore the
object-level conflict evidence for Starbase Extended. Treat this as sufficient
for research planning, but not as a live UI or save/reload proof.

## Acceptance Decision

T22 acceptance is met for a research-only surface study:

- Starbase Extended identity is proven from active source roots and descriptor
  fields.
- Starbase module/building scope evidence is validated and summarized.
- Active conflict rows identify high-risk neighboring surfaces and current
  Director-owned starbase override winners.
- Safe future AI levers and forbidden paths are explicitly separated.
- Runtime/UI proof is not claimed.

