# Identity-specific tradition and ascension preferences

Target: Stellaris Pegasus 4.4.4 active stack. This slice extends the Director's already-reviewed copied ascension-perk, tradition-category, and selectable-tradition objects through their existing native `ai_weight` transformers.

## Behavior

Resolved Research prefers Technological Ascendancy and Discovery; resolved Diplomatic prefers Diplomacy; resolved Defensive prefers Adaptability; resolved Conquest and Extermination prefer Supremacy and Lord of War. The single lead-secondary vector contributes a smaller preference to the same object family only when it is not the resolved primary.

Defining civics remain independent consumers: Megacorp prefers Mercantile, Inward Perfection prefers Adaptability, Barbaric Despoiler and Assimilator prefer Supremacy, and Rogue Servitor prefers Diplomacy. This preserves dedicated civic behavior while still allowing a different resolved primary and secondary to shape other legal choices.

All identity multipliers are between 1.05 and 1.15. Existing object `potential`, prerequisites, route readiness, survival, recovery, catastrophic-collapse, and core-deficit gates remain authoritative. No adoption/finish reward, unity grant, perk slot, or policy effect is changed.

## Top five risks and controls

1. **Illegal strategy selection:** an identity could appear to force an unavailable tree/perk. Control: copied parent `potential`, `possible`, prerequisites, and draw rules remain; only legal native weights are multiplied.
2. **Primary/secondary double counting:** hard evidence or same-vector secondary could stack. Control: consumers use resolved `staid_archetype_*`, never `hard_*`; each lead-secondary trigger requires that archetype not be primary.
3. **Defining-civic oversteer:** direct civic, primary, and secondary vectors can overlap. Control: each factor is at most 1.15 and object-specific; the highest reviewed overlap is 1.27008, and no factor-zero directive or automatic grant exists.
4. **Recovery distraction:** long-term strategy could outrank survival. Control: all identity modifiers require survival, recovery, catastrophic-collapse, and core short-runway modes to be false plus the existing route gate.
5. **Full-object/source drift:** copied parent objects could become stale or collide. Control: current route-source reconstruction, fixed five-output archetype generator, additive overlay-vs-zero tests, parser/reference validation, and final active-stack load position.

## Proof and rollback

Static validation proves only additive AI-weight insertion against the dynamically rendered zero-overlay baseline, per-factor bounds, resolved primary/secondary/defining triggers, legal source preservation, and absence of state mutation. Runtime acceptance compares completed tradition and ascension choices across classified empires; it must not infer success from generated weights alone.

Rollback is one fine-grained commit restoring the prior two-output archetype generator and parent strategy weights while leaving diplomatic, economic, army, and territorial identity consumers intact.
