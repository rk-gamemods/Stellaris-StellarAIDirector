# Stellar AI Director Computed Strategy Kernel Addendum

Date: 2026-07-07
Source input: `C:\Users\Admin\.codex\attachments\dcc318fd-e5d1-43a6-ae9b-91317c53a955\pasted-text.txt`
Related plan: `research/stellar-ai/stellar-ai-director-opening-research-policy-fleet-specialization-implementation-plan-2026-07-07.md`

## Purpose

This addendum incorporates the Web ChatGPT clarification pass without doing a broad plan rewrite. The full strategy scope remains alive. Nothing from the expanded plan should be narrowed, removed, or downgraded unless local vanilla/mod files, repo contracts, or explicit user instruction prove that narrowing is required.

The key correction is implementation shape:

- Use computed strategic state first.
- Use persistent state only where hysteresis, cooldowns, or memory are actually required.
- Keep runtime/scenario testing outside Codex validation unless the user explicitly asks for it.

## Version Target

The project should now treat Stellaris PC 4.4.5 live as the default target, while retaining a 4.4.4 inventory/compatibility mode for users who pin the previous stable version.

Evidence checked on 2026-07-07:

- Official Steam news for Stellaris says `Stellaris 4.4.5 patch released (2f57)` and that the update is ready for Steam, GOG, and MS Store: https://steamcommunity.com/app/281990/allnews/
- The official Steam news surface says 4.4.5 adds the Resource Abundance slider: https://store.steampowered.com/news/?appgroupname=Stellaris+-+Galaxy+Edition&appids=281990&feed=steam_community_announcements
- The local repo still has older guidance that defaulted to 4.4.4 stable, so generator validation must make version drift visible instead of silently assuming one version.

Implementation rule:

- If local installed files are 4.4.5, emit 4.4.5 artifacts.
- If local installed files are 4.4.4, emit 4.4.4-compatible artifacts or fail closed when a planned 4.4.5 hook is required.
- Do not use 4.5 beta fleet doctrine behavior as a 4.4.5 implementation dependency.

## Computed Strategy Kernel

The strategy kernel should be a library of generated predicates and optional scalar values, not a constantly mutating country-variable AI brain.

Computed state should cover:

- `staid_is_opening_phase`
- `staid_is_midgame_scaling_phase`
- `staid_has_safe_basic_stockpiles`
- `staid_can_afford_research_push`
- `staid_opening_direct_research`
- `staid_opening_unity_to_research`
- `staid_opening_military_to_pops`
- `staid_opening_defensive_tall_research`
- `staid_opening_trade_to_research`
- `staid_security_threatened`
- `staid_security_existential`
- `staid_megastructure_prereq_rush`
- `staid_megastructure_alloy_release`
- `staid_fleet_defensive_minimum`
- `staid_fleet_strategic_aggression`
- `staid_fleet_survival_emergency`

Preferred generated surfaces:

