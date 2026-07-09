# Console Testing Cheatsheet For Modded Stellaris 4.4.x

## Scope and rule

Use this cheat sheet in non-Ironman disposable saves only. The Paradox Wiki states the console is available in non-Ironman games and lists key combinations by keyboard layout [S060]. Every command with a modded ID must be checked with in-game `help`, `debugtooltip`, local Workshop source, or generated object inventories before use.

## Core discovery commands

```text
help
help <command>
debugtooltip
observe
human_ai
play <country_id>
ai
```

Use `debugtooltip` to discover country IDs, planet IDs, leader IDs, starbase IDs, pop/planet details, and internal object names where the UI exposes them [S062]. Use `observe` + `human_ai` for observer-style AI tests, then `play <country_id>` only in disposable saves.

## Economy/resource testing

```text
cash 100000
minerals 100000
food 100000
alloys 100000
influence 1000
unity 100000
minor_artifacts 1000
resource <resource_id> <amount>
```

`resource <resource_id> <amount>` should be verified with `help resource` because modded resources vary by active stack.

### Modded resource examples to verify locally

```text
resource giga_sr_sentient_metal 10000
resource giga_sr_negative_mass 10000
resource giga_sr_amb_megaconstruction 10000
resource <esc_resource_id> 10000
resource <pd_or_guilli_resource_id> 10000
```

These are examples for later active-stack verification, not guaranteed command IDs. The external research establishes that Gigas special-resource routes matter [S013] and that URP exists to display added strategic resources [S051]; exact resource keys must come from local source.

## Technology testing

```text
research_all_technologies
finish_research
research_technology tech_mega_engineering
research_technology <nsc_hull_tech_id>
research_technology <esc_component_tech_id>
research_technology <gigas_tech_id>
```

Use `research_all_technologies` for designer validity sweeps, then staged `research_technology` tests for route-specific unlocks. Engineering congestion is important because NSC3, ESC, and Gigas all add engineering-heavy routes [S025][S028][S001].

## Planet class, deposit, and modifier testing

The Paradox Wiki planetary feature examples use selected-scope `effect` commands for deposits/features [S061]. Use a selected planet, then apply:

```text
effect add_deposit=d_mineral_deposit
effect add_deposit=d_energy_deposit
effect add_deposit=<modded_deposit_id>
effect add_modifier = {{ modifier = <planet_modifier_id> days = -1 }}
planet_class pc_gaia
planet_class <pd_planet_class_id>
```

For PD/Guilli tests, use local source or debugtooltip to identify current planet classes/modifier/deposit IDs. Planetary Diversity and Guilli strategy depends on role valuation from modifiers/deposits, not names alone [S054][S057][S059].

## Megastructure testing

```text
create_megastructure <megastructure_id>
effect solar_system = {{ create_megastructure = {{ type = <megastructure_id> }}}}
effect <scope_wrapper> = {{ create_megastructure = {{ type = <megastructure_id> }}}}
```

`create_megastructure` is scope-sensitive. A community troubleshooting thread shows it can fail with wrong player/scope context [S064]. Verify with:

```text
help create_megastructure
help effect
```

Then use a selected star/system/planet and a locally verified megastructure ID. For Gigas, do not trust community wiki names for exact IDs; use local source or Gigas GitHub/Workshop source [S003][S015].

## Ship and fleet testing

```text
add_ship <design_or_ship_name>
create_navy <amount>
attackallfleets
```

Recommended active-stack test sequence:

1. Start disposable game with NSC3 + ESC NEXT + SFT.
2. Configure ESC NEXT reactors before first month [S029].
3. Run `research_all_technologies`.
4. Open ship designer.
5. Try to save designs for every vanilla and NSC hull.
6. Check for empty behavior/computer slots, missing sections, negative power, and missing component icons [S030].
7. Spawn or build small fleets to confirm combat behavior.

## Event and crisis testing

```text
event <event_id>
effect country_event = {{ id = <event_id> }}
effect planet_event = {{ id = <event_id> }}
effect set_country_flag = <flag>
effect remove_country_flag = <flag>
```

For Gigas crises, exact event IDs and flags must come from current mod source. External research fills the strategy: Katzen uses resistance/sabotage [S006][S007], Blokkats use knowledge/research/counterstructures [S004][S005], Aeternum uses celestial ships [S009][S011], and Compound-style threats are event/research gated [S015].

## AI observer test schedule

```text
2200.01.01: debugtooltip
2200.01.01: human_ai
2200.01.01: observe
2250.01.01: pause and save
2300.01.01: pause and save
2325.01.01: pause and save
2350.01.01: pause and save
```

Capture per-AI metrics: science, alloys, energy, minerals, CG, unity, pops, colonies, systems, naval cap used/available, fleet power, shipyard count, megastructures, Gigas resources, NSC hull techs, ESC tier techs, starbase levels, and crisis counters.

## Commands requiring local verification

- All `giga_*`, `nsc_*`, `esc_*`, PD, Guilli, and Starbase Extended IDs.
- Crisis event IDs and flags.
- `create_megastructure` scope syntax for current 4.4.5.
- SFT combat computer and behavior object names.
- AI global design keys.

These are not unresolved research questions; they are local active-stack IDs and in-game help checks.
