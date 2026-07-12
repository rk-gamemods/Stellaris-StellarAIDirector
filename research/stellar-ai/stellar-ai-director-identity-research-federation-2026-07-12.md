# Identity-aware Research Cooperative preference

Target: active Pegasus 4.4.4 stack with Federations DLC availability preserved by the vanilla `research_federation` object. This slice adds resolved H08 Research and Diplomatic identity tie-breakers to the existing Director-owned Research Cooperative `ai_weight` only.

Research and Diplomatic primary vectors each add 100; their lead-secondary vectors each add 50. A mixed empire can therefore combine a primary and the other vector's secondary for at most +150 identity weight. Existing +250 route readiness, science/runway/materialist/tradition signals, federation legality, DLC checks, acceptance, cohesion, laws, succession, and member behavior remain authoritative. Identity conflict or ineligible country classification prevents every new modifier.

## Top five risks and controls

1. **Federation monoculture:** identity weights could make every eligible empire choose Research Cooperative. Control: +100/+50 are bounded below the existing +250 route signal and do not alter base legality or alternative federation objects.
2. **Mixed-vector overstacking:** Research and Diplomatic signals can combine. Control: primary/secondary classification remains bounded; the maximum new mixed contribution is +150.
3. **Recovery or economic mismatch:** an identity label alone may not make research cooperation useful. Control: every identity modifier also requires the existing `staid_research_diplomacy_priority_ready` route gate, which owns current readiness.
4. **Scope inversion:** federation `ai_weight` evaluates the prospective country through `from`. Control: all four modifiers retain the source-proven `from` country scope and focused tests assert the exact generated object.
5. **Diplomatic coercion:** changing action acceptance or using events could force unwanted federation formation. Control: no diplomatic action, opinion, trust, acceptance, event, on_action, pact, rivalry, or federation-state mutation is added.

## Static/runtime boundary and rollback

Static proof covers one exact final-winner object, additive overlay parity, resolved primary/secondary triggers, conflict/eligibility/readiness gates, bounded contribution, parser validity, and absence of diplomatic-action overrides or state mutation. Only runtime observation can prove which federation is proposed, formed, accepted, or retained.

Rollback is one fine-grained commit removing the four identity modifiers and the federation artifact from the focused archetype overlay renderer while preserving the pre-existing Research Cooperative route weights.
