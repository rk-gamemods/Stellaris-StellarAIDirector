# Stellar AI Director First-75 Route Trigger Review

Date: 2026-07-09

Task card: T06 - First-75-year route trigger review

Target: Stellaris 4.4.5, `mods/StellarAIDirector`, generated standalone Director surfaces.

Runtime boundary: static review only. No Stellaris launch, observer run, or live launcher change was performed for this card.

## Sources Consulted

- Packet task card: `plans/stellar-ai-director-strategic-v2/CODEX_TASK_SLICES.md`, T06.
- Behavior model: `plans/stellar-ai-director-strategic-v2/AI_BEHAVIOR_DESIGN.md`, "Opening Route Classifier".
- Phase plan: `plans/stellar-ai-director-strategic-v2/IMPLEMENTATION_ROADMAP.md`, "Opening Economy And Research Compounding V2".
- Strategy hypothesis: `mods/StellarAIDirector/notes/stellar_ai_director_strategy_hypothesis_2026-07-08.md`, phases 2200-2225, 2225-2250, and 2250-2275.
- Generated trigger sources:
  - `tools/stellar_ai_director_lib.py`
  - `mods/StellarAIDirector/common/scripted_triggers/zzzz_staid_10_opening_strategy_triggers.txt`
  - `mods/StellarAIDirector/common/scripted_triggers/zzzz_staid_20_strategy_kernel_triggers.txt`
- Generated consumers:
  - `mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt`
  - `mods/StellarAIDirector/common/policies/zzzz_staid_10_opening_growth_policies.txt`
  - `mods/StellarAIDirector/common/edicts/zzzz_staid_10_opening_growth_edicts.txt`
  - `mods/StellarAIDirector/common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt`
  - `mods/StellarAIDirector/common/bombardment_stances/zzzz_staid_12_militarist_raiding_bombardment.txt`
  - `mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt`
- JDataMunch dataset: `stellar_ai_director_policy_matrix_20260706`.
- Prior runtime-log classifier output: `research/stellar-ai/stellar-ai-director-4-4-5-log-risk-report-2026-07-09.csv`.

## Trigger Families Present

The opening classifier is generated as reusable scripted triggers rather than persistent country flags or mutable external state:

| Trigger | Route role | Current support gate |
| --- | --- | --- |
| `staid_opening_direct_research` | Materialist, machine, or technocracy direct research opening | `staid_is_opening_phase`, `staid_can_afford_research_push` |
| `staid_opening_unity_to_research` | Spiritualist/priest/death-cult route into later research payoff | `staid_is_opening_phase`, `staid_has_safe_basic_stockpiles` |
| `staid_opening_military_to_pops` | Militarist/authoritarian productive aggression and pop-gain route | `staid_is_opening_phase`, `staid_has_safe_basic_stockpiles`, no alloy deficit |
| `staid_opening_hostile_fauna_clearance` | Early space-fauna clearance route | `staid_is_opening_phase`, `staid_has_safe_basic_stockpiles`, no alloy deficit |
| `staid_opening_defensive_tall_research` | Pacifist/xenophobe tall defensive research route | `staid_is_opening_phase`, `staid_can_afford_research_push` |
| `staid_opening_trade_to_research` | Xenophile/merchant trade-to-research support route | `staid_is_opening_phase`, `staid_has_safe_basic_stockpiles` |
| `staid_opening_hive_growth_research` | Hive growth/research route | `staid_is_opening_phase`, `staid_has_safe_basic_stockpiles` |
| `staid_opening_machine_growth_research` | Machine growth/research route | `staid_is_opening_phase`, `staid_has_safe_basic_stockpiles` |
| `staid_opening_nomad_arkship_research` | Nomad/Arkship research compatibility route | `staid_is_opening_phase`, `is_nomadic`, `staid_has_safe_basic_stockpiles` |
| `staid_opening_any_research_route` | Aggregate research-opening classifier | OR of non-military research-opening route triggers |

The shared strategy kernel also provides reusable support gates:

