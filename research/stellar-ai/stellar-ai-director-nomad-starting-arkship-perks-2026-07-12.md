# Nomad starting-Arkship ascension preferences

Target: active Pegasus 4.4.4 vanilla Nomads surfaces. Vanilla start effects persist exactly one of `starting_civilian_arkship`, `starting_science_arkship`, or `starting_military_arkship`; vanilla Nomad council agendas already consume those flags. The Director reuses them without adding state:

- Civilian Arkship: `ap_mastery_of_nature` factor 1.5.
- Science Arkship: `ap_technological_ascendancy` factor 1.5.
- Military Arkship: `ap_eternal_vigilance_nomads` factor 1.5.

Every modifier also requires `is_nomadic = yes`. The three vanilla source objects are hash-locked. `ap_technological_ascendancy` retains its existing settled Research route behavior; the Nomad modifier composes independently. The other two objects preserve their vanilla weights and receive only the matching factor.

The settled H08 classifier remains unchanged and continues to exclude Nomads. This is intentional: broadening `staid_archetype_eligible_country` would leak settled colony, claim, federation, and megastructure assumptions into mobile empires.

## Top five risks and controls

1. **Starting flag becomes stale after reforms:** starting specialization intentionally describes the Arkship foundation rather than current government. Control: reuse the vanilla agenda identity contract; do not invent mutable Director state.
2. **Perk overcommit:** a 1.5 preference might crowd out another legal perk. Control: bounded multiplicative preference only; vanilla potential, prerequisites, and alternative weights remain authoritative.
3. **Settled leakage:** a non-Nomad with a stray flag could receive the bias. Control: `is_nomadic = yes` is mandatory on all three modifiers.
4. **Wrong specialization crossover:** one starting flag could bias multiple perks. Control: exact one-to-one map and regression tests excluding the other two flags from each object.
5. **Full-object drift or collision:** vanilla/overhaul changes could invalidate copied objects. Control: active playset showed vanilla as final winner; per-object hashes fail closed and focused rendering preserves parent content.

## Boundary and rollback

No event, on_action, Wayline order, route placement, contract mutation, ship size, starbase, megastructure, or helper flag is added. Static proof covers source hashes, exact three-object allowlist, correct flag/Nomad gates, bounded factors, parser validity, and settled-overlay isolation. Runtime acceptance must observe perk choices across the three starting Arkship specializations.

Contracts, Wayline movement, route placement, and operational Arkship orders remain executable-owned/runtime surfaces under the native-AI-only rule. Rollback is one fine-grained commit removing these three modifiers and two dedicated route rows while retaining every settled identity consumer.
