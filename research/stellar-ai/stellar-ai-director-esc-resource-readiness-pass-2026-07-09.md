# Stellar AI Director ESC Resource Readiness Pass

Date: 2026-07-09

Task card: T16 - ESC resource readiness support pass

## Scope

This pass improves ESC high-tier component readiness only through safe
technology and economy levers. It does not add component-template,
component-set, section-template, ship-size, ship-behavior, or global-design
output.

## Change

Added a generated economic-plan subplan:

`Stellar AI Director ESC component resource readiness`

The subplan activates when:

- `staid_research_input_runway_safe = yes`
- catastrophic collapse is not active
- `staid_advanced_component_resource_support_ready` is not already satisfied
- at least one ESC-adjacent trigger is present: vanilla dark-matter core tech,
  the ESC dark-matter power-core route tech, fleet-conversion repeatable phase,
  or year 80+ pressure

It adds income pressure for:

- `volatile_motes = 12`
- `exotic_gases = 12`
- `rare_crystals = 12`
- `sr_dark_matter = 3`
- `sr_zro = 3`
- `nanites = 3`
- `engineering_research = 600`
- `energy = 500`
- `minerals = 400`
- `trade = 150`

## Why This Is Safe

T15 showed the safe NSC3/ESC lane is technology route pressure only. The new
T16 subplan supports that lane by helping the economy satisfy the existing
`staid_advanced_component_resource_support_ready` gate that ESC route techs
already check. It avoids all direct ship graph folders and leaves ESC/NSC3
component and design loader semantics untouched.

## Validation

- `python tools/generate_stellar_ai_director_patch.py` passed.
- `python -m py_compile tools\stellar_ai_director_lib.py tools\generate_stellar_ai_director_patch.py tools\validate_stellar_ai_director_patch.py tools\tests\test_stellar_ai_director.py` passed.
- `python tools\validate_stellar_ai_director_patch.py` passed.
- Focused regression passed:
  `python -m unittest tools.tests.test_stellar_ai_director.GeneratedModValidityTests.test_support_economy_bridge_keeps_resource_bottlenecks_first_class`
- Generated reference audit updated with the new economic-plan references and
  all new rows are `ok`.
- Direct generated ship graph check returned no paths:
  `rg --files mods\StellarAIDirector\common | rg "common/(ship_sizes|section_templates|component_templates|component_sets|global_ship_designs|ship_behaviors|component_slot_templates)"`

## Remaining Runtime Proof

This static pass improves preparation for ESC high-tier components, but it does
not prove runtime use of final ESC components, NSC3 sections, ship designer
visibility, or AI design behavior. Those remain blocked behind the final
observer/smoke evidence lane described in T15 and the packet runbook.
