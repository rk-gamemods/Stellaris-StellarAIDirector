# H08 behavior-consumer completion boundary

Authority: current live-linked branch `codex/stellar-ai-director-research-refinements` through `68e4af3d`, active Pegasus 4.4.4 files, the enabled 116-mod launcher stack, generated artifacts, validators, and user-provided save evidence. This is a research/support ledger with no separate rendered counterpart.

The H08 static behavior-consumer program is implemented across every named identity family through native AI surfaces. This does **not** prove runtime executor outcomes. The full goal remains open until the runtime claims below are observed or otherwise resolved.

## Identity coverage

| Identity | Implemented native consumers | Remaining proof |
|---|---|---|
| Extermination | economy, fleet/technology pressure, armies, traditions, personalities/stances, military megastructures | target selection and war completion |
| Conquest | economy, outposts/claims, fleet/technology pressure, armies, traditions, Martial Alliance/Hegemony, military megastructures | declarations, target choice, execution |
| Gestalt growth | economy, expansion, technology, megastructures, ordinary-Hive Synchronicity and Expansionist posture | actual stance and construction choices |
| Defensive/isolationist | economy, Isolationist posture, static defense, expansion, traditions, megastructures | actual investment mix |
| Research | economy, technology, Tech-World contract, Cooperative posture, Research Cooperative, traditions/perks, science megastructures | designation conversion and executor follow-through |
| Diplomatic/federation | economy, Cooperative posture, Diplomacy tradition, federation-family weights | proposal timing, acceptance, votes |
| Balanced | neutral fallback plus shared legality/recovery/runway controls | runtime neutrality |
| Megacorp/trade | economy, Mercantile posture/tradition, Trade League, Arc Welders, economy megastructures | commercial proposal timing |
| Subject/overlord | role labels and 18 specialist agreement presets | proposal/acceptance behavior |
| Special origins | Arc Welders, Mechanist assembly, Progenitor assembly, Common Ground/Hegemon routing, Tree of Life reserve, slaver/Khan raiding | actual construction and origin-chain execution |
| Nomad/Arkship | settled-classifier exclusion, Waystation budgets, perk specialization, three Contract-unlock technology preferences | Waylines, Contracts, movement, harvesting, Operational Reserve |
| Machine/Servitor/Assimilator | exact identities, economy, traditions, armies, Cooperative/Belligerent posture, federation behavior | policy reevaluation and execution |
| Hive/Swarm | ordinary-Hive growth consumers; Devouring Swarm economy, armies, Hunger posture and aggressive personality | operational war behavior |
| Pacifist/Inward Perfection | defensive identity plus economy, Isolationist posture, traditions, static defense and megastructures | runtime investment mix |
| Raider/Despoiler | economy, claims, armies, bombardment, traditions and military megastructures; no forced Nihilistic Acquisition | actual raiding behavior |
| Reforms/mixed cases | stateless recomputation, one primary plus bounded lead secondary, no persistent identity labels | engine policy reevaluation timing |

## Behavior-domain boundary

| Domain | Static implementation | Runtime boundary |
|---|---|---|
| Economic plans | identity plans below legality, resource-use, recovery and runway controls | plan/executor response |
| Fleet versus technology | identity budgets and bounded technology preferences | divergence over time |
| Fleet composition | sub-Battleship demand becomes zero after Battleships; larger hulls remain eligible | existing-template refresh |
| Fleet reinforcement | affordability and native `ai_ship_data` demand surfaces | template creation, target expansion and queue scheduling |
| Shipyards | unlock/megastructure routes exist | idle-slot scheduling and cancellation |
| Naval fill | underfill affordability and late-hull demand | utilization, saturation and over-cap response |
| Static defense | exact starbase building/module weights | placement and completed defense |
| Expansion/claims | native budgets and global broad-reach distance policy | candidate execution and target distance |
| War posture | personalities, stances, budgets and broad reach | declarations, near/far preference and war completion |
| Diplomacy | stances and federation families | actor proposal desire is not exposed on reviewed pact/rivalry objects |
| Traditions/perks | primary, secondary, defining identity, origin and Nomad overlays | draw/selection outcomes |
| Megastructures | exact start-stage identity sequencing | queues and completed sequencing |

## Proven no-safe-hook findings

The active winners for `action_form_research_agreement`, `action_form_commercial_pact`, `action_form_defensive_pact`, and `action_make_rival` are vanilla `common/diplomatic_actions/00_actions.txt`; all 116 enabled mod roots contain no duplicates.

- Pact objects expose legality and recipient `AI_acceptance_base_value = -50`, not actor proposal desire.
- Rivalry is `auto_accepted = yes`, which is acceptance behavior, not desire.
- None exposes `ai_weight` or `ai_will_do`.
- Editing `ai_acceptance` would change recipient/player-facing responses without making the actor propose anything.

Therefore `common/diplomatic_actions` remains forbidden in the Director until a verified actor-side native consumer exists.

No verified per-identity war-target distance surface exists. Global policy remains broad reach (`MAX_DISTANCE = 300`) with nearer preference beginning at 25; this must not be converted into a hard empire-radius cutoff.

No safe data consumer was found for Wayline placement, Contract execution, Arkship orders, fleet-template refresh, shipyard scheduling, or construction/designation executor commands. Implementing those through events, orders, free resources, or persistent helper state would violate the native-AI-only boundary.

## Runtime acceptance queue

Use copied/read-only saves or an explicitly authorized observer run:

1. Post-H07 outposts: scanned unclaimed candidates, constructor routing, queue creation, affordability and threat IDs.
2. Threatened peacetime fleets: template targets, current counts, reinforcement deficit, queued hulls and naval utilization over 2–5 years.
3. Late fleets: verify sub-Battleship target demand reaches zero after Battleships and capital hulls dominate new construction.
4. Identity divergence: matched research, conquest, defensive, trade, gestalt and extermination empires; compare budgets, technology, traditions and completed construction.
5. War distance: compare selected near and distant targets without imposing a hard radius.
6. Nomads: specialization tech draws, Waystation spending, Contracts, Waylines and Arkship operations.
7. Reforms: verify identity and policy choices recompute after civic, authority or government changes.
8. Performance: pulse cost, candidate counts, fleet counts and late-game scheduling.

## Top five residual risks

1. **Static-to-runtime overclaim:** weights can be correct while engine executors remain idle. Control: keep runtime items open.
2. **Acceptance/desire confusion:** recipient fields can be mistaken for proposal hooks. Control: preserve the diplomatic-action prohibition.
3. **Template inertia:** corrected hull demand may not refresh serialized templates. Control: inspect per-hull target/current/reinforcement evidence.
4. **Version drift:** evidence is local 4.4.4 while the policy target is 4.4.5. Control: re-hash and reconstruct winners before a 4.4.5 release.
5. **Active-stack changes:** newly enabled mods may replace copied objects. Control: rerun winner/conflict inventories and fail-closed source hashes.

Rollback remains commit-granular to locked baseline `78627926`; do not squash the fine-grained H08 slices.