- `common/scripted_triggers/zzzz_staid_strategy_kernel_triggers.txt`
- `common/script_values/zzzz_staid_strategy_values.txt`, only after local syntax verification
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt`
- route-specific technology, building, district, policy, edict, and diplomacy `ai_weight` modifiers

Persistent state is allowed only for:

- doctrine lock-in, to prevent weapon-family flip-flopping;
- planet role locks, to prevent repeated specialization churn;
- megastructure attempt flags or cooldowns, to prevent repeated reservation for impossible structures;
- long cooldowns or hysteresis where computed triggers would oscillate too much.

Do not implement a generic mutable value such as `staid_current_route = 3` unless local evidence proves that route lock persistence is needed and that the chosen storage surface is stable.

## Verified Or Candidate 4.4.5 Hooks

These are not cuts. They are keep-and-verify items.

| Surface | Ruling | Implementation note |
| --- | --- | --- |
| `ai_building_set_affinity` | Keep, local inventory required | Use for colony type/building-set affinity after extracting actual colony type IDs and building-set IDs. |
| Zone/district specialization affinity | Keep, high-value static work | Prefer colony designation plus building-set affinity before any event-driven rebuild logic. |
| Colony/Carrier scopes | Keep, compatibility gate | Replace planet-only assumptions where Arkship/carrier-colony logic may apply. |
| `resource_stockpile_percent` | Keep, likely safe after local syntax check | Use for edict, storage, alloy, and megastructure affordability gates. |
| Optional economic subplans | Keep | Use optional subplans for soft priorities; do not encode hard gates as optional behavior. |
| AI storage reactions | Keep as context, not a hook | Use explicit storage weights and stockpile triggers instead of relying on hidden vanilla behavior. |
| Fleet upgrade logic | Keep as context, not a hook | Improve tech/component readiness; do not script direct fleet upgrades unless a control surface is verified. |
| `-logempirestats` | Keep as manual-test support | Build parsers and reports for user-run tests only; do not make scenario runs part of Codex validation. |
| Fleet automation / `has_automation_flag` | Later | Useful for automation mods, not first-slice empire scaling. |
| 4.5 fleet doctrine AI | Later / not 4.4.5 dependency | Do not depend on 4.5 beta behavior for this 4.4.5 plan. |

## Policy And Edict Control

Policies and edicts remain in scope. Treat policy and edict changes as full-object override risk unless local tests prove safe merge behavior.

Preferred policy control:

1. Inventory exact policy IDs and option IDs from the active stack.
2. Copy the full winning policy object when overriding.
3. Modify option-level `ai_weight`.
4. Use event-driven `set_policy` only as fallback after syntax and behavior verification.

Policy areas to inventory:

- `economic_policy`
- `trade_policy`
- `production_policy`
- `diplomatic_stance`
- `war_philosophy`
- `artificial_intelligence_policy`
- `robot_pop_policy`
- `refugees`
- migration pact and species-rights surfaces
- `research_restrictions`, if present

Edict areas to inventory:

- Map the Stars
- Research Subsidies
- Capacity Subsidies
- Mining Subsidies
- Farming Subsidies
- Nutritional Plenitude and hive-compatible growth edicts
- Healthcare Campaign
- Education Campaign
- Recycling Campaign
- Fortify the Border

Every edict pass must parse active-stack `resources`, `cost`, `upkeep`, `modifier`, `potential`, `allow`, and existing `ai_weight` before emitting overrides.

## Diplomacy, Research Pacts, And Research Federation

Research pact and Research Federation behavior remain in scope. Do not cut them because their surfaces are high risk.

Recommended order:

1. Use Diplomatic Stance weights as the first practical indirect lever.
2. Inventory `common/federation_types`, `common/federation_laws`, `common/diplomatic_actions`, and `common/personalities`.
3. Implement Research Federation type weights only after full-object extraction and conflict review.
4. Delay diplomatic-action overrides until the exact modding limitations and active-stack winning files are known.
5. Delay personality overrides unless the user accepts full personality compatibility patches.

Candidate IDs to verify:

- `research_federation`
- `action_form_research_agreement`
- `action_break_research_agreement`
- `action_form_migration_pact`
- `action_form_commercial_pact`
- `action_form_federation`

## Mega Engineering And Gigas Sequencing

Do not hand-code Mega Engineering prerequisites from memory. The active stack is authoritative.

Required extractor output for `tech_mega_engineering`:

- object ID;
- winning file;
- source mod;
- area;
- tier;
- prerequisites;
- potential;
- weight modifier;
- feature flags;
- diff versus vanilla 4.4.4 and 4.4.5 when available.

Generator rules:

- Fail validation if `tech_mega_engineering` is absent.
- Warn if the winning file is not vanilla.
- Fail validation if any active-stack prerequisite is missing.
- Use active-stack prerequisites, not public/wiki assumptions.

Gigas sequencing should be generated from installed files, not manually maintained. Inventory:

- `common/megastructures`
- `common/technology`
- `common/ascension_perks`
- `common/scripted_triggers`
- `common/scripted_effects`
- `common/resources`
- `common/deposits`
- `common/starbase_buildings`
- `common/starbase_modules`
- Gigas event files

Strategic queue classes:

- early kilo/economy;
- research release;
- alloy release;
- naval/shipyard release;
- War Moon path;
- Planetcraft path;
- Systemcraft path.

## NSC3 And ESC Lane Maps

Do not hand-maintain NSC3 or ESC lane maps. Generate them from the active stack every time.

Inventory:

- `common/technology`
- `common/component_templates`
- `common/section_templates`
- `common/ship_sizes`
- `common/starbase_buildings`
- `common/starbase_modules`
- `common/strategic_resources`
- `common/resources`
- `common/ship_behaviors`
- `common/personalities`

Safe first-pass work:

- weight verified vanilla and mod tech IDs;
- weight component readiness through strategic resource availability;
- map doctrine to tech lanes;
- keep ship-design, component-template, section-template, and ship-size overrides behind later compatibility gates.

Counterfitting should initially mean broad enemy-signature inference plus technology/resource readiness, not forced ship designs.

## Revised Implementation Order

### A. Safe Immediate Generator Work

1. Active-stack inventory extractor for policies, edicts, techs, buildings, districts/zones, colony types, building sets, federation types, diplomatic actions, components, sections, ship sizes, megastructures, resources, and strategic upkeep.
2. ID validation gate that fails closed on absent or unexpectedly overwritten IDs.
3. Computed strategy triggers for route, phase, resource, security, and threat state.
4. Opening economic subplans for mineral tempo, consumer goods bridge, research capital, pop assembly, defensive tall, military-to-pops, and recovery.
5. `-logempirestats` parser as manual-test support only.

### B. High-Value Verified Static Work

1. Policy `ai_weight` overrides after full-object inventory.
2. Edict `ai_weight` overrides after cost/upkeep inventory.
3. Colony designation `ai_building_set_affinity`.
4. Research/economy technology weights.
5. Mega Engineering prerequisite and draw-protection weights.
6. NSC3/ESC tech-lane weighting from discovered IDs.
7. Research Federation `ai_weight` after full-object federation review.

### C. High-Risk Override Work

Keep these in scope, but do not implement before exact local verification:

- diplomatic action overrides;
- personality overrides;
- federation law rewrites;
- production policy rewrites for Gestalts;
- species rights, living standards, migration controls;
- ship design, component, section, or ship-size overrides;
- event-driven policy forcing;
- Gigas megastructure object overrides.

### D. Manual-Test Support Tooling

Keep as user-support tooling, not Codex validation:

- `-logempirestats` KPI reports for 2250, 2275, 2300, and 2350;
- active-stack conflict report with winning file per object ID;
- Mega Engineering diff report for 4.4.4 vanilla, 4.4.5 vanilla, and active stack;
- NSC3/ESC lane report from tech to component to strategic upkeep to ship section;
- Gigas megastructure queue report;
- save-safety notes for whether generated overrides require a new game.

## Static Validation Boundary

Codex validation remains static:

- Python syntax checks;
- generator execution;
- deterministic unit tests;
- generated PDXScript parse/load-safety checks where available;
- local ID inventory validation;
- Git diff/whitespace hygiene.

Do not make observer games, scenario simulations, save checkpoints, or crisis outcome proof part of the implementation acceptance criteria.

## Bottom Line

The expanded Web ChatGPT strategy should be preserved. The implementation language should be tightened to:

> The generator emits a computed strategy kernel made of scripted triggers, optional economic subplans, scripted values where verified, and `ai_weight` modifiers. Persistent flags or variables are used only for hysteresis, cooldowns, planet memory, doctrine lock-in, and megastructure attempt tracking.

That keeps the ambition while making the plan implementable in Stellaris script.
