# Identity-specific specialist subject preferences

Target: Stellaris Pegasus 4.4.4 active stack. Live inventory on 2026-07-12 had 116 enabled mods and the Director last; no enabled mod replaces the targeted vanilla specialist preset IDs. More Events Mod adds unique agreement presets and remains untouched.

## Native surface and complete proposal families

The native selection surface is `common/agreement_presets` through evaluator-side `overlord_weight` and `subject_weight`. `overlord_weight` evaluates the prospective overlord with `FROM` as the subject; `subject_weight` evaluates the prospective subject with `FROM` as the overlord.

The behaviorally complete surface is eighteen objects, not only the three visible parent presets. Each Bulwark, Scholarium, and Prospectorium family also has five hidden AI proposal variants (`nice_01`, `nice_02`, `mean_01`, `mean_02`, `mean_03`) whose base weights can dominate the parent. Four focused generated files preserve the exact source-file-local `@` constants and full objects, with an expected logical SHA-256 for every object. Generation fails closed if any active source object drifts.

Defensive identity prefers Bulwark, Research prefers Scholarium, and Gestalt Growth prefers Prospectorium. The resolved primary factor is 1.15 and lead-secondary factor is 1.05. Both apply to positive overlord proposal weights. Subject-side factors apply only to the parent and `nice_01`/`nice_02` variants with positive base weights; the three negative `mean_*` subject weights remain unchanged so multiplication cannot make exploitative terms more acceptable or produce misleading negative-weight behavior.

Each side-specific weight block already establishes whether the current evaluator is the prospective overlord or subject. The modifiers deliberately do not require current-state `is_overlord`/`is_subject`, because those predicates are false during a first agreement proposal before the relationship exists. Each factor instead requires a conflict-free eligible resolved identity, safe basic-economy runway, and no survival, recovery, catastrophic-collapse, or core-deficit short-runway state. Existing potential, terms, resource transfers, loyalty, integration, war obligations, acceptance, technology-ratio checks, and both-side Nomad/Inward Perfection exclusions remain byte-equivalent to the active source after removing the inserted modifier lines.

## Top five risks and controls

1. **Incomplete specialist family:** patching only visible parents would be dominated by hidden AI variants. Control: fixed manifest and tests require all six objects for each of three families—exactly eighteen.
2. **Full-object drift or alias collision:** copied presets may change or file-local `@` values may differ. Control: per-object hashes, four source-aligned outputs, copied required aliases, fixed output allowlist, and fail-closed generation.
3. **Negative subject-weight inversion:** multiplying a negative exploitative-terms weight can produce unintended acceptance pressure. Control: no identity modifier is inserted into `mean_01`, `mean_02`, or `mean_03` `subject_weight`; original negative values remain exact.
4. **Economic harm from specialization:** subsidies or taxes may be unaffordable even when the identity matches. Control: safe-runway and recovery/deficit gates constrain the preference; native term scoring, acceptance, and potential remain authoritative.
5. **Nomad, special-contract, or generic-vassal breakage:** broad preset ownership could collide with Satrapy, Subsidiary, Vassal, Tributary, origin, or Nomad behavior. Control: no generic, subjugation-initialization, Nomad, satrapy, relic, purger, agreement-term, or diplomatic-action object is copied or changed.

## Static/runtime boundary and rollback

Static proof covers exact active source hashes, four-file/eighteen-object completeness, source-local aliases, side-specific evaluator blocks without erroneous current-role guards, bounded factors, negative subject-weight preservation, full-object fidelity, original legality/terms, parser/reference validity, and absence of events or state mutation. It cannot prove proposal timing, chosen term harshness, counterpart acceptance, conversion completion, loyalty trajectory, or long-run subject/overlord economics.

Runtime acceptance records both countries' resolved/secondary identities, role, proposed preset and variant, complete terms, subsidies/taxes, acceptance reasons, monthly economy before/after, loyalty, conversion state, and renegotiation outcome. No game launch or save mutation was performed.

Rollback is one fine-grained commit deleting the four generated preset files and their focused generator/tests without affecting prior diplomacy, federation, stance, economic, claim, or static-defense identity consumers.
