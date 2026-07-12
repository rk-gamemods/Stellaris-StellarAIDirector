# Ordinary Hive diplomatic growth posture

Target: the Director-owned full `diplomatic_stance` object copied from active Pegasus 4.4.4 vanilla. Ordinary Hives already differ from Devouring Swarms across economy, armies, personalities, Hunger stance, federation eligibility, traditions, fleet pressure, claims, technology, megastructures, and defense, but their peaceful growth posture remained generic.

A conflict-free eligible `staid_identity_ordinary_hive` whose resolved primary is Gestalt Growth receives a bounded factor 1.15 preference for `diplo_stance_expansionist`. It applies only while independent, outside a federation, at peace, outside native war posture, and outside survival, recovery, core-short-runway deficit, or collapse. Devouring Swarms are excluded by the ordinary-Hive classifier and receive no modifier.

## Top five risks and controls

1. **Swarm leakage:** total-war Hives must retain Hunger rather than Expansionist pressure. Control: exact ordinary-Hive classifier excludes the Devouring Swarm civic, plus absence tests.
2. **Federation incompatibility:** an established federation member should not be pushed toward a conflicting outward posture. Control: `has_federation = no`.
3. **Subject-role conflict:** subjects may need their contract posture rather than autonomous expansion. Control: `staid_role_subject = no`.
4. **War or economic distraction:** growth posture must not compete with survival decisions. Control: war, native-war, survival, recovery, deficit, and collapse gates.
5. **Overweighting:** a defining identity could dominate other stance signals. Control: one factor 1.15 tie-breaker, preserving all vanilla and Director option weights.

## Proof boundary and rollback

Static proof covers the exact option, identity and primary-route gates, exclusions, additive-only source diff, parser validity, and focused policy generation. Runtime proof must observe stance selection and subsequent proposal behavior; the modifier does not force diplomacy or expansion. Rollback is one fine-grained commit.
