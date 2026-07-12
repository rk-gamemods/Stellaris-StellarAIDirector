# Identity-aware federation families

Target: active Pegasus 4.4.4 vanilla federation types. This slice extends the proven `federation_type.ai_weight` approach from Research Cooperative to four exact vanilla final winners while preserving all legality, DLC, cohesion, succession, law, acceptance, personality, and relative-power rules.

- Galactic Union (`default_federation`): Diplomatic primary +100 / secondary +50; peaceful nonexistential Defensive primary +50 / secondary +25.
- Trade League (`trade_federation`): Megacorp +125; Diplomatic primary +75 / secondary +40.
- Martial Alliance (`military_federation`): Defensive primary +100 / secondary +50; Conquest primary +75 / secondary +40.
- Hegemony (`hegemony_federation`): Conquest primary +100 / secondary +50; Barbaric Despoiler +75; Rogue Servitor +75.

These are additive preferences, not exclusive trees. Conquest can compare Martial Alliance and Hegemony through vanilla personality, relative-power, and availability signals; Diplomatic Megacorps can blend Trade League signals. Balanced empires retain vanilla behavior. Every new line requires conflict-free eligible H08 classification, excludes Extermination and Inward Perfection, and is disabled during survival, recovery, short-runway core deficit, or catastrophic collapse. Research Cooperative identity modifiers now carry the same Extermination/Inward exclusions. Its new H08 identity contribution is bounded at +150 for a compatible primary-plus-secondary blend, but the copied vanilla/Director object already contains other positive additions totaling as much as +710; a compatible combined path can therefore reach +860. The +150 bound must not be described as a total `ai_weight` ceiling.

## Top five risks and controls

1. **Federation monoculture:** one family could dominate every eligible empire. Control: family-specific bounded additions preserve vanilla personality/relative-power terms and allow competing compatible families.
2. **Incompatible extermination pressure:** a secondary vector could accidentally encourage federation formation. Control: every new family and Research Cooperative identity modifier explicitly requires `staid_archetype_extermination = no`.
3. **Inward Perfection leakage:** a defensive identity could receive federation pressure despite isolationist doctrine. Control: `staid_identity_inward_perfection = no` on every new modifier.
4. **Recovery distraction:** federation identity could overrule urgent economic/security conditions. Control: survival, recovery, core-deficit-short-runway, and collapse states disable family modifiers.
5. **Full-object/source drift:** copied federation objects could lose new vanilla behavior. Control: exact five-object SHA-256 locks (including Research Cooperative), shared full-object renderer, zero-overlay parity for the four new family objects, and focused source-hash tests.

## Boundary and rollback

No diplomatic action, invitation, acceptance, trust, opinion, pact, rivalry, federation creation, event, on_action, or persistent state is changed. Static proof covers exact objects, source hashes, additive modifiers, compatibility and safety gates, generated parity, and parser validity. Runtime observation must prove proposal, acceptance, formation, conversion, and retention choices.

Rollback is one fine-grained commit removing the four family rows/modifiers while retaining Research Cooperative behavior and all earlier identity consumers.
