# Identity-specific diplomatic stances

Target: Stellaris Pegasus 4.4.4 active stack. The Director already owns the generated full `diplomatic_stance` policy object, so this slice adds no new overwrite ID or production file.

## Behavior

- Primary diplomatic, lead-secondary diplomatic, primary research, lead-secondary research, and subject-role vectors independently prefer the legal Cooperative stance.
- Megacorps independently prefer the legal Mercantile stance.
- Primary and lead-secondary defensive vectors prefer the legal Isolationist stance only when the empire is at peace, not a federation member, not a subject, and not under active native war posture.
- Nomad stance variants remain parent-owned in this slice because their contract economy and diplomacy require separate evidence.

The factors are native `ai_weight` multipliers, not policy effects. Vanilla option `potential`, `valid`, and policy-change rules remain intact. The largest modeled Cooperative overlap is `1.40 * 1.10 * 1.15 = 1.771`, which is a preference rather than a hard directive.

## Top five risks and controls

1. **Multiplicative oversteer:** several compatible vectors could collapse to one stance. Control: fixed factors from 1.10 to 1.40, explicit maximum-overlap test below 1.80, and no factor-zero identity directive.
2. **Isolationism trapping allies or subjects:** a defensive vector could abandon obligations. Control: Isolationist identity factors require no federation, no subject role, and no active war posture.
3. **Peaceful identity suppressing necessary war posture:** Cooperative could outlive changed circumstances. Control: the existing `factor = 0` native-war-posture exit remains in the same option and dominates every positive identity multiplier.
4. **Illegal special-country choices:** genocidal, Inward Perfection, Nomad, or modded governments could receive an invalid option. Control: source `potential`/`valid` blocks are preserved byte-for-byte; identity factors target only standard non-Nomad option IDs.
5. **Full-object drift or collision:** the copied policy could become stale or lose to another mod. Control: verified-source reconstruction, existing full-object ownership, fixed single-output generator, parser/tests, and active-playset final-load evidence. Runtime selection remains unproven statically.

## Proof and rollback

Static validation proves source-preserving generation, exact option targeting, bounded factors, safety exclusions, no Nomad leakage, and no event/state mutation. It cannot prove when the engine reevaluates policy or which stance wins among all legal options. Runtime acceptance compares stance choices after a fresh policy evaluation across mixed identity fixtures.

Rollback is one fine-grained commit that restores the prior generated policy weights without affecting the H08 classifier or economic consumers.
