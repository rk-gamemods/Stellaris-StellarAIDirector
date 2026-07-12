# Machine-subtype diplomatic stances

Target: active Pegasus 4.4.4 policy objects. Direct diplomatic-action proposal weights are not exposed on the inspected final winners: rivalry, defensive/commercial/research pacts, and federation invitations provide legality and recipient acceptance, not an actor `ai_weight`. Changing acceptance would affect recipients and players without creating proposal desire, so the Director continues to avoid `common/diplomatic_actions`.

The existing full-object `diplomatic_stance` policy is a proven native choice surface. This slice adds:

- Rogue Servitor: factor 1.25 for Cooperative while at peace, outside existential security and native-war posture, and with valid conflict-free H08 classification.
- Assimilator: factor 1.25 for Belligerent only outside survival, recovery, core-deficit-short-runway, and catastrophic-collapse states, with valid conflict-free H08 classification.

Determined Exterminator and Devouring Swarm are unchanged because vanilla already hard-locks their unique Extermination and Hunger stances at weight 100.

## Top five risks and controls

1. **Full-object policy collision:** another enabled mod could own the same policy. Control: retain the existing Director final-winner file and source-preservation tests; no new policy object is introduced.
2. **Servitor defense suppression:** Cooperative could persist during danger. Control: war, existential security, and native-war posture all disable the subtype preference.
3. **Assimilator recovery aggression:** Belligerent could consume diplomatic/economic bandwidth during collapse. Control: survival, recovery, core deficit, and collapse gates are authoritative.
4. **Homicidal invalid-option leakage:** generic subtype logic could interfere with Hunger/Extermination. Control: exact Servitor/Assimilator triggers only; no Swarm or Exterminator modifier.
5. **Multiplicative stacking:** subtype preference composes with resolved primary/secondary identity and role modifiers. Control: factor is limited to 1.25 and existing threat/recovery factor-zero choices remain dominant; runtime observation must verify reevaluation.

## Boundary and rollback

No pact, rivalry, invitation, acceptance, opinion, trust, event, on_action, or state mutation changes. Static proof covers exact option placement, conflict/eligibility and safety gates, additive policy rendering, preserved legality, and the continued absence of `common/diplomatic_actions`. Runtime proof is required for stance reevaluation and downstream proposal behavior.

Rollback is one fine-grained commit removing the two inserted policy modifiers while retaining all prior stance behavior.
