# Progenitor Hive assembly planning

Target: active Pegasus 4.4.4 vanilla `building_spawning_pool` and `building_offspring_nest`. The Director already contained Progenitor-specific construction logic, but the focused H08 renderer omitted both objects, leaving the modeled origin behavior inert.

This slice adds the exact source-hash-locked pair to the existing focused assembly artifact. Ordinary Hives receive a bounded factor 1.25 spawning-pool preference. Progenitor Hives receive factor 0 for the ordinary spawning pool and factor 1.5 for their legal offspring nest. The previously dormant 6 and 8 multipliers were reduced before activation. Original legality, jobs, cost, upkeep, conversion, destruction, prerequisite, and origin restrictions remain authoritative, and the shared population-assembly readiness veto still applies.

## Top five risks and controls

1. **Wrong or drifting source objects:** copied origin buildings could lose vanilla restrictions. Control: exact two-object hashes fail closed.
2. **Both assembly chains compete:** Progenitors could attempt the ordinary pool and offspring nest. Control: explicit factor 0 on the ordinary pool for `origin_progenitor_hive`.
3. **Growth crowds out urgent construction:** assembly can consume a scarce slot during economic stress. Control: shared `staid_pop_assembly_snowball_ready` veto and preserved vanilla slot/destruction rules.
4. **Extreme dormant weights:** the unmaterialized model used factors 6 and 8. Control: activation uses bounded 1.25 and 1.5 factors.
5. **Unreviewed assembly families leak in:** machines and clone vats are modeled but not yet origin-audited. Control: fixed four-object artifact allowlist still excludes machine assembly and clone vats.

## Proof boundary and rollback

Static proof covers source hashes, the Progenitor mutual exclusion, exact weights, shared readiness gate, legal-source markers, excluded assembly families, parser validity, and focused generator idempotence. Runtime observation must prove legal queue selection, offspring-drone output, and sustainable upkeep. Rollback is one fine-grained commit.
