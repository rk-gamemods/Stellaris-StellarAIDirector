# Stellar AI Director fleet economic model refactor

Date: 2026-07-12

## Scope and authority

This slice targets Stellaris PC 4.4.5 by repository policy. Its active-stack
source evidence is the locally installed 4.4-compatible NSC3, Extra Ship
Components NEXT, Gigastructures, and Spacefleet Tactica content. The existing
2269 save evidence is Pegasus 4.4.4 comparative runtime evidence, not 4.4.5
runtime proof.

The authoritative implementation inputs are the current Workshop PDXScript
files and `tools/stellar_ai_fleet_economy_model.py`. The generated JSON report
is derived evidence. It has no HTML or rendered-document counterpart.

Runtime testing was not authorized or run. No event, on_action, resource grant,
forced fleet template, construction order, or ship graph override is used.

## Recurring pressure inventory

The deterministic scanner inspects `common/ship_sizes` and
`common/component_templates`, accepting only `category = ships` and
`category = ship_components`. This excludes starbase and unrelated economy
objects.

| Source | Construction inputs | Recurring upkeep/logistics |
|---|---|---|
| NSC3 | alloys, energy, food, minerals, influence, motes, gases, crystals, dark matter, Zro | alloys, energy, food, minerals, trade |
| ESC NEXT | alloys, energy, food, minerals, motes, gases, crystals, dark matter, Zro, nanites, living metal | alloys, energy, food, minerals |
| Gigastructures | alloys, energy, food, special Gigas resources, artifacts, motes, gases, crystals, dark matter, Zro | alloys, energy, food, sentient metal, influence, trade |
| Spacefleet Tactica | alloys and advanced component inputs | alloys, energy, food |

Construction inputs are not sustainability gates. Native affordability and
the corresponding resource-specific `category = ships` budgets decide whether
a design can be queued. Wartime stockpile size is not an economic-safety gate.

The recurring policy therefore requires positive energy, alloy, and trade net
income for every surge. Biological fleets additionally require positive food.
Food on standard hulls, minerals, sentient metal, and influence are
component/special-hull-sensitive: negative net income blocks the surge, while
zero is allowed only when total country expense for that resource is zero. If
the country spends the resource for any reason, its net income must be positive.
The engine exposes total expense but cannot isolate the share caused by ships.

## Decision and model boundary

The production rule is deliberately small:

1. The country is a normal AI empire at war, uses standard ship sizes, has a
   capital-hull technology, and is below 90% naval capacity.
2. All universal recurring fleet resources have positive net income.
3. Biological food pressure is positive when applicable.
4. Optional component/special-hull resources either have zero total expense or
   positive net income.
5. The existing 1.5 ship-budget factor applies on top of the native wartime
   factor. The fixed `desired_min + 5000 alloys` reserve is removed.
6. No stockpile or two-month-runway condition is applied to this wartime surge.

`evaluate_completion_tranche` is the external logical model. It subtracts a
candidate completion wave's upkeep vector from current net income and requires
every consumed recurring resource to remain positive. This is stricter than
the production trigger because Stellaris exposes neither the next auto-design's
component upkeep vector nor the future upkeep of ships already committed to
queues at country scope.

Consequently, the production trigger is a bounded native heuristic, not a
proof that simultaneous queue completions cannot overshoot. The model makes
that limitation testable rather than hiding it.

## Top five risks

1. **Discrete megaship completion:** one exceptional Gigas hull can add 1,500
   alloys, 0.5 influence, and 250 trade upkeep.
2. **Parallel queue overshoot:** multiple shipyards can commit while income is
   positive and complete after the budget gate closes.
3. **Component-sensitive pressure:** an otherwise standard hull can mount an
   ESC mineral-upkeep, SFT food-upkeep, or Gigas sentient-metal component.
4. **Optional-resource attribution:** country scope exposes total expense, not
   ship-only expense. The conservative rule can therefore stop fleet growth for
   an optional resource currently consumed elsewhere in the economy.
5. **War shock:** lost production, trade routes, anchorages, or naval capacity
   can invalidate a previously safe decision while construction is underway.

Exceptional Gigas megaships should remain on separately modeled construction
lanes. They must not be treated as an ordinary generic fleet-surge tranche.

## Validation contract

- Run `python tools/generate_stellar_ai_fleet_economy.py` for the narrow three-
  artifact regeneration path.
- Run `python -m unittest tools.tests.test_stellar_ai_fleet_economy_model` for
  scanner and scenario behavior.
- Run `python -m unittest tools.tests.test_stellar_ai_director.ShipBudgetAvailabilityTests`
  for generated trigger/budget parity.
- Run the project static validator and scripted-trigger cycle checks before
  integration.

Runtime follow-up, when explicitly approved, should measure current and queued
ship upkeep by resource, shipyard concurrency, post-completion net income,
naval-cap utilization, and whether new templates are actually created.
