# Ordinary Hive Synchronicity preference

Target: active Pegasus 4.4.4 vanilla `tradition_synchronicity`. Existing Director consumers already distinguish Devouring Swarms from ordinary Hives across personality, Hunger stance, federation exclusion, economy, armies, fleet pressure, claims, technology, megastructures, and defense. This slice fills the one remaining source-proven strategy gap.

`staid_identity_ordinary_hive` requires a default, non-Nomadic, non-Wilderness Hive empire without `civic_hive_devouring_swarm`. It adds a factor 1.12 tie-breaker to the native Synchronicity category only when identity classification is conflict-free and the empire is outside survival, recovery, core-short-runway deficit, catastrophic collapse, and native war posture. The factor changes neither availability nor any tradition effect.

## Top five risks and controls

1. **Wrong final-winner object:** an inactive Workshop trigger-undercoat mod also defines Synchronicity. Control: current active stack uses vanilla; exact vanilla source hash fails closed. Reconstruct the winner if that mod is enabled.
2. **Classifier leakage into Swarms:** extermination Hives must not receive the ordinary-Hive preference. Control: explicit civic exclusion plus mutual-exclusion tests.
3. **Military distraction under threat:** Synchronicity must not suppress urgent war traditions. Control: native-war, survival, recovery, deficit, and collapse gates.
4. **Weight stacking:** other identity vectors could compound unexpectedly. Control: one defining factor at 1.12, within the existing strategy ceiling of 1.15.
5. **Static/runtime ambiguity:** an AI weight cannot guarantee category selection. Control: static proof is limited to source, scope, weight, and gates; runtime acceptance must observe actual tradition choices.

## Proof boundary and rollback

Static validation covers classifier shape, source hash, exact modifier, safety gates, absence from Devouring Swarm, parser validity, and focused generator idempotence. No event, state, effect, or individual tradition is changed. Rollback is one fine-grained commit.
