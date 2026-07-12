# Identity-specific static-defense preference

Target: Stellaris Pegasus 4.4.4 active stack, with the project 4.4.5 policy treated as a separate future revalidation target. Live launcher inventory on 2026-07-12 contained 116 enabled mods with no missing descriptors; NSC3 loaded at position 70, Starbase Extended 3.0 at 71, and the launcher-linked Stellar AI Director last at 115.

## Final-winner scope and behavior

The Director already owns copied, final-winner AI-weight objects for four starbase buildings and ten Starbase Extended modules, including five orbital-ring defense modules. This slice changes only those existing `ai_weight` blocks. It does not add or alter starbase levels, starbase types, slots, ship sizes, sections, components, defense platforms, upgrade paths, cooldown effects, Arkships, or Waystations.

The resolved Defensive vector adds a 1.15 preference, its lead-secondary vector adds 1.05, and Inward Perfection adds 1.10. Primary and same-vector secondary are mutually exclusive; the largest reviewed identity/civic overlap is 1.265. Every modifier executes from the existing starbase AI surface through explicit `owner` country scope and requires a conflict-free eligible identity, `staid_static_defense_investment_ready`, and no survival, recovery, catastrophic-collapse, or core-deficit short-runway state. Existing parent `potential`, prerequisites, module-count limits, and Director factor-zero readiness veto remain authoritative.

No Conquest or Extermination factor is added. Those identities retain the existing threat/economy-gated defense behavior without turning every aggressive empire into a static-fortification specialist.

## Top five risks and controls

1. **Slot crowd-out:** stronger defense weights could displace shipyards, trade, detection, or economic modules. Control: factors are at most 1.15, apply only after the common defense readiness gate, and modify no slot count or factor-zero parent condition.
2. **Interior overbuilding:** a country-level identity cannot identify the best chokepoint by itself. Control: preserve each parent object's starbase-scope scoring and legality; runtime acceptance separates border/chokepoint, shipyard, trade, and interior stations.
3. **Economic overreaction:** defense spending could starve fleets or colonies during a deficit. Control: the existing readiness trigger requires safe alloy/energy economy and threat/defensive strategy; all new factors shut off in survival, recovery, collapse, and short-runway core deficit.
4. **Compatibility collision:** overriding Starbase Extended, NSC3, ESC, Arkship, or Waystation graphs could break slots or references. Control: use only the fourteen already-copied final-winner building/module objects; no level/type/section/component/Arkship/Waystation surface is added to Director ownership.
5. **Identity stacking:** defensive primary, secondary, or Inward Perfection could multiply excessively. Control: primary and same-vector secondary are mutually exclusive, individual factors are bounded, and the reviewed maximum is 1.265.

## Validation and rollback boundary

Static proof covers current launcher roots, dated conflict/source datasets, final generated object IDs, preserved parent blocks, explicit owner scope, bounded factors, recovery gates, additive zero-to-production generation, references, and absence of state mutation. It cannot prove the executable's chosen station, module competition, upgrade timing, orbital-ring construction, or fleet-versus-fortification outcome.

Runtime acceptance records starbase role/location, available slots, candidate legality, selected module/building, construction queue, alloy/energy runway, threat, identity classification, and competing shipyard/trade/economic choices. No game launch or save mutation was performed for this slice.

Rollback is one fine-grained commit removing the identity modifiers and the two defense files from the focused archetype overlay allowlist while retaining the prior parent-safe static-defense implementation.
