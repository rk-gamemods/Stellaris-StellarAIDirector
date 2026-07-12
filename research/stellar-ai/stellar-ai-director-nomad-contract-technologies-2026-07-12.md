# Nomad Arkship contract-unlock technology preferences

Target: active Pegasus 4.4.4 vanilla `tech_arkship_planetary_refinery`, `tech_arkship_system_scanner`, and `tech_arkship_stellar_igniter`. These Nomad-only rare technologies unlock specialization-relevant Contracts but have empty vanilla `ai_weight` blocks and no Workshop duplicate in the inspected stack.

The Director adds factor 1.5 only for the matching starting Arkship specialization: civilian → planetary refinery, science → system scanner, military → stellar igniter. Every modifier also requires `is_nomadic = yes`. `tech_arkship_exodus_jump` remains untouched because it has no source-proven specialization mapping or urgency gate.

## Top five risks and controls

1. **Contract unlock mistaken for Contract execution:** drawing a technology cannot guarantee use. Control: claims are limited to research selection; execution remains runtime/engine-owned.
2. **Wrong specialization receives pressure:** a generic Nomad factor would blur Arkship roles. Control: exact starting-Arkship flags and one-to-one tests.
3. **Rare technology crowding:** factor 1.5 could displace a more urgent draw. Control: bounded specialization factor and preserved vanilla potential/prerequisites.
4. **Source drift or collision:** another mod could redefine the technology. Control: exact three-object source hashes fail closed; current Workshop inventory found no duplicates.
5. **Speculative Exodus pressure:** the fourth Contract technology lacks a defensible role mapping. Control: explicit absence test for `tech_arkship_exodus_jump`.

## Proof boundary and rollback

Static proof covers exact objects, source hashes, zero-overlay source parity, specialization flags, Nomad scope, bounded factors, Exodus exclusion, parser validity, and focused generator idempotence. Waystation placement, Wayline routing, Contract execution, Arkship movement/harvesting, and Operational Reserve remain runtime-only engine operations. Rollback is one fine-grained commit.