- `staid_is_opening_phase`: `years_passed < 75`.
- `staid_has_safe_basic_stockpiles`: no energy, minerals, food, or consumer-goods deficit, plus energy/mineral stockpile runway.
- `staid_can_afford_research_push`: collapse-safe and either stockpiles/snowball/spenddown pressure plus research-input runway/snowball/spenddown pressure.
- `staid_security_existential`: routes out of research preference during severe starbase or survival pressure.
- `staid_opening_route_research_priority`: aggregate gate for opening research routes or under-curve research state.

## Generated Consumer Coverage

Static search confirms generated consumers reference the opening route triggers across economy, policy, edict, AP, bombardment, and decision-state surfaces:

- Economic plans use direct research, trade-to-research, hive growth, machine growth, military-to-pops, and Nomad/Arkship route gates.
- Policies weight cooperative diplomacy, mercantile stance, expansionist stance, bombardment, and surrender behavior through route gates.
- Edicts weight `research_subsidies`, `encourage_free_thought`, `map_the_stars`, and basic-resource subsidies through opening/support gates.
- Ascension perks and bombardment stance surfaces reference the military-to-pops opening route for pop-acquisition payoff.
- Decision-state triggers reference military-to-pops and hostile-fauna clearance route gates for downstream strategy classifiers.

The policy matrix contains current route rows for T06-adjacent families:

| Route | Policy matrix rows |
| --- | ---: |
| `crowded_tall_route` | 1697 |
| `mega_engineering_core` | 1269 |
| `conquest_escape_route` | 657 |
| `research_throughput_infrastructure` | 270 |
| `pop_assembly_snowball_core` | 70 |
| `research_diplomacy_core` | 14 |

## Static Gaps For Follow-On Cards

This review supports the route-trigger layer, but it does not prove the first-75-year behavior is strong enough. The following gaps remain for the dependent cards:

- T07: research-world and lab construction pressure still needs a targeted pass. The route trigger can identify research-friendly empires, but construction/building pressure must prove that labs and research designations are actively favored when consumer goods, energy, and staffing are safe.
- T08: pop assembly is only indirectly represented by route families here. Hive, machine, robot, clone, spawning, and organic assembly paths need explicit construction/support review.
- T09: support-economy bridges need review. Current support gates prevent obvious deficit spirals, but the packet specifically calls for consumer-goods, energy, minerals, trade/logistics, and unstaffed-job safety.
- T10: unity-to-research has a route classifier, but traditions, APs, edicts, and downstream research payoff need a dedicated route pass.
- T11: research diplomacy has an opening aggregate and policy hooks, but research agreements, Research Cooperative preference, and lower-value federation avoidance need a safe-lane review.
- T18/T19/T20/T21: military-to-pops and hostile-fauna routes are named, but fleet payoff, clearance reserves, and war-chain value need separate proof.

## Log-Risk Carry-Forward

The 4.4.5 log-risk report contains Director-owned entries for `common/policies/zzzz_staid_10_opening_growth_policies.txt`, including copied `capital_scope` checks inside primitive diplomatic stance policy options. Vanilla `common/policies/00_policies.txt` has the same `capital_scope` blocks, so this T06 pass did not surgically change policy semantics inside a trigger-review card. The risk remains assigned to follow-on policy/diplomacy hardening, especially T11, and must be resolved or explicitly justified before live-test readiness.

## Validation

- Added deterministic unit coverage in `tools/tests/test_stellar_ai_director.py`: `test_opening_route_trigger_references_resolve_across_generated_surfaces`.
- The test asserts:
  - all required opening route triggers exist;
  - required shared kernel gates exist;
  - generated `staid_opening_*` references across `common/` resolve to generated route or kernel definitions;
  - generated opening/kernel triggers do not model the route classifier as `staid_opening_*` country flags.
- Focused validation passed:

```text
python -m unittest tools.tests.test_stellar_ai_director.GeneratedModValidityTests.test_opening_route_trigger_references_resolve_across_generated_surfaces
.
Ran 1 test in 18.740s
OK
```

## T06 Conclusion

T06 is satisfied for static route-trigger review: the first-75-year route classifier is generated, reusable across multiple generated AI surfaces, protected by reusable support gates, and now covered by a missing-reference test. It is not gameplay proof. The strongest remaining risks are downstream construction pressure, pop assembly, support-economy sufficiency, unity/research diplomacy payoff, and the policy-surface `capital_scope` runtime-log risk.
