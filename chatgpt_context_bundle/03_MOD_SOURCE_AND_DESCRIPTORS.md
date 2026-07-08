> Snapshot commit: `27aa7547b610e2876d897771a804656453f948ee` | Branch: `master` | Working tree: `dirty` | Generated: `2026-07-08T15:18:04-04:00`

# Mod Source And Descriptors

Source mod files are copied path-preserving. Treat launcher descriptors as metadata, not proof that script content loads.

## mods/README.md

```markdown
# Mods

Create one folder per Stellaris mod here.

Default to Stellaris PC 4.4.5 stable/current local install unless the mod README says otherwise. Use `supported_version="v4.4.*"` for stable 4.4 descriptors, including 4.4.5.

Each mod should include its own `README.md` with:

- mod purpose;
- target Stellaris version;
- required or assumed DLC;
- touched vanilla systems;
- mod prefix;
- object keys added or overridden;
- localisation keys added or overridden;
- compatibility notes;
- test checklist.

## Mod Folder Rules

- Use unique, prefixed filenames instead of vanilla-like names such as `00_civics.txt`.
- Add only folders the mod actually needs.
- Keep source project files here, not in the live Stellaris launcher mod directory.
- When preparing a playable local copy, use the descriptor pair described in `research/stellaris-modding-guide-2026-07-04.md`.
- Treat overwrites, copied vanilla files, UI files, and `replace_path` as high-risk until validated against current vanilla files and Irony conflict results.

The attached research bundle includes a starter skeleton at `research/stellaris-modding-research-bundle-2026-07-04/templates/stellaris_mod_skeleton/`.

## Local 4.4 Replacements

- `StellarAIDirector/` - AI budget/priority patch for the Irony playset.
- `RKImmortalLeadersTrait/` - local 4.4 replacement for the old Immortal Leaders Trait mod.
- `RKCheatTraits44/` - local 4.4 replacement for udk Cheat Traits; use this for effectively unlimited custom empire trait points/picks.
- `RKGodlyTraitsRedux44/` - local 4.4 compatibility copy of Godly Traits Redux 4.0 with powerful species and leader traits.
- `RKMoreTraitPoints/` - local 4.4 replacement for More Trait Points; do not stack with other species-archetype trait-point mods.
- `RKMilitusExtraTraitPicks/` - local 4.4 replacement for Militus' Extra Trait Points; do not stack with other species-archetype trait-point mods.
- `RKThreeCivicMoreTraitPointsPicks/` - local 4.4 replacement for 3 Civic Points + More Trait Points/Picks; do not stack with other species-archetype trait-point mods.
```

## mods/RKCheatTraits44/README.md

```markdown
# RK Cheat Traits 4.4

Local 4.4-compatible replacement for `udk Cheat Traits (Updated for 4.0)`.

The Workshop mod is still marked for `v4.0.*`. Its species-archetype overwrite
also references the old `pop_resources/regular_upkeep` inline script, which is
not present in the local 4.4.4 install. This local version uses the current
4.4 vanilla species-archetype file and changes only the trait-pick caps.

What this does:

- Sets biological, lithoid, machine, robot, and presapient trait pick caps to
  `99`.
- Adds `RK Cheat: 500 Trait Points`, a player-only species trait with cost
  `-500`.
- Adds `RK Cheat: Immortality`, a player-only species trait that sets
  `immortal_leaders = yes`.
- Prevents random/AI selection of the cheat traits.

Do not stack this with any other mod that overwrites
`common/species_archetypes/00_species_archetypes.txt`.
```

## mods/RKCheatTraits44/common/species_archetypes/00_species_archetypes.txt

```text
# 4.4 vanilla species archetypes with RK Cheat Traits pick caps.

@robot_trait_points = 0
@robot_max_traits = 99
@machine_trait_points = 1
@machine_max_traits = 99
@species_trait_points = 2
@species_max_traits = 99

BIOLOGICAL = {
	species_trait_points = @species_trait_points
	species_max_traits = @species_max_traits

	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}

ROBOT = {
	species_trait_points = @robot_trait_points
	species_max_traits = @robot_max_traits
	robotic = yes
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

MACHINE = {
	species_trait_points = @machine_trait_points
	species_max_traits = @machine_max_traits
	robotic = yes
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

PRESAPIENT = {
	species_trait_points = @species_trait_points
	species_max_traits = @species_max_traits
	uses_modifiers = no
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

LITHOID = {
	inherit_trait_points_from = BIOLOGICAL
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}

OTHER = {
	uses_modifiers = no
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}
```

## mods/RKCheatTraits44/common/traits/rk_cheat_traits.txt

```text
trait_rk_cheat_500_points = {
	cost = -500
	category = normal
	icon = "gfx/interface/icons/traits/trait_communal.dds"
	initial = yes
	randomized = no
	sorting_priority = -100

	species_potential_add = {
		from = { is_ai = no }
	}
	species_possible_add = {
		from = { is_ai = no }
	}
	species_possible_remove = {
		from = { is_ai = no }
	}
	species_possible_merge_add = {
		from = { is_ai = no }
	}

	allowed_archetypes = { BIOLOGICAL LITHOID ROBOT MACHINE }
	tags = { organic lithoid machine positive special }

	modifier = {
		BIOLOGICAL_species_trait_picks_add = 99
		LITHOID_species_trait_picks_add = 99
		ROBOT_species_trait_picks_add = 99
		MACHINE_species_trait_picks_add = 99
	}

	ai_weight = {
		weight = 0
	}
}

trait_rk_cheat_immortality = {
	cost = 0
	category = normal
	icon = "gfx/interface/icons/traits/trait_venerable.dds"
	initial = yes
	randomized = no
	immortal_leaders = yes
	sorting_priority = -99

	species_potential_add = {
		from = { is_ai = no }
	}
	species_possible_add = {
		from = { is_ai = no }
	}
	species_possible_remove = {
		from = { is_ai = no }
	}
	species_possible_merge_add = {
		from = { is_ai = no }
	}

	allowed_archetypes = { BIOLOGICAL LITHOID ROBOT MACHINE }
	tags = { organic lithoid machine positive leader special }
	opposites = {
		"trait_enduring"
		"trait_venerable"
		"trait_fleeting"
		"trait_fleeting_lithoid"
	}

	ai_weight = {
		weight = 0
	}
}
```

## mods/RKCheatTraits44/descriptor.mod

```text
version="1.0.0"
tags={
	"Utilities"
	"Species"
	"Gameplay"
}
name="RK Cheat Traits 4.4"
supported_version="v4.4.*"
```

## mods/RKCheatTraits44/localisation/english/rk_cheat_traits_l_english.yml

```yaml
l_english:
 trait_rk_cheat_500_points:0 "RK Cheat: 500 Trait Points"
 trait_rk_cheat_500_points_desc:0 "Adds enough trait points and trait picks to build a deliberately overpowered custom empire."
 trait_rk_cheat_immortality:0 "RK Cheat: Immortality"
 trait_rk_cheat_immortality_desc:0 "Leaders of this species do not die of old age."
```

## mods/RKGodlyTraitsRedux44/README.md

```markdown
# RK Godly Traits Redux 4.4

Local Stellaris 4.4.5/current 4.4-line compatibility copy of Steam Workshop mod `Godly Traits Redux 4.0` (`2945430513`).

This preserves the source mod's powerful species traits, point-granting traits, leader traits, civics, events, localization, and icons. The local copy updates metadata to `v4.4.*` and fixes compatibility issues found in the installed 4.0 source:

- removed stale `PLANTOID` species archetype references that are not present in vanilla 4.4;
- changed missing `trait_demigod_race.dds` icon references to the shipped `trait_demigod.dds`;
- removed an obsolete `general` leader event branch that referenced undefined `leader_trait_general_godly`;
- fixed malformed `NOR` event syntax;
- fixed the duplicated Nephalem localization key so the description loads as `_desc`.

Source Workshop page: https://steamcommunity.com/sharedfiles/filedetails/?id=2945430513
```

## mods/RKGodlyTraitsRedux44/common/governments/civics/GTR_civics.txt

```text
GTR_extra_traits_4 = {
	icon = "gfx/interface/icons/traits/trait_4_extra.dds"

	modification = no
	pickable_at_start = yes
	random_weight = {
		base = 0
		modifier = {
			factor = 0
		}
	}
	modifier = {
        BIOLOGICAL_species_trait_picks_add = 4
		LITHOID_species_trait_picks_add = 4
		MACHINE_species_trait_picks_add = 4
		ROBOT_species_trait_picks_add = 4
	}
}

GTR_extra_traits_8 = {
	icon = "gfx/interface/icons/traits/trait_8_extra.dds"

	modification = no
	pickable_at_start = yes
	random_weight = {
		base = 0
		modifier = {
			factor = 0
		}
	}
	modifier = {
        BIOLOGICAL_species_trait_picks_add = 8
		LITHOID_species_trait_picks_add = 8
		MACHINE_species_trait_picks_add = 8
		ROBOT_species_trait_picks_add = 8
	}
}

GTR_extra_traits_16 = {
	icon = "gfx/interface/icons/traits/trait_16_extra.dds"

	modification = no
	pickable_at_start = yes
	random_weight = {
		base = 0
		modifier = {
			factor = 0
		}
	}
	modifier = {
        BIOLOGICAL_species_trait_picks_add = 16
		LITHOID_species_trait_picks_add = 16
		MACHINE_species_trait_picks_add = 16
		ROBOT_species_trait_picks_add = 16
	}
}

GTR_extra_traits_32 = {
	icon = "gfx/interface/icons/traits/trait_32_extra.dds"

	modification = no
	pickable_at_start = yes
	random_weight = {
		base = 0
		modifier = {
			factor = 0
		}
	}
	modifier = {
        BIOLOGICAL_species_trait_picks_add = 32
		LITHOID_species_trait_picks_add = 32
		MACHINE_species_trait_picks_add = 32
		ROBOT_species_trait_picks_add = 32
	}
}```

## mods/RKGodlyTraitsRedux44/common/on_actions/GTR_on_actions.txt

```text
on_leader_spawned = {
	events = {
		GTR_trait.101
		GTR_trait.102
	}
}
on_modification_complete = {
	events = {
		GTR_trait.103
	}
}
on_ruler_created = {
	events = {
		GTR_trait.104
		GTR_trait.105
		GTR_trait.107
		GTR_trait.108
	}
}

on_ruler_removed = {
	events = {
		GTR_trait.106
	}
}

```

## mods/RKGodlyTraitsRedux44/common/traits/GTR_traits.txt

```text
#########Species

GTR_trait_hyper_fertile = {
	icon = "gfx/interface/icons/traits/trait_hyper_fertile.dds"
	cost = 5
	initial = yes
	modification = yes
	randomized = no
	advanced_trait = yes
	immortal_leaders = yes
	allowed_archetypes = { BIOLOGICAL LITHOID }
	opposites = { "GTR_trait_super_fertile" "GTR_trait_nano_assemblers" }

	tags = {
		organic
		positive
		pop_growth
		leader
		housing
	}
	modifier = {
        logistic_growth_mult = 3.0
		pop_housing_usage_mult = 0.25
		planet_building_build_speed_mult = 0.5
		pop_cat_slave_happiness = -0.2
		leaders_upkeep_mult = -0.3
	}

	ai_weight = {
		weight = 0
	}
}

GTR_trait_super_fertile = {
	icon = "gfx/interface/icons/traits/trait_super_fertile.dds"
	cost = 3
	initial = yes
	modification = yes
	randomized = no
	immortal_leaders = yes
	allowed_archetypes = { BIOLOGICAL LITHOID }
	opposites = { "GTR_trait_hyper_fertile" "GTR_trait_nano_assemblers" }

	modifier = {
        logistic_growth_mult = 1.0
		pop_housing_usage_mult = -0.1
		pop_cat_slave_happiness = -0.2
		leaders_upkeep_mult = -0.1
	}

	tags = {
		housing
		leader
		pop_growth
		positive
		organic
	}

	ai_weight = {
		weight = 0
	}
}

GTR_trait_nano_assemblers = {
	icon = "gfx/interface/icons/traits/trait_hyper_fertile.dds"
	cost = 3
	initial = yes
	modification = yes
	randomized = no
	immortal_leaders = yes
	allowed_archetypes = { MACHINE ROBOT }
	opposites = { "GTR_trait_super_fertile" "GTR_trait_hyper_fertile" }

	modifier = {
        planet_pop_assembly_mult = 2.0
        pop_housing_usage_mult = -0.25
		negative_leader_traits_species = -3
		leaders_upkeep_mult = -0.2
	}

	tags = {
		housing
		leader
		pop_growth
		positive
		machine
	}

	ai_weight = {
		weight = 0
	}
}

GTR_trait_nephalem = {
	icon = "gfx/interface/icons/traits/trait_god.dds"
	cost = 5
    initial = no
	modification = no
	randomized = no
	advanced_trait = yes
	immortal_leaders = yes
	allowed_archetypes = { BIOLOGICAL LITHOID }
	opposites = { "GTR_trait_godly_species" "GTR_trait_deus_machina" "GTR_trait_borg" "GTR_trait_divine_ancestors" "GTR_trait_demigods"}

    modifier = {
		pop_bonus_workforce_mult = 2.0
		pop_happiness = 1.0
		pop_government_ethic_attraction = 0.5
        logistic_growth_mult = 2.0
        pop_housing_usage_mult = -0.50
        pop_environment_tolerance = 1.0
		army_health = 2.0
        army_morale = 2.0
		army_morale_damage_mult = 1.0
        army_defense_damage_mult = 1.0
        army_damage_mult = 0.50
		army_starting_experience_add = 10000
		species_leader_exp_gain = 10.0
        leader_skill_levels = 10
		negative_leader_traits_species = -6
		leaders_upkeep_mult = -0.6
	}

	ai_weight = {
		weight = 0
	}
}

GTR_trait_godly_species = {
	icon = "gfx/interface/icons/traits/trait_god.dds"
	cost = 5
    initial = yes
	modification = yes
	randomized = no
	advanced_trait = yes
	immortal_leaders = yes
	allowed_archetypes = { BIOLOGICAL LITHOID }
	opposites = { "GTR_trait_nephalem" "GTR_trait_deus_machina" "GTR_trait_borg" "GTR_trait_divine_ancestors" "GTR_trait_demigods"}

    modifier = {
		pop_bonus_workforce_mult = 1.0
		pop_happiness = 0.5
		pop_government_ethic_attraction = 0.5
        logistic_growth_mult = 1.0
        pop_housing_usage_mult = -0.25
        pop_environment_tolerance = 0.5
		army_health = 1.0
        army_morale = 1.0
		army_morale_damage_mult = 0.5
        army_defense_damage_mult = 0.5
        army_damage_mult = 0.25
		army_starting_experience_add = 1000
		species_leader_exp_gain = 5.0
        leader_skill_levels = 10
		negative_leader_traits_species = -3
		leaders_upkeep_mult = -0.3
	}

	ai_weight = {
		weight = 0
	}
}

GTR_trait_demigods = {
	icon = "gfx/interface/icons/traits/trait_demigod.dds"
	cost = 3
    initial = yes
	modification = yes
	randomized = no
	allowed_archetypes = { BIOLOGICAL LITHOID MACHINE ROBOT }
	opposites = { "GTR_trait_nephalem" "GTR_trait_godly_species" "GTR_trait_deus_machina" "GTR_trait_borg" "GTR_trait_divine_ancestors" }

    modifier = {
		pop_bonus_workforce_mult = 0.5
		pop_happiness = 0.20
		pop_government_ethic_attraction = 0.5
        logistic_growth_mult = 0.50
        pop_housing_usage_mult = -0.10
        pop_environment_tolerance = 0.15
		army_health = 0.5
        army_morale = 0.5
		army_morale_damage_mult = 0.20
        army_defense_damage_mult = 0.20
        army_damage_mult = 0.10
		army_starting_experience_add = 500
		species_leader_exp_gain = 2.0
        leader_lifespan_add = 300
        leader_skill_levels = 5
		negative_leader_traits_species = -2
		leaders_upkeep_mult = -0.2
	}

	ai_weight = {
		weight = 0
	}
}

GTR_trait_divine_ancestors = {
	icon = "gfx/interface/icons/traits/trait_ancient.dds"

	cost = 3
    initial = yes
	modification = yes
	randomized = no
	opposites = { "GTR_trait_nephalem" "GTR_trait_godly_species" "GTR_trait_deus_machina" "GTR_trait_borg" "GTR_trait_demigods" }

	allowed_archetypes = { BIOLOGICAL LITHOID MACHINE ROBOT }

    modifier = {
		pop_bonus_workforce_mult = 0.2
		pop_happiness = 0.10
		pop_government_ethic_attraction = 0.5
        pop_environment_tolerance = 0.10
		army_health = 0.25
        army_morale = 0.25
		army_morale_damage_mult = 0.10
        army_defense_damage_mult = 0.10
        army_damage_mult = 0.10
        army_starting_experience_add = 200
		species_leader_exp_gain = 1.0
        leader_lifespan_add = 100
        leader_skill_levels = 2
		negative_leader_traits_species = -1
		leaders_upkeep_mult = -0.1
	}

	ai_weight = {
		weight = 0
	}
}

GTR_trait_everlasting = {
	icon = "gfx/interface/icons/traits/trait_ancient.dds"
	cost = 3
	initial = yes
	modification = yes
	randomized = no
	advanced_trait = yes
	immortal_leaders = yes
	allowed_archetypes = { BIOLOGICAL LITHOID MACHINE ROBOT }
	opposites = { "trait_venerable" "trait_enduring" "trait_fleeting" "GTR_trait_ancient_hive" "GTR_trait_ancient" }

	ai_weight = {
		weight = 0
	}
}

GTR_trait_ancient = {
	icon = "gfx/interface/icons/traits/trait_ancient.dds"
	cost = 5
	initial = yes
	modification = no
	randomized = no
	immortal_leaders = yes
	allowed_archetypes = { BIOLOGICAL LITHOID }
	opposites = { "trait_venerable" "trait_enduring" "trait_fleeting" "GTR_trait_ancient_hive" "GTR_trait_everlasting" }

	modifier = {
		leader_skill_levels = 10
		leaders_upkeep_mult = 1
		species_leader_exp_gain = -0.25
		negative_leader_traits_species = -2
	}

	leader_age_min = 100
	leader_age_max = 10000

	ai_weight = {
		weight = 0
	}
}

GTR_trait_ancient_hive = {
	icon = "gfx/interface/icons/traits/trait_god.dds"
	cost = 0
	initial = no
	randomized = no
	modification = no
	immortal_leaders = yes
	allowed_archetypes = { BIOLOGICAL LITHOID }
	opposites = { "trait_venerable" "trait_enduring" "trait_fleeting" "GTR_trait_ancient" "GTR_trait_everlasting" }

	modifier = {
		leader_skill_levels = 10
		leaders_upkeep_mult = 1
		species_leader_exp_gain = -0.25
		negative_leader_traits_species = -2
		leaders_upkeep_mult = -0.2
	}

	leader_age_min = 100
	leader_age_max = 10000

	ai_weight = {
		weight = 0
	}
}

GTR_trait_deus_machina = {
	icon = "gfx/interface/icons/traits/trait_god.dds"
	cost = 5
    initial = yes
	modification = yes
	randomized = no
	immortal_leaders = yes
	allowed_archetypes = { ROBOT MACHINE }
	opposites = { "GTR_trait_nephalem" "GTR_trait_godly_species" "GTR_trait_borg" "GTR_trait_divine_ancestors" "GTR_trait_demigods"}


    modifier = {
		# 1.75x Elite, 2.5x specialist, 1.75x worker
		pop_bonus_workforce_mult = 0.75
		specialist_and_complex_drone_cat_bonus_workforce_mult = 0.75
		planet_pop_assembly_mult = 1.0
        pop_housing_usage_mult = -0.30
        pop_environment_tolerance = 0.50
        army_health = 1.0
        army_morale = 1.0
		army_morale_damage_mult = 1.0
        army_defense_damage_mult = 1.0
        army_damage_mult = 0.5
        army_starting_experience_add = 1000
		species_leader_exp_gain = 5.0
        leader_skill_levels = 10
		negative_leader_traits_species = -2
		leaders_upkeep_mult = -0.2
	}

	ai_weight = {
		weight = 0
	}
}

GTR_trait_borg = {
	icon = "gfx/interface/icons/traits/trait_god.dds"
	cost = 5
    initial = yes
	modification = yes
	randomized = no
	immortal_leaders = yes
	allowed_archetypes = { ROBOT MACHINE }
	opposites = { "GTR_trait_nephalem" "GTR_trait_godly_species" "GTR_trait_deus_machina" "GTR_trait_divine_ancestors" "GTR_trait_demigods"}

    modifier = {
		pop_bonus_workforce_mult = 1.0
		planet_pops_food_upkeep_mult = -0.25
		army_health = 1.0
        army_morale = 1.0
		army_morale_damage_mult = 1.0
        army_defense_damage_mult = 1.0
        army_damage_mult = 0.5
        army_starting_experience_add = 1000
		planet_pop_assembly_mult = 0.5
		logistic_growth_mult = 0.5
        pop_housing_usage_mult = -0.5
        pop_environment_tolerance = -0.50
		species_leader_exp_gain = 2.5
        leader_skill_levels = 10
		negative_leader_traits_species = -2
		leaders_upkeep_mult = -0.2
	}

	ai_weight = {
		weight = 0
	}
}

trait_4_point = {
	icon = "gfx/interface/icons/traits/trait_4_extra.dds"
	cost = -4
	initial = yes
	modification = yes
	randomized = no
	advanced_trait = no
	allowed_archetypes = { BIOLOGICAL LITHOID ROBOT MACHINE }

	ai_weight = {
		weight = 0
	}
}

trait_8_point = {
	icon = "gfx/interface/icons/traits/trait_8_extra.dds"
	cost = -8
	initial = yes
	modification = yes
	randomized = no
	advanced_trait = yes
	allowed_archetypes = { BIOLOGICAL LITHOID ROBOT MACHINE }

	ai_weight = {
		weight = 0
	}
}

trait_16_point = {
	icon = "gfx/interface/icons/traits/trait_16_extra.dds"
	cost = -16
	initial = yes
	modification = yes
	randomized = no
	advanced_trait = yes
	allowed_archetypes = { BIOLOGICAL LITHOID ROBOT MACHINE }

	ai_weight = {
		weight = 0
	}
}

trait_32_point = {
	icon = "gfx/interface/icons/traits/trait_32_extra.dds"
	cost = -32
	initial = yes
	modification = no
	randomized = no
	advanced_trait = yes
	allowed_archetypes = { BIOLOGICAL LITHOID ROBOT MACHINE }

	ai_weight = {
		weight = 0
	}
}

##############Commanders

leader_trait_commander_godly = {
	icon = "gfx/interface/icons/traits/trait_god.dds"
	cost = 0
	modification = no
	planet_modifier = {
		planet_defense_armies_add = 20
		job_soldier_per_pop = 0.10
		job_researcher_naval_cap_add = 4
		planet_soldiers_engineering_research_produces_add = 1
		planet_orbital_bombardment_damage = -0.5
		army_defense_damage_mult = 1
		planet_army_build_speed_mult = 1
		army_starting_experience_add = 1000
	}
	sector_modifier = {
		planet_defense_armies_add = 10
		job_soldier_per_pop = 0.05
		job_researcher_naval_cap_add = 2
		planet_soldiers_engineering_research_produces_add = 0.5
		planet_orbital_bombardment_damage = -0.25
		army_defense_damage_mult = 0.5
		planet_army_build_speed_mult = 0.2
		army_starting_experience_add = 500
	}
	fleet_modifier = {
		ship_experience_gain_mult = 1.0
        ship_fire_rate_mult = 0.25
		ship_weapon_damage = 0.25
		ship_weapon_range_mult = 0.25
        ship_speed_mult = 0.5
		ship_evasion_mult = 0.25
		ship_tracking_mult = 0.25
	}
	army_modifier = {
		army_experience_gain_mult = 1.0
        army_damage_mult = 0.25
        army_morale_damage_mult = 0.50
        army_morale = 0.20
        army_health = 0.50
		army_disengage_chance_mult = 0.25
	}
	councilor_modifier = {
		shipclass_military_station_damage_mult = 0.5
		shipclass_military_station_hull_mult = 0.5
		monthly_loyalty_from_subjects = 1
		army_experience_gain_mult = 1
		planet_army_build_speed_mult = 1
		armies_cost_mult = -0.5
		envoy_improve_relations_mult = 1
		intel_decryption_add = 2
		intel_encryption_add = 2
		planet_defense_armies_add = 2
		planet_orbital_bombardment_damage = -0.2
		spy_network_daily_value_mult = 2
		operations_cost_mult = -0.5
		envoys_add = 2
	}
	leader_class = { commander }
	initial = no
	randomized = no
}

leader_trait_commander_demigod = {
	icon = "gfx/interface/icons/traits/trait_demigod.dds"
	cost = 0
	modification = no
	planet_modifier = {
		planet_defense_armies_add = 10
		job_soldier_per_pop = 0.05
		job_researcher_naval_cap_add = 2
		planet_soldiers_engineering_research_produces_add = 0.5
		planet_orbital_bombardment_damage = -0.25
		army_defense_damage_mult = 0.5
		planet_army_build_speed_mult = 0.5
		army_starting_experience_add = 500
	}
	sector_modifier = {
		planet_defense_armies_add = 5
		job_soldier_per_pop = 0.025
		job_researcher_naval_cap_add = 1
		planet_soldiers_engineering_research_produces_add = 0.25
		planet_orbital_bombardment_damage = -0.1
		army_defense_damage_mult = 0.25
		planet_army_build_speed_mult = 0.1
		army_starting_experience_add = 250
	}
	fleet_modifier = {
		ship_experience_gain_mult = 0.5
        ship_fire_rate_mult = 0.10
		ship_weapon_damage = 0.10
		ship_weapon_range_mult = 0.10
        ship_speed_mult = 0.25
		ship_evasion_mult = 0.10
		ship_tracking_mult = 0.10
	}
	army_modifier = {
		army_experience_gain_mult = 0.5
        army_damage_mult = 0.10
        army_morale_damage_mult = 0.25
        army_morale = 0.10
        army_health = 0.25
		army_disengage_chance_mult = 0.10
	}
	councilor_modifier = {
		shipclass_military_station_damage_mult = 0.25
		shipclass_military_station_hull_mult = 0.25
		monthly_loyalty_from_subjects = 0.5
		army_experience_gain_mult = 0.5
		planet_army_build_speed_mult = 0.5
		armies_cost_mult = -0.25
		envoy_improve_relations_mult = 0.5
		intel_decryption_add = 1
		intel_encryption_add = 1
		planet_defense_armies_add = 1
		planet_orbital_bombardment_damage = -0.1
		spy_network_daily_value_mult = 1
		operations_cost_mult = -0.25
		envoys_add = 1
	}
	leader_class = { commander }
	initial = no
	randomized = no
}

############Officials

leader_trait_official_godly = {
	icon = "gfx/interface/icons/traits/trait_god.dds"
	cost = 0
	modification = no
	modifier = {
		planet_jobs_engineering_research_produces_mult = 0.25
		planet_jobs_physics_research_produces_mult = 0.25
		planet_jobs_society_research_produces_mult = 0.25
        planet_districts_cost_mult = -0.25
		planet_buildings_cost_mult = -0.25
		planet_building_build_speed_mult = 1.0
		deposit_blockers_cost_mult = -0.25
		planet_clear_blocker_time_mult = -0.50
        planet_stability_add = 25
		planet_crime_add = -25
		planet_army_build_speed_mult = 0.25
		pop_happiness = 0.25
		logistic_growth_mult = 0.2
		planet_pop_assembly_mult = 0.2
	}
	councilor_modifier = {
		ship_colonizer_cost_mult = -0.5
		planet_colony_development_speed_mult = 0.3
		planet_resettlement_unemployed_mult = 1
		planet_jobs_produces_mult = 0.3
	}
	leader_class = { official }
	initial = no
	randomized = no
}

leader_trait_official_demigod = {
	icon = "gfx/interface/icons/traits/trait_demigod.dds"
	cost = 0
	modification = no
	modifier = {
		planet_jobs_engineering_research_produces_mult = 0.10
		planet_jobs_physics_research_produces_mult = 0.10
		planet_jobs_society_research_produces_mult = 0.10
        planet_districts_cost_mult = -0.10
		planet_buildings_cost_mult = -0.10
		planet_building_build_speed_mult = 0.50
		deposit_blockers_cost_mult = -0.10
		planet_clear_blocker_time_mult = -0.25
        planet_stability_add = 10
		planet_crime_add = -10
		planet_army_build_speed_mult = 0.10
		pop_happiness = 0.10
		logistic_growth_mult = 0.1
		planet_pop_assembly_mult = 0.1
	}
	councilor_modifier = {
		ship_colonizer_cost_mult = -0.25
		planet_colony_development_speed_mult = 0.15
		planet_resettlement_unemployed_mult = 0.5
		planet_jobs_produces_mult = 0.15
	}
	leader_class = { official }
	initial = no
	randomized = no
}

###############Scientists

leader_trait_scientist_godly = {
	icon = "gfx/interface/icons/traits/trait_god.dds"
	cost = 0
	modification = no
	modifier = {
        science_ship_survey_speed = 0.50
		ship_anomaly_research_speed_mult = 0.50
		ship_anomaly_generation_chance_mult = 0.50
		ship_disengage_chance_mult = 1.0
        ship_hull_mult = 2.5
		ship_shield_mult = 2.5
		ship_armor_mult = 2.5
		ship_speed_mult = 1.0
	}
	councilor_modifier = {
		all_technology_research_speed = 0.25
		num_tech_alternatives_add = 1
		species_leader_exp_gain = 0.3
		starbase_shipyard_build_speed_mult = 0.5
		ship_archaeological_site_excavation_speed_mult = 0.5
		station_gatherers_produces_mult = 0.10
		station_gatherers_cost_mult = -0.20
		starbase_modules_cost_mult = -0.2
		starbase_upgrade_cost_mult = -0.1
		starbase_outpost_cost_mult = -0.1
		country_starbase_influence_cost_mult = -0.1
		scientist_exp_gain = 0.3
		ship_archaeological_site_clues_add = 2
	}
	planet_modifier = {
		planet_jobs_physics_research_produces_mult = 0.1
		planet_jobs_society_research_produces_mult = 0.1
		planet_jobs_engineering_research_produces_mult = 0.1
		planet_amenities_add = 2000
	}
	sector_modifier = {
		planet_jobs_physics_research_produces_mult = 0.025
		planet_jobs_society_research_produces_mult = 0.025
		planet_jobs_engineering_research_produces_mult = 0.025
	}
	triggered_planet_modifier = {
		potential = {
			trait_is_wilderness_check = no
		}
		planet_miners_minerals_produces_add = 0.5
	}
	triggered_planet_modifier = {
		potential = {
			trait_is_wilderness_check = yes
		}
		planet_jobs_minerals_produces_mult = 0.05
	}
	triggered_sector_modifier = {
		potential = {
			trait_is_wilderness_check = no
		}
		planet_miners_minerals_produces_add = 0.25
	}
	triggered_sector_modifier = {
		potential = {
			trait_is_wilderness_check = yes
		}
		planet_jobs_minerals_produces_mult = 0.025
	}

	leader_class = { scientist }
	initial = no
	randomized = no

	ai_categories = {
		physics
		society
		engineering
	}
}

leader_trait_scientist_demigod = {
	icon = "gfx/interface/icons/traits/trait_demigod.dds"
	cost = 0
	modification = no
	modifier = {
        science_ship_survey_speed = 0.25
		ship_anomaly_research_speed_mult = 0.25
		ship_anomaly_generation_chance_mult = 0.25
		ship_disengage_chance_mult = 0.5
        ship_hull_mult = 1.5
		ship_shield_mult = 1.5
		ship_armor_mult = 1.5
		ship_speed_mult = 0.5
	}
	councilor_modifier = {
		all_technology_research_speed = 0.15
		species_leader_exp_gain = 0.15
		starbase_shipyard_build_speed_mult = 0.25
		ship_archaeological_site_excavation_speed_mult = 0.25
		station_gatherers_produces_mult = 0.05
		station_gatherers_cost_mult = -0.10
		starbase_modules_cost_mult = -0.2
		starbase_upgrade_cost_mult = -0.05
		starbase_outpost_cost_mult = -0.05
		country_starbase_influence_cost_mult = -0.05
		scientist_exp_gain = 0.15
		ship_archaeological_site_clues_add = 1
	}
	planet_modifier = {
		planet_jobs_physics_research_produces_mult = 0.05
		planet_jobs_society_research_produces_mult = 0.05
		planet_jobs_engineering_research_produces_mult = 0.05
		planet_amenities_add = 1000
	}
	sector_modifier = {
		planet_jobs_physics_research_produces_mult = 0.025
		planet_jobs_society_research_produces_mult = 0.025
		planet_jobs_engineering_research_produces_mult = 0.025
	}
	triggered_planet_modifier = {
		potential = {
			trait_is_wilderness_check = no
		}
		planet_miners_minerals_produces_add = 0.25
	}
	triggered_planet_modifier = {
		potential = {
			trait_is_wilderness_check = yes
		}
		planet_jobs_minerals_produces_mult = 0.025
	}
	triggered_sector_modifier = {
		potential = {
			trait_is_wilderness_check = no
		}
		planet_miners_minerals_produces_add = 0.125
	}
	triggered_sector_modifier = {
		potential = {
			trait_is_wilderness_check = yes
		}
		planet_jobs_minerals_produces_mult = 0.012
	}
	leader_class = { scientist }
	initial = no
	randomized = no

	ai_categories = {
		physics
		society
		engineering
	}
}

################Ruler

leader_trait_ruler_godly = {
	icon = "gfx/interface/icons/traits/trait_god.dds"
	force_councilor_trait = yes
	councilor_modifier = {
		all_technology_research_speed = 0.20
		starbase_upgrade_cost_mult = -0.50
        starbase_upgrade_speed_mult = 0.50
        starbase_shipyard_build_cost_mult = -0.50
        country_ship_upgrade_cost_mult = -0.50
		terraform_speed_mult = 1.00
		terraforming_cost_mult = -0.50
		species_leader_exp_gain = 1.00
		station_researchers_produces_mult = 1.00
		num_tech_alternatives_add = 2
		planet_colony_development_speed_mult = 1.0
		armies_cost_mult = -0.25
        pop_government_ethic_attraction = 0.25
		country_base_influence_produces_add = 1.0
		country_subject_acceptance_add = 0.25
		country_command_limit_add = 200
		country_naval_cap_mult = 0.25
	}
	leader_class = { official commander scientist }
	initial = no
	randomized = no
}

leader_trait_ruler_demigod = {
	icon = "gfx/interface/icons/traits/trait_demigod.dds"
	force_councilor_trait = yes
	councilor_modifier = {
		all_technology_research_speed = 0.10
		starbase_upgrade_cost_mult = -0.25
        starbase_upgrade_speed_mult = 0.25
        starbase_shipyard_build_cost_mult = -0.25
        country_ship_upgrade_cost_mult = -0.25
		terraform_speed_mult = 0.50
		terraforming_cost_mult = -0.25
		species_leader_exp_gain = 0.50
		station_researchers_produces_mult = 0.50
		num_tech_alternatives_add = 1
		planet_colony_development_speed_mult = 0.5
		armies_cost_mult = -0.10
        pop_government_ethic_attraction = 0.10
		country_base_influence_produces_add = 0.5
		country_subject_acceptance_add = 0.10
		country_command_limit_add = 100
		country_naval_cap_mult = 0.10
	}
	leader_class = { official commander scientist }
	initial = no
	randomized = no
}

leader_trait_ruler_godly_nexus = {
	icon = "gfx/interface/icons/traits/trait_god.dds"
	force_councilor_trait = yes
	councilor_modifier = {
		all_technology_research_speed = 0.20
		starbase_upgrade_cost_mult = -0.50
        starbase_upgrade_speed_mult = 0.50
        starbase_shipyard_build_cost_mult = -0.50
        country_ship_upgrade_cost_mult = -0.50
		terraform_speed_mult = 1.00
		terraforming_cost_mult = -0.50
		species_leader_exp_gain = 1.00
		station_researchers_produces_mult = 1.00
		num_tech_alternatives_add = 2
		planet_colony_development_speed_mult = 1.0
		armies_cost_mult = -0.25
        pop_government_ethic_attraction = 0.25
		country_base_influence_produces_add = 1.0
		country_subject_acceptance_add = 0.25
		country_command_limit_add = 200
		country_naval_cap_mult = 0.25
	}
	leader_class = { official commander scientist }
	initial = no
	randomized = no
}

leader_trait_ruler_demigod_nexus = {
	icon = "gfx/interface/icons/traits/trait_demigod.dds"
	force_councilor_trait = yes
	councilor_modifier = {
		all_technology_research_speed = 0.10
		starbase_upgrade_cost_mult = -0.25
        starbase_upgrade_speed_mult = 0.25
        starbase_shipyard_build_cost_mult = -0.25
        country_ship_upgrade_cost_mult = -0.25
		terraform_speed_mult = 0.50
		terraforming_cost_mult = -0.25
		species_leader_exp_gain = 0.50
		station_researchers_produces_mult = 0.50
		num_tech_alternatives_add = 1
		planet_colony_development_speed_mult = 0.5
		armies_cost_mult = -0.10
        pop_government_ethic_attraction = 0.10
		country_base_influence_produces_add = 0.5
		country_subject_acceptance_add = 0.10
		country_command_limit_add = 100
		country_naval_cap_mult = 0.10
	}
	leader_class = { official commander scientist }
	initial = no
	randomized = no
}
```

## mods/RKGodlyTraitsRedux44/descriptor.mod

```text
version="1.0.0"
tags={
	"Species"
	"Leaders"
}
picture="thumbnail.png"
name="RK Godly Traits Redux 4.4"
supported_version="v4.4.*"
```

## mods/RKGodlyTraitsRedux44/events/GTR_trait_events.txt

```text
namespace = GTR_trait

country_event = {
    id = GTR_trait.101
    hide_window = yes
	is_triggered_only = yes

    trigger = {
        from = {
            species = {
                OR = {
                    has_trait = GTR_trait_deus_machina
                    has_trait = GTR_trait_borg
                    has_trait = GTR_trait_godly_species
                    has_trait = GTR_trait_nephalem
                }
            }
            NOR = {
                has_trait = leader_trait_commander_godly
                has_trait = leader_trait_official_godly
                has_trait = leader_trait_scientist_godly
                has_trait = leader_trait_ruler_godly
            }
        }
    }

    immediate = {
        from = {
            if = {
                limit = { leader_class = commander }
                add_trait = {
					trait = leader_trait_commander_godly
					show_message = no
				}
            }
            if = {
                limit = { leader_class = official }
                add_trait = {
					trait = leader_trait_official_godly
					show_message = no
				}
            }
            if = {
                limit = { leader_class = scientist }
				add_trait = {
					trait = leader_trait_scientist_godly
					show_message = no
				}
            }
            set_leader_flag = leader_death_events_blocked
            set_leader_flag = immune_to_negative_traits
        }
	}
}

country_event = {
    id = GTR_trait.102
    hide_window = yes
	is_triggered_only = yes

    trigger = {
        from = {
            species = {
                OR = {
                    has_trait = GTR_trait_demigods
                    has_trait = GTR_trait_divine_ancestors
                }
            }
            NOR = {
                has_trait = leader_trait_commander_demigod
                has_trait = leader_trait_official_demigod
                has_trait = leader_trait_scientist_demigod
                has_trait = leader_trait_ruler_demigod
            }
        }
    }
    immediate = {
        from = {
            if = {
                limit = { leader_class = commander }
                add_trait = {
					trait = leader_trait_commander_demigod
					show_message = no
				}
            }
            if = {
                limit = { leader_class = official }
                add_trait = {
					trait = leader_trait_official_demigod
					show_message = no
				}
            }
            if = {
                limit = { leader_class = scientist }
				add_trait = {
					trait = leader_trait_scientist_demigod
					show_message = no
				}
            }
            set_leader_flag = leader_death_events_blocked
            set_leader_flag = immune_to_negative_traits
        }
	}
}

country_event = {
    id = GTR_trait.103
    hide_window = yes
	is_triggered_only = yes

    immediate = {
        every_owned_leader = {
            limit = {
                species = {
                    OR = {
                        has_trait = GTR_trait_demigods
                        has_trait = GTR_trait_divine_ancestors
                    }
                }
                NOR = {
                    has_trait = leader_trait_commander_demigod
                    has_trait = leader_trait_official_demigod
                    has_trait = leader_trait_scientist_demigod
                }
            }
            if = {
                limit = { leader_class = commander }
                add_trait = {
					trait = leader_trait_commander_demigod
					show_message = no
				}
            }
            if = {
                limit = { leader_class = official }
                add_trait = {
					trait = leader_trait_official_demigod
					show_message = no
				}
            }
            if = {
                limit = { leader_class = scientist }
				add_trait = {
					trait = leader_trait_scientist_demigod
					show_message = no
				}
            }
            set_leader_flag = leader_death_events_blocked
            set_leader_flag = immune_to_negative_traits
        }
        every_pool_leader = {
            limit = {
                species = {
                    OR = {
                        has_trait = GTR_trait_demigods
                        has_trait = GTR_trait_divine_ancestors
                    }
                }
                NOR = {
                    has_trait = leader_trait_commander_demigod
                    has_trait = leader_trait_official_demigod
                    has_trait = leader_trait_scientist_demigod
                }
            }
            if = {
                limit = { leader_class = commander }
                add_trait = {
					trait = leader_trait_commander_demigod
					show_message = no
				}
            }
            if = {
                limit = { leader_class = official }
                add_trait = {
					trait = leader_trait_official_demigod
					show_message = no
				}
            }
            if = {
                limit = { leader_class = scientist }
				add_trait = {
					trait = leader_trait_scientist_demigod
					show_message = no
				}
            }
            set_leader_flag = leader_death_events_blocked
            set_leader_flag = immune_to_negative_traits
        }
        every_owned_leader = {
            limit = {
                species = {
                    OR = {
                        has_trait = GTR_trait_deus_machina
                        has_trait = GTR_trait_borg
                        has_trait = GTR_trait_godly_species
                        has_trait = GTR_trait_nephalem
                    }
                }
                NOR = {
                    has_trait = leader_trait_commander_godly
                    has_trait = leader_trait_official_godly
                    has_trait = leader_trait_scientist_godly
                }
            }
            if = {
                limit = { leader_class = commander }
                add_trait = {
					trait = leader_trait_commander_godly
					show_message = no
				}
            }
            if = {
                limit = { leader_class = official }
                add_trait = {
					trait = leader_trait_official_godly
					show_message = no
				}
            }
            if = {
                limit = { leader_class = scientist }
				add_trait = {
					trait = leader_trait_scientist_godly
					show_message = no
				}
            }
            set_leader_flag = leader_death_events_blocked
            set_leader_flag = immune_to_negative_traits
        }
        every_pool_leader = {
            limit = {
                species = {
                    OR = {
                        has_trait = GTR_trait_deus_machina
                        has_trait = GTR_trait_borg
                        has_trait = GTR_trait_godly_species
                        has_trait = GTR_trait_nephalem
                    }
                }
                NOR = {
                    has_trait = leader_trait_commander_godly
                    has_trait = leader_trait_official_godly
                    has_trait = leader_trait_scientist_godly
                }
            }
            if = {
                limit = { leader_class = commander }
                add_trait = {
					trait = leader_trait_commander_godly
					show_message = no
				}
            }
            if = {
                limit = { leader_class = official }
                add_trait = {
					trait = leader_trait_official_godly
					show_message = no
				}
            }
            if = {
                limit = { leader_class = scientist }
				add_trait = {
					trait = leader_trait_scientist_godly
					show_message = no
				}
            }
            set_leader_flag = leader_death_events_blocked
            set_leader_flag = immune_to_negative_traits
        }
    }
}

country_event = {
    id = GTR_trait.104
    hide_window = yes
	is_triggered_only = yes


    trigger = {
        from = {
            species = {
                OR = {
                    has_trait = GTR_trait_deus_machina
                    has_trait = GTR_trait_borg
                    has_trait = GTR_trait_godly_species
                    has_trait = GTR_trait_nephalem
                }
            }
            is_ruler = yes
            NOR = {
                has_trait = leader_trait_ruler_godly
                has_trait = leader_trait_ruler_godly_nexus
            }
        }
    }
    immediate = {

        if = {
            limit = {
                NOR = {
                    has_authority = auth_hive_mind
                    has_authority = auth_machine_intelligence
                }
                from = {
                    add_trait = {
					trait = leader_trait_ruler_godly
					show_message = no
				}
                    set_leader_flag = leader_death_events_blocked
                    set_leader_flag = immune_to_negative_traits
                }
            }
        }
        if = {
            limit = {
                OR = {
                    has_authority = auth_hive_mind
                    has_authority = auth_machine_intelligence
                }
                from = {
                add_trait = {
					trait = leader_trait_ruler_godly_nexus
					show_message = no
				}
                }
            }
        }
	}
}

country_event = {
    id = GTR_trait.105
    hide_window = yes
	is_triggered_only = yes


    trigger = {
        from = {
            species = {
                OR = {
                    has_trait = GTR_trait_demigods
                    has_trait = GTR_trait_divine_ancestors
                }
            }
            is_ruler = yes
            NOR = {
                has_trait = leader_trait_ruler_demigod
                has_trait = leader_trait_ruler_demigod_nexus
            }
        }
    }
    immediate = {
        from = {
            add_trait = {
					trait = leader_trait_ruler_demigod
					show_message = no
				}
        }
        if = {
            limit = {
                OR = {
                    has_authority = auth_hive_mind
                    has_authority = auth_machine_intelligence
                }
                from = { is_ruler = yes }
            }
            from = {
                add_trait = {
					trait = leader_trait_ruler_demigod_nexus
					show_message = no
				}
            }
        }
	}
}
country_event = {
    id = GTR_trait.106
    hide_window = yes
	is_triggered_only = yes
    immediate = {
        from = {
            if = {
                limit = { has_trait = leader_trait_ruler_demigod }
                remove_trait = leader_trait_ruler_demigod
            }
            if = {
                limit = { has_trait = leader_trait_ruler_godly }
                remove_trait = leader_trait_ruler_godly
            }
        }
	}
}

country_event = {
    id = GTR_trait.107
    hide_window = yes
	is_triggered_only = yes

    trigger = {
        from = {
            species = {
                OR = {
                    has_trait = GTR_trait_demigods
                    has_trait = GTR_trait_divine_ancestors
                }
            }
            NOR = {
                has_trait = leader_trait_ruler_demigod
                has_trait = leader_trait_ruler_demigod_nexus
            }
        }
    }

    immediate = {
        ruler = {
            add_trait = {
					trait = leader_trait_ruler_demigod_nexus
					show_message = no
				}
        }
	}
}

country_event = {
    id = GTR_trait.108
    hide_window = yes
	is_triggered_only = yes

    trigger = {
        from = {
            species = {
                OR = {
                    has_trait = GTR_trait_deus_machina
                    has_trait = GTR_trait_borg
                    has_trait = GTR_trait_godly_species
                    has_trait = GTR_trait_nephalem
                }
            }
            NOR = {
                has_trait = leader_trait_ruler_godly
                has_trait = leader_trait_ruler_godly_nexus
            }
        }
    }

    immediate = {
        ruler = {
            add_trait = {
					trait = leader_trait_ruler_godly_nexus
					show_message = no
				}
        }
	}
}

```

## mods/RKGodlyTraitsRedux44/localisation/english/GTR_l_english.yml

```yaml
﻿l_english:
leader_trait_commander_godly: "A godly commander"
leader_trait_commander_godly_desc: "An commander only gods could produce."
leader_trait_official_godly: "A godly official"
leader_trait_official_godly_desc: "A official only gods could produce."
leader_trait_scientist_godly: "A godly scientist"
leader_trait_scientist_godly_desc: "A scientist only gods could produce."
leader_trait_ruler_godly: "A godly Ruler"
leader_trait_ruler_godly_desc: "A Monarch to rule gods."
leader_trait_ruler_godly_nexus: "A godly Ruler"
leader_trait_ruler_godly_nexus_desc: "A Monarch to rule gods."

leader_trait_commander_demigod: "A demigod commander"
leader_trait_commander_demigod_desc: "Can do the Kessel run in 11 Parsec!"
leader_trait_official_demigod: "A demigod official"
leader_trait_official_demigod_desc: "You don't want to see their spreadsheets."
leader_trait_scientist_demigod: "A demigod scientist"
leader_trait_scientist_demigod_desc: "Writes a full 100-page research paper in only 15 hours."
leader_trait_ruler_demigod: "A demigod Ruler"
leader_trait_ruler_demigod_desc: "Has a very pointy finger. People know better than to doubt them."
leader_trait_ruler_demigod_nexus: "A demigod Ruler"
leader_trait_ruler_demigod_nexus_desc: "Has a very pointy finger. People know better than to doubt them."

GTR_trait_nephalem: "Neffalim"
GTR_trait_nephalem_desc: "Xeno-compatibility gone wrong. At least Diablo and Malthael aren't coming after you."

GTR_trait_godly_species: "Godly Species"
GTR_trait_godly_species_desc: "You are gods. They will respect you as they should respect gods. \n\nLeaders from this species gain an additional trait."

GTR_trait_demigods: "Demigods"
GTR_trait_demigods_desc: "The result of ancient Xeno-compatibility. Is it really that bad?"

GTR_trait_divine_ancestors: "Divine Ancestors"
GTR_trait_divine_ancestors_desc: "Divine blood runs thin..."

GTR_trait_hyper_fertile: "Hyper Fertile"
GTR_trait_hyper_fertile_desc: "9 months of pregnancy? What about 9 weeks."

GTR_trait_super_fertile: "Super Fertile"
GTR_trait_super_fertile_desc: "100% Twins guaranteed. Buy now with 40% off."

GTR_trait_nano_assemblers: "Nano Assemblers"
GTR_trait_nano_assemblers_desc: "> 4 & X"

GTR_trait_everlasting: "Everlasting"
GTR_trait_everlasting_desc: "We just don't die. Unless we do die, then we die."

GTR_trait_ancient: "Ancient Species"
GTR_trait_ancient_desc: "Immortal, but not invulnerable."

GTR_trait_ancient_hive: "Ancient Hive Drones"
GTR_trait_ancient_hive_desc: "These drones belong in the Ancient Hive."

GTR_trait_deus_machina: "Deus Machina"
GTR_trait_deus_machina_desc: "The ex was destroyed, must have been the Terminator \n\nLeaders from this species gain an additional trait."

GTR_trait_borg: "Borg"
GTR_trait_borg_desc: "I am become Borg, the destroyer of worlds. \n\nLeaders from this species gain an additional trait."

trait_4_point: "4 extra points"
trait_4_point_desc: "It took you a while to get to space. +4 trait points."
trait_8_point: "8 extra points"
trait_8_point_desc: "It took you a long time to get to space. +8 trait points."
trait_16_point: "16 extra points"
trait_16_point_desc: "It took you ages to get to space. Legend says that you are older than the fallen empires. +16 trait points."
trait_32_point: "32 extra points"
trait_32_point_desc: "It took you almost forever to get to space. You were the first intelligent lifeforms. +32 trait points."

GTR_extra_traits_4: "4 extra perk picks"
GTR_extra_traits_4_desc: "Your genome is impressive. +4 trait picks."
GTR_extra_traits_8: "8 extra perk picks"
GTR_extra_traits_8_desc: "Your genome catalogues all life on your planet. +8 trait picks."
GTR_extra_traits_16: "16 extra perk picks"
GTR_extra_traits_16_desc: "Your genome catalogues all life in the galaxy. +16 trait picks."
GTR_extra_traits_32: "32 extra perk picks"
GTR_extra_traits_32_desc: "Your genome catalouges all life in the known universe. +32 trait picks."
```

## mods/RKImmortalLeadersTrait/README.md

```markdown
# RK Immortal Leaders Trait

Local 4.4-compatible replacement for the old `Immortal Leaders Trait` Workshop mod.

This keeps the old trait key `trait_Immortality` so existing custom empire
templates are more likely to keep working, but uses current 4.4 species trait
syntax and the engine-supported `immortal_leaders = yes` flag.

Do not enable this together with another immortality trait mod unless you want
duplicate species traits in empire creation.
```

## mods/RKImmortalLeadersTrait/common/traits/rk_immortal_leaders_trait.txt

```text
trait_Immortality = {
	cost = 1
	category = normal
	initial = yes
	randomized = no
	immortal_leaders = yes

	allowed_archetypes = { BIOLOGICAL LITHOID ROBOT MACHINE }
	tags = { organic machine positive leader special }
	opposites = {
		"trait_enduring"
		"trait_venerable"
		"trait_fleeting"
		"trait_fleeting_lithoid"
	}

	ai_weight = {
		weight = 0
	}
}
```

## mods/RKImmortalLeadersTrait/descriptor.mod

```text
version="1.0.0"
tags={
	"Species"
	"Gameplay"
	"Leaders"
}
name="RK Immortal Leaders Trait"
supported_version="v4.4.*"
```

## mods/RKImmortalLeadersTrait/localisation/english/rk_immortal_leaders_trait_l_english.yml

```yaml
l_english:
 trait_Immortality:0 "Immortality"
 trait_Immortality_desc:0 "This species' leaders do not die of old age."
```

## mods/RKMilitusExtraTraitPicks/README.md

```markdown
# RK Militus Extra Trait Picks

Local 4.4-compatible replacement for `Militus' Extra Trait Points`.

Values preserved from the source mod:

- Biological and lithoid: 2 trait points, 15 picks.
- Machine: 1 trait point, 13 picks.
- Robot: 0 trait points, 11 picks.

This overwrites `common/species_archetypes/00_species_archetypes.txt` using the
current 4.4 vanilla file as its base so new 4.4 resource blocks are preserved.
Enable only one species-archetype trait-points mod at a time.
```

## mods/RKMilitusExtraTraitPicks/common/species_archetypes/00_species_archetypes.txt

```text
# 4.4 vanilla species archetypes with Militus-style extra picks.

@robot_trait_points = 0
@robot_max_traits = 11
@machine_trait_points = 1
@machine_max_traits = 13
@species_trait_points = 2
@species_max_traits = 15

BIOLOGICAL = {
	species_trait_points = @species_trait_points
	species_max_traits = @species_max_traits

	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}

ROBOT = {
	species_trait_points = @robot_trait_points
	species_max_traits = @robot_max_traits
	robotic = yes
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

MACHINE = {
	species_trait_points = @machine_trait_points
	species_max_traits = @machine_max_traits
	robotic = yes
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

PRESAPIENT = {
	species_trait_points = @species_trait_points
	species_max_traits = @species_max_traits
	uses_modifiers = no
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

LITHOID = {
	inherit_trait_points_from = BIOLOGICAL
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}

OTHER = {
	uses_modifiers = no
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}
```

## mods/RKMilitusExtraTraitPicks/descriptor.mod

```text
version="1.0.0"
tags={
	"Balance"
	"Species"
	"Gameplay"
}
name="RK Militus Extra Trait Picks"
supported_version="v4.4.*"
```

## mods/RKMoreTraitPoints/README.md

```markdown
# RK More Trait Points

Local 4.4-compatible replacement for the old `More Trait Points` Workshop mod.

Values preserved from the source mod:

- Biological and lithoid: 3 trait points, 7 picks.
- Machine: 2 trait points, 7 picks.
- Robot: 0 trait points, 4 picks.

This overwrites `common/species_archetypes/00_species_archetypes.txt` using the
current 4.4 vanilla file as its base so new 4.4 resource blocks are preserved.
Enable only one species-archetype trait-points mod at a time.
```

## mods/RKMoreTraitPoints/common/species_archetypes/00_species_archetypes.txt

```text
# 4.4 vanilla species archetypes with RK More Trait Points values.

@robot_trait_points = 0
@robot_max_traits = 4
@machine_trait_points = 2
@machine_max_traits = 7
@species_trait_points = 3
@species_max_traits = 7

BIOLOGICAL = {
	species_trait_points = @species_trait_points
	species_max_traits = @species_max_traits

	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}

ROBOT = {
	species_trait_points = @robot_trait_points
	species_max_traits = @robot_max_traits
	robotic = yes
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

MACHINE = {
	species_trait_points = @machine_trait_points
	species_max_traits = @machine_max_traits
	robotic = yes
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

PRESAPIENT = {
	species_trait_points = @species_trait_points
	species_max_traits = @species_max_traits
	uses_modifiers = no
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

LITHOID = {
	inherit_trait_points_from = BIOLOGICAL
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}

OTHER = {
	uses_modifiers = no
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}
```

## mods/RKMoreTraitPoints/descriptor.mod

```text
version="1.0.0"
tags={
	"Species"
	"Utilities"
	"Balance"
}
name="RK More Trait Points"
supported_version="v4.4.*"
```

## mods/RKThreeCivicMoreTraitPointsPicks/README.md

```markdown
# RK 3 Civic Points + More Trait Points/Picks

Local 4.4-compatible replacement for `3 Civic Points + More Trait Points/Picks`.

Values preserved from the source mod:

- Civic points: 3.
- Biological and lithoid: 3 trait points, 7 picks.
- Machine: 2 trait points, 6 picks.
- Robot: 0 trait points, 5 picks.

This overwrites `common/species_archetypes/00_species_archetypes.txt` using the
current 4.4 vanilla file as its base so new 4.4 resource blocks are preserved.
Enable only one species-archetype trait-points mod at a time.
```

## mods/RKThreeCivicMoreTraitPointsPicks/common/defines/rk_trait_points_defines.txt

```text
NGameplay = {
	GOVERNMENT_CIVIC_POINTS_BASE = 3
}
```

## mods/RKThreeCivicMoreTraitPointsPicks/common/species_archetypes/00_species_archetypes.txt

```text
# 4.4 vanilla species archetypes with 3-civic trait-point values.

@robot_trait_points = 0
@robot_max_traits = 5
@machine_trait_points = 2
@machine_max_traits = 6
@species_trait_points = 3
@species_max_traits = 7

BIOLOGICAL = {
	species_trait_points = @species_trait_points
	species_max_traits = @species_max_traits

	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}

ROBOT = {
	species_trait_points = @robot_trait_points
	species_max_traits = @robot_max_traits
	robotic = yes
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

MACHINE = {
	species_trait_points = @machine_trait_points
	species_max_traits = @machine_max_traits
	robotic = yes
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

PRESAPIENT = {
	species_trait_points = @species_trait_points
	species_max_traits = @species_max_traits
	uses_modifiers = no
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
	}
}

LITHOID = {
	inherit_trait_points_from = BIOLOGICAL
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}

OTHER = {
	uses_modifiers = no
	resources = {
		category = planet_pops
		inline_script = "pop_resources/pop_misc_production"
		produces = {
			trigger = {
				exists = planet
				planet = {
					has_modifier = astralnomical_interest_modifier
				}
				is_enslaved = no
			}
			physics_research = 1
		}
	}
}
```

## mods/RKThreeCivicMoreTraitPointsPicks/descriptor.mod

```text
version="1.0.0"
tags={
	"Balance"
	"Gameplay"
	"Species"
}
name="RK 3 Civic Points + More Trait Points/Picks"
supported_version="v4.4.*"
```

## mods/StellarAIDirector/README.md

```markdown
# Stellar AI Director

Late-loading deterministic AI policy patch for the active Irony playset.

This mod is a deterministic, full-power AI replacement policy for the current
4.4 high-scale playset. It does not try to preserve vanilla or Stellar AI
assumptions after the opening curve; it encodes explicit state gates,
priorities, and emergency exits for Gigastructural Engineering, NSC3, ESC NEXT,
Starbase Extended, and the active supporting mods.

## Required Parents

- Stellar AI
- Gigastructural Engineering & More (4.4)
- NSC3
- Extra Ship Components NEXT
- Starbase Extended 3.0
- !!!Universal Resource Patch [2.4+]

Detected selected collection: `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`.

Missing required Steam parents during generation: none.

## Scope

- Adds scripted decision-state triggers for survival, recovery, megastructure
  prep, safe commit, surplus-sink pressure, and shipyard payoff exploitation.
- Overrides Stellar AI's megastructure alloy budget object with explicit
  emergency exits and larger reserves for Gigas/NSC3-scale projects.
- Replaces the base economic plan with a mod-set-specific high-scale survival
  plan that forces research, alloy, trade, naval-cap, tall-scaling, and
  megastructure pressure on a mid-2300s crisis curve.
- Adds economic-plan targets for alloy reserves, Gigas special resources,
  and static-defense/starbase pressure when empires need to climb toward
  Gigas/NSC3/ESC-scale economy and fleet power.
- Adds trade-capacity recovery and reserve subplans so the Director preserves
  Stellaris 4.4 logistics/upkeep headroom instead of treating trade as a
  normal buy/sell commodity.
- Adds a monthly market cap-breaker for AI empires that are wasting large
  positive-income stockpiles, converting marketable overflow into trade
  currency instead of letting storage caps void the income.
- Adds a two-pulse stranded-fleet recovery guard that uses vanilla
  `set_mia = mia_return_home` only for idle, MIA-eligible AI fleets outside
  their owner's space while the homeland is under wartime pressure.
- Adds a fleet-throughput economic subplan so Mega Shipyard unlocks and strong
  surplus can become fleet power without ignoring energy/alloy/trade runway checks.
- Adds a planetary-capacity economic subplan plus direct research lab and
  habitat science district construction weights for safe mineral/energy-backed
  tall growth without broad job automation rewrites or trade logistics collapse.
- Adds mandatory unlock-research pressure so AI empires keep pushing
  engineering/research/unity toward Mega Engineering, Mega Shipyard,
  planetcraft/systemcraft chains, NSC hulls, and ESC component tiers.
- Adds a bounded V1 threat-response layer for observed classified aggression:
  opinion modifiers, timed relation/country flags, and a third-party defensive
  readiness economy subplan capped at alloys 7, energy 6, and naval cap 40.
- Keeps unknown or unclassified war goals inert and does not declare wars,
  join wars, add punitive casus belli, or override diplomatic actions.
- Adds full-object route overrides for Mega Engineering, Mega Shipyard, Gigas
  planetcraft/systemcraft unlocks, NSC3 hull unlocks, ESC high-tier component
  unlocks, AP/tradition pressure, economy megastructures, planetcraft, war moon,
  systemcraft, and ESC starbase reactor support.
- Leaves ESC internal component-template `key = ...` overrides and direct NSC3
  ship-design templates as manual-review blockers until the atlas models those
  loader surfaces safely.

## Load Order

Place Stellar AI Director after all required parents and after parent
compatibility patches that the Director must supersede. In the current selected
collection, the latest required parent is at load position
115.
The Director should be below Stellar AI so its megastructure alloy reserve
override wins intentionally.

## Load Proof

When a player-controlled country starts, the mod fires a one-time popup titled
`Stellar AI Director Loaded`. Seeing that popup proves Irony loaded the Director into
the active playset and the game executed the Director event/on_action surface.

## Surplus Sink Ordering

After survival and recovery gates, the Director treats strong alloy/energy
surplus, capped marketable resources, or under-curve research as signals that
the empire needs useful spending outlets. The v1 order is:

1. research sink;
2. fleet-production sink;
3. unity sink.

`source_has_ai_weight` in the ROI matrix only reports whether the parent mod
defined an upstream AI weight. The Director's own policy is expressed in the
separate `director_*` columns.

## Validation

Run:

```powershell
python tools/validate_stellar_ai_director_patch.py
python -m unittest discover -s tools/tests
```
```

## mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: intentionally replaces upstream megastructure alloy
# budgeting with high-scale Gigas/NSC3 survival pressure. This is deliberately
# aggressive: an AI that can build megastructures but does not reserve for them
# will lose the modded crisis curve.

alloys_expenditure_megastructures = {
	resource = alloys
	type = expenditure
	category = megastructures

	potential = {
		is_country_type = default
		can_build_megastructures = yes
		NOT = { staid_pause_new_megastructure = yes }
	}

	weight = {
		weight = 8

		modifier = { factor = 0.5 staid_survival_mode = yes }
		modifier = { factor = 1.5 staid_recovery_mode = yes }
		modifier = { factor = 5 staid_megastructure_prep_ready = yes }
		modifier = {
			factor = 8
			staid_megastructure_commit_safe = yes
			any_owned_megastructure = { can_be_upgraded = yes }
		}
		modifier = {
			factor = 5
			has_technology = tech_mega_engineering
		}
		modifier = {
			factor = 3
			years_passed > 79
		}
	}

	desired_min = {
		base = 25000
		modifier = { add = 100000 staid_megastructure_prep_ready = yes }
		modifier = {
			add = 250000
			staid_megastructure_commit_safe = yes
			any_owned_megastructure = { can_be_upgraded = yes }
		}
		modifier = { add = 500000 years_passed > 119 }
	}

	desired_max = {
		base = 100000
		modifier = { add = 250000 has_technology = tech_mega_engineering }
		modifier = { add = 500000 staid_megastructure_prep_ready = yes }
		modifier = {
			add = 1000000
			staid_megastructure_commit_safe = yes
			any_owned_megastructure = { can_be_upgraded = yes }
		}
		modifier = { add = 1500000 years_passed > 119 }
	}
}
```

## mods/StellarAIDirector/common/ai_budget/zzz_staid_gigas_resource_budgets.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object overrides: intentionally replaces narrow Gigas special-resource
# megastructure budget objects so the Director can pause exotic projects during
# survival/recovery and reserve rare resources for safe commits.

sentient_metal_expenditure_megastructures = {
	resource = giga_sr_sentient_metal
	type = expenditure
	category = megastructures

	potential = {
		is_country_type = default
		NOT = { staid_pause_new_megastructure = yes }
	}

	weight = {
		weight = 0.35
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.25 staid_recovery_mode = yes }
		modifier = { factor = 2 staid_megastructure_commit_safe = yes }
	}
}

negative_mass_expenditure_megastructures = {
	resource = giga_sr_negative_mass
	type = expenditure
	category = megastructures

	potential = {
		is_country_type = default
		NOT = { staid_pause_new_megastructure = yes }
	}

	weight = {
		weight = 0.30
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.20 staid_recovery_mode = yes }
		modifier = { factor = 2 staid_megastructure_commit_safe = yes }
	}
}

supertensiles_upkeep_megastructures = {
	resource = giga_sr_amb_megaconstruction
	type = upkeep
	category = megastructures

	potential = {
		is_country_type = default
		NOT = { staid_survival_mode = yes }
	}

	weight = {
		weight = 1
		modifier = { factor = 0.25 staid_recovery_mode = yes }
		modifier = { factor = 1.5 staid_megastructure_commit_safe = yes }
	}
}
```

## mods/StellarAIDirector/common/ai_budget/zzzz_staid_08_site_limited_expansion_ai_budget.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/ai_budget


# policy_route = conquest_escape_route; source = common/ai_budget/00_influence_budget.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
influence_expenditure_claims = {
	resource = influence
	type = expenditure
	category = claims

	potential = {
		is_nomadic = no
		NOT = {
			OR = {
				is_pacifist = yes
				has_crisis_level = crisis_level_2
			}
		}
		has_potential_claims = yes
	}

	weight = {
		weight = 0.15
	}
}


# policy_route = conquest_escape_route; source = common/ai_budget/00_influence_budget.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
influence_expenditure_claims_militarist = {
	resource = influence
	type = expenditure
	category = claims

	potential = {
		is_nomadic = no
		has_ethic = ethic_militarist
		has_potential_claims = yes
	}

	weight = {
		weight = 0.05
	}
}


# policy_route = conquest_escape_route; source = common/ai_budget/00_influence_budget.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
influence_expenditure_claims_fanatic_militarist = {
	resource = influence
	type = expenditure
	category = claims

	potential = {
		is_nomadic = no
		has_ethic = ethic_fanatic_militarist
		has_potential_claims = yes
	}

	weight = {
		weight = 0.10
	}
}

```

## mods/StellarAIDirector/common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: vanilla makes planet mineral spending less attractive as stockpiles grow.
# The Director reverses that for high-scale modded economies so idle pops and empty slots become spend pressure.

minerals_expenditure_planets_low = {
	resource = minerals
	type = expenditure
	category = planets

	potential = {
		is_country_type = default
		resource_stockpile_compare = { resource = minerals value < 1000 }
	}

	weight = {
		weight = 8.0
		modifier = { factor = 12 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 12 staid_core_deficit_short_runway = yes }
		modifier = { factor = 35 staid_construction_spenddown_pressure = yes }
		modifier = { factor = 18 staid_resource_waste_pressure = yes }
		modifier = { factor = 24 staid_high_scale_snowball_pressure = yes }
		modifier = { factor = 40 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }
		modifier = { factor = 30 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }
		modifier = { factor = 20 resource_stockpile_compare = { resource = minerals value > 10000 } }
		modifier = { factor = 30 resource_stockpile_compare = { resource = minerals value > 25000 } }
	}

	desired_min = {
		base = 2000
		modifier = { add = 5000 staid_core_deficit_short_runway = yes }
		modifier = { add = 10000 staid_planetary_capacity_growth_ready = yes }
		modifier = { add = 150000 staid_construction_spenddown_pressure = yes }
		modifier = { add = 25000 staid_high_scale_snowball_pressure = yes }
		modifier = { add = 100000 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }
		modifier = { add = 100000 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }
		modifier = { add = 75000 resource_stockpile_compare = { resource = minerals value > 25000 } }
	}

	desired_max = {
		base = 10000
		modifier = { add = 20000 staid_core_deficit_short_runway = yes }
		modifier = { add = 40000 staid_planetary_capacity_growth_ready = yes }
		modifier = { add = 500000 staid_construction_spenddown_pressure = yes }
		modifier = { add = 100000 staid_high_scale_snowball_pressure = yes }
		modifier = { add = 300000 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }
		modifier = { add = 300000 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }
		modifier = { add = 250000 resource_stockpile_compare = { resource = minerals value > 25000 } }
	}
}

minerals_expenditure_planets_med = {
	resource = minerals
	type = expenditure
	category = planets

	potential = {
		is_country_type = default
		resource_stockpile_compare = { resource = minerals value >= 1000 }
		resource_stockpile_compare = { resource = minerals value < 2000 }
	}

	weight = {
		weight = 14.0
		modifier = { factor = 12 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 12 staid_core_deficit_short_runway = yes }
		modifier = { factor = 35 staid_construction_spenddown_pressure = yes }
		modifier = { factor = 18 staid_resource_waste_pressure = yes }
		modifier = { factor = 24 staid_high_scale_snowball_pressure = yes }
		modifier = { factor = 40 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }
		modifier = { factor = 30 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }
		modifier = { factor = 20 resource_stockpile_compare = { resource = minerals value > 10000 } }
		modifier = { factor = 30 resource_stockpile_compare = { resource = minerals value > 25000 } }
	}

	desired_min = {
		base = 2000
		modifier = { add = 5000 staid_core_deficit_short_runway = yes }
		modifier = { add = 10000 staid_planetary_capacity_growth_ready = yes }
		modifier = { add = 150000 staid_construction_spenddown_pressure = yes }
		modifier = { add = 25000 staid_high_scale_snowball_pressure = yes }
		modifier = { add = 100000 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }
		modifier = { add = 100000 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }
		modifier = { add = 75000 resource_stockpile_compare = { resource = minerals value > 25000 } }
	}

	desired_max = {
		base = 10000
		modifier = { add = 20000 staid_core_deficit_short_runway = yes }
		modifier = { add = 40000 staid_planetary_capacity_growth_ready = yes }
		modifier = { add = 500000 staid_construction_spenddown_pressure = yes }
		modifier = { add = 100000 staid_high_scale_snowball_pressure = yes }
		modifier = { add = 300000 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }
		modifier = { add = 300000 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }
		modifier = { add = 250000 resource_stockpile_compare = { resource = minerals value > 25000 } }
	}
}

minerals_expenditure_planets_high = {
	resource = minerals
	type = expenditure
	category = planets

	potential = {
		is_country_type = default
		resource_stockpile_compare = { resource = minerals value >= 2000 }
	}

	weight = {
		weight = 28.0
		modifier = { factor = 12 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 12 staid_core_deficit_short_runway = yes }
		modifier = { factor = 35 staid_construction_spenddown_pressure = yes }
		modifier = { factor = 18 staid_resource_waste_pressure = yes }
		modifier = { factor = 24 staid_high_scale_snowball_pressure = yes }
		modifier = { factor = 40 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }
		modifier = { factor = 30 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }
		modifier = { factor = 20 resource_stockpile_compare = { resource = minerals value > 10000 } }
		modifier = { factor = 30 resource_stockpile_compare = { resource = minerals value > 25000 } }
	}

	desired_min = {
		base = 2000
		modifier = { add = 5000 staid_core_deficit_short_runway = yes }
		modifier = { add = 10000 staid_planetary_capacity_growth_ready = yes }
		modifier = { add = 150000 staid_construction_spenddown_pressure = yes }
		modifier = { add = 25000 staid_high_scale_snowball_pressure = yes }
		modifier = { add = 100000 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }
		modifier = { add = 100000 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }
		modifier = { add = 75000 resource_stockpile_compare = { resource = minerals value > 25000 } }
	}

	desired_max = {
		base = 10000
		modifier = { add = 20000 staid_core_deficit_short_runway = yes }
		modifier = { add = 40000 staid_planetary_capacity_growth_ready = yes }
		modifier = { add = 500000 staid_construction_spenddown_pressure = yes }
		modifier = { add = 100000 staid_high_scale_snowball_pressure = yes }
		modifier = { add = 300000 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }
		modifier = { add = 300000 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }
		modifier = { add = 250000 resource_stockpile_compare = { resource = minerals value > 25000 } }
	}
}
```

## mods/StellarAIDirector/common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/ascension_perks


# policy_route = economy_megastructure_core; source = common/ascension_perks/giga_ascension_perks.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
ap_gigastructural_constructs = {
	on_enabled = {
		custom_tooltip = "ap_gigastructural_constructs_add_research"
		hidden_effect = {
			if = { limit = { NOT = { has_technology = giga_tech_hrae_mc } }				add_research_option = giga_tech_hrae_mc }
			if = { limit = { NOT = { has_technology = giga_tech_ringworld_behemoth } }	add_research_option = giga_tech_ringworld_behemoth }
			if = { limit = { NOT = { has_technology = giga_tech_matrioshka_brain_1 } }	add_research_option = giga_tech_matrioshka_brain_1 }
		}
	}

	modifier = {
		country_megastructure_build_cap_add = 1
	}

	possible = {
		custom_tooltip = {
			fail_text = "requires_built_or_repaired_gigastructure"
			or = {
				has_country_flag = has_built_or_repaired_gigastructure
				and = {
					is_ai = yes
					or = {
						num_ascension_perks > 6
						any_country = {
							is_ai = no
							has_galactic_wonders = yes
						}
					}
				}
			}
		}
		custom_tooltip = { fail_text = "requires_ap_galactic_wonders"				has_galactic_wonders = yes }
		custom_tooltip = { fail_text = "requires_ascension_perks_3"					num_ascension_perks > 2 }
		custom_tooltip = { fail_text = "requires_mega_engineering"					has_technology = tech_mega_engineering }
		custom_tooltip = { fail_text = "requires_sentient_ai"						has_technology = tech_self_aware_logic }
		custom_tooltip = { fail_text = "requires_dark_matter"						has_technology = tech_mine_dark_matter }
		custom_tooltip = { fail_text = "requires_titanic_ringworld"				has_technology = giga_tech_ringworld_titanic_1 }
	}

	potential = {
		NOT = { has_ascension_perk = ap_gigastructural_constructs has_global_flag = giga_gigastructural_perk_disabled }
		is_nomadic = no
	}

	ai_weight = {
		factor = 120000

		# policy_route = economy_megastructure_core
		# source_object = ascension_perk:ap_gigastructural_constructs
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_core_unlock_research_priority_ready = yes } }
		modifier = { factor = 4 staid_core_unlock_research_priority_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 5 years_passed > 79 }
		modifier = { factor = 8 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
	}
}


# policy_route = planetcraft_route; source = common/ascension_perks/giga_ascension_perks.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
ap_celestial_printing = {
	on_enabled = {
		custom_tooltip = "ap_celestial_printing_effects"
		hidden_effect = {
			# if = { limit = { NOT = { has_technology = giga_tech_planetary_matter_harvesting } }		add_research_option = giga_tech_planetary_matter_harvesting } Removed tech?
			if = { limit = { NOT = { has_technology = giga_tech_lunar_assembly } }					add_research_option = giga_tech_lunar_assembly }
			if = { limit = { NOT = { has_technology = giga_tech_war_system_1 } } 					add_research_option = giga_tech_war_system_1 }
			if = {
				limit = { has_global_flag = giga_bulk_matter_cost_disabled }
				country_event = { id = giga_printer.1015 }
			}
		}
	}

	modifier = {
		country_megastructure_build_cap_add = 1
		megastructure_build_speed_mult = 0.20
		country_resource_max_add = 25000
		command_limit_mult = 0.3
	}

	possible = {
		custom_tooltip = { fail_text = "requires_ap_gigastructural_constructs"		has_gigastructural_constructs = yes }
		custom_tooltip = { fail_text = "requires_ascension_perks_3"					num_ascension_perks > 2 }
		custom_tooltip = { fail_text = "requires_war_planets"						has_technology = giga_tech_war_planet }
		custom_tooltip = { fail_text = "requires_tetraengineering"					has_technology = giga_tech_tetradimensional_engineering }
	}

	potential = {
		NOR = {
			has_ascension_perk = ap_celestial_printing
			AND = {
				has_global_flag = giga_celestial_printing_moon_disabled
				has_global_flag = giga_celestial_printing_planet_disabled
				has_global_flag = systemcraft_disabled
			}
		}
		is_nomadic = no
	}

	ai_weight = {
		factor = 180000

		# policy_route = planetcraft_route
		# source_object = ascension_perk:ap_celestial_printing
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_planetcraft_research_priority_ready = yes } }
		modifier = { factor = 4 staid_planetcraft_research_priority_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 6 years_passed > 79 }
		modifier = { factor = 10 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 4 has_technology = giga_tech_planet_assembly }
		modifier = { factor = 3 has_ascension_perk = ap_celestial_printing }
	}
}


# policy_route = conquest_escape_route; source = common/ascension_perks/00_ascension_perks.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
ap_lord_of_war = {
	potential = {
		host_has_dlc = "Overlord"
		NOR = {
			has_ascension_perk = ap_lord_of_war
			has_valid_civic = civic_fanatic_purifiers
			has_valid_civic = civic_scorched_earth
		}
		OR = {
			is_regular_empire = yes
			has_valid_civic = civic_machine_tactical_algorithms
		}
	}

	on_enabled ={
		custom_tooltip = ap_lord_of_war_tooltip
	}

	modifier = {
		country_enclave_capacity_add = 1
		diplo_weight_naval_mult = 0.25
		#Bonus to dividends frequency handled in the dividends situation.
	}


	ai_weight = {
		factor = 80000

		# policy_route = conquest_escape_route
		# source_object = ascension_perk:ap_lord_of_war
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 4 staid_aggressive_fleet_pressure = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 7 years_passed > 79 }
		modifier = { factor = 11 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 10 staid_site_limited_expansion_ready = yes }
		modifier = { factor = 5 staid_fleet_buildup_economy_safe = yes }
		modifier = { factor = 8 staid_militarist_conquest_strategy = yes }
		modifier = { factor = 6 has_ethic = ethic_militarist }
		modifier = { factor = 12 has_ethic = ethic_fanatic_militarist }
	}
}


# policy_route = raiding_pop_acquisition_route; source = common/ascension_perks/00_ascension_perks.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
ap_nihilistic_acquisition = {
	potential = {
		host_has_dlc = "Apocalypse"
		NOT = {
			has_ascension_perk = ap_nihilistic_acquisition
		}
		NOR = {
			has_valid_civic = civic_barbaric_despoilers
			has_origin = origin_slavers
			has_origin = origin_khan_successor
			has_origin = origin_wilderness
		}
	}

	on_enabled = {
		custom_tooltip = "allow_raiding"
	}

	possible = {
		OR = {
			is_authoritarian = yes
			is_xenophobe = yes
			has_ethic = ethic_gestalt_consciousness
		}
	}


	ai_weight = {
		factor = 170000

		# policy_route = raiding_pop_acquisition_route
		# source_object = ascension_perk:ap_nihilistic_acquisition
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_raiding_pop_acquisition_priority = yes } }
		modifier = { factor = 4 staid_raiding_pop_acquisition_priority = yes }
		modifier = { factor = 6 years_passed > 44 }
		modifier = { factor = 10 years_passed > 79 }
		modifier = { factor = 14 years_passed > 119 }
		modifier = { factor = 7 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 14 staid_raiding_pop_growth_strategy = yes }
		modifier = { factor = 8 staid_opening_military_to_pops = yes }
		modifier = { factor = 5 has_ethic = ethic_militarist }
		modifier = { factor = 10 has_ethic = ethic_fanatic_militarist }
	}
}

```

## mods/StellarAIDirector/common/bombardment_stances/zzzz_staid_12_militarist_raiding_bombardment.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: vanilla raiding bombardment stance with Director-owned abduct-pop AI weighting.

raiding = {
	trigger = {
		OR = {
			owner = { has_ascension_perk = ap_nihilistic_acquisition }
			owner = { has_valid_civic = civic_barbaric_despoilers }
			owner = { has_origin = origin_slavers }
			owner = { has_origin = origin_khan_successor }
			owner = { is_country_type = debt_collectors }
			AND = {
				owner = { is_mercenary = yes }
				controller = {
					OR = {
						has_ascension_perk = ap_nihilistic_acquisition
						has_valid_civic = civic_barbaric_despoilers
						has_origin = origin_slavers
						has_origin = origin_khan_successor
					}
				}
			}
		}
		NOT = {
			any_owned_ship = {
				has_ship_flag = behemoth_hatchling_ship
			}
		}
	}

	default = no

	stop_when_armies_dead = no
	stop_when_ground_combat = no
	abduct_pops = yes

	planet_damage = 0.5
	army_damage = 0.5

	kill_pop_chance = {
		base = 0.15
	}
	min_pops_to_kill_pop = 200
	kill_pop_amount = { min = 0 max = 200 }

	# root = fleet
	# from = planet

	ai_weight = {
		weight = 80
		modifier = {
			factor = 0
			exists = from
			from = {
				OR = {
					pop_amount < 200
					owner = { NOT = { is_hostile = root.owner } }
				}
			}
		}
		modifier = { factor = 60 owner = { staid_raiding_pop_growth_strategy = yes } }
		modifier = { factor = 25 owner = { staid_militarist_conquest_strategy = yes } }
		modifier = { factor = 8 owner = { staid_opening_military_to_pops = yes } }
		modifier = {
			factor = 0.25
			exists = from
			from = { owner = { has_claim = root.solar_system } }
		}
	}
}
```

## mods/StellarAIDirector/common/buildings/zzzz_staid_06_research_infrastructure_buildings.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/buildings


# Source-local variables required by copied parent objects.
@b1_minerals = 400
@b1_time = 360
@b1_upkeep = 2
@b2_minerals = 600
@b2_rare_cost = 50
@b2_rare_upkeep = 1
@b2_time = 480
@b2_upkeep = 5
@b3_minerals = 800
@b3_rare_cost = 100
@b3_rare_upkeep = 2
@b3_time = 600
@b3_upkeep = 8
@building_static_jobs = 200
@building_static_jobs_3 = 60
@building_static_jobs_high_3 = 120
@building_static_jobs_very_high_3 = 180
@nomadic_minerals_to_strategic_ratio	= 0.1
@research_building_tier1_coefficient = 4.8
@research_building_tier2_coefficient = 5.0
@research_lab_tier1_coefficient = 4.0
@research_lab_tier2_coefficient = 4.5
@research_lab_tier3_coefficient = 4.5

# policy_route = research_throughput_infrastructure; source = common/buildings/~stellarai_research_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_research_lab_1 = {
	can_build = yes
	base_buildtime = @b1_time
	exempt_from_ai_planet_specialization = no

	category = research

	building_sets = {
		research
	}

	potential = {
		NOR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
			has_modifier = penal_colony
		}
		exists = owner
		owner = {
			is_wilderness_empire = no
		}
		is_special_colony_type = no

		OR = {
			has_carrier_flag = ignore_ai_building_limitations
			owner = {
				is_ai = no
			}

			# AI is allowed to build one of these.
			AND = {
				has_any_research_zone = yes
				NOR = {
					has_building = building_research_lab_1
					has_building = building_research_lab_2
					has_building = building_research_lab_3
				}
			}

			# Nomadic AI is allowed to build up to 3 of these total across all tiers.
			AND = {
				owner = { is_nomadic = yes }
				tiered_building_below_cap = {
					BUILDING = research_lab
				}
			}
		}
	}

	allow = {
	}

	ai_weight_coefficient = 8

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
			has_modifier = penal_colony
		}
	}

	inline_script = {
		script = jobs/researchers_add
		AMOUNT = @building_static_jobs_3
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = exotic_gases
			COST = @b1_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		upkeep = {
			energy = @b1_upkeep
		}
	}

	prerequisites = {
		"tech_basic_science_lab_1"
	}

	upgrades = {
		"building_research_lab_2"
	}
	additional_ai_weight = 600
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_research_input_runway_safe = yes } } }
	}
}


# policy_route = research_throughput_infrastructure; source = common/buildings/~stellarai_research_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_research_lab_2 = {
	base_buildtime = @b2_time
	can_build = no
	category = research

	building_sets = {
		research
	}

	potential = {
		exists = owner
		owner = {
			is_wilderness_empire = no # see 'building_brain_node_3'
		}
		is_special_colony_type = no
	}

	allow = {
	}

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
			has_modifier = penal_colony
		}
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = exotic_gases
			COST = @b2_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		cost = {
			exotic_gases = @b2_rare_cost
		}
		upkeep = {
			energy = @b2_upkeep
			exotic_gases = @b2_rare_upkeep
		}
	}

	inline_script = {
		script = jobs/researchers_add
		AMOUNT = @building_static_jobs_high_3
	}

	prerequisites = {
		"tech_basic_science_lab_2"
	}

	show_tech_unlock_if = {
		is_wilderness_empire = no
	}
	upgrades = {
		"building_research_lab_3"
	}

	ai_weight_coefficient = 10
	additional_ai_weight = 900
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_research_input_runway_safe = yes } } }
	}
}


# policy_route = research_throughput_infrastructure; source = common/buildings/~stellarai_research_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_research_lab_3 = {
	base_buildtime = @b3_time
	category = research
	can_build = no
	building_sets = {
		research
	}

	potential = {
		exists = owner
		owner = {
			is_wilderness_empire = no # see 'building_brain_node_4'
		}
		is_special_colony_type = no
	}

	allow = {
	}

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
			has_modifier = penal_colony
		}
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = exotic_gases
			COST = @b3_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		cost = {
			exotic_gases = @b3_rare_cost
		}
		upkeep = {
			energy = @b3_upkeep
			exotic_gases = @b3_rare_upkeep
		}
	}

	inline_script = {
		script = jobs/researchers_add
		AMOUNT = @building_static_jobs_very_high_3
	}

	prerequisites = {
		"tech_basic_science_lab_3"
	}

	show_tech_unlock_if = {
		is_wilderness_empire = no
	}

	ai_weight_coefficient = 12
	additional_ai_weight = 1200
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_research_input_runway_safe = yes } } }
	}
}


# policy_route = research_throughput_infrastructure; source = common/buildings/~stellarai_research_buildings.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
building_institute = {
	base_buildtime = @b2_time
	planet_limit = 1
	category = research

	building_sets = {
		research
	}

	potential = {
		NOR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
			has_modifier = penal_colony
		}
		exists = owner
		owner = { is_regular_empire = yes }
	}

	destroy_trigger = {
		exists = owner
		OR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
			has_modifier = penal_colony
			owner = { is_regular_empire = no }
		}
	}

	convert_to = {
		building_supercomputer
	}

	allow = {
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = exotic_gases
			COST = @b2_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		cost = {
			exotic_gases = @b2_rare_cost
		}
		upkeep = {
			energy = @b2_upkeep
			exotic_gases = @b2_rare_upkeep
		}
	}

	planet_modifier = {
		planet_physicists_physics_research_produces_add = 0.5
		planet_biologists_society_research_produces_add = 0.5
		planet_engineers_engineering_research_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		planet_researchers_consumer_goods_upkeep_add = 1
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_machine_empire = yes
			}
		}
		planet_researchers_energy_upkeep_add = 2
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_hive_empire = yes
			}
		}
		planet_researchers_minerals_upkeep_add = 2
	}

	inline_script = {
		script = "jobs/politician_add_from_civic"
		AMOUNT = @building_static_jobs
		CIVIC = civic_technocracy
	}

	prerequisites = {
		"tech_global_research_initiative"
	}

	show_tech_unlock_if = {
		is_regular_empire = yes
	}

	ai_weight_coefficient = 8

	inline_script = {
		script = districts/ai_research_extra_weighting
		AMOUNT = 10
	}

	ai_weight = {
		factor = 1
		inline_script = {
			script = stellarai/rare_resource_guard_modifiers
			STRATEGIC_RESOURCE = exotic_gases
			MIN_INCOME = @b2_rare_upkeep
			MIN_STOCKPILE = 8
			EARLY_FACTOR = 0.25
			EARLY_YEARS = 61
			EARLY_STOCKPILE = 25
			SURPLUS_FACTOR = 1.08
			SURPLUS_INCOME = 4
			SURPLUS_STOCKPILE = 45
		}
		inline_script = {
			script = stellarai/invalid_planet_type_guard
			PLANET_FLAG = stellarai_invalid_for_research_to_build
		}

		modifier = { factor = 0 owner = { NOT = { staid_research_input_runway_safe = yes } } }
	}
	additional_ai_weight = 800
}


# policy_route = research_throughput_infrastructure; source = common/buildings/~stellarai_research_buildings.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
building_supercomputer = {
	base_buildtime = @b2_time
	planet_limit = 1
	icon = building_institute

	category = research

	building_sets = {
		research
	}

	potential = {
		exists = owner
		owner = {
			is_gestalt = yes
			is_wilderness_empire = no
		}
		NOR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
			has_modifier = penal_colony
		}
	}

	allow = {
		has_major_upgraded_capital = yes
	}

	destroy_trigger = {
		exists = owner
		OR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
			has_modifier = penal_colony
			owner = { is_regular_empire = yes }
			owner = { is_wilderness_empire = yes }
		}
	}

	convert_to = {
		building_institute
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = exotic_gases
			COST = @b2_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		cost = {
			exotic_gases = @b2_rare_cost
		}
		upkeep = {
			energy = @b2_upkeep
			exotic_gases = @b2_rare_upkeep
		}
	}

	planet_modifier = {
		planet_physicists_physics_research_produces_add = 0.5
		planet_biologists_society_research_produces_add = 0.5
		planet_engineers_engineering_research_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		planet_researchers_consumer_goods_upkeep_add = 1
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_machine_empire = yes
			}
		}
		planet_researchers_energy_upkeep_add = 2
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_hive_empire = yes
			}
		}
		planet_researchers_minerals_upkeep_add = 2
	}

	prerequisites = {
		"tech_global_research_initiative"
	}

	show_tech_unlock_if = {
		is_gestalt = yes
		is_wilderness_empire = no
	}

	ai_weight_coefficient = 8

	inline_script = {
		script = districts/ai_research_extra_weighting
		AMOUNT = 10
	}

	ai_weight = {
		factor = 1
		inline_script = {
			script = stellarai/rare_resource_guard_modifiers
			STRATEGIC_RESOURCE = exotic_gases
			MIN_INCOME = @b2_rare_upkeep
			MIN_STOCKPILE = 8
			EARLY_FACTOR = 0.25
			EARLY_YEARS = 61
			EARLY_STOCKPILE = 25
			SURPLUS_FACTOR = 1.08
			SURPLUS_INCOME = 4
			SURPLUS_STOCKPILE = 45
		}
		inline_script = {
			script = stellarai/invalid_planet_type_guard
			PLANET_FLAG = stellarai_invalid_for_research_to_build
		}

		modifier = { factor = 0 owner = { NOT = { staid_research_input_runway_safe = yes } } }
	}
	additional_ai_weight = 800
}


# policy_route = research_throughput_infrastructure; source = common/buildings/~stellarai_research_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_archaeostudies_faculty = {
	base_buildtime = @b2_time
	planet_limit = 1
	category = research

	building_sets = {
		research
	}

	empire_limit = {
		base = 1
	}

	potential = {
		NOR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
			has_modifier = penal_colony
		}
		exists = owner
		owner = {
			is_wilderness_empire = no
		}
	}

	destroy_trigger = {
		exists = owner
		OR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
			has_modifier = penal_colony
			owner = { is_wilderness_empire = yes }
		}
	}

	allow = {
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = exotic_gases
			COST = @b2_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		cost = {
			minor_artifacts = @b2_rare_cost
		}
		upkeep = {
			energy = @b3_upkeep
		}
	}

	planet_modifier = {
		planet_biologists_society_research_produces_add = 0.25
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		planet_biologists_consumer_goods_upkeep_add = 0.5
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_machine_empire = yes
			}
		}
		planet_biologists_energy_upkeep_add = 1
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_hive_empire = yes
			}
		}
		planet_biologists_minerals_upkeep_add = 1
	}

	triggered_planet_modifier = {
		potential = {
			is_planet_class = pc_relic
		}
		planet_biologists_minor_artifacts_produces_add = 0.25
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_ascension_perk = ap_archaeoengineers
			}
		}
		planet_biologists_minor_artifacts_produces_add = 0.15
	}

	triggered_country_modifier = {
		potential = {
			exists = owner
			owner = {
				has_ascension_perk = ap_archaeoengineers
			}
		}
		country_resource_max_minor_artifacts_add = 3000
	}

	triggered_country_modifier = {
		potential = {
			is_planet_class = pc_relic
		}
		category_archaeostudies_research_speed_mult = 0.25
	}

	inline_script = {
		script = jobs/biologists_add
		AMOUNT = @building_static_jobs
	}

	country_modifier = {
		category_archaeostudies_research_speed_mult = 0.25
		country_resource_max_minor_artifacts_add = 2000
	}

	prerequisites = {
		"tech_archaeostudies"
	}

	show_tech_unlock_if = {
		is_wilderness_empire = no
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		text = biologist_is_archaeo_engineer_tt
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_hive_empire = yes
			}
		}
		text = biology_drone_is_archaeo_engineer_tt
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_machine_empire = yes
			}
		}
		text = biology_unit_is_archaeo_engineer_tt
	}

	triggered_desc = {
		text = building_archaeostudies_faculty_relic_effect
	}

	ai_weight_coefficient = 6

	inline_script = {
		script = districts/ai_research_society_extra_weighting
		AMOUNT = 5
	}
	additional_ai_weight = 500
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_research_input_runway_safe = yes } } }
	}
}

```

## mods/StellarAIDirector/common/buildings/zzzz_staid_07_pop_assembly_buildings.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/buildings


# Source-local variables required by copied parent objects.
@b1_minerals = 400
@b1_time = 360
@b1_upkeep = 2
@b2_alloy_upkeep = 3
@b2_minerals = 600
@b2_upkeep = 5
@b3_minerals = 800
@b3_rare_cost = 100
@b3_rare_upkeep = 2
@b3_time = 600
@b3_upkeep = 8
@building_static_jobs = 200
@building_static_jobs_low = 100
@clones_sustained_low = 500
@nomadic_minerals_to_strategic_ratio	= 0.1
@replicatory_association_amenities_add = 500
@replicatory_association_trade_mult = 0.10

# policy_route = pop_assembly_snowball_core; source = common/buildings/01_pop_assembly_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_robot_assembly_plant = {
	base_buildtime = @b1_time
	planet_limit = 1

	category = pop_assembly

	building_sets = {
		government
		urban
	}

	potential = {
		exists = owner
		owner = {
			is_regular_empire = yes
			is_individual_machine = no
			NOT = { has_policy_flag = robots_outlawed }
			OR = {
				is_ai = no
				NOT = { has_ascension_perk = ap_engineered_evolution }
				is_materialist = yes
			}
		}
		NOT = {	has_modifier = resort_colony }
	}

	convert_to = {
		building_machine_assembly_plant
	}

	upgrades = {
		building_robot_assembly_complex
	}

	allow = {
		hidden_trigger = {
			OR = {
				owner = { is_ai = no }
				NAND = {
					free_district_slots = 0
					free_building_slots <= 1
					free_housing <= 0
					free_jobs <= 0
				}
			}
		}
	}

	destroy_trigger = {
		exists = owner
		OR = {
			owner = {
				OR = {
					is_regular_empire = no
					has_policy_flag = robots_outlawed
				}
			}
			AND = {
				owner = { is_ai = yes }
				free_district_slots = 0
				free_building_slots = 0
				free_housing <= 0
				free_jobs <= 0
			}
			owner = {
				is_ai = yes
				has_ascension_perk = ap_engineered_evolution
				is_materialist = no
			}
		}
	}

	inline_script = {
		script = jobs/roboticist_add
		AMOUNT = @building_static_jobs_low
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				OR = {
					has_origin = origin_mechanists
					is_individual_machine = yes
					has_country_flag = synthetic_empire
				}
			}
			any_owned_pop_group = {
				has_auto_modding_trait = yes
			}
		}
		modifier = {
			auto_mod_monthly_add = 200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_unscheduled_updates
			}
		}
		modifier = {
			planet_pop_assembly_mult = 0.1
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_safe_updates
			}
		}
		modifier = {
			planet_pop_assembly_mult = -0.1
			planet_stability_add = 2
		}
	}

	### JOB STRATA FOCUS MODIFIERS ###
	triggered_planet_modifier = { # Synth ruler focus
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_focus_rulers
			}
		}
		modifier = {
			planet_jobs_ruler_produces_mult = 0.15
		}
	}

	triggered_planet_modifier = { # Synth specialist focus
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_focus_specialists
			}
		}
		modifier = {
			planet_jobs_specialist_produces_mult = 0.05
		}
	}

	triggered_planet_modifier = { # Synth worker focus
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_focus_workers
			}
		}
		modifier = {
			planet_jobs_worker_produces_mult = 0.10
		}
	}

	triggered_planet_modifier = { # Synth upkeep focus
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_focus_upkeep
			}
		}
		modifier = {
			planet_jobs_upkeep_mult = -0.05
		}
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = rare_crystals
			COST = @b2_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		upkeep = {
			energy = @b2_upkeep
		}
	}

	prerequisites = {
		"tech_robotic_workers"
	}
	ai_weight_coefficient = 8
	additional_ai_weight = 900
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_pop_assembly_snowball_ready = yes } } }
	}
}


# policy_route = pop_assembly_snowball_core; source = common/buildings/01_pop_assembly_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_robot_assembly_complex = {
	icon = building_machine_assembly_complex
	base_buildtime = @b3_time
	can_build = no

	category = pop_assembly

	building_sets = {
		government
		urban
	}

	potential = {
		exists = owner
		owner = {
			is_regular_empire = yes
			is_individual_machine = no
			NOT = { has_policy_flag = robots_outlawed }
			OR = {
				is_ai = no
				NOT = { has_ascension_perk = ap_engineered_evolution }
				is_materialist = yes
			}
		}
	}

	convert_to = {
		building_machine_assembly_complex
	}

	destroy_trigger = {
		exists = owner
		OR = {
			owner = {
				OR = {
					is_regular_empire = no
					has_policy_flag = robots_outlawed
				}
			}
			AND = {
				owner = { is_ai = yes }
				free_district_slots = 0
				free_building_slots = 0
				free_housing <= 0
				free_jobs <= 0
			}
			owner = {
				is_ai = yes
				has_ascension_perk = ap_engineered_evolution
				is_materialist = no
			}
		}
	}

	inline_script = {
		script = jobs/roboticist_add
		AMOUNT = @building_static_jobs
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				OR = {
					has_origin = origin_mechanists
					is_individual_machine = yes
					has_country_flag = synthetic_empire
				}
			}
			any_owned_pop_group = {
				has_auto_modding_trait = yes
			}
		}
		modifier = {
			auto_mod_monthly_add = 400
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_unscheduled_updates
			}
		}
		modifier = {
			planet_pop_assembly_mult = 0.1
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_safe_updates
			}
		}
		modifier = {
			planet_pop_assembly_mult = -0.1
			planet_stability_add = 2
		}
	}

	### JOB STRATA FOCUS MODIFIERS ###
	triggered_planet_modifier = { # Synth ruler focus
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_focus_rulers
			}
		}
		modifier = {
			planet_jobs_ruler_produces_mult = 0.15
		}
	}

	triggered_planet_modifier = { # Synth specialist focus
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_focus_specialists
			}
		}
		modifier = {
			planet_jobs_specialist_produces_mult = 0.05
		}
	}

	triggered_planet_modifier = { # Synth worker focus
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_focus_workers
			}
		}
		modifier = {
			planet_jobs_worker_produces_mult = 0.10
		}
	}

	triggered_planet_modifier = { # Synth upkeep focus
		potential = {
			exists = owner
			owner = {
				has_country_flag = synth_focus_upkeep
			}
		}
		modifier = {
			planet_jobs_upkeep_mult = -0.05
		}
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = rare_crystals
			COST = @b3_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		cost = {
			rare_crystals = @b3_rare_cost
		}
		upkeep = {
			energy = @b3_upkeep
			rare_crystals = @b3_rare_upkeep
		}
	}

	prerequisites = {
		tech_robot_assembly_complex
	}
	ai_weight_coefficient = 10
	additional_ai_weight = 1200
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_pop_assembly_snowball_ready = yes } } }
	}
}


# policy_route = pop_assembly_snowball_core; source = common/buildings/01_pop_assembly_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_machine_assembly_plant = {
	icon = building_robot_assembly_plant
	base_buildtime = @b1_time
	planet_limit = 1

	category = pop_assembly

	building_sets = {
		government
		urban
	}

	potential = {
		exists = owner
		owner = {
			OR = {
				is_machine_empire = yes
				is_individual_machine = yes
				is_hive_empire_with_machines = yes
			}
		}
		NOT = {
			has_modifier = resort_colony
		}
	}

	convert_to = {
		building_robot_assembly_plant
	}

	allow = {
		hidden_trigger = {
			OR = {
				owner = { is_ai = no }
				NAND = {
					free_district_slots = 0
					free_building_slots <= 1
					free_housing <= 0
					free_jobs <= 0
				}
			}
		}
	}

	destroy_trigger = {
		exists = owner
		OR = {
			owner = {
				is_robot_empire = no
				is_hive_empire_with_machines = no
			}
			AND = {
				owner = { is_ai = yes }
				free_district_slots = 0
				free_building_slots = 0
				free_housing <= 0
				free_jobs <= 0
			}
		}
	}

	inline_script = {
		script = jobs/roboticist_add
		AMOUNT = @building_static_jobs_low
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				OR = {
					is_machine_empire = yes
					is_individual_machine = yes
				}
			}
			any_owned_pop_group = {
				has_auto_modding_trait = yes
			}
		}
		modifier = {
			auto_mod_monthly_add = 200
		}
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = rare_crystals
			COST = @b1_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		upkeep = {
			energy = @b1_upkeep
		}
	}

	upgrades = {
		building_machine_assembly_complex
	}

	prerequisites = {

	}

	ai_weight_coefficient = 8
	additional_ai_weight = 900
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_pop_assembly_snowball_ready = yes } } }
	}
}


# policy_route = pop_assembly_snowball_core; source = common/buildings/01_pop_assembly_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_machine_assembly_complex = {
	base_buildtime = @b3_time
	can_build = no

	category = pop_assembly

	building_sets = {
		government
		urban
	}

	potential = {
		exists = owner
		owner = {
			OR = {
				is_machine_empire = yes
				is_individual_machine = yes
				is_hive_empire_with_machines = yes
			}
		}
		NOT = {
			has_modifier = resort_colony
		}
	}

	convert_to = {
		building_robot_assembly_complex
	}

	destroy_trigger = {
		exists = owner
		OR = {
			owner = {
				is_robot_empire = no
				is_hive_empire_with_machines = no
			}
			AND = {
				owner = { is_ai = yes }
				free_district_slots = 0
				free_building_slots = 0
				free_housing <= 0
				free_jobs <= 0
			}
		}
	}

	inline_script = {
		script = jobs/roboticist_add
		AMOUNT = @building_static_jobs
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				OR = {
					is_machine_empire = yes
					is_individual_machine = yes
				}
			}
			any_owned_pop_group = {
				has_auto_modding_trait = yes
			}
		}
		modifier = {
			auto_mod_monthly_add = 400
		}
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = rare_crystals
			COST = @b3_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		cost = {
			rare_crystals = @b3_rare_cost
		}
		upkeep = {
			energy = @b3_upkeep
			rare_crystals = @b3_rare_upkeep
		}
	}

	prerequisites = {
		tech_mega_assembly
	}
	ai_weight_coefficient = 10
	additional_ai_weight = 1200
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_pop_assembly_snowball_ready = yes } } }
	}
}


# policy_route = pop_assembly_snowball_core; source = common/buildings/01_pop_assembly_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_clone_vats = {
	base_buildtime = @b1_time

	category = pop_assembly

	planet_limit = {
		base = 1
		modifier = {
			exists = owner
			owner = {
				has_tradition = tr_cloning_finish
			}
			has_upgraded_capital = yes
			add = 1
		}
		modifier = {
			exists = owner
			owner = {
				has_tradition = tr_cloning_finish
			}
			has_major_upgraded_capital = yes
			add = 1
		}
		modifier = {
			exists = owner
			owner = {
				has_tradition = tr_cloning_finish
			}
			has_fully_upgraded_capital = yes
			add = 1
		}
	}

	building_sets = {
		government
		urban
	}

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		OR = {
			owner = { is_ai = no }
			NAND = {
				free_district_slots = 0
				free_building_slots <= 1
				free_housing <= 0
				free_jobs <= 0
			}
		}
	}

	destroy_trigger = {
		exists = owner
		OR = {
			AND = {
				owner = { is_ai = yes }
				free_district_slots = 0
				free_building_slots = 0
				free_housing <= 0
				free_jobs <= 0
			}
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_gene_tailoring
			}
			any_owned_pop_group = {
				has_auto_modding_trait = yes
			}
		}
		modifier = {
			auto_mod_monthly_add = 200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				game_start_auto_mod_empire = yes
			}
			any_owned_pop_group = {
				has_auto_modding_trait = yes
			}
		}
		modifier = {
			auto_mod_monthly_add = 200
		}
	}

	triggered_planet_pop_group_modifier_for_all = {
		potential = {
			owner = {
				has_cloning_tradition = no
			}
		}
		bonus_pop_growth = 1.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_cloning_tradition = no
			}
		}
		fake_pop_growth_mod = 1.5
	}

	triggered_planet_pop_group_modifier_for_all = {
		potential = {
			exists = owner
			owner = {
				has_cloning_tradition = yes
				NOT = {
					has_tradition = tr_genetics_efficient_cloning
				}
			}
		}
		bonus_pop_growth = 3
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_cloning_tradition = yes
				NOT = {
					has_tradition = tr_genetics_efficient_cloning
				}
			}
		}
		fake_pop_growth_mod = 3
	}

	triggered_planet_pop_group_modifier_for_all = {
		potential = {
			exists = owner
			owner = {
				has_cloning_tradition = yes
				has_tradition = tr_genetics_efficient_cloning
			}
		}
		bonus_pop_growth = 4.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_cloning_tradition = yes
				has_tradition = tr_genetics_efficient_cloning
			}
		}
		fake_pop_growth_mod = 4.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_country_flag = clone_army_full_potential
				has_active_tradition = tr_cloning_adopt_clone_army
			}
		}
		clone_soldiers_sustained = @clones_sustained_low
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_country_flag = clone_army_full_potential
				has_active_tradition = tr_cloning_finish_clone_army
			}
		}
		clone_soldiers_sustained = @clones_sustained_low
	}

	resources = {
		category = planet_buildings_clone_vats

		# Base cost
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = rare_crystals
			COST = 500
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		# Organic/Lithoid/infernal cost
		inline_script = {
			script = buildings/nomadic_cost_switcher_with_additional_trigger
			TRIGGER = "owner? = { is_lithoid_or_infernal_empire = no }"
			REGULAR_RESOURCE = food
			NOMADIC_RESOURCE = exotic_gases
			COST = 500
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		inline_script = {
			script = buildings/nomadic_cost_switcher_with_additional_trigger
			TRIGGER = "owner? = { is_lithoid_or_infernal_empire = yes }"
			REGULAR_RESOURCE = energy
			NOMADIC_RESOURCE = rare_crystals
			COST = 500
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}

		# Base upkeep
		upkeep = {
			energy = 2
		}
		# Organic/Lithoid/infernal upkeep
		upkeep = {
			trigger = {
				exists = owner
				owner = {
					is_lithoid_or_infernal_empire = no
				}
			}
			food = 15
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = {
					is_lithoid_or_infernal_empire = no
					has_cloning_tradition = yes
				}
			}
			food = 15
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = {
					is_lithoid_empire = yes
				}
			}
			minerals = 15
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = {
					is_lithoid_empire = yes
					has_cloning_tradition = yes
				}
			}
			minerals = 15
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = {
					is_infernal_empire = yes
				}
			}
			alloys = @b2_alloy_upkeep
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = {
					is_infernal_empire = yes
					has_cloning_tradition = yes
				}
			}
			alloys = @b2_alloy_upkeep
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_cloning_authority = yes
				is_megacorp = yes
			}
		}
		planet_jobs_trade_produces_mult = @replicatory_association_trade_mult
		planet_amenities_add = @replicatory_association_amenities_add
	}

	prerequisites = {
		tech_cloning
	}

	ai_weight_coefficient = 10
	additional_ai_weight = 1200
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_pop_assembly_snowball_ready = yes } } }
	}
}


# policy_route = pop_assembly_snowball_core; source = common/buildings/01_pop_assembly_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_spawning_pool = {
	base_buildtime = @b1_time
	planet_limit = 1

	category = pop_assembly

	building_sets = {
		government
		urban
	}

	potential = {
		exists = owner
		owner = {
			is_hive_empire = yes
			is_wilderness_empire = no
			NOT = { has_origin = origin_progenitor_hive }
		}
	}

	destroy_trigger = {
		exists = owner
		owner = {
			OR = {
				is_hive_empire = no
				has_origin = origin_progenitor_hive
			}
		}
	}

	inline_script = {
		script = jobs/spawning_drone_add
		AMOUNT = @building_static_jobs_low
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_gene_tailoring
			}
			any_owned_pop_group = {
				has_auto_modding_trait = yes
			}
		}
		modifier = {
			auto_mod_monthly_add = 200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				game_start_auto_mod_empire = yes
			}
			any_owned_pop_group = {
				has_auto_modding_trait = yes
			}
		}
		modifier = {
			auto_mod_monthly_add = 200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_cybernetics_synaptic_sub_processing }
		}
		modifier = {
			job_augmentor_drone_add = 200
		}
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = rare_crystals
			COST = @b1_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		upkeep = {
			energy = 2
		}
	}

	convert_to = {
		building_offspring_nest
	}

	triggered_desc = {
		text = spawning_pool_tooltip
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 1000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_pop_assembly_snowball_ready = yes } } }
	}
}


# policy_route = pop_assembly_snowball_core; source = common/buildings/01_pop_assembly_buildings.txt; parent_ai = parent_ai_absent; source_ai_weight = no
building_offspring_nest = {
	base_buildtime = @b1_time
	planet_limit = 1

	category = pop_assembly

	building_sets = {
		government
		urban
	}

	potential = {
		owner? = {
			has_origin = origin_progenitor_hive
		}
	}

	allow = {
		NOT = {
			fleet.starbase? = {
				has_starbase_building = arkship_offspring_outlook
			}
		}
	}

	destroy_trigger = {
		OR = {
			owner? = {
				NOT = {
					has_origin = origin_progenitor_hive
				}
			}
			fleet.starbase? = {
				has_starbase_building = arkship_offspring_outlook
			}
		}
	}

	#ruined_trigger = {
	#	has_carrier_flag = offspring_defeated
	#}

	inline_script = {
		script = jobs/spawning_drone_add
		AMOUNT = @building_static_jobs_low
	}

	convert_to = {
		building_spawning_pool
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_cybernetics_synaptic_sub_processing }
		}
		modifier = {
			job_augmentor_drone_add = 200
		}
	}

	resources = {
		category = planet_buildings
		inline_script = {
			script = buildings/nomadic_cost_switcher
			REGULAR_RESOURCE = minerals
			NOMADIC_RESOURCE = rare_crystals
			COST = @b1_minerals
			NOMADIC_COST_MULT = @nomadic_minerals_to_strategic_ratio
		}
		upkeep = {
			energy = 2
		}
	}

	triggered_desc = {
		text = offspring_nest_tooltip
	}
	ai_weight_coefficient = 7
	additional_ai_weight = 800
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_pop_assembly_snowball_ready = yes } } }
	}
}

```

## mods/StellarAIDirector/common/buildings/zzzz_staid_12_planetary_diversity_buildings.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied Planetary Diversity buildings with Director-owned economic ROI weights.
# Availability owns PD prerequisites; weights classify the planet modifier/deposit role and the 2350 horizon payoff.

# Source-local variables required by copied Planetary Diversity building objects.
@b2_rare_cost = 50
@b2_rare_upkeep = 1
@b2_time = 480
@b3_rare_cost = 100
@b3_rare_upkeep = 2
@b4_rare_cost = 200
@b4_upkeep = 10

# Source: common/buildings/pd_buildings_overwrites.txt
# pd_economic_role = energy
building_gaiaseeders_1 = {
	base_buildtime = @b2_time
	planet_limit = 1
	can_be_disabled = no
	upgrades = { "building_gaiaseeders_2" }

	category = government

	building_sets = {
		government
		urban
	}

	potential = {
		exists = owner
		owner = {
			is_country_type = default
			is_idyllic_bloom_empire = yes
		}
		pd_is_planet_class_gaia = no
		pd_aw_is_superproject_class = no
		NOR = {
			is_planet_class = pc_city
			is_planet_class = pc_hive
			is_planet_class = pc_machine
			is_planet_class = pc_relic
		}
		is_artificial = no
		NOT = { planet = { has_planet_flag = pd_unique_world } }
	}

	allow = {
		has_upgraded_capital = yes
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_gaia = yes # No double bonuses if player uses other tools to turn it into a Gaia world.
			is_planet_class = pc_city
			is_planet_class = pc_hive
			is_planet_class = pc_machine
			is_planet_class = pc_relic
			NOT = { exists = owner }
			owner = {
				is_idyllic_bloom_empire = no
			}
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			energy = 1500
			multiplier = value:gaiaseeder_cost_mult
		}

		cost = {
			trigger = {
				exists = owner
				owner = {
					is_wilderness_empire = yes
				}
			}
			biomass = 200
		}

		upkeep = {
			energy = 20
			multiplier = value:gaiaseeder_upkeep
		}
	}

	inline_script = {
		script = buildings/on_all_wilderness_buildings_districts
	}

	planet_modifier = {
		logistic_growth_mult = 0.1
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = energy
building_gaiaseeders_2 = {
	base_buildtime = @b2_time
	can_build = no
	can_be_disabled = no
	upgrades = { "building_gaiaseeders_3" }

	category = government

	building_sets = {
		government
		urban
	}

	resources = {
		category = planet_buildings
		cost = {
			energy = 1500
			exotic_gases = @b2_rare_cost
		}

		cost = {
			trigger = {
				exists = owner
				owner = {
					is_wilderness_empire = yes
				}
			}
			biomass = 400
		}

		upkeep = {
			energy = 20
			exotic_gases = @b2_rare_upkeep
			multiplier = value:gaiaseeder_upkeep
		}
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_gaia = yes
			is_planet_class = pc_city
			is_planet_class = pc_hive
			is_planet_class = pc_machine
			NOT = { exists = owner }
			owner = {
				is_idyllic_bloom_empire = no
			}
		}
	}

	allow = {
		exists = planet
		planet = {
			can_build_gaiaseeder = yes
		}
	}

	inline_script = {
		script = buildings/on_all_wilderness_buildings_districts
	}

	planet_modifier = {
		logistic_growth_mult = 0.05
		pop_environment_tolerance = 0.1
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = energy
building_gaiaseeders_3 = {
	base_buildtime = @b2_time
	can_build = no
	can_be_disabled = no
	upgrades = { "building_gaiaseeders_4" }

	category = government

	building_sets = {
		government
		urban
	}

	resources = {
		category = planet_buildings
		cost = {
			energy = 1500
			exotic_gases = @b3_rare_cost
		}

		cost = {
			trigger = {
				exists = owner
				owner = {
					is_wilderness_empire = yes
				}
			}
			biomass = 600
		}

		upkeep = {
			energy = 20
			exotic_gases = @b3_rare_upkeep
			multiplier = value:gaiaseeder_upkeep
		}
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_gaia = yes
			is_planet_class = pc_city
			is_planet_class = pc_hive
			is_planet_class = pc_machine
			NOT = { exists = owner }
			owner = {
				is_idyllic_bloom_empire = no
			}
		}
	}

	inline_script = {
		script = buildings/on_all_wilderness_buildings_districts
	}

	allow = {
		exists = planet
		planet = {
			can_build_gaiaseeder = yes
		}
	}

	planet_modifier = {
		pop_environment_tolerance = 0.2
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = energy
building_gaiaseeders_4 = {
	base_buildtime = @b2_time
	can_build = no
	can_demolish = no
	can_be_ruined = no
	can_be_disabled = no
	position_priority = 0

	category = government

	building_sets = {
		government
		urban
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_gaia = no
			NOT = { exists = owner }
			owner = {
				is_idyllic_bloom_empire = no
			}
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			energy = 1500
			exotic_gases = @b4_rare_cost
		}

		cost = {
			trigger = {
				exists = owner
				owner = {
					is_wilderness_empire = yes
				}
			}
			biomass = 800
		}

		upkeep = {
			energy = @b4_upkeep
			exotic_gases = @b3_rare_upkeep
			multiplier = value:gaiaseeder_cost_mult
		}
	}

	inline_script = {
		script = buildings/on_all_wilderness_buildings_districts
	}

	triggered_desc = {
		text = building_gaiaseeders_4_effect_desc
		trigger = {
			exists = planet
			planet = {
				NOT = {
					is_planet_class = pc_gaia
				}
			}
		}
	}

	triggered_desc = {
		text = gaia_seeder_bloomed_pops_effect
	}

	triggered_desc = {
		text = gaia_seeder_bloom_timer_tooltip
		trigger = {
			has_carrier_flag = gaia_seeder_bloom_timer
		}
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = energy
building_gaiaseeders_pc_gaia = {
	base_buildtime = @b2_time
	planet_limit = 1
	can_demolish = no
	can_be_ruined = no
	can_be_disabled = no
	position_priority = 0
	icon = building_gaiaseeders_4

	category = government

	building_sets = {
		government
		urban
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_gaia = no
			NOT = { exists = owner }
			owner = {
				is_idyllic_bloom_empire = no
			}
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			energy = 1500
			exotic_gases = @b4_rare_cost
		}

		cost = {
			trigger = {
				exists = owner
				owner = {
					is_wilderness_empire = yes
				}
			}
			biomass = 800
		}

		upkeep = {
			energy = @b4_upkeep
			exotic_gases = @b3_rare_upkeep
			multiplier = value:gaiaseeder_cost_mult
		}
	}

	potential = {
		hidden_trigger = {
			exists = owner
			owner = {
				is_country_type = default
				is_idyllic_bloom_empire = yes
			}
			pd_is_planet_class_gaia = yes
			NOR = {
				has_building = building_gaiaseeders_4
				has_building_construction = building_gaiaseeders_4
				has_building = building_gaiaseeders_pc_gaia
				has_building_construction = building_gaiaseeders_pc_gaia
			}
		}
	}

	allow = {
		has_upgraded_capital = yes
		exists = planet
		planet = {
			can_build_gaiaseeder = yes
		}
	}

	inline_script = {
		script = buildings/on_all_wilderness_buildings_districts
	}

	triggered_desc = {
		text = building_gaiaseeders_4_effect_desc
		trigger = {
			exists = planet
			planet = {
				NOT = {
					is_planet_class = pc_gaia
				}
			}
		}
	}

	triggered_desc = {
		text = gaia_seeder_bloomed_pops_effect
	}

	triggered_desc = {
		text = gaia_seeder_bloom_timer_tooltip
		trigger = {
			has_carrier_flag = gaia_seeder_bloom_timer
		}
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# Source: common/buildings/pd_gaia_buildings.txt
# pd_economic_role = research
building_gaia_lab = {
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		pd_is_planet_class_gaia = yes
		NOT = { has_modifier = resort_colony }
		NOT = { has_building = building_gaia_lab }
		NOT = { has_building_construction = building_gaia_lab }
		NOT = { has_building = building_gaia_unity_admin }
		NOT = { has_building_construction = building_gaia_unity_admin }
		NOT = { has_building = building_gaia_unity_temple }
		NOT = { has_building_construction = building_gaia_unity_temple }
		NOT = { has_building = building_gaia_unity_robot }
		NOT = { has_building_construction = building_gaia_unity_robot }
		NOT = { has_building = building_gaia_unity_servitor }
		NOT = { has_building_construction = building_gaia_unity_servitor }
		NOT = { has_building = building_gaia_unity_hive }
		NOT = { has_building_construction = building_gaia_unity_hive }
		NOT = { has_building = building_gaia_resort }
		NOT = { has_building_construction = building_gaia_resort }
	}

	building_sets = {
		research
		physics
		society
		engineering
	}

	allow = {
		has_upgraded_capital = yes
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 8
		}
	}

	inline_script = "buildings/pd_rare_physics_building"
	inline_script = "buildings/pd_rare_society_building"
	inline_script = "buildings/pd_rare_engineering_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_regular_empire = yes }
		}
		modifier = {
			job_physicist_add = 50
			job_biologist_add = 50
			job_engineer_add = 50
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 50
			job_calculator_biologist_add = 50
			job_calculator_engineer_add = 50
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 50
			job_calculator_biologist_add = 50
			job_calculator_engineer_add = 50
		}
	}

	destroy_trigger = {
		planet = {
			pd_is_planet_class_gaia = no
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = minerals
building_gaia_unity_admin = {
	base_buildtime = 600

	category = unity

	potential = {
		exists = owner
		pd_is_planet_class_gaia = yes
		NOT = { has_modifier = slave_colony }
		NOT = { has_building = building_gaia_lab }
		NOT = { has_building_construction = building_gaia_lab }
		NOT = { has_building = building_gaia_unity_admin }
		NOT = { has_building_construction = building_gaia_unity_admin }
		NOT = { has_building = building_gaia_unity_temple }
		NOT = { has_building_construction = building_gaia_unity_temple }
		NOT = { has_building = building_gaia_unity_robot }
		NOT = { has_building_construction = building_gaia_unity_robot }
		NOT = { has_building = building_gaia_unity_servitor }
		NOT = { has_building_construction = building_gaia_unity_servitor }
		NOT = { has_building = building_gaia_unity_hive }
		NOT = { has_building_construction = building_gaia_unity_hive }
		NOT = { has_building = building_gaia_resort }
		NOT = { has_building_construction = building_gaia_resort }
		owner = {
			is_regular_empire = yes
			is_spiritualist = no
			has_make_spiritualist_perk = no
		}
	}

	building_sets = {
		unity
	}

	allow = {
		has_upgraded_capital = yes
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 8
		}
	}

	planet_modifier = {
		job_politician_add = 100
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_planetary_government }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_colonial_bureaucracy }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_galactic_bureaucracy }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	convert_to = {
		building_gaia_unity_temple
		building_gaia_unity_robot
		building_gaia_unity_servitor
		building_gaia_unity_hive
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_gaia = no
			has_modifier = slave_colony
			AND = {
				exists = owner
				owner = {
					OR = {
						is_regular_empire = no
						is_spiritualist = yes
						has_make_spiritualist_perk = yes
					}
				}
			}
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_gaia_unity_temple = {
	base_buildtime = 600

	category = unity

	potential = {
		exists = owner
		pd_is_planet_class_gaia = yes
		NOT = { has_modifier = slave_colony }
		NOT = { has_building = building_gaia_lab }
		NOT = { has_building_construction = building_gaia_lab }
		NOT = { has_building = building_gaia_unity_admin }
		NOT = { has_building_construction = building_gaia_unity_admin }
		NOT = { has_building = building_gaia_unity_temple }
		NOT = { has_building_construction = building_gaia_unity_temple }
		NOT = { has_building = building_gaia_unity_robot }
		NOT = { has_building_construction = building_gaia_unity_robot }
		NOT = { has_building = building_gaia_unity_servitor }
		NOT = { has_building_construction = building_gaia_unity_servitor }
		NOT = { has_building = building_gaia_unity_hive }
		NOT = { has_building_construction = building_gaia_unity_hive }
		NOT = { has_building = building_gaia_resort }
		NOT = { has_building_construction = building_gaia_resort }
		owner = {
			OR = {
				is_spiritualist = yes
				AND = {
					is_gestalt = no
					has_make_spiritualist_perk = yes
				}
			}
		}
	}

	building_sets = {
		unity
	}

	allow = {
		has_upgraded_capital = yes
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 8
		}
	}

	planet_modifier = {
		job_politician_add = 100
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_cultural_heritage }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_holographic_rituals }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_consecration_fields }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	convert_to = {
		building_gaia_unity_admin
		building_gaia_unity_robot
		building_gaia_unity_servitor
		building_gaia_unity_hive
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_gaia = no
			has_modifier = slave_colony
			AND = {
				exists = owner
				owner = {
					OR = {
						AND = {
							is_spiritualist = no
							has_make_spiritualist_perk = no
						}
						is_gestalt = yes
					}
				}
			}
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_gaia_unity_robot = {
	base_buildtime = 600

	category = unity

	potential = {
		exists = owner
		pd_is_planet_class_gaia = yes
		NOT = { has_modifier = slave_colony }
		NOT = { has_building = building_gaia_lab }
		NOT = { has_building_construction = building_gaia_lab }
		NOT = { has_building = building_gaia_unity_admin }
		NOT = { has_building_construction = building_gaia_unity_admin }
		NOT = { has_building = building_gaia_unity_temple }
		NOT = { has_building_construction = building_gaia_unity_temple }
		NOT = { has_building = building_gaia_unity_robot }
		NOT = { has_building_construction = building_gaia_unity_robot }
		NOT = { has_building = building_gaia_unity_servitor }
		NOT = { has_building_construction = building_gaia_unity_servitor }
		NOT = { has_building = building_gaia_unity_hive }
		NOT = { has_building_construction = building_gaia_unity_hive }
		NOT = { has_building = building_gaia_resort }
		NOT = { has_building_construction = building_gaia_resort }
		owner = {
			is_machine_empire = yes
			NOT = {
				has_valid_civic = civic_machine_servitor
			}
		}
	}

	building_sets = {
		government
		urban
	}

	allow = {
		has_upgraded_capital = yes
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 8
		}
	}

	planet_modifier = {
		job_coordinator_add = 100
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_planetary_government }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_colonial_bureaucracy }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_galactic_bureaucracy }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	convert_to = {
		building_gaia_unity_admin
		building_gaia_unity_temple
		building_gaia_unity_servitor
		building_gaia_unity_hive
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_gaia = no
			has_modifier = slave_colony
			AND = {
				exists = owner
				owner = {
					OR = {
						is_machine_empire = no
						has_valid_civic = civic_machine_servitor
					}
				}
			}
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_gaia_unity_servitor = {
	base_buildtime = 600

	category = unity

	potential = {
		exists = owner
		pd_is_planet_class_gaia = yes
		NOT = { has_modifier = slave_colony }
		NOT = { has_building = building_gaia_lab }
		NOT = { has_building_construction = building_gaia_lab }
		NOT = { has_building = building_gaia_unity_admin }
		NOT = { has_building_construction = building_gaia_unity_admin }
		NOT = { has_building = building_gaia_unity_temple }
		NOT = { has_building_construction = building_gaia_unity_temple }
		NOT = { has_building = building_gaia_unity_robot }
		NOT = { has_building_construction = building_gaia_unity_robot }
		NOT = { has_building = building_gaia_unity_servitor }
		NOT = { has_building_construction = building_gaia_unity_servitor }
		NOT = { has_building = building_gaia_unity_hive }
		NOT = { has_building_construction = building_gaia_unity_hive }
		NOT = { has_building = building_gaia_resort }
		NOT = { has_building_construction = building_gaia_resort }
		owner = { has_valid_civic = civic_machine_servitor }
	}

	building_sets = {
		urban
		unity
	}

	allow = {
		has_upgraded_capital = yes
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 8
		}
	}

	planet_modifier = {
		job_bio_trophy_add = 2500
		planet_bio_trophies_unity_produces_add = 0.25
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_planetary_government }
		}
		planet_bio_trophies_unity_produces_add = 0.25
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_paradise_dome }
		}
		planet_bio_trophies_unity_produces_add = 0.5
	}

	convert_to = {
		building_gaia_unity_admin
		building_gaia_unity_temple
		building_gaia_unity_robot
		building_gaia_unity_hive
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_gaia = no
			has_modifier = slave_colony
			AND = {
				exists = owner
				owner = {
					NOT = { has_valid_civic = civic_machine_servitor }
				}
			}
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_gaia_unity_hive = {
	base_buildtime = 600

	category = unity

	potential = {
		exists = owner
		pd_is_planet_class_gaia = yes
		NOT = { has_modifier = slave_colony }
		NOT = { has_building = building_gaia_lab }
		NOT = { has_building_construction = building_gaia_lab }
		NOT = { has_building = building_gaia_unity_admin }
		NOT = { has_building_construction = building_gaia_unity_admin }
		NOT = { has_building = building_gaia_unity_temple }
		NOT = { has_building_construction = building_gaia_unity_temple }
		NOT = { has_building = building_gaia_unity_robot }
		NOT = { has_building_construction = building_gaia_unity_robot }
		NOT = { has_building = building_gaia_unity_servitor }
		NOT = { has_building_construction = building_gaia_unity_servitor }
		NOT = { has_building = building_gaia_unity_hive }
		NOT = { has_building_construction = building_gaia_unity_hive }
		NOT = { has_building = building_gaia_resort }
		NOT = { has_building_construction = building_gaia_resort }
		owner = { is_hive_empire = yes }
	}

	building_sets = {
		government
		unity
	}

	allow = {
		has_upgraded_capital = yes
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 8
		}
	}

	planet_modifier = {
		job_evaluator_add = 100
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_hive_node }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_hive_cluster }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_hive_confluence }
		}
		planet_bureaucrats_unity_produces_add = 0.5
	}

	convert_to = {
		building_gaia_unity_admin
		building_gaia_unity_temple
		building_gaia_unity_robot
		building_gaia_unity_servitor
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_gaia = no
			has_modifier = slave_colony
			AND = {
				exists = owner
				owner = { is_hive_empire = no }
			}
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = trade
building_gaia_resort = {
	base_buildtime = 600

	category = amenity

	potential = {
		exists = owner
		pd_is_planet_class_gaia = yes
		owner = { is_gestalt = no }
		NOT = { has_building = building_gaia_lab }
		NOT = { has_building_construction = building_gaia_lab }
		NOT = { has_building = building_gaia_unity_admin }
		NOT = { has_building_construction = building_gaia_unity_admin }
		NOT = { has_building = building_gaia_unity_temple }
		NOT = { has_building_construction = building_gaia_unity_temple }
		NOT = { has_building = building_gaia_unity_robot }
		NOT = { has_building_construction = building_gaia_unity_robot }
		NOT = { has_building = building_gaia_unity_servitor }
		NOT = { has_building_construction = building_gaia_unity_servitor }
		NOT = { has_building = building_gaia_unity_hive }
		NOT = { has_building_construction = building_gaia_unity_hive }
		NOT = { has_building = building_gaia_resort }
		NOT = { has_building_construction = building_gaia_resort }
	}

	building_sets = {
		urban
		trade
	}

	inline_script = "buildings/pd_rare_resort_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_frontier_health }
		}
		job_healthcare_add = 100
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_frontier_hospital }
		}
		job_healthcare_add = 100
	}

	destroy_trigger = {
		planet = {
			pd_is_planet_class_gaia = no
		}
	}
	ai_weight_coefficient = 11
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_trade_value = yes }
		modifier = { factor = 8 years_passed < 30 }
		modifier = { factor = 6 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# Source: common/buildings/pd_planetary_infesters_buildings.txt
# pd_economic_role = energy
building_pd_planet_infester_1 = {
	base_buildtime = 900
	base_cap_amount = 1
	category = government
	can_be_disabled = no
	upgrades = {
		"building_pd_planet_infester_2"
	}

	building_sets = {
		urban
		government
	}

	potential = {
		exists = owner
		owner = {
			is_country_type = default
			has_civic = civic_hive_pd_planetary_infesters
		}
		pd_is_planet_class_all = yes
		NOT = { planet = { has_planet_flag = pd_unique_world } }
	}

	allow = {
		exists = owner
		owner = {
			is_country_type = default
			has_civic = civic_hive_pd_planetary_infesters
		}
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_all = no
			NOT = { exists = owner }
			owner = {
				NOT = { has_civic = civic_hive_pd_planetary_infesters }
			}
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			energy = 2000
		}
		upkeep = {
			energy = 20
		}
	}

	planet_modifier = {
		pop_environment_tolerance = 0.2
	}

	on_destroy = {
		pd_aw_back_to_normal_view_effect = yes
	}

	is_essential = yes
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = energy
building_pd_planet_infester_2 = {
	base_buildtime = 900
	can_build = no
	category = government
	can_be_disabled = no
	upgrades = { "building_pd_planet_infester_3" }

	building_sets = {
		urban
		government
	}

	resources = {
		category = planet_buildings
		cost = {
			energy = 2000
			exotic_gases = 10
		}
		upkeep = {
			energy = 20
			exotic_gases = 2
		}
	}

	destroy_trigger = {
		OR = {
			pd_is_planet_class_all = no
			NOT = { exists = owner }
			owner = {
				NOT = { has_civic = civic_hive_pd_planetary_infesters }
			}
		}
	}

	allow = {
		has_upgraded_capital = yes
	}

	planet_modifier = {
		pop_environment_tolerance = 0.4
	}

	on_destroy = {
		pd_aw_back_to_normal_view_effect = yes
	}

	is_essential = yes
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = energy
building_pd_planet_infester_3 = {
	base_buildtime = 1800
	category = government
	can_build = no
	can_demolish = no
	can_be_ruined = no
	can_be_disabled = no
	position_priority = 0

	building_sets = {
		urban
		government
	}

	destroy_trigger = {
		OR = {
			NOR = {
				is_planet_class = pc_hive
				is_planet_class = pc_pd_hive_tidally_locked
				is_planet_class = pc_pd_hive_cave
				is_planet_class = pc_pd_hive_superhabitable
			}
			NOT = { exists = owner }
			owner = {
				NOT = { has_civic = civic_hive_pd_planetary_infesters }
			}
		}
	}

	allow = {
		has_upgraded_capital = yes
		owner = {
			has_technology = tech_climate_restoration
		}
	}

	planet_modifier = {
		pop_bonus_workforce_mult = 0.1
		pop_amenities_usage_mult = -0.2
	}

	resources = {
		category = planet_buildings
		cost = {
			energy = 2000
			exotic_gases = 20
		}
		upkeep = {
			energy = 20
		}
	}

	triggered_desc = {
		text = building_pd_planet_infester_3_effect_desc
		trigger = {
			exists = planet
			planet = {
				NOT = {
					is_planet_class = pc_hive
				}
			}
		}
	}

	on_destroy = {
		change_pc = pc_arid
	}

	is_essential = yes
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# Source: common/buildings/pd_rare_buildings.txt
# pd_economic_role = minerals
building_megalfora_mine = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = resource

	building_sets = {
		mining
	}

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_megaflora
		NOT = { has_building = building_megalfora_lab }
		NOT = { has_building_construction = building_megalfora_lab }
		NOT = { has_building = building_megalfora_grid }
		NOT = { has_building_construction = building_megalfora_grid }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_mining_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_mining_building"

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_mining_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_megaflora }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_megalfora_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_megaflora
		NOT = { has_building = building_megalfora_mine }
		NOT = { has_building_construction = building_megalfora_mine }
		NOT = { has_building = building_megalfora_grid }
		NOT = { has_building_construction = building_megalfora_grid }
	}

	building_sets = {
		research
		society
		engineering
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_engineering_building"
	inline_script = "buildings/pd_rare_society_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_biologist_add = 75
			job_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_megaflora }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = minerals
building_megalfora_grid = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = resource

	building_sets = {
		generator
	}

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_megaflora
		NOT = { has_building = building_megalfora_mine }
		NOT = { has_building_construction = building_megalfora_mine }
		NOT = { has_building = building_megalfora_lab }
		NOT = { has_building_construction = building_megalfora_lab }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_generator_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_energy_building"

	destroy_trigger = {
		OR = {
			OR = {
				has_modifier = resort_colony
			}
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_generator_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_megaflora }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_petrified_mine = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		mining
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_petrified
		NOT = { has_building = building_petrified_guild }
		NOT = { has_building_construction = building_petrified_guild }
		NOT = { has_building = building_petrified_lab }
		NOT = { has_building_construction = building_petrified_lab }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_mining_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_mining_building"

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_mining_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_petrified }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_petrified_guild = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		industrial
		factory
	}

	category = manufacturing

	potential = {
		owner = { is_gestalt = no }
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_petrified
		NOT = { has_building = building_petrified_mine }
		NOT = { has_building_construction = building_petrified_mine }
		NOT = { has_building = building_petrified_lab }
		NOT = { has_building_construction = building_petrified_lab }
	}

	inline_script = "buildings/pd_rare_consumer_goods_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_petrified }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_petrified_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_petrified
		NOT = { has_building = building_petrified_mine }
		NOT = { has_building_construction = building_petrified_mine }
		NOT = { has_building = building_petrified_guild }
		NOT = { has_building_construction = building_petrified_guild }
	}

	building_sets = {
		research
		society
		engineering
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_engineering_building"
	inline_script = "buildings/pd_rare_society_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_biologist_add = 75
			job_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_petrified }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = research
building_reef_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_reef
		NOT = { has_building = building_reef_guild }
		NOT = { has_building_construction = building_reef_guild }
		NOT = { has_building = building_reef_mine }
		NOT = { has_building_construction = building_reef_mine }
	}

	building_sets = {
		research
		society
		engineering
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_engineering_building"
	inline_script = "buildings/pd_rare_society_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_biologist_add = 75
			job_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = { NOT = { has_modifier = pd_reef } }
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = minerals
building_reef_guild = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600
	category = manufacturing

	building_sets = {
		industrial
		factory
	}

	potential = {
		exists = owner
		owner = {
			OR = {
				country_uses_consumer_goods = yes
				has_origin = origin_fear_of_the_dark
			}
		}
		NOR = {
			has_modifier = resort_colony
			has_modifier = slave_colony
		}
		has_modifier = pd_reef
		NOT = { has_building = building_reef_lab }
		NOT = { has_building_construction = building_reef_lab }
		NOT = { has_building = building_reef_mine }
		NOT = { has_building_construction = building_reef_mine }
	}

	inline_script = "buildings/pd_rare_consumer_goods_building"

	destroy_trigger = {
		planet = { NOT = { has_modifier = pd_reef } }
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_reef_mine = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		mining
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_reef
		NOT = { has_building = building_reef_lab }
		NOT = { has_building_construction = building_reef_lab }
		NOT = { has_building = building_reef_guild }
		NOT = { has_building_construction = building_reef_guild }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_mining_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_mining_building"

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_mining_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_reef }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = alloys
building_archipelago_foundry = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = manufacturing

	building_sets = {
		industrial
		foundry
	}

	potential = {
		NOT = { has_modifier = resort_colony }
		owner = { NOT = { is_catalytic_empire = yes } }
		has_modifier = pd_archipelago
		NOT = { has_building = building_archipelago_farm }
		NOT = { has_building_construction = building_archipelago_farm }
		NOT = { has_building = building_archipelago_resort }
		NOT = { has_building_construction = building_archipelago_resort }
	}

	inline_script = "buildings/pd_rare_foundry_building"

	destroy_trigger = {
		planet = { NOT = { has_modifier = pd_archipelago } }
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = alloys
building_archipelago_farm = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		farming
	}

	category = resource

	potential = {
		exists = owner
		owner = {
			country_uses_food = yes
		}
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_archipelago
		NOT = { has_building = building_archipelago_foundry }
		NOT = { has_building_construction = building_archipelago_foundry }
		NOT = { has_building = building_archipelago_resort }
		NOT = { has_building_construction = building_archipelago_resort }

	}

	inline_script = "buildings/pd_rare_farm_building"

	inline_script = {
		script = jobs/farmers_add
		FARMER_AMOUNT = 2
		ANGLER_AMOUNT = 2
	}

	destroy_trigger = {
		OR = {
			owner = {
				is_ai = yes
				country_uses_food = no
			}
			has_modifier = resort_colony

			planet = { NOT = { has_modifier = pd_archipelago } }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = alloys
building_archipelago_resort = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		urban
		trade
	}

	category = trade

	potential = {
		owner = { is_gestalt = no }
		has_modifier = pd_archipelago
		NOT = { has_building = building_archipelago_foundry }
		NOT = { has_building_construction = building_archipelago_foundry }
		NOT = { has_building = building_archipelago_farm }
		NOT = { has_building_construction = building_archipelago_farm }
	}

	inline_script = "buildings/pd_rare_resort_building"

	destroy_trigger = {
		planet = { NOT = { has_modifier = pd_archipelago  } }
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = research
building_biolumen_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_biolumen
		NOT = { has_building = building_biolumen_resort }
		NOT = { has_building_construction = building_biolumen_resort }
		NOT = { has_building = building_biolumen_farm }
		NOT = { has_building_construction = building_biolumen_farm }
	}

	allow = {
		has_upgraded_capital = yes
	}

	building_sets = {
		research
		society
	}

	inline_script = "buildings/pd_rare_society_building"
	inline_script = "buildings/pd_rare_society_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_biologist_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 150
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_biolumen }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = trade
building_biolumen_resort = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		urban
		trade
	}

	category = trade

	potential = {
		owner = { is_gestalt = no }
		has_modifier = pd_biolumen
		NOT = { has_building = building_biolumen_lab }
		NOT = { has_building_construction = building_biolumen_lab }
		NOT = { has_building = building_biolumen_farm }
		NOT = { has_building_construction = building_biolumen_farm }
	}

	inline_script = "buildings/pd_rare_resort_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_biolumen }
		}
	}
	ai_weight_coefficient = 11
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_trade_value = yes }
		modifier = { factor = 8 years_passed < 30 }
		modifier = { factor = 6 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = food
building_biolumen_farm = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		farming
	}

	category = resource

	potential = {
		exists = owner
		owner = {
			country_uses_food = yes
		}
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_biolumen
		NOT = { has_building = building_biolumen_lab }
		NOT = { has_building_construction = building_biolumen_lab }
		NOT = { has_building = building_biolumen_resort }
		NOT = { has_building_construction = building_biolumen_resort }

	}

	inline_script = "buildings/pd_rare_farm_building"

	inline_script = {
		script = jobs/farmers_add
		FARMER_AMOUNT = 2
		ANGLER_AMOUNT = 2
	}

	destroy_trigger = {
		OR = {
			owner = {
				is_ai = yes
				country_uses_food = no
			}
			has_modifier = resort_colony

			planet = { NOT = { has_modifier = pd_biolumen } }
		}
	}
	ai_weight_coefficient = 7
	additional_ai_weight = 2783
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_food_value = yes }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 4 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = alloys
building_geothermal_grid = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = resource

	building_sets = {
		generator
	}

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_geothermal
		NOT = { has_building = building_geothermal_foundry }
		NOT = { has_building_construction = building_geothermal_foundry }
		NOT = { has_building = building_geothermal_lab }
		NOT = { has_building_construction = building_geothermal_lab }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_generator_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_energy_building"

	destroy_trigger = {
		OR = {
			OR = {
				has_modifier = resort_colony
			}
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_generator_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_geothermal }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = alloys
building_geothermal_foundry = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		industrial
		foundry
	}

	category = manufacturing

	potential = {
		NOT = { has_modifier = resort_colony }
		owner = { NOT = { is_catalytic_empire = yes } }
		has_modifier = pd_geothermal
		NOT = { has_building = building_geothermal_grid }
		NOT = { has_building_construction = building_geothermal_grid }
		NOT = { has_building = building_geothermal_lab }
		NOT = { has_building_construction = building_geothermal_lab }
	}

	inline_script = "buildings/pd_rare_foundry_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_geothermal }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = research
building_geothermal_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		research
		engineering
	}

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_geothermal
		NOT = { has_building = building_geothermal_grid }
		NOT = { has_building_construction = building_geothermal_grid }
		NOT = { has_building = building_geothermal_foundry }
		NOT = { has_building_construction = building_geothermal_foundry }
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_engineering_building"
	inline_script = "buildings/pd_rare_engineering_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_engineer_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_engineer_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_engineer_add = 150
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_geothermal }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = research
building_salt_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		research
		engineering
	}

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_salt
		NOT = { has_building = building_salt_mine }
		NOT = { has_building_construction = building_salt_mine }
		NOT = { has_building = building_salt_foundry }
		NOT = { has_building_construction = building_salt_foundry }
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_engineering_building"
	inline_script = "buildings/pd_rare_engineering_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_engineer_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_engineer_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_engineer_add = 150
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = { NOT = { has_modifier = pd_salt } }
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = alloys
building_salt_foundry = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		industrial
		foundry
	}

	category = manufacturing

	potential = {
		NOT = { has_modifier = resort_colony }
		owner = { NOT = { is_catalytic_empire = yes } }
		has_modifier = pd_salt
		NOT = { has_building = building_salt_mine }
		NOT = { has_building_construction = building_salt_mine }
		NOT = { has_building = building_salt_lab }
		NOT = { has_building_construction = building_salt_lab }
	}

	inline_script = "buildings/pd_rare_foundry_building"

	destroy_trigger = {
		planet = { NOT = { has_modifier = pd_salt } }
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = alloys
building_salt_mine = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		mining
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_salt
		NOT = { has_building = building_salt_lab }
		NOT = { has_building_construction = building_salt_lab }
		NOT = { has_building = building_salt_foundry }
		NOT = { has_building_construction = building_salt_foundry }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_mining_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_mining_building"

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_mining_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_salt }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = food
building_aquifer_farm = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		farming
	}

	category = resource

	potential = {
		exists = owner
		owner = {
			country_uses_food = yes
		}
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_aquifer
		NOT = { has_building = building_aquifer_lab }
		NOT = { has_building_construction = building_aquifer_lab }
		NOT = { has_building = building_aquifer_resort }
		NOT = { has_building_construction = building_aquifer_resort }

	}

	inline_script = "buildings/pd_rare_farm_building"

	inline_script = {
		script = jobs/farmers_add
		FARMER_AMOUNT = 2
		ANGLER_AMOUNT = 2
	}

	destroy_trigger = {
		OR = {
			owner = {
				is_ai = yes
				country_uses_food = no
			}
			has_modifier = resort_colony

			planet = { NOT = { has_modifier = pd_aquifer } }
		}
	}
	ai_weight_coefficient = 7
	additional_ai_weight = 2783
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_food_value = yes }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 4 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_aquifer_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		research
		society
	}

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_aquifer
		NOT = { has_building = building_aquifer_farm }
		NOT = { has_building_construction = building_aquifer_farm }
		NOT = { has_building = building_aquifer_resort }
		NOT = { has_building_construction = building_aquifer_resort }
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_society_building"
	inline_script = "buildings/pd_rare_society_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_biologist_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 150
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = { NOT = { has_modifier = pd_aquifer } }
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = trade
building_aquifer_resort = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		urban
		trade
	}

	category = trade

	potential = {
		owner = { is_gestalt = no }
		has_modifier = pd_aquifer
		NOT = { has_building = building_aquifer_farm }
		NOT = { has_building_construction = building_aquifer_farm }
		NOT = { has_building = building_aquifer_lab }
		NOT = { has_building_construction = building_aquifer_lab }
	}

	inline_script = "buildings/pd_rare_resort_building"

	destroy_trigger = {
		planet = { NOT = { has_modifier = pd_aquifer } }
	}
	ai_weight_coefficient = 11
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_trade_value = yes }
		modifier = { factor = 8 years_passed < 30 }
		modifier = { factor = 6 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = alloys
building_primal_foundry = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		industrial
		foundry
	}

	category = manufacturing

	potential = {
		NOT = { has_modifier = resort_colony }
		owner = { NOT = { is_catalytic_empire = yes } }
		has_modifier = pd_primal
		NOT = { has_building = building_primal_grid }
		NOT = { has_building_construction = building_primal_grid }
		NOT = { has_building = building_primal_mine }
		NOT = { has_building_construction = building_primal_mine }
	}

	inline_script = "buildings/pd_rare_foundry_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_primal }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = alloys
building_primal_grid = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		generator
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_primal
		NOT = { has_building = building_primal_foundry }
		NOT = { has_building_construction = building_primal_foundry }
		NOT = { has_building = building_primal_mine }
		NOT = { has_building_construction = building_primal_mine }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_generator_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_energy_building"

	destroy_trigger = {
		OR = {
			OR = {
				has_modifier = resort_colony
			}
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_generator_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_primal }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = alloys
building_primal_mine = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		mining
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_primal
		NOT = { has_building = building_primal_foundry }
		NOT = { has_building_construction = building_primal_foundry }
		NOT = { has_building = building_primal_grid }
		NOT = { has_building_construction = building_primal_grid }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_mining_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_mining_building"

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_mining_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_primal }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = trade
building_coral_resort = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		urban
		trade
	}

	category = trade

	potential = {
		owner = { is_gestalt = no }
		has_modifier = pd_coral
		NOT = { has_building = building_coral_lab }
		NOT = { has_building_construction = building_coral_lab }
		NOT = { has_building = building_coral_guild }
		NOT = { has_building_construction = building_coral_guild }
	}

	inline_script = "buildings/pd_rare_resort_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_coral }
		}
	}
	ai_weight_coefficient = 11
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_trade_value = yes }
		modifier = { factor = 8 years_passed < 30 }
		modifier = { factor = 6 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_coral_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_coral
		NOT = { has_building = building_coral_resort }
		NOT = { has_building_construction = building_coral_resort }
		NOT = { has_building = building_coral_guild }
		NOT = { has_building_construction = building_coral_guild }
	}

	building_sets = {
		research
		society
		engineering
	}

	inline_script = "buildings/pd_rare_society_building"
	inline_script = "buildings/pd_rare_engineering_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_biologist_add = 75
			job_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_coral }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = consumer_goods
building_coral_guild = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		industrial
		factory
	}

	category = manufacturing

	potential = {
		exists = owner
		owner = { is_gestalt = no }
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_coral
		NOT = { has_building = building_coral_resort }
		NOT = { has_building_construction = building_coral_resort }
		NOT = { has_building = building_coral_lab }
		NOT = { has_building_construction = building_coral_lab }
	}

	inline_script = "buildings/pd_rare_consumer_goods_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_coral }
		}
	}
	ai_weight_coefficient = 14
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_consumer_goods_value = yes }
		modifier = { factor = 10 years_passed < 30 }
		modifier = { factor = 8 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 5 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 2 AND = { years_passed > 99 years_passed < 150 } }
	}
}

# pd_economic_role = energy
building_supercon_farm = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		farming
	}

	category = resource

	potential = {
		exists = owner
		owner = {
			country_uses_food = yes
		}
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_supercontinent
		NOT = { has_building = building_supercon_lab }
		NOT = { has_building_construction = building_supercon_lab }
		NOT = { has_building = building_supercon_grid }
		NOT = { has_building_construction = building_supercon_grid }

	}

	inline_script = "buildings/pd_rare_farm_building"

	inline_script = {
		script = jobs/farmers_add
		FARMER_AMOUNT = 2
		ANGLER_AMOUNT = 2
	}

	destroy_trigger = {
		OR = {
			owner = {
				is_ai = yes
				country_uses_food = no
			}
			has_modifier = resort_colony

			planet = { NOT = { has_modifier = pd_supercontinent } }
		}
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_supercon_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_supercontinent
		NOT = { has_building = building_supercon_farm }
		NOT = { has_building_construction = building_supercon_farm }
		NOT = { has_building = building_supercon_grid }
		NOT = { has_building_construction = building_supercon_grid }
	}

	building_sets = {
		research
		physics
		society
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_physics_building"
	inline_script = "buildings/pd_rare_society_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_physicist_add = 75
			job_biologist_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 75
			job_calculator_biologist_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 75
			job_calculator_biologist_add = 75
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_supercontinent }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = energy
building_supercon_grid = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		generator
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_supercontinent
		NOT = { has_building = building_supercon_farm }
		NOT = { has_building_construction = building_supercon_farm }
		NOT = { has_building = building_supercon_lab }
		NOT = { has_building_construction = building_supercon_lab }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_generator_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_energy_building"

	destroy_trigger = {
		OR = {
			OR = {
				has_modifier = resort_colony
			}
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_generator_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_supercontinent }
		}
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_pd_sinkhole_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_sinkhole
		NOT = { has_building = building_pd_sinkhole_mine }
		NOT = { has_building_construction = building_pd_sinkhole_mine }
		NOT = { has_building = building_pd_sinkhole_guild }
		NOT = { has_building_construction = building_pd_sinkhole_guild }
	}

	allow = {
		has_upgraded_capital = yes
	}

	building_sets = {
		research
		society
		engineering
	}

	inline_script = "buildings/pd_rare_society_building"
	inline_script = "buildings/pd_rare_engineering_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_biologist_add = 75
			job_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_sinkhole }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = minerals
building_pd_sinkhole_mine = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		mining
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_sinkhole
		NOT = { has_building = building_pd_sinkhole_lab }
		NOT = { has_building_construction = building_pd_sinkhole_lab }
		NOT = { has_building = building_pd_sinkhole_guild }
		NOT = { has_building_construction = building_pd_sinkhole_guild }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_mining_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_mining_building"

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_mining_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_sinkhole }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_pd_sinkhole_guild = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		industrial
		factory
	}

	category = manufacturing

	potential = {
		exists = owner
		owner = { is_gestalt = no }
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_sinkhole
		NOT = { has_building = building_pd_sinkhole_lab }
		NOT = { has_building_construction = building_pd_sinkhole_lab }
		NOT = { has_building = building_pd_sinkhole_mine }
		NOT = { has_building_construction = building_pd_sinkhole_mine }
	}

	inline_script = "buildings/pd_rare_consumer_goods_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_sinkhole }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_storm_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_storm
		NOT = { has_building = building_storm_grid }
		NOT = { has_building_construction = building_storm_grid }
		NOT = { has_building = building_storm_mine }
		NOT = { has_building_construction = building_storm_mine }
	}

	allow = {
		has_upgraded_capital = yes
	}

	building_sets = {
		research
		physics
		engineering
	}

	inline_script = "buildings/pd_rare_physics_building"
	inline_script = "buildings/pd_rare_engineering_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_physicist_add = 75
			job_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_storm }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = minerals
building_storm_grid = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		generator
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_storm
		NOT = { has_building = building_storm_lab }
		NOT = { has_building_construction = building_storm_lab }
		NOT = { has_building = building_storm_mine }
		NOT = { has_building_construction = building_storm_mine }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_generator_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_energy_building"

	destroy_trigger = {
		OR = {
			OR = {
				has_modifier = resort_colony
			}
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_generator_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_storm }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_storm_mine = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		mining
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_storm
		NOT = { has_building = building_storm_lab }
		NOT = { has_building_construction = building_storm_lab }
		NOT = { has_building = building_storm_grid }
		NOT = { has_building_construction = building_storm_grid }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_mining_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_mining_building"

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_mining_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_storm }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_iceberg_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_iceberg
		NOT = { has_building = building_iceberg_farm }
		NOT = { has_building_construction = building_iceberg_farm }
		NOT = { has_building = building_iceberg_foundry }
		NOT = { has_building_construction = building_iceberg_foundry }
	}

	building_sets = {
		research
		society
		engineering
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_society_building"
	inline_script = "buildings/pd_rare_engineering_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_regular_empire = yes }
		}
		modifier = {
			job_biologist_add = 75
			job_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_iceberg }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = alloys
building_iceberg_farm = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		farming
	}

	category = resource

	potential = {
		exists = owner
		owner = {
			country_uses_food = yes
		}
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_iceberg
		NOT = { has_building = building_iceberg_lab }
		NOT = { has_building_construction = building_iceberg_lab }
		NOT = { has_building = building_iceberg_foundry }
		NOT = { has_building_construction = building_iceberg_foundry }

	}

	inline_script = "buildings/pd_rare_farm_building"

	inline_script = {
		script = jobs/farmers_add
		FARMER_AMOUNT = 2
		ANGLER_AMOUNT = 2
	}

	destroy_trigger = {
		OR = {
			owner = {
				is_ai = yes
				country_uses_food = no
			}
			has_modifier = resort_colony

			planet = { NOT = { has_modifier = pd_iceberg } }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = alloys
building_iceberg_foundry = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		industrial
		foundry
	}

	category = manufacturing

	potential = {
		NOT = { has_modifier = resort_colony }
		owner = { NOT = { is_catalytic_empire = yes } }
		has_modifier = pd_iceberg
		NOT = { has_building = building_iceberg_lab }
		NOT = { has_building_construction = building_iceberg_lab }
		NOT = { has_building = building_iceberg_farm }
		NOT = { has_building_construction = building_iceberg_farm }
	}

	inline_script = "buildings/pd_rare_foundry_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_iceberg }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = research
building_cryo_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_cryoflora
		NOT = { has_building = building_cryo_lab }
		NOT = { has_building = building_cryo_guild }
		NOT = { has_building = building_cryo_resort }
		NOT = { has_building_construction = building_cryo_lab }
		NOT = { has_building_construction = building_cryo_guild }
		NOT = { has_building_construction = building_cryo_resort }
	}

	allow = {
		has_upgraded_capital = yes
	}

	building_sets = {
		research
		physics
		society
	}

	inline_script = "buildings/pd_rare_physics_building"
	inline_script = "buildings/pd_rare_society_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_regular_empire = yes }
		}
		modifier = {
			job_physicist_add = 75
			job_biologist_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 75
			job_calculator_biologist_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 75
			job_calculator_biologist_add = 75
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_cryoflora }
		}
	}

	ai_resource_production = {
		trigger = {
			planet_resource_compare = {
				resource = physics_research
				value >= 30
			}
		}
		physics_research = 5
		society_research = 5
		engineering_research = 5
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = consumer_goods
building_cryo_guild = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		industrial
		factory
	}

	category = manufacturing

	potential = {
		owner = { is_gestalt = no }
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_cryoflora
		NOT = { has_building = building_cryo_lab }
		NOT = { has_building = building_cryo_guild }
		NOT = { has_building = building_cryo_resort }
		NOT = { has_building_construction = building_cryo_lab }
		NOT = { has_building_construction = building_cryo_guild }
		NOT = { has_building_construction = building_cryo_resort }
	}

	inline_script = "buildings/pd_rare_consumer_goods_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_cryoflora }
		}
	}
	ai_weight_coefficient = 14
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_consumer_goods_value = yes }
		modifier = { factor = 10 years_passed < 30 }
		modifier = { factor = 8 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 5 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 2 AND = { years_passed > 99 years_passed < 150 } }
	}
}

# pd_economic_role = trade
building_cryo_resort = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		urban
		trade
	}

	category = trade

	potential = {
		owner = { is_gestalt = no }
		#NOT = { has_modifier = resort_colony }
		has_modifier = pd_cryoflora
		NOT = { has_building = building_cryo_lab }
		NOT = { has_building = building_cryo_guild }
		NOT = { has_building = building_cryo_resort }
		NOT = { has_building_construction = building_cryo_lab }
		NOT = { has_building_construction = building_cryo_guild }
		NOT = { has_building_construction = building_cryo_resort }
	}

	inline_script = "buildings/pd_rare_resort_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_cryoflora }
		}
	}
	ai_weight_coefficient = 11
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_trade_value = yes }
		modifier = { factor = 8 years_passed < 30 }
		modifier = { factor = 6 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = energy
building_lichen_farm = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		farming
	}

	category = resource

	potential = {
		exists = owner
		owner = {
			country_uses_food = yes
		}
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_lichen
		NOT = { has_building = building_lichen_grid }
		NOT = { has_building_construction = building_lichen_grid }
		NOT = { has_building = building_lichen_lab }
		NOT = { has_building_construction = building_lichen_lab }

	}

	inline_script = "buildings/pd_rare_farm_building"

	inline_script = {
		script = jobs/farmers_add
		FARMER_AMOUNT = 2
		ANGLER_AMOUNT = 2
	}

	destroy_trigger = {
		OR = {
			owner = {
				is_ai = yes
				country_uses_food = no
			}
			has_modifier = resort_colony

			planet = { NOT = { has_modifier = pd_lichen } }
		}
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = energy
building_lichen_grid = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		generator
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_lichen
		NOT = { has_building = building_lichen_farm }
		NOT = { has_building_construction = building_lichen_farm }
		NOT = { has_building = building_lichen_lab }
		NOT = { has_building_construction = building_lichen_lab }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_generator_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_energy_building"

	destroy_trigger = {
		OR = {
			OR = {
				has_modifier = resort_colony
			}
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_generator_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_lichen }
		}
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_lichen_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_lichen
		NOT = { has_building = building_lichen_farm }
		NOT = { has_building_construction = building_lichen_farm }
		NOT = { has_building = building_lichen_grid }
		NOT = { has_building_construction = building_lichen_grid }
	}

	building_sets = {
		research
		society
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_society_building"
	inline_script = "buildings/pd_rare_society_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_regular_empire = yes }
		}
		modifier = {
			job_biologist_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 150
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_lichen }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = alloys
building_glacio_foundry = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		industrial
		foundry
	}

	category = manufacturing

	potential = {
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_glaciovolcanic
		owner = { NOT = { is_catalytic_empire = yes } }
		NOT = { has_building = building_glacio_resort }
		NOT = { has_building_construction = building_glacio_resort }
		NOT = { has_building = building_glacio_mine }
		NOT = { has_building_construction = building_glacio_mine }
	}
	inline_script = "buildings/pd_rare_foundry_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_glaciovolcanic }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = alloys
building_glacio_resort = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		urban
		trade
	}

	category = trade

	potential = {
		owner = { is_gestalt = no }
		has_modifier = pd_glaciovolcanic
		NOT = { has_building = building_glacio_foundry }
		NOT = { has_building_construction = building_glacio_foundry }
		NOT = { has_building = building_glacio_mine }
		NOT = { has_building_construction = building_glacio_mine }
	}

	inline_script = "buildings/pd_rare_resort_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_glaciovolcanic }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = alloys
building_glacio_mine = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		mining
	}

	category = resource

	potential = {
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_glaciovolcanic
		NOT = { has_building = building_glacio_foundry }
		NOT = { has_building_construction = building_glacio_foundry }
		NOT = { has_building = building_glacio_resort }
		NOT = { has_building_construction = building_glacio_resort }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_mining_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_mining_building"

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_mining_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_glaciovolcanic }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = minerals
building_lanthanide_mine = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		mining
	}

	category = resource

	potential = {
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_lanthanide
		NOT = { has_building = building_lanthanide_guild }
		NOT = { has_building_construction = building_lanthanide_guild }
		NOT = { has_building = building_lanthanide_lab }
		NOT = { has_building_construction = building_lanthanide_lab }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_mining_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_mining_building"

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_mining_district_or_building = no
			}
		}
		planet = {
			NOT = { has_modifier = pd_lanthanide }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_lanthanide_guild = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	building_sets = {
		industrial
		factory
	}

	category = manufacturing

	potential = {
		owner = { is_gestalt = no }
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_lanthanide
		NOT = { has_building = building_lanthanide_mine }
		NOT = { has_building_construction = building_lanthanide_mine }
		NOT = { has_building = building_lanthanide_lab }
		NOT = { has_building_construction = building_lanthanide_lab }
	}

	inline_script = "buildings/pd_rare_consumer_goods_building"

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_lanthanide }
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_lanthanide_lab = {
	can_build = yes
	base_cap_amount = 1
	base_buildtime = 600

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		has_modifier = pd_lanthanide
		NOT = { has_building = building_lanthanide_mine }
		NOT = { has_building_construction = building_lanthanide_mine }
		NOT = { has_building = building_lanthanide_guild }
		NOT = { has_building_construction = building_lanthanide_guild }
	}

	building_sets = {
		research
		physics
		engineering
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_engineering_building"
	inline_script = "buildings/pd_rare_physics_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_regular_empire = yes }
		}
		modifier = {
			job_physicist_add = 75
			job_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 75
			job_calculator_engineer_add = 75
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 4
		}
	}

	destroy_trigger = {
		planet = {
			NOT = { has_modifier = pd_lanthanide }
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# Source: common/buildings/pd_uncommon_buildings.txt
# pd_economic_role = energy
building_wet_td_farm = {
	base_buildtime = 600
	can_build = yes
	base_cap_amount = 1

	building_sets = {
		farming
	}

	category = resource

	potential = {
		exists = owner
		owner = {
			country_uses_food = yes
		}
		NOT = { has_modifier = resort_colony }
		pd_is_planet_class_tidally_locked = yes
		NOT = { has_building = building_wet_td_grid }
		NOT = { has_building_construction = building_wet_td_grid }
		NOT = { has_building = building_wet_td_bio_lab }
		NOT = { has_building_construction = building_wet_td_bio_lab }
	}

	inline_script = "buildings/pd_rare_farm_building"

	destroy_trigger = {
		OR = {
			owner = {
				is_ai = yes
				country_uses_food = no
			}
			has_modifier = resort_colony
			planet = {
				NOT = {
					pd_is_planet_class_tidally_locked = yes
				}
			}
		}
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = energy
building_wet_td_grid = {
	base_buildtime = 600
	can_build = yes
	base_cap_amount = 1

	building_sets = {
		generator
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		pd_is_planet_class_tidally_locked = yes
		NOT = { has_building = building_wet_td_farm }
		NOT = { has_building_construction = building_wet_td_farm }
		NOT = { has_building = building_wet_td_bio_lab }
		NOT = { has_building_construction = building_wet_td_bio_lab }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_generator_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_energy_building"

	destroy_trigger = {
		OR = {
			OR = {
				has_modifier = resort_colony
			}
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_generator_district_or_building = no
			}
		}
		planet = {
			NOT = {
				pd_is_planet_class_tidally_locked = yes
			}
		}
	}
	ai_weight_coefficient = 6
	additional_ai_weight = 2474
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_energy_value = yes }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_wet_td_bio_lab = {
	base_buildtime = 600
	can_build = yes
	base_cap_amount = 1

	building_sets = {
		research
		physics
		society
	}

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		pd_is_planet_class_tidally_locked = yes
		NOT = { has_building = building_wet_td_farm }
		NOT = { has_building_construction = building_wet_td_farm }
		NOT = { has_building = building_wet_td_grid }
		NOT = { has_building_construction = building_wet_td_grid }
	}

	allow = {
		has_upgraded_capital = yes
	}
	inline_script = "buildings/pd_rare_society_building"
	inline_script = "buildings/pd_rare_physics_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_regular_empire = yes }
		}
		modifier = {
			job_physicist_add = 150
			job_biologist_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 150
			job_calculator_biologist_add = 150
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 150
			job_calculator_biologist_add = 150
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 8
		}
	}

	destroy_trigger = {
		planet = {
			NOT = {
				pd_is_planet_class_tidally_locked = yes
			}
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = minerals
building_karst_grid = {
	base_buildtime = 600
	can_build = yes
	base_cap_amount = 1

	building_sets = {
		generator
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		pd_is_planet_class_cave = yes
		NOT = { has_building = building_karst_mine }
		NOT = { has_building_construction = building_karst_mine }
		NOT = { has_building = building_karst_lab }
		NOT = { has_building_construction = building_karst_lab }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_generator_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_energy_building"

	destroy_trigger = {
		OR = {
			OR = {
				has_modifier = resort_colony
			}
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_generator_district_or_building = no
			}
		}
		planet = {
			pd_is_planet_class_cave = no
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = minerals
building_karst_mine = {
	base_buildtime = 600
	can_build = yes
	base_cap_amount = 1

	building_sets = {
		mining
	}

	category = resource

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		pd_is_planet_class_cave = yes
		NOT = { has_building = building_karst_grid }
		NOT = { has_building_construction = building_karst_grid }
		NOT = { has_building = building_karst_lab }
		NOT = { has_building_construction = building_karst_lab }
		OR = {
			owner = {
				is_ai = no
			}
			has_any_mining_district_or_building = yes
		}
	}

	inline_script = "buildings/pd_rare_mining_building"

	destroy_trigger = {
		OR = {
			has_modifier = resort_colony
			AND = {
				exists = owner
				owner = {
					is_ai = yes
				}
				has_any_mining_district_or_building = no
			}
		}
		planet = {
			pd_is_planet_class_cave = no
		}
	}
	ai_weight_coefficient = 9
	additional_ai_weight = 3503
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_minerals_value = yes }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
	}
}

# pd_economic_role = research
building_karst_lab = {
	base_buildtime = 600
	can_build = yes
	base_cap_amount = 1

	building_sets = {
		research
		engineering
	}

	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		pd_is_planet_class_cave = yes
		NOT = { has_building = building_karst_grid }
		NOT = { has_building_construction = building_karst_grid }
		NOT = { has_building = building_karst_mine }
		NOT = { has_building_construction = building_karst_mine }
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_engineering_building"
	inline_script = "buildings/pd_rare_engineering_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_regular_empire = yes }
		}
		modifier = {
			job_engineer_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_engineer_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_engineer_add = 300
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 8
		}
	}

	destroy_trigger = {
		planet = {
			pd_is_planet_class_cave = no
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = research
building_superhab_lab = {
	base_buildtime = 600
	can_build = yes
	base_cap_amount = 1

	building_sets = {
		research
		society
	}
	category = research

	potential = {
		exists = owner
		NOT = { has_modifier = resort_colony }
		pd_is_planet_class_superhabitable = yes
		NOT = { has_building = building_superhab_farm }
		NOT = { has_building_construction = building_superhab_farm }
		NOT = { has_building = building_superhab_foundry }
		NOT = { has_building_construction = building_superhab_foundry }
	}

	allow = {
		has_upgraded_capital = yes
	}

	inline_script = "buildings/pd_rare_society_building"
	inline_script = "buildings/pd_rare_society_building"

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_regular_empire = yes }
		}
		modifier = {
			job_biologist_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_biologist_add = 300
		}
	}

	resources = {
		category = planet_buildings
		cost = {
			minerals = 800
		}
		upkeep = {
			energy = 8
		}
	}

	destroy_trigger = {
		planet = {
			pd_is_planet_class_superhabitable = no
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_research_value = yes }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
	}
}

# pd_economic_role = alloys
building_superhab_farm = {
	base_buildtime = 600
	can_build = yes
	base_cap_amount = 1

	building_sets = {
		farming
	}

	category = resource

	potential = {
		exists = owner
		owner = {
			country_uses_food = yes
		}
		NOT = { has_modifier = resort_colony }
		pd_is_planet_class_superhabitable = yes
		NOT = { has_building = building_superhab_lab }
		NOT = { has_building_construction = building_superhab_lab }
		NOT = { has_building = building_superhab_foundry }
		NOT = { has_building_construction = building_superhab_foundry }

	}

	inline_script = "buildings/pd_rare_farm_building"

	destroy_trigger = {
		OR = {
			owner = {
				is_ai = yes
				country_uses_food = no
			}
			has_modifier = resort_colony

			planet = {
				pd_is_planet_class_superhabitable = no
			}
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}

# pd_economic_role = alloys
building_superhab_foundry = {
	base_buildtime = 600
	can_build = yes
	base_cap_amount = 1

	building_sets = {
		industrial
		foundry
	}

	category = manufacturing

	potential = {
		NOT = { has_modifier = resort_colony }
		owner = { NOT = { is_catalytic_empire = yes } }
		pd_is_planet_class_superhabitable = yes
		NOT = { has_building = building_superhab_lab }
		NOT = { has_building_construction = building_superhab_lab }
		NOT = { has_building = building_superhab_farm }
		NOT = { has_building_construction = building_superhab_farm }
	}

	inline_script = "buildings/pd_rare_foundry_building"

	destroy_trigger = {
		planet = {
			pd_is_planet_class_superhabitable = no
		}
	}
	ai_weight_coefficient = 16
	additional_ai_weight = 4000
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 8 staid_pd_planet_alloys_value = yes }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 12 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }
	}
}
```

## mods/StellarAIDirector/common/buildings/zzzz_staid_13_dataset_job_pressure_buildings.txt

_Omitted inline because this file is 481350 bytes. See the source manifest and use the local repo or JDataMunch/JDocMunch/JCodeMunch for exact retrieval._

## mods/StellarAIDirector/common/decisions/zzzz_staid_12_planetary_diversity_outpost_decisions.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied Planetary Diversity outpost decisions with Director-owned AI weighting.
# The copied parent potential/allow blocks decide whether a button exists; Director does not duplicate PD tech/site prerequisite checks.

# Source: common/decisions/pd_domed_base_decisions.txt

# planetary_diversity_role = moon_network_hub
decision_build_pd_moon_base = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			trigger = {
				num_moons = 1
			}
			minerals = 1000
		}
		cost = {
			trigger = {
				num_moons = 2
			}
			minerals = 2000
		}
		cost = {
			trigger = {
				num_moons = 3
			}
			minerals = 3000
		}
		cost = {
			trigger = {
				num_moons = 4
			}
			minerals = 4000
		}
		cost = {
			trigger = {
				num_moons = 5
			}
			minerals = 5000
		}
	}

	allow = {
		any_moon = {
			has_modifier = pd_domed_moonbase_site_1
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		any_moon = {
			has_modifier = pd_domed_moonbase_site_1
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		every_moon = {
			limit = {
				has_modifier = pd_domed_moonbase_site_1
			}
			custom_tooltip = MAKE_MOON_BASES
			hidden_effect = {
				planet_event = {
					id = pddomebases.50
				}
				pd_create_outpost_visual_effect = yes
			}
		}
	}


	ai_weight = {
		factor = 400000

		# policy_route = planetary_diversity_moon_network_hub
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 11 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 4 is_capital = yes }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}

# planetary_diversity_role = moon_colony_network_hub
decision_build_pd_moon_base_moon_colony = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			trigger = {
				orbit = {
					num_moons = 2
				}
			}
			minerals = 1000
		}
		cost = {
			trigger = {
				orbit = {
					num_moons = 3
				}
			}
			minerals = 2000
		}
		cost = {
			trigger = {
				orbit = {
					num_moons = 4
				}
			}
			minerals = 3000
		}
		cost = {
			trigger = {
				orbit = {
					num_moons = 5
				}
			}
			minerals = 4000
		}
		cost = {
			trigger = {
				orbit = {
					num_moons = 6
				}
			}
			minerals = 5000
		}
	}

	allow = {
		exists = owner
		is_moon = yes
		exists = orbit
		orbit = {
			any_moon = {
				has_modifier = pd_domed_moonbase_site_1
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		is_moon = yes
		exists = orbit
		orbit = {
			any_moon = {
				has_modifier = pd_domed_moonbase_site_1
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		orbit = {
			every_moon = {
				limit = {
					has_modifier = pd_domed_moonbase_site_1
				}
				custom_tooltip = MAKE_MOON_BASES
				hidden_effect = {
					planet_event = {
						id = pddomebases.50
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 400000

		# policy_route = planetary_diversity_moon_colony_network_hub
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 15 years_passed < 30 }
		modifier = { factor = 11 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 8 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 5 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 4 is_capital = yes }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}

# planetary_diversity_role = mining_outpost
decision_build_pd_mining_base = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_mining_site_1
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_mining_site_1
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_mining_site_1
				}
				custom_tooltip = MAKE_MINIG_BASES
				hidden_effect = {
					remove_modifier = pd_domed_mining_site_1
					add_modifier = {
						modifier = pd_domed_base_mining
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 175143

		# policy_route = planetary_diversity_mining_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 6 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 5 owner = { has_monthly_income = { resource = minerals value < 250 } } }
		modifier = { factor = 3 owner = { staid_resource_waste_pressure = yes } }
	}
}

# planetary_diversity_role = mining_outpost
decision_build_pd_mining_base_2 = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_mining_site_2
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_mining_site_2
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_mining_site_2
				}
				custom_tooltip = MAKE_MINIG_BASES
				hidden_effect = {
					remove_modifier = pd_domed_mining_site_2
					add_modifier = {
						modifier = pd_domed_base_mining
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 175143

		# policy_route = planetary_diversity_mining_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 6 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 5 owner = { has_monthly_income = { resource = minerals value < 250 } } }
		modifier = { factor = 3 owner = { staid_resource_waste_pressure = yes } }
	}
}

# planetary_diversity_role = mining_outpost
decision_build_pd_mining_base_3 = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_mining_site_3
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_mining_site_3
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_mining_site_3
				}
				custom_tooltip = MAKE_MINIG_BASES
				hidden_effect = {
					remove_modifier = pd_domed_mining_site_3
					add_modifier = {
						modifier = pd_domed_base_mining
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 175143

		# policy_route = planetary_diversity_mining_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 6 years_passed < 30 }
		modifier = { factor = 5 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 6 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 5 owner = { has_monthly_income = { resource = minerals value < 250 } } }
		modifier = { factor = 3 owner = { staid_resource_waste_pressure = yes } }
	}
}

# planetary_diversity_role = food_outpost
decision_build_pd_food_base = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_food_site_1
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_food_site_1
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_food_site_1
				}
				custom_tooltip = MAKE_FOOD_BASES
				hidden_effect = {
					remove_modifier = pd_domed_food_site_1
					add_modifier = {
						modifier = pd_domed_base_food
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 139143

		# policy_route = planetary_diversity_food_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 4 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 0 owner = { NOT = { country_uses_food = yes } } }
		modifier = { factor = 6 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 5 owner = { country_uses_food = yes NOT = { staid_food_runway_safe = yes } } }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}

# planetary_diversity_role = food_outpost
decision_build_pd_food_base_2 = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_food_site_2
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_food_site_2
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_food_site_2
				}
				custom_tooltip = MAKE_FOOD_BASES
				hidden_effect = {
					remove_modifier = pd_domed_food_site_2
					add_modifier = {
						modifier = pd_domed_base_food
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 139143

		# policy_route = planetary_diversity_food_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 4 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 0 owner = { NOT = { country_uses_food = yes } } }
		modifier = { factor = 6 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 5 owner = { country_uses_food = yes NOT = { staid_food_runway_safe = yes } } }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}

# planetary_diversity_role = food_outpost
decision_build_pd_food_base_3 = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_food_site_3
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_food_site_3
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_food_site_3
				}
				custom_tooltip = MAKE_FOOD_BASES
				hidden_effect = {
					remove_modifier = pd_domed_food_site_3
					add_modifier = {
						modifier = pd_domed_base_food
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 139143

		# policy_route = planetary_diversity_food_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 4 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 0 owner = { NOT = { country_uses_food = yes } } }
		modifier = { factor = 6 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 5 owner = { country_uses_food = yes NOT = { staid_food_runway_safe = yes } } }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}

# planetary_diversity_role = energy_outpost
decision_build_pd_energy_base = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_energy_site_1
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_energy_site_1
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_energy_site_1
				}
				custom_tooltip = MAKE_ENERGY_BASES
				hidden_effect = {
					remove_modifier = pd_domed_energy_site_1
					add_modifier = {
						modifier = pd_domed_base_energy
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 123714

		# policy_route = planetary_diversity_energy_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 6 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 5 owner = { has_monthly_income = { resource = energy value < 250 } } }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}

# planetary_diversity_role = energy_outpost
decision_build_pd_energy_base_2 = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_energy_site_2
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_energy_site_2
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_energy_site_2
				}
				custom_tooltip = MAKE_ENERGY_BASES
				hidden_effect = {
					remove_modifier = pd_domed_energy_site_2
					add_modifier = {
						modifier = pd_domed_base_energy
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 123714

		# policy_route = planetary_diversity_energy_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 6 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 5 owner = { has_monthly_income = { resource = energy value < 250 } } }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}

# planetary_diversity_role = energy_outpost
decision_build_pd_energy_base_3 = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_energy_site_3
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_energy_site_3
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_energy_site_3
				}
				custom_tooltip = MAKE_ENERGY_BASES
				hidden_effect = {
					remove_modifier = pd_domed_energy_site_3
					add_modifier = {
						modifier = pd_domed_base_energy
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 123714

		# policy_route = planetary_diversity_energy_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 6 owner = { staid_planetary_diversity_outpost_investment_ready = yes } }
		modifier = { factor = 5 owner = { has_monthly_income = { resource = energy value < 250 } } }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}

# planetary_diversity_role = capital_research_outpost
decision_build_pd_research_base = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_research_site_1
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_research_site_1
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_research_site_1
				}
				custom_tooltip = MAKE_RESEARCH_BASES
				hidden_effect = {
					remove_modifier = pd_domed_research_site_1
					add_modifier = {
						modifier = pd_domed_base_research
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 400000

		# policy_route = planetary_diversity_capital_research_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 8 owner = { staid_pd_research_outpost_priority_ready = yes } }
		modifier = { factor = 7 is_capital = yes }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
		modifier = { factor = 4 owner = { staid_research_input_runway_safe = yes } }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}

# planetary_diversity_role = capital_research_outpost
decision_build_pd_research_base_2 = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_research_site_2
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_research_site_2
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_research_site_2
				}
				custom_tooltip = MAKE_RESEARCH_BASES
				hidden_effect = {
					remove_modifier = pd_domed_research_site_2
					add_modifier = {
						modifier = pd_domed_base_research
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 400000

		# policy_route = planetary_diversity_capital_research_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 8 owner = { staid_pd_research_outpost_priority_ready = yes } }
		modifier = { factor = 7 is_capital = yes }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
		modifier = { factor = 4 owner = { staid_research_input_runway_safe = yes } }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}

# planetary_diversity_role = capital_research_outpost
decision_build_pd_research_base_3 = {
	icon = decision_build_moonbase
	owned_planets_only = yes

	enactment_time = 360
	resources = {
		category = decisions
		cost = {
			minerals = 1000
		}
	}

	allow = {
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_research_site_3
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	potential = {
		exists = owner
		NOT = { is_planet_class = pc_ark }	# arkship carriers can't host system outpost decisions (4.4 nomads)
		solar_system = {
			any_system_planet = {
				has_modifier = pd_domed_research_site_3
			}
		}
		owner = {
			has_technology = tech_pd_domed_colonies
		}
	}

	effect = {
		if = {
			limit = {
				NOT = {
					has_deposit = d_pd_solar_system_network_hub
				}
			}
			add_deposit = d_pd_solar_system_network_hub
			hidden_effect = {
				set_planet_flag = pd_solar_system_network_hub
			}
		}
		solar_system = {
			random_system_planet = {
				limit = {
					has_modifier = pd_domed_research_site_3
				}
				custom_tooltip = MAKE_RESEARCH_BASES
				hidden_effect = {
					remove_modifier = pd_domed_research_site_3
					add_modifier = {
						modifier = pd_domed_base_research
						days = -1
					}
					pd_create_outpost_visual_effect = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 400000

		# policy_route = planetary_diversity_capital_research_outpost
		# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.
		# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.
		modifier = { factor = 0 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 16 years_passed < 30 }
		modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }
		modifier = { factor = 8 owner = { staid_pd_research_outpost_priority_ready = yes } }
		modifier = { factor = 7 is_capital = yes }
		modifier = { factor = 5 owner = { staid_research_under_curve = yes } }
		modifier = { factor = 4 owner = { staid_research_input_runway_safe = yes } }
		modifier = { factor = 3 owner = { staid_planetary_capacity_growth_ready = yes } }
	}
}
```

## mods/StellarAIDirector/common/defines/zzzz_staid_14_high_scale_ai_defines.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object define override: removes vanilla construction and war hesitation
# that assumes a much smaller economy than the active Gigas/NSC3/ESC mod stack.
# User-directed 2026-07-08 tuning: keep local war aggression high, but do not
# encourage long-distance wars or galaxy-crossing fleet commitments.

NAI = {
	AI_FREE_JOBS_DISTRICT_BUILD_CAP = 2000
	AI_FREE_JOBS_BUILDING_BUILD_CAP = 5000
	AI_DEFICIT_SCORE_MULT = 500
	AI_FOCUS_SCORE_MULT = 12
	AI_RESOURCE_PRODUCTION_SCORE_MULT = 8
	AI_AMENITIES_SCORE_MULT = 8
	AI_HOUSING_SCORE_MULT = 8
	AI_CRIME_REDUCTION_SCORE_MULT = 4
	AI_ADMIN_CAP_SCORE_MULT = 6
	AI_POPS_SCORE_MULT = 0.25
	AI_NAVAL_CAP_SCORE_MULT = 25
	AI_UPGRADE_SCORE_MULT = 10
	AI_RESOURCE_TARGET_EXPIRATION_MONTHS = 6
	AI_RESOURCE_TARGET_VALID_THRESHOLD = 0.90
	AI_DISTRICT_MAX_OPPORTUNITY_COST_FACTOR = 0.05
	AI_DISTRICT_OPPORTUNITY_COST_FALLOFF = 0.25
	AI_BUILDING_MAX_OPPORTUNITY_COST_FACTOR = 0.05
	AI_BUILDING_OPPORTUNITY_COST_FALLOFF = 0.25
	AI_BUILDING_MIN_HYPOTHETICAL_WEIGHT = 5
	AI_DISTRICT_MIN_HYPOTHETICAL_WEIGHT = 5
	BUILDING_BUILD_THRESHOLD = 0.1
	BUILDING_EXISTS_DIV_SCORE = 0.2
	UNDERDEVELOPED_PLANET_LIMIT = 999
	AI_UNBUILT_DISTRICT_BOOST_POP_THRESHOLD = 250
	AI_UNBUILT_DISTRICT_BOOST_MULTIPLIER = 8.0
	AI_STORAGE_BUILDING_CAPPED_RESOURCE_BOOST = 1000
	AI_WAR_PREPARATION_MIN_MONTHS = 1
	AI_WAR_PREPARATION_MAX_MONTHS = 4
	AI_AGGRESSIVENESS_BASE = 50
	AI_AGGRESSIVENESS_BOXED_IN_MULT = 18
	AI_AGGRESSIVENESS_NO_COLONY_TARGET_MULT = 12
	ENEMY_FLEET_POWER_MULT = 0.55
	WAR_DECLARATION_MINIMUM_SCORE = 0.05
	WAR_DECLARATION_MALUS = 0.05
	WAR_DECLARATION_MAX_DISTANCE = 200
	OFFENSE_VS_DEFENSE_STRATEGY_ALLOTMENT = 3.0
}
```

## mods/StellarAIDirector/common/districts/zzzz_staid_06_research_infrastructure_districts.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/districts


# Source-local variables required by copied parent objects.
@base_rural_district_jobs = 200
@giga_planet_district_buildtime			= 240
@giga_planet_science_alloys 			= 2
@giga_planet_science_cost 				= 500
@giga_planet_science_maintenance 		= 5
@giga_planet_sr							= 25
@hab_cost = 150
@hab_maintenance = 2
@hab_time = 360
@habitat_research_district_jobs = 30
@low_hab_maintenance = 0.25

# policy_route = crowded_tall_route; source = common/districts/03_habitat_districts.txt; parent_ai = parent_ai_absent; source_ai_weight = no
district_hab_science = {
	base_buildtime = @hab_time
	is_uncapped = {	always = no }
	overlay_icon = GFX_district_research
	shared_capacity_modifier = district_hab_science

	zone_slots = {
		slot_habitat_research
	}

	show_on_uncolonized = {
		uses_district_set = habitat
	}

	potential = {
		uses_district_set = habitat
	}

	prerequisites = {
		tech_basic_science_lab_1
	}

	show_tech_unlock_if = {
		is_nomadic = no
		is_wilderness_empire = no
	}

	allow = {
		hidden_trigger = {
			OR = {
				NOT = { exists = owner }
				owner = {
					has_technology = tech_basic_science_lab_1
				}
				has_deposit = d_payback_habitat_research
			}
		}
	}

	resources = {
		category = planet_districts_hab
		cost = {
			alloys = @hab_cost
		}
		upkeep = {
			energy = @hab_maintenance
			alloys = @low_hab_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 300
	}

	inline_script = {
		script = jobs/habitat_researchers_add
		AMOUNT = @habitat_research_district_jobs
	}

	on_built = {
		carrier_event = {
			id = megastructures.220		# Spawn a research orbital
		}
	}

	triggered_name = {
		text = city_research_1
	}
	ai_weight_coefficient = 4
	additional_ai_weight = 500
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_planetary_capacity_growth_ready = yes } } }
	}
}


# policy_route = planetary_computer_research_core; source = common/districts/giga_planetary_computer.txt; parent_ai = parent_ai_absent; source_ai_weight = no
district_giga_pcc_science = {
	base_buildtime = @giga_planet_district_buildtime
	icon = district_virtual_science
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		uses_district_set = giga_planetary_computer
	}

	potential = {
		uses_district_set = giga_planetary_computer
	}

	zone_slots = {
		slot_gigas_research
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @giga_planet_science_cost
			alloys = @giga_planet_sr
		}
		upkeep = {
			energy = @giga_planet_science_maintenance
			alloys = @giga_planet_science_alloys
		}
	}

	inline_script = {
		script = jobs/researchers_add
		AMOUNT = @base_rural_district_jobs
	}

	#base stats
	planet_modifier = {
		planet_housing_add = 300
	}

	# inline_script = {
	# 	script = planet/research/giga_researcher_job_swap
	# 	jobs = 5
	# 	district = @yes
	# }

	# ai_resource_production = {
	# 	trigger = {
	# 		exists = owner
	# 		num_unemployed >= 3
	# 		owner = {
	# 			resource_income_compare = {
	# 				resource = energy
	# 				value > 0
	# 			}
	# 		}
	# 	}

	# 	ai_unobtainium = 1000
	# }
	ai_weight_coefficient = 12
	additional_ai_weight = 1800
	ai_weight = {
		factor = 1
		modifier = { factor = 0 owner = { NOT = { staid_planetary_computer_build_priority_ready = yes } } }
	}
}

```

## mods/StellarAIDirector/common/districts/zzzz_staid_09_gigas_habitat_zone_slot_compat_districts.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object compatibility override for Gigas habitat/orbital districts exposed by Director's crowded-tall route.
# Stellaris 4.4 district objects require zone_slots; the parent Gigas 4.4 files omit them for these districts.

# Source-local variables required by copied parent district objects.
@giga_hab_cost							= 500
@giga_hab_district_buildtime			= 240
@giga_hab_maintenance					= 2
@giga_planet_cost						= 300
@giga_planet_district_buildtime			= 240
@giga_planet_maintenance				= 1
@giga_planet_urban_cost 				= 500
@giga_planet_urban_district_buildtime 	= 480
@giga_planet_urban_maintenance 			= 2
@yes = 1

# Source: common/districts/giga_habitats.txt
district_giga_hab_city = {
	zone_slots = {
		slot_city_government
		slot_habitat_01
		slot_habitat_02
	}
	base_buildtime = @giga_hab_district_buildtime
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes

	show_on_uncolonized = {
		exists = from
		from = { is_gestalt = no }
		uses_district_set = giga_habitat
	}

	potential = {
		exists = owner
		owner = { is_gestalt = no }
		uses_district_set = giga_habitat
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_hab_nexus
		district_giga_hab_hive
	}

	resources = {
		category = planet_districts
		cost = { minerals = @giga_hab_cost }
		upkeep = { energy = @giga_hab_maintenance }
	}

	planet_modifier = {
		planet_housing_add = 800
	}

	inline_script = {
		script = planet/maintenance/giga_clerk_job_swap
		jobs = 3
		district = @yes
	}

	triggered_planet_modifier = { potential = { exists = owner owner = { has_valid_civic = civic_agrarian_idyll } }												modifier = { planet_housing_add = -100 } }
	triggered_planet_modifier = { potential = { exists = owner owner = { has_active_tradition = tr_prosperity_public_works } }								modifier = { planet_housing_add = 100 } }
	triggered_planet_modifier = { potential = { exists = owner owner = { has_technology = tech_housing_1 } }													modifier = { planet_housing_add = 100 } }
	triggered_planet_modifier = { potential = { exists = owner owner = { has_technology = tech_housing_2 NOT = { has_valid_civic = civic_agrarian_idyll } } }	modifier = { planet_housing_add = 100 } }

	# Bug Branch
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_bugged_rooftop_farmers = yes }
		}
		modifier = {
			job_farmer_add = 1
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_bugged_rooftop_farmers = yes }
		}
		text = job_farmer_effect_desc
	}
	# Bug Branch
}

district_giga_hab_hive = {
	zone_slots = {
		slot_city_government
		slot_habitat_01
		slot_habitat_02
	}
	base_buildtime = @giga_hab_district_buildtime
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes

	show_on_uncolonized = {
		exists = from
		from = { is_hive_empire = yes }
		uses_district_set = giga_habitat
	}

	potential = {
		exists = owner
		owner = { is_hive_empire = yes }
		uses_district_set = giga_habitat
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_hab_nexus
		district_giga_hab_city
	}

	resources = {
		category = planet_districts
		cost = { minerals = @giga_hab_cost }
		upkeep = { energy = @giga_hab_maintenance }
	}

	triggered_planet_modifier = {
		modifier = {
			planet_housing_add = 800
			job_maintenance_drone_add = 2
		}
	}

	triggered_planet_modifier = { potential = { exists = owner owner = { has_technology = tech_housing_1 } }								modifier = { planet_housing_add = 100 } }
	triggered_planet_modifier = { potential = { exists = owner owner = { has_technology = tech_housing_2 } }								modifier = { planet_housing_add = 100 job_maintenance_drone_add = 1 } }
	triggered_planet_modifier = { potential = { exists = owner owner = { has_active_tradition = tr_prosperity_extended_hives } }			modifier = { planet_housing_add = 100 } }
	triggered_desc = {																														text = "job_maintenance_drone_effect_desc" }
}

district_giga_hab_nexus = {
	zone_slots = {
		slot_city_government
		slot_habitat_01
		slot_habitat_02
	}
	base_buildtime = @giga_hab_district_buildtime
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes

	show_on_uncolonized = {
		exists = from
		from = { is_machine_empire = yes }
		uses_district_set = giga_habitat
	}

	potential = {
		exists = owner
		owner = { is_machine_empire = yes }
		uses_district_set = giga_habitat
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_hab_hive
		district_giga_hab_city
	}

	resources = {
		category = planet_districts
		cost = { minerals = @giga_hab_cost }
		upkeep = { energy = @giga_hab_maintenance }
	}

	triggered_planet_modifier = {
		modifier = {
			planet_housing_add = 800
			job_maintenance_drone_add = 1
			job_technician_drone_add = 1
		}
	}

	triggered_planet_modifier = { potential = { exists = owner owner = { has_technology = tech_housing_1 } }								modifier = { planet_housing_add = 100 } }
	triggered_planet_modifier = { potential = { exists = owner owner = { has_technology = tech_housing_2 } }								modifier = { planet_housing_add = 100 job_maintenance_drone_add = 1 } }
	triggered_planet_modifier = { potential = { exists = owner owner = { has_active_tradition = tr_prosperity_optimized_nexus } }			modifier = { planet_housing_add = 100 } }
	triggered_desc = {																														text = "job_maintenance_drone_effect_desc" }
}

district_giga_hab_science = {
	zone_slots = {
		slot_habitat_research
	}
	base_buildtime = @giga_hab_district_buildtime
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		uses_district_set = giga_habitat
		has_planet_flag = giga_interstellar_hab
	}

	potential = {
		uses_district_set = giga_habitat
		has_planet_flag = giga_interstellar_hab
	}

	resources = {
		category = planet_districts
		cost = { minerals = @giga_hab_cost }
		upkeep = { energy = @giga_hab_maintenance }
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_hab_city
		district_giga_hab_hive
		district_giga_hab_nexus
	}

	planet_modifier = {
		planet_housing_add = 400
	}

	### Interstellar Habitat
	triggered_planet_modifier = { potential = { has_planet_flag = giga_interstellar_hab exists = owner owner = { is_gestalt = no } }					modifier = { job_giga_interstellar_researcher_add = 4 } }
	triggered_planet_modifier = { potential = { has_planet_flag = giga_interstellar_hab exists = owner owner = { is_gestalt = yes } }					modifier = { job_giga_interstellar_researcher_drone_add = 4 } }
	triggered_desc = {				trigger = { has_planet_flag = giga_interstellar_hab exists = owner owner = { is_gestalt = no } }					text = "job_giga_interstellar_researcher_effect_desc" }
	triggered_desc = {				trigger = { has_planet_flag = giga_interstellar_hab exists = owner owner = { is_gestalt = yes } }					text = "job_giga_interstellar_researcher_drone_effect_desc" }
}

district_giga_hab_scavenger = {
	zone_slots = {
		slot_habitat_minerals
	}
	base_buildtime = @giga_hab_district_buildtime
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		uses_district_set = giga_habitat
		has_planet_flag = giga_interstellar_hab
	}

	potential = {
		uses_district_set = giga_habitat
		has_planet_flag = giga_interstellar_hab
	}

	resources = {
		category = planet_districts
		cost = { minerals = @giga_hab_cost }
		upkeep = { energy = @giga_hab_maintenance }
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_hab_city
		district_giga_hab_hive
		district_giga_hab_nexus
	}

	triggered_planet_modifier = { modifier = { planet_housing_add = 200 } }

	### Interstellar Habitat
	triggered_planet_modifier = { potential = { has_planet_flag = giga_interstellar_hab exists = owner owner = { is_gestalt = yes } }	modifier = { job_giga_interstellar_scavenger_drone_add = 2 } }
	triggered_planet_modifier = { potential = { has_planet_flag = giga_interstellar_hab exists = owner owner = { is_gestalt = no } }	modifier = { job_giga_interstellar_scavenger_add = 2 } }
	triggered_desc = {				trigger = { has_planet_flag = giga_interstellar_hab exists = owner owner = { is_gestalt = yes } }	text = "job_giga_interstellar_scavenger_drone_effect_desc" }
	triggered_desc = {				trigger = { has_planet_flag = giga_interstellar_hab exists = owner owner = { is_gestalt = no } }	text = "job_giga_interstellar_scavenger_effect_desc" }
}

# Source: common/districts/giga_orbital.txt
district_giga_orbital_farming = {
	zone_slots = {
		slot_city_01
	}
	base_buildtime = @giga_planet_district_buildtime
	icon = district_farming
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		or = {
			uses_district_set = giga_orbital
			uses_district_set = giga_ancient_elysium # legacy
		}
	}

	potential = {
		or = {
			uses_district_set = giga_orbital
			uses_district_set = giga_ancient_elysium # legacy
		}
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @giga_planet_cost
		}
		cost = {
			trigger = {
				AND = {
					exists = owner
					owner = { is_anglers_empire = yes }
					planet = { has_modifier = flooded_habitat }
				}
			}
			minerals = -50
		}
		upkeep = {
			energy = @giga_planet_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 200
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_agrarian_idyll
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_agri_drone_add = 3
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_agri_drone_add = 2
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
				is_fallen_empire_spiritualist = no
				NAND = {
					is_anglers_empire = yes
					PREV = { planet = { has_modifier = flooded_habitat } }
				}
			}
		}
		modifier = {
			job_farmer_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_fallen_empire_spiritualist = yes }
		}
		modifier = {
			job_fe_acolyte_farm_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_anglers_empire = yes }
			planet = { has_modifier = flooded_habitat }
		}
		modifier = {
			job_angler_add = 1
			job_pearl_diver_add = 1
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		text = job_agri_drone_effect_desc
	}
	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
				is_fallen_empire_spiritualist = no
				NAND = {
					is_anglers_empire = yes
					PREV = { planet = { has_modifier = flooded_habitat } }
				}
			}
		}
		text = job_farmer_effect_desc
	}
	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_fallen_empire_spiritualist = yes }
		}
		text = job_fe_acolyte_farm_effect_desc
	}
	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_anglers_empire = yes }
			planet = { has_modifier = flooded_habitat }
		}
		text = job_aqu_angler_effect_desc
	}
	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_anglers_empire = yes }
			planet = { has_modifier = flooded_habitat }
		}
		text = job_pearl_diver_effect_desc
	}

	prerequisites = {
		tech_industrial_farming
	}

	destroy_trigger = {
		exists = owner
		AND = {
			owner = { is_ai = yes }
			owner = { country_uses_food = no }
		}
	}
}

district_giga_orbital_sanctuary = {
	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}
	base_buildtime = @giga_planet_urban_district_buildtime
	icon = district_arcology_organic_housing
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		uses_district_set = giga_orbital
		from = {
			has_valid_civic = civic_machine_servitor
		}
	}

	potential = {
		uses_district_set = giga_orbital
		exists = owner
		owner = {
			has_valid_civic = civic_machine_servitor
		}
	}

	resources = {
		category = planet_districts
		cost = { minerals = @giga_planet_urban_cost }
		upkeep = { energy = @giga_planet_urban_maintenance }
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_planet_admin
		district_giga_planet_admin_religious
		district_giga_planet_sanctuary
	}

	planet_modifier = {
		job_bio_trophy_add = 10
		planet_carry_cap_add = 10
	}

	# Bug Branch
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
				is_bugged_rooftop_farmers = yes
			}
		}
		modifier = {
			job_farmer_add = 1
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
				is_bugged_rooftop_farmers = yes
			}
		}
		text = job_farmer_effect_desc
	}
	# Bug Branch

	triggered_desc = {
		text = job_bio_trophy_effect_desc
	}
	triggered_desc = {
		text = job_artisan_drone_effect_desc
	}
}

district_giga_orbital_preserve = {
	zone_slots = {
		slot_city_01
	}
	base_buildtime = @giga_planet_district_buildtime
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		uses_district_set = giga_orbital
		exists = from
		from = {
			NOT = { has_valid_civic = civic_dystopian_society }
		}
	}

	potential = {
		uses_district_set = giga_orbital
		exists = owner
		owner = {
			NOT = { has_valid_civic = civic_dystopian_society }
		}
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @giga_planet_cost
		}
		# upkeep = {
		# 	energy = @giga_planet_maintenance
		# }
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		job_giga_preserver_add = 1
	}
	triggered_desc = {
		trigger = {	exists = owner owner = { is_gestalt = no } }
		text = job_giga_preserver_effect_desc
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		job_giga_preserver_drone_add = 1
	}
	triggered_desc = {
		trigger = {	exists = owner owner = { is_gestalt = yes } }
		text = job_giga_preserver_drone_effect_desc
	}
}

district_giga_orbital_logistics = {
	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}
	base_buildtime = @giga_planet_urban_district_buildtime

	show_on_uncolonized = {
		uses_district_set = giga_orbital
	}

	potential = {
		uses_district_set = giga_orbital
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @giga_planet_urban_cost
		}
		upkeep = {
			energy = 5
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { has_valid_civic = civic_machine_servitor }
			}
			energy = 5
		}
	}

	planet_modifier = {
		giga_system_resettlement_unemployed_mult = 0.1
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				not = { has_valid_civic = civic_machine_servitor }
			}
		}
		giga_system_resettlement_unemployed_mult = 0.1
		planet_jobs_productive_produces_mult = 0.05
		planet_jobs_productive_upkeep_mult = 0.05
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_machine_servitor
			}
		}
		giga_system_bio_trophy_propagation = 0.1
		planet_bio_trophies_consumer_goods_upkeep_add = 0.25
		planet_bio_trophies_energy_upkeep_add = 1
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		job_enforcer_add = 1
		job_clerk_add = 1
	}
	triggered_desc = {
		trigger = {	exists = owner owner = { is_gestalt = no } }
		text = job_enforcer_effect_desc
	}
	triggered_desc = {
		trigger = {	exists = owner owner = { is_gestalt = no } }
		text = job_clerk_effect_desc
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		job_patrol_drone_add = 1
		job_maintenance_drone_add = 1
	}
	triggered_desc = {
		trigger = {	exists = owner owner = { is_gestalt = yes } }
		text = job_patrol_drone_effect_desc
	}
	triggered_desc = {
		trigger = {	exists = owner owner = { is_gestalt = yes } }
		text = job_maintenance_drone_effect_desc
	}
}
```

## mods/StellarAIDirector/common/districts/zzzz_staid_13_dataset_job_pressure_districts.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object overrides copied from active-stack construction winners.
# Dataset-driven job pressure: if a planet has unemployed pops and no free jobs, build economically viable job providers instead of leaving pops idle.
# Source potential/allow/possible blocks still own prerequisites and legality.
# Source dataset: research/stellar-ai/stellar-ai-director-economic-valuation-2026-07-07.csv

# Source-local variables required by copied construction objects.
@advanced_cost = 1000
@advanced_rare_cost = 50
@advanced_rare_upkeep = 1
@advanced_time = 720
@advanced_upkeep = 5
@b2_jobs = 400
@b2_minerals = 600
@b2_time = 480
@b2_upkeep = 5
@b3_rare_cost = 100
@b3_upkeep = 8
@b4_minerals = 2000
@b4_upkeep = 10
@base_cost = 300
@base_district_jobs = 100
@base_rural_district_jobs = 200
@biomass_cost = 50
@city_cost = 500
@city_time = 480
@city_upkeep = 2
@elysium_cost = 500
@elysium_maintenance = 5
@giga_alderson_cost						= 10000
@giga_alderson_maintenance				= 30
@giga_amb_flag = giga_buildcap_j # menu option variable name, checked for feature activation
@giga_birch_insula_cost = 5000 # minerals and alloys
@giga_birch_insula_maintenance = 40
@giga_birch_insula_time = 2400
@giga_gas_giant_habitat_cost				 	= 500
@giga_gas_giant_habitat_district_buildtime		= 240
@giga_gas_giant_habitat_upkeep_energy_heavy 	= 3
@giga_planet_cost						= 300
@giga_planet_district_buildtime			= 240
@giga_planet_maintenance				= 1
@giga_planet_urban_district_buildtime 	= 480
@hab_cost = 150
@hab_maintenance = 2
@hab_time = 360
@low_hab_maintenance = 0.25
@maginot_barracks_police_jobs_add = 200
@maginot_barracks_police_jobs_add_ringworld = 1000
@maginot_bunker_police_jobs_add = 100
@maginot_bunker_police_jobs_add_ringworld = 500
@maginot_district_amenities_barracks = 1000
@maginot_district_amenities_barracks_ringworld = 5000
@maginot_district_buildtime = 600
@maginot_district_buildtime_ringworld = 1200
@maginot_district_cost_alloys_cheap = 10
@maginot_district_cost_alloys_cheap_ringworld = 20
@maginot_district_cost_alloys_expensive = 500
@maginot_district_cost_alloys_medium = 100
@maginot_district_cost_alloys_medium_ringworld = 200
@maginot_district_cost_minerals = 1000
@maginot_district_cost_minerals_ringworld = 2000
@maginot_district_cost_sr = 50
@maginot_district_cost_sr_ringworld = 100
@maginot_district_housing_barracks = 1500
@maginot_district_housing_barracks_ringworld = 7500
@maginot_district_housing_buffs = 300
@maginot_district_housing_bunkers = 500
@maginot_district_housing_bunkers_ringworld = 2500
@maginot_district_upkeep_alloys = 10
@maginot_district_upkeep_energy_barracks = 12
@maginot_district_upkeep_energy_barracks_ringworld = 24
@maginot_district_upkeep_energy_medium = 8
@maginot_district_upkeep_energy_medium_ringworld = 16
@maginot_district_upkeep_energy_shields = 50
@maginot_district_upkeep_sr = 1
@maginot_district_upkeep_sr_ringworld = 3
@maginot_entertainer_filler_jobs_add = 400
@maginot_entertainer_filler_jobs_add_ringworld = 2000
@maginot_entertainer_filler_jobs_buff = 300
@maginot_entertainer_filler_jobs_buff_ringworld = 300
@maginot_special_jobs_add = 100
@maginot_special_jobs_add_ringworld = 500
@mega_time = 960
@rw_cost = 1000
@rw_cost_sr = 50
@rw_district_buildtime = 360
@rw_maintenance = 5
@rw_maintenance_sr = 2
@special_district_jobs = 300
@wilderness_district_build_short = 240
@yes = 1

# object = district:district_srw_commercial; source = Planetary Diversity - More Arcologies::common\districts\00_urban_districts.txt
# staid_dataset_job_pressure = family:consumer_goods_repair jobs:400.0 roi2250:2894100.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack|unresolved_variables
district_srw_commercial = {
	base_buildtime = 240

	overlay_icon = GFX_district_trade

	min_for_deposits_on_planet = 3
	max_for_deposits_on_planet = 15

	zone_slots = {
		slot_city_04
	}

	show_on_uncolonized = {
		always = no
		exists = from
		from = { is_regular_empire = yes }
		uses_district_set = shattered_ring_world
	}

	potential = {
		always = no
		exists = owner
		owner = { is_regular_empire = yes }
		uses_district_set = shattered_ring_world
	}

	allow = {
		hidden_trigger = {
			NOT = { has_modifier = resort_colony }
		}
		custom_tooltip = {
			fail_text = arcology_project_construction_fail_tt
			NOT = { has_carrier_flag = arcology_project_construction }
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_rw_commercial
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @base_cost
		}
		upkeep = {
			energy = 1
		}
	}

	planet_modifier = {
		planet_housing_add = 200
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_fallen_empire_spiritualist = no }
		}
		modifier = {
			job_trader_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_regular_empire = yes
			}
		}
		job_artisan_add = 100
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_fallen_empire_spiritualist = yes }
		}
		modifier = {
			job_bureaucrat_add = @base_district_jobs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_active_tradition = tr_mercantile_commercial_enterprise
			}
		}
		modifier = {
			job_trader_add = 100
		}
	}
	ai_weight_coefficient = 26
	additional_ai_weight = 5138
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 18 owner = { country_uses_consumer_goods = yes NOT = { staid_consumer_goods_runway_safe = yes } } }
	}

	ai_resource_production = {
		consumer_goods = 4
	}
}

# object = district:district_giga_frameworld_factory_advanced; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:consumer_goods_repair jobs:1.0 roi2250:22800.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_giga_frameworld_factory_advanced = {
	base_buildtime = @advanced_time
	icon = district_arcology_civilian_industry
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		exists = from
		uses_district_set = giga_frameworld
		has_carrier_flag = frameworld_advanced_industrial
		from = {
			or = {
				is_gestalt = no
				has_valid_civic = civic_machine_servitor
				country_uses_consumer_goods = yes
			}
		}
	}

	potential = {
		exists = owner
		uses_district_set = giga_frameworld
		has_carrier_flag = frameworld_advanced_industrial
		owner = {
			or = {
				is_gestalt = no
				has_valid_civic = civic_machine_servitor
				country_uses_consumer_goods = yes
			}
		}
	}

	conversion_ratio = 2
	convert_to = {
		district_giga_frameworld_foundry
	}

	resources = {
		category = planet_districts_industrial
		cost = {
			minerals = @advanced_cost
			rare_crystals = @advanced_rare_cost
		}
		upkeep = {
			energy = @advanced_upkeep
			rare_crystals = @advanced_rare_upkeep
		}

		upkeep = {
			trigger = {
				exists = owner
				owner = {
					has_edict = industrial_maintenance
				}
			}
			energy = 2
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_crafter_empire = yes }
		}
		modifier = {
		}
	}

	inline_script = {
		script = planet/consumer_goods/giga_artisan_job_swap
		jobs = 4
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_machine_empire = yes
				has_edict = industrial_maintenance
			}
		}
		modifier = {
			job_maintenance_drone_add = 1
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_machine_empire = yes
				has_edict = industrial_maintenance
			}
		}
		text = job_maintenance_drone_effect_desc
	}


	#ai_resource_production = {
	#	ai_unobtainium = 1000
	#	trigger = {
	#		frameworld_want_industrial = yes
	#	}
	#}
	ai_weight_coefficient = 17
	additional_ai_weight = 1315
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 18 owner = { country_uses_consumer_goods = yes NOT = { staid_consumer_goods_runway_safe = yes } } }
	}

	ai_resource_production = {
		consumer_goods = 10
	}
}

# object = district:district_giga_frameworld_factory; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:consumer_goods_repair jobs:1.0 roi2250:18300.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_giga_frameworld_factory = {
	base_buildtime = @city_time
	icon = district_arcology_civilian_industry
	is_uncapped = { always = yes }

	prerequisites = {
		tech_basic_industry
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
	}

	show_on_uncolonized = {
		exists = from
		uses_district_set = giga_frameworld
		not = { has_carrier_flag = frameworld_advanced_industrial }
		from = {
			or = {
				is_gestalt = no
				has_valid_civic = civic_machine_servitor
				country_uses_consumer_goods = yes
			}
		}
	}

	potential = {
		exists = owner
		uses_district_set = giga_frameworld
		not = { has_carrier_flag = frameworld_advanced_industrial }
		owner = {
			or = {
				is_gestalt = no
				has_valid_civic = civic_machine_servitor
				country_uses_consumer_goods = yes
			}
		}
	}

	conversion_ratio = 0.5
	convert_to = {
		district_giga_frameworld_factory_advanced
	}

	resources = {
		category = planet_districts_industrial
		cost = {
			minerals = @city_cost
		}
		upkeep = {
			energy = @city_upkeep
		}

		upkeep = {
			trigger = {
				exists = owner
				owner = {
					has_edict = industrial_maintenance
				}
			}
			energy = 2
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_crafter_empire = yes }
		}
		modifier = {
		}
	}

	inline_script = {
		script = planet/consumer_goods/giga_artisan_job_swap
		jobs = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_machine_empire = yes
				has_edict = industrial_maintenance
			}
		}
		modifier = {
			job_maintenance_drone_add = 1
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_machine_empire = yes
				has_edict = industrial_maintenance
			}
		}
		text = job_maintenance_drone_effect_desc
	}


	#ai_resource_production = {
	#	ai_unobtainium = 1000
	#	trigger = {
	#		frameworld_want_industrial = yes
	#	}
	#}
	ai_weight_coefficient = 17
	additional_ai_weight = 1287
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 18 owner = { country_uses_consumer_goods = yes NOT = { staid_consumer_goods_runway_safe = yes } } }
	}

	ai_resource_production = {
		consumer_goods = 5
	}
}

# object = district:district_giga_frameworld_supertensiles; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:alloy_scaling jobs:6.0 roi2250:79890.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep
district_giga_frameworld_supertensiles = {
	base_buildtime = @b2_time
	icon = district_giga_supertensiles
	is_uncapped = { always = yes }

	prerequisites = {
		giga_tech_amb_supertensiles
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
	}

	show_on_uncolonized = {
		has_global_flag = @giga_amb_flag
		exists = from
		from = {
			has_technology = giga_tech_amb_supertensiles
		}
		uses_district_set = giga_frameworld
	}

	potential = {
		has_global_flag = @giga_amb_flag
		exists = owner
		owner = {
			has_technology = giga_tech_amb_supertensiles
		}
		uses_district_set = giga_frameworld
	}

	resources = {
		category = planet_districts_industrial
		cost = {
			minerals = @b2_minerals
		}
		upkeep = {
			energy = @b2_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
				is_fallen_empire_spiritualist = no
			}
		}
		modifier = {
			job_giga_megaengineer_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		modifier = {
			job_giga_megaengineer_drone_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_fallen_empire_spiritualist = yes
			}
		}
		modifier = {
			job_giga_amb_fe_acolyte_foundry_add = 2
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
				is_fallen_empire_spiritualist = no
			}
		}
		text = job_giga_megaengineer_effect_desc
	}
	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		text = job_giga_megaengineer_drone_effect_desc
	}
	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_fallen_empire_spiritualist = yes
			}
		}
		text = job_giga_amb_fe_acolyte_foundry_effect_desc
	}

	ai_weight_coefficient = 20
	additional_ai_weight = 1519
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { has_monthly_income = { resource = alloys value < 500 } } }
	}

	ai_resource_production = {
		alloys = 1
		giga_sr_amb_megaconstruction = 2
	}
}

# object = district:district_giga_frameworld_foundry; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:alloy_scaling jobs:1.0 roi2250:9600.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_giga_frameworld_foundry = {
	base_buildtime = @city_time
	icon = district_arcology_arms_industry
	is_uncapped = { always = yes }

	prerequisites = {
		tech_basic_industry
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
	}

	show_on_uncolonized = {
		exists = from
		uses_district_set = giga_frameworld
		not = { has_carrier_flag = frameworld_advanced_industrial }
	}

	potential = {
		exists = owner
		uses_district_set = giga_frameworld
		not = { has_carrier_flag = frameworld_advanced_industrial }
	}

	conversion_ratio = 0.5
	convert_to = {
		district_giga_frameworld_foundry_advanced
	}

	resources = {
		category = planet_districts_industrial
		cost = {
			minerals = @city_cost
		}
		upkeep = {
			energy = @city_upkeep
		}

		upkeep = {
			trigger = {
				exists = owner
				owner = {
					has_edict = industrial_maintenance
				}
			}
			energy = 2
		}

		# nanite upgrade
		upkeep = {
			trigger = {
				frameworld_has_active_nanite_upgrade = yes
			}
			energy = 10
			nanites = 1
		}
		produces = {
			trigger = {
				frameworld_has_active_nanite_upgrade = yes
			}
			alloys = 5
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_crafter_empire = yes }
		}
		modifier = {
		}
	}

	inline_script = {
		script = planet/alloys/giga_foundry_job_swap
		jobs = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_machine_empire = yes
				has_edict = industrial_maintenance
			}
		}
		modifier = {
			job_maintenance_drone_add = 1
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_machine_empire = yes
				has_edict = industrial_maintenance
			}
		}
		text = job_maintenance_drone_effect_desc
	}


	ai_weight_coefficient = 16
	additional_ai_weight = 1203
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { has_monthly_income = { resource = alloys value < 500 } } }
	}

	ai_resource_production = {
		alloys = 7
	}
}

# object = district:district_giga_frameworld_foundry_advanced; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:alloy_scaling jobs:1.0 roi2250:5400.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_giga_frameworld_foundry_advanced = {
	base_buildtime = @advanced_time
	icon = district_arcology_arms_industry
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		exists = from
		uses_district_set = giga_frameworld
		has_carrier_flag = frameworld_advanced_industrial
	}

	potential = {
		exists = owner
		uses_district_set = giga_frameworld
		has_carrier_flag = frameworld_advanced_industrial
	}

	conversion_ratio = 2
	convert_to = {
		district_giga_frameworld_foundry
	}

	resources = {
		category = planet_districts_industrial
		cost = {
			minerals = @advanced_cost
			volatile_motes = @advanced_rare_cost
		}
		upkeep = {
			energy = @advanced_upkeep
			volatile_motes = @advanced_rare_upkeep
		}

		upkeep = {
			trigger = {
				exists = owner
				owner = {
					has_edict = industrial_maintenance
				}
			}
			energy = 2
		}

		# nanite upgrade
		upkeep = {
			trigger = {
				frameworld_has_active_nanite_upgrade = yes
			}
			energy = 20
			nanites = 2
		}
		produces = {
			trigger = {
				frameworld_has_active_nanite_upgrade = yes
			}
			alloys = 10
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_crafter_empire = yes }
		}
		modifier = {
		}
	}

	inline_script = {
		script = planet/alloys/giga_foundry_job_swap
		jobs = 4
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_machine_empire = yes
				has_edict = industrial_maintenance
			}
		}
		modifier = {
			job_maintenance_drone_add = 1
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_machine_empire = yes
				has_edict = industrial_maintenance
			}
		}
		text = job_maintenance_drone_effect_desc
	}


	ai_weight_coefficient = 15
	additional_ai_weight = 1128
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { has_monthly_income = { resource = alloys value < 500 } } }
	}

	ai_resource_production = {
		alloys = 14
	}
}

# object = district:district_mindlink; source = Stellaris vanilla::common\districts\00_special_districts.txt
# staid_dataset_job_pressure = family:research_scaling jobs:3000.0 roi2250:22062075.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|uses_inline_script
district_mindlink = {
	icon = district_city
	overlay_icon = GFX_district_feral_insight
	base_buildtime = 720
	gridbox = district_city

	exempt_from_ai_planet_specialization = yes

	show_on_uncolonized = {
		always = no
	}

	potential = {
		exists = owner
		is_capital = yes
		owner = {
			has_menace_perk = menp_behemoth_mind_meld
		}
	}

	allow = {
		hidden_trigger = {
			NOR = {
				has_modifier = resort_colony
				has_modifier = penal_colony
				has_modifier = slave_colony
			}
		}
		custom_tooltip = {
			fail_text = arcology_project_construction_fail_tt
			OR = {
				owner = { is_nomadic = yes }
				NOT = { has_carrier_flag = arcology_project_construction }
			}
		}
	}

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	conversion_ratio = 1
	convert_to = {
		district_ark_city
		district_arcology_housing
		district_rw_city
		district_rw_hive
		district_rw_nexus
		district_city
		district_nexus
		district_hive
		district_hab_housing
		district_crashed_slaver_ship
		district_craglands
	}

	resources = {
		category = planet_districts_cities
		cost = {
			food = 1500
		}
		cost = {
			trigger = {
				owner = { is_wilderness_empire = yes }
			}
			biomass = @biomass_cost
		}
		upkeep = {
			food = 2
		}
		produces = {
			trigger = {
				owner = { is_variable_set =  pops_transferred }
				owner = { is_wilderness_empire = no }
			}
			unity = 1.5
			physics_research = 0.5
			society_research = 0.5
			engineering_research = 0.5
			mult = owner.value:transferred_pops_district_percent
		}
		produces = {
			trigger = {
				owner = { is_variable_set =  pops_transferred }
				owner = { is_wilderness_empire = yes }
			}
			unity = 300
			physics_research = 100
			society_research = 100
			engineering_research = 100
			mult = owner.value:transferred_pops_district_percent
		}
	}

	inline_script = {
		script = buildings/on_all_wilderness_buildings_districts
	}

	planet_modifier = {
		planet_housing_add = 3000
	}

	triggered_planet_modifier = { #Regular modifiers
		potential = {
			exists = owner
			owner = { is_regular_empire = yes }
		}
		modifier = {
			job_transference_volunteer_add = 1500
		}
	}

	triggered_planet_modifier = { # Gestalt modifiers
		potential = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		modifier = {
			planet_housing_add = 1000
			job_transference_drone_add = 1500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_desc = { #same as transference drone so everyone gets it
		trigger = {
			exists = owner
		}
		text = job_transference_volunteer_effect_desc
	}
	ai_weight_coefficient = 29
	additional_ai_weight = 15000
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { staid_research_under_curve = yes } }
	}

	ai_resource_production = {
		engineering_research = 100
		physics_research = 100
		society_research = 100
		unity = 302
	}
}

# object = district:district_rw_generator; source = Stellaris vanilla::common\districts\04_ringworld_districts.txt
# staid_dataset_job_pressure = family:energy_scaling jobs:4500.0 roi2250:32414400.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_rw_generator = {
	base_buildtime = @rw_district_buildtime


	zone_slots = {
		slot_energy
	}

	show_on_uncolonized = {
		always = no
	}

	potential = {
		always = no
	}

	convert_to = {
		district_rw_commercial
		district_ark_generator
	}

	resources = {
		category = planet_districts_rw_generator
		cost = {
			minerals = @rw_cost
			rare_crystals = @rw_cost_sr
		}
		upkeep = {
			energy = @rw_maintenance
			rare_crystals = @rw_maintenance_sr
		}
	}

	triggered_planet_modifier = {
		planet_housing_add = 1000
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		job_technician_drone_add = 1000
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		planet_housing_add = 500
		job_technician_drone_add = 1500
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
				is_fallen_empire_spiritualist = no
			}
		}
		modifier = {
			job_technician_add = 1000
		}
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_fallen_empire_spiritualist = yes }
		}
		modifier = {
			job_fe_acolyte_generator_add = 1000
		}
	}

	triggered_desc = {
		trigger = {
			planet = {
				has_deposit = d_arcane_generator
				NOT = { has_district = district_rw_generator }
			}
		}
		text = arcane_generator_upkeep_desc
	}
	ai_weight_coefficient = 30
	additional_ai_weight = 15000
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { has_monthly_income = { resource = energy value < 500 } } }
	}

	ai_resource_production = {
		energy = 45
	}
}

# object = district:district_giga_frameworld_negative_mass; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:energy_scaling jobs:800.0 roi2250:5790900.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep
district_giga_frameworld_negative_mass = {
	base_buildtime = @advanced_time
	icon = district_giga_negative_mass
	is_uncapped = { always = yes }

	prerequisites = {
		tech_nm_utilization_2
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
	}

	show_on_uncolonized = {
		exists = from
		from = {
			has_technology = tech_nm_utilization_2
		}
		uses_district_set = giga_frameworld
	}

	potential = {
		exists = owner
		owner = {
			has_technology = tech_nm_utilization_2
		}
		uses_district_set = giga_frameworld
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @b4_minerals
			exotic_gases = @b3_rare_cost
			rare_crystals = @b3_rare_cost
		}
		upkeep = {
			energy = @b3_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		modifier = {
			job_ehof_energy_converter_add = @b2_jobs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		modifier = {
			job_ehof_energy_converter_drone_add = @b2_jobs
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		text = job_ehof_energy_converter_effect_desc
	}
	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		text = job_ehof_energy_converter_drone_effect_desc
	}

	ai_weight_coefficient = 27
	additional_ai_weight = 8429
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { has_monthly_income = { resource = energy value < 500 } } }
	}

	ai_resource_production = {
		energy = 8
		giga_sr_negative_mass = 2
	}
}

# object = district:district_rw_nexus; source = Stellaris vanilla::common\districts\04_ringworld_districts.txt
# staid_dataset_job_pressure = family:energy_scaling jobs:200.0 roi2250:1450800.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_rw_nexus = {
	base_buildtime = @rw_district_buildtime

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = { is_machine_empire = yes }
		uses_district_set = ring_world
	}

	potential = {
		exists = owner
		owner = { is_machine_empire = yes }
		uses_district_set = ring_world
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	conversion_ratio = 0.5
	convert_to = {
		district_rw_hive
		district_rw_city
		district_mindlink
		district_ark_city
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @rw_cost
		}
		upkeep = {
			energy = @rw_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 2500
		job_technician_drone_add = @base_district_jobs
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_1 }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_2 }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_optimized_nexus }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	triggered_desc = {
		trigger = {
			planet = {
				has_deposit = d_arcane_generator
				NOT = { has_district = district_rw_nexus }
			}
		}
		text = arcane_generator_upkeep_desc
	}

	inline_script = {
		script = districts/district_triggered_name_machine
	}
	ai_weight_coefficient = 25
	additional_ai_weight = 3448
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { has_monthly_income = { resource = energy value < 500 } } }
	}

	ai_resource_production = {
		energy = 2
	}
}

# object = district:district_photosynthesis_fields; source = Stellaris vanilla::common\districts\05_wilderness_districts.txt
# staid_dataset_job_pressure = family:energy_scaling jobs:200.0 roi2250:1448295.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|uses_inline_script
district_photosynthesis_fields = {
	expansion_planner = yes
	base_buildtime = @wilderness_district_build_short
	overlay_icon = GFX_district_energy
	shared_capacity_modifier = district_generator
	is_uncapped = {
		is_wilderness_generator_district_uncapped = yes
	}

	min_for_deposits_on_planet = 3
	max_for_deposits_on_planet = 15

	zone_slots = {
		slot_energy
	}

	show_on_uncolonized = {
		uses_district_set = standard
		exists = from
		from = {
			is_wilderness_empire = yes
		}
	}

	potential = {
		uses_district_set = standard
		exists = owner
		owner = {
			is_wilderness_empire = yes
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_generator
		district_nexus_1
		district_hive_1
	}
	expansion_planner_type = district_generator

	resources = {
		category = planet_districts_generator
		cost = {
			minerals = 300
		}
		cost = {
			biomass = @biomass_cost
		}
		upkeep = {
			energy = 1
		}
	}
	planet_modifier = {
		job_technician_drone_add = @base_rural_district_jobs
		planet_housing_add = 100
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_tradition = tr_prosperity_public_works
			}
		}
		planet_housing_add = 50
	}

	inline_script = {
		script = buildings/on_all_wilderness_buildings_districts
	}

	prerequisites = {
		tech_power_plant_1
	}

	show_tech_unlock_if = {
		is_wilderness_empire = yes
	}


	ai_estimate_without_unemployment = yes
	additional_ai_weight = 3448
	ai_weight_coefficient = 25
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { has_monthly_income = { resource = energy value < 500 } } }
	}

	ai_resource_production = {
		energy = 5
	}
}

# object = district:district_giga_frameworld_maginot_shield_generators; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:energy_scaling jobs:200.0 roi2250:1426750.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep
district_giga_frameworld_maginot_shield_generators = {
	base_buildtime = @mega_time
	icon = district_maginot_world_shield_generators

	show_on_uncolonized = {
		has_carrier_flag = frameworld_maginot
		uses_district_set = giga_frameworld
	}

	potential = {
		has_carrier_flag = frameworld_maginot
		uses_district_set = giga_frameworld
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @maginot_district_cost_minerals
			alloys = @maginot_district_cost_alloys_medium
			exotic_gases = @maginot_district_cost_sr
		}
		upkeep = {
			energy = @maginot_district_upkeep_energy_shields
			exotic_gases = @maginot_district_upkeep_sr
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_maginot_shield_generator_operator_add = @maginot_special_jobs_add
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		modifier = {
			job_maginot_shield_generator_operator_gestalt_add = @maginot_special_jobs_add
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		text = job_maginot_shield_generator_operator_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		text = job_maginot_shield_generator_operator_gestalt_effect_desc
	}

	triggered_desc = {
		trigger = { exists = owner }
		text = job_maginot_planetary_shield_effect_desc
	}

	planet_modifier = {
		planet_orbital_bombardment_damage = -0.20 # yes these are spammable to 100% and beyond, intentional
		# stuff on the planet is protected by shields from damage
		army_collateral_damage_mult = -1.00
	}

	triggered_desc = {
		text = district_giga_frameworld_maginot_shield_generators_cap
	}

	#on_queued = { giga_frameworld_start_maginot_shield = yes }
	#on_unqueued = { giga_frameworld_stop_maginot_shield = yes }
	#on_built = { giga_frameworld_stop_maginot_shield = yes }
	#on_destroy = { giga_frameworld_update_maginot_deposits = yes }
	ai_weight_coefficient = 25
	additional_ai_weight = 3446
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { has_monthly_income = { resource = energy value < 500 } } }
	}

	ai_resource_production = {
		energy = 2
	}
}

# object = district:district_giga_frameworld_trade; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:energy_scaling jobs:8.0 roi2250:70200.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_frameworld_trade = {
	base_buildtime = @advanced_time
	icon = district_hab_commercial
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		exists = from
		from = {
			is_gestalt = no
			has_technology = "tech_interstellar_economics"
		}
		uses_district_set = giga_frameworld
	}

	potential = {
		exists = owner
		owner = {
			is_gestalt = no
			has_technology = "tech_interstellar_economics"
		}
		uses_district_set = giga_frameworld
	}

	prerequisites = {
		tech_interstellar_economics
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
		is_gestalt = no
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_frameworld_generator
	}

	resources = {
		category = planet_districts_hab_trade
		cost = {
			minerals = @advanced_cost
			rare_crystals = @advanced_rare_cost
		}
		upkeep = {
			energy = @advanced_upkeep
			rare_crystals = @advanced_rare_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 2
		job_clerk_add = 4
		job_trader_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_active_tradition = tr_mercantile_commercial_enterprise
			}
		}
		modifier = {
			job_trader_add = 2
		}
	}

	triggered_desc = {
		text = job_clerk_effect_desc
	}

	triggered_desc = {
		text = job_trader_effect_desc
	}

	ai_weight_coefficient = 19
	additional_ai_weight = 1518
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { has_monthly_income = { resource = energy value < 500 } } }
	}

	ai_resource_production = {
		energy = 6
	}
}

# object = district:district_hollow_mountains; source = Stellaris vanilla::common\districts\05_wilderness_districts.txt
# staid_dataset_job_pressure = family:mineral_scaling jobs:200.0 roi2250:1448895.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep
district_hollow_mountains = {
	expansion_planner = yes
	base_buildtime = @wilderness_district_build_short
	shared_capacity_modifier = district_mining
	overlay_icon = GFX_district_minerals
	is_uncapped = {
		is_wilderness_mining_district_uncapped = yes
	}

	min_for_deposits_on_planet = 1
	max_for_deposits_on_planet = 15

	zone_slots = {
		slot_minerals
	}

	show_on_uncolonized = {
		uses_district_set = standard
		exists = from
		from = {
			is_wilderness_empire = yes
		}
	}

	potential = {
		uses_district_set = standard
		exists = owner
		owner = {
			is_wilderness_empire = yes
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_mining
		district_nexus_2
		district_hive_2
	}
	expansion_planner_type = district_mining

	resources = {
		category = planet_districts_mining
		cost = {
			minerals = 300
		}
		cost = {
			biomass = @biomass_cost
		}
		upkeep = {
			food = 1
		}
	}

	planet_modifier = {
		job_mining_drone_add = @base_rural_district_jobs
		planet_housing_add = 100
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_tradition = tr_prosperity_public_works
			}
		}
		planet_housing_add = 50
	}

	prerequisites = {
		tech_mechanized_mining
	}

	show_tech_unlock_if = {
		is_wilderness_empire = yes
	}


	ai_estimate_without_unemployment = yes
	additional_ai_weight = 3448
	ai_weight_coefficient = 25
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 8 owner = { has_monthly_income = { resource = minerals value < 500 } } }
	}

	ai_resource_production = {
		minerals = 5
	}
}

# object = district:district_maginot_ringworld_barracks; source = Gigastructural Engineering & More (4.4)::common\districts\giga_maginot_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:15300.0 roi2250:110169680.0 flags:ai_weight_zero_or_gated_zero|has_build_cost|has_jobs|has_upkeep
district_maginot_ringworld_barracks = {
	base_buildtime = @maginot_district_buildtime_ringworld
	is_uncapped = { always = yes }
    icon = district_maginot_world_barracks
	district_background = district_city
	gridbox = district_city
	exempt_from_ai_planet_specialization = yes
    overlay_icon = GFX_district_government

	show_on_uncolonized = {
		uses_district_set = maginot_ringworld_districts
	}

	potential = {
		uses_district_set = maginot_ringworld_districts
	}

	allow = {
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @maginot_district_cost_minerals_ringworld
			alloys = @maginot_district_cost_alloys_cheap_ringworld
			rare_crystals = @maginot_district_cost_sr_ringworld
		}
		upkeep = {
			energy = @maginot_district_upkeep_energy_barracks_ringworld
			rare_crystals = @maginot_district_upkeep_sr_ringworld
		}
	}

	on_built = {
		maginot_check_upgrade_points = yes
	}

	zone_slots = {
		slot_city_government
		slot_maginot_barracks_01
		slot_maginot_barracks_02
	}
	# base jobs

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		modifier = {
			job_entertainer_add = @maginot_entertainer_filler_jobs_add_ringworld
			job_clerk_add = @maginot_entertainer_filler_jobs_add_ringworld
			job_maginot_military_police_add = @maginot_barracks_police_jobs_add_ringworld
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				owner = { is_hive_empire = yes }
			}
		}
		modifier = {
			job_synapse_drone_add = @maginot_entertainer_filler_jobs_add_ringworld
			job_maintenance_drone_add = @maginot_entertainer_filler_jobs_add_ringworld
			job_patrol_drone_add = @maginot_barracks_police_jobs_add_ringworld
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				owner = { is_machine_empire = yes }
			}
		}
		modifier = {
			job_coordinator_add = @maginot_entertainer_filler_jobs_add_ringworld
			job_maintenance_drone_add = @maginot_entertainer_filler_jobs_add_ringworld
			job_patrol_drone_add = @maginot_barracks_police_jobs_add_ringworld
		}
	}

	# extra jobs from tradition/tech

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				is_gestalt = yes
			}
		}
		modifier = {
			job_maintenance_drone_add = @maginot_entertainer_filler_jobs_buff_ringworld
		}
	}


	# planet housing and additions

	planet_modifier = {
		planet_housing_add = @maginot_district_housing_barracks_ringworld
		planet_amenities_add = @maginot_district_amenities_barracks_ringworld
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = @maginot_district_housing_buffs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = @maginot_district_housing_buffs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = @maginot_district_housing_buffs
		}
	}

	# AI weight

	ai_weight = {
		weight = 0
		modifier = {
			weight = 500
			free_housing < 5
		}
		modifier = {
			weight = 500
			free_amenities < 5
		}
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}
	ai_weight_coefficient = 32
	additional_ai_weight = 15000

	ai_resource_production = {
		energy = 153
		minerals = 153
	}
}

# object = district:district_rw_science; source = Stellaris vanilla::common\districts\04_ringworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:12000.0 roi2250:86425200.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_rw_science = {
	base_buildtime = @rw_district_buildtime


	zone_slots = {
		slot_city_01
	}

	show_on_uncolonized = {
		always = no
	}

	potential = {
		always = no
	}

	prerequisites = {
		tech_basic_science_lab_1
	}

	show_tech_unlock_if = {
		always = no
	}

	allow = {
		hidden_trigger = {
			OR = {
				NOT = { exists = owner }
				owner = {
					has_technology = tech_basic_science_lab_1
				}
			}
		}
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @rw_cost
			exotic_gases = @rw_cost_sr
		}
		upkeep = {
			energy = @rw_maintenance
			exotic_gases = @rw_maintenance_sr
		}
	}

	triggered_planet_modifier = {
		planet_housing_add = 1000
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_regular_empire = yes }
		}
		modifier = {
			job_physicist_add = 1000
			job_biologist_add = 1000
			job_engineer_add = 1000
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 1000
			job_calculator_biologist_add = 1000
			job_calculator_engineer_add = 1000
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_calculator_physicist_add = 1000
			job_calculator_biologist_add = 1000
			job_calculator_engineer_add = 1000
		}
	}

	#Jobs from Virtuality ascension

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_regular_empire = yes
				has_active_tradition = tr_virtuality_4
			}
		}
		job_physicist_add = 500
		job_biologist_add = 500
		job_engineer_add = 500
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_machine_empire = yes
				has_active_tradition = tr_virtuality_4
			}
		}
		job_calculator_physicist_add = 500
		job_calculator_biologist_add = 500
		job_calculator_engineer_add = 500
	}

	triggered_desc = {
		trigger = {
			planet = {
				has_deposit = d_arcane_generator
				NOT = { has_district = district_rw_science }
			}
		}
		text = arcane_generator_upkeep_desc
	}
	ai_weight_coefficient = 32
	additional_ai_weight = 15000
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 120
		minerals = 120
	}
}

# object = district:district_rw_farming; source = Stellaris vanilla::common\districts\04_ringworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:4500.0 roi2250:32414400.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_rw_farming = {
	base_buildtime = @rw_district_buildtime


	zone_slots = {
		slot_food
	}

	show_on_uncolonized = {
		always = no
	}

	potential = {
		always = no
	}

	convert_to = {
		district_ark_basic
	}

	resources = {
		category = planet_districts_rw_farming
		cost = {
			minerals = @rw_cost
			volatile_motes = @rw_cost_sr
		}
		upkeep = {
			energy = @rw_maintenance
			volatile_motes = @rw_maintenance_sr
		}
	}

	# triggered for tooltip formatting purposes
	triggered_planet_modifier = {
		modifier = {
			planet_housing_add = 1000
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_hive_empire = yes }
		}
		modifier = {
			planet_housing_add = 500
			job_agri_drone_add = 1500
		}
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_machine_empire = yes }
		}
		modifier = {
			job_agri_drone_add = 1000
		}
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
				is_fallen_empire_spiritualist = no
			}
		}
		modifier = {
			job_farmer_add = 1000
		}
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_fallen_empire_spiritualist = yes }
		}
		modifier = {
			job_fe_acolyte_farm_add = 1000
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_agrarian_idyll
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}
	ai_weight_coefficient = 30
	additional_ai_weight = 15000
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 45
		minerals = 45
	}
}

# object = district:district_maginot_ringworld_bunkers; source = Gigastructural Engineering & More (4.4)::common\districts\giga_maginot_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:3000.0 roi2250:21604700.0 flags:has_build_cost|has_jobs|has_upkeep|uses_inline_script
district_maginot_ringworld_bunkers = {
	base_buildtime = @maginot_district_buildtime_ringworld
    icon = district_maginot_world_bunkers
	is_uncapped = { always = yes }
    overlay_icon = GFX_district_fortress
	gridbox = district_arcology_fortress
	district_background = district_arcology_fortress

	show_on_uncolonized = {
		uses_district_set = maginot_ringworld_districts
	}

	allow = {
	}

	potential = {
		uses_district_set = maginot_ringworld_districts
		NOT = { is_planet_class = pc_giga_maginot_gas_giant }
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @maginot_district_cost_minerals_ringworld
			alloys = @maginot_district_cost_alloys_medium_ringworld
			volatile_motes = @maginot_district_cost_sr_ringworld
		}
		upkeep = {
			energy = @maginot_district_upkeep_energy_medium_ringworld
			volatile_motes = @maginot_district_upkeep_sr_ringworld
		}
	}

	on_built = {
		maginot_check_upgrade_points = yes
	}

	zone_slots = {
		slot_maginot_bunker_complexes
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_maginot_bunker_officer_add = @maginot_special_jobs_add_ringworld
			job_soldier_add = @maginot_bunker_police_jobs_add_ringworld
			job_maginot_military_police_add = @maginot_bunker_police_jobs_add_ringworld
		}
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		modifier = {
			job_maginot_bunker_officer_gestalt_add = @maginot_special_jobs_add_ringworld
			job_warrior_drone_add = @maginot_bunker_police_jobs_add_ringworld
			job_patrol_drone_add = @maginot_bunker_police_jobs_add_ringworld
		}
	}

	planet_modifier = {
		planet_housing_add = @maginot_district_housing_bunkers_ringworld
	}

	triggered_desc = {
		trigger = { exists = owner }
		text = job_maginot_planetary_bunker_effect_desc
	}

	inline_script = {
		script = districts/maginot/maginot_triggered_names_bunkers
	}

	ai_weight = {
		weight = 33
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}
	ai_weight_coefficient = 29
	additional_ai_weight = 15000

	ai_resource_production = {
		energy = 30
		minerals = 30
	}
}

# object = district:district_rw_commercial; source = Stellaris vanilla::common\districts\04_ringworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:2600.0 roi2250:18734400.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_rw_commercial = {
	base_buildtime = @rw_district_buildtime


	zone_slots = {
		slot_city_04
	}

	show_on_uncolonized = {
		always = no
	}

	potential = {
		always = no
	}

	convert_to = {
		district_rw_generator
		district_ark_generator
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @rw_cost
			rare_crystals = @rw_cost_sr
		}
		upkeep = {
			energy = @rw_maintenance
			rare_crystals = @rw_maintenance_sr
		}
	}

	triggered_planet_modifier = {
		planet_housing_add = 1000
		job_trader_add = @base_district_jobs
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = no
			}
		}
		modifier = {
			job_clerk_add = 600
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 600
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_active_tradition = tr_mercantile_commercial_enterprise
			}
		}
		modifier = {
			job_trader_add = @base_district_jobs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_active_tradition = tr_virtuality_4
				is_tankbound_empire = no
			}
		}
		modifier = {
			job_clerk_add = 600
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_active_tradition = tr_virtuality_4
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 600
		}
	}

	triggered_desc = {
		trigger = {
			planet = {
				has_deposit = d_arcane_generator
				NOT = { has_district = district_rw_commercial }
			}
		}
		text = arcane_generator_upkeep_desc
	}
	ai_weight_coefficient = 29
	additional_ai_weight = 15000
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 26
		minerals = 26
	}
}

# object = district:district_rw_city; source = Stellaris vanilla::common\districts\04_ringworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:1900.0 roi2250:13690800.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_rw_city = {
	base_buildtime = @rw_district_buildtime

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = { is_gestalt = no }
		uses_district_set = ring_world
	}

	potential = {
		exists = owner
		owner = { is_gestalt = no }
		uses_district_set = ring_world
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	conversion_ratio = 0.5
	convert_to = {
		district_rw_nexus
		district_rw_hive
		district_mindlink
		district_ark_city
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @rw_cost
		}
		upkeep = {
			energy = @rw_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 2500
	}

	inline_script = {
		script = jobs/enforcers_add
		AMOUNT = @base_district_jobs
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_regular_empire = yes
				is_fallen_empire = no
				is_tankbound_empire = no
			}
		}
		modifier = {
			job_clerk_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_regular_empire = yes
				is_fallen_empire = no
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_regular_empire = yes
				is_fallen_empire = no
				has_active_tradition = tr_virtuality_4
				is_tankbound_empire = no
			}
		}
		modifier = {
			job_clerk_add = 600
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_regular_empire = yes
				is_fallen_empire = no
				has_active_tradition = tr_virtuality_4
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 600
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	triggered_desc = {
		trigger = {
			planet = {
				has_deposit = d_arcane_generator
				NOT = { has_district = district_rw_city }
			}
		}
		text = arcane_generator_upkeep_desc
	}

	inline_script = {
		script = districts/district_triggered_name_urban
	}
	ai_weight_coefficient = 29
	additional_ai_weight = 15000
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 19
		minerals = 19
	}
}

# object = district:district_maginot_world_barracks; source = Gigastructural Engineering & More (4.4)::common\districts\giga_maginot_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:1800.0 roi2250:12983440.0 flags:ai_weight_zero_or_gated_zero|has_build_cost|has_jobs|has_upkeep
district_maginot_world_barracks = {
	base_buildtime = @maginot_district_buildtime
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes
	district_background = district_city
	gridbox = district_city
    overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_maginot_barracks_01
		slot_maginot_barracks_02
	}

	conversion_ratio = 1
	convert_to = {
		district_maginot_world_barracks_wilderness
	}

	show_on_uncolonized = {
		uses_district_set = maginot_world_districts
		exists = from
		from = { is_wilderness_empire = no }
	}

	potential = {
		uses_district_set = maginot_world_districts
		exists = owner
		owner = { is_wilderness_empire = no }
	}

	allow = {
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @maginot_district_cost_minerals
			alloys = @maginot_district_cost_alloys_cheap
			rare_crystals = @maginot_district_cost_sr
		}
		upkeep = {
			energy = @maginot_district_upkeep_energy_barracks
			rare_crystals = @maginot_district_upkeep_sr
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		modifier = {
			job_entertainer_add = @maginot_entertainer_filler_jobs_add
			job_maginot_military_police_add = @maginot_barracks_police_jobs_add
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		modifier = {
			job_coordinator_add = @maginot_entertainer_filler_jobs_add
			job_patrol_drone_add = @maginot_barracks_police_jobs_add
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_active_tradition = tr_virtuality_4
			}
		}
		modifier = {
			job_coordinator_add = 200
		}
	}

	# extra jobs from tradition/tech
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				is_gestalt = yes
			}
		}
		modifier = {
			job_maintenance_drone_add = @maginot_entertainer_filler_jobs_buff #mostly obsolete but helps virtuality
		}
	}

	# Bug Branch
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_bugged_rooftop_farmers = yes }
		}
		modifier = {
			job_clerk_add = -100
			job_farmer_add = 100
		}
	}


	# planet housing and additions

	planet_modifier = {
		planet_housing_add = @maginot_district_housing_barracks
		planet_amenities_add = @maginot_district_amenities_barracks
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = @maginot_district_housing_buffs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = @maginot_district_housing_buffs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = @maginot_district_housing_buffs
		}
	}

	# AI weight

	ai_weight = {
		weight = 0
		modifier = {
			weight = 500
			free_housing < 5
		}
		modifier = {
			weight = 500
			free_amenities < 5
		}
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}
	ai_weight_coefficient = 28
	additional_ai_weight = 15000

	ai_resource_production = {
		energy = 18
		minerals = 18
	}
}

# object = district:district_maginot_world_barracks_wilderness; source = Gigastructural Engineering & More (4.4)::common\districts\giga_maginot_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:1200.0 roi2250:8656240.0 flags:ai_weight_zero_or_gated_zero|has_build_cost|has_jobs|has_upkeep
district_maginot_world_barracks_wilderness = {
	icon = district_maginot_world_barracks
	base_buildtime = @maginot_district_buildtime
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes
	district_background = district_city
	gridbox = district_city
	zone_slots = {
		slot_city_government
		slot_maginot_barracks_01
		slot_maginot_barracks_02
	}

	conversion_ratio = 1
	convert_to = {
		district_maginot_world_barracks
	}

	show_on_uncolonized = {
		uses_district_set = maginot_world_districts
		exists = from
		from = { is_wilderness_empire = yes }
	}

	potential = {
		uses_district_set = maginot_world_districts
		exists = owner
		owner = { is_wilderness_empire = yes }
	}

	allow = {
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @maginot_district_cost_minerals
			alloys = @maginot_district_cost_alloys_cheap
			rare_crystals = @maginot_district_cost_sr
		}
		upkeep = {
			energy = @maginot_district_upkeep_energy_barracks
			rare_crystals = @maginot_district_upkeep_sr
		}
	}

	triggered_planet_modifier = {
		potential = {
			always = yes
		}
		modifier = {
			job_coordinator_add = @maginot_entertainer_filler_jobs_add
			job_patrol_drone_add = @maginot_barracks_police_jobs_add
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_active_tradition = tr_virtuality_4
			}
		}
		modifier = {
			job_coordinator_add = 200
		}
	}

	# extra jobs from tradition/tech
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				is_gestalt = yes
			}
		}
		modifier = {
			job_maintenance_drone_add = @maginot_entertainer_filler_jobs_buff #mostly obsolete but helps virtuality
		}
	}

	# Bug Branch
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_bugged_rooftop_farmers = yes }
		}
		modifier = {
			job_clerk_add = -100
			job_farmer_add = 100
		}
	}


	# planet housing and additions

	planet_modifier = {
		planet_housing_add = @maginot_district_housing_barracks
		planet_amenities_add = @maginot_district_amenities_barracks
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = @maginot_district_housing_buffs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = @maginot_district_housing_buffs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = @maginot_district_housing_buffs
		}
	}

	# AI weight

	ai_weight = {
		weight = 0
		modifier = {
			weight = 500
			free_housing < 5
		}
		modifier = {
			weight = 500
			free_amenities < 5
		}
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}
	ai_weight_coefficient = 28
	additional_ai_weight = 11681

	ai_resource_production = {
		energy = 12
		minerals = 12
	}
}

# object = district:district_giga_frameworld_sentient_metal; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:800.0 roi2250:5863100.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep
district_giga_frameworld_sentient_metal = {
	base_buildtime = @advanced_time
	icon = district_giga_sentient_metal
	is_uncapped = { always = yes }

	prerequisites = {
		tech_ehof_sentient_tier_3
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
	}

	show_on_uncolonized = {
		exists = from
		from = {
			has_technology = tech_ehof_sentient_tier_3
		}
		uses_district_set = giga_frameworld
	}

	potential = {
		exists = owner
		owner = {
			has_technology = tech_ehof_sentient_tier_3
		}
		uses_district_set = giga_frameworld
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @b4_minerals
		}
		upkeep = {
			energy = @b4_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		modifier = {
			job_ehof_cultivator_add = @b2_jobs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		modifier = {
			job_ehof_cultivation_drone_add = @b2_jobs
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		text = job_ehof_cultivator_effect_desc
	}
	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		text = job_ehof_cultivation_drone_effect_desc
	}

	ai_weight_coefficient = 27
	additional_ai_weight = 8430
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 8
		giga_sr_sentient_metal = 8
		minerals = 8
	}
}

# object = district:district_maginot_world_bunkers; source = Gigastructural Engineering & More (4.4)::common\districts\giga_maginot_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:600.0 roi2250:4337350.0 flags:has_build_cost|has_jobs|has_upkeep|uses_inline_script
district_maginot_world_bunkers = {
	base_buildtime = @maginot_district_buildtime
	is_uncapped = { always = yes }
    overlay_icon = GFX_district_fortress
	gridbox = district_arcology_fortress
	district_background = district_arcology_fortress
	show_on_uncolonized = {
		uses_district_set = maginot_world_districts
		NOT = { is_planet_class = pc_giga_maginot_gas_giant }
		exists = from
		from = { is_wilderness_empire = no }
	}
	zone_slots = {
		slot_maginot_bunker_complexes
	}

	conversion_ratio = 1
	convert_to = {
		district_maginot_world_bunkers_wilderness
	}

	allow = {
	}

	potential = {
		uses_district_set = maginot_world_districts
		NOT = { is_planet_class = pc_giga_maginot_gas_giant }
		exists = owner
		owner = { is_wilderness_empire = no }
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @maginot_district_cost_minerals
			alloys = @maginot_district_cost_alloys_medium
			volatile_motes = @maginot_district_cost_sr
		}
		upkeep = {
			energy = @maginot_district_upkeep_energy_medium
			volatile_motes = @maginot_district_upkeep_sr
		}
	}

	on_built = {
		maginot_check_upgrade_points = yes
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_maginot_bunker_officer_add = @maginot_special_jobs_add
			job_soldier_add = @maginot_bunker_police_jobs_add
			job_maginot_military_police_add = @maginot_bunker_police_jobs_add
		}
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		modifier = {
			job_maginot_bunker_officer_gestalt_add = @maginot_special_jobs_add
			job_warrior_drone_add = @maginot_bunker_police_jobs_add
			job_patrol_drone_add = @maginot_bunker_police_jobs_add
		}
	}

	planet_modifier = {
		planet_housing_add = @maginot_district_housing_bunkers
	}

	triggered_desc = {
		trigger = { exists = owner }
		text = job_maginot_planetary_bunker_effect_desc
	}

	inline_script = {
		script = districts/maginot/maginot_triggered_names_bunkers
	}

	ai_weight = {
		weight = 33
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}
	ai_weight_coefficient = 27
	additional_ai_weight = 6791

	ai_resource_production = {
		energy = 6
		minerals = 6
	}
}

# object = district:district_resort; source = Planetary Diversity - More Arcologies::common\districts\00_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:500.0 roi2250:3609600.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack|unresolved_variables
district_resort = {
	base_buildtime = 480

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_trade

	zone_slots = {
		slot_city_government
		slot_resort_01
		slot_resort_02
	}

	show_on_uncolonized = {
		exists = from
		from = { is_regular_empire = yes }
		has_modifier = resort_colony
	}

	potential = {
		exists = owner
		owner = { is_regular_empire = yes }
		has_modifier = resort_colony
	}

	allow = {
		hidden_trigger = {
			NOT = { has_modifier = slave_colony }
		}
		custom_tooltip = {
			fail_text = arcology_project_construction_fail_tt
			NOT = { has_carrier_flag = arcology_project_construction }
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_city
		district_arcology_housing
		district_rw_city
		district_nexus
		district_hive
		district_craglands
		district_mindlink
		district_crashed_slaver_ship
		district_prison
	}

	resources = {
		category = planet_districts_cities
		cost = {
			minerals = @city_cost
			trigger = {
				NOT = { has_modifier = wooden_planet }
			}
		}
		cost = {
			food = @city_cost
			trigger = {
				has_modifier = wooden_planet
			}
		}
		upkeep = {
			energy = 2
			trigger = {
				NOT = { has_modifier = wooden_planet }
			}
		}
		upkeep = {
			food = 2
			trigger = {
				has_modifier = wooden_planet
			}
		}
	}

	planet_modifier = {
		planet_housing_add = 500
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_regular_empire = yes
			}
		}
		modifier = {
			job_resort_worker_add = @special_district_jobs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_regular_empire = yes
			}
		}
		modifier = {
			job_resort_worker_add = @base_district_jobs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	triggered_name = {
		text = resort_default
	}

	triggered_flavor_desc = {
		text = district_resort_desc
	}
	ai_weight_coefficient = 26
	additional_ai_weight = 5967
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 5
		minerals = 5
	}
}

# object = district:district_crashed_slaver_ship; source = Planetary Diversity - More Arcologies::common\districts\00_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:400.0 roi2250:2893800.0 flags:ai_weight_absent|has_jobs|has_upkeep|overridden_in_stack
district_crashed_slaver_ship = {
	shared_capacity_modifier = district_crashed_slaver_ship
	is_uncapped = {	always = no }
	can_demolish = no
	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
	}

	show_on_uncolonized = {
		always = no
		exists = from
		from = { is_wilderness_empire = no }
	}

	potential = {
		uses_district_set = standard
		has_deposit = d_crashed_slaver_ship
		if = {
			limit = {
				exists = owner
			}
			NAND = {
				is_capital = yes
				owner = {
					has_menace_perk = menp_behemoth_mind_meld
				}
			}
			owner = { is_wilderness_empire = no }
		}
	}

	allow = {
		hidden_trigger = {
			NAND = {
				has_modifier = resort_colony
				has_modifier = slave_colony
			}
		}
		custom_tooltip = {
			fail_text = arcology_project_construction_fail_tt
			NOT = { has_carrier_flag = arcology_project_construction }
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_city
		district_arcology_housing
		district_rw_city
		district_nexus
		district_hive
		district_craglands
		district_mindlink
		district_ark_city
	}

	resources = {
		category = planet_districts_cities
		upkeep = {
			energy = 2
		}
	}

	planet_modifier = {
		planet_housing_add = 1000
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				NOT = { has_country_flag = origin_broken_shackles_crashed_slaver_ship_depleted }
			}
		}
		job_broken_shackles_scavenger_add = 100
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_country_flag = origin_broken_shackles_crashed_slaver_ship_depleted
				is_tankbound_empire = no
			}
		}
		modifier = {
			job_clerk_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_country_flag = origin_broken_shackles_crashed_slaver_ship_depleted
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}
	ai_weight_coefficient = 26
	additional_ai_weight = 5138
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 4
		minerals = 4
	}
}

# object = district:district_alderson_logistics; source = Gigastructural Engineering & More (4.4)::common\districts\giga_alderson.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:400.0 roi2250:2881900.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep
district_alderson_logistics = {
	icon = district_alderson_logistics
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_government
	#custom_gui = planet_district_entry_width_2

	zone_slots = {
		slot_city_government
		slot_district_alderson_logistics_01
		slot_district_alderson_logistics_02
	}

	show_on_uncolonized = {
		exists = from
		uses_district_set = giga_alderson
	}

	base_buildtime = 720

	potential = {
		exists = owner
		uses_district_set = giga_alderson
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	conversion_ratio = 0.5

	resources = {
		category = planet_districts
		cost = {
			minerals = @giga_alderson_cost
		}
		upkeep = {
			energy = @giga_alderson_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 2500
	}

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = {
                is_gestalt = no
            }
        }
        job_enforcer_add = @base_district_jobs
    }
    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = {
                is_gestalt = yes
            }
        }
        job_patrol_drone_add = @base_district_jobs
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = { is_tankbound_empire = yes }
        }
        modifier = {
            job_production_overseer_add = 200
        }
    }
	ai_weight_coefficient = 26
	additional_ai_weight = 5138
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 4
		minerals = 4
	}
}

# object = district:district_giga_gas_giant_habitat_exotic; source = Gigastructural Engineering & More (4.4)::common\districts\giga_gas_giant_habitat_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:300.0 roi2250:2173325.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep
district_giga_gas_giant_habitat_exotic = {
	base_buildtime = @giga_gas_giant_habitat_district_buildtime
	is_uncapped = { always = yes }
    gridbox = district_arcology_administrative
    district_background = district_arcology_administrative
    overlay_icon = GFX_district_exotic_gases

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	show_on_uncolonized = {
		uses_district_set = giga_gas_giant_habitat
		exists = from
		from = {
			is_wilderness_empire = no
		}
	}

	potential = {
		uses_district_set = giga_gas_giant_habitat
		exists = owner
		owner = {
			is_wilderness_empire = no
		}
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @giga_gas_giant_habitat_cost
		}
		upkeep = {
			energy = @giga_gas_giant_habitat_upkeep_energy_heavy
		}
	}

	zone_slots = {
        slot_gigas_gas_giant_exotic
	}

	# base stats
	planet_modifier = {
		planet_housing_add = 200
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		job_giga_gas_extraction_manager_add = 100
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		job_giga_gas_extraction_manager_drone_add = 100
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		text = job_giga_gas_extraction_manager_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = yes
			}
		}
		text = job_giga_gas_extraction_manager_drone_effect_desc
	}
	ai_weight_coefficient = 25
	additional_ai_weight = 4301
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 3
		minerals = 3
	}
}

# object = district:district_maginot_world_bunkers_wilderness; source = Gigastructural Engineering & More (4.4)::common\districts\giga_maginot_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:300.0 roi2250:2166550.0 flags:has_build_cost|has_jobs|has_upkeep|uses_inline_script
district_maginot_world_bunkers_wilderness = {
	icon = district_maginot_world_bunkers
	base_buildtime = @maginot_district_buildtime
	is_uncapped = { always = yes }
	gridbox = district_arcology_fortress
	district_background = district_arcology_fortress
	show_on_uncolonized = {
		uses_district_set = maginot_world_districts
		NOT = { is_planet_class = pc_giga_maginot_gas_giant }
		exists = from
		from = { is_wilderness_empire = yes }
	}
	zone_slots = {
		slot_maginot_bunker_complexes
	}

	conversion_ratio = 1
	convert_to = {
		district_maginot_world_bunkers
	}

	allow = {
	}

	potential = {
		uses_district_set = maginot_world_districts
		NOT = { is_planet_class = pc_giga_maginot_gas_giant }
		exists = owner
		owner = { is_wilderness_empire = yes }
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @maginot_district_cost_minerals
			alloys = @maginot_district_cost_alloys_medium
			volatile_motes = @maginot_district_cost_sr
		}
		upkeep = {
			energy = @maginot_district_upkeep_energy_medium
			volatile_motes = @maginot_district_upkeep_sr
		}
	}

	on_built = {
		maginot_check_upgrade_points = yes
	}

	triggered_planet_modifier = {
		potential = {
			always = yes
		}
		modifier = {
			job_maginot_bunker_officer_gestalt_add = @maginot_special_jobs_add
			job_warrior_drone_add = @maginot_bunker_police_jobs_add
			job_patrol_drone_add = @maginot_bunker_police_jobs_add
		}
	}

	planet_modifier = {
		planet_housing_add = @maginot_district_housing_bunkers
	}

	triggered_desc = {
		trigger = { exists = owner }
		text = job_maginot_planetary_bunker_effect_desc
	}

	inline_script = {
		script = districts/maginot/maginot_triggered_names_bunkers
	}

	ai_weight = {
		weight = 33
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}
	ai_weight_coefficient = 25
	additional_ai_weight = 4301

	ai_resource_production = {
		energy = 3
		minerals = 3
	}
}

# object = district:district_rw_hive; source = Stellaris vanilla::common\districts\04_ringworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:200.0 roi2250:1450800.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_rw_hive = {
	base_buildtime = @rw_district_buildtime

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = { is_hive_empire = yes }
		uses_district_set = ring_world
	}

	potential = {
		exists = owner
		owner = { is_hive_empire = yes }
		uses_district_set = ring_world
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	conversion_ratio = 0.5
	convert_to = {
		district_rw_nexus
		district_rw_city
		district_mindlink
		district_ark_city
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @rw_cost
		}
		upkeep = {
			energy = @rw_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 3000
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_1 }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_2 }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
		}
		modifier = {
			job_coordinator_add = @base_district_jobs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_extended_hives }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	triggered_desc = {
		trigger = {
			planet = {
				has_deposit = d_arcane_generator
				NOT = { has_district = district_rw_hive }
			}
		}
		text = arcane_generator_upkeep_desc
	}

	inline_script = {
		script = districts/district_triggered_name_hive
	}
	ai_weight_coefficient = 25
	additional_ai_weight = 3448
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 2
		minerals = 2
	}
}

# object = district:district_slave; source = Planetary Diversity - More Arcologies::common\districts\00_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:200.0 roi2250:1450200.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack|unresolved_variables
district_slave = {
	base_buildtime = 480

	exempt_from_ai_planet_specialization = yes
	icon = district_city
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = { is_regular_empire = yes }
		has_modifier = slave_colony
	}

	potential = {
		exists = owner
		owner = { is_regular_empire = yes }
		has_modifier = slave_colony
	}

	allow = {
		hidden_trigger = {
			has_modifier = slave_colony
		}
		custom_tooltip = {
			fail_text = arcology_project_construction_fail_tt
			NOT = { has_carrier_flag = arcology_project_construction }
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_arcology_housing
		district_rw_city
		district_nexus
		district_hive
		district_city
	}

	resources = {
		category = planet_districts_cities
		cost = {
			minerals = @city_cost
		}
		upkeep = {
			energy = 2
		}
	}

	planet_modifier = {
		planet_housing_add = 1000
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
				is_fallen_empire_spiritualist = no
			}
		}
		modifier = {
			job_slave_overseer_add = @base_district_jobs
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}
	ai_weight_coefficient = 25
	additional_ai_weight = 3448
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 2
		minerals = 2
	}
}

# object = district:district_orchard_forests; source = Stellaris vanilla::common\districts\05_wilderness_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:200.0 roi2250:1448295.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|uses_inline_script
district_orchard_forests = {
	expansion_planner = yes
	base_buildtime = @wilderness_district_build_short
	shared_capacity_modifier = district_farming
	overlay_icon = GFX_district_food
	is_uncapped = {
		is_wilderness_farming_district_uncapped = yes
	}

	min_for_deposits_on_planet = 3
	max_for_deposits_on_planet = 15

	zone_slots = {
		slot_food
	}

	show_on_uncolonized = {
		uses_district_set = standard
		exists = from
		from = {
			is_wilderness_empire = yes
		}
	}

	potential = {
		uses_district_set = standard
		exists = owner
		owner = {
			is_wilderness_empire = yes
		}
	}

	allow = {
		NOT = { has_modifier = resort_colony }
	}

	conversion_ratio = 1
	convert_to = {
		district_farming
		district_nexus_3
		district_hive_3
	}
	expansion_planner_type = district_farming

	resources = {
		category = planet_districts_farming
		cost = {
			minerals = 300
		}
		cost = {
			biomass = @biomass_cost
		}
		upkeep = {
			energy = 1
		}
	}

	planet_modifier = {
		job_agri_drone_add = @base_rural_district_jobs
		planet_housing_add = 100
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_tradition = tr_prosperity_public_works
			}
		}
		planet_housing_add = 50
	}

	inline_script = {
		script = buildings/on_all_wilderness_buildings_districts
	}

	prerequisites = {
		tech_industrial_farming
	}

	show_tech_unlock_if = {
		is_wilderness_empire = yes
	}


	ai_estimate_without_unemployment = yes
	additional_ai_weight = 3448
	ai_weight_coefficient = 25
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 2
		food = 5
		minerals = 2
	}
}

# object = district:district_ark_city; source = Stellaris vanilla::common\districts\07_ark_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:200.0 roi2250:1446600.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_ark_city = {
	base_buildtime = 600
	exempt_from_ai_planet_specialization = yes

	overlay_icon = GFX_district_government
	gridbox = district_city

	zone_slots = {
		slot_city_government
		slot_ark_city_01
		slot_ark_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = {
			is_nomadic = yes
		}
		uses_district_set = nomad
		is_special_colony_type = no
	}

	potential = {
		OR = {
			NOT = { exists = owner } #this condition is needed for galaxy generation
			uses_district_set = nomad
		}
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	allow = {
		uses_district_set = nomad
	}

	conversion_ratio = 1
	convert_to = {
		district_mindlink
		district_city
		district_nexus
		district_hive
		district_hab_housing
		district_arcology_housing
		district_rw_city
		district_rw_hive
		district_rw_nexus
	}

	resources = {
		category = planet_districts_cities
		cost = {
			alloys = @city_cost
		}
		upkeep = {
			energy = 2
		}
	}

	planet_modifier = {
		planet_housing_add = 2500
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works_nomads }
		}
		modifier = {
			planet_housing_add = 250
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 200
		}
	}
	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		text = job_production_overseer_effect_desc
	}

	inline_script = {
		script = districts/district_triggered_name_urban
	}

	inline_script = {
		script = districts/district_triggered_flavor_desc_urban
	}

	inline_script = {
		script = districts/ai_urban_district_extra_weighting
	}
	ai_weight_coefficient = 25
	additional_ai_weight = 3448
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 2
		minerals = 2
	}
}

# object = district:district_giga_frameworld_maginot_planetary_cannons; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:200.0 roi2250:1431950.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep
district_giga_frameworld_maginot_planetary_cannons = {
	base_buildtime = @mega_time
	icon = district_maginot_world_planetary_cannons

	show_on_uncolonized = {
		has_carrier_flag = frameworld_maginot
		uses_district_set = giga_frameworld
	}

	potential = {
		has_carrier_flag = frameworld_maginot
		uses_district_set = giga_frameworld
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @maginot_district_cost_minerals
			alloys = @maginot_district_cost_alloys_expensive
		}
		upkeep = {
			energy = @maginot_district_upkeep_energy_medium
			alloys = @maginot_district_upkeep_alloys
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_maginot_planetary_cannon_operator_add = @maginot_special_jobs_add
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		modifier = {
			job_maginot_planetary_cannon_operator_gestalt_add = @maginot_special_jobs_add
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
			}
		}
		text = job_maginot_planetary_cannon_operator_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		text = job_maginot_planetary_cannon_operator_gestalt_effect_desc
	}

	triggered_desc = {
		trigger = { exists = owner }
		text = job_maginot_planetary_artillery_effect_desc
	}

	triggered_desc = {
		text = district_giga_frameworld_maginot_planetary_cannons_cap
	}

	#on_queued = { giga_frameworld_start_maginot_gun = yes }
	#on_unqueued = {	giga_frameworld_stop_maginot_gun = yes }
	#on_built = { giga_frameworld_stop_maginot_gun = yes }
	#on_destroy = { giga_frameworld_update_maginot_deposits = yes }
	ai_weight_coefficient = 25
	additional_ai_weight = 3447
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 2
		minerals = 2
	}
}

# object = district:district_city_katzen; source = Gigastructural Engineering & More (4.4)::common\districts\00_giga_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:730800.0 flags:ai_weight_absent|has_jobs
district_city_katzen = { #For special countries
	base_buildtime = 120
    is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes

	show_on_uncolonized = {
		exists = from
		from = {
			exists = event_target:flusion_primitives_country
			is_country = event_target:flusion_primitives_country
			is_regular_empire = no
			NOT = { is_country_type = primitive }
		}
		nor = {
			is_planet_class = pc_flusion_gaia_ecu
			uses_district_set = flusion_gaia_ecu
		}
	}

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	potential = {
		exists = owner
		owner = {
			exists = event_target:flusion_primitives_country
			is_country = event_target:flusion_primitives_country
			is_regular_empire = no
			NOT = { is_country_type = primitive }
		}
		nor = {
			is_planet_class = pc_flusion_gaia_ecu
			uses_district_set = flusion_gaia_ecu
		}
	}

	resources = {
		category = planet_districts_cities
	}

	conversion_ratio = 1
	convert_to = {
		district_flusion_city
		district_city
		district_nexus
		district_hive
	}

	triggered_planet_modifier = {
		potential = {
			always = yes
		}
		planet_housing_add = 600
		planet_amenities_add = 1000
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2559
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_rw_urban_3; source = Stellaris vanilla::common\districts\04_ringworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:727200.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_rw_urban_3 = {
	icon = district_rw_city_secondary
	base_buildtime = @rw_district_buildtime

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_housing

	zone_slots = {
		slot_rw_urban_03
	}

	convert_to = {
		district_ark_basic
	}

	show_on_uncolonized = {
		exists = from
		uses_district_set = ring_world
	}

	potential = {
		exists = owner
		uses_district_set = ring_world
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @rw_cost
		}
		upkeep = {
			energy = @rw_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 2500
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = yes
			}
		}
		job_production_overseer_add = 100
	}

	triggered_desc = {
		trigger = {
			planet = {
				has_deposit = d_arcane_generator
				NOT = { has_district = district_rw_city }
			}
		}
		text = arcane_generator_upkeep_desc
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_rw_urban_2; source = Stellaris vanilla::common\districts\04_ringworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:727200.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_rw_urban_2 = {
	icon = district_rw_city_secondary
	base_buildtime = @rw_district_buildtime

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_housing

	zone_slots = {
		slot_rw_urban_02
	}

	convert_to = {
		district_ark_military
	}

	show_on_uncolonized = {
		exists = from
		uses_district_set = ring_world
	}

	potential = {
		exists = owner
		uses_district_set = ring_world
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @rw_cost
		}
		upkeep = {
			energy = @rw_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 2500
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = yes
			}
		}
		job_production_overseer_add = 100
	}

	triggered_desc = {
		trigger = {
			planet = {
				has_deposit = d_arcane_generator
				NOT = { has_district = district_rw_city }
			}
		}
		text = arcane_generator_upkeep_desc
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_rw_urban_1; source = Stellaris vanilla::common\districts\04_ringworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:727200.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_rw_urban_1 = {
	icon = district_rw_city_secondary
	base_buildtime = @rw_district_buildtime

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_housing

	zone_slots = {
		slot_rw_urban_01
	}

	convert_to = {
		district_ark_generator
	}

	show_on_uncolonized = {
		exists = from
		uses_district_set = ring_world
	}

	potential = {
		exists = owner
		uses_district_set = ring_world
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @rw_cost
		}
		upkeep = {
			energy = @rw_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 2500
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 500
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = yes
			}
		}
		job_production_overseer_add = 100
	}

	triggered_desc = {
		trigger = {
			planet = {
				has_deposit = d_arcane_generator
				NOT = { has_district = district_rw_city }
			}
		}
		text = arcane_generator_upkeep_desc
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_hab_housing; source = Stellaris vanilla::common\districts\03_habitat_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:727200.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_hab_housing = {
	base_buildtime = @hab_time

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_habitat_01
		slot_habitat_02
	}

	show_on_uncolonized = {
		uses_district_set = habitat
	}

	potential = {
		uses_district_set = habitat
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	convert_to = {
		district_mindlink
		district_ark_city
	}

	resources = {
		category = planet_districts_hab
		cost = {
			alloys = @hab_cost
		}
		upkeep = {
			energy = @hab_maintenance
			alloys = @low_hab_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 1000
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_void_works }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 100
		}
		mult = owner.value:hab_void_dweller_jobs
	}

	inline_script = {
		script = districts/ai_urban_district_extra_weighting
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_prison; source = Planetary Diversity - More Arcologies::common\districts\00_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:726600.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack|unresolved_variables|uses_inline_script
district_prison = {
	base_buildtime = 480

	exempt_from_ai_planet_specialization = yes
	icon = district_city
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = { is_regular_empire = yes }
		has_modifier = penal_colony
	}

	potential = {
		exists = owner
		owner = { is_regular_empire = yes }
		has_modifier = penal_colony
	}

	allow = {
		hidden_trigger = {
			has_modifier = penal_colony
		}
		custom_tooltip = {
			fail_text = arcology_project_construction_fail_tt
			NOT = { has_carrier_flag = arcology_project_construction }
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_city
		district_arcology_housing
		district_rw_city
		district_nexus
		district_hive
	}

	resources = {
		category = planet_districts_cities
		cost = {
			minerals = @city_cost
		}
		upkeep = {
			energy = 2
		}
	}

	planet_modifier = {
		planet_housing_add = 300
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 200
		}
	}

	inline_script = {
		script = jobs/enforcers_add
		AMOUNT = @base_district_jobs
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_nexus; source = Planetary Diversity - More Arcologies::common\districts\00_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:726600.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack|unresolved_variables|uses_inline_script
district_nexus = {
	base_buildtime = 480

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = {
			is_machine_empire = yes
		}
		OR = {
			uses_district_set = standard
			uses_district_set = volcanic_world
			uses_district_set = hive_world
			uses_district_set = machine_world
			uses_district_set = shattered_ring_world
		}
	}

	potential = {
		exists = owner
		owner = {
			is_machine_empire = yes
		}
		OR = {
			uses_district_set = standard
			uses_district_set = volcanic_world
			uses_district_set = hive_world
			uses_district_set = machine_world
			uses_district_set = shattered_ring_world
		}
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	allow = {
		hidden_trigger = {
			NOT = { has_modifier = resort_colony }
		}
		custom_tooltip = {
			fail_text = arcology_project_construction_fail_tt
			NOT = { has_carrier_flag = arcology_project_construction }
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_arcology_housing
		district_rw_nexus
		district_city
		district_hive
		district_craglands
		district_mindlink
		district_ark_city
	}

	resources = {
		category = planet_districts_cities
		cost = {
			minerals = @city_cost
		}
		upkeep = {
			energy = 2
		}
	}

	planet_modifier = {
		planet_housing_add = 1100
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_1 }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_2 }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_optimized_nexus }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	inline_script = {
		script = districts/district_triggered_name_machine
	}

	inline_script = {
		script = districts/district_triggered_flavor_desc_machine
	}

	inline_script = {
		script = districts/ai_urban_district_extra_weighting
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_hive; source = Planetary Diversity - More Arcologies::common\districts\00_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:726600.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack|unresolved_variables|uses_inline_script
district_hive = {
	base_buildtime = 480

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = { is_hive_empire = yes }
		OR = {
			uses_district_set = standard
			uses_district_set = volcanic_world
			uses_district_set = hive_world
			uses_district_set = machine_world
			uses_district_set = shattered_ring_world
		}
		exists = from
		from = { is_wilderness_empire = no }
	}

	potential = {
		exists = owner
		owner = {
			is_hive_empire = yes
			is_wilderness_empire = no
		}
		OR = {
			uses_district_set = standard
			uses_district_set = volcanic_world
			uses_district_set = hive_world
			uses_district_set = machine_world
			uses_district_set = shattered_ring_world
		}
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	allow = {
		hidden_trigger = {
			NOT = { has_modifier = resort_colony }
		}
		custom_tooltip = {
			fail_text = arcology_project_construction_fail_tt
			NOT = { has_carrier_flag = arcology_project_construction }
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_arcology_housing
		district_rw_hive
		district_nexus
		district_city
		district_craglands
		district_mindlink
		district_ark_city
	}

	resources = {
		category = planet_districts_cities
		cost = {
			minerals = @city_cost
		}
		upkeep = {
			energy = 2
		}
	}

	planet_modifier = {
		planet_housing_add = 1200
	}

	triggered_planet_modifier = {
		potential = {
			is_planet_class = pc_hive
		}
		modifier = {
			planet_housing_add = 600
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_1 }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_2 }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_extended_hives }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	inline_script = {
		script = districts/district_triggered_name_hive
	}

	inline_script = {
		script = districts/district_triggered_flavor_desc_hive
	}

	inline_script = {
		script = districts/ai_urban_district_extra_weighting
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_battle_thrall; source = Planetary Diversity - More Arcologies::common\districts\00_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:726600.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack|unresolved_variables
district_battle_thrall = {
	base_buildtime = 480

	overlay_icon = GFX_district_fortress

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	prerequisites = {
		tech_basic_industry
	}

	show_tech_unlock_if = {
		always = no
	}

	show_on_uncolonized = {
		exists = from
		has_modifier = slave_colony
	}

	potential = {
		always = no
	}

	allow = {
		hidden_trigger = {
			has_modifier = slave_colony
		}
		custom_tooltip = {
			fail_text = arcology_project_construction_fail_tt
			NOT = { has_carrier_flag = arcology_project_construction }
		}
	}

	conversion_ratio = 1
	convert_to = {
	}

	resources = {
		category = planet_districts_industrial
		cost = {
			minerals = @city_cost
		}
		upkeep = {
			energy = 2
		}
	}

	planet_modifier = {
		planet_housing_add = 200
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
				is_fallen_empire_spiritualist = no
			}
		}
		modifier = {
			job_battle_thrall_add = @base_district_jobs
		}
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_planet_nexus; source = Gigastructural Engineering & More (4.4)::common\districts\00_giga_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:726300.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_giga_planet_nexus = {
	base_buildtime = @giga_planet_urban_district_buildtime
	icon = district_nexus
    is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes
    overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = { is_machine_empire = yes }
		giga_uses_city_district = yes
	}

	potential = {
		exists = owner
		owner = { is_machine_empire = yes }
		giga_uses_city_district = yes
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	allow = {
		NOT = { has_modifier = resort_colony }
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_planet_city
		district_giga_planet_hive
		district_giga_gas_giant_craglands
	}

	resources = {
		category = planet_districts_cities
		cost = { minerals = @city_cost }
		upkeep = {
			energy = 2 # you need immutable upkeep for triggered upkeeps to apply properly
		}
		upkeep = {
			trigger = { planet = { has_planet_flag = giga_hab_gas_giant } }
			energy = 1
		}
	}

	# vanilla district clone start
    planet_modifier = {
        planet_housing_add = 1100
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = { has_technology = tech_housing_1 }
        }
        modifier = {
            planet_housing_add = 100
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = { has_technology = tech_housing_2 }
        }
        modifier = {
            planet_housing_add = 100
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = { has_active_tradition = tr_prosperity_optimized_nexus }
        }
        modifier = {
            planet_housing_add = 100
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = { is_tankbound_empire = yes }
        }
        modifier = {
            job_production_overseer_add = 100
        }
    }

    inline_script = {
        script = districts/district_triggered_name_machine
    }

    inline_script = {
        script = districts/district_triggered_flavor_desc_machine
    }

    inline_script = {
        script = districts/ai_urban_district_extra_weighting
    }
	# vanilla district clone end
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_planet_hive; source = Gigastructural Engineering & More (4.4)::common\districts\00_giga_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:726300.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_giga_planet_hive = {
	base_buildtime = @giga_planet_urban_district_buildtime
	icon = district_hive
    is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes
    overlay_icon = GFX_district_government

	show_on_uncolonized = {
		exists = from
		from = { is_hive_empire = yes }
		giga_uses_city_district = yes
		from = { is_wilderness_empire = no }
	}

	potential = {
		exists = owner
		giga_uses_city_district = yes
		owner = {
			is_hive_empire = yes
			is_wilderness_empire = no
		}
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	allow = {
		NOT = { has_modifier = resort_colony }
	}

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_planet_city
		district_giga_planet_nexus
		district_giga_gas_giant_craglands
	}

	resources = {
		category = planet_districts_cities
		cost = { minerals = @city_cost }
		upkeep = {
			energy = 2 # you need immutable upkeep for triggered upkeeps to apply properly
		}
		upkeep = {
			trigger = { planet = { has_planet_flag = giga_hab_gas_giant } }
			energy = 1
		}
	}

	# vanilla district clone start
    planet_modifier = {
        planet_housing_add = 1200
    }

    triggered_planet_modifier = {
        potential = {
            is_planet_class = pc_hive
        }
        modifier = {
            planet_housing_add = 600
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = { has_technology = tech_housing_1 }
        }
        modifier = {
            planet_housing_add = 100
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = { has_technology = tech_housing_2 }
        }
        modifier = {
            planet_housing_add = 100
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = { has_active_tradition = tr_prosperity_extended_hives }
        }
        modifier = {
            planet_housing_add = 100
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = { is_tankbound_empire = yes }
        }
        modifier = {
            job_production_overseer_add = 100
        }
    }

    inline_script = {
        script = districts/district_triggered_name_hive
    }

    inline_script = {
        script = districts/district_triggered_flavor_desc_hive
    }

    inline_script = {
        script = districts/ai_urban_district_extra_weighting
    }
	# vanilla district clone end
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_gas_giant_habitat_exotic_wilderness; source = Gigastructural Engineering & More (4.4)::common\districts\giga_gas_giant_habitat_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:726125.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep
district_giga_gas_giant_habitat_exotic_wilderness = {
	icon = district_giga_gas_giant_habitat_exotic
	base_buildtime = @giga_gas_giant_habitat_district_buildtime
	is_uncapped = { always = yes }
    gridbox = district_arcology_administrative
    district_background = district_arcology_administrative
    overlay_icon = GFX_district_exotic_gases

	show_on_uncolonized = {
		uses_district_set = giga_gas_giant_habitat
		exists = from
		from = {
			is_wilderness_empire = yes
		}
	}

	potential = {
		uses_district_set = giga_gas_giant_habitat
		exists = owner
		owner = {
			is_wilderness_empire = yes
		}
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @giga_gas_giant_habitat_cost
		}
		upkeep = {
			energy = @giga_gas_giant_habitat_upkeep_energy_heavy
		}
	}

	zone_slots = {
        slot_gigas_gas_giant_exotic
	}

	# base stats
	planet_modifier = {
		planet_housing_add = 200
		job_giga_gas_extraction_manager_drone_add = 100
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_city; source = Planetary Diversity - More Arcologies::common\districts\00_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:726000.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack|unresolved_variables|uses_inline_script
district_city = {
	base_buildtime = 480

	exempt_from_ai_planet_specialization = yes
	default_starting_district = yes
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = {
			is_regular_empire = yes
		}
		OR = {
			uses_district_set = standard
			uses_district_set = hive_world
			uses_district_set = machine_world
			uses_district_set = shattered_ring_world
			uses_district_set = volcanic_world
		}
		is_special_colony_type = no
	}

	potential = {
		OR = {
			NOT = { exists = owner } #this condition is needed for galaxy generation
			AND = {
				exists = owner
				owner = {
					OR = {
						is_regular_empire = yes
						AND = {
							is_country_type = primitive
							is_hive_empire = no
						}
						is_country_type = mechanocalibrator
					}
				}
			}
		}
		NOT = { has_deposit = d_crashed_slaver_ship }
		OR = {
			uses_district_set = district_resort
			uses_district_set = standard
			uses_district_set = hive_world
			uses_district_set = machine_world
			uses_district_set = shattered_ring_world
			uses_district_set = volcanic_world
		}
		is_special_colony_type = no

		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	allow = {
		hidden_trigger = { is_special_colony_type = no }
		custom_tooltip = {
			fail_text = arcology_project_construction_fail_tt
			NOT = { has_carrier_flag = arcology_project_construction }
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_crashed_slaver_ship
		district_arcology_housing
		district_rw_city
		district_nexus
		district_hive
		district_prison
		district_craglands
		district_mindlink
		district_crashed_slaver_ship
		district_resort
		district_slave
		district_ark_city
		district_pd_garden_arcology_housing
		district_pd_fortress_arcology_housing
		district_pd_commercial_arcology_housing
	}

	resources = {
		category = planet_districts_cities
		cost = {
			minerals = @city_cost
			trigger = {
				NOT = { has_modifier = wooden_planet }
			}
		}
		cost = {
			food = @city_cost
			trigger = {
				has_modifier = wooden_planet
			}
		}
		upkeep = {
			energy = 2
			trigger = {
				NOT = { has_modifier = wooden_planet }
			}
		}
		upkeep = {
			food = 2
			trigger = {
				has_modifier = wooden_planet
			}
		}
	}

	planet_modifier = {
		planet_housing_add = 1000
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_agrarian_idyll
			}
		}
		modifier = {
			planet_housing_add = -200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 100
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 200
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	inline_script = {
		script = districts/district_triggered_name_urban
	}

	inline_script = {
		script = districts/district_triggered_flavor_desc_urban
	}

	inline_script = {
		script = districts/ai_urban_district_extra_weighting
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_planet_city; source = Gigastructural Engineering & More (4.4)::common\districts\00_giga_urban_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:725700.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_giga_planet_city = {
	base_buildtime = @giga_planet_urban_district_buildtime
	icon = district_city
    is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes
	default_starting_district = yes
    overlay_icon = GFX_district_government

	show_on_uncolonized = {
		exists = from
		from = { is_gestalt = no }
		giga_uses_city_district = yes
		NOT = { has_modifier = resort_colony }
	}

	potential = {
		exists = owner
		owner = { is_gestalt = no }
		giga_uses_city_district = yes
		NOT = { has_modifier = resort_colony }
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
	}

	allow = {
		NOT = { has_modifier = slave_colony }
	}

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	conversion_ratio = 1
	convert_to = {
		district_city
		district_giga_planet_hive
		district_giga_gas_giant_craglands
		district_giga_planet_nexus
	}

	# vanilla district clone start
    resources = {
        category = planet_districts_cities
        cost = {
            minerals = @city_cost
            trigger = {
                NOT = { has_modifier = wooden_planet }
            }
        }
        cost = {
            food = @city_cost
            trigger = {
                has_modifier = wooden_planet
            }
        }
        upkeep = {
            energy = 2
            trigger = {
                NOT = { has_modifier = wooden_planet }
            }
        }
        upkeep = {
            food = 2
            trigger = {
                has_modifier = wooden_planet
            }
        }
		upkeep = {
			trigger = { planet = { has_planet_flag = giga_hab_gas_giant } }
			energy = 1
		}
    }

    planet_modifier = {
        planet_housing_add = 1000
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = {
                has_valid_civic = civic_agrarian_idyll
            }
        }
        modifier = {
            planet_housing_add = -200
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = { has_active_tradition = tr_prosperity_public_works }
        }
        modifier = {
            planet_housing_add = 100
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = {
                has_technology = tech_housing_1
            }
        }
        modifier = {
            planet_housing_add = 100
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = {
                has_technology = tech_housing_2
                NOT = { has_valid_civic = civic_agrarian_idyll }
            }
        }
        modifier = {
            planet_housing_add = 200
        }
    }

    triggered_planet_modifier = {
        potential = {
            exists = owner
            owner = {
                is_tankbound_empire = yes
            }
        }
        modifier = {
            job_production_overseer_add = 100
        }
    }

    inline_script = {
        script = districts/district_triggered_name_urban
    }

    inline_script = {
        script = districts/district_triggered_flavor_desc_urban
    }

    inline_script = {
        script = districts/ai_urban_district_extra_weighting
    }
	# vanilla district clone end
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_arcology_urban_3; source = Planetary Diversity - More Arcologies::common\districts\01_arcology_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:725200.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack
district_arcology_urban_3 = {
	icon = district_arcology_housing_secondary
	base_buildtime = 600

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_housing

	zone_slots = {
		slot_arcology_urban_03
	}

	show_on_uncolonized = {
		uses_district_set = city_world
		is_pd_garden_arcology = no
		is_pd_fortress_arcology = no
		is_pd_commercial_arcology = no
	}

	potential = {
		uses_district_set = city_world
		is_pd_garden_arcology = no
		is_pd_fortress_arcology = no
		is_pd_commercial_arcology = no
	}

	conversion_ratio = 1
	convert_to = {
		district_city
		district_nexus
		district_hive
		district_ark_military
	}

	resources = {
		category = planet_districts
		cost = {
			alloys = 500
		}
		upkeep = {
			energy = 5
		}
	}

	planet_modifier = {
		planet_housing_add = 1500
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	triggered_name = {
		text = district_arcology_name
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_arcology_urban_2; source = Planetary Diversity - More Arcologies::common\districts\01_arcology_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:725200.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack
district_arcology_urban_2 = {
	icon = district_arcology_housing_secondary
	base_buildtime = 600

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_housing

	zone_slots = {
		slot_arcology_urban_02
	}

	show_on_uncolonized = {
		uses_district_set = city_world
		is_pd_garden_arcology = no
		is_pd_fortress_arcology = no
		is_pd_commercial_arcology = no
	}

	potential = {
		uses_district_set = city_world
		is_pd_garden_arcology = no
		is_pd_fortress_arcology = no
		is_pd_commercial_arcology = no
	}

	conversion_ratio = 1
	convert_to = {
		district_city
		district_nexus
		district_hive
		district_ark_basic
	}

	resources = {
		category = planet_districts
		cost = {
			alloys = 500
		}
		upkeep = {
			energy = 5
		}
	}

	planet_modifier = {
		planet_housing_add = 1500
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	triggered_name = {
		text = district_arcology_name
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_arcology_urban_1; source = Planetary Diversity - More Arcologies::common\districts\01_arcology_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:725200.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack
district_arcology_urban_1 = {
	icon = district_arcology_housing_secondary
	base_buildtime = 600

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_housing

	zone_slots = {
		slot_arcology_urban_01
	}

	show_on_uncolonized = {
		uses_district_set = city_world
		is_pd_garden_arcology = no
		is_pd_fortress_arcology = no
		is_pd_commercial_arcology = no
	}

	potential = {
		uses_district_set = city_world
		is_pd_garden_arcology = no
		is_pd_fortress_arcology = no
		is_pd_commercial_arcology = no
	}

	conversion_ratio = 1
	convert_to = {
		district_city
		district_nexus
		district_hive
		district_ark_generator
	}

	resources = {
		category = planet_districts
		cost = {
			alloys = 500
		}
		upkeep = {
			energy = 5
		}
	}

	planet_modifier = {
		planet_housing_add = 1500
	}
	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_tankbound_empire = yes }
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	triggered_name = {
		text = district_arcology_name
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_arcology_housing; source = Planetary Diversity - More Arcologies::common\districts\01_arcology_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:725200.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack
district_arcology_housing = {
	base_buildtime = 600

	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_government

	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		exists = from
		from = { is_wilderness_empire = no }
		uses_district_set = city_world
		NOR = {
			has_modifier = pd_commercial_arcology
			has_modifier = pd_garden_arcology
			has_modifier = pd_fortress_arcology
		}
	}

	potential = {
		uses_district_set = city_world
		NAND = {
			is_capital = yes
			owner = {
				has_menace_perk = menp_behemoth_mind_meld
			}
		}
		NOR = {
			has_modifier = pd_commercial_arcology
			has_modifier = pd_garden_arcology
			has_modifier = pd_fortress_arcology
		}
	}

	conversion_ratio = 1
	convert_to = {
		district_city
		district_nexus
		district_hive
		district_mindlink
		district_ark_city
		district_pd_garden_arcology_housing
		district_pd_fortress_arcology_housing
		district_pd_commercial_arcology_housing
	}

	resources = {
		category = planet_districts
		cost = {
			alloys = 500
		}
		upkeep = {
			energy = 5
		}
	}

	planet_modifier = {
		planet_housing_add = 1500
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_public_works }
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_1
			}
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_technology = tech_housing_2
				NOT = { has_valid_civic = civic_agrarian_idyll }
			}
		}
		modifier = {
			planet_housing_add = 300
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2558
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_arcology_leisure; source = Planetary Diversity - More Arcologies::common\districts\01_arcology_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:100.0 roi2250:720350.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|overridden_in_stack|uses_inline_script
district_arcology_leisure = {
	base_buildtime = 600


	zone_slots = {
		slot_city_government
		slot_city_01
		slot_city_02
	}

	show_on_uncolonized = {
		always = no
	}

	potential = {
		always = no
	}

	conversion_ratio = 1
	convert_to = {
		district_arcology_organic_housing
		district_city
		district_craglands
		district_nexus
		district_hive
		district_arcology_housing
		district_ark_city
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = 1000
			exotic_gases = 50
		}
		upkeep = {
			energy = 5
			exotic_gases = 1
		}
	}

	planet_modifier = {
		planet_housing_add = 1000
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_tankbound_empire = yes
			}
		}
		modifier = {
			job_production_overseer_add = 100
		}
	}

	inline_script = {
		script = jobs/entertainers_add
		AMOUNT = 600
	}
	ai_weight_coefficient = 23
	additional_ai_weight = 2557
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_frameworld_nexus_advanced; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:12.0 roi2250:93600.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_frameworld_nexus_advanced = {
	base_buildtime = @advanced_time
	icon = district_nexus
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes

	show_on_uncolonized = {
		from = { is_machine_empire = yes }
		uses_district_set = giga_frameworld
		has_carrier_flag = frameworld_advanced_city
	}

	potential = {
		exists = owner
		owner = { is_machine_empire = yes }
		uses_district_set = giga_frameworld
		has_carrier_flag = frameworld_advanced_city
	}

	allow = {
		#hidden_trigger = {
			exists = owner
			or = {
				owner = {
					is_ai = no
				}

				# we need more housing
				free_housing < 10

				# we might still need to unlock buildings
				num_districts = {
					type = district_giga_frameworld_nexus_advanced
					value < 5
				}

				# if we need more maintenance drones
				frameworld_needs_more_maintenance_drones = yes
			}
		#}
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_frameworld_city
		district_giga_frameworld_hive

		district_giga_frameworld_city_advanced
		district_giga_frameworld_nexus
		district_giga_frameworld_hive_advanced
	}

	resources = {
		category = planet_districts_cities
		cost = {
			minerals = @advanced_cost
		}
		upkeep = {
			energy = @advanced_upkeep
		}
	}

	triggered_planet_modifier = {
		potential = { always = yes }
		planet_housing_add = 10
		job_maintenance_drone_add = 6
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_1 }
		}
		modifier = {
			planet_housing_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_2 }
		}
		modifier = {
			planet_housing_add = 2
			job_maintenance_drone_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_virtuality_4 }
		}
		modifier = {
			job_maintenance_drone_add = 4
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_optimized_nexus }
		}
		modifier = {
			planet_housing_add = 2
		}
	}
	ai_weight_coefficient = 20
	additional_ai_weight = 1587
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_frameworld_anticrime; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:10.0 roi2250:82800.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_frameworld_anticrime = {
	base_buildtime = @advanced_time
	#icon = district_penrose_generator
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		exists = from
		from = {
			has_technology = "tech_colonial_centralization"
		}
		uses_district_set = giga_frameworld
	}

	potential = {
		exists = owner
		owner = {
			has_technology = "tech_colonial_centralization"
		}
		uses_district_set = giga_frameworld
	}

	prerequisites = {
		tech_colonial_centralization
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @advanced_cost
			volatile_motes = @advanced_rare_cost
		}
		upkeep = {
			energy = @advanced_upkeep
			volatile_motes = @advanced_rare_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_enforcer_add = 5
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		modifier = {
			job_patrol_drone_add = 5
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = no }
		}
		text = job_enforcer_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		text = job_patrol_drone_effect_desc
	}

	ai_weight_coefficient = 20
	additional_ai_weight = 1555
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_frameworld_amenities_gestalt; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:10.0 roi2250:82800.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_frameworld_amenities_gestalt = {
	base_buildtime = @advanced_time
	icon = district_arcology_leisure
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		exists = from
		from = {
			is_gestalt = yes
			has_technology = "tech_unity_of_purpose"
		}
		uses_district_set = giga_frameworld
	}

	potential = {
		exists = owner
		owner = {
			is_gestalt = yes
			has_technology = "tech_unity_of_purpose"
		}
		uses_district_set = giga_frameworld
	}

	allow = {
		hidden_trigger = {
			exists = owner
			or = {
				owner = {
					is_ai = no
				}

				frameworld_needs_more_maintenance_drones = yes
			}
		}
	}

	prerequisites = {
		tech_unity_of_purpose
	}

	conversion_ratio = 1.0
	convert_to = {
		district_giga_frameworld_amenities_dystopian
		district_giga_frameworld_amenities
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
		is_gestalt = yes
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @advanced_cost
			rare_crystals = @advanced_rare_cost
		}
		upkeep = {
			energy = @advanced_upkeep
			rare_crystals = @advanced_rare_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 2
		job_maintenance_drone_add = 8
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_2 }
		}
		modifier = {
			job_maintenance_drone_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			has_carrier_flag = frameworld_advanced_city
		}
		modifier = {
			job_frame_maintenance_overseer_add = 2
			job_maintenance_drone_add = -2
		}
	}

	triggered_desc = {
		text = job_maintenance_drone_effect_desc
	}

	triggered_desc = {
		trigger = {
			has_deposit = d_frameworld_advanced_nexus
		}
		text = job_frame_maintenance_overseer_effect_desc
	}
	ai_weight_coefficient = 20
	additional_ai_weight = 1555
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_elysium_control; source = Gigastructural Engineering & More (4.4)::common\districts\giga_elysium.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:7.0 roi2250:72000.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_elysium_control = {
	base_buildtime = 240
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		uses_district_set = giga_elysium
	}

	potential = {
		uses_district_set = giga_elysium
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @elysium_cost
		}
		upkeep = {
			energy = @elysium_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 200
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_giga_elysium_controller_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
				has_ascension_perk = ap_mind_over_matter
			}
		}
		modifier = {
			job_telepath_add = 1
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				is_gestalt = no
				not = { has_ascension_perk = ap_mind_over_matter }
			}
		}
		modifier = {
			job_enforcer_add = 1
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		modifier = {
			job_giga_elysium_controller_drone_add = 2
			job_patrol_drone_add = 1
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = no }
		}
		text = job_giga_elysium_controller_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
				has_ascension_perk = ap_mind_over_matter
			}
		}
		text = job_telepath_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				is_gestalt = no
				not = { has_ascension_perk = ap_mind_over_matter }
			}
		}
		text = job_enforcer_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		text = job_giga_elysium_controller_drone_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		text = job_patrol_drone_effect_desc
	}
	ai_weight_coefficient = 19
	additional_ai_weight = 1513
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_frameworld_fortress; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:8.0 roi2250:68400.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_frameworld_fortress = {
	base_buildtime = @advanced_time
	icon = district_maginot_world_bunkers
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		exists = from
		from = {
			has_technology = "tech_global_defense_grid"
		}
		uses_district_set = giga_frameworld
	}

	potential = {
		exists = owner
		owner = {
			has_technology = "tech_global_defense_grid"
		}
		uses_district_set = giga_frameworld
	}

	prerequisites = {
		tech_global_defense_grid
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @advanced_cost
			volatile_motes = @advanced_rare_cost
		}
		upkeep = {
			energy = @advanced_upkeep
			volatile_motes = @advanced_rare_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		modifier = {
			job_soldier_add = 4
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		modifier = {
			job_warrior_drone_add = 4
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = no }
		}
		text = job_soldier_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		text = job_warrior_drone_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			is_giga_maginot_frameworld = yes
		}
		text = job_maginot_planetary_bunker_effect_desc
	}

	ai_weight_coefficient = 19
	additional_ai_weight = 1515
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_frameworld_amenities; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:8.0 roi2250:68400.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_frameworld_amenities = {
	base_buildtime = @advanced_time
	icon = district_arcology_leisure
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		exists = from
		from = {
			is_gestalt = no
			NOT = { has_valid_civic = civic_dystopian_society }
			has_technology = tech_hyper_entertainment_forum
		}
		uses_district_set = giga_frameworld
	}

	potential = {
		exists = owner
		owner = {
			is_gestalt = no
			NOT = { has_valid_civic = civic_dystopian_society }
			has_technology = tech_hyper_entertainment_forum
		}
		uses_district_set = giga_frameworld
	}

	prerequisites = {
		tech_hyper_entertainment_forum
	}

	conversion_ratio = 1.0
	convert_to = {
		district_giga_frameworld_amenities_dystopian
		district_giga_frameworld_amenities_gestalt
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
		is_gestalt = no
		NOT = { has_valid_civic = civic_dystopian_society }
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @advanced_cost
			exotic_gases = @advanced_rare_cost
		}
		upkeep = {
			energy = @advanced_upkeep
			exotic_gases = @advanced_rare_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { NOT = { has_valid_civic = civic_warrior_culture } }
		}
		modifier = {
			job_entertainer_add = 4
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_valid_civic = civic_warrior_culture }
		}
		modifier = {
			job_duelist_add = 4
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { NOT = { has_valid_civic = civic_warrior_culture } }
		}
		text = job_entertainer_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { has_valid_civic = civic_warrior_culture }
		}
		text = job_duelist_effect_desc
	}
	ai_weight_coefficient = 19
	additional_ai_weight = 1515
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_frameworld_hive_advanced; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:8.0 roi2250:64800.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_frameworld_hive_advanced = {
	base_buildtime = @advanced_time
	icon = district_hive
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes

	show_on_uncolonized = {
		from = { is_hive_empire = yes }
		uses_district_set = giga_frameworld
		has_carrier_flag = frameworld_advanced_city
	}

	potential = {
		exists = owner
		owner = { is_hive_empire = yes }
		uses_district_set = giga_frameworld
		has_carrier_flag = frameworld_advanced_city
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_frameworld_nexus
		district_giga_frameworld_city

		district_giga_frameworld_city_advanced
		district_giga_frameworld_nexus_advanced
		district_giga_frameworld_hive
	}

	resources = {
		category = planet_districts_cities
		cost = {
			minerals = @advanced_cost
		}
		upkeep = {
			energy = @advanced_upkeep
		}
	}

	triggered_planet_modifier = {
		potential = { always = yes }
		planet_housing_add = 12
		job_maintenance_drone_add = 6
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_1 }
		}
		modifier = {
			planet_housing_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_2 }
		}
		modifier = {
			planet_housing_add = 2
			job_maintenance_drone_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_extended_hives }
		}
		modifier = {
			planet_housing_add = 2
		}
	}
	ai_weight_coefficient = 19
	additional_ai_weight = 1507
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_frameworld_nexus; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:6.0 roi2250:50400.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_frameworld_nexus = {
	base_buildtime = @city_time
	icon = district_nexus
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes

	show_on_uncolonized = {
		from = { is_machine_empire = yes }
		uses_district_set = giga_frameworld
		not = { has_carrier_flag = frameworld_advanced_city }
	}

	potential = {
		exists = owner
		owner = { is_machine_empire = yes }
		uses_district_set = giga_frameworld
		not = { has_carrier_flag = frameworld_advanced_city }
	}

	allow = {
		#hidden_trigger = {
			exists = owner
			or = {
				owner = {
					is_ai = no
				}

				# we need more housing
				free_housing < 10

				# we might still need to unlock buildings
				num_districts = {
					type = district_giga_frameworld_nexus
					value < 10
				}

				# if we need more maintenance drones
				frameworld_needs_more_maintenance_drones = yes
			}
		#}
	}

	conversion_ratio = 0.5
	convert_to = {
		district_giga_frameworld_city
		district_giga_frameworld_hive

		district_giga_frameworld_city_advanced
		district_giga_frameworld_nexus_advanced
		district_giga_frameworld_hive_advanced
	}

	resources = {
		category = planet_districts_cities
		cost = {
			minerals = @city_cost
		}
		upkeep = {
			energy = @city_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 5
		job_maintenance_drone_add = 3
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_1 }
		}
		modifier = {
			planet_housing_add = 1
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_2 }
		}
		modifier = {
			planet_housing_add = 1
			job_maintenance_drone_add = 1
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_virtuality_4 }
		}
		modifier = {
			job_maintenance_drone_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_optimized_nexus }
		}
		modifier = {
			planet_housing_add = 1
		}
	}
	ai_weight_coefficient = 19
	additional_ai_weight = 1459
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_elysium_entertainment; source = Gigastructural Engineering & More (4.4)::common\districts\giga_elysium.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:5.0 roi2250:50400.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_elysium_entertainment = {
	base_buildtime = 240
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes
	icon = district_hab_cultural

	show_on_uncolonized = {
		uses_district_set = giga_elysium

		exists = from
		from = {
			is_gestalt = no
			NOT = { has_valid_civic = civic_dystopian_society }
		}
	}

	potential = {
		uses_district_set = giga_elysium

		exists = owner
		owner = {
			is_gestalt = no
			NOT = { has_valid_civic = civic_dystopian_society }
		}
	}

	conversion_ratio = 0.5
	convert_to = {
		district_giga_elysium_admin
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @elysium_cost
		}
		upkeep = {
			energy = @elysium_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 200
		job_giga_media_coordinator_add = 1
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				NOT = { has_valid_civic = civic_warrior_culture }
			}
		}
		modifier = {
			job_entertainer_add = 2
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_valid_civic = civic_warrior_culture
			}
		}
		modifier = {
			job_duelist_add = 2
		}
	}

	triggered_desc = {
		text = job_giga_media_coordinator_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				has_valid_civic = civic_warrior_culture
			}
		}
		text = job_duelist_effect_desc
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				NOT = { has_valid_civic = civic_warrior_culture }
			}
		}
		text = job_entertainer_effect_desc
	}
	ai_weight_coefficient = 19
	additional_ai_weight = 1451
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_planet_sanctuary; source = Gigastructural Engineering & More (4.4)::common\districts\giga_planets.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:5.0 roi2250:39195.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep
district_giga_planet_sanctuary = {
	base_buildtime = @giga_planet_district_buildtime
	icon = district_arcology_organic_housing
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		giga_uses_admin_district = yes
		not = { uses_district_set = giga_orbital } # has its own better sanctuary
		from = {
			has_valid_civic = civic_machine_servitor
		}
	}

	potential = {
		giga_uses_admin_district = yes
		not = { uses_district_set = giga_orbital }
		exists = owner
		owner = {
			has_valid_civic = civic_machine_servitor
		}
	}

	resources = {
		category = planet_districts
		cost = { minerals = @giga_planet_cost }
		upkeep = { energy = @giga_planet_maintenance }
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_planet_admin
		district_giga_planet_admin_religious
		district_giga_orbital_sanctuary
	}

	planet_modifier = {
		job_bio_trophy_add = 5
	}

	triggered_desc = {
		text = job_bio_trophy_effect_desc
	}
	triggered_desc = {
		text = job_maintenance_drone_effect_desc
	}
	ai_weight_coefficient = 18
	additional_ai_weight = 1418
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_frameworld_hive; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:4.0 roi2250:36000.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables
district_giga_frameworld_hive = {
	base_buildtime = @city_time
	icon = district_hive
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes

	show_on_uncolonized = {
		from = { is_hive_empire = yes }
		uses_district_set = giga_frameworld
		not = { has_carrier_flag = frameworld_advanced_city }
	}

	potential = {
		exists = owner
		owner = { is_hive_empire = yes }
		uses_district_set = giga_frameworld
		not = { has_carrier_flag = frameworld_advanced_city }
	}

	conversion_ratio = 0.5
	convert_to = {
		district_giga_frameworld_nexus
		district_giga_frameworld_city

		district_giga_frameworld_city_advanced
		district_giga_frameworld_nexus_advanced
		district_giga_frameworld_hive_advanced
	}

	resources = {
		category = planet_districts_cities
		cost = {
			minerals = @city_cost
		}
		upkeep = {
			energy = @city_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 6
		job_maintenance_drone_add = 3
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_1 }
		}
		modifier = {
			planet_housing_add = 1
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_technology = tech_housing_2 }
		}
		modifier = {
			planet_housing_add = 1
			job_maintenance_drone_add = 1
		}
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { has_active_tradition = tr_prosperity_extended_hives }
		}
		modifier = {
			planet_housing_add = 1
		}
	}
	ai_weight_coefficient = 18
	additional_ai_weight = 1399
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_elysium_housing; source = Gigastructural Engineering & More (4.4)::common\districts\giga_elysium.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:2.0 roi2250:21600.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_giga_elysium_housing = {
	base_buildtime = 240
	is_uncapped = { always = yes }
	exempt_from_ai_planet_specialization = yes
	icon = district_hab_housing

	show_on_uncolonized = {
		uses_district_set = giga_elysium
	}

	potential = {
		uses_district_set = giga_elysium
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @elysium_cost
		}
		upkeep = {
			energy = @elysium_maintenance
		}
	}

	planet_modifier = {
		planet_housing_add = 800
	}

	#######################################################
	# Normal empires

	inline_script = {
		script = planet/rulers/giga_ruler_job_swap
		jobs = 1
		district = @yes
		condition = "owner = { is_gestalt = no }"
	}

	#######################################################
	# Gestalts

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		modifier = {
			job_maintenance_drone_add = 2
		}
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		text = job_maintenance_drone_effect_desc
	}
	ai_weight_coefficient = 17
	additional_ai_weight = 1316
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}

# object = district:district_giga_frameworld_synapse; source = Gigastructural Engineering & More (4.4)::common\districts\giga_frameworld_districts.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:1.0 roi2250:15000.0 flags:ai_weight_absent|has_ai_or_direct_output|has_build_cost|has_jobs|has_upkeep|unresolved_variables|uses_inline_script
district_giga_frameworld_synapse = {
	base_buildtime = @advanced_time
	icon = district_arcology_administrative
	is_uncapped = { always = yes }

	show_on_uncolonized = {
		exists = from
		from = {
			is_hive_empire = yes
			has_technology = "tech_hive_cluster"
		}
		uses_district_set = giga_frameworld
	}

	potential = {
		exists = owner
		owner = {
			is_hive_empire = yes
			has_technology = "tech_hive_cluster"
		}
		uses_district_set = giga_frameworld
	}

	prerequisites = {
		tech_hive_cluster
	}

	show_tech_unlock_if = {
		giga_has_frameworld_origin = yes
		is_hive_empire = yes
		not = { has_valid_civic = civic_machine_servitor }
	}

	conversion_ratio = 1
	convert_to = {
		district_giga_frameworld_simulation
		district_giga_frameworld_administrative
		district_giga_frameworld_temple
		district_giga_frameworld_sanctuary
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @advanced_cost
			exotic_gases = @advanced_rare_cost
		}
		upkeep = {
			energy = @advanced_upkeep
			exotic_gases = @advanced_rare_upkeep
		}
	}

	planet_modifier = {
		planet_housing_add = 2
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_active_tradition = tr_domination_synaptic_extensions
			}
		}
		modifier = {
			planet_housing_add = 2
		}
	}

	inline_script = {
		script = planet/unity/giga_unity_job_swap
		jobs = 4
		district = @yes
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = {
				has_edict = synaptic_reinforcement
			}
		}
		job_maintenance_drone_add = 1
	}

	triggered_desc = {
		trigger = {
			exists = owner
			owner = {
				has_edict = synaptic_reinforcement
			}
		}
		text = job_maintenance_drone_effect_desc
	}

	ai_weight_coefficient = 17
	additional_ai_weight = 1261
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
		unity = 1
	}
}

# object = district:district_giga_birch_structure; source = Gigastructural Engineering & More (4.4)::common\districts\giga_birch_world.txt
# staid_dataset_job_pressure = family:general_job_pressure jobs:2.0 roi2250:2850.0 flags:ai_weight_absent|has_build_cost|has_jobs|has_upkeep
district_giga_birch_structure = {
	base_buildtime = @giga_birch_insula_time
    is_uncapped = { always = no }
	base_cap_amount = 1
	can_demolish = no
	exempt_from_ai_planet_specialization = yes
	overlay_icon = GFX_district_government

	has_primary_zone = yes
	custom_gui = giga_planet_district_entry_birch_structure

	zone_slots = {
		slot_city_government
		slot_giga_birch_structure_extra
	}

	show_on_uncolonized = {
		uses_district_set = giga_birch_world
		not = {	has_planet_flag = giga_birch_ruined	}
	}

	potential = {
		uses_district_set = giga_birch_world
		not = {	has_planet_flag = giga_birch_ruined	}
	}

	resources = {
		category = planet_districts
		cost = {
			minerals = @giga_birch_insula_cost
			alloys = @giga_birch_insula_cost
		}
		upkeep = { energy = @giga_birch_insula_maintenance }
	}

	planet_modifier = {
		giga_birch_district_insula_base = 1
		giga_birch_district_insula_per_pop = 0.0001
	}
	triggered_desc = {
		trigger = { always = yes }
		text = giga_birch_district_insula_tooltip
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = no }
		}
		job_giga_birch_structure_manager_add = 1
		job_giga_birch_structure_manager_per_pop = 0.01

		job_enforcer_per_pop = 0.04
	}

	triggered_planet_modifier = {
		potential = {
			exists = owner
			owner = { is_gestalt = yes }
		}
		job_giga_birch_structure_manager_drone_add = 1
		job_giga_birch_structure_manager_drone_per_pop = 0.01

		job_patrol_drone_per_pop = 0.06
	}

	triggered_name = { text = district_giga_birch_structure_subtitle }
	ai_weight_coefficient = 14
	additional_ai_weight = 1052
	ai_weight = {
		factor = 1
		modifier = { factor = 30 num_unemployed > 0 free_jobs < 1 }
		modifier = { factor = 18 num_unemployed > 0 free_jobs < 3 }
		modifier = { factor = 16 owner = { staid_construction_spenddown_pressure = yes } }
		modifier = { factor = 14 owner = { staid_core_deficit_short_runway = yes } }
		modifier = { factor = 18 owner = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 10 owner = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 6 owner = { staid_surplus_sink_pressure = yes } }
		modifier = { factor = 6 owner = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
	}

	ai_resource_production = {
		energy = 1
		minerals = 1
	}
}
```

## mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: intentionally replaces `basic_economy_plan` with a
# mod-set-specific high-scale survival plan. This is not a compatibility shim:
# the Director assumes Gigas/NSC3/ESC crisis scaling and forces research,
# alloy, trade, naval-cap, habitat/tall, and megastructure pressure early.

basic_economy_plan = {
	ai_weight = { weight = 5000 }

	income = {
		physics_research = 400
		society_research = 400
		engineering_research = 600
		alloys = 120
		consumer_goods = 150
		food = 60
		energy = 150
		minerals = 150
		unity = 120
		trade = 75
	}

	focus = {
		physics_research = 150
		society_research = 150
		engineering_research = 250
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director opening direct research route"
		potential = {
			staid_opening_direct_research = yes
		}
		income = {
			physics_research = 450
			society_research = 450
			engineering_research = 650
			consumer_goods = 180
			energy = 180
		}
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director opening trade to research route"
		potential = {
			staid_opening_trade_to_research = yes
		}
		income = {
			trade = 300
			consumer_goods = 180
			physics_research = 300
			society_research = 300
			engineering_research = 450
		}
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director opening growth to research route"
		potential = {
			OR = {
				staid_opening_hive_growth_research = yes
				staid_opening_machine_growth_research = yes
				staid_opening_military_to_pops = yes
				staid_opening_nomad_arkship_research = yes
			}
		}
		income = {
			alloys = 180
			minerals = 260
			energy = 220
			physics_research = 250
			society_research = 250
			engineering_research = 400
		}
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director consumer goods runway repair"
		potential = {
			country_uses_consumer_goods = yes
			NOT = { staid_consumer_goods_runway_safe = yes }
		}
		income = {
			consumer_goods = 500
			minerals = 350
			energy = 250
			trade = 200
		}
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director food break-even repair"
		potential = {
			country_uses_food = yes
			NOT = { staid_food_runway_safe = yes }
		}
		income = {
			food = 300
			energy = 100
			trade = 75
		}
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director early modded research rush"
		potential = {
			years_passed < 50
			NOT = { staid_catastrophic_collapse_mode = yes }
			OR = {
				staid_research_input_runway_safe = yes
				staid_high_scale_snowball_pressure = yes
				staid_construction_spenddown_pressure = yes
			}
		}
		income = {
			physics_research = 350
			society_research = 350
			engineering_research = 550
			unity = 100
		}
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director midgame megastructure rush"
		potential = {
			years_passed > 44
			NOT = { staid_catastrophic_collapse_mode = yes }
			OR = {
				staid_research_input_runway_safe = yes
				staid_high_scale_snowball_pressure = yes
				staid_construction_spenddown_pressure = yes
			}
		}
		income = {
			physics_research = 1500
			society_research = 1500
			engineering_research = 2500
			alloys = 500
			energy = 350
			minerals = 350
			unity = 300
			trade = 150
		}
		naval_cap = 600
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director crisis-scale giga rush"
		potential = {
			years_passed > 79
			NOT = { staid_catastrophic_collapse_mode = yes }
			OR = {
				staid_research_input_runway_safe = yes
				staid_high_scale_snowball_pressure = yes
				staid_construction_spenddown_pressure = yes
			}
		}
		income = {
			physics_research = 4500
			society_research = 4500
			engineering_research = 7000
			alloys = 1500
			energy = 1000
			minerals = 1000
			unity = 600
			trade = 250
		}
		naval_cap = 1500
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director planetcraft survival curve"
		potential = {
			years_passed > 119
			NOT = { staid_catastrophic_collapse_mode = yes }
			OR = {
				staid_research_input_runway_safe = yes
				staid_high_scale_snowball_pressure = yes
				staid_construction_spenddown_pressure = yes
			}
		}
		income = {
			physics_research = 10000
			society_research = 10000
			engineering_research = 15000
			alloys = 3500
			energy = 2500
			minerals = 2500
			unity = 1200
			trade = 400
		}
		naval_cap = 3500
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director pathological snowball reserve"
		potential = {
			staid_high_scale_snowball_pressure = yes
		}
		income = {
			physics_research = 20000
			society_research = 20000
			engineering_research = 30000
			alloys = 10000
			energy = 10000
			minerals = 8000
			consumer_goods = 2500
			food = 1500
			unity = 2500
			trade = 1500
		}
		naval_cap = 8000
		pops = 1000000
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director construction spenddown reserve"
		potential = {
			staid_construction_spenddown_pressure = yes
		}
		income = {
			minerals = 30000
			energy = 18000
			consumer_goods = 6000
			alloys = 8000
			food = 2000
			physics_research = 12000
			society_research = 12000
			engineering_research = 18000
			unity = 5000
			trade = 3000
		}
		naval_cap = 5000
		pops = 1000000
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director unemployed pop construction catch-up"
		potential = {
			any_owned_planet = {
				num_unemployed > 0
				free_jobs < 1
			}
		}
		income = {
			minerals = 12000
			energy = 8000
			consumer_goods = 2500
			alloys = 3000
			food = 1200
			physics_research = 6000
			society_research = 6000
			engineering_research = 9000
			unity = 2000
			trade = 1200
		}
		pops = 1000000
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director open slot construction catch-up"
		potential = {
			any_owned_planet = {
				free_building_slots > 0
				num_unemployed > 0
			}
		}
		income = {
			minerals = 16000
			energy = 10000
			consumer_goods = 3000
			alloys = 4000
			physics_research = 8000
			society_research = 8000
			engineering_research = 12000
			unity = 2500
			trade = 1500
		}
		pops = 1000000
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director rich empire spend-down construction"
		potential = {
			resource_stockpile_compare = { resource = minerals value > 10000 }
			any_owned_planet = {
				OR = {
					num_unemployed > 0
					free_building_slots > 0
				}
			}
		}
		income = {
			minerals = 25000
			energy = 16000
			consumer_goods = 5000
			alloys = 7000
			physics_research = 12000
			society_research = 12000
			engineering_research = 18000
			unity = 4000
			trade = 2500
		}
		naval_cap = 5000
		pops = 1000000
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director megastructure spam reserve"
		potential = {
			OR = {
				staid_megastructure_commit_safe = yes
				staid_high_scale_snowball_pressure = yes
			}
		}
		income = {
			alloys = 8000
			energy = 8000
			minerals = 5000
			giga_sr_sentient_metal = 10
			giga_sr_negative_mass = 10
			giga_sr_amb_megaconstruction = 10
			trade = 1000
		}
		naval_cap = 4000
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director habitat and terraforming expansion reserve"
		potential = {
			OR = {
				staid_planetary_capacity_growth_ready = yes
				staid_high_scale_snowball_pressure = yes
			}
		}
		income = {
			minerals = 5000
			energy = 5000
			consumer_goods = 1200
			food = 800
			unity = 1000
			trade = 800
		}
		pops = 1000000
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director trade capacity reserve"
		potential = {
			staid_trade_capacity_safe = yes
		}
		income = {
			trade = 100
		}
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director trade deficit recovery"
		potential = {
			NOT = { staid_trade_capacity_safe = yes }
		}
		income = {
			trade = 150
		}
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director mega alloy reserve"
		potential = {
			staid_megastructure_prep_ready = yes
		}
		income = {
			alloys = 15
			trade = 25
		}
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director giga special resource reserve"
		potential = {
			OR = {
				has_technology = tech_ehof_sentient_tier_1
				has_technology = tech_nm_utilization_1
				has_technology = giga_tech_amb_supertensiles
			}
			NOT = { staid_catastrophic_collapse_mode = yes }
		}
		income = {
			giga_sr_sentient_metal = 5
			giga_sr_negative_mass = 3
			giga_sr_amb_megaconstruction = 5
		}
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director payoff exploitation alloys"
		potential = {
			staid_fleet_payoff_exploitation_ready = yes
		}
		income = {
			alloys = 20
			energy = 20
			trade = 50
		}
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director militarist conquest fleet reserve"
		potential = {
			staid_militarist_conquest_strategy = yes
		}
		income = {
			alloys = 6000
			energy = 3500
			minerals = 2500
			unity = 1000
			trade = 800
		}
		naval_cap = 6000
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director raiding pop acquisition reserve"
		potential = {
			staid_raiding_pop_growth_strategy = yes
		}
		income = {
			alloys = 4500
			energy = 3000
			minerals = 1800
			unity = 800
			trade = 700
		}
		naval_cap = 4500
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director hostile fauna clearance reserve"
		potential = {
			staid_hostile_fauna_clearance_strategy = yes
		}
		income = {
			alloys = 220
			energy = 160
			minerals = 90
		}
		naval_cap = 250
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director modded unlock research reserve"
		potential = {
			staid_research_input_runway_safe = yes
			OR = {
				staid_core_unlock_research_priority_ready = yes
				years_passed > 44
			}
		}
		income = {
			physics_research = 1200
			society_research = 1200
			engineering_research = 1800
			unity = 250
		}
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director capped stockpile research conversion"
		potential = {
			staid_research_input_runway_safe = yes
			OR = {
				staid_resource_waste_pressure = yes
				staid_research_under_curve = yes
			}
		}
		income = {
			physics_research = 1600
			society_research = 1600
			engineering_research = 2200
			trade = 250
			unity = 350
		}
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director 2360 physics catchup"
		potential = {
			years_passed > 119
			staid_research_input_runway_safe = yes
			staid_research_under_curve = yes
			has_monthly_income = { resource = physics_research value < 1200 }
		}
		income = { physics_research = 1800 }
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director 2360 society catchup"
		potential = {
			years_passed > 119
			staid_research_input_runway_safe = yes
			staid_research_under_curve = yes
			has_monthly_income = { resource = society_research value < 1200 }
		}
		income = { society_research = 1800 }
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director 2360 engineering catchup"
		potential = {
			years_passed > 119
			staid_research_input_runway_safe = yes
			staid_research_under_curve = yes
			has_monthly_income = { resource = engineering_research value < 1400 }
		}
		income = { engineering_research = 2400 }
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director fleet throughput reserve"
		potential = {
			staid_shipyard_expansion_ready = yes
		}
		income = {
			alloys = 500
			energy = 300
			trade = 150
		}
		naval_cap = 800
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director threat readiness reserve"
		potential = {
			has_country_flag = staid_tr_defensive_readiness_low
			staid_tr_foreign_affairs_safe = yes
		}
		income = {
			alloys = 7
			energy = 6
			trade = 25
		}
		naval_cap = 40
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director planetary capacity reserve"
		potential = {
			staid_planetary_capacity_growth_ready = yes
		}
		income = {
			minerals = 500
			energy = 400
			consumer_goods = 250
			food = 150
			trade = 150
		}
		pops = 400000
	}

	subplan = {
		optional = yes
		scaling = yes
		set_name = "Stellar AI Director Planetary Diversity outpost reserve"
		potential = {
			staid_planetary_diversity_outpost_investment_ready = yes
		}
		income = {
			minerals = 800
			energy = 500
			consumer_goods = 250
			physics_research = 400
			society_research = 400
			engineering_research = 600
			trade = 150
		}
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director defensive starbase reserve"
		potential = {
			staid_static_defense_investment_ready = yes
		}
		income = {
			alloys = 2200
			energy = 1400
			minerals = 1200
			trade = 500
		}
		naval_cap = 1000
	}

	subplan = {
		scaling = yes
		set_name = "Stellar AI Director crisis starbase reserve"
		potential = {
			staid_crisis_starbase_pressure = yes
		}
		income = {
			alloys = 3500
			energy = 2200
			minerals = 1800
			trade = 800
		}
		naval_cap = 2000
	}
}
```

## mods/StellarAIDirector/common/edicts/zzzz_staid_10_opening_growth_edicts.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Verified full-object edict overrides from installed vanilla edicts.
# Required source-local @variables are copied into this file to preserve vanilla parse context.
@Edict1Cost = 10
@Edict2Cost = 20
@Edict3Cost = 30
@EdictPerpetual = -1
@EdictHighPrio = 100
@EdictMedPrio = 10

research_subsidies = {
	length = @EdictPerpetual
	icon = "GFX_edict_type_policy"

	resources = {
		category = edicts
		cost = {
			unity = @Edict3Cost
			multiplier = value:edict_size_effect
		}
		upkeep = {
			unity = @Edict3Cost
			multiplier = value:edict_size_effect
		}
	}

	modifier = {
		researcher_jobs_bonus_workforce_mult = 0.10
		planet_physicists_trade_upkeep_add = 1
		planet_biologists_trade_upkeep_add = 1
		planet_engineers_trade_upkeep_add = 1
	}

	potential = {
		has_tradition = tr_discovery_databank_uplinks
		is_wilderness_empire = no
	}

	ai_weight = {
		weight = @EdictMedPrio
		modifier = { factor = 12 staid_opening_route_research_priority = yes staid_can_afford_research_push = yes }
	}
}

encourage_free_thought = {
	length = @EdictPerpetual
	icon = "GFX_edict_type_policy"

	resources = {
		category = edicts
		cost = {
			unity = @Edict1Cost
			multiplier = value:edict_size_effect
		}
		upkeep = {
			unity = @Edict1Cost
			multiplier = value:edict_size_effect
		}
	}

	modifier = {
		pop_ethics_shift_speed_mult = 1
	}

	potential = {
		is_egalitarian = yes
	}

	ai_weight = {
		weight = 0
		modifier = { factor = 8 staid_opening_route_research_priority = yes staid_can_afford_research_push = yes }
	}
}

map_the_stars = {
	length = @EdictPerpetual
	icon = "GFX_edict_type_policy"

	resources = {
		category = edicts
		cost = {
			unity = @Edict1Cost
			multiplier = value:edict_size_effect
		}
		upkeep = {
			unity = @Edict1Cost
			multiplier = value:edict_size_effect
		}
	}

	modifier = {
		science_ship_survey_speed = 0.25
		ship_anomaly_generation_chance_mult = 0.10
		ship_hyperlane_range_add = 1
	}

	potential = {
		has_tradition = tr_discovery_adopt
	}

	ai_weight = {
		weight = 0
		modifier = {
			weight = @EdictHighPrio
			years_passed < 50
		}
		modifier = { factor = 5 staid_is_opening_phase = yes staid_has_safe_basic_stockpiles = yes }
	}
}

capacity_subsidies = {
	length = @EdictPerpetual
	icon = "GFX_edict_type_policy"

	resources = {
		category = edicts
		cost = {
			unity = @Edict3Cost
			multiplier = value:edict_size_effect
		}
		upkeep = {
			unity = @Edict3Cost
			multiplier = value:edict_size_effect
		}
	}

	modifier = {
		technician_jobs_bonus_workforce_mult = 0.20
		planet_technician_trade_upkeep_add = 0.50
	}

	potential = {
		is_wilderness_empire = no
	}
	show_tech_unlock_if = {
		is_wilderness_empire = no
	}

	prerequisites = {
		"tech_power_hub_1"
	}

	ai_weight = {
		weight = @EdictHighPrio
		modifier = {
			should_ai_focus_on_trade = yes
			factor = 0
		}
		modifier = { factor = 6 staid_is_opening_phase = yes NOT = { has_deficit = energy } }
	}
}

mining_subsidies = {
	length = @EdictPerpetual
	icon = "GFX_edict_type_policy"

	resources = {
		category = edicts
		cost = {
			unity = @Edict3Cost
			multiplier = value:edict_size_effect
		}
		upkeep = {
			unity = @Edict3Cost
			multiplier = value:edict_size_effect
		}
	}

	modifier = {
		miner_jobs_bonus_workforce_mult = 0.20
		planet_miners_trade_upkeep_add = 0.50
	}

	potential = {
		is_wilderness_empire = no
		is_nomadic = no
	}

	show_tech_unlock_if = {
		is_wilderness_empire = no
		is_nomadic = no
	}

	prerequisites = {
		"tech_mineral_purification_1"
	}

	ai_weight = {
		weight = @EdictHighPrio
		modifier = { factor = 6 staid_is_opening_phase = yes NOT = { has_deficit = minerals } }
	}
}

farming_subsidies = {
	length = @EdictPerpetual
	icon = "GFX_edict_type_policy"

	resources = {
		category = edicts
		cost = {
			unity = @Edict3Cost
			multiplier = value:edict_size_effect
		}
		upkeep = {
			unity = @Edict3Cost
			multiplier = value:edict_size_effect
		}
	}

	modifier = {
		farmer_jobs_bonus_workforce_mult = 0.20
		planet_farmers_trade_upkeep_add = 0.50
	}

	potential = {
		is_wilderness_empire = no
	}

	show_tech_unlock_if = {
		is_wilderness_empire = no
	}

	prerequisites = {
		"tech_food_processing_1"
	}

	ai_weight = {
		weight = @EdictHighPrio
		modifier = {
			country_uses_food = no
			factor = 0
		}
		modifier = { factor = 4 staid_is_opening_phase = yes NOT = { has_deficit = food } }
	}
}

fortify_the_border = {
	length = @EdictPerpetual
	icon = "GFX_edict_type_policy"

	resources = {
		category = edicts
		cost = {
			unity = @Edict1Cost
			multiplier = value:edict_size_effect
		}
		upkeep = {
			unity = @Edict1Cost
			multiplier = value:edict_size_effect
		}
	}

	modifier = {
		starbase_upgrade_speed_mult = 0.50
		country_starbase_capacity_add = 2
	}

	potential = {
		is_nomadic = no
	}

	ai_weight = {
		weight = 0
		modifier = {
			factor = 0
			NOT = { has_country_flag = has_encountered_other_empire }
		}
		modifier = { factor = 6 staid_security_threatened = yes }
	}
}
```

## mods/StellarAIDirector/common/federation_types/zzzz_staid_15_research_diplomacy_federation_types.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/federation_types


# Source-local variables required by copied parent objects.
@xp_to_level_2 = 1200
@xp_to_level_3 = 2400
@xp_to_level_4 = 4800
@xp_to_level_5 = 9600

# policy_route = research_diplomacy_core; source = common/federation_types/00_federation_types.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
research_federation = {
	base_intel = 50
	icon = "GFX_research_federation"
	ownership_limits = default
	potential = {
		host_has_dlc = Federations
	}
	allow = {
		federation_check_for_subject_trigger = yes
		OR = {
			custom_tooltip = {
				fail_text = civic_tooltip_materialist
				is_materialist = yes
			}
			is_machine_empire = yes
			custom_tooltip = {
				fail_text = discovery_traditions_completed
				has_active_tradition = tr_discovery_federations_finish
			}
		}
		custom_tooltip = {
			fail_text = requires_actor_not_barbaric_despoilers
			NOT = { has_valid_civic = civic_barbaric_despoilers }
		}
	}
	levels = {
		level_1 = { # Starting rank
			experience = @xp_to_level_2 # Experience until next rank
			perks = {
				research_federation_passive
			}
		}

		level_2 = {
			experience = @xp_to_level_3
			perks = {
				research_share_1
				research_boost_1
				president_option_1
			}
		}

		level_3 = {
			experience = @xp_to_level_4
			perks = {
				research_share_2
				rare_tech_boost
				tech_diplo_weight_1
			}
		}

		level_4 = {
			experience = @xp_to_level_5
			perks = {
				research_share_3
				crisis_research_1
				extra_envoy_1
			}
		}

		level_5 = {
			perks = {
				research_share_4
				crisis_research_2
				president_megastructure_1
			}
		}
	}
	on_create = {
		remove_federation_flag = enable_federation_cooldowns
		set_federation_law = centralization_minimal
		set_federation_law = succession_type_rotation
		set_federation_law = succession_term_years_20
		set_federation_law = fleet_contribution_none
		set_federation_law = federation_build_fleets_everyone
		set_federation_law = vote_weight_equal
		set_federation_law = declare_war_unanimous_vote
		set_federation_law = invite_members_unanimous_vote
		set_federation_law = kick_members_majority_vote
		set_federation_law = free_migration_no
		set_federation_law = treaties_separate_yes
		set_federation_law = allow_subjects_to_join_no
		set_federation_flag = enable_federation_cooldowns
	}
	ai_weight = {
		base = 0
		modifier = {
			desc = federation_acceptance_honorbound_warriors
			add = -20
			from = {
				has_ai_personality = honorbound_warriors
			}
		}
		modifier = {
			desc = federation_acceptance_evangelising_zealots
			add = -20
			from = {
				has_ai_personality = evangelising_zealots
			}
		}
		modifier = {
			desc = federation_acceptance_erudite_explorers
			add = 10
			from = {
				has_ai_personality = erudite_explorers
			}
		}
		modifier = {
			desc = federation_acceptance_spiritual_seekers
			add = -10
			from = {
				has_ai_personality = spiritual_seekers
			}
		}
		modifier = {
			desc = federation_acceptance_ruthless_capitalists
			add = -10
			from = {
				has_ai_personality = ruthless_capitalists
			}
		}
		modifier = {
			desc = federation_acceptance_peaceful_traders
			add = 10
			from = {
				has_ai_personality = peaceful_traders
			}
		}
		modifier = {
			desc = federation_acceptance_hegemonic_imperialists
			add = -20
			from = {
				has_ai_personality = hegemonic_imperialists
			}
		}
		modifier = {
			desc = federation_acceptance_slaving_despots
			add = -10
			from = {
				has_ai_personality = slaving_despots
			}
		}
		modifier = {
			desc = federation_acceptance_decadent_hierarchy
			add = -30
			from = {
				has_ai_personality = decadent_hierarchy
			}
		}
		modifier = {
			desc = federation_acceptance_democratic_crusaders
			add = 0
			from = {
				has_ai_personality = democratic_crusaders
			}
		}
		modifier = {
			desc = federation_acceptance_harmonious_hierarchy
			add = 0
			from = {
				has_ai_personality = harmonious_hierarchy
			}
		}
		modifier = {
			desc = federation_acceptance_federation_builders
			add = 10
			from = {
				has_ai_personality = federation_builders
			}
		}
		modifier = {
			desc = federation_acceptance_xenophobic_isolationists
			add = -50
			from = {
				has_ai_personality = xenophobic_isolationists
			}
		}
		modifier = {
			desc = federation_acceptance_hive_mind
			add = -50
			from = {
				has_ai_personality = hive_mind
			}
		}
		modifier = {
			desc = federation_acceptance_migrating_flock
			add = 20
			from = {
				has_ai_personality = migrating_flock
			}
		}
		modifier = {
			desc = federation_acceptance_machine_intelligence
			add = -20
			from = {
				has_ai_personality = machine_intelligence
			}
		}
		modifier = {
			desc = federation_acceptance_assimilators
			add = -50
			from = {
				has_ai_personality = assimilators
			}
		}
		modifier = {
			desc = federation_acceptance_servitors
			add = 0
			from = {
				has_ai_personality = servitors
			}
		}
		modifier = {
			desc = federation_acceptance_fanatic_befrienders
			add = 30
			from = {
				has_ai_personality = fanatic_befrienders
			}
		}
		modifier = {
			add = -100
			desc = alert_federation_low_cohesion_title
			from = {
				has_federation = yes
			}
			exists = federation
			federation = { federation_cohesion <= -50 }
		}
		modifier = {
			add = -50
			desc = alert_federation_low_cohesion_title
			from = {
				has_federation = yes
			}
			exists = federation
			federation = {
				federation_cohesion > -50
				federation_cohesion <= 0
			}
		}
		modifier = {
			add = 30
			desc = COHESION_LABEL
			from = {
				has_federation = yes
			}
			exists = federation
			federation = { federation_cohesion >= 80 }
		}
		modifier = {
			add = 20
			desc = federation_acceptance_hegemony
			from = {
				has_federation = yes
				NOT = {
					relative_power = {
						who = prev
						value > equivalent
					}
				}
			}
			exists = federation
			federation = { has_federation_type = hegemony_federation }
		}
		modifier = {
			add = 50
			desc = federation_acceptance_hegemony
			from = {
				has_federation = yes
				relative_power = {
					who = prev
					value > equivalent
				}
			}
			exists = federation
			federation = { has_federation_type = hegemony_federation }
		}
		# staid_research_diplomacy_core = verified Research Cooperative preference
		modifier = { add = 250 desc = staid_research_diplomacy_core from = { staid_research_diplomacy_priority_ready = yes } }
		modifier = { add = 175 desc = staid_science_snowball from = { staid_science_nexus_research_priority_ready = yes } }
		modifier = { add = 125 desc = staid_research_runway from = { staid_research_input_runway_safe = yes } }
		modifier = { add = 90 desc = staid_materialist_research from = { OR = { has_ethic = ethic_materialist has_ethic = ethic_fanatic_materialist has_authority = auth_machine_intelligence } } }
		modifier = { add = 70 desc = staid_discovery_federation from = { has_active_tradition = tr_discovery_federations_finish } }
		modifier = { add = -80 desc = staid_conquest_route_prefers_other_federation from = { staid_aggressive_fleet_pressure = yes NOT = { staid_research_diplomacy_priority_ready = yes } } }
		modifier = { add = -60 desc = staid_spiritualist_research_federation_drift from = { OR = { has_ethic = ethic_spiritualist has_ethic = ethic_fanatic_spiritualist } NOT = { staid_research_diplomacy_priority_ready = yes } } }
	}
}

```

## mods/StellarAIDirector/common/megastructures/zzzz_staid_03_megastructures_megastructures.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/megastructures


# Source-local variables required by copied parent objects.
@central_orbital_alloy_cost = 1500
@central_orbital_build_time = 1800
@central_orbital_influence_cost = 200
@giga_big_mega_start_unity_cost		= 5000
@giga_big_mega_unity_cost			= 5000
@giga_giga_unity_cost				= 10000
@giga_mega_unity_cost				= 2500
@giga_small_mega_unity_cost			= 1000
@giga_tera_start_unity_cost			= 20000
@matrioshka_p5_upkeep_alloys_g_star				= 200		# 100% Vanilla
@matrioskha_brain_1_bm_cost = 50
@ring_world_2_intermediate_bm_cost = 100
@ring_world_3_intermediate_bm_cost = 0
@science_kilo_alloys_3 		= 1500
@science_kilo_alloys_4 		= 2000
@science_kilo_cost_1 		= 500
@science_kilo_cost_2 		= 1000
@science_kilo_unity_3 		= 2000
@science_kilo_unity_4 		= 4000

# policy_route = economy_megastructure_core; source = common/megastructures/zz_e_dyson_sphere.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
dyson_sphere_0 = {
	entity = "construction_platform_entity"
	construction_entity = "construction_platform_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	entity_offset = { x = -7 y = -7 }
	custom_tooltip_requirements = "MEGASTRUCTURE_TOOLTIP_REQUIREMENTS_DYSON_SPHERE"
	prerequisites = { "tech_dyson_sphere" }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_dyson_sphere
		cost = {
			unity = @giga_big_mega_start_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 5000
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|alloys|AMOUNT|5000| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|unity|AMOUNT|@giga_big_mega_start_unity_cost| }
		upkeep = { energy = 5 }
	}

	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = alloys AMOUNT = 5000 }
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = unity  AMOUNT = @giga_big_mega_start_unity_cost }
	}
	on_build_cancel = {
		giga_ai_savings_refund = { CATEGORY = important RESOURCE = alloys }
		giga_ai_savings_refund = { CATEGORY = important RESOURCE = unity }
	}

	potential = {
		NOT = { has_global_flag = vanilla_dyson_disabled }
		OR = {
			has_global_flag = vanilla_dyson_capped_u
			check_variable = {
				which = giga_current_vanilla_dyson
				value < value:giga_vanilla_dyson_limit
			}
		}
		custom_tooltip = {
			fail_text = "requires_no_machine_age"
			OR = {
				has_machine_age_dlc = no
				has_global_flag = vanilla_dyson_swarm_replace_disabled
				AND = {
					OR = {
						has_global_flag = has_real_space_mod
						NOT = { has_global_flag = giga_o_stars_disabled }
					}
					has_technology = giga_tech_dyson_o_star
				}
			}
		}
	}

	possible = {
		hidden_trigger = {
			exists = starbase
		}
		custom_tooltip = { fail_text = "requires_inside_border"			is_inside_border = from }
		custom_tooltip = { fail_text = "requires_surveyed_system"		giga_system_is_surveyed = yes }
		custom_tooltip = {
			fail_text = "requires_no_colonies"
			NOT = {
				any_system_planet = {
					is_colony = yes
					is_artificial = no
					exists = owner
					owner = {
						is_primitive = no
					}
				}
			}
		}

		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = vanilla_dyson_capped_u
					check_variable = {
						which = giga_current_vanilla_dyson
						value < value:giga_vanilla_dyson_limit
					}
				}
			}
		}
		custom_tooltip = {
			fail_text = "blocked_by_pre_ftl_policy"
			if = {
				limit = {
					any_system_planet = {
						exists = owner
						owner = {
							is_primitive = yes
						}
					}
				}
				from = {
					has_policy_flag = interference_aggressive
				}
			}
		}
		custom_tooltip = {
			fail_text = "requires_no_arc_furnace"
			system_has_arc_furnace = no
		}
		custom_tooltip = {
			fail_text = "requires_no_arc_furnace_construction"
			if = {
				limit = {
					system_has_arc_furnace = no
				}
				NOT = {
					solar_system = {
						has_star_flag = arc_furnace_construction
					}
				}
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"		planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "must_build_around_star"					is_star = yes }
			custom_tooltip = { fail_text = "requires_no_anomaly"					has_anomaly = no }
			custom_tooltip = { fail_text = "requires_further_stars" 				NOR = { AND = { giga_is_close_pair_star = yes is_primary_star = no } giga_is_close_pair_primary = yes } }
			custom_tooltip = {
				fail_text = "requires_dyson_swarm"
				OR = {
					AND = {
						giga_is_o_star_for_megas = yes
						from = { has_technology = giga_tech_dyson_o_star }
						NOT = { has_global_flag = vanilla_dyson_swarm_replace_disabled }
					}
					has_global_flag = vanilla_dyson_swarm_replace_disabled
				}
			}
			custom_tooltip = {
				fail_text = "requires_standard_planet_class_o_star"
				OR = {
					giga_is_standard_star = yes
					AND = {
						giga_is_o_star_for_megas = yes
						from = { has_technology = giga_tech_dyson_o_star }
					}
				}
			}
		}
	}


	on_build_complete = {
		set_star_flag = dyson_sphere_built
		every_system_planet = { limit = { has_modifier = terraforming_candidate }	remove_modifier = terraforming_candidate }
		from = {
			set_timed_country_flag = { flag = has_recently_built_dyson_sphere years = 20 }
			set_country_flag = built_dyson_sphere
			change_variable = { which = giga_current_vanilla_dyson value = 1 }
		}
		if = {	limit = { fromfrom.planet = { giga_is_o_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = dyson_sphere_0_o_star finish_upgrade = yes} }
		if = {
			limit = { has_global_flag = giga_dyson_scaling }
			if = {		limit = { fromfrom.planet = { giga_is_b_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = dyson_sphere_0_b_star finish_upgrade = yes} }
			else_if = {	limit = { fromfrom.planet = { giga_is_m_giant_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = dyson_sphere_0_m_giant_star finish_upgrade = yes} }
			else_if = {	limit = { fromfrom.planet = { giga_is_a_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = dyson_sphere_0_a_star finish_upgrade = yes} }
			else_if = {	limit = { fromfrom.planet = { giga_is_f_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = dyson_sphere_0_f_star finish_upgrade = yes} }
			else_if = {	limit = { fromfrom.planet = { giga_is_g_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = dyson_sphere_0_g_star finish_upgrade = yes} }
			else_if = {	limit = { fromfrom.planet = { giga_is_k_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = dyson_sphere_0_k_star finish_upgrade = yes} }
			else_if = {	limit = { fromfrom.planet = { giga_is_m_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = dyson_sphere_0_m_star finish_upgrade = yes} }
		}
		fromfrom.planet = {
			giga_set_has_mega_flag = yes
			if = { limit = { has_orbital_station = yes } orbital_station = { dismantle = yes } }
		}
	}

	ai_weight = {
		factor = 130000

		# policy_route = economy_megastructure_core
		# source_object = megastructure:dyson_sphere_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_economy_megastructure_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_economy_megastructure_build_priority_ready = yes } }
		modifier = { factor = 3 from = { years_passed > 44 } }
		modifier = { factor = 5 from = { years_passed > 79 } }
		modifier = { factor = 8 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
	}
}


# policy_route = early_kilo_economy_core; source = common/megastructures/zz_c_orbital_arc_furnace.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
orbital_arc_furnace_1 = {
    entity = "arc_crucible_stage_1_entity"
    construction_entity = "arc_crucible_stage_1_entity"
    construction_scale = 1.02 #to avoid z-fighting of consrucion entity with the base entity
    portrait = "GFX_megastructure_arc_furnace_background"
    place_entity_on_planet_plane = yes
    entity_offset = { x = 0 y = 0 }
    rotate_to_center = no
    scale_offset = yes
    #show_in_outliner = no
    use_planet_resource = yes
    scales_with_planet = yes
    build_time = 360 # 1 year
    resources = {
		category = giga_kilostructures
        cost = {
            unity = 500
        }
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
            alloys = 500
        }

        upkeep = {
            energy = 20
        }
    }

    construction_blocks_and_blocked_by = self_type

	prerequisites = { "tech_orbital_arc_furnace" }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_system_tooltip = giga_arc_furnace_tooltip
    tooltip_system_score = {
        base = 0
        complex_trigger_modifier = {
            trigger = count_system_planet
            parameters = {
                limit = {
                    NOT = { has_deposit_for = shipclass_research_station }
                    is_star = no
                    is_astral_scar = no
                    colonizable_planet = no
                }
            }
            mode = add
        }
    }
    tooltip_system_score_low_threshold = 10
    tooltip_system_score_high_threshold = 16
    tooltip_best_systems_header = "MEGASTRUCTURE_ARC_FURNACE_BEST_SYSTEMS_TOOLTIP_HEADER"
    tooltip_system_filter = {
        system_has_arc_furnace = no
    }

	potential = {
		has_machine_age_dlc = yes
		OR = {
			check_variable = {
				which = arc_furnace_counter
				value < value:arc_furnace_limit
			}
			has_global_flag = vanilla_furnace_capped_u
		}
	}

    possible = {
        inline_script = megastructures/system_ownership_or_waystation_check
        custom_tooltip = {
            fail_text = "requires_surveyed_system"
            NOT = {
                any_system_planet = {
                    is_surveyed = {
                        who = prev.from
                        status = no
                    }
                }
            }
        }
        custom_tooltip = {
            fail_text = "requires_no_dyson_sphere"
            system_has_dyson_sphere = no
        }
        custom_tooltip = {
            fail_text = "requires_no_dyson_sphere_construction"
            if = {
                limit = {
                    system_has_dyson_sphere = no
                }
                NOT = {
                    solar_system = {
                        has_star_flag = dyson_sphere_construction
                    }
                }
            }
        }
        custom_tooltip = {
            fail_text = "requires_no_arc_furnace"
            system_has_arc_furnace = no
        }
		custom_tooltip = {
			fail_text = "requires_no_planetary_seeder_nexus"
			giga_system_has_planetary_seeder_nexus = no
		}
		custom_tooltip = {
			fail_text = "requires_no_macro_test_site"
			giga_system_has_macro_test = no
		}
		custom_tooltip = {
			fail_text = "requires_no_atmosphere_shredder"
			giga_system_has_atmosphere_shredder = no
		}
		custom_tooltip = {
			fail_text = "requires_no_orb_eco_arc"
			giga_system_has_artificial_eco = no
		}

        custom_tooltip = {
            fail_text = "requires_less_than_x_arc_furnaces"
            from = {
				OR = {
					check_variable = {
						which = arc_furnace_counter
						value < value:arc_furnace_limit
					}
					has_global_flag = vanilla_furnace_capped_u
				}

			}
		}
	}

	dismantle_cost = {
		category = giga_kilostructures
		cost = {
			energy = 500
		}
	}

	dismantle_time = 360

	dismantle_potential = {
		always = yes
	}

	dismantle_possible = {
		can_dismantle_megastructure = {
			TECH = tech_orbital_arc_furnace
		}
	}

	on_dismantle_complete = {
		every_system_planet = {
			limit = {
				has_modifier = orbital_arc_furnace_1_mod
			}
			dismantle_arc_furnace_effect = yes
		}
		random_system_planet = {
			limit = {
				has_planet_flag = has_arc_furnace
			}
			set_planet_entity = { entity = pc_molten }
			remove_carrier_flag = has_megastructure
			remove_planet_flag = has_arc_furnace
		}
		from = {
			add_resource = {
				alloys = 500
				mult = modifier:megastructure_dismantle_refund_mult
			}
			if = {
				limit = {
                check_variable = {
                    which = arc_furnace_counter
						value >= 1
					}
				}
				change_variable = {
					which = arc_furnace_counter
					value = -1
                }
            }
        }
    }

    placement_rules = {
        planet_possible = {
            custom_tooltip = {
                fail_text = "requires_no_anomaly"
				NOT = { has_anomaly = yes }
            }
            is_planet_class = pc_molten
            custom_tooltip = {
                fail_text = "requires_no_existing_megastructure"
                NOR = {
                    has_carrier_flag = megastructure
                    has_carrier_flag = has_megastructure
                }
            }
            if = {
                limit = {
					from = { is_ai = yes }
                }
                solar_system = {
                    count_system_planet = {
                        count >= 8
                        limit = {
							NOT = { has_deposit_for = shipclass_research_station }
                            is_star = no
                            is_astral_scar = no
                            colonizable_planet = no
                        }
                    }
                }
            }
        }
    }

    country_modifier = {
        custom_tooltip = orbital_arc_furnace_1_mod_tooltip
    }

    # root = system
    # from = country

    on_build_start = {
        set_star_flag = arc_furnace_construction
            from = {
			set_country_flag = is_currently_building_orbital_arc_furnace
        }
    }
    on_build_cancel = {
        remove_star_flag = arc_furnace_construction
            from = {
			remove_country_flag = is_currently_building_orbital_arc_furnace
        }
    }
    on_build_complete = {
        remove_star_flag = arc_furnace_construction
        fromfrom.planet = {
            set_carrier_flag = has_megastructure
            set_carrier_flag = has_arc_furnace
            if = {
                limit = {
                    has_orbital_station = yes
                }
                orbital_station = {
                    dismantle = yes
                }
            }
			set_planet_entity = { entity = invisible_turret_entity }
        }
        from = {
			remove_country_flag = is_currently_building_orbital_arc_furnace
			set_timed_country_flag = { flag = has_recently_built_orbital_arc_furnace years = 3 }
            country_event = {
                id = cybernetics.1000
            }
            country_event = {
                id = machine_age.3405 #2nd Arc Furnace built
            }
			change_variable = {
				which = arc_furnace_counter
				value = 1
        }
    }

	}

	ai_weight = {
		factor = 130000

		# policy_route = early_kilo_economy_core
		# source_object = megastructure:orbital_arc_furnace_1
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_early_kilo_economy_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_early_kilo_economy_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 6 from = { years_passed > 79 } }
		modifier = { factor = 8 from = { years_passed > 119 } }
		modifier = { factor = 4 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 3 from = { has_technology = tech_orbital_arc_furnace } }
		modifier = { factor = 3 from = { has_technology = giga_tech_asteroid_manufactory } }
		modifier = { factor = 6 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 8 from = { staid_high_scale_snowball_pressure = yes } }
	}
}


# policy_route = early_kilo_economy_core; source = common/megastructures/zz_c_asteroid_manufactory.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
asteroid_manufactory_0 = {
	inline_script = {
		script = megastructures/asteroid_industry/asteroid_industry_construction
		type = player
		potential = "is_ai = no"
		ai_weight = ""
		on_build_complete = "
			from = {
				country_event = {
					id = giga_asteroid_industry.001
					scopes = {
						from = this # might seem a bit odd but we use the same trigger in placement rules and this event so it is necessary
						fromfrom = root.fromfrom # mega scope
					}
				}
			}
		"
	}
	show_prereqs = yes

	ai_weight = {
		factor = 125000

		# policy_route = early_kilo_economy_core
		# source_object = megastructure:asteroid_manufactory_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_early_kilo_economy_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_early_kilo_economy_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 6 from = { years_passed > 79 } }
		modifier = { factor = 8 from = { years_passed > 119 } }
		modifier = { factor = 4 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 3 from = { has_technology = tech_orbital_arc_furnace } }
		modifier = { factor = 3 from = { has_technology = giga_tech_asteroid_manufactory } }
		modifier = { factor = 6 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 8 from = { staid_high_scale_snowball_pressure = yes } }
	}
}


# policy_route = science_kilo_snowball_core; source = common/megastructures/zz_c_macroengineering_test_site.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
macro_test_site_0 = {
	entity = "giga_test_site_1"
	construction_entity = "giga_test_site_stage_1_entity_con"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = yes
	scales_with_planet = yes
	prerequisites = { giga_tech_engineering_test_site }
	use_planet_resource = yes
	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}
	construction_blocks_and_blocked_by = none

	build_time = 360
	resources = {
		category = giga_kilostructures
		cost = {
			unity = @science_kilo_cost_1
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = @science_kilo_cost_1
		}
		upkeep = {
			energy = 10
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Standard empire
					is_gestalt = no
				}
			}
			consumer_goods = 5
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Hivemind / default
					is_gestalt = yes
					is_machine_empire = no
				}
			}
			minerals = 15
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Robot upkeep
					is_gestalt = yes
					is_machine_empire = yes
				}
			}
			energy = 10
		}
	}

	build_system_tooltip = giga_science_candidate_count
	tooltip_system_score = {
		base = 0
		complex_trigger_modifier = {
			trigger = count_system_planet
			parameters = {
				limit = {
					NOT = { has_deposit_for = shipclass_mining_station }
					is_star = no
					is_astral_scar = no
					colonizable_planet = no
				}
			}
			mode = add
		}
	}
	tooltip_system_score_low_threshold = 10
	tooltip_system_score_high_threshold = 16
	tooltip_best_systems_header = "MEGASTRUCTURE_SCIENCE_KILO_BEST_SYSTEMS_TOOLTIP_HEADER"
	tooltip_system_filter = {
		solar_system = {
			giga_system_has_macro_test = no
		}
		system_has_arc_furnace = no
	}

	potential = {
		has_technology = giga_tech_engineering_test_site
		NOT = { has_global_flag = megabase_disabled }
		OR = {
			has_global_flag = megabase_capped_u
			check_variable = {
				which = giga_current_megabase
				value < value:giga_megabase_limit
			}
		}
	}
	country_modifier = {
		custom_tooltip = orbital_test_site_1_mod_tooltip
	}
	possible = {
        inline_script = megastructures/system_ownership_or_waystation_check
		custom_tooltip = { fail_text = "requires_no_anomaly" 				NOT = { any_system_planet = { has_anomaly = yes } } }
		custom_tooltip = { fail_text = "requires_no_arc_furnace" 			system_has_arc_furnace = no }
		custom_tooltip = { fail_text = "requires_no_macro_test_site"		NOT = { any_system_megastructure = { ehof_giga_new_is_macrotest = yes } } }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = megabase_capped_u
					check_variable = {
						which = giga_current_megabase
						value < value:giga_megabase_limit
					}
				}
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_no_anomaly"				has_anomaly = no }
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"	planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "requires_survey_not_habitable"		is_surveyed = { who = prev.from status = yes } is_planet_habitable = no }
			custom_tooltip = { fail_text = "requires_not_star"					is_star = no }
			custom_tooltip = { fail_text = "must_build_around_frozen" 			giga_is_frozen = yes }
			custom_tooltip = {
				fail_text = "requires_not_astral_scar"
				is_astral_scar = no
			}
			OR = {
				from = { is_ai = no }
				solar_system = {
					count_system_planet = {
						count >= 8
						limit = {
							giga_is_science_candidate = yes
						}
					}
				}
			}
		}
	}

	on_build_start = {
		from = {
			set_country_flag = is_currently_building_macro_test_site
		}
		set_star_flag = mega_base_construction
	}
	on_build_cancel = {
		from = {
			remove_country_flag = is_currently_building_macro_test_site
		}
		remove_star_flag = mega_base_construction
	}
	on_build_complete = {
		save_event_target_as = giga_system
		remove_star_flag = mega_base_construction
		fromfrom.planet = {
			set_planet_flag = has_test_site
			save_event_target_as = giga_planet
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			giga_set_has_mega_flag = yes
			set_planet_entity = {
				entity = invisible_turret_entity
			}
		}
		fromfrom = {
			set_megastructure_flag = giga_dismantle_ready
		}
		from = {
			set_timed_country_flag = { flag = has_recently_built_macro_test_site years = 10 }
			remove_country_flag = is_currently_building_macro_test_site
			create_message = {
				type = MEGASTRUCTURE_BUILT
				localization = MESSAGE_MEGASTRUCTURE_BUILT
				days = 30
				target = from # the Go To
				variable = {
					type = name
					localization = MEGASTRUCTURE
					scope = from
				}
				variable = {
					type = name
					localization = SYSTEM
					scope = root
				}
			}
			change_variable = { which = giga_current_megabase value = 1 }
		}
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			remove_trade_deposits = yes
			set_planet_flag = giga_test_site_stage_1
			save_event_target_as = target_planet
			add_deposit = d_engineering_2
			science_kilo_update_orbital_effect = yes
			# add_modifier = {
			# 	modifier = orbital_atmosphere_shredder_1_mod
			# 	days = -1
			# }
		}
	}

	dismantle_cost = {
		category = giga_kilostructures
		cost = {
			energy = 500
		}
	}

	dismantle_time = 360

	dismantle_potential = {
		always = yes
	}

	dismantle_possible = {
		can_dismantle_megastructure = {
			TECH = giga_tech_engineering_test_site
		}
		# custom_tooltip = {
		# 	fail_text = "requires_not_old_update"
		# 	has_megastructure_flag = giga_dismantle_ready
		# }
	}
	on_dismantle_start = { # Catch for old variants of the mega where it hadn't set the proper flags
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
				NOT = { has_planet_flag = giga_test_site_stage_1 }
			}
			set_planet_flag = giga_test_site_stage_1
		}
		fromfrom.planet = {
			set_planet_flag = has_test_site
		}
	}
	on_dismantle_complete = {
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			giga_dismantle_science_kilo_effect = {
				FLAG = test_site
				TYPE = engineering
			}
		}
		random_system_planet = {
			limit = {
				has_planet_flag = has_test_site
			}
			remove_carrier_flag = has_megastructure
			remove_planet_flag = has_test_site
			set_planet_entity = { entity = giga_test_site_devastated_planet_entity }
		}
		from = {
			add_resource = {
				alloys = 500
				mult = modifier:megastructure_dismantle_refund_mult
			}
			if = {
				limit = {
					check_variable = {
						which = giga_current_megabase
						value >= 1
					}
				}
				change_variable = {
					which = giga_current_megabase
					value = -1
				}
			}
		}
	}

	ai_weight = {
		factor = 145000

		# policy_route = science_kilo_snowball_core
		# source_object = megastructure:macro_test_site_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }
		modifier = { factor = 5 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 11 from = { years_passed > 119 } }
		modifier = { factor = 4 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }
		modifier = { factor = 4 from = { has_technology = giga_tech_macro_scale_weather_manipulation } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = science_kilo_snowball_core; source = common/megastructures/zz_c_macroengineering_test_site.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
macro_test_site_1 = {
	entity = "giga_test_site_2"
	construction_entity = "giga_planet_frame_test_site_2"
	portrait = "GFX_megastructure_cybernetics"
	place_entity_on_planet_plane = yes
	scales_with_planet = yes
	use_planet_resource = yes
	construction_blocks_and_blocked_by = none
	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	# Test Model settings
	# entity_offset = { x = 0 y = 0 }
	# scales_with_planet = yes
	upgrade_from = { macro_test_site_0 }
	country_modifier = {
		custom_tooltip = orbital_test_site_2_mod_tooltip
	}
	build_time = 1080
	resources = {
		category = giga_kilostructures
		cost = {
			unity = @science_kilo_cost_2
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = @science_kilo_cost_2
		}
		upkeep = {
			energy = 20
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Standard empire
					is_gestalt = no
				}
			}
			consumer_goods = 10
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Hivemind / default
					is_gestalt = yes
					is_machine_empire = no
				}
			}
			minerals = 30
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Robot upkeep
					is_gestalt = yes
					is_machine_empire = yes
				}
			}
			energy = 20
		}
	}

	potential = { NOT = { has_global_flag = megabase_disabled } }
	possible = { from = { has_technology = giga_tech_engineering_test_site } }

	on_build_complete = {
		save_event_target_as = giga_system
		remove_star_flag = mega_base_construction
		fromfrom.planet = {
			set_planet_flag = has_test_site
			save_event_target_as = giga_planet
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			giga_set_has_mega_flag = yes
		}

		fromfrom = {
			if = {
				limit = {
					NOT = { has_megastructure_flag = giga_dismantle_ready }
				}
				set_megastructure_flag = giga_dismantle_ready
			}
		}

		# from = { country_event = { id = giga_dialog.402 } }# Notification

		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			set_planet_flag = giga_test_site_stage_2
			remove_planet_flag = giga_test_site_stage_1
			save_event_target_as = target_planet
			add_deposit = d_engineering_2
			science_kilo_update_orbital_effect = yes
			# add_modifier = {
			# 	modifier = orbital_atmosphere_shredder_1_mod
			# 	days = -1
			# }
		}
	}


	dismantle_cost = {
		category = giga_kilostructures
		cost = {
			energy = 1000
		}
	}

	dismantle_time = 360

	dismantle_potential = {
		always = yes
	}

	dismantle_possible = {
		can_dismantle_megastructure = {
			TECH = giga_tech_engineering_test_site
		}
		custom_tooltip = {
			fail_text = "requires_not_old_update"
			has_megastructure_flag = giga_dismantle_ready
		}
	}

	on_dismantle_start = { # Catch for old variants of the mega where it hadn't set the proper flags
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
				NOT = { has_planet_flag = giga_test_site_stage_2 }
			}
			set_planet_flag = giga_test_site_stage_2
		}
		fromfrom.planet = {
			set_planet_flag = has_test_site
		}
	}

	on_dismantle_complete = {
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			giga_dismantle_science_kilo_effect = {
				FLAG = test_site
				TYPE = engineering
			}
		}
		random_system_planet = {
			limit = {
				has_planet_flag = has_test_site
			}
			remove_carrier_flag = has_megastructure
			remove_planet_flag = has_test_site
			set_planet_entity = { entity = giga_test_site_devastated_planet_entity }
		}
		from = {
			add_resource = {
				alloys = 1000
				mult = modifier:megastructure_dismantle_refund_mult
			}
			if = {
				limit = {
					check_variable = {
						which = giga_current_megabase
						value >= 1
					}
				}
				change_variable = {
					which = giga_current_megabase
					value = -1
				}
			}
		}
	}

	ai_weight = {
		factor = 160000

		# policy_route = science_kilo_snowball_core
		# source_object = megastructure:macro_test_site_1
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }
		modifier = { factor = 5 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 11 from = { years_passed > 119 } }
		modifier = { factor = 4 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }
		modifier = { factor = 4 from = { has_technology = giga_tech_macro_scale_weather_manipulation } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = science_kilo_snowball_core; source = common/megastructures/zz_c_macroengineering_test_site.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
macro_test_site_2 = {
	entity = "giga_test_site_3"
	construction_entity = "giga_test_site_stage_3_entity_con"
	portrait = "GFX_megastructure_cybernetics"
	place_entity_on_planet_plane = yes
	scales_with_planet = yes
	use_planet_resource = yes
	construction_blocks_and_blocked_by = none
	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	# Test Model settings
	# entity_offset = { x = 0 y = 0 }
	# scales_with_planet = yes
	upgrade_from = { macro_test_site_1 }
	country_modifier = {
		custom_tooltip = orbital_test_site_3_mod_tooltip
	}
	build_time = 1080
	resources = {
		category = giga_kilostructures
		cost = {
			unity = @science_kilo_unity_3
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = @science_kilo_alloys_3
		}
		upkeep = {
			energy = 40
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Standard empire
					is_gestalt = no
				}
			}
			consumer_goods = 20
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Hivemind / default
					is_gestalt = yes
					is_machine_empire = no
				}
			}
			minerals = 60
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Robot upkeep
					is_gestalt = yes
					is_machine_empire = yes
				}
			}
			energy = 40
		}
	}

	potential = { NOT = { has_global_flag = megabase_disabled } }
	possible = { from = { has_technology = giga_tech_engineering_test_site } }

	on_build_complete = {
		save_event_target_as = giga_system
		fromfrom = {
			if = {
				limit = {
					NOT = { has_megastructure_flag = giga_dismantle_ready }
				}
				set_megastructure_flag = giga_dismantle_ready
			}
		}
		from = {
			create_message = {
				type = MEGASTRUCTURE_UPGRADED
				localization = MESSAGE_MEGASTRUCTURE_UPGRADED
				days = 30
				target = from # the Go To
				variable = {
					type = name
					localization = MEGASTRUCTURE
					scope = from
				}
				variable = {
					type = name
					localization = SYSTEM
					scope = root
				}
			}
		}
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			remove_planet_flag = giga_test_site_stage_2
			set_planet_flag = giga_test_site_stage_3
			save_event_target_as = target_planet
			add_deposit = d_engineering_1
			science_kilo_update_orbital_effect = yes
			add_modifier = {
				modifier = orbital_test_site_3_mod
				days = -1
			}
		}
	}

	dismantle_cost = {
		category = giga_kilostructures
		cost = {
			energy = 1500
		}
	}

	dismantle_time = 360

	dismantle_potential = {
		always = yes
	}

	dismantle_possible = {
		can_dismantle_megastructure = {
			TECH = giga_tech_engineering_test_site
		}
		# custom_tooltip = {
		# 	fail_text = "requires_not_old_update"
		# 	has_megastructure_flag = giga_dismantle_ready
		# }
	}
	on_dismantle_start = { # Catch for old variants of the mega where it hadn't set the proper flags
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
				NOT = { has_planet_flag = giga_test_site_stage_3 }
			}
			set_planet_flag = giga_test_site_stage_3
		}
		fromfrom.planet = {
			set_planet_flag = has_test_site
		}
	}
	on_dismantle_complete = {
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			giga_dismantle_science_kilo_effect = {
				FLAG = test_site
				TYPE = engineering
			}
		}
		random_system_planet = {
			limit = {
				has_planet_flag = has_test_site
			}
			remove_carrier_flag = has_megastructure
			remove_planet_flag = has_test_site
			set_planet_entity = { entity = giga_test_site_devastated_planet_entity }
		}
		from = {
			add_resource = {
				alloys = 1500
				mult = modifier:megastructure_dismantle_refund_mult
			}
			if = {
				limit = {
					check_variable = {
						which = giga_current_megabase
						value >= 1
					}
				}
				change_variable = {
					which = giga_current_megabase
					value = -1
				}
			}
		}
	}

	ai_weight = {
		factor = 175000

		# policy_route = science_kilo_snowball_core
		# source_object = megastructure:macro_test_site_2
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }
		modifier = { factor = 5 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 11 from = { years_passed > 119 } }
		modifier = { factor = 4 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }
		modifier = { factor = 4 from = { has_technology = giga_tech_macro_scale_weather_manipulation } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = science_kilo_snowball_core; source = common/megastructures/zz_c_macroengineering_test_site.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
macro_test_site_3 = {
	entity = "giga_test_site_4"
	construction_entity = "giga_test_site_stage_4_entity_con"
	portrait = "GFX_megastructure_cybernetics"
	place_entity_on_planet_plane = yes
	scales_with_planet = yes
	use_planet_resource = yes
	construction_blocks_and_blocked_by = none
	show_in_outliner = yes
	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	# Test Model settings
	# entity_offset = { x = 0 y = 0 }
	# scales_with_planet = yes
	upgrade_from = { macro_test_site_2 }
	country_modifier = {
		custom_tooltip = orbital_test_site_4_mod_tooltip
	}
	build_time = 1080 # 3 years
	resources = {
		category = giga_kilostructures
		cost = {
			unity = @science_kilo_unity_4
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = @science_kilo_alloys_4
		}
		upkeep = {
			energy = 50
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Standard empire
					is_gestalt = no
				}
			}
			consumer_goods = 25
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Hivemind / default
					is_gestalt = yes
					is_machine_empire = no
				}
			}
			minerals = 75
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Robot upkeep
					is_gestalt = yes
					is_machine_empire = yes
				}
			}
			energy = 50
		}
	}
	potential = { NOT = { has_global_flag = megabase_disabled } }
	possible = { from = { has_technology = giga_tech_engineering_test_site } }

	on_build_complete = {
		fromfrom = { set_megastructure_flag = giga_outliner_hidden_by_@owner }
		save_event_target_as = giga_system
		from = {
			create_message = {
				type = MEGASTRUCTURE_UPGRADED
				localization = MESSAGE_MEGASTRUCTURE_UPGRADED
				days = 30
				target = from # the Go To
				variable = {
					type = name
					localization = MEGASTRUCTURE
					scope = from
				}
				variable = {
					type = name
					localization = SYSTEM
					scope = root
				}
			}
			if = {
				limit = {
					NOR = {
						has_global_flag = giga_achievements_disabled
						has_country_flag = giga_achievement_55
					}
				}
				set_country_flag = giga_achievement_55
				set_timed_country_flag = { flag = giga_achievement_55_notification days = 30 }
				giga_achievement_sound = yes
			}
		}
		fromfrom = {
			set_name = "name_eng_test_site"
			if = {
				limit = {
					NOT = { has_megastructure_flag = giga_dismantle_ready }
				}
				set_megastructure_flag = giga_dismantle_ready
			}
		}
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			remove_planet_flag = giga_test_site_stage_3
			set_planet_flag = giga_test_site_stage_4
			save_event_target_as = target_planet
			add_deposit = d_engineering_1
			science_kilo_update_orbital_effect = yes
			add_modifier = {
				modifier = orbital_test_site_4_mod
				days = -1
			}
			if = {
				limit = {
					has_modifier = orbital_test_site_3_mod
				}
				remove_modifier = orbital_test_site_3_mod
			}
		}
	}

	dismantle_cost = {
		category = giga_kilostructures
		cost = {
			energy = 2000
		}
	}

	dismantle_time = 360

	dismantle_potential = {
		always = yes
	}

	dismantle_possible = {
		can_dismantle_megastructure = {
			TECH = giga_tech_engineering_test_site
		}
		# custom_tooltip = {
		# 	fail_text = "requires_not_old_update"
		# 	has_megastructure_flag = giga_dismantle_ready
		# }
	}
	on_dismantle_start = { # Catch for old variants of the mega where it hadn't set the proper flags
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
				NOT = { has_planet_flag = giga_test_site_stage_4 }
			}
			set_planet_flag = giga_test_site_stage_4
		}
		fromfrom.planet = {
			set_planet_flag = has_test_site
		}
	}
	on_dismantle_complete = {
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			giga_dismantle_science_kilo_effect = {
				FLAG = test_site
				TYPE = engineering
			}
		}
		random_system_planet = {
			limit = {
				has_planet_flag = has_test_site
			}
			remove_carrier_flag = has_megastructure
			remove_planet_flag = has_test_site
			set_planet_entity = { entity = giga_test_site_devastated_planet_entity }
		}
		from = {
			add_resource = {
				alloys = 2000
				mult = modifier:megastructure_dismantle_refund_mult
			}
			if = {
				limit = {
					check_variable = {
						which = giga_current_megabase
						value >= 1
					}
				}
				change_variable = {
					which = giga_current_megabase
					value = -1
				}
			}
		}
	}

	ai_weight = {
		factor = 190000

		# policy_route = science_kilo_snowball_core
		# source_object = megastructure:macro_test_site_3
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }
		modifier = { factor = 5 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 11 from = { years_passed > 119 } }
		modifier = { factor = 4 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }
		modifier = { factor = 4 from = { has_technology = giga_tech_macro_scale_weather_manipulation } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = science_kilo_snowball_core; source = common/megastructures/zz_c_atmospheric_storm_observatory.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
atmosphere_shredder_0 = {
	entity = "giga_storm_observatory_1"
	construction_entity = "giga_storm_observatory_1_con"
	portrait = "GFX_megastructure_gas_giant"
	place_entity_on_planet_plane = yes
	use_planet_resource = yes
	entity_offset = { x = 0 y = 0 }
	scales_with_planet = yes
	construction_blocks_and_blocked_by = none

	prerequisites = { giga_tech_macro_scale_weather_manipulation }

	build_time = 360
	resources = {
		category = giga_kilostructures
		cost = {
			unity = @science_kilo_cost_1
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = @science_kilo_cost_1
		}
		upkeep = {
			energy = 10
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Standard empire
					is_gestalt = no
				}
			}
			consumer_goods = 5
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Hivemind / default
					is_gestalt = yes
					is_machine_empire = no
				}
			}
			minerals = 15
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Robot upkeep
					is_gestalt = yes
					is_machine_empire = yes
				}
			}
			energy = 10
		}
	}

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_system_tooltip = giga_science_candidate_count
	tooltip_system_score = {
		base = 0
		complex_trigger_modifier = {
			trigger = count_system_planet
			parameters = {
				limit = {
					NOT = { has_deposit_for = shipclass_mining_station }
					is_star = no
					is_astral_scar = no
					colonizable_planet = no
				}
			}
			mode = add
		}
	}
	tooltip_system_score_low_threshold = 10
	tooltip_system_score_high_threshold = 16
	tooltip_best_systems_header = "MEGASTRUCTURE_SCIENCE_KILO_BEST_SYSTEMS_TOOLTIP_HEADER"
	tooltip_system_filter = {
		solar_system = {
			giga_system_has_atmosphere_shredder = no
		}
		system_has_arc_furnace = no
	}

	potential = {
		has_technology = giga_tech_macro_scale_weather_manipulation
		NOT = { has_global_flag = storm_observatory_disabled }
		OR = {
			has_global_flag = storm_observatory_capped_u
			check_variable = {
				which = giga_current_storm_observatory
				value < value:giga_storm_observatory_limit
			}
		}
	}

	possible = {
        inline_script = megastructures/system_ownership_or_waystation_check
		custom_tooltip = { fail_text = "requires_no_anomaly" 				NOT = { any_system_planet = { has_anomaly = yes } } }
		custom_tooltip = { fail_text = "requires_no_arc_furnace" 			system_has_arc_furnace = no }
		custom_tooltip = { fail_text = "requires_no_atmosphere_shredder"	giga_system_has_atmosphere_shredder = no }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = storm_observatory_capped_u
					check_variable = {
						which = giga_current_storm_observatory
						value < value:giga_storm_observatory_limit
					}
				}
			}
		}
	}

	country_modifier = {
		custom_tooltip = orbital_atmosphere_shredder_1_mod_tooltip
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_no_anomaly"				has_anomaly = no }
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"	planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "requires_survey_not_habitable"		is_surveyed = { who = prev.from status = yes } is_planet_habitable = no }
			custom_tooltip = { fail_text = "requires_not_star"					is_star = no }
			custom_tooltip = { fail_text = "must_build_around_gas" 				giga_is_gas_giant = yes }
			custom_tooltip = {
				fail_text = "requires_not_astral_scar"
				is_astral_scar = no
			}
			OR = {
				from = { is_ai = no }
				solar_system = {
					count_system_planet = {
						count >= 8
						limit = {
							giga_is_science_candidate = yes
						}
					}
				}
			}
		}
	}

	on_build_start = {
		from = {
			set_country_flag = is_currently_building_atmosphere_shredder
		}
		set_star_flag = atmosphere_shredder_construction
	}
	on_build_cancel = {
		from = {
			remove_country_flag = is_currently_building_atmosphere_shredder
		}
		remove_star_flag = atmosphere_shredder_construction
	}
	on_build_complete = {
		save_event_target_as = giga_system
		remove_star_flag = atmosphere_shredder_construction
		fromfrom.planet = {
			set_planet_flag = has_atmosphere_shredder
			save_event_target_as = giga_planet
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			giga_set_has_mega_flag = yes
			set_planet_entity = {
				entity = storm_gas_giant_01_entity
			}
		}
		from = {
			set_timed_country_flag = { flag = has_recently_built_atmosphere_shredder years = 20 }
			remove_country_flag = is_currently_building_atmosphere_shredder
			create_message = {
				type = MEGASTRUCTURE_BUILT
				localization = MESSAGE_MEGASTRUCTURE_BUILT
				days = 30
				target = from # the Go To
				variable = {
					type = name
					localization = MEGASTRUCTURE
					scope = from
				}
				variable = {
					type = name
					localization = SYSTEM
					scope = root
				}
			}
			change_variable = { which = giga_current_storm_observatory value = 1 }
		}
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			remove_trade_deposits = yes
			set_planet_flag = giga_atmosphere_shredder_stage_1
			save_event_target_as = target_planet
			add_deposit = d_physics_2
			science_kilo_update_orbital_effect = yes
			# add_modifier = {
			# 	modifier = orbital_atmosphere_shredder_1_mod
			# 	days = -1
			# }
		}
	}

	dismantle_cost = {
		category = giga_kilostructures
		cost = {
			energy = 500
		}
	}

	dismantle_time = 360

	dismantle_potential = {
		always = yes
	}

	dismantle_possible = {
		can_dismantle_megastructure = {
			TECH = giga_tech_macro_scale_weather_manipulation
		}
		# custom_tooltip = {
		# 	fail_text = "requires_not_old_update"
		# 	has_megastructure_flag = giga_dismantle_ready
		# }
	}
	on_dismantle_start = { # Catch for old variants of the mega where it hadn't set the proper flags
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
				NOT = { has_planet_flag = giga_atmosphere_shredder_stage_1 }
			}
			set_planet_flag = giga_atmosphere_shredder_stage_1
		}
		fromfrom.planet = {
			set_planet_flag = has_atmosphere_shredder
		}
	}
	on_dismantle_complete = {
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			giga_dismantle_science_kilo_effect = {
				FLAG = atmosphere_shredder
				TYPE = physics
			}
		}
		random_system_planet = {
			limit = {
				has_planet_flag = has_atmosphere_shredder
			}
			remove_carrier_flag = has_megastructure
			remove_planet_flag = has_atmosphere_shredder
			set_planet_entity = {
				entity = pc_gas_giant
			}
		}
		from = {
			add_resource = {
				alloys = 500
				mult = modifier:megastructure_dismantle_refund_mult
			}
			if = {
				limit = {
					check_variable = {
						which = giga_current_storm_observatory
						value >= 1
					}
				}
				change_variable = {
					which = giga_current_storm_observatory
					value = -1
				}
			}
		}
	}

	ai_weight = {
		factor = 150000

		# policy_route = science_kilo_snowball_core
		# source_object = megastructure:atmosphere_shredder_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }
		modifier = { factor = 5 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 11 from = { years_passed > 119 } }
		modifier = { factor = 4 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }
		modifier = { factor = 4 from = { has_technology = giga_tech_macro_scale_weather_manipulation } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = science_kilo_snowball_core; source = common/megastructures/zz_c_atmospheric_storm_observatory.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
atmosphere_shredder_1 = {
	entity = "giga_storm_observatory_2"
	construction_entity = "giga_storm_observatory_2_con"
	portrait = "GFX_megastructure_gas_giant"
	place_entity_on_planet_plane = yes
	use_planet_resource = yes
	entity_offset = { x = 0 y = 0 }
	scales_with_planet = yes
	upgrade_from = { atmosphere_shredder_0 }
	construction_blocks_and_blocked_by = none


	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1080
	resources = {
		category = giga_kilostructures
		cost = {
			unity = @science_kilo_cost_2
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = @science_kilo_cost_2
		}
		upkeep = {
			energy = 20
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Standard empire
					is_gestalt = no
				}
			}
			consumer_goods = 10
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Hivemind / default
					is_gestalt = yes
					is_machine_empire = no
				}
			}
			minerals = 30
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Robot upkeep
					is_gestalt = yes
					is_machine_empire = yes
				}
			}
			energy = 20
		}
	}

	potential = { NOT = { has_global_flag = storm_observatory_disabled } }
	possible = { from = { has_technology = giga_tech_macro_scale_weather_manipulation } }
	country_modifier = {
		custom_tooltip = orbital_atmosphere_shredder_2_mod_tooltip
	}
	on_build_complete = {
		save_event_target_as = giga_system
		fromfrom.planet = {
			set_planet_entity = {
				entity = storm_gas_giant_01_entity
			}
		}
		from = {
			create_message = {
				type = MEGASTRUCTURE_UPGRADED
				localization = MESSAGE_MEGASTRUCTURE_UPGRADED
				days = 30
				target = from # the Go To
				variable = {
					type = name
					localization = MEGASTRUCTURE
					scope = from
				}
				variable = {
					type = name
					localization = SYSTEM
					scope = root
				}
			}
		}
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			remove_planet_flag = giga_atmosphere_shredder_stage_1
			set_planet_flag = giga_atmosphere_shredder_stage_2
			save_event_target_as = target_planet
			add_deposit = d_physics_2
			science_kilo_update_orbital_effect = yes
		}
	}

	dismantle_cost = {
		category = giga_kilostructures
		cost = {
			energy = 1000
		}
	}

	dismantle_time = 360

	dismantle_potential = {
		always = yes
	}

	dismantle_possible = {
		can_dismantle_megastructure = {
			TECH = giga_tech_macro_scale_weather_manipulation
		}
		# custom_tooltip = {
		# 	fail_text = "requires_not_old_update"
		# 	has_megastructure_flag = giga_dismantle_ready
		# }
	}
	on_dismantle_start = { # Catch for old variants of the mega where it hadn't set the proper flags
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
				NOT = { has_planet_flag = giga_atmosphere_shredder_stage_2 }
			}
			set_planet_flag = giga_atmosphere_shredder_stage_2
		}
		fromfrom.planet = {
			set_planet_flag = has_atmosphere_shredder
		}
	}
	on_dismantle_complete = {
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			giga_dismantle_science_kilo_effect = {
				FLAG = atmosphere_shredder
				TYPE = physics
			}
		}
		random_system_planet = {
			limit = {
				has_planet_flag = has_atmosphere_shredder
			}
			remove_carrier_flag = has_megastructure
			remove_planet_flag = has_atmosphere_shredder
			set_planet_entity = {
				entity = pc_gas_giant
			}
		}
		from = {
			add_resource = {
				alloys = 1000
				mult = modifier:megastructure_dismantle_refund_mult
			}
			if = {
				limit = {
					check_variable = {
						which = giga_current_storm_observatory
						value >= 1
					}
				}
				change_variable = {
					which = giga_current_storm_observatory
					value = -1
				}
			}
		}
	}

	ai_weight = {
		factor = 165000

		# policy_route = science_kilo_snowball_core
		# source_object = megastructure:atmosphere_shredder_1
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }
		modifier = { factor = 5 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 11 from = { years_passed > 119 } }
		modifier = { factor = 4 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }
		modifier = { factor = 4 from = { has_technology = giga_tech_macro_scale_weather_manipulation } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = science_kilo_snowball_core; source = common/megastructures/zz_c_atmospheric_storm_observatory.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
atmosphere_shredder_2 = {
	entity = "giga_storm_observatory_3"
	construction_entity = "giga_storm_observatory_3_con"
	portrait = "GFX_megastructure_gas_giant"
	place_entity_on_planet_plane = yes
	use_planet_resource = yes
	entity_offset = { x = 0 y = 0 }
	scales_with_planet = yes
	upgrade_from = { atmosphere_shredder_1 }
	construction_blocks_and_blocked_by = none

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}
	country_modifier = {
		custom_tooltip = orbital_atmosphere_shredder_3_mod_tooltip
	}
	build_time = 1080
	resources = {
		category = giga_kilostructures
		cost = {
			unity = @science_kilo_unity_3
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = @science_kilo_alloys_3
		}
		upkeep = {
			energy = 40
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Standard empire
					is_gestalt = no
				}
			}
			consumer_goods = 20
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Hivemind / default
					is_gestalt = yes
					is_machine_empire = no
				}
			}
			minerals = 60
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Robot upkeep
					is_gestalt = yes
					is_machine_empire = yes
				}
			}
			energy = 40
		}
	}

	potential = { NOT = { has_global_flag = storm_observatory_disabled } }
	possible = { from = { has_technology = giga_tech_macro_scale_weather_manipulation } }

	on_build_complete = {
		save_event_target_as = giga_system
		fromfrom.planet = {
			set_planet_entity = {
				entity = storm_gas_giant_01_entity
			}
		}
		from = {
			create_message = {
				type = MEGASTRUCTURE_UPGRADED
				localization = MESSAGE_MEGASTRUCTURE_UPGRADED
				days = 30
				target = from # the Go To
				variable = {
					type = name
					localization = MEGASTRUCTURE
					scope = from
				}
				variable = {
					type = name
					localization = SYSTEM
					scope = root
				}
			}
		}
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			remove_planet_flag = giga_atmosphere_shredder_stage_2
			set_planet_flag = giga_atmosphere_shredder_stage_3
			save_event_target_as = target_planet
			add_deposit = d_physics_1
			science_kilo_update_orbital_effect = yes
			add_modifier = {
				modifier = orbital_atmosphere_shredder_3_mod
				days = -1
			}
		}
	}

	dismantle_cost = {
		category = giga_kilostructures
		cost = {
			energy = 1500
		}
	}

	dismantle_time = 360

	dismantle_potential = {
		always = yes
	}

	dismantle_possible = {
		can_dismantle_megastructure = {
			TECH = giga_tech_macro_scale_weather_manipulation
		}
		# custom_tooltip = {
		# 	fail_text = "requires_not_old_update"
		# 	has_megastructure_flag = giga_dismantle_ready
		# }
	}
	on_dismantle_start = { # Catch for old variants of the mega where it hadn't set the proper flags
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
				NOT = { has_planet_flag = giga_atmosphere_shredder_stage_3 }
			}
			set_planet_flag = giga_atmosphere_shredder_stage_3
		}
		fromfrom.planet = {
			set_planet_flag = has_atmosphere_shredder
		}
	}
	on_dismantle_complete = {
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			giga_dismantle_science_kilo_effect = {
				FLAG = atmosphere_shredder
				TYPE = physics
			}
		}
		random_system_planet = {
			limit = {
				has_planet_flag = has_atmosphere_shredder
			}
			remove_carrier_flag = has_megastructure
			remove_planet_flag = has_atmosphere_shredder
			set_planet_entity = {
				entity = pc_gas_giant
			}
		}
		from = {
			add_resource = {
				alloys = 1500
				mult = modifier:megastructure_dismantle_refund_mult
			}
			if = {
				limit = {
					check_variable = {
						which = giga_current_storm_observatory
						value >= 1
					}
				}
				change_variable = {
					which = giga_current_storm_observatory
					value = -1
				}
			}
		}
	}

	ai_weight = {
		factor = 180000

		# policy_route = science_kilo_snowball_core
		# source_object = megastructure:atmosphere_shredder_2
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }
		modifier = { factor = 5 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 11 from = { years_passed > 119 } }
		modifier = { factor = 4 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }
		modifier = { factor = 4 from = { has_technology = giga_tech_macro_scale_weather_manipulation } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = science_kilo_snowball_core; source = common/megastructures/zz_c_atmospheric_storm_observatory.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
atmosphere_shredder_3 = {
	entity = "giga_storm_observatory_4"
	construction_entity = "giga_storm_observatory_4_con"
	portrait = "GFX_megastructure_gas_giant"
	place_entity_on_planet_plane = yes
	use_planet_resource = yes
	entity_offset = { x = 0 y = 0 }
	scales_with_planet = yes
	upgrade_from = { atmosphere_shredder_2 }
	construction_blocks_and_blocked_by = none
	show_in_outliner = yes

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}
	country_modifier = {
		custom_tooltip = orbital_atmosphere_shredder_4_mod_tooltip
	}
	build_time = 1080 # 3 years
	resources = {
		category = giga_kilostructures
		cost = {
			unity = @science_kilo_unity_4
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = @science_kilo_alloys_4
		}

		upkeep = {
			energy = 50
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Standard empire
					is_gestalt = no
				}
			}
			consumer_goods = 25
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Hivemind / default
					is_gestalt = yes
					is_machine_empire = no
				}
			}
			minerals = 75
		}
		upkeep = {
			trigger = {
				exists = owner
				owner = { # Robot upkeep
					is_gestalt = yes
					is_machine_empire = yes
				}
			}
			energy = 50
		}
	}

	potential = { NOT = { has_global_flag = storm_observatory_disabled } }
	possible = { from = { has_technology = giga_tech_macro_scale_weather_manipulation } }

	on_build_complete = {
		fromfrom = {
			set_megastructure_flag = giga_outliner_hidden_by_@owner
		}
		save_event_target_as = giga_system
		fromfrom.planet = {
			set_planet_entity = {
				entity = storm_gas_giant_02_entity
			}
		}
		from = {
			create_message = {
				type = MEGASTRUCTURE_UPGRADED
				localization = MESSAGE_MEGASTRUCTURE_UPGRADED
				days = 30
				target = from # the Go To
				variable = {
					type = name
					localization = MEGASTRUCTURE
					scope = from
				}
				variable = {
					type = name
					localization = SYSTEM
					scope = root
				}
			}
			if = {
				limit = {
					NOR = {
						has_global_flag = giga_achievements_disabled
						has_country_flag = giga_achievement_53
					}
				}
				set_country_flag = giga_achievement_53
				set_timed_country_flag = { flag = giga_achievement_53_notification days = 30 }
				giga_achievement_sound = yes
			}
		}
		fromfrom = {
			set_name = "atmosphere_shredder_complete_name"
		}
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			remove_planet_flag = giga_atmosphere_shredder_stage_3
			set_planet_flag = giga_atmosphere_shredder_stage_4
			save_event_target_as = target_planet
			add_deposit = d_physics_1
			science_kilo_update_orbital_effect = yes
			add_modifier = {
				modifier = orbital_atmosphere_shredder_4_mod
				days = -1
			}
			if = {
				limit = {
					has_modifier = orbital_atmosphere_shredder_3_mod
				}
				remove_modifier = orbital_atmosphere_shredder_3_mod
			}
		}
	}

	dismantle_cost = {
		category = giga_kilostructures
		cost = {
			energy = 2000
		}
	}

	dismantle_time = 360

	dismantle_potential = {
		always = yes
	}

	dismantle_possible = {
		can_dismantle_megastructure = {
			TECH = giga_tech_macro_scale_weather_manipulation
		}
		# custom_tooltip = {
		# 	fail_text = "requires_not_old_update"
		# 	has_megastructure_flag = giga_dismantle_ready
		# }
	}
	on_dismantle_start = { # Catch for old variants of the mega where it hadn't set the proper flags
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
				NOT = { has_planet_flag = giga_atmosphere_shredder_stage_4 }
			}
			set_planet_flag = giga_atmosphere_shredder_stage_4
		}
		fromfrom.planet = {
			set_planet_flag = has_atmosphere_shredder
		}
	}
	on_dismantle_complete = {
		every_system_planet = {
			limit = {
				giga_is_science_candidate = yes
			}
			giga_dismantle_science_kilo_effect = {
				FLAG = atmosphere_shredder
				TYPE = physics
			}
		}
		random_system_planet = {
			limit = {
				has_planet_flag = has_atmosphere_shredder
			}
			remove_carrier_flag = has_megastructure
			remove_planet_flag = has_atmosphere_shredder
			set_planet_entity = {
				entity = pc_gas_giant
			}
		}
		from = {
			add_resource = {
				alloys = 2000
				mult = modifier:megastructure_dismantle_refund_mult
			}
			if = {
				limit = {
					check_variable = {
						which = giga_current_storm_observatory
						value >= 1
					}
				}
				change_variable = {
					which = giga_current_storm_observatory
					value = -1
				}
			}
		}
	}

	ai_weight = {
		factor = 195000

		# policy_route = science_kilo_snowball_core
		# source_object = megastructure:atmosphere_shredder_3
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }
		modifier = { factor = 5 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 11 from = { years_passed > 119 } }
		modifier = { factor = 4 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }
		modifier = { factor = 4 from = { has_technology = giga_tech_macro_scale_weather_manipulation } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = research_megastructure_core; source = common/megastructures/zz_e_science_nexus.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
think_tank_0 = {
	entity = "construction_platform_entity"
	construction_entity = "construction_platform_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	entity_offset = { x = 0 y = -20 }
	prerequisites = { "tech_science_nexus" }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_science_nexus
		cost = {
			unity = @giga_big_mega_start_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 5000
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|alloys|AMOUNT|5000| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|unity|AMOUNT|@giga_big_mega_start_unity_cost| }
		upkeep = { energy = 5 }
	}

	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = alloys AMOUNT = 5000 }
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = unity  AMOUNT = @giga_big_mega_start_unity_cost }
	}
	on_build_cancel = {
		giga_ai_savings_refund = { CATEGORY = important RESOURCE = alloys }
		giga_ai_savings_refund = { CATEGORY = important RESOURCE = unity }
	}

	potential = {
		NOT = { has_global_flag = vanilla_nexus_disabled }
		OR = {
			has_global_flag = vanilla_nexus_capped_u
			check_variable = {
				which = giga_current_vanilla_nexus
				value < value:giga_vanilla_nexus_limit
			}
		}
	}

	possible = {
		hidden_trigger = {
			exists = starbase
		}
		custom_tooltip = { fail_text = "requires_inside_border"						is_inside_border = from }
		custom_tooltip = { fail_text = "requires_surveyed_system"					giga_system_is_surveyed = yes }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = vanilla_nexus_capped_u
					check_variable = {
						which = giga_current_vanilla_nexus
						value < value:giga_vanilla_nexus_limit
					}
				}
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_survey_not_habitable"		is_surveyed = { who = prev.from status = yes } is_planet_habitable = no }
			custom_tooltip = { fail_text = "requires_no_anomaly"				has_anomaly = no }
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"	planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "requires_not_star"					is_star = no }
			custom_tooltip = {
				fail_text = "requires_not_astral_scar"
				is_astral_scar = no
			}
			custom_tooltip = { fail_text = "requires_not_ring_world"			is_ringworld = no }
		}
	}


	on_build_complete = {
		set_star_flag = think_tank_built
		from = {
			set_timed_country_flag = { flag = has_recently_built_think_tank years = 20 }
			set_country_flag = built_think_tank
			change_variable = { which = giga_current_vanilla_nexus value = 1 }
		}
		fromfrom.planet = {
			giga_set_has_mega_flag = yes
		}
	}

	ai_weight = {
		factor = 155000

		# policy_route = research_megastructure_core
		# source_object = megastructure:think_tank_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_nexus_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_nexus_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 7 from = { years_passed > 79 } }
		modifier = { factor = 10 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 4 from = { has_technology = tech_science_nexus } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = research_megastructure_core; source = common/megastructures/zz_e_science_nexus.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
think_tank_1 = {
	entity = "thinktank_phase_01_entity"
	construction_entity = "thinktank_phase_01_entity"
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	entity_offset = { x = 0 y = -20 }
	upgrade_from = { think_tank_0 }
	prerequisites = { "tech_science_nexus" }
	country_modifier = { all_technology_research_speed = 0.05 }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 3600
	resources = {
		category = giga_megastructures
		cost = {
			unity = @giga_big_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 15000
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|alloys|AMOUNT|15000| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|unity|AMOUNT|@giga_big_mega_unity_cost| }
		upkeep = { energy = 25 }
		produces = {
			society_research = 100
			engineering_research = 100
			physics_research = 100
		}
	}
	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = alloys AMOUNT = 15000 }
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = unity  AMOUNT = @giga_big_mega_unity_cost }
	}

	ai_weight = {
		factor = 170000

		# policy_route = research_megastructure_core
		# source_object = megastructure:think_tank_1
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_nexus_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_nexus_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 7 from = { years_passed > 79 } }
		modifier = { factor = 10 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = tech_science_nexus } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = research_megastructure_core; source = common/megastructures/zz_e_science_nexus.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
think_tank_2 = {
	entity = "thinktank_phase_02_entity"
	construction_entity = "thinktank_phase_02_entity"
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	entity_offset = { x = 0 y = -20 }
	upgrade_from = { think_tank_1 }
	prerequisites = { "tech_science_nexus" }
	country_modifier = { all_technology_research_speed = 0.10 }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 3600
	resources = {
		category = giga_megastructures
		cost = {
			unity = @giga_big_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 15000
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|alloys|AMOUNT|15000| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|unity|AMOUNT|@giga_big_mega_unity_cost| }
		upkeep = { energy = 50 }
		produces = {
			society_research = 200
			engineering_research = 200
			physics_research = 200
		}
	}
	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = alloys AMOUNT = 15000 }
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = unity  AMOUNT = @giga_big_mega_unity_cost }
	}

	ai_weight = {
		factor = 185000

		# policy_route = research_megastructure_core
		# source_object = megastructure:think_tank_2
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_nexus_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_nexus_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 7 from = { years_passed > 79 } }
		modifier = { factor = 10 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = tech_science_nexus } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = research_megastructure_core; source = common/megastructures/zz_e_science_nexus.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
think_tank_3 = {
	entity = "thinktank_phase_03_entity"
	construction_entity = "thinktank_phase_03_entity"
	portrait = "GFX_megastructure_think_tank_background"
	place_entity_on_planet_plane = no
	entity_offset = { x = 0 y = -20 }
	upgrade_from = { think_tank_2 }
	prerequisites = { "tech_science_nexus" }
	show_prereqs = yes
	country_modifier = { all_technology_research_speed = 0.15 }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 3600
	resources = {
		category = giga_megastructures
		cost = {
			unity = @giga_big_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 15000
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|alloys|AMOUNT|15000| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|unity|AMOUNT|@giga_big_mega_unity_cost| }
		upkeep = { energy = 75 }
		produces = {
			society_research = 300
			engineering_research = 300
			physics_research = 300
		}
	}
	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = alloys AMOUNT = 15000 }
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = unity  AMOUNT = @giga_big_mega_unity_cost }
	}

	on_build_complete = { from = { set_country_flag = has_built_or_repaired_megastructure } }

	ai_weight = {
		factor = 200000

		# policy_route = research_megastructure_core
		# source_object = megastructure:think_tank_3
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_science_nexus_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_science_nexus_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 7 from = { years_passed > 79 } }
		modifier = { factor = 10 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = tech_science_nexus } }
		modifier = { factor = 3 from = { staid_research_under_curve = yes } }
	}
}


# policy_route = ring_world_growth_core; source = common/megastructures/zz_e_ring_world.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
ring_world_1 = {
	entity = "construction_platform_entity"
	construction_entity = "construction_platform_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = yes
	prerequisites = { "tech_ring_world" }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_megastructures
		cost = {
			influence = 300
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 5000
		}
		upkeep = { energy = 5 }
	}

	custom_tooltip_requirements = "MEGASTRUCTURE_TOOLTIP_REQUIREMENTS_RING_WORLD"

	potential = {
		NOT = { has_global_flag = vanilla_ringworld_disabled }
		giga_can_use_habitables = yes
		OR = {
			has_global_flag = vanilla_ringworld_capped_u
			check_variable = {
				which = giga_current_vanilla_ringworld
				value < value:giga_vanilla_ringworld_limit
			}
		}
	}

	possible = {
		custom_tooltip = { fail_text = "requires_inside_border"						is_inside_border = from }
		custom_tooltip = { fail_text = "requires_surveyed_system"					giga_system_is_surveyed = yes }
		custom_tooltip = { fail_text = "requires_no_habitable_planets"				giga_any_hab_planets = no }
		custom_tooltip = { fail_text = "requires_no_binary_trinary"					giga_is_bitrinary = no }
		custom_tooltip = {
			fail_text = "requires_no_existing_megastructure"
			if = {
				limit = {
					star = {
						has_carrier_flag = has_stabilised_penrose_sphere
					}
				}
				giga_has_normal_ringworld = no
			}
			else = { has_no_non_gate_megastructure = yes }
		}
		if = { limit = { star = { has_carrier_flag = has_stabilised_penrose_sphere } } from = { has_technology = giga_tech_penrose_sphere_3 } }
		custom_tooltip = {
			fail_text = "requires_no_existing_megastructure"
			NOT = {
				any_system_planet = {
					OR = {
						is_planet_class = pc_ringworld_habitable_damaged
						is_planet_class = pc_ringworld_tech_damaged
						is_planet_class = pc_ringworld_seam_damaged
						is_planet_class = pc_shattered_ring_habitable
						is_planet_class = pc_ringworld_habitable
					}
				}
			}
		} # Shattered Ring System
		custom_tooltip = { fail_text = "requires_no_crisis_system"					NOT = { any_system_planet = { has_planet_flag = crisis_vital_planet } } }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = vanilla_ringworld_capped_u
					check_variable = {
						which = giga_current_vanilla_ringworld
						value < value:giga_vanilla_ringworld_limit
					}
				}
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "must_build_around_star"					is_star = yes }
			custom_tooltip = { fail_text = "requires_no_anomaly"					has_anomaly = no }
			# custom_tooltip = { fail_text = "requires_planets_for_material"			hidden:solar_system = { any_system_planet = { NOT = { is_star = yes } } } }
			custom_tooltip = {
				fail_text = "requires_standard_planet_class"
				OR = {
					giga_is_standard_star = yes
					AND = {
						giga_is_standard_black_hole = yes
						has_carrier_flag = has_stabilised_penrose_sphere
					}
				}
			}
		}
	}


    on_build_start = {
        set_star_flag = giga_forbid_planet_dismantlement
    }

    on_build_cancel = {
        remove_star_flag = giga_forbid_planet_dismantlement
    }

	on_build_complete = {
		set_variable = { which = ring_segments value = 0 }

		inline_script = {
			script = megastructures/generic_parts/giga_mega_bulk_matter_calculations
			giga_system_bm_cost = @ring_world_2_intermediate_bm_cost
		}

		from = {
			set_timed_country_flag = { flag = has_recently_built_vanilla_ring years = 20 }
			set_country_flag = giga_started_ringworld
			change_variable = { which = giga_current_vanilla_ringworld value = 1 }
		}

		fromfrom.planet = {
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			giga_set_has_mega_flag = yes
		}
	}

	ai_weight = {
		factor = 145000

		# policy_route = ring_world_growth_core
		# source_object = megastructure:ring_world_1
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_ring_world_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_ring_world_build_priority_ready = yes } }
		modifier = { factor = 3 from = { years_passed > 44 } }
		modifier = { factor = 6 from = { years_passed > 79 } }
		modifier = { factor = 9 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 4 from = { has_technology = tech_ring_world } }
		modifier = { factor = 2 from = { staid_planetary_capacity_growth_ready = yes } }
	}
}


# policy_route = ring_world_growth_core; source = common/megastructures/zz_e_ring_world.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
ring_world_2_intermediate = {
	entity = ""
	construction_entity = "vanilla_full_entity"
	portrait = "GFX_megastructure_construction_background"
	upgrade_from = { ring_world_1 }
	prerequisites = { "tech_ring_world" }
	show_in_outliner = no

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 4800
	resources = {
		category = giga_megastructures
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 10000
		}
	}


	possible = {
		has_enough_bm = yes
	}

	on_build_start = {
		remove_bm_cost_from_stockpile = yes
		if = {
			limit = {
				from = {
					NOR = {
						graphical_culture = arthropoid_01
						graphical_culture = avian_01
						graphical_culture = fungoid_01
						graphical_culture = humanoid_01
						graphical_culture = mammalian_01
						graphical_culture = molluscoid_01
						graphical_culture = plantoid_01
						graphical_culture = reptilian_01
						graphical_culture = lithoid_01
						graphical_culture = necroid_01
					}
				}
			}
			fromfrom = { set_graphical_culture = mammalian_01 }
		}
		else = { fromfrom = { set_graphical_culture = root.from } }
		set_variable = { which = ring_segments value = 0 }
	}

	on_build_complete = {
		giga_remove_system_planets = yes
		giga_remove_system_debris = yes
		set_asteroid_belt = { radius = 0 }
		remove_megastructure = fromfrom
		generate_bulk_matter_cache = yes

		spawn_megastructure = { name = "Ring Section A" type = "ring_world_2" orbit_angle = 0	orbit_distance = 45 owner = from graphical_culture = fromfrom }
		spawn_megastructure = { name = "Ring Section B" type = "ring_world_2" orbit_angle = 90	orbit_distance = 45 owner = from graphical_culture = fromfrom }
		spawn_megastructure = { name = "Ring Section C" type = "ring_world_2" orbit_angle = 180	orbit_distance = 45 owner = from graphical_culture = fromfrom }
		spawn_megastructure = { name = "Ring Section D" type = "ring_world_2" orbit_angle = 270	orbit_distance = 45 owner = from graphical_culture = fromfrom }
	}

	ai_weight = {
		factor = 160000

		# policy_route = ring_world_growth_core
		# source_object = megastructure:ring_world_2_intermediate
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_ring_world_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_ring_world_build_priority_ready = yes } }
		modifier = { factor = 3 from = { years_passed > 44 } }
		modifier = { factor = 6 from = { years_passed > 79 } }
		modifier = { factor = 9 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = tech_ring_world } }
		modifier = { factor = 2 from = { staid_planetary_capacity_growth_ready = yes } }
	}
}


# policy_route = ring_world_growth_core; source = common/megastructures/zz_e_ring_world.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
ring_world_3_intermediate = {
	entity = ""
	construction_entity = "vanilla_quarter_construction_entity"
	portrait = "GFX_megastructure_construction_background"
	upgrade_from = { ring_world_2 }
	prerequisites = { "tech_ring_world" }
	#show_prereqs = yes # needs to be a fake entry instead for tech swaps :(
	prereq_name = "RING_WORLD_SHOW_NAME"
	show_in_outliner = no

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 3600
	resources = {
		category = giga_megastructures
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 10000
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_bulk_matter_cost
			giga_sr_bulk_matter = @ring_world_3_intermediate_bm_cost
		}
	}

	on_build_complete = {
		from = { set_country_flag = has_built_or_repaired_megastructure }

		change_variable = { which = ring_segments value = 1 }
		if = {
			limit = { check_variable = { which = ring_segments value >= 4 } }
			set_variable = { which = ring_segments value = 0 }
			from = {
				remove_country_flag = giga_started_ringworld
				change_variable = { which = completed_ringworlds value = 1 }
			}
			set_star_flag = ring_world_built
		}

		spawn_planet = {
			class = "pc_ringworld_tech"
			location = fromfrom
			orbit_angle_offset = 30
			init_effect = {
				set_name = "Ring Section"
				giga_set_ringworld_graphical_culture = {
					TARGET = this
					SOURCE = prev.from
					SIZE = vanilla
					TYPE = tech
					VANILLA_TYPE = tech
				}
				set_surveyed = { surveyed = yes surveyor = from }
				set_all_comms_surveyed = yes
				set_planet_flag = forbid_guillis_planet_modifiers
				set_carrier_flag = megastructure
				set_carrier_flag = colony_event			# Vanilla uses to prevent unwanted events on planets
			}
		}
		spawn_planet = {
			class = "pc_ringworld_seam"
			location = fromfrom
			init_effect = {
				set_name = "Ring Section"
				giga_set_ringworld_graphical_culture = {
					TARGET = this
					SOURCE = prev.from
					SIZE = vanilla
					TYPE = seam
					VANILLA_TYPE = seam
				}
				set_surveyed = { surveyed = yes surveyor = from }
				set_all_comms_surveyed = yes
				set_planet_flag = forbid_guillis_planet_modifiers
				set_carrier_flag = megastructure
			}
		}
		spawn_planet = {
			class = "pc_ringworld_habitable"
			location = fromfrom
			orbit_angle_offset = -30
			init_effect = {
				giga_set_ringworld_graphical_culture = {
					TARGET = this
					SOURCE = prev.from
					SIZE = vanilla
					TYPE = gaia_habitable
					VANILLA_TYPE = habitable
				}
				set_surveyed = { surveyed = yes surveyor = from }
				set_all_comms_surveyed = yes
				clear_blockers = yes
				save_event_target_as = ring_section
				trigger_megastructure_icon = yes
				set_planet_flag = forbid_guillis_planet_modifiers
				set_carrier_flag = megastructure
				set_carrier_flag = colony_event			# Vanilla uses to prevent unwanted events on planets
				set_planet_flag = giga_ringworld_van

				giga_start_ai_colony_if_safe = yes
			}
		}
		if = {		limit = { NOT = { has_star_flag = ring_01 } } set_star_flag = ring_01 event_target:ring_section = { set_name = "Habitable Section A" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_02 } } set_star_flag = ring_02 event_target:ring_section = { set_name = "Habitable Section B" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_03 } } set_star_flag = ring_03 event_target:ring_section = { set_name = "Habitable Section C" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_04 } } set_star_flag = ring_04 event_target:ring_section = { set_name = "Habitable Section D" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_05 } } set_star_flag = ring_05 event_target:ring_section = { set_name = "Habitable Section E" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_06 } } set_star_flag = ring_06 event_target:ring_section = { set_name = "Habitable Section F" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_07 } } set_star_flag = ring_07 event_target:ring_section = { set_name = "Habitable Section G" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_08 } } set_star_flag = ring_08 event_target:ring_section = { set_name = "Habitable Section H" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_09 } } set_star_flag = ring_09 event_target:ring_section = { set_name = "Habitable Section I" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_10 } } set_star_flag = ring_10 event_target:ring_section = { set_name = "Habitable Section J" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_11 } } set_star_flag = ring_11 event_target:ring_section = { set_name = "Habitable Section K" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_12 } } set_star_flag = ring_12 event_target:ring_section = { set_name = "Habitable Section L" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_13 } } set_star_flag = ring_13 event_target:ring_section = { set_name = "Habitable Section M" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_14 } } set_star_flag = ring_14 event_target:ring_section = { set_name = "Habitable Section N" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_15 } } set_star_flag = ring_15 event_target:ring_section = { set_name = "Habitable Section O" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_16 } } set_star_flag = ring_16 event_target:ring_section = { set_name = "Habitable Section P" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_17 } } set_star_flag = ring_17 event_target:ring_section = { set_name = "Habitable Section Q" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_18 } } set_star_flag = ring_18 event_target:ring_section = { set_name = "Habitable Section R" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_19 } } set_star_flag = ring_19 event_target:ring_section = { set_name = "Habitable Section S" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_20 } } set_star_flag = ring_20 event_target:ring_section = { set_name = "Habitable Section T" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_21 } } set_star_flag = ring_21 event_target:ring_section = { set_name = "Habitable Section U" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_22 } } set_star_flag = ring_22 event_target:ring_section = { set_name = "Habitable Section V" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_23 } } set_star_flag = ring_23 event_target:ring_section = { set_name = "Habitable Section W" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_24 } } set_star_flag = ring_24 event_target:ring_section = { set_name = "Habitable Section X" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_25 } } set_star_flag = ring_25 event_target:ring_section = { set_name = "Habitable Section Y" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_26 } } set_star_flag = ring_26 event_target:ring_section = { set_name = "Habitable Section Z" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_27 } } set_star_flag = ring_27 event_target:ring_section = { set_name = "Habitable Section Aa" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_28 } } set_star_flag = ring_28 event_target:ring_section = { set_name = "Habitable Section Ab" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_29 } } set_star_flag = ring_29 event_target:ring_section = { set_name = "Habitable Section Ac" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_30 } } set_star_flag = ring_30 event_target:ring_section = { set_name = "Habitable Section Ad" } }
		else_if = {	limit = { NOT = { has_star_flag = ring_31 } } set_star_flag = ring_31 event_target:ring_section = { set_name = "Habitable Section Ae" } }
		else_if = {
			limit = { NOT = { has_star_flag = ring_32 } }
			set_star_flag = ring_32
			event_target:ring_section = { set_name = "Habitable Section Af" }
			remove_star_flag = ring_01
			remove_star_flag = ring_02
			remove_star_flag = ring_03
			remove_star_flag = ring_04
			remove_star_flag = ring_05
			remove_star_flag = ring_06
			remove_star_flag = ring_07
			remove_star_flag = ring_08
			remove_star_flag = ring_09
			remove_star_flag = ring_10
			remove_star_flag = ring_11
			remove_star_flag = ring_12
			remove_star_flag = ring_13
			remove_star_flag = ring_14
			remove_star_flag = ring_15
			remove_star_flag = ring_16
			remove_star_flag = ring_17
			remove_star_flag = ring_18
			remove_star_flag = ring_19
			remove_star_flag = ring_20
			remove_star_flag = ring_21
			remove_star_flag = ring_22
			remove_star_flag = ring_23
			remove_star_flag = ring_24
			remove_star_flag = ring_25
			remove_star_flag = ring_26
			remove_star_flag = ring_27
			remove_star_flag = ring_28
			remove_star_flag = ring_29
			remove_star_flag = ring_30
			remove_star_flag = ring_31
			remove_star_flag = ring_32
		}
		remove_megastructure = fromfrom
	}

	ai_weight = {
		factor = 175000

		# policy_route = ring_world_growth_core
		# source_object = megastructure:ring_world_3_intermediate
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_ring_world_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_ring_world_build_priority_ready = yes } }
		modifier = { factor = 3 from = { years_passed > 44 } }
		modifier = { factor = 6 from = { years_passed > 79 } }
		modifier = { factor = 9 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = tech_ring_world } }
		modifier = { factor = 2 from = { staid_planetary_capacity_growth_ready = yes } }
	}
}


# policy_route = storage_cap_core; source = common/megastructures/zz_c_kugelblitz.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
kugelblitz_0 = {
	entity = "kugelblitz_new_empty_entity"
	construction_entity = "kugelblitz_new_empty_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	prerequisites = { giga_tech_kugelblitz }
	construction_blocks_and_blocked_by = none

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_kilostructures
		cost = {
			unity = @giga_small_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 5000
		}
		upkeep = {
			alloys = 5
		}
	}

	potential = {
		has_technology = giga_tech_kugelblitz
		NOT = { has_global_flag = kugel_disabled }
		OR = {
			has_global_flag = kugel_capped_u
			check_variable = {
				which = giga_current_kugel
				value < value:giga_kugel_limit
			}
		}
	}

	possible = {
		custom_tooltip = { fail_text = "requires_inside_border" is_inside_border = from }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = kugel_capped_u
					check_variable = {
						which = giga_current_kugel
						value < value:giga_kugel_limit
					}
				}
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"	planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "requires_no_anomaly"				has_anomaly = no }
			custom_tooltip = { fail_text = "requires_not_star"					is_star = no }
			custom_tooltip = {
				fail_text = "requires_not_astral_scar"
				is_astral_scar = no
			}
		}
	}


	on_build_start = {
		from = {
			set_country_flag = is_currently_building_kugelblitz
		}
	}
	on_build_cancel = {
		from = {
			remove_country_flag = is_currently_building_kugelblitz
		}
	}

	on_build_complete = {
		save_event_target_as = giga_system
		fromfrom.planet = {
			save_event_target_as = giga_planet
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			giga_set_has_mega_flag = yes
		}
		from = {
			set_timed_country_flag = { flag = has_recently_built_kugelblitz years = 20 }
			remove_country_flag = is_currently_building_kugelblitz
			# country_event = { id = giga_dialog.101 }	# Notification
			# country_event = { id = giga_dialog.102 }	# Notification
			change_variable = { which = giga_current_kugel value = 1 }
		}
	}

	ai_weight = {
		factor = 125000

		# policy_route = storage_cap_core
		# source_object = megastructure:kugelblitz_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_kugelblitz_new_start_budget_ready = yes } } }
		modifier = { factor = 4 from = { staid_kugelblitz_new_start_budget_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 7 from = { years_passed > 79 } }
		modifier = { factor = 10 from = { years_passed > 119 } }
		# kugelblitz_start_budget = empty_silos_are_capped_storage_not_income
		modifier = { factor = 0 from = { has_country_flag = is_currently_building_kugelblitz } }
		modifier = { factor = 0 from = { staid_unfinished_kugelblitz_exists = yes } }
		modifier = { factor = 0 from = { check_variable = { which = giga_current_kugel value >= 10 } } }
		modifier = { factor = 0.03 from = { has_country_flag = has_recently_built_kugelblitz } }
		modifier = { factor = 0.02 from = { check_variable = { which = giga_current_kugel value >= 9 } } }
		modifier = { factor = 0.04 from = { check_variable = { which = giga_current_kugel value >= 8 } } }
		modifier = { factor = 0.08 from = { check_variable = { which = giga_current_kugel value >= 7 } } }
		modifier = { factor = 0.15 from = { check_variable = { which = giga_current_kugel value >= 6 } } }
		modifier = { factor = 0.25 from = { check_variable = { which = giga_current_kugel value >= 5 } } }
		modifier = { factor = 0.4 from = { check_variable = { which = giga_current_kugel value >= 4 } } }
		modifier = { factor = 0.6 from = { check_variable = { which = giga_current_kugel value >= 3 } } }
	}
}


# policy_route = storage_cap_core; source = common/megastructures/zz_c_kugelblitz.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
kugelblitz_1 = {
	entity = "kugelblitz_new_entity"
	portrait = "GFX_megastructure_black_hole"
	place_entity_on_planet_plane = no
	construction_blocks_and_blocked_by = none
	upgrade_from = { kugelblitz_0 kugelblitz_restored }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_kilostructures
		cost = {
			energy = 25000
			unity = @giga_small_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 1000
		}
		upkeep = {
			alloys = 15
			energy = 50
		}
	}

	potential = { NOT = { has_global_flag = kugel_disabled } }
	possible = { from = { has_technology = giga_tech_kugelblitz } }

	country_modifier = { country_resource_max_add = 50000 }

	on_build_complete = {
		save_event_target_as = giga_system
		if = { limit = { exists = fromfrom.planet } fromfrom.planet = { save_event_target_as = giga_planet } }
		from = {
			country_event = { id = giga_dialog.103 }	# Notification
			if = {
				limit = {
					NOR = {
						has_global_flag = giga_achievements_disabled
						has_country_flag = giga_achievement_64
					}
				}
				set_country_flag = giga_achievement_64
				set_timed_country_flag = { flag = giga_achievement_64_notification days = 30 }
				giga_achievement_sound = yes
			}
		}
	}

	ai_weight = {
		factor = 150000

		# policy_route = storage_cap_core
		# source_object = megastructure:kugelblitz_1
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_storage_cap_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_storage_cap_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 7 from = { years_passed > 79 } }
		modifier = { factor = 10 from = { years_passed > 119 } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = giga_tech_kugelblitz } }
		modifier = { factor = 10 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 14 from = { staid_high_scale_snowball_pressure = yes } }
	}
}


# policy_route = storage_cap_core; source = common/megastructures/zz_c_kugelblitz.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
kugelblitz_2 = { # Megastructur
	entity = "kugelblitz_mega_entity"
	portrait = "GFX_megastructure_black_hole"
	place_entity_on_planet_plane = no
	upgrade_from = { kugelblitz_1 }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 3600
	resources = {
		category = giga_megastructures
		cost = {
			energy = 37500
			unity = @giga_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 2500
		}
		upkeep = {
			alloys = 20
			energy = 75
		}
	}

	potential = { NOT = { has_global_flag = kugel_disabled } }
	possible = { from = { has_technology = giga_tech_kugelblitz has_technology = tech_mega_engineering } }

	country_modifier = { country_resource_max_add = 150000 }

	on_build_complete = {
		save_event_target_as = giga_system
		if = { limit = { exists = fromfrom.planet } fromfrom.planet = { save_event_target_as = giga_planet } }
		from = {
			save_event_target_as = giga_system_owner
			set_country_flag = has_built_or_repaired_megastructure
			country_event = { id = giga_dialog.106 }	# Notification
			if = {
				limit = {
					NOR = {
						has_global_flag = giga_achievements_disabled
						has_country_flag = giga_achievement_64
					}
				}
				set_country_flag = giga_achievement_64
				set_timed_country_flag = { flag = giga_achievement_64_notification days = 30 }
				giga_achievement_sound = yes
			}
		}
	}

	ai_weight = {
		factor = 170000

		# policy_route = storage_cap_core
		# source_object = megastructure:kugelblitz_2
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_storage_cap_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_storage_cap_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 7 from = { years_passed > 79 } }
		modifier = { factor = 10 from = { years_passed > 119 } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = giga_tech_kugelblitz } }
		modifier = { factor = 10 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 14 from = { staid_high_scale_snowball_pressure = yes } }
	}
}


# policy_route = storage_cap_core; source = common/megastructures/zz_c_kugelblitz.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
kugelblitz_3 = { # Gigastructur
	entity = "kugelblitz_giga_entity"
	portrait = "GFX_megastructure_black_hole"
	place_entity_on_planet_plane = no
	upgrade_from = { kugelblitz_2 }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 5400
	resources = {
		category = giga_gigastructures
		cost = {
			energy = 75000
			unity = @giga_big_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 5000
		}
		upkeep = {
			alloys = 25
			energy = 100
		}
	}

	potential = { NOT = { has_global_flag = kugel_disabled } }
	possible = { from = { has_technology = giga_tech_kugelblitz has_technology = giga_tech_tetradimensional_engineering } }

	country_modifier = { country_resource_max_add = 500000 }

	on_build_complete = {
		save_event_target_as = giga_system
		if = { limit = { exists = fromfrom.planet } fromfrom.planet = { save_event_target_as = giga_planet } }
		from = {
			set_country_flag = has_built_or_repaired_megastructure
			country_event = { id = giga_dialog.107 }	# Notification
			if = {
				limit = {
					NOR = {
						has_global_flag = giga_achievements_disabled
						has_country_flag = giga_achievement_64
					}
				}
				set_country_flag = giga_achievement_64
				set_timed_country_flag = { flag = giga_achievement_64_notification days = 30 }
				giga_achievement_sound = yes
			}
		}
	}

	ai_weight = {
		factor = 190000

		# policy_route = storage_cap_core
		# source_object = megastructure:kugelblitz_3
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_storage_cap_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_storage_cap_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 7 from = { years_passed > 79 } }
		modifier = { factor = 10 from = { years_passed > 119 } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 4 from = { has_technology = giga_tech_kugelblitz } }
		modifier = { factor = 10 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 14 from = { staid_high_scale_snowball_pressure = yes } }
	}
}


# policy_route = crowded_tall_route; source = common/megastructures/zz_b_habitats.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
habitat_central_complex = {
    entity = "habitat_phase_03_entity"
    construction_entity = "habitat_phase_03_entity"
    portrait = "GFX_megastructure_habitat_background"
    place_entity_on_planet_plane = no
    show_galactic_map_icon = no
    hide_name = yes
    show_in_outliner = no
    entity_offset = { x = 7 y = -7 }
    build_time = @central_orbital_build_time

    resources = {
        category = megastructures_habitat
        cost = {
            influence = @central_orbital_influence_cost
        }
        inline_script = {
            script = megastructures/generic_parts/giga_mega_alloy_cost
            alloys = @central_orbital_alloy_cost
        }
    }

    construction_blocks_and_blocked_by = self_type
    custom_tooltip_requirements = "MEGASTRUCTURE_TOOLTIP_REQUIREMENTS_HABITAT_CENTRAL_COMPLEX"
    build_system_tooltip = habitat_tooltip
    tooltip_system_score = {
        base = 0
        add = value:max_habitat_districts_value
    }
    tooltip_best_systems_header = "MEGASTRUCTURE_HABITAT_BEST_SYSTEMS_TOOLTIP_HEADER"
    tooltip_system_filter = {
        NOT = {
            OR = {
                any_system_planet = {
                    OR = {
                        has_planet_flag = habitat
                        has_planet_flag = hold_the_line_habitat
                    }
                }
                has_megastructure = habitat_central_complex_ruined
            }
        }
    }
    tooltip_system_score_low_threshold = 10
    tooltip_system_score_high_threshold = 16

    potential = {
        giga_are_habitats_available = yes
    }

    possible = {
        hidden_trigger = { exists = starbase }
        custom_tooltip = {
            fail_text = "requires_inside_border"
            is_inside_border = from
        }
        custom_tooltip = {
            fail_text = "requires_not_habitat_central_complex"
            NOT = {
                OR = {
                    any_system_planet = {
                        OR = {
                            has_carrier_flag = habitat
                            has_carrier_flag = hold_the_line_habitat
                        }
                    }
                    has_megastructure = habitat_central_complex_ruined
                }
            }
        }
        custom_tooltip = {
            fail_text = "requires_no_orbital_debris"
            NOT = {
                any_system_planet = {
                    has_carrier_flag = has_orbital_debris
                }
            }
        }

        # The AI has a hard cap on number of habitats scaling with galaxy size and difficulty (vanilla)
        hidden_trigger = {
            from = {
                if = {
                    limit = {
                        is_ai = yes
                    }
                    count_planet_within_border = {
                        count <= value:ai_habitat_cap
                        limit = {
                            is_planet_class = pc_habitat
                        }
                    }
                }
            }
        }
    }

    placement_rules = {
        planet_possible = {
            custom_tooltip = {
                fail_text = "requires_surveyed_planet"
                is_surveyed = {			# prevent leaking habitability information
                    who = prev.from
                    status = yes
                }
            }
            custom_tooltip = {
                fail_text = "requires_no_anomaly"
                NOT = { has_anomaly = yes }
            }
            custom_tooltip = {
                fail_text = "requires_no_existing_megastructure"
                #can_build_megastructure_on_planet = yes
                NOR = {
                    has_carrier_flag = megastructure
                    has_carrier_flag = has_megastructure
                    solar_system = {
                        OR = {
                            has_star_flag = ring_world_built
                            has_star_flag = ithomes_gate
                        }
                    }
                    is_planet_class = pc_ringworld_habitable
                    is_planet_class = pc_ringworld_habitable_damaged
                    is_planet_class = pc_ringworld_tech
                    is_planet_class = pc_ringworld_tech_damaged
                    is_planet_class = pc_ringworld_seam
                    is_planet_class = pc_ringworld_seam_damaged
                    is_planet_class = pc_habitat
                    is_planet_class = pc_cosmogenesis_world
                }
            }
            custom_tooltip = {
				fail_text = "requires_not_astral_scar"
				is_astral_scar = no
			}
            # balance for habitats
            custom_tooltip = {
                fail_text = "requires_not_minor_planetary_body"
                NOR = {
                    is_asteroid = yes
                    is_moon = yes
                }
            }
            custom_tooltip = {
                fail_text = "requires_not_solarpunk"
                NOT = {
                    solar_system = {
                        has_star_flag = solarpunk_system_02
                    }
                }
            }
            if = {
                limit = {
                    from = { is_ai = yes }
                }
                or = {
                    has_deposit_for = shipclass_mining_station
                    has_deposit_for = shipclass_research_station
                }
            }
        } # use these for all non-star megastructures
    }

    # root = system
    # from = country

    on_build_queued = {
        from = {
            set_timed_country_flag = { flag = has_recently_built_habitat years = 30 }
        }
    }
    on_build_unqueued = {
        from = {
            remove_country_flag = has_recently_built_habitat
        }
    }
    on_build_cancel = {
        from = {
            remove_country_flag = has_recently_built_habitat
        }
    }

    on_build_complete = {
        fromfrom.planet = {
            save_event_target_as = target_planet
        }
        if = {
            limit = {
                fromfrom.planet = {
                    is_star = yes
                }
            }
            spawn_habitat_effect = {
                HABITAT_OWNER = root
                TARGET_PLANET = event_target:target_planet
                DISTANCE = 19.798
            }
        }
        else = {
            spawn_habitat_effect = {
                HABITAT_OWNER = root
                TARGET_PLANET = event_target:target_planet
                DISTANCE = 9.899
            }
        }
        fromfrom.solar_system = {
            set_star_flag = has_habitat
        }
        from = {
            save_event_target_as = habitat_owner
        }
        remove_megastructure = fromfrom
        from = {
            country_event = { id = megastructures.10 }
        }
    }

	ai_weight = {
		factor = 125000

		# policy_route = crowded_tall_route
		# source_object = megastructure:habitat_central_complex
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_planetary_capacity_growth_ready = yes } } }
		modifier = { factor = 4 from = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 2 from = { years_passed > 44 } }
		modifier = { factor = 3 from = { years_passed > 79 } }
		modifier = { factor = 5 from = { years_passed > 119 } }
		modifier = { factor = 5 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = crowded_tall_route; source = common/megastructures/zz_e_interstellar_habitat.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
interstellar_habitat_0 = {
	entity = "construction_platform_entity"
	construction_entity = "construction_platform_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	show_galactic_map_icon = yes
	prerequisites = { giga_tech_interstellar_habitat }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_megastructures
		cost = {
			influence = 75
			unity = @giga_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 2500
		}
		upkeep = { energy = 5 }
	}

	potential = {
		always = no #disabled 4.0 rework
		has_technology = giga_tech_interstellar_habitat
		NOT = { has_global_flag = stellarhabitat_disabled }
		giga_can_use_habitables = yes
		OR = {
			has_global_flag = stellarhabitat_capped_u
			check_variable = {
				which = giga_current_stellarhabitat
				value < value:giga_stellarhabitat_limit
			}
		}
	}

	possible = {
		custom_tooltip = { fail_text = "requires_inside_border"			is_inside_border = from }
		custom_tooltip = { fail_text = "requires_surveyed_system"		NOT = { any_system_planet = { is_surveyed = { who = prev.from status = no } } } }
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"			planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "must_build_around_star"						is_star = yes }
			custom_tooltip = { fail_text = "requires_no_anomaly"						has_anomaly = no }
			custom_tooltip = { fail_text = "cant_build_on_interstellar_habitat"			NOT = { solar_system = { has_star_flag = habitat_system } } }
			custom_tooltip = {
				fail_text = "requires_not_capped"
				from = {
					OR = {
						has_global_flag = stellarhabitat_capped_u
						check_variable = {
							which = giga_current_stellarhabitat
							value < value:giga_stellarhabitat_limit
						}
					}
				}
			}
		}
	}


	on_build_complete = {
		set_star_flag = habitat_system
		set_star_flag = habitat_hyperlane_needed
		save_event_target_as = giga_system
		set_variable = { which = i_ring_segments value = 0 }
		save_event_target_as = interstellar_system
		fromfrom.planet = {
			save_event_target_as = giga_planet
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
		}
		from = {
			set_timed_country_flag = { flag = has_recently_built_interstellar_habitat years = 20 }
			set_country_flag = giga_started_i_ringworld
			change_variable = { which = giga_current_stellarhabitat value = 1 }
			country_event = { id = giga_dialog.2901 }	# Notification + Choose where
		}
		remove_megastructure = fromfrom
	}

	ai_weight = {
		factor = 145000

		# policy_route = crowded_tall_route
		# source_object = megastructure:interstellar_habitat_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_planetary_capacity_growth_ready = yes } } }
		modifier = { factor = 4 from = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 2 from = { years_passed > 44 } }
		modifier = { factor = 3 from = { years_passed > 79 } }
		modifier = { factor = 5 from = { years_passed > 119 } }
		modifier = { factor = 5 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = crowded_tall_route; source = common/megastructures/zz_e_stellar_ring_habitat.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
stellar_ring_habitat_0 = {
	entity = construction_platform_entity
	construction_entity = construction_platform_entity
	construction_blocks_and_blocked_by = multi_stage_type
	portrait = GFX_megastructure_construction_background
	place_entity_on_planet_plane = no
	entity_offset = { x = 0 y = -20 }
	prerequisites = { giga_tech_stellar_ring_habitat }

	build_time = 1800
	resources = {
		category = giga_megastructures
		cost = {
			alloys = 5000
			unity = @giga_big_mega_start_unity_cost
			influence = 200
		}
		upkeep = { energy = 5 }
	}

	# potential = {
	# 	always = no #disabled 4.0 rework
	# }

	possible = {
		hidden_trigger = {
			exists = starbase
		}
		custom_tooltip = { fail_text = "requires_inside_border"						is_inside_border = from }
		custom_tooltip = { fail_text = "requires_surveyed_system"					giga_system_is_surveyed = yes }

	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "must_build_around_asteroid"			is_asteroid = yes is_moon = no }
			custom_tooltip = { fail_text = "requires_no_anomaly"				has_anomaly = no }
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"	planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "requires_survey_not_habitable"		is_surveyed = { who = prev.from status = yes } is_planet_habitable = no is_colony = no }
			custom_tooltip = { fail_text = "requires_no_existing_orbital"		solar_system = { not = { has_star_flag = has_giga_stellar_ring_habitat } } }
		}
	}


	on_build_complete = {
		save_event_target_as = giga_system

		fromfrom.planet = {
			giga_set_has_mega_flag = yes
			save_event_target_as = giga_planet
		}

		from = {
			set_timed_country_flag = { flag = has_recently_built_stellar_ring_habitat years = 20 }
			country_event = { id = giga_dialog.13601 }	# Notification
			change_variable = { which = giga_current_stellar_ring value = 1 }
		}
	}

	ai_weight = {
		factor = 145000

		# policy_route = crowded_tall_route
		# source_object = megastructure:stellar_ring_habitat_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_planetary_capacity_growth_ready = yes } } }
		modifier = { factor = 4 from = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 2 from = { years_passed > 44 } }
		modifier = { factor = 3 from = { years_passed > 79 } }
		modifier = { factor = 5 from = { years_passed > 119 } }
		modifier = { factor = 5 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = planetary_computer_research_core; source = common/megastructures/zz_e_planetary_computer.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
planetary_computer_0 = {
	entity = "giga_consite_5_5_entity"
	construction_entity = "giga_consite_5_5_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	prerequisites = { giga_tech_planetary_computer }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_planetary_computer
		cost = {
			influence = 150
			unity = @giga_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 2500
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|resource|RESOURCE|alloys|AMOUNT|2500| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|resource|RESOURCE|unity|AMOUNT|@giga_mega_unity_cost| }
		upkeep = { energy = 5 }
	}

	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = resource RESOURCE = alloys AMOUNT = 2500 }
		giga_ai_savings_withdraw = { CATEGORY = resource RESOURCE = unity  AMOUNT = @giga_mega_unity_cost }
	}
	on_build_cancel = {
		giga_ai_savings_refund = { CATEGORY = resource RESOURCE = alloys }
		giga_ai_savings_refund = { CATEGORY = resource RESOURCE = unity }
	}

	potential = {
		has_technology = giga_tech_planetary_computer
		NOT = { has_global_flag = planetary_computer_disabled }
		OR = {
			has_global_flag = planetary_computer_capped_u
			check_variable = {
				which = giga_current_planetary_computer
				value < value:giga_planetary_computer_limit
			}
		}
		is_wilderness_empire = no #Wilderness can get a swap of the tech but can't build the mega
        is_nomadic = no
	}

	possible = {
		custom_tooltip = { fail_text = "requires_inside_border"		is_inside_border = from }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = planetary_computer_capped_u
					check_variable = {
						which = giga_current_planetary_computer
						value < value:giga_planetary_computer_limit
					}
				}
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_no_anomaly"				has_anomaly = no }
			custom_tooltip = { fail_text = "requires_not_asteroid"				is_asteroid = no }
			custom_tooltip = { fail_text = "requires_not_star"					is_star = no }
			custom_tooltip = {
				fail_text = "requires_not_astral_scar"
				is_astral_scar = no
			}
			custom_tooltip = {
				fail_text = "requires_no_colonized_planets"
				NOT = { is_colony = yes }
			}
			custom_tooltip = { fail_text = "requires_no_crisis_planet"			NOT = { has_planet_flag = crisis_vital_planet } }
			custom_tooltip = {
				fail_text = "requires_habitable"
				NOR = {
					is_planet_class = pc_giga_planetary_computer
					has_planet_flag = has_planet_pc_mega
				}
				habitable_structure = no
				is_planet_habitable = yes
			}
			custom_tooltip = {
				fail_text = "requires_surveyed_planet"
				OR = {
					AND = {
						is_surveyed = { who = prev.from status = yes }
						prev.from = { is_ai = no }
					}
					AND = {
						is_surveyed = { who = prev.from status = yes }
						prev.from = { is_ai = yes }
						is_planet_habitable = no
					}
				}
			}
			custom_tooltip = {
				fail_text = "requires_owned_colony"
				OR = {
					NOT = { exists = owner }
					owner = {
						is_same_value = prev.space_owner
					}
				}
			}
		}
	}


	on_build_complete = {
		save_event_target_as = giga_system
		fromfrom.planet = {
			save_event_target_as = giga_planet
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			giga_set_has_mega_flag = yes
			set_planet_flag = has_planet_pc_mega
		}
		from = {
			set_timed_country_flag = { flag = has_recently_built_planetary_computer years = 230 }
			country_event = { id = giga_dialog.1301 }	# Notification
			change_variable = { which = giga_current_planetary_computer value = 1 }
		}
	}

	ai_weight = {
		factor = 175000

		# policy_route = planetary_computer_research_core
		# source_object = megastructure:planetary_computer_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_planetary_computer_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_planetary_computer_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 12 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 5 from = { has_technology = giga_tech_planetary_computer } }
		modifier = { factor = 4 from = { staid_research_under_curve = yes } }
		modifier = { factor = 2 from = { staid_planetary_capacity_growth_ready = yes } }
	}
}


# policy_route = planetary_computer_research_core; source = common/megastructures/zz_e_planetary_computer.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
planetary_computer_1 = {
	entity = ""
	portrait = "GFX_megastructure_construction_background"
	upgrade_from = { planetary_computer_0 }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 2500
	resources = {
		category = giga_megastructures
		cost = {
			energy = 5000
			unity = @giga_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 5000
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|resource|RESOURCE|alloys|AMOUNT|5000| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|resource|RESOURCE|unity|AMOUNT|@giga_mega_unity_cost| }
		upkeep = {
			energy = 10
			alloys = 10
		}
	}

	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = resource RESOURCE = alloys AMOUNT = 5000 }
		giga_ai_savings_withdraw = { CATEGORY = resource RESOURCE = unity  AMOUNT = @giga_mega_unity_cost }
	}

	potential = { NOT = { has_global_flag = planetary_computer_disabled } }
	possible = { from = { has_technology = giga_tech_planetary_computer } }

	on_build_complete = {
		save_event_target_as = giga_system
		if = { limit = { exists = fromfrom.planet } fromfrom.planet = { save_event_target_as = giga_planet } }
		from = { country_event = { id = giga_dialog.1302 } }	# Notification
	}

	ai_weight = {
		factor = 190000

		# policy_route = planetary_computer_research_core
		# source_object = megastructure:planetary_computer_1
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_planetary_computer_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_planetary_computer_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 12 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 3 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 5 from = { has_technology = giga_tech_planetary_computer } }
		modifier = { factor = 4 from = { staid_research_under_curve = yes } }
		modifier = { factor = 2 from = { staid_planetary_capacity_growth_ready = yes } }
	}
}


# policy_route = mega_shipyard_core; source = common/megastructures/zz_e_mega_shipyard.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
mega_shipyard_0 = {
	entity = "construction_platform_entity"
	construction_entity = "construction_platform_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	entity_offset = { x = -27 y = -27 }
	prerequisites = { "tech_mega_shipyard" }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_mega_shipyard
		cost = {
			unity = @giga_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 3000
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|utility|RESOURCE|alloys|AMOUNT|3000| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|utility|RESOURCE|unity|AMOUNT|@giga_mega_unity_cost| }
		upkeep = { energy = 5 }
	}

	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = utility RESOURCE = alloys AMOUNT = 3000 }
		giga_ai_savings_withdraw = { CATEGORY = utility RESOURCE = unity  AMOUNT = @giga_mega_unity_cost }
	}
	on_build_cancel = {
		giga_ai_savings_refund = { CATEGORY = utility RESOURCE = alloys }
		giga_ai_savings_refund = { CATEGORY = utility RESOURCE = unity }
	}

	potential = {
		NOT = { has_global_flag = vanilla_shipyard_disabled }
		OR = {
			has_global_flag = vanilla_shipyard_capped_u
			check_variable = {
				which = giga_current_vanilla_shipyard
				value < value:giga_vanilla_shipyard_limit
			}
		}
	}

	possible = {
		hidden_trigger = {
			exists = starbase
		}
		custom_tooltip = { fail_text = "requires_inside_border"			is_inside_border = from }
		custom_tooltip = { fail_text = "requires_surveyed_system"		giga_system_is_surveyed = yes }
		custom_tooltip = { fail_text = "requires_no_binary_trinary"		giga_is_bitrinary = no }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = vanilla_shipyard_capped_u
					check_variable = {
						which = giga_current_vanilla_shipyard
						value < value:giga_vanilla_shipyard_limit
					}
				}
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "must_build_around_star"					is_star = yes }
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"		planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "requires_no_anomaly"					has_anomaly = no }
			custom_tooltip = { fail_text = "requires_standard_planet_class"			giga_is_standard_star = yes }
		}
	}


	on_build_complete = {
		from = {
			set_timed_country_flag = { flag = has_recently_built_mega_shipyard years = 20 }
			set_country_flag = built_mega_shipyard_site
			change_variable = { which = giga_current_vanilla_shipyard value = 1 }
		}
		fromfrom.planet = {
			giga_set_has_mega_flag = yes
			if = { limit = { has_orbital_station = yes } orbital_station = { dismantle = yes } }
		}
	}

	ai_weight = {
		factor = 150000

		# policy_route = mega_shipyard_core
		# source_object = megastructure:mega_shipyard_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_mega_shipyard_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_mega_shipyard_build_priority_ready = yes } }
		modifier = { factor = 3 from = { years_passed > 44 } }
		modifier = { factor = 5 from = { years_passed > 79 } }
		modifier = { factor = 8 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = economy_megastructure_core; source = common/megastructures/zz_i_matrioshka_brain_revised.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
matrioshka_brain_0_g_star = {
    entity = "giga_consite_7_7_entity"
    construction_entity = "giga_consite_7_7_entity"
    # construction_blocks_and_blocked_by = none # BLOCKING TEST
    portrait = "GFX_megastructure_construction_background"
    place_entity_on_planet_plane = no
    prerequisites = { giga_tech_matrioshka_brain_1 }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

    build_time = 500
    resources = {
        category = giga_matrioshka_brain
        cost = {
            unity = @giga_giga_unity_cost
            influence = 300
            inline_script = {
                script = megastructures/generic_parts/giga_mega_alloy_cost
                alloys = 10000
            }
        }
        cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|alloys|AMOUNT|10000| }
        cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|unity|AMOUNT|@giga_giga_unity_cost| }
        upkeep = { energy = 10 }
    }

    on_build_start = {
        set_star_flag = giga_forbid_planet_dismantlement
        giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = alloys AMOUNT = 10000 }
        giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = unity  AMOUNT = @giga_giga_unity_cost }
    }
    on_build_cancel = {
        remove_star_flag = giga_forbid_planet_dismantlement
        giga_ai_savings_refund = { CATEGORY = important RESOURCE = alloys }
        giga_ai_savings_refund = { CATEGORY = important RESOURCE = unity }
    }

    potential = {
        has_gigastructural_constructs = yes
        has_technology = giga_tech_matrioshka_brain_1
        NOT = { has_global_flag = matrioshka_brain_disabled }
        OR = {
            has_global_flag = matrioshka_brain_capped_u
            check_variable = {
                which = giga_current_matrioshka_brain
                value < value:giga_matrioshka_brain_limit
            }
        }
    }

    possible = {
        custom_tooltip = { fail_text = "requires_inside_border"					is_inside_border = from }
        custom_tooltip = { fail_text = "requires_surveyed_system"				giga_system_is_surveyed = yes }
        custom_tooltip = { fail_text = "requires_no_binary_trinary"				giga_is_bitrinary = no }
        custom_tooltip = { fail_text = "requires_no_colonized_planets"			NOT = { any_system_planet = { is_colony = yes } } }
        custom_tooltip = { fail_text = "requires_no_existing_megastructure"		has_no_non_gate_megastructure = yes }
        custom_tooltip = { fail_text = "requires_no_crisis_system"							NOT = { any_system_planet = { has_planet_flag = crisis_vital_planet } } }
        custom_tooltip = {
            fail_text = "requires_not_capped"
            from = {
                OR = {
                    has_global_flag = matrioshka_brain_capped_u
                    check_variable = {
                        which = giga_current_matrioshka_brain
                        value < value:giga_matrioshka_brain_limit
                    }
                }
            }
        }
    }

    placement_rules = {
        planet_possible = {
            custom_tooltip = { fail_text = "requires_no_existing_megastructure"		planet_has_no_megastructure = yes }
            custom_tooltip = { fail_text = "must_build_around_star"					is_star = yes }
            custom_tooltip = { fail_text = "requires_no_anomaly"					has_anomaly = no }
            custom_tooltip = {
                fail_text = "requires_standard_planet_class_o_star"
                OR = {
                    giga_is_standard_star = yes
                    AND = {
                        giga_is_o_star_for_megas = yes
                        from = { has_technology = giga_tech_brain_o_star }
                    }
                }
            }
        }
    }


    on_build_complete = {
        save_event_target_as = giga_system
        fromfrom.planet = {
            save_event_target_as = giga_planet
            if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
            giga_set_has_mega_flag = yes
        }
        if = {	limit = { fromfrom.planet = { giga_is_o_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = matrioshka_brain_0_o_star finish_upgrade = yes } }
        if = {
            limit = { has_global_flag = giga_matroishka_scaling }
            if = {		limit = { fromfrom.planet = { giga_is_b_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = matrioshka_brain_0_b_star finish_upgrade = yes } }
            else_if = {	limit = { fromfrom.planet = { giga_is_m_giant_star_for_megas = yes } }	fromfrom = { upgrade_megastructure_to = matrioshka_brain_0_m_giant_star finish_upgrade = yes } }
            else_if = {	limit = { fromfrom.planet = { giga_is_a_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = matrioshka_brain_0_a_star finish_upgrade = yes } }
            else_if = {	limit = { fromfrom.planet = { giga_is_f_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = matrioshka_brain_0_f_star finish_upgrade = yes }}
            else_if = {	limit = { fromfrom.planet = { giga_is_k_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = matrioshka_brain_0_k_star finish_upgrade = yes } }
            else_if = {	limit = { fromfrom.planet = { giga_is_m_star_for_megas = yes } } fromfrom = { upgrade_megastructure_to = matrioshka_brain_0_m_star finish_upgrade = yes } }
        }
		inline_script = {
			script = megastructures/generic_parts/giga_mega_bulk_matter_calculations
			giga_system_bm_cost = @matrioskha_brain_1_bm_cost
		}
        from = {
            set_timed_country_flag = { flag = has_recently_built_matrioshka_brain years = 20 }
            country_event = { id = giga_dialog.501 }	# Notification
            change_variable = { which = giga_current_matrioshka_brain value = 1 }
        }
    }

	ai_weight = {
		factor = 145000

		# policy_route = economy_megastructure_core
		# source_object = megastructure:matrioshka_brain_0_g_star
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_economy_megastructure_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_economy_megastructure_build_priority_ready = yes } }
		modifier = { factor = 3 from = { years_passed > 44 } }
		modifier = { factor = 5 from = { years_passed > 79 } }
		modifier = { factor = 8 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
	}
}


# policy_route = apex_site_preservation_core; source = common/megastructures/zz_i_matrioshka_brain_revised.txt; parent_ai = parent_ai_absent; source_ai_weight = no
matrioshka_brain_0_o_star = {
    inline_script = megastructures/matrioshka_brain/matrioshka_brain_0

	ai_weight = {
		factor = 230000

		# policy_route = apex_site_preservation_core
		# source_object = megastructure:matrioshka_brain_0_o_star
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_apex_site_preservation_ready = yes } } }
		modifier = { factor = 4 from = { staid_apex_site_preservation_ready = yes } }
		modifier = { factor = 2 from = { years_passed > 44 } }
		modifier = { factor = 5 from = { years_passed > 79 } }
		modifier = { factor = 9 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 8 from = { has_technology = giga_tech_matrioshka_brain_1 } }
		modifier = { factor = 4 from = { has_technology = giga_tech_neutronium_gigaforge } }
		modifier = { factor = 0.15 from = { NOT = { staid_apex_site_preservation_ready = yes } } }
	}
}


# policy_route = apex_site_preservation_core; source = common/megastructures/zz_e_dyson_sphere_o_star.txt; parent_ai = parent_ai_absent; source_ai_weight = no
dyson_sphere_0_o_star = {
	entity = "construction_platform_entity"
	construction_entity = "construction_platform_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	entity_offset = { x = -40 y = -40 }
	potential = { always = no }

	upgrade_from = { dyson_sphere_0 }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	resources = {
		category = giga_dyson_sphere
		upkeep = { energy = 5 }
	}

	ai_weight = {
		factor = 45000

		# policy_route = apex_site_preservation_core
		# source_object = megastructure:dyson_sphere_0_o_star
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_apex_site_preservation_ready = yes } } }
		modifier = { factor = 4 from = { staid_apex_site_preservation_ready = yes } }
		modifier = { factor = 2 from = { years_passed > 44 } }
		modifier = { factor = 5 from = { years_passed > 79 } }
		modifier = { factor = 9 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		# megastructure_continuation_priority = finish_existing_before_new_start
		modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }
		modifier = { factor = 8 from = { staid_resource_waste_pressure = yes } }
		modifier = { factor = 6 from = { staid_high_scale_snowball_pressure = yes } }
		modifier = { factor = 8 from = { has_technology = giga_tech_matrioshka_brain_1 } }
		modifier = { factor = 4 from = { has_technology = giga_tech_neutronium_gigaforge } }
		modifier = { factor = 0.15 from = { NOT = { staid_apex_site_preservation_ready = yes } } }
	}
}


# policy_route = apex_site_preservation_core; source = common/megastructures/zz_e_neutronium_gigaforge.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
neutronium_gigaforge_0 = {
	entity = "giga_consite_7_7_entity"
	construction_entity = "giga_consite_7_7_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	prerequisites = { giga_tech_neutronium_gigaforge }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_neutronium_gigaforge
		cost = {
			unity = @giga_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 3500
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|alloys|AMOUNT|3500| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|unity|AMOUNT|@giga_mega_unity_cost| }
		upkeep = { energy = 5 }
	}

	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = alloys AMOUNT = 3500 }
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = unity  AMOUNT = @giga_mega_unity_cost }
	}
	on_build_cancel = {
		giga_ai_savings_refund = { CATEGORY = important RESOURCE = alloys }
		giga_ai_savings_refund = { CATEGORY = important RESOURCE = unity }
	}

	potential = {
		has_technology = giga_tech_neutronium_gigaforge
		NOT = { has_global_flag = gigaforge_disabled }
		OR = {
			has_global_flag = gigaforge_capped_u
			check_variable = {
				which = giga_current_gigaforge
				value < value:giga_gigaforge_limit
			}
		}
	}

	possible = {
		custom_tooltip = { fail_text = "requires_inside_border"				is_inside_border = from }
		custom_tooltip = { fail_text = "requires_surveyed_system"			NOT = { any_system_planet = { is_surveyed = { who = prev.from status = no } } } }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = gigaforge_capped_u
					check_variable = {
						which = giga_current_gigaforge
						value < value:giga_gigaforge_limit
					}
				}
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_no_anomaly"					has_anomaly = no }
			custom_tooltip = { fail_text = "must_build_around_neutron_star"			OR = { is_planet_class = pc_neutron_star is_planet_class = pc_pulsar } }
			custom_tooltip = {
				fail_text = "requires_no_existing_megastructure"
				OR = {
					planet_has_no_megastructure = yes
					AND = {
						has_planet_flag = has_nidavellir
						NOT = { has_planet_flag = has_gigaforge }
					}
				}
			}
		}
	}


	on_build_complete = {
		save_event_target_as = giga_system
		fromfrom.planet = {
			save_event_target_as = giga_planet
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			giga_set_has_mega_flag = yes
			set_planet_flag = has_gigaforge
		}
		from = {
			set_timed_country_flag = { flag = has_recently_built_neutronium_gigaforge years = 20 }
			country_event = { id = giga_dialog.701 }	# Notification
			change_variable = { which = giga_current_gigaforge value = 1 }
		}
	}

	ai_weight = {
		factor = 210000

		# policy_route = apex_site_preservation_core
		# source_object = megastructure:neutronium_gigaforge_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_apex_site_preservation_ready = yes } } }
		modifier = { factor = 4 from = { staid_apex_site_preservation_ready = yes } }
		modifier = { factor = 2 from = { years_passed > 44 } }
		modifier = { factor = 5 from = { years_passed > 79 } }
		modifier = { factor = 9 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 8 from = { has_technology = giga_tech_matrioshka_brain_1 } }
		modifier = { factor = 4 from = { has_technology = giga_tech_neutronium_gigaforge } }
		modifier = { factor = 0.15 from = { NOT = { staid_apex_site_preservation_ready = yes } } }
	}
}


# policy_route = apex_site_preservation_core; source = common/megastructures/zz_i_nidavellir_forge.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
nidavellir_forge_0 = {
	entity = "giga_consite_7_7_entity"
	construction_entity = "giga_consite_7_7_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	prerequisites = { giga_tech_nidavellir }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_nidavellir_forge
		cost = {
			influence = 150
			unity = @giga_giga_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 3500
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|alloys|AMOUNT|3500| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|important|RESOURCE|unity|AMOUNT|@giga_giga_unity_cost| }
		upkeep = { energy = 5 }
	}

	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = alloys AMOUNT = 3500 }
		giga_ai_savings_withdraw = { CATEGORY = important RESOURCE = unity  AMOUNT = @giga_giga_unity_cost }
	}
	on_build_cancel = {
		giga_ai_savings_refund = { CATEGORY = important RESOURCE = alloys }
		giga_ai_savings_refund = { CATEGORY = important RESOURCE = unity }
	}

	potential = {
		has_gigastructural_constructs = yes
		has_technology = giga_tech_nidavellir
		NOT = { has_global_flag = nidavellir_disabled }
		OR = {
			has_global_flag = nidavellir_capped_u
			check_variable = {
				which = giga_current_nidavellir
				value < value:giga_nidavellir_limit
			}
		}
	}

	possible = {
		custom_tooltip = { fail_text = "requires_inside_border"						is_inside_border = from }
		custom_tooltip = { fail_text = "requires_surveyed_system"					giga_system_is_surveyed = yes }
		custom_tooltip = { fail_text = "requires_no_colonized_planets"				NOT = { any_system_planet = { is_colony = yes } } }
		custom_tooltip = { fail_text = "requires_no_crisis_system"					NOT = { any_system_planet = { has_planet_flag = crisis_vital_planet } } }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = nidavellir_capped_u
					check_variable = {
						which = giga_current_nidavellir
						value < value:giga_nidavellir_limit
					}
				}
			}
		}
		custom_tooltip = {
			fail_text = "requires_no_binary_trinary"
			NOR = {
				is_trinary_star = yes
				is_binary_star = yes
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_larger_star"					planet_size >= 10 }
			custom_tooltip = { fail_text = "must_build_around_neutron_star"			OR = { is_planet_class = pc_neutron_star is_planet_class = pc_pulsar } }
			custom_tooltip = { fail_text = "requires_no_anomaly"					has_anomaly = no }
			custom_tooltip = {
				fail_text = "requires_no_existing_megastructure"
				OR = {
					planet_has_no_megastructure = yes
					AND = {
						has_planet_flag = has_gigaforge
						NOT = { has_planet_flag = has_nidavellir }
					}
				}
			}
		}
	}


	on_build_complete = {
		save_event_target_as = giga_system
		fromfrom.planet = {
			save_event_target_as = giga_planet
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			giga_set_has_mega_flag = yes
			set_planet_flag = has_nidavellir
		}
		from = {
			set_timed_country_flag = { flag = has_recently_built_nidavellir_forge years = 20 }
			country_event = { id = giga_dialog.801 }	# Notification
			change_variable = { which = giga_current_nidavellir value = 1 }
		}
	}

	ai_weight = {
		factor = 220000

		# policy_route = apex_site_preservation_core
		# source_object = megastructure:nidavellir_forge_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_apex_site_preservation_ready = yes } } }
		modifier = { factor = 4 from = { staid_apex_site_preservation_ready = yes } }
		modifier = { factor = 2 from = { years_passed > 44 } }
		modifier = { factor = 5 from = { years_passed > 79 } }
		modifier = { factor = 9 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 8 from = { has_technology = giga_tech_matrioshka_brain_1 } }
		modifier = { factor = 4 from = { has_technology = giga_tech_neutronium_gigaforge } }
		modifier = { factor = 0.15 from = { NOT = { staid_apex_site_preservation_ready = yes } } }
	}
}


# policy_route = planetcraft_route; source = common/megastructures/zz_i_behemoth_assembly_plant.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
planetcraft_printer_0 = {
	entity = "construction_platform_entity"
	construction_entity = "construction_platform_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	prerequisites = { giga_tech_planet_assembly }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_gigastructures
		cost = {
			influence = 300
			unity = @giga_giga_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 5000
		}
		upkeep = { energy = 5 }
	}

	potential = {
		has_technology = giga_tech_planet_assembly
		NOT = { has_global_flag = warplanet_disabled }
	}

	possible = {
		custom_tooltip = { fail_text = "requires_inside_border"		is_inside_border = from }
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_no_anomaly"				has_anomaly = no }
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"	planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "requires_survey_not_habitable"		is_surveyed = { who = prev.from status = yes } is_planet_habitable = no }
			custom_tooltip = { fail_text = "requires_standard_planet_class"			giga_is_standard_star = yes }
		}
	}


	on_build_complete = {
		save_event_target_as = giga_system
		if = { limit = { exists = fromfrom.planet } fromfrom.planet = { save_event_target_as = giga_planet } }
		from = {
			country_event = { id = giga_printer.2010 }	# Notification
		}
		fromfrom.planet = {
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			giga_set_has_mega_flag = yes
		}

		# replace this with the "real" upgrade path
		spawn_megastructure = {
			type = planetcraft_printer_0_real
			owner = from
			planet = fromfrom.planet
		}
		remove_megastructure = fromfrom
	}

	ai_weight = {
		factor = 180000

		# policy_route = planetcraft_route
		# source_object = megastructure:planetcraft_printer_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_planetcraft_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_planetcraft_build_priority_ready = yes } }
		modifier = { factor = 3 from = { years_passed > 44 } }
		modifier = { factor = 6 from = { years_passed > 79 } }
		modifier = { factor = 10 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 from = { AND = { years_passed > 59 years_passed < 100 } } }
		modifier = { factor = 4 from = { has_technology = giga_tech_planet_assembly } }
		modifier = { factor = 3 from = { has_ascension_perk = ap_celestial_printing } }
	}
}


# policy_route = war_moon_route; source = common/megastructures/zz_e_attack_moon.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
war_moon_0 = {
	entity = "construction_platform_entity"
	construction_entity = "construction_platform_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	prerequisites = { giga_tech_war_moon_2 }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_attack_moon
		cost = {
			unity = @giga_mega_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 5000
		}
		cost = { alloys = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|military|RESOURCE|alloys|AMOUNT|5000| }
		cost = { unity = -1 multiplier = value:giga_ai_savings_cost|CATEGORY|military|RESOURCE|unity|AMOUNT|@giga_mega_unity_cost| }
		upkeep = { energy = 5 }
	}

	on_build_start = {
		giga_ai_savings_withdraw = { CATEGORY = military RESOURCE = alloys AMOUNT = 3500 }
		giga_ai_savings_withdraw = { CATEGORY = military RESOURCE = unity  AMOUNT = @giga_mega_unity_cost }
	}
	on_build_cancel = {
		giga_ai_savings_refund = { CATEGORY = military RESOURCE = alloys }
		giga_ai_savings_refund = { CATEGORY = military RESOURCE = unity }
	}

	potential = {
		has_technology = giga_tech_war_moon_2
		NOT = { has_global_flag = warmoon_disabled }
		OR = {
			has_global_flag = warmoon_capped_u
			check_variable = {
				which = giga_current_warmoon
				value < value:giga_warmoon_limit
			}
		}
	}

	possible = {
		custom_tooltip = { fail_text = "requires_inside_border"		is_inside_border = from }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = warmoon_capped_u
					check_variable = {
						which = giga_current_warmoon
						value < value:giga_warmoon_limit
					}
				}
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = {
				fail_text = "must_build_size_567"
				OR = {
					AND = {
						planet_size >= 5
						planet_size <= 7
						NOT = { is_planet_class = pc_core_mined }
					}
					AND = {
						planet_size >= 1
						planet_size <= 4
						is_planet_class = pc_core_mined
					}
				}
			}
			custom_tooltip = { fail_text = "requires_no_anomaly"				has_anomaly = no }
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"	planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "requires_survey_not_habitable"		is_surveyed = { who = prev.from status = yes } is_planet_habitable = no }
			custom_tooltip = { fail_text = "requires_no_crisis_planet"			NOT = { has_planet_flag = crisis_vital_planet } }
			custom_tooltip = { fail_text = "requires_not_asteroid"				is_asteroid = no }
			custom_tooltip = { fail_text = "requires_not_star"					is_star = no }
			custom_tooltip = {
				fail_text = "requires_not_astral_scar"
				is_astral_scar = no
			}
			custom_tooltip = {
				fail_text = "must_build_around_molten_barren_stripmined"
				OR = {
					giga_is_molten = yes
					giga_is_frozen = yes
					giga_is_barren_cn = yes
					#is_planet_class = pc_disco_moon #Nooooooo :(
					is_planet_class = pc_core_mined
				}
			}
		}
	}


	on_build_complete = {
		save_event_target_as = giga_system
		if = { limit = { exists = fromfrom.planet } fromfrom.planet = { save_event_target_as = giga_planet } }
		from = {
			set_timed_country_flag = { flag = has_recently_built_war_moon years = 5 }
			country_event = { id = giga_dialog.2601 }	# Notification
			change_variable = { which = giga_current_warmoon value = 1 }
		}
		fromfrom.planet = {
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			giga_set_has_mega_flag = yes
			set_carrier_flag = megastructure
			set_planet_size = 6
		}
	}

	ai_weight = {
		factor = 165000

		# policy_route = war_moon_route
		# source_object = megastructure:war_moon_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_war_moon_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_war_moon_build_priority_ready = yes } }
		modifier = { factor = 3 from = { years_passed > 44 } }
		modifier = { factor = 6 from = { years_passed > 79 } }
		modifier = { factor = 10 from = { years_passed > 119 } }
		modifier = { factor = 2 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 4 from = { has_technology = giga_tech_war_moon_1 } }
		modifier = { factor = 6 from = { has_technology = giga_tech_war_moon_2 } }
	}
}


# policy_route = systemcraft_route; source = common/megastructures/zz_i_stellar_systemcraft.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
war_system_0 = {
	entity = "construction_platform_entity"
	construction_entity = "construction_platform_entity"
	# construction_blocks_and_blocked_by = none # BLOCKING TEST
	portrait = "GFX_megastructure_construction_background"
	place_entity_on_planet_plane = no
	prerequisites = { giga_tech_war_system_1 }

	outliner_trigger = {
		exists = owner
		NOT = { has_megastructure_flag = giga_outliner_hidden_by_@owner }
	}

	build_time = 1800
	resources = {
		category = giga_gigastructures
		cost = {
			influence = 300
			unity = @giga_tera_start_unity_cost
		}
		inline_script = {
			script = megastructures/generic_parts/giga_mega_alloy_cost
			alloys = 10000
		}
		upkeep = { energy = 5 }
	}

	potential = {
		has_technology = giga_tech_war_system_1
		has_ascension_perk = ap_celestial_printing
		NOT = { has_global_flag = systemcraft_disabled }
		OR = {
			has_global_flag = systemcraft_capped_u
			check_variable = {
				which = giga_current_systemcraft
				value < value:giga_systemcraft_limit
			}
		}
	}

	possible = {
		custom_tooltip = { fail_text = "requires_no_habitable_planets"		NOT = { any_system_planet = { is_colony = yes } } }
		custom_tooltip = { fail_text = "requires_inside_border"				is_inside_border = from }
		custom_tooltip = { fail_text = "requires_no_crisis_system"			NOT = { any_system_planet = { has_planet_flag = crisis_vital_planet } } }
		custom_tooltip = {
			fail_text = "requires_not_capped"
			from = {
				OR = {
					has_global_flag = systemcraft_capped_u
					check_variable = {
						which = giga_current_systemcraft
						value < value:giga_systemcraft_limit
					}
				}
			}
		}
	}

	placement_rules = {
		planet_possible = {
			custom_tooltip = { fail_text = "requires_no_existing_megastructure"				planet_has_no_megastructure = yes }
			custom_tooltip = { fail_text = "must_build_around_star"							is_star = yes }
			custom_tooltip = { fail_text = "requires_no_anomaly"							has_anomaly = no }
			custom_tooltip = {
				fail_text = "requires_standard_planet_class"
				giga_is_standard_star = yes
				NOT = {
					giga_is_bitrinary = yes
				}
			}
		}
	}

	on_build_complete = {
		save_event_target_as = giga_system
		if = { limit = { exists = fromfrom.planet } fromfrom.planet = { save_event_target_as = giga_planet } }
		from = {
			country_event = { id = giga_dialog.2802 }	# Notification
			change_variable = { which = giga_current_systemcraft value = 1 }
		}
		fromfrom.planet = {
			if = { limit = { exists = orbital_station } orbital_station = { dismantle = yes } }
			set_carrier_flag = megastructure
			if = { limit = { NOT = { has_planet_flag = shroud_storm_changed } } } set_planet_flag = shroud_storm_changed
			giga_set_has_mega_flag = yes
		}
	}

	ai_weight = {
		factor = 200000

		# policy_route = systemcraft_route
		# source_object = megastructure:war_system_0
		modifier = { factor = 0 from = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 from = { staid_recovery_mode = yes } }
		modifier = { factor = 0 from = { NOT = { staid_systemcraft_build_priority_ready = yes } } }
		modifier = { factor = 4 from = { staid_systemcraft_build_priority_ready = yes } }
		modifier = { factor = 4 from = { years_passed > 44 } }
		modifier = { factor = 8 from = { years_passed > 79 } }
		modifier = { factor = 12 from = { years_passed > 119 } }
		modifier = { factor = 3 from = { years_passed < 30 } }
		modifier = { factor = 2 from = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 3 from = { has_ascension_perk = ap_celestial_printing } }
		modifier = { factor = 4 from = { has_technology = giga_tech_war_system_1 } }
		modifier = { factor = 5 from = { has_technology = giga_tech_war_system_2 } }
		modifier = { factor = 6 from = { has_technology = giga_tech_war_system_3 } }
		modifier = { factor = 8 from = { has_technology = giga_tech_war_system_6 } }
	}
}

```

## mods/StellarAIDirector/common/on_actions/zzz_staid_load_proof_on_actions.txt

```text
on_game_start_country = {
	events = {
		staid_load_proof.1
	}
}
```

## mods/StellarAIDirector/common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Monthly Director safety layer for market cap breaking and stranded fleet recovery.

on_monthly_pulse = {
	events = {
		staid_economy_safety.1
	}
}
```

## mods/StellarAIDirector/common/on_actions/zzz_staid_threat_response_on_actions.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Source of truth: tools/stellar_ai_director_lib.py threat-response tables.

on_war_beginning = {
	events = {
		staid_tr.1
	}
}
```

## mods/StellarAIDirector/common/opinion_modifiers/zzz_staid_threat_response_opinions.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Source of truth: tools/stellar_ai_director_lib.py threat-response tables.
staid_tr_anti_aggressor_low = {
	opinion = -30
	decay = 1
	accumulative = no
}

staid_tr_anti_aggressor_medium = {
	opinion = -60
	decay = 1
	accumulative = no
}

staid_tr_anti_aggressor_high = {
	opinion = -120
	decay = 1
	accumulative = no
}

staid_tr_anti_aggressor_severe = {
	opinion = -200
	decay = 1
	accumulative = no
}

staid_tr_shared_threat_low = {
	opinion = 15
	decay = 1
	accumulative = no
}

staid_tr_shared_threat_medium = {
	opinion = 30
	decay = 1
	accumulative = no
}

staid_tr_shared_threat_high = {
	opinion = 60
	decay = 1
	accumulative = no
}

staid_tr_alignment_low = {
	opinion = 10
	decay = 1
	accumulative = no
}

staid_tr_alignment_medium = {
	opinion = 25
	decay = 1
	accumulative = no
}

staid_tr_alignment_high = {
	opinion = 40
	decay = 1
	accumulative = no
}
```

## mods/StellarAIDirector/common/policies/zzzz_staid_10_opening_growth_policies.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Verified full-object policy overrides from installed vanilla diplomatic and orbital bombardment policies.

diplomatic_stance = {
	potential = {
		OR = {
			is_country_type = default
			is_country_type = fallen_empire
			is_country_type = awakened_fallen_empire
			is_country_type = primitive
			is_country_type = awakened_marauders
			is_country_type = mirrored_country
			is_country_type = exiled
		}
	}

	allow = {
		is_at_war = no # Not allowed to change policies in this group while at war
	}

	option = {
		name = "diplo_stance_belligerent"
		icon = "GFX_diplomatic_stance_belligerent"

		potential = {
			OR = {
				is_country_type = default
				is_country_type = awakened_fallen_empire
			}
			is_nomadic = no
		}

		valid = {
			NOT = { has_valid_civic = civic_inwards_perfection }
			is_homicidal = no # They have their own variants of this
		}

		policy_flags = {
			diplo_stance_belligerent
		}

		modifier = {
			country_war_exhaustion_mult = -0.1
			country_naval_cap_mult = 0.1
			country_claim_influence_cost_mult = -0.1
			external_leader_pool_add = -1
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			# Pacifists
			modifier = { # Fanatic Pacifists will *only* go belligerent if there's a rival neighbor...
				factor = 0
				has_ethic = ethic_fanatic_pacifist
				NOT = {
					any_neighbor_country = {
						is_rival = root
					}
				}
			}
			modifier = { # Regular Pacifists have only a small chance to go belligerent unless there's a rival neighbor...
				factor = 0.5
				has_ethic = ethic_pacifist
				NOT = {
					any_neighbor_country = {
						is_rival = root
					}
				}
			}
			modifier = {
				factor = 0.5 # ...but they're still less likely to.
				is_pacifist = yes
			}

			# Angry people like to be belligerent
			modifier = {
				factor = 2.0
				has_ethic = ethic_fanatic_militarist
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_militarist
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_fanatic_authoritarian
			}
			modifier = {
				factor = 1.25
				has_ethic = ethic_authoritarian
			}
			modifier = {
				factor = 5.0 # Intentionally high value for despoilers/Nihilistic Acquisition
				is_slaver = yes
			}
			modifier = {
				factor = 1.5
				has_valid_civic = civic_nationalistic_zeal
			}
			modifier = {
				factor = 1.5
				OR = {
					has_valid_civic = civic_hive_strength_of_legions
					has_valid_civic = civic_machine_warbots
					has_valid_civic = civic_private_military_companies
					has_valid_civic = civic_warrior_culture
				}
			}

			modifier = {
				factor = 1.5
				has_ai_personality_behaviour = conqueror
			}
			modifier = {
				factor = 1.5
				has_ai_personality_behaviour = subjugator
			}

			modifier = {
				factor = 3.0 # Blocked in propagators get ANGRY
				has_ai_expansion_plan = no
				has_ai_personality_behaviour = propagator
			}
		}
	}

	option = {
		name = "diplo_stance_cooperative"
		icon = "GFX_diplomatic_stance_cooperative"

		potential = {
			OR = {
				is_country_type = default
				is_country_type = awakened_fallen_empire
				is_country_type = mirrored_country
			}
			is_nomadic = no
		}

		valid = {
			NOT = { has_valid_civic = civic_inwards_perfection }
			is_unfriendly = no # Not homicidal or barbaric despoilers
		}

		policy_flags = {
			diplo_stance_cooperative
		}

		modifier = {
			diplo_weight_mult = 0.25
			envoy_improve_relations_mult = 0.5
			country_border_friction_mult = -0.5
			operations_cost_mult = 0.25
			operations_upkeep_mult = 0.25
			external_leader_pool_add = 1
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0.01
				has_ascension_perk = ap_become_the_crisis
			}

			modifier = {
				factor = 0
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			# Tons of Ethics modifiers!
			# Cranky people:
			modifier = {
				factor = 0
				is_fanatic_xenophobe = yes
			}
			modifier = {
				factor = 0.1
				has_ethic = ethic_xenophobe
			}
			modifier = {
				factor = 0.5
				has_ethic = ethic_fanatic_authoritarian
			}
			modifier = {
				factor = 0.75
				has_ethic = ethic_authoritarian
			}

			# Nice people:
			modifier = {
				factor = 2.0
				has_ethic = ethic_fanatic_xenophile
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_xenophile
			}
			modifier = {
				factor = 1.3
				has_valid_civic = civic_machine_exploration_protocol
			}
			modifier = {
				factor = 1.3
				has_ethic = ethic_fanatic_pacifist
			}
			modifier = {
				factor = 1.15
				has_ethic = ethic_pacifist
			}
			modifier = {
				factor = 1.3
				has_ethic = ethic_fanatic_egalitarian
			}
			modifier = {
				factor = 1.15
				has_ethic = ethic_egalitarian
			}
			modifier = {
				factor = 1.1
				has_ethic = ethic_fanatic_materialist
			}
			modifier = {
				factor = 1.05
				has_ethic = ethic_materialist
			}

			modifier = {
				factor = 1.25
				has_ai_personality_behaviour = multispecies
			}

			modifier = {
				factor = 3.0
				has_ai_personality = federation_builders
			}

			modifier = {
				factor = 3.0
				has_ai_personality = hive_mind_friend
			}

			modifier = {
				factor = 3.0
				has_country_flag = fallen_empire_hive_control
			}
			modifier = { factor = 12 staid_opening_route_research_priority = yes NOT = { staid_security_existential = yes } }
		}
	}

	option = {
		name = "diplo_stance_isolationist"
		icon = "GFX_diplomatic_stance_isolationist"

		potential = {
			OR = {
				is_country_type = default
				is_country_type = awakened_fallen_empire
				is_country_type = exiled
			}
			is_nomadic = no
		}

		valid = {
			is_megacorp = no # "NO! YOU CAN'T BUY OUR STUFF!" makes the shareholders sad
			is_homicidal = no # Homicidal variants below
		}

		policy_flags = {
			diplo_stance_isolationist
		}

		modifier = {
			country_unity_produces_mult = 0.10
			diplo_weight_mult = -0.25
			diplomacy_upkeep_mult = 1
			pop_government_ethic_attraction = 0.25
			country_border_friction_mult = 2.0
			external_leader_pool_add = -2
		}

		on_enabled = {
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0.01
				has_ascension_perk = ap_become_the_crisis
			}

			modifier = {
				factor = 0.25 # Let the isolationists start in this if they want
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			modifier = {
				factor = 0
				OR = {
					has_ai_personality = federation_builders
					has_ai_personality = fanatic_befrienders
				}
			}

			modifier = {
				factor = 100.0 # Inwards Perfection should almost always go isolationist
				has_valid_civic = civic_inwards_perfection
			}

			modifier = {
				factor = 3.0
				has_ai_personality_behaviour = isolationist
			}

			modifier = {
				factor = 2.0
				is_xenophobe = yes
				is_militarist = no
				is_authoritarian = no
			}
		}
	}

	option = {
		name = "diplo_stance_expansionist"
		icon = "GFX_diplomatic_stance_expansionist"

		potential = {
			is_wilderness_empire = no
			is_nomadic = no
			OR = {
				is_country_type = default
				is_country_type = awakened_fallen_empire
			}
		}

		valid = {
			is_homicidal = no
		}

		policy_flags = {
			diplo_stance_expansionist
		}

		modifier = {
			starbase_outpost_cost_mult = -0.10
			planet_colony_development_speed_mult = 0.15
			country_border_friction_mult = 1.0
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 2
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			modifier = {
				factor = 0.01
				has_ascension_perk = ap_become_the_crisis
			}
			modifier = { factor = 4 staid_opening_military_to_pops = yes staid_has_safe_basic_stockpiles = yes }
		}
	}

	option = {
		name = "diplo_stance_expansionist_wilderness"
		icon = "GFX_diplomatic_stance_expansionist"

		potential = {
			is_wilderness_empire = yes
			OR = {
				is_country_type = default
				is_country_type = awakened_fallen_empire
			}
		}

		valid = {
			is_homicidal = no
		}

		policy_flags = {
			diplo_stance_expansionist
		}

		modifier = {
			starbase_outpost_cost_mult = -0.10
			terraform_speed_mult = 0.15
			country_border_friction_mult = 1.0
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 2
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			modifier = {
				factor = 0.01
				has_ascension_perk = ap_become_the_crisis
			}
		}
	}

	option = {
		name = "diplo_stance_mercantile"
		icon = "GFX_diplomatic_stance_mercantile"

		potential = {
			OR = {
				is_country_type = default
				is_country_type = awakened_fallen_empire
				is_country_type = mirrored_country
			}
			is_gestalt = no
		}

		valid = {
			NOT = { has_valid_civic = civic_inwards_perfection }
			is_homicidal = no
			# some ugliness to preserve the
			# auth/civic - potential/valid divide for tooltip
			if = {
				limit = {
					has_megacorp = yes
					is_megacorp = yes
				}
				is_megacorp = yes
			}
			else_if = {
				limit = { has_megacorp = yes }
				has_civic = civic_merchant_guilds
			}
			else = { has_civic = civic_corporate_dominion }
		}

		policy_flags = {
			diplo_stance_mercantile
		}

		modifier = {
			diplo_weight_economy_mult = 0.25
			country_trade_produces_mult = 0.1
			external_leader_pool_add = 1
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0.01
				has_ascension_perk = ap_become_the_crisis
			}
			modifier = {
				factor = 3.0
				is_megacorp = yes # Megacorps should generally prefer this diplo stance unless their ethics get them to specialize differently
			}
			modifier = {
				factor = 1.25
				has_valid_civic = civic_free_traders
			}
			modifier = {
				factor = 10
				should_ai_focus_on_trade = yes
			}
			modifier = {
				factor = 0.65
				OR = {
					has_valid_civic = civic_private_prospectors
					has_valid_civic = civic_private_military_companies
				}
			}
			modifier = { factor = 5 staid_opening_trade_to_research = yes }
		}
	}

	option = {
		name = "diplo_stance_supremacist"
		icon = "GFX_diplomatic_stance_supremacy"

		potential = {
			OR = {
				is_country_type = awakened_fallen_empire
				is_country_type = awakened_marauders
				is_country_type = default
				is_country_type = mirrored_country
			}
			is_nomadic = no
		}
		valid = {
			NOR = {
				has_valid_civic = civic_inwards_perfection
				has_modifier = humiliated
			}
			is_homicidal = no
			custom_tooltip = {
				fail_text = "requires_supremacy_traditions"
				OR = {
					has_tradition = tr_supremacy_finish
					NOT = { is_country_type = default }
				}
			}
			is_subject = no
		}

		policy_flags = {
			diplo_stance_supremacist
		}

		modifier = {
			diplo_weight_naval_mult = 1.00
			diplo_weight_economy_mult = -0.5
			diplo_weight_technology_mult = -0.5
			country_war_exhaustion_mult = -0.20
			country_naval_cap_mult = 0.20
			country_claim_influence_cost_mult = -0.1
		}

		on_enabled = {
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			modifier = {
				factor = 0
				is_pacifist = yes
			}

			modifier = {
				factor = 10
				OR = {
					is_country_type = awakened_fallen_empire
					is_country_type = awakened_marauders
				}
			}

			# Angry people want to be Supreme
			modifier = {
				factor = 2.0
				has_ethic = ethic_fanatic_militarist
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_militarist
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_fanatic_authoritarian
			}
			modifier = {
				factor = 1.25
				has_ethic = ethic_authoritarian
			}
			modifier = {
				factor = 1.25 # Despoilers/Nihilistic Acquisition intentionally get a higher multiplier for Belligerent than Supremacist
				is_slaver = yes
			}
			modifier = {
				factor = 2
				has_valid_civic = civic_nationalistic_zeal
			}
			modifier = {
				factor = 3
				OR = {
					has_valid_civic = civic_hive_strength_of_legions
					has_valid_civic = civic_machine_warbots
					has_valid_civic = civic_private_military_companies
					has_valid_civic = civic_warrior_culture
					has_country_flag = fallen_empire_hive_war
				}
			}

			modifier = {
				factor = 1.5
				has_ai_personality_behaviour = conqueror
			}
			modifier = {
				factor = 1.5
				has_ai_personality_behaviour = subjugator
			}

			modifier = { # Don't be suicidal
				factor = 0
				any_relation = {
					has_communications = root
					has_policy_flag = diplo_stance_supremacist
					is_country_type = default
					is_subject = no
					relative_power = {
						who = root
						category = fleet
						value = overwhelming
					}
				}
			}
			modifier = {
				factor = 0.25
				any_neighbor_country = {
					has_communications = root
					is_country_type = default
					is_subject = no
					relative_power = {
						who = root
						category = fleet
						value > equivalent
					}
				}
			}
			modifier = { factor = 18 staid_militarist_conquest_strategy = yes }
		}
	}
	option = {
		name = "diplo_stance_animosity"
		icon = "GFX_diplomatic_stance_animosity"

		potential = {
			is_country_type = default
			is_nomadic = no
		}
		valid = {
			is_homicidal = no
			custom_tooltip = {
				fail_text = "requires_enmity_traditions"
				OR = {
					has_tradition = tr_enmity_finish
					NOT = { is_country_type = default }
				}
			}
			is_subject = no
		}

		policy_flags = {
			diplo_stance_animosity
		}

		modifier = {
			max_rivalries = 2
			rivalries_unity_produces_add = 10
			country_border_friction_mult = 1
			diplo_weight_rivals_mult = 0.05
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			modifier = {
				factor = 0
				OR = {
					is_fanatic_xenophile = yes
					has_valid_civic = civic_hive_empath
				}
			}

			modifier = {
				factor = 0
				num_rivals = 0
			}

			# Ambitious people who want to be rivals
			modifier = {
				factor = 2.0
				is_fanatic = yes
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_militarist
			}
			modifier = {
				factor = 1.25
				has_ethic = ethic_authoritarian
			}
			modifier = {
				factor = 2
				OR = {
					has_valid_civic = civic_nationalistic_zeal
					has_valid_civic = civic_pompous_purists
				}
			}
			modifier = {
				factor = 3
				OR = {
					has_valid_civic = civic_hive_strength_of_legions
					has_valid_civic = civic_machine_warbots
					has_valid_civic = civic_private_military_companies
					has_valid_civic = civic_warrior_culture
					has_origin = origin_payback
				}
			}

			modifier = {
				factor = 1.5
				OR = {
					has_ai_personality_behaviour = subjugator
					has_ai_personality_behaviour = opportunist
					has_ai_personality_behaviour = propagator
				}
			}
			modifier = {
				factor = 20
				has_ai_personality = metalhead
			}
		}
	}

	option = {
		name = "diplo_stance_hunger"
		icon = "GFX_diplomatic_stance_rest"

		potential = {
			OR = {
				is_hive_empire = yes
				has_menace_perk = menp_behemoth_ever_hungry
			}
		}

		valid = {
			OR = {
				has_valid_civic = civic_hive_devouring_swarm
				has_menace_perk = menp_behemoth_ever_hungry
			}
		}

		policy_flags = {
			diplo_stance_hunger
		}

		modifier = {
		}

		ai_weight = {
			weight = 100
		}
	}

	option = {
		name = "diplo_stance_extermination"
		icon = "GFX_diplomatic_stance_recompiling"

		potential = {
			is_machine_empire = yes
		}

		valid = {
			has_valid_civic = civic_machine_terminator
		}

		policy_flags = {
			diplo_stance_extermination
		}

		modifier = {
		}

		ai_weight = {
			weight = 100
		}
	}

	option = {
		name = "diplo_stance_purification"
		icon = "GFX_diplomatic_stance_withdrawn"

		valid = {
			has_valid_civic = civic_fanatic_purifiers
		}

		policy_flags = {
			diplo_stance_purification
		}

		modifier = {
		}

		ai_weight = {
			weight = 100
		}
	}

	option = {
		name = "diplo_stance_isolationist_fallen_empire"
		icon = "GFX_diplomatic_stance_isolationist"

		potential = {
			is_country_type = fallen_empire
		}

		policy_flags = {
			diplo_stance_isolationist_fallen_empire
		}

		modifier = {
		}

		ai_weight = {
			weight = 100
		}
	}

	option = {
		name = "diplo_stance_ignorant"
		icon = "GFX_diplomatic_stance_isolationist"

		potential = {
			is_country_type = primitive
			current_awareness_level < medium
			capital_scope = {
				NOT = { has_modifier = culture_shock_diplomacy }
			}
		}

		policy_flags = {
			diplo_stance_ignorant
		}

		modifier = {
		}

		ai_weight = {
			weight = 1
		}
	}

	option = {
		name = "diplo_stance_questioning"
		icon = "GFX_diplomatic_stance_expansionist"

		potential = {
			is_country_type = primitive
			current_awareness_level = medium
			capital_scope = {
				NOT = { has_modifier = culture_shock_diplomacy }
			}
		}

		policy_flags = {
			diplo_stance_questioning
		}

		modifier = {
		}

		ai_weight = {
			weight = 1
		}
	}

	option = {
		name = "diplo_stance_eager"
		icon = "GFX_diplomatic_stance_cooperative"

		potential = {
			is_country_type = primitive
			current_awareness_level >= high
			is_xenophile = yes
			capital_scope = {
				NOT = { has_modifier = culture_shock_diplomacy }
			}
		}

		policy_flags = {
			diplo_stance_eager
		}

		modifier = {
		}

		ai_weight = {
			weight = 1
		}
	}

	option = {
		name = "diplo_stance_fearful"
		icon = "GFX_diplomatic_stance_withdrawn"

		potential = {
			is_country_type = primitive
			current_awareness_level >= high
			is_xenophobe = yes
			capital_scope = {
				NOT = { has_modifier = culture_shock_diplomacy }
			}
		}

		policy_flags = {
			diplo_stance_fearful
		}

		modifier = {
		}

		ai_weight = {
			weight = 1
		}
	}

	option = {
		name = "diplo_stance_uncertain"
		icon = "GFX_diplomatic_stance_isolationist"

		potential = {
			is_country_type = primitive
			current_awareness_level >= high
			is_xenophile = no
			is_xenophobe = no
			capital_scope = {
				NOT = { has_modifier = culture_shock_diplomacy }
			}
		}

		policy_flags = {
			diplo_stance_uncertain
		}

		modifier = {
		}

		ai_weight = {
			weight = 1
		}
	}

	option = {
		name = "diplo_stance_culture_shock"
		icon = "GFX_diplomatic_stance_belligerent"

		potential = {
			is_country_type = primitive
			capital_scope = {
				has_modifier = culture_shock_diplomacy
			}
		}

		policy_flags = {
			diplo_stance_culture_shock
		}

		modifier = {
			diplo_action_acceptance_add = -100
		}

		ai_weight = {
			weight = 100
		}
	}

	option = {
		name = "diplo_stance_devastators"
		icon = "GFX_diplomatic_stance_devastators"

		potential = {
			OR = {
				has_valid_civic = civic_scorched_earth
				has_valid_civic = civic_hive_scorched_earth
			}
		}

		valid = {
			OR = {
				has_valid_civic = civic_scorched_earth
				has_valid_civic = civic_hive_scorched_earth
			}
		}

		policy_flags = {
			diplo_stance_purification
		}

		modifier = {
		}

		ai_weight = {
			weight = 100
		}
	}

	#Nomadic stance variants because triggered modifiers arent supported:

	option = {
		name = "diplo_stance_belligerent_nomad"
		icon = "GFX_diplomatic_stance_belligerent"

		potential = {
			is_nomadic = yes
		}

		valid = {
			NOT = { has_valid_civic = civic_inwards_perfection }
			is_homicidal = no # They have their own variants of this
		}

		policy_flags = {
			diplo_stance_belligerent
		}

		modifier = {
			country_war_exhaustion_mult = -0.1
			country_naval_cap_mult = 0.1
			starbase_waystations_upkeep_mult = -0.2
			starbase_waystations_modules_upkeep_mult = -0.2
			external_leader_pool_add = -1
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			# Pacifists
			modifier = { # Fanatic Pacifists will *only* go belligerent if there's a rival neighbor...
				factor = 0
				has_ethic = ethic_fanatic_pacifist
				NOT = {
					any_neighbor_country = {
						is_rival = root
					}
				}
			}
			modifier = { # Regular Pacifists have only a small chance to go belligerent unless there's a rival neighbor...
				factor = 0.5
				has_ethic = ethic_pacifist
				NOT = {
					any_neighbor_country = {
						is_rival = root
					}
				}
			}
			modifier = {
				factor = 0.5 # ...but they're still less likely to.
				is_pacifist = yes
			}

			# Angry people like to be belligerent
			modifier = {
				factor = 2.0
				has_ethic = ethic_fanatic_militarist
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_militarist
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_fanatic_authoritarian
			}
			modifier = {
				factor = 1.25
				has_ethic = ethic_authoritarian
			}
			modifier = {
				factor = 5.0 # Intentionally high value for despoilers/Nihilistic Acquisition
				is_slaver = yes
			}
			modifier = {
				factor = 1.5
				has_valid_civic = civic_nationalistic_zeal
			}
			modifier = {
				factor = 1.5
				OR = {
					has_valid_civic = civic_hive_strength_of_legions
					has_valid_civic = civic_machine_warbots
					has_valid_civic = civic_private_military_companies
					has_valid_civic = civic_warrior_culture
				}
			}

			modifier = {
				factor = 1.5
				has_ai_personality_behaviour = conqueror
			}
			modifier = {
				factor = 1.5
				has_ai_personality_behaviour = subjugator
			}

			modifier = {
				factor = 3.0 # Blocked in propagators get ANGRY
				has_ai_expansion_plan = no
				has_ai_personality_behaviour = propagator
			}
		}
	}

	option = {
		name = "diplo_stance_cooperative_nomad"
		icon = "GFX_diplomatic_stance_cooperative"

		potential = {
			is_nomadic = yes
		}

		valid = {
			NOT = { has_valid_civic = civic_inwards_perfection }
			is_unfriendly = no # Not homicidal or barbaric despoilers
		}

		policy_flags = {
			diplo_stance_cooperative
		}

		modifier = {
			diplo_weight_mult = 0.25
			envoy_improve_relations_mult = 0.5
			unlicensed_waystations_scaling_mult = -0.5
			operations_cost_mult = 0.25
			operations_upkeep_mult = 0.25
			external_leader_pool_add = 1
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0.01
				has_ascension_perk = ap_become_the_crisis
			}

			modifier = {
				factor = 0
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			# Tons of Ethics modifiers!
			# Cranky people:
			modifier = {
				factor = 0
				is_fanatic_xenophobe = yes
			}
			modifier = {
				factor = 0.1
				has_ethic = ethic_xenophobe
			}
			modifier = {
				factor = 0.5
				has_ethic = ethic_fanatic_authoritarian
			}
			modifier = {
				factor = 0.75
				has_ethic = ethic_authoritarian
			}

			# Nice people:
			modifier = {
				factor = 2.0
				has_ethic = ethic_fanatic_xenophile
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_xenophile
			}
			modifier = {
				factor = 1.3
				has_valid_civic = civic_machine_exploration_protocol
			}
			modifier = {
				factor = 1.3
				has_ethic = ethic_fanatic_pacifist
			}
			modifier = {
				factor = 1.15
				has_ethic = ethic_pacifist
			}
			modifier = {
				factor = 1.3
				has_ethic = ethic_fanatic_egalitarian
			}
			modifier = {
				factor = 1.15
				has_ethic = ethic_egalitarian
			}
			modifier = {
				factor = 1.1
				has_ethic = ethic_fanatic_materialist
			}
			modifier = {
				factor = 1.05
				has_ethic = ethic_materialist
			}

			modifier = {
				factor = 1.25
				has_ai_personality_behaviour = multispecies
			}

			modifier = {
				factor = 3.0
				has_ai_personality = federation_builders
			}

			modifier = {
				factor = 3.0
				has_ai_personality = hive_mind_friend
			}

			modifier = {
				factor = 3.0
				has_country_flag = fallen_empire_hive_control
			}
		}
	}

	option = {
		name = "diplo_stance_isolationist_nomad"
		icon = "GFX_diplomatic_stance_isolationist"

		potential = {
			is_nomadic = yes
		}

		valid = {
			is_megacorp = no # "NO! YOU CAN'T BUY OUR STUFF!" makes the shareholders sad
			is_homicidal = no # Homicidal variants below
		}

		policy_flags = {
			diplo_stance_isolationist
		}

		modifier = {
			country_unity_produces_mult = 0.10
			diplo_weight_mult = -0.25
			diplomacy_upkeep_mult = 1
			pop_government_ethic_attraction = 0.25
			unlicensed_waystations_scaling_mult = 2
			external_leader_pool_add = -2
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0.01
				has_ascension_perk = ap_become_the_crisis
			}

			modifier = {
				factor = 0.25 # Let the isolationists start in this if they want
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			modifier = {
				factor = 0
				OR = {
					has_ai_personality = federation_builders
					has_ai_personality = fanatic_befrienders
				}
			}

			modifier = {
				factor = 100.0 # Inwards Perfection should almost always go isolationist
				has_valid_civic = civic_inwards_perfection
			}

			modifier = {
				factor = 3.0
				has_ai_personality_behaviour = isolationist
			}

			modifier = {
				factor = 2.0
				is_xenophobe = yes
				is_militarist = no
				is_authoritarian = no
			}
		}
	}

	option = {
		name = "diplo_stance_supremacist_nomad"
		icon = "GFX_diplomatic_stance_supremacy"

		potential = {
			OR = {
				is_country_type = awakened_fallen_empire
				is_country_type = awakened_marauders
				is_country_type = default
				is_country_type = mirrored_country
			}
			is_nomadic = yes
		}
		valid = {
			NOR = {
				has_valid_civic = civic_inwards_perfection
				has_modifier = humiliated
			}
			is_homicidal = no
			custom_tooltip = {
				fail_text = "requires_supremacy_traditions"
				OR = {
					has_tradition = tr_supremacy_finish
					NOT = { is_country_type = default }
				}
			}
			is_subject = no
		}

		policy_flags = {
			diplo_stance_supremacist
		}

		modifier = {
			diplo_weight_naval_mult = 1.00
			diplo_weight_economy_mult = -0.5
			diplo_weight_technology_mult = -0.5
			country_war_exhaustion_mult = -0.20
			country_naval_cap_mult = 0.20
			starbase_waystations_upkeep_mult = -0.2
			starbase_waystations_modules_upkeep_mult = -0.2
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			modifier = {
				factor = 0
				is_pacifist = yes
			}

			modifier = {
				factor = 10
				OR = {
					is_country_type = awakened_fallen_empire
					is_country_type = awakened_marauders
				}
			}

			# Angry people want to be Supreme
			modifier = {
				factor = 2.0
				has_ethic = ethic_fanatic_militarist
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_militarist
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_fanatic_authoritarian
			}
			modifier = {
				factor = 1.25
				has_ethic = ethic_authoritarian
			}
			modifier = {
				factor = 1.25 # Despoilers/Nihilistic Acquisition intentionally get a higher multiplier for Belligerent than Supremacist
				is_slaver = yes
			}
			modifier = {
				factor = 2
				has_valid_civic = civic_nationalistic_zeal
			}
			modifier = {
				factor = 3
				OR = {
					has_valid_civic = civic_hive_strength_of_legions
					has_valid_civic = civic_machine_warbots
					has_valid_civic = civic_private_military_companies
					has_valid_civic = civic_warrior_culture
					has_country_flag = fallen_empire_hive_war
				}
			}

			modifier = {
				factor = 1.5
				has_ai_personality_behaviour = conqueror
			}
			modifier = {
				factor = 1.5
				has_ai_personality_behaviour = subjugator
			}

			modifier = { # Don't be suicidal
				factor = 0
				any_relation = {
					has_communications = root
					has_policy_flag = diplo_stance_supremacist
					is_country_type = default
					is_subject = no
					relative_power = {
						who = root
						category = fleet
						value = overwhelming
					}
				}
			}
			modifier = {
				factor = 0.25
				any_neighbor_country = {
					has_communications = root
					is_country_type = default
					is_subject = no
					relative_power = {
						who = root
						category = fleet
						value > equivalent
					}
				}
			}
		}
	}
	option = {
		name = "diplo_stance_animosity_nomad"
		icon = "GFX_diplomatic_stance_animosity"

		potential = {
			is_country_type = default
			is_nomadic = yes
		}
		valid = {
			is_homicidal = no
			custom_tooltip = {
				fail_text = "requires_enmity_traditions"
				OR = {
					has_tradition = tr_enmity_finish
					NOT = { is_country_type = default }
				}
			}
			is_subject = no
		}

		policy_flags = {
			diplo_stance_animosity
		}

		modifier = {
			max_rivalries = 2
			rivalries_unity_produces_add = 10
			unlicensed_waystations_scaling_mult = 1
			diplo_weight_rivals_mult = 0.05
		}

		ai_weight = {
			weight = 10

			modifier = {
				factor = 0
				NOT = { has_country_flag = has_encountered_other_empire }
			}

			modifier = {
				factor = 0
				OR = {
					is_fanatic_xenophile = yes
					has_valid_civic = civic_hive_empath
				}
			}

			modifier = {
				factor = 0
				num_rivals = 0
			}

			# Ambitious people who want to be rivals
			modifier = {
				factor = 2.0
				is_fanatic = yes
			}
			modifier = {
				factor = 1.5
				has_ethic = ethic_militarist
			}
			modifier = {
				factor = 1.25
				has_ethic = ethic_authoritarian
			}
			modifier = {
				factor = 2
				OR = {
					has_valid_civic = civic_nationalistic_zeal
					has_valid_civic = civic_pompous_purists
				}
			}
			modifier = {
				factor = 3
				OR = {
					has_valid_civic = civic_hive_strength_of_legions
					has_valid_civic = civic_machine_warbots
					has_valid_civic = civic_private_military_companies
					has_valid_civic = civic_warrior_culture
					has_origin = origin_payback
				}
			}

			modifier = {
				factor = 1.5
				OR = {
					has_ai_personality_behaviour = subjugator
					has_ai_personality_behaviour = opportunist
					has_ai_personality_behaviour = propagator
				}
			}
			modifier = {
				factor = 20
				has_ai_personality = metalhead
			}
		}
	}
}
orbital_bombardment = {

	potential = {
		OR = {
			is_country_type = default
			is_country_type = vol
		}
	}

	option = {
		name = "orbital_bombardment_selective"
		policy_flags = {
			orbital_bombardment_selective
		}

		valid = {
			NOT = {
				has_event_chain = contract_raid_planet_chain
			}
		}

		ai_weight = {
			modifier = {
				factor = 0
				NOR = {
					has_ethic = "ethic_pacifist"
					has_ethic = "ethic_fanatic_pacifist"
				}
				NOT = {
					is_galactic_community_member = yes
					OR = {
						is_active_resolution = "resolution_rulesofwar_independent_tribunals"
						is_active_resolution = "resolution_rulesofwar_last_resort_doctrine"
						is_active_resolution = "resolution_rulesofwar_demobilization_initiative"
					}
				}
			}
		}
	}
	option = {
		name = "orbital_bombardment_indiscriminate"

		in_breach_of = {
			{
				key = resolution_rulesofwar_independent_tribunals
			}
			{
				key = resolution_rulesofwar_last_resort_doctrine
			}
			{
				key = resolution_rulesofwar_demobilization_initiative
			}
		}

		policy_flags = {
			orbital_bombardment_indiscriminate
		}
		modifier = {}

		valid = {
			NOR = {
				has_ethic = "ethic_pacifist"
				has_ethic = "ethic_fanatic_pacifist"
			}
		}
		ai_weight = {
			modifier = {
				factor = 0.1
				is_galactic_community_member = yes
				OR = {
					is_active_resolution = "resolution_rulesofwar_independent_tribunals"
					is_active_resolution = "resolution_rulesofwar_last_resort_doctrine"
					is_active_resolution = "resolution_rulesofwar_demobilization_initiative"
				}
			}
			modifier = { factor = 18 staid_militarist_conquest_strategy = yes }
			modifier = { factor = 8 staid_opening_military_to_pops = yes staid_has_safe_basic_stockpiles = yes }
		}
	}
	option = {
		name = "orbital_bombardment_armageddon"

		in_breach_of = {
			{
				key = resolution_rulesofwar_independent_tribunals
			}
			{
				key = resolution_rulesofwar_last_resort_doctrine
			}
			{
				key = resolution_rulesofwar_demobilization_initiative
			}
		}

		potential = {
			OR = {
				has_valid_civic = civic_fanatic_purifiers
				has_valid_civic = civic_machine_terminator
			}
		}

		policy_flags = {
			orbital_bombardment_armageddon
		}
		modifier = {}

		ai_weight = {
			modifier = {
				factor = 10
				OR = {
					has_valid_civic = civic_fanatic_purifiers
					has_valid_civic = civic_machine_terminator
				}
			}
			modifier = {
				factor = 10
				has_ascension_perk = ap_become_the_crisis
			}
		}
	}

	option = {
		name = "orbital_bombardment_devastation"

		in_breach_of = {
			{
				key = resolution_rulesofwar_independent_tribunals
			}
			{
				key = resolution_rulesofwar_last_resort_doctrine
			}
			{
				key = resolution_rulesofwar_demobilization_initiative
			}
		}

		potential = {
			OR = {
				has_valid_civic = civic_scorched_earth
				has_valid_civic = civic_hive_scorched_earth
			}
		}

		policy_flags = {
			orbital_bombardment_devastation
		}
		modifier = {}

		ai_weight = {
			modifier = {
				factor = 10
				OR = {
					has_valid_civic = civic_scorched_earth
					has_valid_civic = civic_hive_scorched_earth
				}
			}
			modifier = {
				factor = 10
				has_ascension_perk = ap_become_the_crisis
			}
		}
	}
}
orbital_bombardment_accept_surrender = {

	potential = {
		is_homicidal = no
	}

	option = {
		name = "orbital_bombardment_surrender_forbidden"

		policy_flags = {
			orbital_bombardment_surrender_forbidden
		}
		modifier = {}


		ai_weight = {
			base = 1
			modifier = { factor = 80 staid_raiding_pop_growth_strategy = yes }
			modifier = { factor = 20 staid_militarist_conquest_strategy = yes }
			modifier = { factor = 8 staid_opening_military_to_pops = yes staid_has_safe_basic_stockpiles = yes }
			modifier = {
				factor = 0.01
				NOT = { staid_raiding_pop_growth_strategy = yes }
				NOT = { staid_militarist_conquest_strategy = yes }
				NOT = { staid_opening_military_to_pops = yes }
			}
		}
	}

	option = {
		name = "orbital_bombardment_surrender_allowed"

		potential = {
			is_homicidal = no #locked to "forbidden"
		}

		policy_flags = {
			orbital_bombardment_surrender_allowed
		}
	}
}
```

## mods/StellarAIDirector/common/script_values/zzz_staid_roi_values.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Numeric anchors for documentation, debug events, and future generated gates.

staid_alloy_equivalent_alloys = 1
staid_alloy_equivalent_minerals = 0.35
staid_alloy_equivalent_energy = 0.25
staid_alloy_equivalent_consumer_goods = 0.75
staid_alloy_equivalent_unity = 0.50
staid_min_megastructure_prep_alloys = 15000
staid_min_megastructure_prep_income_alloys = 130
staid_shipyard_payoff_stockpile_alloys = 12000
staid_shipyard_payoff_income_alloys = 150
staid_roi_matrix_eligible_rows = 140
staid_safe_deficit_runway_months = 24
```

## mods/StellarAIDirector/common/script_values/zzz_staid_threat_response_values.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Source of truth: tools/stellar_ai_director_lib.py threat-response tables.
staid_tr_anti_aggressor_score_min = 0
staid_tr_anti_aggressor_score_max = 100
staid_tr_alignment_score_min = 0
staid_tr_alignment_score_max = 60
staid_tr_defensive_readiness_score_min = 0
staid_tr_defensive_readiness_score_max = 50
staid_tr_relation_flag_days = 7200
staid_tr_country_flag_days = 7200
staid_tr_economy_ratio_cap_percent = 20
staid_tr_economy_alloys_cap = 7
staid_tr_economy_energy_cap = 6
staid_tr_economy_naval_cap = 40
staid_tr_anti_aggressor_low_cutoff = 25
staid_tr_anti_aggressor_medium_cutoff = 45
staid_tr_anti_aggressor_high_cutoff = 65
staid_tr_anti_aggressor_severe_cutoff = 85
staid_tr_alignment_low_cutoff = 20
staid_tr_alignment_medium_cutoff = 35
staid_tr_alignment_high_cutoff = 50
staid_tr_defensive_readiness_low_cutoff = 25
staid_tr_defensive_readiness_high_cutoff = 40
```

## mods/StellarAIDirector/common/scripted_effects/zzz_staid_gigas_habitat_compat_effects.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object scripted-effect compatibility override for Gigas 4.4 habitat orbitals.
# The copied Gigas effects probe removed *_orbital_resource ship-size keys.
# No active 4.4 source defines a replacement orbital ship_size key, so fail that probe closed.

science_kilo_update_orbital_effect = {
	# Find the orbital and habitat complex and save them as event targets
	if = {
		limit = {
			any_fleet_in_orbit = {
				OR = {
					always = no # removed stale major_orbital_resource ship-size probe
					always = no # removed stale minor_orbital_resource ship-size probe
				}
			}
		}

		random_fleet_in_orbit = {
			limit = {
				OR = {
					always = no # removed stale major_orbital_resource ship-size probe
					always = no # removed stale minor_orbital_resource ship-size probe
				}
			}
			save_event_target_as = target_orbital
		}

		solar_system = {
			random_system_planet = {
				limit = {
					has_planet_flag = habitat
				}
				save_event_target_as = target_habitat
			}
		}

		last_added_deposit = {
			switch = {
				trigger = is_deposit_type
				# Minerals
				d_physics_2 = {
					event_target:target_orbital = {
						set_fleet_flag = science_orbital
					}
				}
                d_society_2 = {
					event_target:target_orbital = {
						set_fleet_flag = science_orbital
					}
                }
                d_engineering_2 = {
					event_target:target_orbital = {
						set_fleet_flag = science_orbital
					}
                }
			}
		}
	}
}

giga_dismantle_science_kilo_effect = {
	# USES $TYPE$ AND $FLAG$
	# Find the orbital and habitat complex and save them as event targets
	if = {
		limit = {
			any_fleet_in_orbit = {
				OR = {
					always = no # removed stale major_orbital_resource ship-size probe
					always = no # removed stale minor_orbital_resource ship-size probe
				}
			}
		}

		random_fleet_in_orbit = {
			limit = {
				OR = {
					always = no # removed stale major_orbital_resource ship-size probe
					always = no # removed stale minor_orbital_resource ship-size probe
				}
			}
			save_event_target_as = target_orbital
		}

		solar_system = {
			random_system_planet = {
				limit = {
					has_planet_flag = habitat
				}
				save_event_target_as = target_habitat
			}
		}
	}

	switch = {
		trigger = has_planet_flag
		giga_$FLAG$_stage_4 = {
			remove_deposit = d_$TYPE$_1
			remove_deposit = d_$TYPE$_1
			remove_deposit = d_$TYPE$_2
			remove_deposit = d_$TYPE$_2
			remove_modifier = orbital_$FLAG$_4_mod

			remove_planet_flag = giga_$FLAG$_stage_4
			remove_planet_flag = giga_$FLAG$_stage_3
			remove_planet_flag = giga_$FLAG$_stage_2
			remove_planet_flag = giga_$FLAG$_stage_1
		}
		giga_$FLAG$_stage_3 = {
			remove_deposit = d_$TYPE$_1
			remove_deposit = d_$TYPE$_2
			remove_deposit = d_$TYPE$_2
			remove_modifier = orbital_$FLAG$_3_mod

			remove_planet_flag = giga_$FLAG$_stage_3
			remove_planet_flag = giga_$FLAG$_stage_2
			remove_planet_flag = giga_$FLAG$_stage_1
		}
		giga_$FLAG$_stage_2 = {
			remove_deposit = d_$TYPE$_2
			remove_deposit = d_$TYPE$_2

			remove_planet_flag = giga_$FLAG$_stage_2
			remove_planet_flag = giga_$FLAG$_stage_1
		}
		giga_$FLAG$_stage_1 = {
			remove_deposit = d_$TYPE$_2

			remove_planet_flag = giga_$FLAG$_stage_1
		}
	}
	if = {
		limit = {
			NOT = { has_deposit_for = shipclass_research_station }
			exists = event_target:target_orbital
		}
		event_target:target_orbital = {
			remove_fleet_flag = science_orbital
		}
	}
}
```

## mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Deterministic state gates for late-game investment decisions.

staid_core_deficit_short_runway = {
	OR = {
		has_deficit = energy
		has_deficit = minerals
		has_deficit = alloys
		has_deficit = trade
		AND = { country_uses_consumer_goods = yes has_deficit = consumer_goods }
		AND = { country_uses_food = yes has_deficit = food }
		AND = {
			NOT = { has_monthly_income = { resource = energy value > 0 } }
			resource_stockpile_compare = { resource = energy value < 2400 }
		}
		AND = {
			NOT = { has_monthly_income = { resource = minerals value > 0 } }
			resource_stockpile_compare = { resource = minerals value < 2400 }
		}
		AND = {
			NOT = { has_monthly_income = { resource = alloys value > 0 } }
			resource_stockpile_compare = { resource = alloys value < 2400 }
		}
		AND = {
			NOT = { has_monthly_income = { resource = trade value > 0 } }
			resource_stockpile_compare = { resource = trade value < 2400 }
		}
		AND = {
			country_uses_consumer_goods = yes
			NOT = { has_monthly_income = { resource = consumer_goods value > 0 } }
			resource_stockpile_compare = { resource = consumer_goods value < 2400 }
		}
		AND = {
			country_uses_food = yes
			NOT = { has_monthly_income = { resource = food value > 0 } }
			resource_stockpile_compare = { resource = food value < 2400 }
		}
	}
}

staid_consumer_goods_runway_safe = {
	OR = {
		NOT = { country_uses_consumer_goods = yes }
		AND = {
			NOT = { has_deficit = consumer_goods }
			has_monthly_income = { resource = consumer_goods value > 75 }
			resource_stockpile_compare = { resource = consumer_goods value > 1500 }
		}
	}
}

staid_food_runway_safe = {
	OR = {
		NOT = { country_uses_food = yes }
		AND = {
			NOT = { has_deficit = food }
			has_monthly_income = { resource = food value > 25 }
			resource_stockpile_compare = { resource = food value > 1500 }
		}
	}
}

staid_research_input_runway_safe = {
	staid_consumer_goods_runway_safe = yes
	NOT = { has_deficit = energy }
	has_monthly_income = { resource = energy value > 100 }
	resource_stockpile_compare = { resource = energy value > 3000 }
}

staid_research_diplomacy_priority_ready = {
	NOT = { staid_survival_mode = yes }
	NOT = { staid_core_deficit_short_runway = yes }
	OR = {
		staid_science_nexus_research_priority_ready = yes
		staid_research_input_runway_safe = yes
		has_ethic = ethic_materialist
		has_ethic = ethic_fanatic_materialist
		has_authority = auth_machine_intelligence
		has_active_tradition = tr_discovery_federations_finish
	}
}

staid_basic_economy_runway_safe = {
	staid_research_input_runway_safe = yes
	staid_food_runway_safe = yes
	NOT = { has_deficit = minerals }
	NOT = { has_deficit = alloys }
	has_monthly_income = { resource = minerals value > 100 }
	has_monthly_income = { resource = alloys value > 75 }
	resource_stockpile_compare = { resource = minerals value > 3000 }
	resource_stockpile_compare = { resource = alloys value > 3000 }
}

staid_trade_capacity_safe = {
	NOT = { has_deficit = trade }
	has_monthly_income = { resource = trade value > 25 }
}

staid_trade_fleet_capacity_safe = {
	staid_trade_capacity_safe = yes
	has_monthly_income = { resource = trade value > 75 }
}

staid_trade_planetary_capacity_safe = {
	staid_trade_capacity_safe = yes
	has_monthly_income = { resource = trade value > 50 }
}

staid_trade_surplus_capacity_safe = {
	staid_trade_capacity_safe = yes
	has_monthly_income = { resource = trade value > 100 }
}

staid_high_scale_snowball_pressure = {
	is_nomadic = no
	OR = {
		resource_stockpile_compare = { resource = minerals value > 25000 }
		resource_stockpile_compare = { resource = energy value > 50000 }
		resource_stockpile_compare = { resource = alloys value > 15000 }
		AND = {
			years_passed > 79
			has_monthly_income = { resource = minerals value > 500 }
			has_monthly_income = { resource = energy value > 500 }
			has_monthly_income = { resource = alloys value > 500 }
		}
		AND = {
			years_passed > 119
			resource_stockpile_compare = { resource = minerals value > 12000 }
			resource_stockpile_compare = { resource = energy value > 12000 }
		}
	}
}

staid_catastrophic_collapse_mode = {
	is_nomadic = no
	OR = {
		AND = { has_deficit = energy resource_stockpile_compare = { resource = energy value < 600 } }
		AND = { has_deficit = minerals resource_stockpile_compare = { resource = minerals value < 600 } }
		AND = { has_deficit = alloys resource_stockpile_compare = { resource = alloys value < 600 } }
		AND = { country_uses_consumer_goods = yes has_deficit = consumer_goods resource_stockpile_compare = { resource = consumer_goods value < 400 } }
		AND = { country_uses_food = yes has_deficit = food resource_stockpile_compare = { resource = food value < 400 } }
		AND = { is_at_war = yes highest_threat > 50 used_naval_capacity_percent < 0.45 }
		AND = { recently_lost_war = yes used_naval_capacity_percent < 0.35 }
	}
}

staid_survival_mode = {
	is_nomadic = no
	OR = {
		staid_catastrophic_collapse_mode = yes
		AND = { recently_lost_war = yes used_naval_capacity_percent < 0.45 }
		AND = { is_at_war = yes highest_threat > 60 used_naval_capacity_percent < 0.55 }
	}
}

staid_recovery_mode = {
	is_nomadic = no
	OR = {
		staid_catastrophic_collapse_mode = yes
		AND = { recently_lost_war = yes used_naval_capacity_percent < 0.50 }
	}
}

staid_megastructure_prep_ready = {
	is_nomadic = no
	can_build_megastructures = yes
	OR = {
		NOT = { staid_recovery_mode = yes }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		staid_basic_economy_runway_safe = yes
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		staid_trade_planetary_capacity_safe = yes
		staid_high_scale_snowball_pressure = yes
	}
	resource_stockpile_compare = { resource = alloys value > 8000 }
	has_monthly_income = { resource = alloys value > 80 }
	has_monthly_income = { resource = energy value > 40 }
	has_monthly_income = { resource = minerals value > 40 }
	OR = {
		is_at_war = no
		used_naval_capacity_percent > 0.70
		staid_high_scale_snowball_pressure = yes
	}
}

staid_megastructure_commit_safe = {
	is_nomadic = no
	can_build_megastructures = yes
	OR = {
		NOT = { staid_core_deficit_short_runway = yes }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		staid_basic_economy_runway_safe = yes
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		staid_trade_planetary_capacity_safe = yes
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		is_at_war = no
		used_naval_capacity_percent > 0.65
		staid_high_scale_snowball_pressure = yes
	}
}

staid_megastructure_continuation_priority_ready = {
	staid_megastructure_commit_safe = yes
	OR = {
		NOT = { staid_survival_mode = yes }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		staid_surplus_sink_pressure = yes
		staid_resource_waste_pressure = yes
		staid_high_scale_snowball_pressure = yes
	}
}

staid_pause_new_megastructure = {
	NOT = { staid_high_scale_snowball_pressure = yes }
	OR = {
		staid_survival_mode = yes
		AND = { is_at_war = yes used_naval_capacity_percent < 0.55 }
		AND = { highest_threat > 75 used_naval_capacity_percent < 0.65 }
	}
}

staid_shipyard_payoff_ready = {
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		has_monthly_income = { resource = alloys value > 80 }
		resource_stockpile_compare = { resource = alloys value > 5000 }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		has_monthly_income = { resource = energy value > 80 }
		resource_stockpile_compare = { resource = energy value > 5000 }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		resource_stockpile_compare = { resource = alloys value > 12000 }
		AND = {
			used_naval_capacity_percent < 1.60
			has_monthly_income = { resource = alloys value > 80 }
		}
		AND = {
			used_naval_capacity_percent < 1.40
			has_monthly_income = { resource = alloys value > 80 }
		}
	}
}

staid_fleet_buildup_economy_safe = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	used_naval_capacity_percent < 1.85
	OR = {
		has_monthly_income = { resource = alloys value > 40 }
		resource_stockpile_compare = { resource = alloys value > 1500 }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		has_monthly_income = { resource = energy value > 40 }
		resource_stockpile_compare = { resource = energy value > 1500 }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		AND = {
			resource_stockpile_compare = { resource = alloys value > 15000 }
			resource_stockpile_compare = { resource = energy value > 8000 }
		}
		AND = {
			used_naval_capacity_percent < 1.25
			has_monthly_income = { resource = alloys value > 40 }
			has_monthly_income = { resource = energy value > 40 }
		}
		AND = {
			used_naval_capacity_percent < 1.25
			has_monthly_income = { resource = alloys value > 40 }
			has_monthly_income = { resource = energy value > 40 }
		}
		staid_high_scale_snowball_pressure = yes
	}
}

staid_resource_waste_pressure = {
	OR = {
		AND = {
			has_monthly_income = { resource = minerals value > 0 }
			resource_stockpile_compare = { resource = minerals value > 25000 }
		}
		AND = {
			country_uses_food = yes
			has_monthly_income = { resource = food value > 0 }
			resource_stockpile_compare = { resource = food value > 18000 }
		}
		AND = {
			country_uses_consumer_goods = yes
			has_monthly_income = { resource = consumer_goods value > 0 }
			resource_stockpile_compare = { resource = consumer_goods value > 18000 }
		}
		AND = {
			has_monthly_income = { resource = volatile_motes value > 0 }
			resource_stockpile_compare = { resource = volatile_motes value > 800 }
		}
		AND = {
			has_monthly_income = { resource = exotic_gases value > 0 }
			resource_stockpile_compare = { resource = exotic_gases value > 800 }
		}
		AND = {
			has_monthly_income = { resource = rare_crystals value > 0 }
			resource_stockpile_compare = { resource = rare_crystals value > 800 }
		}
		AND = {
			has_monthly_income = { resource = sr_dark_matter value > 0 }
			resource_stockpile_compare = { resource = sr_dark_matter value > 1000 }
		}
		AND = {
			has_monthly_income = { resource = sr_zro value > 0 }
			resource_stockpile_compare = { resource = sr_zro value > 1000 }
		}
		AND = {
			has_monthly_income = { resource = nanites value > 0 }
			resource_stockpile_compare = { resource = nanites value > 1000 }
		}
		AND = {
			has_technology = tech_ehof_sentient_tier_1
			has_monthly_income = { resource = giga_sr_sentient_metal value > 0 }
			resource_stockpile_compare = { resource = giga_sr_sentient_metal value > 2500 }
		}
	}
}

staid_construction_spenddown_pressure = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_high_scale_snowball_pressure = yes
		staid_resource_waste_pressure = yes
		any_owned_planet = { num_unemployed > 0 free_jobs < 1 }
		any_owned_planet = { free_building_slots > 0 num_unemployed > 0 }
		resource_stockpile_compare = { resource = minerals value > 10000 }
	}
}

staid_research_under_curve = {
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_research_input_runway_safe = yes
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		AND = {
			years_passed > 119
			OR = {
				has_monthly_income = { resource = physics_research value < 1000 }
				has_monthly_income = { resource = society_research value < 1000 }
				has_monthly_income = { resource = engineering_research value < 1200 }
			}
		}
		AND = {
			years_passed > 79
			OR = {
				has_monthly_income = { resource = physics_research value < 750 }
				has_monthly_income = { resource = society_research value < 750 }
				has_monthly_income = { resource = engineering_research value < 900 }
			}
		}
		AND = {
			years_passed > 44
			OR = {
				has_monthly_income = { resource = physics_research value < 400 }
				has_monthly_income = { resource = society_research value < 400 }
				has_monthly_income = { resource = engineering_research value < 550 }
			}
		}
	}
}

staid_surplus_sink_pressure = {
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_research_input_runway_safe = yes
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		NOT = { has_deficit = alloys }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		NOT = { has_deficit = energy }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		staid_resource_waste_pressure = yes
		staid_high_scale_snowball_pressure = yes
		AND = {
			staid_trade_surplus_capacity_safe = yes
			has_monthly_income = { resource = alloys value > 300 }
			has_monthly_income = { resource = energy value > 300 }
			resource_stockpile_compare = { resource = alloys value > 20000 }
		}
	}
}

staid_research_sink_priority_ready = {
	staid_surplus_sink_pressure = yes
}

staid_core_unlock_research_priority_ready = {
	OR = {
		staid_surplus_sink_pressure = yes
		staid_research_under_curve = yes
	}
	OR = {
		NOT = { has_technology = tech_mega_engineering }
		NOT = { has_technology = tech_mega_shipyard }
		staid_research_under_curve = yes
	}
}

staid_early_kilo_economy_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		years_passed > 29
		staid_resource_waste_pressure = yes
		staid_research_under_curve = yes
	}
}

staid_early_kilo_economy_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	OR = {
		has_technology = tech_orbital_arc_furnace
		has_technology = giga_tech_asteroid_manufactory
	}
	OR = {
		staid_resource_waste_pressure = yes
		AND = {
			has_monthly_income = { resource = alloys value > 130 }
			resource_stockpile_compare = { resource = alloys value > 5000 }
		}
	}
}

staid_science_kilo_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_research_under_curve = yes
		AND = {
			years_passed > 24
			staid_early_kilo_economy_research_priority_ready = yes
		}
	}
}

staid_science_kilo_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	OR = {
		has_technology = giga_tech_engineering_test_site
		has_technology = giga_tech_macro_scale_weather_manipulation
	}
	OR = {
		staid_research_under_curve = yes
		AND = {
			has_monthly_income = { resource = alloys value > 90 }
			resource_stockpile_compare = { resource = alloys value > 3000 }
		}
	}
}

staid_pop_assembly_snowball_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_basic_economy_runway_safe = yes
		staid_high_scale_snowball_pressure = yes
		staid_construction_spenddown_pressure = yes
	}
	OR = {
		years_passed > 4
		staid_planetary_capacity_growth_ready = yes
		staid_research_under_curve = yes
	}
}

staid_planetary_computer_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_research_under_curve = yes
		AND = {
			years_passed > 69
			staid_core_unlock_research_priority_ready = yes
		}
	}
}

staid_planetary_computer_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	has_technology = giga_tech_planetary_computer
	OR = {
		staid_research_under_curve = yes
		staid_planetary_capacity_growth_ready = yes
		resource_stockpile_compare = { resource = alloys value > 12000 }
	}
}

staid_science_nexus_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_research_under_curve = yes
		AND = {
			years_passed > 44
			staid_core_unlock_research_priority_ready = yes
		}
	}
}

staid_science_nexus_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	has_technology = tech_science_nexus
	OR = {
		staid_research_under_curve = yes
		resource_stockpile_compare = { resource = alloys value > 15000 }
	}
}

staid_ring_world_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_planetary_capacity_growth_ready = yes
		AND = {
			years_passed > 79
			staid_core_unlock_research_priority_ready = yes
		}
	}
}

staid_ring_world_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	has_technology = tech_ring_world
	OR = {
		staid_planetary_capacity_growth_ready = yes
		resource_stockpile_compare = { resource = alloys value > 20000 }
	}
}

staid_storage_cap_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_resource_waste_pressure = yes
		AND = {
			years_passed > 44
			staid_surplus_sink_pressure = yes
		}
	}
}

staid_storage_cap_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	has_technology = giga_tech_kugelblitz
	OR = {
		staid_resource_waste_pressure = yes
		staid_high_scale_snowball_pressure = yes
		resource_stockpile_compare = { resource = energy value > 25000 }
	}
}

staid_unfinished_kugelblitz_exists = {
	any_owned_megastructure = {
		OR = {
			is_megastructure_type = kugelblitz_0
			is_megastructure_type = kugelblitz_1
			is_megastructure_type = kugelblitz_2
			is_megastructure_type = kugelblitz_restored
		}
	}
}

staid_kugelblitz_new_start_budget_ready = {
	staid_storage_cap_build_priority_ready = yes
	NOT = { has_country_flag = is_currently_building_kugelblitz }
	NOT = { staid_unfinished_kugelblitz_exists = yes }
	NOT = { check_variable = { which = giga_current_kugel value >= 10 } }
	OR = {
		check_variable = { which = giga_current_kugel value < 4 }
		AND = {
			staid_resource_waste_pressure = yes
			check_variable = { which = giga_current_kugel value < 6 }
		}
		AND = {
			staid_high_scale_snowball_pressure = yes
			check_variable = { which = giga_current_kugel value < 8 }
		}
	}
}

staid_phase_mega_engineering_rush = {
	NOT = { has_technology = tech_mega_engineering }
	staid_core_unlock_research_priority_ready = yes
}

staid_phase_early_kilo_economy = {
	OR = {
		NOT = { has_technology = tech_orbital_arc_furnace }
		NOT = { has_technology = giga_tech_asteroid_manufactory }
	}
	staid_early_kilo_economy_research_priority_ready = yes
}

staid_phase_science_kilo_snowball = {
	OR = {
		NOT = { has_technology = giga_tech_engineering_test_site }
		NOT = { has_technology = giga_tech_macro_scale_weather_manipulation }
	}
	staid_science_kilo_research_priority_ready = yes
}

staid_phase_pop_assembly_snowball = {
	staid_pop_assembly_snowball_ready = yes
	OR = {
		NOT = { has_technology = tech_robotic_workers }
		NOT = { has_technology = tech_cloning }
		NOT = { has_technology = tech_robot_assembly_complex }
	}
}

staid_phase_science_nexus_rush = {
	NOT = { has_technology = tech_science_nexus }
	staid_science_nexus_research_priority_ready = yes
}

staid_phase_planetary_computer_research = {
	NOT = { has_technology = giga_tech_planetary_computer }
	staid_planetary_computer_research_priority_ready = yes
}

staid_phase_ring_world_growth = {
	NOT = { has_technology = tech_ring_world }
	staid_ring_world_research_priority_ready = yes
}

staid_phase_storage_cap_expansion = {
	NOT = { has_technology = giga_tech_kugelblitz }
	staid_storage_cap_research_priority_ready = yes
}

staid_phase_boxed_tall_habitat_escape = {
	staid_planetary_capacity_growth_ready = yes
	OR = {
		NOT = { has_technology = tech_habitat_1 }
		NOT = { has_technology = giga_tech_interstellar_habitat }
		NOT = { has_technology = giga_tech_stellar_ring_habitat }
	}
}

staid_phase_galactic_wonders_entry = {
	has_technology = tech_mega_engineering
	NOT = { has_ascension_perk = ap_galactic_wonders }
	OR = {
		staid_unity_sink_priority_ready = yes
		staid_surplus_sink_pressure = yes
		years_passed > 79
	}
}

staid_phase_gigastructural_constructs_rush = {
	has_ascension_perk = ap_galactic_wonders
	NOT = { has_ascension_perk = ap_gigastructural_constructs }
	OR = {
		staid_core_unlock_research_priority_ready = yes
		staid_unity_sink_priority_ready = yes
		years_passed > 79
	}
}

staid_phase_planetcraft_rush = {
	has_ascension_perk = ap_gigastructural_constructs
	NOT = { has_technology = giga_tech_planet_assembly }
	staid_planetcraft_research_priority_ready = yes
}

staid_phase_systemcraft_escalation = {
	has_ascension_perk = ap_celestial_printing
	NOT = { has_technology = giga_tech_war_system_1 }
	staid_systemcraft_research_priority_ready = yes
}

staid_phase_fleet_conversion_repeatables = {
	OR = {
		has_technology = tech_Carrier_1
		has_technology = tech_Dreadnought_1
		has_technology = tech_Flagship_1
		has_technology = giga_tech_war_moon_2
		has_technology = giga_tech_war_system_1
		has_technology = esc_tech_dark_matter_power_core_2
	}
}

staid_shipyard_expansion_ready = {
	has_technology = tech_mega_shipyard
	NOT = { staid_catastrophic_collapse_mode = yes }
	used_naval_capacity_percent < 1.85
	OR = {
		has_monthly_income = { resource = alloys value > 80 }
		resource_stockpile_compare = { resource = alloys value > 5000 }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		staid_surplus_sink_pressure = yes
		AND = { is_at_war = yes highest_threat > 35 used_naval_capacity_percent > 0.80 }
	}
}

staid_fleet_payoff_exploitation_ready = {
	NOT = { staid_catastrophic_collapse_mode = yes }
	used_naval_capacity_percent < 1.85
	OR = {
		AND = { is_at_war = yes highest_threat > 35 }
		AND = { used_naval_capacity_percent < 1.25 has_monthly_income = { resource = alloys value > 80 } }
		AND = { resource_stockpile_compare = { resource = alloys value > 12000 } resource_stockpile_compare = { resource = energy value > 5000 } }
	}
}

staid_advanced_component_resource_support_ready = {
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		has_monthly_income = { resource = volatile_motes value > 5 }
		has_monthly_income = { resource = exotic_gases value > 5 }
		has_monthly_income = { resource = rare_crystals value > 5 }
		has_monthly_income = { resource = sr_dark_matter value > 1 }
		has_monthly_income = { resource = sr_zro value > 1 }
		has_monthly_income = { resource = nanites value > 1 }
		has_monthly_income = { resource = giga_sr_sentient_metal value > 1 }
		has_monthly_income = { resource = giga_sr_negative_mass value > 1 }
		has_monthly_income = { resource = giga_sr_amb_megaconstruction value > 1 }
		staid_resource_waste_pressure = yes
	}
}

staid_nsc3_capital_hull_unlock_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_phase_fleet_conversion_repeatables = yes
		AND = {
			years_passed > 79
			OR = {
				resource_stockpile_compare = { resource = alloys value > 5000 }
				has_monthly_income = { resource = alloys value > 80 }
			}
		}
	}
}

staid_esc_component_unlock_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	staid_advanced_component_resource_support_ready = yes
	OR = {
		staid_phase_fleet_conversion_repeatables = yes
		AND = {
			years_passed > 79
			OR = {
				resource_stockpile_compare = { resource = alloys value > 5000 }
				has_monthly_income = { resource = engineering_research value > 600 }
			}
		}
	}
}

staid_modded_fleet_conversion_ready = {
	NOT = { staid_catastrophic_collapse_mode = yes }
	staid_advanced_component_resource_support_ready = yes
	OR = {
		has_technology = tech_Carrier_1
		has_technology = tech_Dreadnought_1
		has_technology = tech_Flagship_1
		has_technology = giga_tech_war_moon_2
		has_technology = giga_tech_war_system_1
		has_technology = esc_tech_dark_matter_power_core_2
	}
}

staid_planetary_capacity_growth_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_basic_economy_runway_safe = yes
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		has_monthly_income = { resource = minerals value > 40 }
		resource_stockpile_compare = { resource = minerals value > 2500 }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		has_monthly_income = { resource = energy value > 40 }
		resource_stockpile_compare = { resource = energy value > 2500 }
		staid_high_scale_snowball_pressure = yes
	}
}

staid_planetary_diversity_outpost_investment_ready = {
	is_nomadic = no
	NOT = { staid_survival_mode = yes }
	NOT = { staid_core_deficit_short_runway = yes }
	NOT = { has_deficit = minerals }
	NOT = { has_deficit = energy }
	has_monthly_income = { resource = minerals value > 20 }
	has_monthly_income = { resource = energy value > 20 }
	resource_stockpile_compare = { resource = minerals value > 1200 }
	resource_stockpile_compare = { resource = energy value > 1000 }
}

staid_pd_research_outpost_priority_ready = {
	staid_planetary_diversity_outpost_investment_ready = yes
	OR = {
		staid_research_under_curve = yes
		staid_research_input_runway_safe = yes
	}
}

staid_economy_megastructure_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	OR = {
		years_passed > 79
		staid_resource_waste_pressure = yes
		staid_research_under_curve = yes
	}
}

staid_mega_shipyard_build_priority_ready = {
	staid_shipyard_expansion_ready = yes
	has_technology = tech_mega_shipyard
}

staid_planetcraft_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	has_technology = tech_mega_engineering
	OR = {
		years_passed > 79
		staid_research_under_curve = yes
		staid_surplus_sink_pressure = yes
	}
}

staid_planetcraft_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	has_technology = giga_tech_planet_assembly
	has_monthly_income = { resource = alloys value > 300 }
	resource_stockpile_compare = { resource = alloys value > 25000 }
}

staid_war_moon_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	has_technology = tech_mega_engineering
	OR = {
		years_passed > 79
		has_technology = giga_tech_planet_assembly
		staid_fleet_buildup_economy_safe = yes
	}
}

staid_war_moon_build_priority_ready = {
	staid_fleet_buildup_economy_safe = yes
	has_technology = giga_tech_war_moon_2
	has_monthly_income = { resource = alloys value > 350 }
	resource_stockpile_compare = { resource = alloys value > 30000 }
}

staid_systemcraft_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		years_passed > 119
		has_technology = giga_tech_war_moon_2
		staid_surplus_sink_pressure = yes
	}
}

staid_systemcraft_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	has_ascension_perk = ap_celestial_printing
	has_technology = giga_tech_war_system_1
	has_monthly_income = { resource = alloys value > 500 }
	resource_stockpile_compare = { resource = alloys value > 50000 }
}

staid_gigas_special_resource_unlock_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		years_passed > 79
		staid_planetcraft_research_priority_ready = yes
		staid_systemcraft_research_priority_ready = yes
	}
}

staid_defensive_starbase_strategy = {
	is_nomadic = no
	OR = {
		has_ethic = ethic_pacifist
		has_ethic = ethic_fanatic_pacifist
		has_ethic = ethic_militarist
		has_ethic = ethic_fanatic_militarist
		has_ethic = ethic_xenophobe
		has_ethic = ethic_fanatic_xenophobe
		has_valid_civic = civic_barbaric_despoilers
	}
}

staid_crisis_starbase_pressure = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	highest_threat > 50
	has_monthly_income = { resource = alloys value > 80 }
	has_monthly_income = { resource = energy value > 60 }
	resource_stockpile_compare = { resource = alloys value > 5000 }
}

staid_aggressive_fleet_pressure = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		has_ethic = ethic_militarist
		has_ethic = ethic_fanatic_militarist
		has_ethic = ethic_xenophobe
		has_ethic = ethic_fanatic_xenophobe
		has_valid_civic = civic_barbaric_despoilers
		AND = {
			NOT = { has_ethic = ethic_pacifist }
			NOT = { has_ethic = ethic_fanatic_pacifist }
			used_naval_capacity_percent < 1.10
		}
	}
	used_naval_capacity_percent < 1.90
}

staid_militarist_conquest_strategy = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		has_ethic = ethic_militarist
		has_ethic = ethic_fanatic_militarist
		has_valid_civic = civic_barbaric_despoilers
		has_ethic = ethic_xenophobe
		has_ethic = ethic_fanatic_xenophobe
		AND = {
			NOT = { has_ethic = ethic_pacifist }
			NOT = { has_ethic = ethic_fanatic_pacifist }
			years_passed > 9
			used_naval_capacity_percent < 1.15
		}
	}
	used_naval_capacity_percent < 1.95
}

staid_raiding_pop_growth_strategy = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		has_ascension_perk = ap_nihilistic_acquisition
		has_valid_civic = civic_barbaric_despoilers
		has_origin = origin_slavers
		has_origin = origin_khan_successor
	}
	used_naval_capacity_percent < 2.00
}

staid_raiding_pop_acquisition_priority = {
	OR = {
		staid_raiding_pop_growth_strategy = yes
		AND = {
			staid_opening_military_to_pops = yes
			years_passed < 75
		}
	}
}

staid_hostile_fauna_clearance_strategy = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	used_naval_capacity_percent < 1.50
	OR = {
		staid_opening_hostile_fauna_clearance = yes
		AND = {
			years_passed < 60
			has_monthly_income = { resource = alloys value > 45 }
		}
	}
}

staid_site_limited_expansion_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	staid_fleet_buildup_economy_safe = yes
	OR = {
		staid_planetary_capacity_growth_ready = yes
		staid_resource_waste_pressure = yes
		staid_research_under_curve = yes
		years_passed > 79
	}
}

staid_apex_site_preservation_ready = {
	is_nomadic = no
	staid_megastructure_commit_safe = yes
	OR = {
		has_technology = giga_tech_matrioshka_brain_1
		has_technology = giga_tech_neutronium_gigaforge
		has_technology = giga_tech_nidavellir
		years_passed > 119
	}
}

staid_starbase_defense_economy_safe = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		has_monthly_income = { resource = alloys value > 35 }
		resource_stockpile_compare = { resource = alloys value > 1200 }
		staid_high_scale_snowball_pressure = yes
	}
	OR = {
		has_monthly_income = { resource = energy value > 35 }
		resource_stockpile_compare = { resource = energy value > 1200 }
		staid_high_scale_snowball_pressure = yes
	}
}

staid_static_defense_investment_ready = {
	staid_starbase_defense_economy_safe = yes
	OR = {
		staid_defensive_starbase_strategy = yes
		staid_aggressive_fleet_pressure = yes
		staid_militarist_conquest_strategy = yes
		staid_high_scale_snowball_pressure = yes
		staid_crisis_starbase_pressure = yes
	}
}

staid_unity_sink_priority_ready = {
	staid_surplus_sink_pressure = yes
}

staid_homeland_under_attack = {
	is_at_war = yes
	OR = {
		any_owned_planet = { is_occupied_flag = yes }
		any_owned_planet = { has_orbital_bombardment = yes }
		AND = { highest_threat > 35 used_naval_capacity_percent < 0.85 }
	}
}
```

## mods/StellarAIDirector/common/scripted_triggers/zzz_staid_threat_response_triggers.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Source of truth: tools/stellar_ai_director_lib.py threat-response tables.

staid_tr_is_conquest_war_goal = {
	from = { using_war_goal = { type = wg_conquest owner = root } }
}

staid_tr_is_subjugation_war_goal = {
	from = { using_war_goal = { type = wg_subjugation owner = root } }
}

staid_tr_is_humiliation_war_goal = {
	from = { using_war_goal = { type = wg_humiliation owner = root } }
}
staid_tr_war_goal_classified = {
	OR = {
		staid_tr_is_conquest_war_goal = yes
		staid_tr_is_subjugation_war_goal = yes
		staid_tr_is_humiliation_war_goal = yes
	}
}

staid_tr_attacker_war_leader = {
	from = {
		any_attacker = {
			is_same_value = root
			is_war_leader = yes
		}
	}
}

staid_tr_observer_eligible = {
	is_country_type = default
	NOT = { is_same_value = from }
	from = { NOT = { is_war_participant = root } }
	fromfrom = { NOT = { is_war_participant = root } }
}

staid_tr_awareness_known = {
	has_communications = from
}

staid_tr_foreign_affairs_safe = {
	NOT = { staid_core_deficit_short_runway = yes }
	NOT = { staid_survival_mode = yes }
	NOT = { staid_recovery_mode = yes }
	is_at_war = no
	has_monthly_income = { resource = alloys value > 120 }
	has_monthly_income = { resource = energy value > 100 }
	resource_stockpile_compare = { resource = alloys value > 8000 }
	resource_stockpile_compare = { resource = energy value > 5000 }
}

staid_tr_anti_aggressor_low = { check_variable_arithmetic = { which = staid_tr_score value >= 25 } }
staid_tr_anti_aggressor_medium = { check_variable_arithmetic = { which = staid_tr_score value >= 45 } }
staid_tr_anti_aggressor_high = { check_variable_arithmetic = { which = staid_tr_score value >= 65 } }
staid_tr_anti_aggressor_severe = { check_variable_arithmetic = { which = staid_tr_score value >= 85 } }
staid_tr_alignment_low = { check_variable_arithmetic = { which = staid_tr_alignment value >= 20 } }
staid_tr_alignment_medium = { check_variable_arithmetic = { which = staid_tr_alignment value >= 35 } }
staid_tr_alignment_high = { check_variable_arithmetic = { which = staid_tr_alignment value >= 50 } }
staid_tr_defensive_readiness_low = { check_variable_arithmetic = { which = staid_tr_readiness value >= 25 } }
staid_tr_defensive_readiness_high = { check_variable_arithmetic = { which = staid_tr_readiness value >= 40 } }

staid_tr_can_apply_readiness = {
	staid_tr_foreign_affairs_safe = yes
	OR = {
		staid_tr_defensive_readiness_low = yes
		staid_tr_defensive_readiness_high = yes
	}
}
```

## mods/StellarAIDirector/common/scripted_triggers/zzzz_staid_10_opening_strategy_triggers.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Computed opening classifier for the first 75-year strategy kernel.

staid_opening_direct_research = {
	staid_is_opening_phase = yes
	staid_can_afford_research_push = yes
	OR = {
		has_ethic = ethic_materialist
		has_ethic = ethic_fanatic_materialist
		has_authority = auth_machine_intelligence
		has_civic = civic_technocracy
	}
}

staid_opening_unity_to_research = {
	staid_is_opening_phase = yes
	staid_has_safe_basic_stockpiles = yes
	OR = {
		has_ethic = ethic_spiritualist
		has_ethic = ethic_fanatic_spiritualist
		has_civic = civic_exalted_priesthood
		has_civic = civic_death_cult
	}
}

staid_opening_military_to_pops = {
	staid_is_opening_phase = yes
	staid_has_safe_basic_stockpiles = yes
	NOT = { has_deficit = alloys }
	OR = {
		has_ethic = ethic_militarist
		has_ethic = ethic_fanatic_militarist
		has_ethic = ethic_authoritarian
		has_ethic = ethic_fanatic_authoritarian
	}
}

staid_opening_hostile_fauna_clearance = {
	staid_is_opening_phase = yes
	staid_has_safe_basic_stockpiles = yes
	NOT = { has_deficit = alloys }
	OR = {
		has_ethic = ethic_militarist
		has_ethic = ethic_fanatic_militarist
		has_ethic = ethic_xenophobe
		has_ethic = ethic_fanatic_xenophobe
		has_authority = auth_machine_intelligence
	}
}

staid_opening_defensive_tall_research = {
	staid_is_opening_phase = yes
	staid_can_afford_research_push = yes
	OR = {
		has_ethic = ethic_pacifist
		has_ethic = ethic_fanatic_pacifist
		has_ethic = ethic_xenophobe
		has_ethic = ethic_fanatic_xenophobe
	}
}

staid_opening_trade_to_research = {
	staid_is_opening_phase = yes
	staid_has_safe_basic_stockpiles = yes
	OR = {
		has_ethic = ethic_xenophile
		has_ethic = ethic_fanatic_xenophile
		has_civic = civic_merchant_guilds
		has_civic = civic_corporate_dominion
	}
}

staid_opening_hive_growth_research = {
	staid_is_opening_phase = yes
	staid_has_safe_basic_stockpiles = yes
	has_authority = auth_hive_mind
}

staid_opening_machine_growth_research = {
	staid_is_opening_phase = yes
	staid_has_safe_basic_stockpiles = yes
	has_authority = auth_machine_intelligence
}

staid_opening_nomad_arkship_research = {
	staid_is_opening_phase = yes
	is_nomadic = yes
	staid_has_safe_basic_stockpiles = yes
}

staid_opening_any_research_route = {
	OR = {
		staid_opening_direct_research = yes
		staid_opening_unity_to_research = yes
		staid_opening_defensive_tall_research = yes
		staid_opening_trade_to_research = yes
		staid_opening_hive_growth_research = yes
		staid_opening_machine_growth_research = yes
		staid_opening_nomad_arkship_research = yes
	}
}
```

## mods/StellarAIDirector/common/scripted_triggers/zzzz_staid_11_fleet_doctrine_triggers.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Fleet doctrine classifiers for tech and spend weights. These do not force ship designs.

staid_fleet_energy_shield_doctrine = {
	staid_fleet_defensive_minimum_mode = yes
	OR = {
		has_ethic = ethic_materialist
		has_ethic = ethic_fanatic_materialist
		has_technology = tech_lasers_2
		has_technology = tech_shields_2
	}
}

staid_fleet_kinetic_armor_doctrine = {
	staid_fleet_defensive_minimum_mode = yes
	OR = {
		has_ethic = ethic_militarist
		has_ethic = ethic_fanatic_militarist
		has_technology = tech_mass_drivers_2
		has_technology = tech_ship_armor_2
	}
}

staid_fleet_missile_evasion_doctrine = {
	staid_fleet_strategic_aggression_mode = yes
	OR = {
		has_technology = tech_missiles_2
		has_technology = tech_afterburners_1
		has_technology = tech_thrusters_2
	}
}

staid_fleet_carrier_strikecraft_doctrine = {
	OR = {
		staid_fleet_strategic_aggression_mode = yes
		staid_is_midgame_scaling_phase = yes
	}
	OR = {
		has_technology = tech_space_whale_weapon_1
		has_technology = tech_strike_craft_1
		has_technology = tech_starbase_3
	}
}

staid_fleet_balanced_filler_doctrine = {
	NOT = { staid_fleet_energy_shield_doctrine = yes }
	NOT = { staid_fleet_kinetic_armor_doctrine = yes }
	NOT = { staid_fleet_missile_evasion_doctrine = yes }
	NOT = { staid_fleet_carrier_strikecraft_doctrine = yes }
}
```

## mods/StellarAIDirector/common/scripted_triggers/zzzz_staid_12_planetary_diversity_value_triggers.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Planet-scope Planetary Diversity value classifiers.
# These triggers let the Director route planet roles/buildings from actual PD modifiers and deposits.

staid_pd_planet_research_value = {
	OR = {
		has_deposit = d_cd_ancient_tunnels
		has_deposit = d_hab_dark_matter_1
		has_deposit = d_hab_dark_matter_10
		has_deposit = d_hab_dark_matter_2
		has_deposit = d_hab_dark_matter_3
		has_deposit = d_hab_harvester_nanites_1
		has_deposit = d_hab_harvester_nanites_2
		has_deposit = d_hab_harvester_nanites_3
		has_deposit = d_hab_nanites_3
		has_deposit = d_hab_zro_1
		has_deposit = d_hab_zro_2
		has_deposit = d_hab_zro_3
		has_deposit = d_hab_zro_4
		has_deposit = d_hab_zro_5
		has_deposit = d_pd_solar_system_network_hub
		has_deposit = d_pd_tree_of_life_colony
		has_deposit = d_pd_tree_of_life_home
		has_deposit = d_pd_tree_of_life_uncommon
		has_deposit = d_raging_lavafalls
		has_deposit = d_red_giant_dm
		has_deposit = d_red_giant_unstable
		has_deposit = d_rugged_landscape
		has_deposit = d_stasis_pods
		has_modifier = engineered_environment_gaia
		has_modifier = living_sea
		has_modifier = pd_alpha_centauri
		has_modifier = pd_cloudless_gas_giant
		has_modifier = pd_cold_gas_giant
		has_modifier = pd_domed_base_research
		has_modifier = pd_domed_research_site_1
		has_modifier = pd_domed_research_site_2
		has_modifier = pd_domed_research_site_3
		has_modifier = pd_dwarf_gas
		has_modifier = pd_hothouse
		has_modifier = pd_subglacial
	}
}

staid_pd_planet_minerals_value = {
	OR = {
		has_deposit = d_ash_storms
		has_deposit = d_betharian_deposit
		has_deposit = d_bubbling_swamp
		has_deposit = d_cd_ancient_tunnels
		has_deposit = d_crystal_forest
		has_deposit = d_crystal_reef
		has_deposit = d_crystalline_caverns
		has_deposit = d_dust_caverns
		has_deposit = d_dust_desert
		has_deposit = d_fertile_lands
		has_deposit = d_fuming_bog
		has_deposit = d_galvanic_living_metal
		has_deposit = d_geothermal_vent
		has_deposit = d_great_river
		has_deposit = d_hab_alloy_1
		has_deposit = d_hab_alloy_10
		has_deposit = d_hab_alloy_2
		has_deposit = d_hab_alloy_25
		has_deposit = d_hab_alloy_3
		has_deposit = d_hab_alloy_4
		has_deposit = d_hab_alloy_5
		has_deposit = d_hab_consumer_goods_2
		has_deposit = d_hab_crystal_1
		has_deposit = d_hab_crystal_2
		has_deposit = d_hab_crystal_3
		has_deposit = d_hab_crystal_4
		has_deposit = d_hab_crystal_5
		has_deposit = d_hab_dark_matter_1
		has_deposit = d_hab_dark_matter_10
		has_deposit = d_hab_dark_matter_2
		has_deposit = d_hab_dark_matter_3
		has_deposit = d_hab_gas_1
		has_deposit = d_hab_gas_2
		has_deposit = d_hab_gas_3
		has_deposit = d_hab_gas_4
		has_deposit = d_hab_gas_5
		has_deposit = d_hab_living_metal_1
		has_deposit = d_hab_mote_1
		has_deposit = d_hab_mote_2
		has_deposit = d_hab_mote_3
		has_deposit = d_hab_mote_4
		has_deposit = d_hab_mote_5
		has_deposit = d_hab_zro_1
		has_deposit = d_hab_zro_2
		has_deposit = d_hab_zro_3
		has_deposit = d_hab_zro_4
		has_deposit = d_hab_zro_5
		has_deposit = d_lava_flooding
		has_deposit = d_lush_jungle
		has_deposit = d_mineral_fields
		has_deposit = d_mineral_striations
		has_deposit = d_ore_rich_caverns
		has_deposit = d_pd_ammonia_brine_caverns
		has_deposit = d_pd_ammonia_cryolite_reefs
		has_deposit = d_pd_ammonia_salt_dunes
		has_deposit = d_pd_solar_system_network_hub
		has_deposit = d_phab_mining_1
		has_deposit = d_phab_mining_2
		has_deposit = d_phab_mining_3
		has_deposit = d_prosperous_mesa
		has_deposit = d_red_giant_dm
		has_deposit = d_red_giant_unstable
		has_deposit = d_rich_mountain
		has_deposit = d_rugged_landscape
		has_deposit = d_submerged_ore_veins
		has_deposit = d_tempestous_mountain
		has_deposit = d_toxic_atmosphere
		has_deposit = d_underwater_vent
		has_deposit = d_veiny_cliffs
		has_deposit = d_volcanic_fumarole
		has_deposit = d_volcanic_lava_river
		has_deposit = d_volcanic_mineral_fields
		has_deposit = d_volcanic_mineral_hills
		has_deposit = d_volcanic_mineral_layers
		has_deposit = d_volcanic_ore_caverns
		has_deposit = d_volcanic_ore_veins
		has_deposit = d_volcanic_rich_mountain
		has_deposit = d_volcanic_stifling_atmosphere
		has_deposit = d_volcanic_sulfur_lava
		has_deposit = d_volcanic_weak_crust
		has_modifier = pd_carbon
		has_modifier = pd_cold_cave
		has_modifier = pd_coral
		has_modifier = pd_domed_base_mining
		has_modifier = pd_domed_mining_site_1
		has_modifier = pd_domed_mining_site_2
		has_modifier = pd_domed_mining_site_3
		has_modifier = pd_dry_cave
		has_modifier = pd_gaia_cave
		has_modifier = pd_glaciovolcanic
		has_modifier = pd_lanthanide
		has_modifier = pd_lichen
		has_modifier = pd_megaflora
		has_modifier = pd_nuked_cave
		has_modifier = pd_petrified
		has_modifier = pd_reef
		has_modifier = pd_salt
		has_modifier = pd_sinkhole
		has_modifier = pd_wet_cave
	}
}

staid_pd_planet_energy_value = {
	OR = {
		has_deposit = d_arid_highlands
		has_deposit = d_ash_storms
		has_deposit = d_buzzing_plains
		has_deposit = d_charged_atmosphere
		has_deposit = d_dust_caverns
		has_deposit = d_dust_desert
		has_deposit = d_frozen_gas_lake
		has_deposit = d_geothermal_vent
		has_deposit = d_hot_springs
		has_deposit = d_pd_ammonia_lightning_storms
		has_deposit = d_pd_ammonia_polar_ion_columns
		has_deposit = d_pd_ammonia_thermocline
		has_deposit = d_pd_solar_system_network_hub
		has_deposit = d_phab_energy_1
		has_deposit = d_phab_energy_2
		has_deposit = d_phab_energy_3
		has_deposit = d_raging_lavafalls
		has_deposit = d_red_giant_dm
		has_deposit = d_red_giant_unstable
		has_deposit = d_rugged_landscape
		has_deposit = d_rushing_waterfalls
		has_deposit = d_searing_desert
		has_deposit = d_seismic_bombing_crater
		has_deposit = d_stasis_pods
		has_deposit = d_tempestous_mountain
		has_deposit = d_underwater_vent
		has_modifier = pd_cold_tidally_locked
		has_modifier = pd_cryoflora
		has_modifier = pd_domed_base_energy
		has_modifier = pd_domed_energy_site_1
		has_modifier = pd_domed_energy_site_2
		has_modifier = pd_domed_energy_site_3
		has_modifier = pd_dry_tidally_locked
		has_modifier = pd_gaia_tidally_locked
		has_modifier = pd_geothermal
		has_modifier = pd_glaciovolcanic
		has_modifier = pd_hydrocarbon
		has_modifier = pd_megaflora
		has_modifier = pd_nuked_tidally_locked
		has_modifier = pd_primal
		has_modifier = pd_storm
		has_modifier = pd_wet_tidally_locked
	}
}

staid_pd_planet_food_value = {
	OR = {
		has_deposit = d_andisol_soil
		has_deposit = d_black_soil
		has_deposit = d_boggy_fens
		has_deposit = d_bountiful_plains
		has_deposit = d_bubbling_swamp
		has_deposit = d_fertile_lands
		has_deposit = d_forgiving_tundra
		has_deposit = d_fuming_bog
		has_deposit = d_fungal_caves
		has_deposit = d_fungal_forest
		has_deposit = d_great_river
		has_deposit = d_green_hills
		has_deposit = d_lichen_fields
		has_deposit = d_lush_jungle
		has_deposit = d_marvelous_oasis
		has_deposit = d_natural_farmland
		has_deposit = d_nutritious_mudland
		has_deposit = d_pd_ammonia_ammoniated_kelp_forests
		has_deposit = d_pd_ammonia_chemosynthetic_pools
		has_deposit = d_pd_ammonia_organic_haze
		has_deposit = d_pd_solar_system_network_hub
		has_deposit = d_pd_tree_of_life_bloomed
		has_deposit = d_pd_tree_of_life_colony
		has_deposit = d_pd_tree_of_life_home
		has_deposit = d_pd_tree_of_life_uncommon
		has_deposit = d_phab_food_1
		has_deposit = d_phab_food_2
		has_deposit = d_phab_food_3
		has_deposit = d_rugged_woods
		has_deposit = d_teeming_reef
		has_deposit = d_tropical_island
		has_modifier = pd_aquifer
		has_modifier = pd_archipelago
		has_modifier = pd_biolumen
		has_modifier = pd_cold_superhabitable
		has_modifier = pd_domed_base_food
		has_modifier = pd_domed_food_site_1
		has_modifier = pd_domed_food_site_2
		has_modifier = pd_domed_food_site_3
		has_modifier = pd_dry_superhabitable
		has_modifier = pd_gaia_superhabitable
		has_modifier = pd_iceberg
		has_modifier = pd_lichen
		has_modifier = pd_nuked_superhabitable
		has_modifier = pd_salt
		has_modifier = pd_storm
		has_modifier = pd_subglacial
		has_modifier = pd_supercontinent
		has_modifier = pd_wet_superhabitable
	}
}

staid_pd_planet_alloys_value = {
	OR = {
		has_deposit = d_cd_ancient_tunnels
		has_deposit = d_hab_alloy_1
		has_deposit = d_hab_alloy_10
		has_deposit = d_hab_alloy_2
		has_deposit = d_hab_alloy_25
		has_deposit = d_hab_alloy_3
		has_deposit = d_hab_alloy_4
		has_deposit = d_hab_alloy_5
		has_deposit = d_pd_solar_system_network_hub
		has_modifier = pd_chthonian
		has_modifier = pd_iron
		has_modifier = pd_moon_base_foundry
		has_modifier = pd_volcano
	}
}

staid_pd_planet_consumer_goods_value = {
	OR = {
		has_deposit = d_hab_consumer_goods_2
		has_deposit = d_pd_solar_system_network_hub
		has_modifier = pd_moon_base_factory
	}
}

staid_pd_planet_trade_value = {
	OR = {
		has_deposit = d_pd_solar_system_network_hub
		has_modifier = pd_moon_base_trade
	}
}

staid_pd_planet_unity_value = {
	OR = {
		has_deposit = d_alien_pets_deposit
		has_deposit = d_cd_ancient_tunnels
		has_deposit = d_large_volcano
		has_deposit = d_pd_solar_system_network_hub
		has_deposit = d_seismic_bombing_crater
		has_modifier = pd_moon_base_priest
	}
}

staid_pd_planet_growth_value = {
	OR = {
		has_deposit = d_ash_storms
		has_deposit = d_charged_atmosphere
		has_deposit = d_large_volcano
		has_deposit = d_lava_flooding
		has_deposit = d_pd_solar_system_network_hub
		has_deposit = d_pd_tree_of_life_bloomed
		has_deposit = d_pd_tree_of_life_colony
		has_deposit = d_pd_tree_of_life_home
		has_deposit = d_pd_tree_of_life_uncommon
		has_deposit = d_toxic_atmosphere
		has_modifier = pd_aquifer
		has_modifier = pd_biolumen
		has_modifier = pd_coral
		has_modifier = pd_geothermal
		has_modifier = pd_glaciovolcanic
		has_modifier = pd_iceberg
		has_modifier = pd_petrified
		has_modifier = pd_reef
		has_modifier = pd_sinkhole
		has_modifier = pd_storm
		has_modifier = pd_supercontinent
	}
}

staid_pd_planet_defense_value = {
	OR = {
		has_deposit = d_seismic_bombing_crater
		has_modifier = pd_arcology_cave
		has_modifier = pd_cold_cave
		has_modifier = pd_domed_colony
		has_modifier = pd_dry_cave
		has_modifier = pd_gaia_cave
		has_modifier = pd_hive_cave
		has_modifier = pd_machine_cave
		has_modifier = pd_no_lifetree
		has_modifier = pd_nuked_cave
		has_modifier = pd_tree_of_life_bloomed
		has_modifier = pd_tree_of_life_home
		has_modifier = pd_wet_cave
	}
}
```

## mods/StellarAIDirector/common/scripted_triggers/zzzz_staid_20_strategy_kernel_triggers.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Computed strategic state shared by economy, policy, edict, technology, and fleet weights.

staid_is_opening_phase = {
	years_passed < 75
}

staid_is_midgame_scaling_phase = {
	years_passed > 44
	years_passed < 120
}

staid_is_crisis_scaling_phase = {
	years_passed > 119
}

staid_has_safe_basic_stockpiles = {
	NOT = { has_deficit = energy }
	NOT = { has_deficit = minerals }
	NOT = { has_deficit = food }
	NOT = { has_deficit = consumer_goods }
	resource_stockpile_percent = { resource = energy value > 0.10 }
	resource_stockpile_percent = { resource = minerals value > 0.10 }
}

staid_can_afford_research_push = {
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_has_safe_basic_stockpiles = yes
		staid_high_scale_snowball_pressure = yes
		staid_construction_spenddown_pressure = yes
	}
	OR = {
		staid_research_input_runway_safe = yes
		staid_high_scale_snowball_pressure = yes
		staid_construction_spenddown_pressure = yes
	}
}

staid_security_threatened = {
	OR = {
		has_country_flag = staid_tr_defensive_readiness_low
		staid_crisis_starbase_pressure = yes
	}
}

staid_security_existential = {
	OR = {
		staid_crisis_starbase_pressure = yes
		AND = {
			staid_security_threatened = yes
			NOT = { staid_shipyard_payoff_ready = yes }
		}
	}
}

staid_megastructure_prereq_release = {
	staid_megastructure_prep_ready = yes
	staid_can_afford_research_push = yes
}

staid_megastructure_alloy_release = {
	staid_megastructure_commit_safe = yes
	NOT = { staid_security_existential = yes }
}

staid_fleet_defensive_minimum_mode = {
	OR = {
		staid_security_threatened = yes
		staid_shipyard_expansion_ready = yes
	}
}

staid_fleet_strategic_aggression_mode = {
	OR = {
		staid_fleet_payoff_exploitation_ready = yes
		AND = {
			used_naval_capacity_percent < 1.40
			has_monthly_income = { resource = alloys value > 80 }
		}
		staid_hostile_fauna_clearance_strategy = yes
	}
	NOT = { staid_security_existential = yes }
}

staid_fleet_survival_emergency_mode = {
	staid_security_existential = yes
}

staid_opening_route_research_priority = {
	OR = {
		staid_opening_any_research_route = yes
		staid_research_under_curve = yes
	}
}
```

## mods/StellarAIDirector/common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/starbase_buildings


# policy_route = fallen_empire_benchmark_route; source = common/starbase_buildings/esc_starbase_buildings.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
esc_starbase_reactor = {
	icon = "GFX_esc_starbase_reactor"
	construction_days = 360

	potential = {
		exists = owner
		owner = { has_technology = esc_tech_orbital_powerplant }
	}

	possible = {
		custom_tooltip = {
			fail_text = "requires_starfortress"
			has_starbase_size >= starbase_starfortress
		}
	}

	resources = {
		category = starbase_buildings
		cost = {
			alloys = 400
		}
		produces = {
			energy = 12
		}
	}

	show_in_tech = "esc_tech_orbital_powerplant"

	ai_build_at_chokepoint = yes
	ai_build_outside_chokepoint = yes

	ai_weight = {
		factor = 75000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_building:esc_starbase_reactor
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_buildings/nsc_starbase_buildings.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
adv_starbase_defenses = {
	icon = "GFX_starbase_adv_starbase"
	construction_days = 1000
	resources = {
		category = starbase_buildings
		cost = { alloys = 200 }
		upkeep = { energy = 2 }
	}

	station_modifier = {
		ship_armor_add = 3000
		ship_fire_rate_mult = 0.1
		ship_weapon_range_mult = 0.15
	}
	potential = {
		is_normal_starbase = yes
		is_orbital_ring = no
		has_starbase_size >= starbase_citadel
	}
	ai_build_at_chokepoint = no
	ai_build_outside_chokepoint = yes
	show_in_tech = "tech_starbase_5"

	ai_weight = {
		factor = 110000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_building:adv_starbase_defenses
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_buildings/sbx_3_0_buildings.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
reinforced_defenses = {
	icon = "GFX_starbase_reinforced_defenses"
	construction_days = 400
	resources = {
		category = starbase_buildings
		cost = { alloys = 150 }
		upkeep = { energy = 1 }
	}
	station_modifier = {
		ship_shield_add = 6000
		ship_shield_mult = 0.1
		ship_shield_regen_add_perc = 1.0
		ship_armor_add = 10000
		ship_armor_mult = 0.1
		ship_armor_regen_add_perc = 1.0
	}
	potential = { has_starbase_size >= starbase_starport }#not for outposts
	ai_build_at_chokepoint = no
	ai_build_outside_chokepoint = yes

	show_tech_unlock_if = {
		is_nomadic = no
	}


	ai_weight = {
		factor = 105000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_building:reinforced_defenses
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_buildings/sbx_3_0_buildings.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
strategic_defenses = {
	icon = "GFX_starbase_strategic_defenses"
	construction_days = 650
	resources = {
		category = starbase_buildings
		cost = { alloys = 150 }
		upkeep = { energy = 1 }
	}
	station_modifier = {
		ship_shield_add = 6000
		ship_shield_mult = 0.1
		ship_shield_regen_add_perc = 1.0
		ship_fire_rate_mult = 0.25
	}
	potential = { has_starbase_size >= starbase_starfortress }
	ai_build_at_chokepoint = no
	ai_build_outside_chokepoint = yes
	show_in_tech = "tech_starbase_4"

	show_tech_unlock_if = {
		is_nomadic = no
	}


	ai_weight = {
		factor = 120000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_building:strategic_defenses
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}

```

## mods/StellarAIDirector/common/starbase_modules/zzzz_staid_05_starbase_defense_starbase_modules.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/starbase_modules


# policy_route = fallen_empire_benchmark_route; source = common/starbase_modules/sbx_3_0_starbase_modules.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
gun_battery = {
	section = "BATTERY_STARBASE_SECTION"
	icon = GFX_spaceport_modules
	construction_days = 180
	category = sm_defense_cat


	resources = {
		category = starbase_modules
		cost = {
			alloys = 50
		}

		upkeep = {
			energy = 1
		}
	}

	station_modifier = {
		ship_hull_mult = 0.10
		ship_armor_mult = 0.10
		starbase_defense_platform_capacity_add = 1
	}

	ai_build_at_chokepoint = yes
	ai_build_outside_chokepoint = no


	show_in_tech = "tech_mass_drivers_1"

	show_tech_unlock_if = {
		is_nomadic = no
	}


	potential = {
		is_normal_starbase = yes
		has_starbase_size >= starbase_starport
		count_starbase_modules = { type = gun_battery count < 10 }
	}

	ai_weight = {
		factor = 90000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_module:gun_battery
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_modules/sbx_3_0_starbase_modules.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
missile_battery = {
	section = "MISSILE_STARBASE_SECTION"
	icon = "GFX_starbase_missile_battery"
	construction_days = 180
	category = sm_defense_cat


	resources = {
		category = starbase_modules
		cost = {
			alloys = 50
		}

		upkeep = {
			energy = 1
		}
	}

	station_modifier = {
		ship_hull_mult = 0.10
		ship_armor_mult = 0.10
		starbase_defense_platform_capacity_add = 1
	}

	ai_build_at_chokepoint = yes
	ai_build_outside_chokepoint = no



	show_in_tech = "tech_torpedoes_1"

	show_tech_unlock_if = {
		is_nomadic = no
	}


	potential = {
		exists = owner
		owner = { has_technology = tech_torpedoes_1 }
		is_normal_starbase = yes
		has_starbase_size >= starbase_starport
		count_starbase_modules = { type = missile_battery count < 5 }
	}

	ai_weight = {
		factor = 90000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_module:missile_battery
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_modules/sbx_3_0_starbase_modules.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
hangar_bay = {
	section = "HANGAR_STARBASE_SECTION"
	icon = "GFX_starbase_hangar_bay"
	construction_days = 180
	category = sm_defense_cat


	resources = {
		category = starbase_modules
		cost = {
			alloys = 50
		}

		upkeep = {
			energy = 1
		}
	}

	station_modifier = {
		ship_hull_mult = 0.10
		ship_armor_mult = 0.10
		starbase_defense_platform_capacity_add = 1
	}

	ai_build_at_chokepoint = yes
	ai_build_outside_chokepoint = no



	show_in_tech = "tech_strike_craft_1"

	show_tech_unlock_if = {
		is_nomadic = no
	}


	potential = {
		exists = owner
		owner = { has_technology = tech_strike_craft_1 }
		is_normal_starbase = yes
		has_starbase_size >= starbase_starport
		count_starbase_modules = { type = hangar_bay count < 5 }
	}

	ai_weight = {
		factor = 95000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_module:hangar_bay
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_modules/sbx_3_0_starbase_modules.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
large_battery = {
	section = "LARGE_STARBASE_SECTION"
	icon = "GFX_starbase_large_battery"
	construction_days = 240
	category = sm_defense_cat

	resources =	{
		category = starbase_modules
		cost = { alloys = 125 }
		upkeep = { energy = 1 }
	}
	station_modifier = {
		ship_hull_mult = 0.03
		ship_armor_mult = 0.03
	}
	ai_build_at_chokepoint = yes
	ai_build_outside_chokepoint = no

	potential = {
		has_starbase_size >= starbase_starfortress
		count_starbase_modules = { type = large_battery count < 5 }
	}

	show_tech_unlock_if = {
		is_nomadic = no
	}


	ai_weight = {
		factor = 105000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_module:large_battery
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_modules/sbx_3_0_starbase_modules.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
armor_module = {
	section = "ANCHORAGE_STARBASE_SECTION"
	icon = "GFX_starbase_armor_module"
	construction_days = 180
	category = sm_defense_cat

	resources ={
		category = starbase_modules
		cost = { alloys = 75 }
	}
	station_modifier = {
		ship_armor_add = 8000
	}
	ai_build_at_chokepoint = yes
	ai_build_outside_chokepoint = yes
	potential = {
		count_starbase_modules = { type = armor_module count < 4 }
		has_starbase_size >= starbase_starport #not for outposts
	}

	ai_weight = {
		factor = 80000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_module:armor_module
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_modules/sbx_3_0_orbital_ring_modules.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
orbital_ring_gun_battery = {
	section = "ORBITAL_RING_BATTERY_STARBASE_SECTION"
	icon = GFX_spaceport_modules
	construction_days = 180
	starbase_type = orbital_ring
	category = sm_defense_cat


	resources = {
		category = starbase_modules
		cost = {
			alloys = 50
		}

		upkeep = {
			energy = 1
		}
	}

	station_modifier = {
		ship_hull_mult = 0.10
		ship_armor_mult = 0.10
		starbase_defense_platform_capacity_add = 1
	}

	ai_build_at_chokepoint = yes
	ai_build_outside_chokepoint = no


	show_in_tech = "tech_mass_drivers_1"

	potential = {
		is_normal_starbase = yes
		has_starbase_size >= orbital_ring_tier_1
		count_starbase_modules = { type = orbital_ring_gun_battery count < 10 }
	}

	ai_weight = {
		factor = 80000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_module:orbital_ring_gun_battery
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_modules/sbx_3_0_orbital_ring_modules.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
orbital_ring_missile_battery = {
	section = "ORBITAL_RING_MISSILE_SECTION"
	icon = "GFX_starbase_missile_battery"
	construction_days = 180
	starbase_type = orbital_ring
	category = sm_defense_cat


	resources = {
		category = starbase_modules
		cost = {
			alloys = 50
		}

		upkeep = {
			energy = 1
		}
	}

	station_modifier = {
		ship_hull_mult = 0.10
		ship_armor_mult = 0.10
		starbase_defense_platform_capacity_add = 1
	}

	ai_build_at_chokepoint = yes
	ai_build_outside_chokepoint = no



	show_in_tech = "tech_torpedoes_1"

	potential = {
		exists = owner
		owner = { has_technology = tech_torpedoes_1 }
		is_orbital_ring = yes
		has_starbase_size >= orbital_ring_tier_1
		has_starbase_size >= orbital_ring_tier_1
		count_starbase_modules = { type = orbital_ring_missile_battery count < 5 }
	}

	ai_weight = {
		factor = 80000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_module:orbital_ring_missile_battery
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_modules/sbx_3_0_orbital_ring_modules.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
orbital_ring_hangar_bay = {
	icon = "GFX_starbase_hangar_bay"
	section = "HANGAR_ORBITAL_RING_SECTION"
	construction_days = 180
	starbase_type = orbital_ring
	category = sm_defense_cat

	potential = {
		exists = owner
		is_orbital_ring = yes
		has_starbase_size >= orbital_ring_tier_1
		owner = { has_technology = tech_strike_craft_1 }
		count_starbase_modules = { type = orbital_ring_hangar_bay count < 5 }
	}


	resources = {
		category = starbase_modules
		cost = {
			alloys = 50
		}

		upkeep = {
			energy = 1
		}
	}

	station_modifier = {
		ship_hull_mult = 0.20
		ship_armor_mult = 0.20
		starbase_defense_platform_capacity_add = 2
	}

	triggered_station_modifier = {
		potential = {
			exists = planet
			planet = {
				exists = owner.overlord
				has_holding = {
					holding = holding_orbital_assembly_complex
					owner = owner.overlord
				}
			}
		}
	}


	ai_build_outside_chokepoint = yes

	show_in_tech = "tech_strike_craft_1"

	ai_weight = {
		factor = 85000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_module:orbital_ring_hangar_bay
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_modules/sbx_3_0_orbital_ring_modules.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
orbital_ring_large_gun_battery = {
	section = "LARGE_GUN_BATTERY_ORBITAL_RING_SECTION"
	icon = GFX_orbital_ring_large_battery
	construction_days = 180
	starbase_type = orbital_ring
	category = sm_defense_cat

	potential = {
		is_orbital_ring = yes
		has_starbase_size >= orbital_ring_tier_1
		count_starbase_modules = { type = orbital_ring_large_gun_battery count < 5 }
	}


	resources = {
		category = starbase_modules
		cost = {
			alloys = 50
		}

		upkeep = {
			energy = 1
		}
	}

	station_modifier = {
		ship_hull_mult = 0.30
		ship_armor_mult = 0.30
		starbase_defense_platform_capacity_add = 2
	}

	triggered_station_modifier = {
		potential = {
			exists = planet
			planet = {
				exists = owner.overlord
				has_holding = {
					holding = holding_orbital_assembly_complex
					owner = owner.overlord
				}
			}
		}
	}

	show_in_tech = "tech_mass_drivers_1"

	ai_weight = {
		factor = 90000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_module:orbital_ring_large_gun_battery
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/starbase_modules/sbx_3_0_orbital_ring_modules.txt; parent_ai = parent_ai_complete; source_ai_weight = yes
orbital_ring_armor_module = {
	section = "ARMOR_ORBITAL_RING_SECTION"
	icon = "GFX_starbase_armor_module"
	construction_days = 180
	starbase_type = orbital_ring
	category = sm_defense_cat

	resources ={
		category = starbase_modules
		cost = { alloys = 75 }
	}
	station_modifier = {
		ship_armor_add = 8000
	}
	ai_build_at_chokepoint = yes
	ai_build_outside_chokepoint = yes

	potential = {
		has_starbase_size >= orbital_ring_tier_1
		count_starbase_modules = { type = orbital_ring_armor_module count < 4 }
	}


	ai_weight = {
		factor = 75000

		# policy_route = fallen_empire_benchmark_route
		# source_object = starbase_module:orbital_ring_armor_module
		modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }
		modifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }
		modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }
		modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 2 owner = { years_passed > 44 } }
		modifier = { factor = 3 owner = { years_passed > 79 } }
		modifier = { factor = 5 owner = { years_passed > 119 } }
		modifier = { factor = 3 owner = { years_passed < 30 } }
		modifier = { factor = 2 owner = { AND = { years_passed > 29 years_passed < 60 } } }
		modifier = { factor = 2 owner = { AND = { years_passed > 59 years_passed < 100 } } }
	}
}

```

## mods/StellarAIDirector/common/technology/zzzz_staid_01_unlock_technology_technology.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/technology


# Source-local variables required by copied parent objects.
@ACOT_active_flag								= "acot_activated"
@ESC_AI_tech_weight_multiplier = 250
@ESC_TECH_Technology_Ascendancy_weight_modifier	= 1.5
@ESC_TECH_tier6_cost1 							= 64000
@ESC_TECH_tier6_weight1							= 14
@ai_ship_types_factor = 5 # bonus chance for ai to pick new ship techs
@best_megastructure_ai_tech_factor = 100 # Extra AI chance for picking certain Megastructure techs. Late game, so can afford very high weight - not picking Mega-Engineering first time is a bug!
@ehof_tier6cost1 = 64000
@ehof_tier7weight1 = 15
@federation_perk_factor = 2
@giga_50_000_cost = 50000
@giga_aiweight_multiplier_insane = 1000			#The Meta/Multi-stage
@giga_aiweight_multiplier_medium = 10			#Okay/basic resources
@giga_aiweight_multiplier_questionable = 0.1	#STOP RESEARCHING DUMB TECHS THAT DON'T EXIST ANYMORE!
@giga_aiweight_multiplier_strong = 100			#Strong
@giga_aiweight_multiplier_weak = 1				#Bad/requires advanced thought to use
@giga_amb_flag = giga_buildcap_j # menu option variable name, checked for feature activation
@giga_tech_weight_boost_large = 2		# vanilla uses 2x boost for maniacal/spark of genius, non galwonders structures when you get galwonders,
@giga_tech_weight_boost_massive = 6 	# vanilla uses 6x boost for master builders, directly related perks, like one vision for unity, enigmatic engineering for sentry array
@giga_tech_weight_malus_large = 0.5		# vanilla uses half to cut for example military tech weights for pacifists
@giga_tier6cost1 = 32000
@giga_tier6cost2 = 40000
@giga_tier6cost3 = 48000
@giga_tier6weight1 = 18
@giga_tier6weight2 = 16
@giga_tier6weight3 = 14
@giga_tier7cost1 = 64000
@giga_tier7cost2 = 80000
@giga_tier7cost3 = 96000
@giga_tier7weight1 = 12
@giga_tier8cost1 = 128000
@pop_growth_tech_ai_factor = 3 # Extra chance for AI to pick pop growth techs
@robots_ai_tech_factor = 2 	# Extra AI chance for robot-related techs.
@tier1cost3 = 1500
@tier1weight3 = 90
@tier2cost2 = 2500
@tier2cost3 = 3000
@tier2weight2 = 75
@tier2weight3 = 70
@tier3cost1 = 4000
@tier3cost2 = 5000
@tier3weight1 = 65
@tier3weight2 = 60
@tier4cost1 = 8000
@tier4cost2 = 10000
@tier4cost3 = 12000
@tier4cost4 = 28000
@tier4weight1 = 45
@tier4weight2 = 40
@tier4weight3 = 35
@tier5cost2 = 20000
@tier5cost3 = 24000
@tier5cost4 = 56000
@tier5weight2 = 25
@tier5weight3 = 20

# policy_route = mega_engineering_core; source = common/technology/00_megastructures.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_mega_engineering = {
	area = engineering
	cost = @tier5cost3
	tier = 5
	category = { voidcraft }
	ai_update_type = all
	prerequisites = {
		OR = {
			tech_starbase_5
			tech_arkship_tier_3
		}
		tech_zero_point_power
		OR = {
			tech_battleships
			tech_stingers
		}
	}
	weight = @tier5weight3
	is_rare = yes

	feature_flags = {
		megaengineering
	}

	modifier = {
		country_resource_max_add = 20000
		arc_furnace_limit_add = 2
		dyson_swarm_limit_add = 2
		country_starbase_capacity_add = 3
	}

	weight_modifier = {
		factor = 0.25
		modifier = {
			factor = 1.5
			OR = {
				has_trait_in_council = { TRAIT = leader_trait_curator }
				has_trait_in_council = { TRAIT = leader_trait_maniacal }
				has_trait_in_council = { TRAIT = leader_trait_maniacal_2 }
				has_trait_in_council = { TRAIT = leader_trait_maniacal_3 }
			}
		}
		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = tech_mega_engineering
		}
		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_starhold
				count >= 1
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_starhold
				count >= 2
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_starhold
				count >= 3
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_starhold
				count >= 4
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_starhold
				count >= 5
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_starhold
				count >= 6
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_citadel
				count >= 1
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_citadel
				count >= 2
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_citadel
				count >= 3
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_citadel
				count >= 4
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_citadel
				count >= 5
			}
		}

		modifier = {
			factor = 1.5
			count_starbase_sizes = {
				starbase_size = starbase_citadel
				count >= 6
			}
		}

		modifier = {
			factor = 2
			any_owned_planet = {
				is_planet_class = pc_habitat
			}
		}

		modifier = {
			factor = 1.5
			any_neighbor_country = {
				has_technology = tech_mega_engineering
			}
		}

		modifier = {
			factor = 20
			OR = {
				has_any_megastructure_in_empire = yes
				has_origin = origin_shattered_ring
			}
		}

		# Nomad equivalents for starholds/citadels — Waystation tier
		modifier = {
			factor = 1.5
			is_nomadic = yes
			count_starbase_sizes = {
				starbase_size = starbase_waystation_2
				count >= 1
			}
		}
		modifier = {
			factor = 1.5
			is_nomadic = yes
			count_starbase_sizes = {
				starbase_size = starbase_waystation_2
				count >= 3
			}
		}
		modifier = {
			factor = 1.5
			is_nomadic = yes
			count_starbase_sizes = {
				starbase_size = starbase_waystation_3
				count >= 1
			}
		}
		modifier = {
			factor = 1.5
			is_nomadic = yes
			count_starbase_sizes = {
				starbase_size = starbase_waystation_3
				count >= 3
			}
		}
		# Nomad equivalent for any_neighbor_country — waystation in a system owned by an empire with the tech
		modifier = {
			factor = 1.5
			is_nomadic = yes
			any_owned_nonprimary_starbase = {
				is_waystation_starbase = yes
				solar_system = {
					space_owner = {
						has_technology = tech_mega_engineering
					}
				}
			}
		}
		# Nomad equivalent for has_any_megastructure_in_empire — waystation in a system with a megastructure
		modifier = {
			factor = 20
			is_nomadic = yes
			any_owned_nonprimary_starbase = {
				is_waystation_starbase = yes
				solar_system = {
					any_system_megastructure = {
						always = yes
					}
				}
			}
		}
	}


	ai_weight = {
		factor = 200000

		# policy_route = mega_engineering_core
		# source_object = technology:tech_mega_engineering
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_core_unlock_research_priority_ready = yes } }
		modifier = { factor = 4 staid_core_unlock_research_priority_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}


# policy_route = mega_shipyard_core; source = common/technology/00_megastructures.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_mega_shipyard = {
	area = society
	cost = @tier5cost3
	tier = 5
	category = { military_theory }
	ai_update_type = all
	prerequisites = { "tech_mega_engineering" }
	weight = @tier5weight3
	is_rare = yes

	potential = {
		has_federations_dlc = yes
		is_nomadic = no
	}

	weight_modifier = {
		factor = 0.25
		modifier = {
			factor = 0.5
			is_pacifist = yes
		}
		modifier = {
			factor = 2
			is_militarist = yes
		}
		modifier = {
			factor = 2
			OR = {
				has_trait_in_council = { TRAIT = leader_trait_maniacal }
				has_trait_in_council = { TRAIT = leader_trait_maniacal_2 }
				has_trait_in_council = { TRAIT = leader_trait_maniacal_3 }
			}
		}
		modifier = {
			factor = 2
			OR = {
				has_trait_in_council = { TRAIT = leader_trait_spark_of_genius }
				has_trait_in_council = { TRAIT = leader_trait_spark_of_genius_2 }
			}
		}
		modifier = {
			factor = 2
			has_galactic_wonders = yes
		}
		modifier = {
			factor = 6
			has_ascension_perk = ap_master_builders
		}
		modifier = {
			factor = 6
			has_ascension_perk = ap_galactic_force_projection
		}
		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = tech_mega_shipyard
		}
	}


	ai_weight = {
		factor = 180000

		# policy_route = mega_shipyard_core
		# source_object = technology:tech_mega_shipyard
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_core_unlock_research_priority_ready = yes } }
		modifier = { factor = 4 staid_core_unlock_research_priority_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 5 years_passed > 79 }
		modifier = { factor = 8 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}


# policy_route = research_megastructure_core; source = common/technology/00_megastructures.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_science_nexus = {
	area = physics
	cost = @tier5cost3
	tier = 5
	category = { computing }
	ai_update_type = all
	prerequisites = { "tech_mega_engineering" }
	weight = @tier5weight3
	is_rare = yes

	potential = {
		is_nomadic = no
	}

	weight_modifier = {
		factor = 0.25
		modifier = {
			factor = 2
			OR = {
				has_trait_in_council = { TRAIT = leader_trait_maniacal }
				has_trait_in_council = { TRAIT = leader_trait_maniacal_2 }
				has_trait_in_council = { TRAIT = leader_trait_maniacal_3 }
			}
		}
		modifier = {
			factor = 2
			OR = {
				has_trait_in_council = { TRAIT = leader_trait_spark_of_genius }
				has_trait_in_council = { TRAIT = leader_trait_spark_of_genius_2 }
			}
		}
		modifier = {
			factor = 2
			has_galactic_wonders = yes
		}
		modifier = {
			factor = 6
			has_ascension_perk = ap_master_builders
		}
		modifier = {
			factor = 9
			has_ascension_perk = ap_technological_ascendancy
		}
		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = tech_science_nexus
		}
	}


	ai_weight = {
		factor = 185000

		# policy_route = research_megastructure_core
		# source_object = technology:tech_science_nexus
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_science_nexus_research_priority_ready = yes } }
		modifier = { factor = 4 staid_science_nexus_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 7 years_passed > 79 }
		modifier = { factor = 10 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 4 has_technology = tech_science_nexus }
		modifier = { factor = 3 staid_research_under_curve = yes }
	}
}


# policy_route = ring_world_growth_core; source = common/technology/zz_giga_tech_overwrites.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_ring_world = {
    area = engineering
    cost = @tier5cost3
    tier = 5
    category = { voidcraft }
    ai_update_type = all
    prerequisites = { "tech_mega_engineering" }
    weight = @tier5weight3
    is_rare = yes
    potential = { always = yes } # curse tech overwrite weirdness and its potential inheritance jank

    # name change from the vanilla "Ring Segment"
    technology_swap = {
        name = giga_tech_ring_world_swap
        inherit_icon = yes
        inherit_effects = yes

        trigger = {
            giga_can_use_habitables = yes
        }

        prereqfor_desc = {
            custom = {
                title = allow_ring_world
                desc = ring_world_1_MEGASTRUCTURE_DETAILS
            }
        }

        # just so I don't need to repeat the same thing 3 times...
        # it's this way around instead of in the main tech so the ring unlock appears first
        inline_script = technology/giga_ring_world_overwrite
    }

    # swap for non-bioship empires which can't build the ring (e.g. frame with a regular set)
    technology_swap = {
        name = giga_tech_ring_world_swap_no_habitables
        inherit_icon = no
        inherit_effects = no

        trigger = {
            giga_can_use_habitables = no
            country_uses_bio_ships = no
        }

        inline_script = technology/giga_ring_world_overwrite

        category = { industry }
    }

    # swap for bioship empires which can't build the ring (e.g. wilderness, frame with a bio set)
    technology_swap = {
        name = giga_tech_ring_world_swap_no_habitables_bio
        inherit_icon = no
        inherit_effects = no

        trigger = {
            giga_can_use_habitables = no
            country_uses_bio_ships = yes
        }

        inline_script = technology/giga_ring_world_overwrite

        area = society
        category = { biology }
    }

    weight_modifier = {
        factor = 0
    }


	ai_weight = {
		factor = 175000

		# policy_route = ring_world_growth_core
		# source_object = technology:tech_ring_world
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_ring_world_research_priority_ready = yes } }
		modifier = { factor = 4 staid_ring_world_research_priority_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 6 years_passed > 79 }
		modifier = { factor = 9 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 4 has_technology = tech_ring_world }
		modifier = { factor = 2 staid_planetary_capacity_growth_ready = yes }
	}
}


# policy_route = early_kilo_economy_core; source = common/technology/00_machine_age_tech.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_orbital_arc_furnace = {
    area = engineering
    cost = @tier2cost3
    tier = 2
    category = { materials }
    ai_update_type = all
    weight = 0
    is_rare = yes
    is_reverse_engineerable = no
    weight = @tier2weight3

    potential = {
        has_machine_age_dlc = yes
    }

    modifier = {
        arc_furnace_limit_add = 3
    }

    weight_modifier = {
        factor = 0.5

        modifier = {
            factor = 0.2
            NOR = {
                has_trait_in_council = { TRAIT = leader_trait_expertise_materials }
                has_trait_in_council = { TRAIT = leader_trait_curator }
                has_trait_in_council = { TRAIT = leader_trait_spark_of_genius }
                has_trait_in_council = { TRAIT = leader_trait_spark_of_genius_2 }
                has_trait_in_council = { TRAIT = leader_trait_maniacal }
                has_trait_in_council = { TRAIT = leader_trait_maniacal_2 }
                has_trait_in_council = { TRAIT = leader_trait_maniacal_3 }
            }
        }
        modifier = {
            factor = 2
            OR = {
                has_megastructure = orbital_arc_furnace_1
                has_megastructure = orbital_arc_furnace_2
                has_megastructure = orbital_arc_furnace_3
                has_megastructure = orbital_arc_furnace_4
            }
        }
    }
    prereqfor_desc = {
        ship = {
            title = "allow_arc_furnace"
            desc = "orbital_arc_furnace_1_MEGASTRUCTURE_DETAILS"
        }
    }


	ai_weight = {
		factor = 165000

		# policy_route = early_kilo_economy_core
		# source_object = technology:tech_orbital_arc_furnace
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_early_kilo_economy_research_priority_ready = yes } }
		modifier = { factor = 4 staid_early_kilo_economy_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 6 years_passed > 79 }
		modifier = { factor = 8 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 has_technology = tech_orbital_arc_furnace }
		modifier = { factor = 3 has_technology = giga_tech_asteroid_manufactory }
		modifier = { factor = 6 staid_resource_waste_pressure = yes }
		modifier = { factor = 8 staid_high_scale_snowball_pressure = yes }
	}
}


# policy_route = early_kilo_economy_core; source = common/technology/giga_02_society.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_asteroid_manufactory = {
	cost = @tier3cost2
	area = society
	tier = 3
	category = { new_worlds }
	prerequisites = {
		OR = {
			tech_waystation_2
			tech_starbase_3
		}
		tech_space_mining_2
	}

	weight = @tier3weight2

	potential = {
		NOT = { has_global_flag = asteroid_manufactory_disabled }
	}

	modifier = {
		giga_asteroid_manufactory_limit_add = 3
	}

	weight_modifier = {
		modifier = {
			factor = 0.1
			NOT = { years_passed > 50 }
		}

		inline_script = {
			script = technology/tech_weight_boni/neighbor_spread_tech_weight_bonus
			TECHNOLOGY = giga_tech_asteroid_manufactory
		}

		inline_script = technology/tech_weight_boni/expansionist_tech_weight_bonus
		inline_script = technology/tech_weight_boni/exploitative_tech_weight_bonus

		modifier = {
			factor = 1.25
			has_tradition = tr_macroengineering_adopt
		}
		modifier = {
			factor = 1.25
			has_tradition = tr_macroengineering_finish
		}
	}


	ai_weight = {
		factor = 160000

		# policy_route = early_kilo_economy_core
		# source_object = technology:giga_tech_asteroid_manufactory
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_early_kilo_economy_research_priority_ready = yes } }
		modifier = { factor = 4 staid_early_kilo_economy_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 6 years_passed > 79 }
		modifier = { factor = 8 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 has_technology = tech_orbital_arc_furnace }
		modifier = { factor = 3 has_technology = giga_tech_asteroid_manufactory }
		modifier = { factor = 6 staid_resource_waste_pressure = yes }
		modifier = { factor = 8 staid_high_scale_snowball_pressure = yes }
	}
}


# policy_route = science_kilo_snowball_core; source = common/technology/giga_03_engineering.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_engineering_test_site = {
	cost = @tier3cost2
	area = engineering
	tier = 3
	category = { materials }
	prerequisites = {
        OR = {
            tech_starbase_4
            tech_waystation_3
        }
		OR = {
			tech_cruisers
			tech_harbingers
		}
	}
	weight = @tier3weight2
	is_rare = no
	prereqfor_desc = {
		custom = { title = "allow_eng_test_site"	desc = "desc_eng_test_site" }
	}
	modifier = {
		country_resource_max_add = 2500
		ship_armor_mult = 0.05
		giga_megabase_limit_add = 3
	}

	potential = {
		NOT = {
			AND = {
				has_global_flag = megabase_disabled
				has_global_flag = lifters_disabled
				has_global_flag = compressor_disabled
			}
		}
	}

	weight_modifier = {
		# militarists get this, scientists get physics kilo, other empires get society kilo
		inline_script = technology/tech_weight_boni/militarist_tech_weight_bonus

		inline_script = {
			script = technology/tech_weight_boni/neighbor_spread_tech_weight_bonus
			TECHNOLOGY = giga_tech_engineering_test_site
		}
	}


	ai_weight = {
		factor = 165000

		# policy_route = science_kilo_snowball_core
		# source_object = technology:giga_tech_engineering_test_site
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_science_kilo_research_priority_ready = yes } }
		modifier = { factor = 4 staid_science_kilo_research_priority_ready = yes }
		modifier = { factor = 5 years_passed > 44 }
		modifier = { factor = 8 years_passed > 79 }
		modifier = { factor = 11 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 4 has_technology = giga_tech_engineering_test_site }
		modifier = { factor = 4 has_technology = giga_tech_macro_scale_weather_manipulation }
		modifier = { factor = 3 staid_research_under_curve = yes }
	}
}


# policy_route = science_kilo_snowball_core; source = common/technology/giga_01_physics.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_macro_scale_weather_manipulation = {
	cost = @tier3cost2
	area = physics
	tier = 3
	category = { field_manipulation }
	is_rare = no
	prerequisites = {
		tech_sensors_3
		OR = {
			tech_cruisers
			tech_harbingers
		}
	}
	weight = @tier3weight2
	prereqfor_desc = {
		custom = { title = "allow_atmosphere_shredder"	desc = "desc_atmosphere_shredder" }
	}
	modifier = {
		country_resource_max_add = 2500
		ship_shield_mult = 0.05
		giga_storm_observatory_limit_add = 3
	}

	potential = {
		NOT = {
			AND = {
				has_global_flag = storm_observatory_disabled
				# keep tech if prereqs are on
				has_global_flag = suppressor_disabled
				has_global_flag = compressor_disabled
				has_global_flag = ndb_disabled
				has_global_flag = penrose_sphere_disabled
				has_global_flag = planetary_computer_disabled
				has_global_flag = lifters_disabled
				# yes the entire terraform line relies on this tech, apparently
				has_global_flag = terraform_barren_disabled
				has_global_flag = terraform_toxic_disabled
				has_global_flag = terraform_gasgiant_disabled
				has_global_flag = geothermal_disabled
				has_global_flag = glue_disabled
			}
		}
	}

	weight_modifier = {
		# materialists -> physics
		inline_script = technology/tech_weight_boni/scientist_tech_weight_bonus

		inline_script = {
			script = technology/tech_weight_boni/neighbor_spread_tech_weight_bonus
			TECHNOLOGY = giga_tech_macro_scale_weather_manipulation
		}
	}


	ai_weight = {
		factor = 170000

		# policy_route = science_kilo_snowball_core
		# source_object = technology:giga_tech_macro_scale_weather_manipulation
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_science_kilo_research_priority_ready = yes } }
		modifier = { factor = 4 staid_science_kilo_research_priority_ready = yes }
		modifier = { factor = 5 years_passed > 44 }
		modifier = { factor = 8 years_passed > 79 }
		modifier = { factor = 11 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 4 has_technology = giga_tech_engineering_test_site }
		modifier = { factor = 4 has_technology = giga_tech_macro_scale_weather_manipulation }
		modifier = { factor = 3 staid_research_under_curve = yes }
	}
}


# policy_route = planetary_computer_research_core; source = common/technology/giga_02_society.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_planetary_computer = {
	cost = @tier5cost3
	area = society
	tier = 5
	category = { new_worlds }
	is_rare = yes
	prerequisites = { "tech_ecological_adaptation" "tech_self_aware_logic" "tech_power_plant_3" "giga_tech_macro_scale_weather_manipulation" }
	weight = @tier5weight3

	#everyone who isn't Wilderness technically gets a swap so Wilderness doesn't get the "Unlocks Megastructure" desc
	technology_swap = {
		name = giga_tech_planetary_computer
		inherit_icon = yes
		inherit_effects = yes

		prereqfor_desc = {
			custom = { title = "allow_planetary_computer"	desc = "desc_planetary_computer" }
		}

		trigger = {
			is_wilderness_empire = no
		}
	}

	technology_swap = {
		name = giga_tech_planetary_computer_wilderness_swap
		inherit_icon = yes
		inherit_effects = yes

		trigger = {
			is_wilderness_empire = yes
		}
	}

	modifier = {			# Incase this tech's megastructure is disabled or inaccessible to your empire type
		planet_researchers_produces_mult = 0.05
		planet_researchers_upkeep_mult = 0.05
	}

	potential = {
		has_galactic_wonders = yes
		NOT = { has_global_flag = planetary_computer_disabled }
		is_nomadic = no
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/scientist_tech_weight_bonus

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_planetary_computer
		}
	}


	ai_weight = {
		factor = 190000

		# policy_route = planetary_computer_research_core
		# source_object = technology:giga_tech_planetary_computer
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_planetary_computer_research_priority_ready = yes } }
		modifier = { factor = 4 staid_planetary_computer_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 8 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 5 has_technology = giga_tech_planetary_computer }
		modifier = { factor = 4 staid_research_under_curve = yes }
		modifier = { factor = 2 staid_planetary_capacity_growth_ready = yes }
	}
}


# policy_route = pop_assembly_snowball_core; source = common/technology/00_eng_tech.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_robotic_workers = {
	cost = @tier1cost3
	area = engineering
	tier = 1
	category = { industry }
	prerequisites = { "tech_powered_exoskeletons" }
	weight = @tier1weight3

	gateway = robotics

	feature_flags = { robots }

	potential = {
		NOR = {
			has_ethic = "ethic_gestalt_consciousness"
			is_individual_machine = yes
		}
	}

	weight_modifier = {
		factor = 1.5
		modifier = {
			factor = 0
			has_policy_flag = robots_outlawed
		}
		modifier = {
			factor = 0.5
			OR = {
				has_ethic = "ethic_spiritualist"
				has_ethic = "ethic_fanatic_spiritualist"
			}
		}
		modifier = {
			factor = 2
			is_materialist = yes
		}

	}


	ai_weight = {
		factor = 145000

		# policy_route = pop_assembly_snowball_core
		# source_object = technology:tech_robotic_workers
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_pop_assembly_snowball_ready = yes } }
		modifier = { factor = 4 staid_pop_assembly_snowball_ready = yes }
		modifier = { factor = 6 years_passed > 44 }
		modifier = { factor = 9 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 4 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 5 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 3 staid_research_under_curve = yes }
		modifier = { factor = 2 years_passed < 80 }
	}
}


# policy_route = pop_assembly_snowball_core; source = common/technology/00_eng_tech.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_robot_assembly_complex = {
	icon = "tech_mega_assembly"
	cost = @tier4cost1
	area = engineering
	tier = 4
	category = { industry }
	prerequisites = { "tech_robomodding" "tech_galactic_administration" }
	is_rare = yes
	weight = @tier4weight1

	potential = {
		NOT = { has_ethic = "ethic_gestalt_consciousness" }
	}


	weight_modifier = {
		factor = 0.5
		modifier = {
			factor = 0.20
			NOR = {
				has_trait_in_council = { TRAIT = leader_trait_maniacal }
				has_trait_in_council = { TRAIT = leader_trait_maniacal_2 }
				has_trait_in_council = { TRAIT = leader_trait_maniacal_3 }
				has_trait_in_council = { TRAIT = leader_trait_spark_of_genius }
				has_trait_in_council = { TRAIT = leader_trait_spark_of_genius_2 }
				has_trait_in_council = { TRAIT = leader_trait_curator }
				has_trait_in_council = { TRAIT = leader_trait_expertise_industry }
			}
		}
		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = tech_robot_assembly_complex
		}
	}


	ai_weight = {
		factor = 165000

		# policy_route = pop_assembly_snowball_core
		# source_object = technology:tech_robot_assembly_complex
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_pop_assembly_snowball_ready = yes } }
		modifier = { factor = 4 staid_pop_assembly_snowball_ready = yes }
		modifier = { factor = 6 years_passed > 44 }
		modifier = { factor = 9 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 4 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 5 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 3 staid_research_under_curve = yes }
		modifier = { factor = 2 years_passed < 80 }
	}
}


# policy_route = pop_assembly_snowball_core; source = common/technology/00_synthetic_dawn_tech.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_mega_assembly = {
	cost = @tier4cost1
	area = engineering
	tier = 4
	category = { industry }
	prerequisites = { "tech_binary_motivators" "tech_galactic_administration" }
	is_rare = yes
	weight = @tier4weight1

	potential = {
		OR = {
			is_machine_empire = yes
			is_individual_machine = yes
			is_hive_empire_with_machines = yes
		}
	}

	weight_modifier = {
		factor = 0.5
		modifier = {
			factor = 0.20
			NOR = {
				has_trait_in_council = { TRAIT = leader_trait_maniacal }
				has_trait_in_council = { TRAIT = leader_trait_maniacal_2 }
				has_trait_in_council = { TRAIT = leader_trait_maniacal_3 }
				has_trait_in_council = { TRAIT = leader_trait_spark_of_genius }
				has_trait_in_council = { TRAIT = leader_trait_spark_of_genius_2 }
				has_trait_in_council = { TRAIT = leader_trait_curator }
				has_trait_in_council = { TRAIT = leader_trait_expertise_industry }
			}
		}
		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = tech_mega_assembly
		}
	}


	ai_weight = {
		factor = 175000

		# policy_route = pop_assembly_snowball_core
		# source_object = technology:tech_mega_assembly
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_pop_assembly_snowball_ready = yes } }
		modifier = { factor = 4 staid_pop_assembly_snowball_ready = yes }
		modifier = { factor = 6 years_passed > 44 }
		modifier = { factor = 9 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 4 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 5 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 3 staid_research_under_curve = yes }
		modifier = { factor = 2 years_passed < 80 }
	}
}


# policy_route = pop_assembly_snowball_core; source = common/technology/00_soc_tech.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_cloning = {
	cost = @tier2cost2
	area = society
	tier = 2
	category = { biology }
	prerequisites = { "tech_genome_mapping" }
	weight = @tier2weight2

	potential = {
		OR = {
			is_machine_empire = no
			has_civic = civic_machine_assimilator
		}
		is_wilderness_empire = no
		is_natural_design_empire = no
	}

	weight_modifier = {
		factor = 1.5	# genetech needs to be a bit more common
		modifier = {
			factor = 1.25
			is_hive_empire = yes
		}
		modifier = {
			factor = 1.25
			has_tradition = tr_supremacy_adopt
		}
		modifier = {
			factor = 2
			has_relic = r_pox_sample
		}
		modifier = {
			factor = 0.5
			is_individual_machine = yes
		}
		modifier = {
			factor = 0.5
			has_origin = origin_synthetic_fertility
		}
		modifier = {
			factor = 2
			AND = {
				is_individual_machine = yes
				any_owned_species = {
					is_organic_species = yes
				}
			}
		}
	}


	ai_weight = {
		factor = 150000

		# policy_route = pop_assembly_snowball_core
		# source_object = technology:tech_cloning
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_pop_assembly_snowball_ready = yes } }
		modifier = { factor = 4 staid_pop_assembly_snowball_ready = yes }
		modifier = { factor = 6 years_passed > 44 }
		modifier = { factor = 9 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 4 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 5 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 3 staid_research_under_curve = yes }
		modifier = { factor = 2 years_passed < 80 }
	}
}


# policy_route = storage_cap_core; source = common/technology/giga_01_physics.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_kugelblitz = {
	cost = @tier4cost2
	area = physics
	tier = 4
	category = { particles }
	is_rare = no
	prerequisites = { "tech_starbase_5" "tech_zero_point_power" }
	weight = @tier4weight2
	prereqfor_desc = {
		custom = { title = "allow_kugelblitz"	desc = "desc_kugelblitz" }
	}
	modifier = {
        country_resource_max_add = 5000
        giga_kugel_limit_add = 3
    }

	potential = {
		NOT = { has_global_flag = kugel_disabled }
	}

	weight_modifier = {
		inline_script = {
			inline_script = technology/tech_weight_boni/expansionist_tech_weight_bonus

			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_kugelblitz
		}
	}


	ai_weight = {
		factor = 160000

		# policy_route = storage_cap_core
		# source_object = technology:giga_tech_kugelblitz
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_storage_cap_research_priority_ready = yes } }
		modifier = { factor = 4 staid_storage_cap_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 7 years_passed > 79 }
		modifier = { factor = 10 years_passed > 119 }
		modifier = { factor = 4 has_technology = giga_tech_kugelblitz }
		modifier = { factor = 10 staid_resource_waste_pressure = yes }
		modifier = { factor = 14 staid_high_scale_snowball_pressure = yes }
	}
}


# policy_route = apex_site_preservation_core; source = common/technology/giga_05_weightless.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_matrioshka_brain_1 = {
	cost = @giga_tier7cost1
	area = physics
	tier = 5
	category = { field_manipulation }
	weight = 0
	is_rare = yes

	prereqfor_desc = {
		hide_prereq_for_desc = ship
		hide_prereq_for_desc = component
		hide_prereq_for_desc = feature
		hide_prereq_for_desc = resource
		custom = {
			title = "header_01_gigac"
			desc = "header_01_gigac_desc"
		}
		custom = {
			title = "allow_matrioshka_brain"
			desc = "desc_matrioshka_brain"
		}
	}
	potential = {
		has_gigastructural_constructs = yes
		NOT = { has_global_flag = matrioshka_brain_disabled }
	}

	ai_weight = {
		factor = 210000

		# policy_route = apex_site_preservation_core
		# source_object = technology:giga_tech_matrioshka_brain_1
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_apex_site_preservation_ready = yes } }
		modifier = { factor = 4 staid_apex_site_preservation_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 5 years_passed > 79 }
		modifier = { factor = 9 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 8 has_technology = giga_tech_matrioshka_brain_1 }
		modifier = { factor = 4 has_technology = giga_tech_neutronium_gigaforge }
		modifier = { factor = 0.15 NOT = { staid_apex_site_preservation_ready = yes } }
	}
}


# policy_route = apex_site_preservation_core; source = common/technology/giga_03_engineering.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_neutronium_gigaforge = {
	cost = @giga_tier6cost2
	area = engineering
	tier = 5
	category = { voidcraft }
	is_rare = yes
	prerequisites = {
		tech_starbase_5
		OR = {
			tech_battleships
			tech_stingers
		}
		tech_ship_armor_5
	}
	weight = @giga_tier6weight2
	prereqfor_desc = {
		custom = { title = "allow_neut_gigaforge"	desc = "desc_neut_gigaforge" }
	}
	modifier = {
		country_resource_max_add = 10000
		ship_armor_mult = 0.05
	}

	potential = {
		NOT = {
			AND = {
				has_global_flag = gigaforge_disabled
				has_global_flag = nidavellir_disabled
			}
		}
		has_galactic_wonders = yes
	}

	weight_modifier = {
		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_neutronium_gigaforge
		}
	}


	ai_weight = {
		factor = 185000

		# policy_route = apex_site_preservation_core
		# source_object = technology:giga_tech_neutronium_gigaforge
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_apex_site_preservation_ready = yes } }
		modifier = { factor = 4 staid_apex_site_preservation_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 5 years_passed > 79 }
		modifier = { factor = 9 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 8 has_technology = giga_tech_matrioshka_brain_1 }
		modifier = { factor = 4 has_technology = giga_tech_neutronium_gigaforge }
		modifier = { factor = 0.15 NOT = { staid_apex_site_preservation_ready = yes } }
	}
}


# policy_route = apex_site_preservation_core; source = common/technology/giga_03_engineering.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_nidavellir = {
	cost = @giga_tier7cost3
	area = engineering
	tier = 5
	category = { voidcraft }
	is_rare = yes
	weight = @giga_tier7weight1
	prerequisites = { "giga_tech_tetradimensional_engineering" }
	prereqfor_desc = {
		hide_prereq_for_desc = ship
		hide_prereq_for_desc = component
		hide_prereq_for_desc = feature
		hide_prereq_for_desc = resource
		custom = { title = "header_02_tetra"	desc = "header_02_tetra_desc" }
		custom = { title = "allow_nidavellir"	desc = "desc_nidavellir" }
	}

	potential = {
		NOT = { has_global_flag = nidavellir_disabled }
		has_gigastructural_constructs = yes
	}

	weight_modifier = {
		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_nidavellir
		}
	}


	ai_weight = {
		factor = 195000

		# policy_route = apex_site_preservation_core
		# source_object = technology:giga_tech_nidavellir
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_apex_site_preservation_ready = yes } }
		modifier = { factor = 4 staid_apex_site_preservation_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 5 years_passed > 79 }
		modifier = { factor = 9 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 8 has_technology = giga_tech_matrioshka_brain_1 }
		modifier = { factor = 4 has_technology = giga_tech_neutronium_gigaforge }
		modifier = { factor = 0.15 NOT = { staid_apex_site_preservation_ready = yes } }
	}
}


# policy_route = crowded_tall_route; source = common/technology/giga_03_engineering.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_interstellar_habitat = {
	cost = @tier4cost3
	area = engineering
	tier = 4
	category = { voidcraft }
	is_rare = yes
	prerequisites = { "tech_mega_engineering" "tech_gateway_construction" "tech_habitat_1" }
	weight = @tier4weight3
	prereqfor_desc = {
		custom = { title = "allow_interstellar_hab"	desc = "desc_interstellar_hab" }
	}
	modifier = { megastructure_build_speed_mult = 0.05 }			# Incase this tech's megastructure is disabled

	potential = {
		NOT = {
			AND = {
				has_global_flag = stellarhabitat_disabled
				# what's that? nothing to see here
				has_global_flag = svalinn_disabled
			}
		}
		is_void_dweller_empire = yes
		giga_can_use_habitables = yes
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/expansionist_tech_weight_bonus

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_interstellar_habitat
		}
	}


	ai_weight = {
		factor = 155000

		# policy_route = crowded_tall_route
		# source_object = technology:giga_tech_interstellar_habitat
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 4 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}


# policy_route = crowded_tall_route; source = common/technology/giga_02_society.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_stellar_ring_habitat = {
	area = society
	cost = @tier5cost3
	tier = 5
	category = { new_worlds }
	ai_update_type = all
	prerequisites = { tech_mega_engineering tech_habitat_2 }
	weight = @tier5weight3
	is_rare = yes

	prereqfor_desc = {
		custom = { title = allow_giga_orbital	desc = desc_giga_orbital }
	}

	potential = {
		always = no # 3.9 made this mega obsolete, pending rework
		#
		#is_void_dweller_empire = yes
		# is_nomadic = no
	}

	weight_modifier = {
		factor = 0.25

		modifier = {
			factor = @giga_tech_weight_malus_large
			is_militarist = yes
		}
		modifier = {
			factor = @giga_tech_weight_boost_large
			is_pacifist = yes
		}
		modifier = {
			factor = @giga_tech_weight_boost_large
			has_valid_civic = civic_machine_servitor
		}

		inline_script = technology/tech_weight_boni/maniacal_or_spark_tech_weight_bonus

		modifier = {
			factor = @giga_tech_weight_boost_large
			has_galactic_wonders = yes
		}
		modifier = {
			factor = @giga_tech_weight_boost_massive
			has_ascension_perk = ap_master_builders
		}
		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_stellar_ring_habitat
		}

		modifier = { factor = 0	giga_can_use_habitables = no	}
	}


	ai_weight = {
		factor = 150000

		# policy_route = crowded_tall_route
		# source_object = technology:giga_tech_stellar_ring_habitat
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 4 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}


# policy_route = planetcraft_route; source = common/technology/giga_01_physics.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_planet_assembly = {
	cost = @giga_tier7cost3
	area = physics
	tier = 5
	category = { particles }
	is_rare = yes
	weight = @giga_tier7weight1

	prerequisites = { "giga_tech_lunar_assembly" }

	modifier = { megastructure_build_speed_mult = 0.05 }			# Incase this tech's megastructure is disabled

	prereqfor_desc = {
		custom = { title = "allow_planet_assembly"	desc = "allow_planet_assembly_desc" }
	}

	potential = {
		NOT = { has_global_flag = giga_celestial_printing_planet_disabled }
		has_ascension_perk = ap_celestial_printing
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/shipbuilding_tech_weight_bonus

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_planet_assembly
		}
	}


	ai_weight = {
		factor = 160000

		# policy_route = planetcraft_route
		# source_object = technology:giga_tech_planet_assembly
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_planetcraft_research_priority_ready = yes } }
		modifier = { factor = 4 staid_planetcraft_research_priority_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 6 years_passed > 79 }
		modifier = { factor = 10 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 4 has_technology = giga_tech_planet_assembly }
		modifier = { factor = 3 has_ascension_perk = ap_celestial_printing }
	}
}


# policy_route = war_moon_route; source = common/technology/giga_01_physics.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_lunar_assembly = {
	cost = @giga_tier6cost3
	area = physics
	tier = 5
	category = { particles }
	is_rare = yes
	weight = 0

	modifier = { megastructure_build_speed_mult = 0.05 }			# Incase this tech's megastructure is disabled

	potential = {
		NOT = { has_global_flag = giga_celestial_printing_moon_disabled }
		has_ascension_perk = ap_celestial_printing
	}
	prereqfor_desc = {
		custom = { title = "allow_lunar_assembly"	desc = "allow_lunar_assembly_desc" }
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/shipbuilding_tech_weight_bonus
	}


	ai_weight = {
		factor = 135000

		# policy_route = war_moon_route
		# source_object = technology:giga_tech_lunar_assembly
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_war_moon_research_priority_ready = yes } }
		modifier = { factor = 4 staid_war_moon_research_priority_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 6 years_passed > 79 }
		modifier = { factor = 10 years_passed > 119 }
		modifier = { factor = 2 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 has_technology = giga_tech_war_moon_1 }
		modifier = { factor = 6 has_technology = giga_tech_war_moon_2 }
	}
}


# policy_route = war_moon_route; source = common/technology/giga_03_engineering.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_war_moon_1 = {
	cost = @giga_tier6cost1
	area = engineering
	tier = 5
	category = { voidcraft }
	is_rare = yes
	prerequisites = { "tech_mega_engineering" "tech_thrusters_4" "giga_tech_asteroid_artillery" }
	weight = @giga_tier6weight1
	modifier = { ship_base_speed_mult = 0.10 }

	prereqfor_desc = {
		hide_prereq_for_desc = ship
		custom = { title = "giga_mobile_planet_quest_chain" desc = "giga_mobile_planet_quest_chain" }
	}

	potential = {
		NOT = {
			AND = {
				has_global_flag = warmoon_disabled
				has_global_flag = warplanet_disabled
				has_global_flag = systemcraft_disabled
			}
		}
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/militarist_tech_weight_bonus

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_war_moon_1
		}
	}


	ai_weight = {
		factor = 155000

		# policy_route = war_moon_route
		# source_object = technology:giga_tech_war_moon_1
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_war_moon_research_priority_ready = yes } }
		modifier = { factor = 4 staid_war_moon_research_priority_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 6 years_passed > 79 }
		modifier = { factor = 10 years_passed > 119 }
		modifier = { factor = 2 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 has_technology = giga_tech_war_moon_1 }
		modifier = { factor = 6 has_technology = giga_tech_war_moon_2 }
	}
}


# policy_route = war_moon_route; source = common/technology/giga_03_engineering.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_war_moon_2 = {
	cost = @giga_tier6cost2
	area = engineering
	tier = 5
	category = { voidcraft }
	is_rare = yes
	prerequisites = { "giga_tech_war_moon_1" }
	weight = @giga_tier6weight2
	prereqfor_desc = {
		custom = { title = "allow_war_moon"	desc = "desc_war_moons" }
		custom = { title = "giga_mobile_planet_quest_chain" desc = "giga_mobile_planet_quest_chain" }
	}

	modifier = { command_limit_add = 100 }

	potential = {
		NOT = {
			AND = {
				has_global_flag = warmoon_disabled
				has_global_flag = warplanet_disabled
				has_global_flag = systemcraft_disabled
			}
		}
		has_galactic_wonders = yes
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/militarist_tech_weight_bonus

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_war_moon_2
		}
	}


	ai_weight = {
		factor = 180000

		# policy_route = war_moon_route
		# source_object = technology:giga_tech_war_moon_2
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_war_moon_research_priority_ready = yes } }
		modifier = { factor = 4 staid_war_moon_research_priority_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 6 years_passed > 79 }
		modifier = { factor = 10 years_passed > 119 }
		modifier = { factor = 2 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 has_technology = giga_tech_war_moon_1 }
		modifier = { factor = 6 has_technology = giga_tech_war_moon_2 }
	}
}


# policy_route = war_moon_route; source = common/technology/giga_03_engineering.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_war_moon_sections = {
	cost = @giga_tier6cost1
	area = engineering
	tier = 5
	category = { propulsion }
	is_rare = yes
	prerequisites = { "giga_tech_war_moon_2" }
	weight = @giga_tier6weight1

	prereqfor_desc = {
		custom = { title = "allow_attack_moon_specialization"	desc = "allow_attack_moon_specialization" }
	}

	potential = {
		has_galactic_wonders = yes
		NOT = { has_global_flag = warmoon_disabled }
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/militarist_tech_weight_bonus

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_war_moon_sections
		}
	}


	ai_weight = {
		factor = 150000

		# policy_route = war_moon_route
		# source_object = technology:giga_tech_war_moon_sections
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_war_moon_research_priority_ready = yes } }
		modifier = { factor = 4 staid_war_moon_research_priority_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 6 years_passed > 79 }
		modifier = { factor = 10 years_passed > 119 }
		modifier = { factor = 2 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 has_technology = giga_tech_war_moon_1 }
		modifier = { factor = 6 has_technology = giga_tech_war_moon_2 }
	}
}


# policy_route = systemcraft_route; source = common/technology/giga_05_weightless.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_war_system_1 = {
	cost = @giga_50_000_cost
	area = physics
	tier = 5
	category = { particles }
	is_rare = yes
	weight = 0
	modifier = { ship_speed_mult = 0.05 }
	prereqfor_desc = {
		custom = {
			title = "allow_systemcraft_p0"
			desc = "desc_systemcraft_p0"
		}
	}

	modifier = { command_limit_add = 250 }

	potential = {
		has_ascension_perk = ap_celestial_printing
		NOR = {
			has_global_flag = systemcraft_disabled
			has_global_flag = warmoon_disabled
			has_global_flag = warplanet_disabled
		}
	}

	ai_weight = {
		factor = 150000

		# policy_route = systemcraft_route
		# source_object = technology:giga_tech_war_system_1
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_systemcraft_research_priority_ready = yes } }
		modifier = { factor = 4 staid_systemcraft_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 8 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 has_ascension_perk = ap_celestial_printing }
		modifier = { factor = 4 has_technology = giga_tech_war_system_1 }
		modifier = { factor = 5 has_technology = giga_tech_war_system_2 }
		modifier = { factor = 6 has_technology = giga_tech_war_system_3 }
		modifier = { factor = 8 has_technology = giga_tech_war_system_6 }
	}
}


# policy_route = systemcraft_route; source = common/technology/giga_01_physics.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_war_system_2 = {
	cost = @giga_tier7cost1
	area = physics
	tier = 5
	category = { particles }
	is_rare = yes
	prerequisites = { "giga_tech_war_system_1" }
	weight = @giga_tier7weight1
	prereqfor_desc = {
		hide_prereq_for_desc = ship
		hide_prereq_for_desc = component
		hide_prereq_for_desc = feature
		hide_prereq_for_desc = resource
		custom = { title = "allow_systemcraft_p1"	desc = "desc_systemcraft_p1" }
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/militarist_tech_weight_bonus

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_war_system_2
		}
	}


	ai_weight = {
		factor = 170000

		# policy_route = systemcraft_route
		# source_object = technology:giga_tech_war_system_2
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_systemcraft_research_priority_ready = yes } }
		modifier = { factor = 4 staid_systemcraft_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 8 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 has_ascension_perk = ap_celestial_printing }
		modifier = { factor = 4 has_technology = giga_tech_war_system_1 }
		modifier = { factor = 5 has_technology = giga_tech_war_system_2 }
		modifier = { factor = 6 has_technology = giga_tech_war_system_3 }
		modifier = { factor = 8 has_technology = giga_tech_war_system_6 }
	}
}


# policy_route = systemcraft_route; source = common/technology/giga_01_physics.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_war_system_3 = {
	cost = @giga_tier7cost2
	area = physics
	tier = 5
	category = { particles }
	is_rare = yes
	prerequisites = { "giga_tech_war_system_2" }
	weight = @giga_tier7weight1
	prereqfor_desc = {
		hide_prereq_for_desc = ship
		hide_prereq_for_desc = component
		hide_prereq_for_desc = feature
		hide_prereq_for_desc = resource
		custom = { title = "allow_systemcraft_p2"	desc = "desc_systemcraft_p2" }
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/militarist_tech_weight_bonus

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_war_system_3
		}
	}


	ai_weight = {
		factor = 190000

		# policy_route = systemcraft_route
		# source_object = technology:giga_tech_war_system_3
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_systemcraft_research_priority_ready = yes } }
		modifier = { factor = 4 staid_systemcraft_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 8 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 has_ascension_perk = ap_celestial_printing }
		modifier = { factor = 4 has_technology = giga_tech_war_system_1 }
		modifier = { factor = 5 has_technology = giga_tech_war_system_2 }
		modifier = { factor = 6 has_technology = giga_tech_war_system_3 }
		modifier = { factor = 8 has_technology = giga_tech_war_system_6 }
	}
}


# policy_route = systemcraft_route; source = common/technology/giga_01_physics.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_war_system_4 = {
	cost = @giga_tier7cost2
	area = physics
	tier = 5
	category = { field_manipulation }
	is_rare = yes
	prerequisites = { "giga_tech_war_system_3" }
	weight = @ehof_tier7weight1
	prereqfor_desc = {
		hide_prereq_for_desc = ship
		hide_prereq_for_desc = component
		hide_prereq_for_desc = feature
		hide_prereq_for_desc = resource
		custom = { title = "allow_systemcraft_p3"	desc = "desc_systemcraft_p3" }
	}

	weight_modifier = {
		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_war_system_4
		}
	}


	ai_weight = {
		factor = 210000

		# policy_route = systemcraft_route
		# source_object = technology:giga_tech_war_system_4
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_systemcraft_research_priority_ready = yes } }
		modifier = { factor = 4 staid_systemcraft_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 8 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 has_ascension_perk = ap_celestial_printing }
		modifier = { factor = 4 has_technology = giga_tech_war_system_1 }
		modifier = { factor = 5 has_technology = giga_tech_war_system_2 }
		modifier = { factor = 6 has_technology = giga_tech_war_system_3 }
		modifier = { factor = 8 has_technology = giga_tech_war_system_6 }
	}
}


# policy_route = systemcraft_route; source = common/technology/giga_01_physics.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_war_system_5 = {
	cost = @giga_tier7cost3
	area = physics
	tier = 5
	category = { particles }
	is_rare = yes
	prerequisites = { "giga_tech_war_system_4" }
	weight = @giga_tier7weight1
	prereqfor_desc = {
		hide_prereq_for_desc = ship
		hide_prereq_for_desc = component
		hide_prereq_for_desc = feature
		hide_prereq_for_desc = resource
		custom = { title = "allow_systemcraft_p4"	desc = "desc_systemcraft_p4" }
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/militarist_tech_weight_bonus

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_war_system_5
		}
	}


	ai_weight = {
		factor = 230000

		# policy_route = systemcraft_route
		# source_object = technology:giga_tech_war_system_5
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_systemcraft_research_priority_ready = yes } }
		modifier = { factor = 4 staid_systemcraft_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 8 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 has_ascension_perk = ap_celestial_printing }
		modifier = { factor = 4 has_technology = giga_tech_war_system_1 }
		modifier = { factor = 5 has_technology = giga_tech_war_system_2 }
		modifier = { factor = 6 has_technology = giga_tech_war_system_3 }
		modifier = { factor = 8 has_technology = giga_tech_war_system_6 }
	}
}


# policy_route = systemcraft_route; source = common/technology/giga_03_engineering.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_war_system_6 = {
	cost = @giga_tier8cost1
	area = engineering
	tier = 5
	category = { voidcraft }
	is_rare = yes
	prerequisites = { "giga_tech_war_system_5" }
	weight = @giga_tier7weight1

	prereqfor_desc = {
		hide_prereq_for_desc = ship
		hide_prereq_for_desc = component
		hide_prereq_for_desc = feature
		hide_prereq_for_desc = resource
		custom = { title = "header_03_insane"	desc = "header_03_insane_desc" }
		custom = { title = "allow_systemcraft_p5"	desc = "desc_systemcraft_p5" }
	}

	potential = {
		NOT = { has_global_flag = systemcraft_disabled }
	}

	weight_modifier = {
		inline_script = technology/tech_weight_boni/militarist_tech_weight_bonus

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = giga_tech_war_system_6
		}
	}


	ai_weight = {
		factor = 250000

		# policy_route = systemcraft_route
		# source_object = technology:giga_tech_war_system_6
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_systemcraft_research_priority_ready = yes } }
		modifier = { factor = 4 staid_systemcraft_research_priority_ready = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 8 years_passed > 79 }
		modifier = { factor = 12 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 3 has_ascension_perk = ap_celestial_printing }
		modifier = { factor = 4 has_technology = giga_tech_war_system_1 }
		modifier = { factor = 5 has_technology = giga_tech_war_system_2 }
		modifier = { factor = 6 has_technology = giga_tech_war_system_3 }
		modifier = { factor = 8 has_technology = giga_tech_war_system_6 }
	}
}


# policy_route = gigas_special_resource_core; source = common/technology/giga_06_special_project_tech.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_ehof_sentient_tier_1 = {
	area = engineering
	cost = @tier5cost3
	weight = 0
	tier = 5
	category = { industry }
	is_rare = yes
	ai_update_type = all
	modifier = {
		planet_engineers_produces_mult = 0.025
		planet_engineers_upkeep_mult = 0.025
	}
	potential = {
		NOT = { has_global_flag = ehof_disabled }
		OR = {
			AND = {
				any_country = {
					has_technology = tech_ehof_sentient_tier_4
				}
			}
			has_country_flag = ehof_level_1_possible
		}
	}

	ai_weight = {
		factor = 140000

		# policy_route = gigas_special_resource_core
		# source_object = technology:tech_ehof_sentient_tier_1
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_gigas_special_resource_unlock_ready = yes } }
		modifier = { factor = 4 staid_gigas_special_resource_unlock_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 5 years_passed > 79 }
		modifier = { factor = 8 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 has_technology = tech_ehof_sentient_tier_1 }
		modifier = { factor = 4 has_technology = tech_nm_utilization_1 }
		modifier = { factor = 4 has_technology = giga_tech_amb_supertensiles }
	}
}


# policy_route = gigas_special_resource_core; source = common/technology/giga_09_ehof_other.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_nm_utilization_1 = {
	area = physics
	cost = @ehof_tier6cost1
	weight = @giga_tier6weight3
	tier = 5
	is_rare = yes
    category = { particles }
    prerequisites = {
		"tech_u_r_e_t"
		"tech_ssn_det"
		"tech_negative_e_s"
	}

	gateway = ehof

	weight_modifier = {
		modifier = { factor = 0.1	years_passed < 50 }
		modifier = { factor = 2		years_passed > 60 }
		modifier = { factor = 3		years_passed > 70 }
		modifier = { factor = 4		years_passed > 80 }

		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = tech_nm_utilization_1
		}
	}


	ai_weight = {
		factor = 140000

		# policy_route = gigas_special_resource_core
		# source_object = technology:tech_nm_utilization_1
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_gigas_special_resource_unlock_ready = yes } }
		modifier = { factor = 4 staid_gigas_special_resource_unlock_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 5 years_passed > 79 }
		modifier = { factor = 8 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 has_technology = tech_ehof_sentient_tier_1 }
		modifier = { factor = 4 has_technology = tech_nm_utilization_1 }
		modifier = { factor = 4 has_technology = giga_tech_amb_supertensiles }
	}
}


# policy_route = gigas_special_resource_core; source = common/technology/giga_17_alternative_mega_build.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
giga_tech_amb_supertensiles = {
	cost = @tier3cost1
	area = physics
	tier = 1 # we need to be able to draw this potentially from the very start
	category = { field_manipulation }
	prerequisites = {} # notionally behind mega-engineering but prereqs are handled in weights because we need this earlier depending on setup
	weight = @tier3weight1

	potential = { has_global_flag = @giga_amb_flag }

	modifier = {
		country_base_giga_sr_amb_megaconstruction_produces_add = 10
	}

	weight_modifier = {
		# do not draw if
		modifier = { factor = 0
			# none of these are true
			nor = {
				has_technology = tech_starbase_3 # requirement for vanilla early megas
				count_owned_megastructure = { count > 0 limit = { giga_is_wrecked_ship = no } } # if we have any megas we probably need this to upgrade
				has_country_flag = giga_sr_amb_megaconstruction_found # if we found some in the wild we should be able to research it
			}
		}

		modifier = { factor = 0 not = { has_global_flag = @giga_amb_flag }}
	}


	ai_weight = {
		factor = 140000

		# policy_route = gigas_special_resource_core
		# source_object = technology:giga_tech_amb_supertensiles
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_gigas_special_resource_unlock_ready = yes } }
		modifier = { factor = 4 staid_gigas_special_resource_unlock_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 5 years_passed > 79 }
		modifier = { factor = 8 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 4 has_technology = tech_ehof_sentient_tier_1 }
		modifier = { factor = 4 has_technology = tech_nm_utilization_1 }
		modifier = { factor = 4 has_technology = giga_tech_amb_supertensiles }
	}
}


# policy_route = nsc3_capital_hull_route; source = common/technology/nsc_technologies.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_Carrier_1 = {
	cost = @tier4cost1
	area = engineering
	tier = 4
	category = { voidcraft }
	prerequisites = { "tech_battleships" }
	weight = @tier4weight3

	potential = {
		country_uses_bio_ships = no
	}

	gateway = ship

	prereqfor_desc = {
		ship = {
			title = "TECH_UNLOCK_CARRIER_CONSTRUCTION_TITLE"
			desc = "TECH_UNLOCK_CARRIER_CONSTRUCTION_DESC"
		}
	}

	modifier = {
		command_limit_add = 10
		country_naval_cap_add = 20
	}

	weight_modifier = {
		modifier = {
			factor = 10
			any_neighbor_country = { has_technology = tech_Carrier_1 }
		}
	}


	ai_weight = {
		factor = 125000

		# policy_route = nsc3_capital_hull_route
		# source_object = technology:tech_Carrier_1
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }
		modifier = { factor = 4 staid_nsc3_capital_hull_unlock_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 has_technology = tech_Carrier_1 }
		modifier = { factor = 4 has_technology = tech_Dreadnought_1 }
		modifier = { factor = 6 has_technology = tech_Flagship_1 }
		modifier = { factor = 0.5 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }
	}
}


# policy_route = nsc3_capital_hull_route; source = common/technology/nsc_technologies.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_Dreadnought_1 = {
	cost = @tier4cost4
	area = engineering
	tier = 4
	category = { voidcraft }
	prerequisites = { "tech_battleships" }
	weight = @tier4weight3

	potential = {
		country_uses_bio_ships = no
	}

	gateway = ship

	prereqfor_desc = {
		ship = {
			title = "TECH_UNLOCK_DREADNOUGHT_CONSTRUCTION_TITLE"
			desc = "TECH_UNLOCK_DREADNOUGHT_CONSTRUCTION_DESC"
		}
	}

	modifier = {
		command_limit_add = 10
		country_naval_cap_add = 20
	}

	weight_modifier = {
		modifier = {
			factor = 10
			any_neighbor_country = { has_technology = tech_Dreadnought_1 }
		}
	}


	ai_weight = {
		factor = 150000

		# policy_route = nsc3_capital_hull_route
		# source_object = technology:tech_Dreadnought_1
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }
		modifier = { factor = 4 staid_nsc3_capital_hull_unlock_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 has_technology = tech_Carrier_1 }
		modifier = { factor = 4 has_technology = tech_Dreadnought_1 }
		modifier = { factor = 6 has_technology = tech_Flagship_1 }
		modifier = { factor = 0.5 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }
	}
}


# policy_route = nsc3_capital_hull_route; source = common/technology/nsc_technologies.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_Flagship_1 = {
	cost = @tier5cost4
	area = engineering
	tier = 5
	category = { voidcraft }
	is_rare = yes
	weight = @tier5weight3

	potential = {
		country_uses_bio_ships = no
        OR = {
            AND = {
                NOT = { host_has_dlc = "Apocalypse" }
                has_technology = tech_Dreadnought_1
            }
            AND = {
                host_has_dlc = "Apocalypse"
                has_technology = tech_titans
            }
        }
    }

	gateway = ship

	prereqfor_desc = {
		ship = {
			title = "TECH_UNLOCK_FLAGSHIP_CONSTRUCTION_TITLE"
			desc = "TECH_UNLOCK_FLAGSHIP_CONSTRUCTION_DESC"
		}
	}

	modifier = {
		command_limit_add = 50
		country_naval_cap_add = 200
	}

	weight_modifier = {
		modifier = {
			factor = 10
			any_neighbor_country = { has_technology = tech_Flagship_1 }
		}
		inline_script = {
			script = technologies/rare_technologies_weight_modifiers
			TECHNOLOGY = tech_Flagship_1
		}
	}


	ai_weight = {
		factor = 170000

		# policy_route = nsc3_capital_hull_route
		# source_object = technology:tech_Flagship_1
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }
		modifier = { factor = 4 staid_nsc3_capital_hull_unlock_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 has_technology = tech_Carrier_1 }
		modifier = { factor = 4 has_technology = tech_Dreadnought_1 }
		modifier = { factor = 6 has_technology = tech_Flagship_1 }
		modifier = { factor = 0.5 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }
	}
}


# policy_route = nsc3_capital_hull_route; source = common/technology/nsc_technologies.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_heavycarrier_1 = {
	cost = @tier4cost2
	area = engineering
	tier = 4
	category = { voidcraft }
	prerequisites = { "tech_Carrier_1" }
	weight = @tier4weight1

	potential = {
		country_uses_bio_ships = no
	}

	gateway = ship

	prereqfor_desc = {
		ship = {
			title = "TECH_UNLOCK_HEAVYCARRIER_CONSTRUCTION_TITLE"
			desc = "TECH_UNLOCK_HEAVYCARRIER_CONSTRUCTION_DESC"
		}
	}

	weight_modifier = {
		modifier = {
			factor = 10
			any_neighbor_country = { has_technology = tech_heavycarrier_1 }
		}
	}


	technology_swap = {
		name = tech_nsc_space_fauna_strikecraft_2
		inherit_icon = no
		inherit_effects = no

		trigger = {
			is_beastmasters_empire = yes
		}

		modifier = {
			weapon_type_strike_craft_weapon_damage_mult = 0.05
			weapon_type_strike_craft_weapon_fire_rate_mult = 0.05
		}
	}

	ai_weight = {
		factor = 130000

		# policy_route = nsc3_capital_hull_route
		# source_object = technology:tech_heavycarrier_1
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }
		modifier = { factor = 4 staid_nsc3_capital_hull_unlock_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 has_technology = tech_Carrier_1 }
		modifier = { factor = 4 has_technology = tech_Dreadnought_1 }
		modifier = { factor = 6 has_technology = tech_Flagship_1 }
		modifier = { factor = 0.5 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }
	}
}


# policy_route = nsc3_capital_hull_route; source = common/technology/nsc_technologies.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_supercarrier_1 = {
	cost = @tier4cost3
	area = engineering
	tier = 4
	category = { voidcraft }
	prerequisites = { "tech_heavycarrier_1" }
	weight = @tier4weight1

	potential = {
		country_uses_bio_ships = no
	}

	gateway = ship

	prereqfor_desc = {
		hide_prereq_for_desc = component
		ship = {
			title = "TECH_UNLOCK_SUPERCARRIER_CONSTRUCTION_TITLE"
			desc = "TECH_UNLOCK_SUPERCARRIER_CONSTRUCTION_DESC"
		}
	}

	weight_modifier = {
		modifier = {
			factor = 10
			any_neighbor_country = { has_technology = tech_supercarrier_1 }
		}
	}


	technology_swap = {
		name = tech_nsc_space_fauna_strikecraft_3
		inherit_icon = no
		inherit_effects = no

		trigger = {
			is_beastmasters_empire = yes
		}

		modifier = {
			weapon_type_strike_craft_weapon_damage_mult = 0.05
			weapon_type_strike_craft_weapon_fire_rate_mult = 0.05
		}
	}

	ai_weight = {
		factor = 145000

		# policy_route = nsc3_capital_hull_route
		# source_object = technology:tech_supercarrier_1
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }
		modifier = { factor = 4 staid_nsc3_capital_hull_unlock_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 has_technology = tech_Carrier_1 }
		modifier = { factor = 4 has_technology = tech_Dreadnought_1 }
		modifier = { factor = 6 has_technology = tech_Flagship_1 }
		modifier = { factor = 0.5 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }
	}
}


# policy_route = esc_component_route; source = common/technology/esc_technology_req_components.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
esc_tech_dark_matter_power_core_2 = {
	area = physics
	category = { particles }
	tier = 6
	cost = @ESC_TECH_tier6_cost1
	weight = @ESC_TECH_tier6_weight1
	prerequisites = { "tech_dark_matter_power_core" }
	ai_update_type = all
	is_rare = yes
	gateway = ESC_REACTORS

	technology_swap = {
		name = esc_tech_dark_matter_power_core_2_bio
		inherit_icon = no
		inherit_effects = yes
		trigger = { country_uses_bio_ships = yes }
		weight = { factor = 1 }
	}

	prereqfor_desc = {
		hide_prereq_for_desc = component
		custom = {
			title = "ESC_TECH_UNLOCK_DM_REACTOR_2_TITLE"
			desc = "ESC_TECH_UNLOCK_DM_REACTOR_2_DESC"
		}
	}

	potential = {
		NOT = { has_global_flag = ESC_GLOBAL_FLAG_reactors_forbidden }
	}

	weight_modifier = {
		modifier = {
			factor = 0
			has_global_flag = @ACOT_active_flag
		}
		modifier = {
			factor = 1.25
			OR = {
				has_ethic = ethic_materialist
				has_ethic = ethic_fanatic_materialist
			}
		}
		modifier = {
			factor = @ESC_TECH_Technology_Ascendancy_weight_modifier
			has_ascension_perk = ap_technological_ascendancy
		}
		modifier = {
			factor = @federation_perk_factor
			has_federation = yes
			federation = {
				has_federation_perk = rare_tech_boost
				any_member = { has_technology = esc_tech_dark_matter_power_core_2 }
			}
		}
	}


	ai_weight = {
		factor = 150000

		# policy_route = esc_component_route
		# source_object = technology:esc_tech_dark_matter_power_core_2
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_esc_component_unlock_ready = yes } }
		modifier = { factor = 4 staid_esc_component_unlock_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 has_technology = esc_tech_dark_matter_power_core_2 }
		modifier = { factor = 3 has_technology = esc_tech_strikecraft_5 }
		modifier = { factor = 4 has_technology = esc_tech_dreadnought_computer }
		modifier = { factor = 0.25 NOT = { staid_advanced_component_resource_support_ready = yes } }
	}
}


# policy_route = esc_component_route; source = common/technology/esc_technology_strikecraft.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
esc_tech_strikecraft_5 = {
	area = engineering
	category = { voidcraft }
	tier = 5
	cost = @tier5cost3
	weight = @tier5weight3
	ai_update_type = military
	prerequisites = { "esc_tech_strikecraft_4" }
	is_rare = yes

	potential = {
		country_uses_bio_ships = no # bioship empires have access only amoeba-based strikecraft
		NOT = { has_global_flag = ESC_GLOBAL_FLAG_adv_vanilla_strikecrafts_forbidden }
	}

	weight_modifier = {
		modifier = {
			factor = @ESC_TECH_Technology_Ascendancy_weight_modifier
			has_ascension_perk = ap_technological_ascendancy
		}
		modifier = {
			factor = @federation_perk_factor
			has_federation = yes
			federation = {
				has_federation_perk = rare_tech_boost
				any_member = { has_technology = esc_tech_strikecraft_5 }
			}
		}
	}


	ai_weight = {
		factor = 140000

		# policy_route = esc_component_route
		# source_object = technology:esc_tech_strikecraft_5
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_esc_component_unlock_ready = yes } }
		modifier = { factor = 4 staid_esc_component_unlock_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 has_technology = esc_tech_dark_matter_power_core_2 }
		modifier = { factor = 3 has_technology = esc_tech_strikecraft_5 }
		modifier = { factor = 4 has_technology = esc_tech_dreadnought_computer }
		modifier = { factor = 0.25 NOT = { staid_advanced_component_resource_support_ready = yes } }
	}
}


# policy_route = esc_component_route; source = common/technology/esc_technology_req_components.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
esc_tech_dreadnought_computer = {
	area = physics
	category = { computing }
	tier = 4
	cost = @tier4cost2
	weight = @tier4weight2
	ai_update_type = all
	prerequisites = { "tech_cruisers" }
	is_rare = yes
	is_reverse_engineerable = no

	prereqfor_desc = {
		hide_prereq_for_desc = component
		custom = {
			title = "ESC_TECH_UNLOCK_DREADNOUGHT_COMPUTER_TITLE"
			desc = "ESC_TECH_UNLOCK_DREADNOUGHT_COMPUTER_DESC"
		}
	}

	potential = {
		NOT = { has_global_flag = ESC_GLOBAL_FLAG_dreadnought_tech_forbidden }
	}

	weight_modifier = {
		modifier = {
			factor = 0	### event tech
		}
	}

	ai_weight = {
		factor = 130000

		# policy_route = esc_component_route
		# source_object = technology:esc_tech_dreadnought_computer
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_esc_component_unlock_ready = yes } }
		modifier = { factor = 4 staid_esc_component_unlock_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 3 has_technology = esc_tech_dark_matter_power_core_2 }
		modifier = { factor = 3 has_technology = esc_tech_strikecraft_5 }
		modifier = { factor = 4 has_technology = esc_tech_dreadnought_computer }
		modifier = { factor = 0.25 NOT = { staid_advanced_component_resource_support_ready = yes } }
	}
}


# policy_route = fallen_empire_benchmark_route; source = common/technology/sbx_3_0_technologies.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tech_starbase_6 = {
	cost = @tier5cost2
	area = engineering
	tier = 5
	category = { voidcraft }
	prerequisites = { "tech_starbase_5" }
	weight = @tier5weight2
	prereqfor_desc = {
		ship = {
			title = "TECH_UNLOCK_STRONGHOLD_CONSTRUCTION_TITLE"
			desc = "TECH_UNLOCK_STRONGHOLD_CONSTRUCTION_DESC"
		}
	}
	weight_modifier = {
		modifier = { factor = 10 any_neighbor_country = { has_technology = tech_starbase_6 } }
	}

	potential = {
		is_nomadic = no
	}


	ai_weight = {
		factor = 135000

		# policy_route = fallen_empire_benchmark_route
		# source_object = technology:tech_starbase_6
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_static_defense_investment_ready = yes } }
		modifier = { factor = 4 staid_static_defense_investment_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

```

## mods/StellarAIDirector/common/traditions/zzzz_staid_02_perks_traditions_traditions.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.
# Required source-local @variables are copied into this file to preserve parent parse context.
# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.

# Generated surface: common/traditions


# policy_route = conquest_escape_route; source = common/traditions/00_supremacy.txt; parent_ai = parent_ai_absent; source_ai_weight = no
tr_supremacy_adopt = {
	unlocks_agenda = agenda_military_buildup
	modifier = {
		country_naval_cap_add = 20
		army_damage_mult = 0.20
	}

	ai_weight = {
		factor = 90000

		# policy_route = conquest_escape_route
		# source_object = tradition:tr_supremacy_adopt
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_aggressive_fleet_pressure = yes } }
		modifier = { factor = 4 staid_aggressive_fleet_pressure = yes }
		modifier = { factor = 4 years_passed > 44 }
		modifier = { factor = 7 years_passed > 79 }
		modifier = { factor = 11 years_passed > 119 }
		modifier = { factor = 4 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
		modifier = { factor = 10 staid_site_limited_expansion_ready = yes }
		modifier = { factor = 5 staid_fleet_buildup_economy_safe = yes }
		modifier = { factor = 8 staid_militarist_conquest_strategy = yes }
		modifier = { factor = 6 has_ethic = ethic_militarist }
		modifier = { factor = 12 has_ethic = ethic_fanatic_militarist }
	}
}


# policy_route = economy_megastructure_core; source = common/traditions/00_prosperity.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tr_prosperity_adopt = {
	unlocks_agenda = agenda_favored_society
	modifier = {
		station_gatherers_produces_mult = 0.20
	}

	tradition_swap = {
		name = tr_prosperity_adopt_nomad
		inherit_icon = yes
		trigger = {
			is_nomadic = yes
			is_eager_explorer_empire = no
		}
		modifier = {
			arkship_harvest_resources_produces_mult = 0.10
			starbase_stockpile_capacity_mult = 0.25
			shipsize_nomads_constructor_stockpile_capacity_mult = 0.25
		}
		weight = {
			factor = 1
		}
	}

	tradition_swap = {
		name = tr_prosperity_adopt_nomad_eager_explorer
		inherit_icon = yes
		inherit_effects = no
		trigger = {
			is_nomadic = yes
			is_eager_explorer_empire = yes
		}
		modifier = {
			arkship_harvest_resources_produces_mult = 0.10
			starbase_stockpile_capacity_mult = 0.25
			shipsize_nomads_constructor_stockpile_capacity_mult = 0.25
			shipsize_nomads_engineer_vessel_stockpile_capacity_mult = 0.25
		}
		weight = {
			factor = 1
		}
	}

	ai_weight = {
		factor = 85000

		# policy_route = economy_megastructure_core
		# source_object = tradition:tr_prosperity_adopt
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_core_unlock_research_priority_ready = yes } }
		modifier = { factor = 4 staid_core_unlock_research_priority_ready = yes }
		modifier = { factor = 3 years_passed > 44 }
		modifier = { factor = 5 years_passed > 79 }
		modifier = { factor = 8 years_passed > 119 }
		modifier = { factor = 3 years_passed < 30 }
		modifier = { factor = 2 AND = { years_passed > 29 years_passed < 60 } }
	}
}


# policy_route = crowded_tall_route; source = common/traditions/00_adaptability.txt; parent_ai = parent_ai_absent; source_ai_weight = no
tr_adaptability_adopt = {
	unlocks_agenda = agenda_conquer_nature
	triggered_modifier = {
		potential = {
			is_wilderness_empire = no
		}
		pop_housing_usage_mult = -0.10
	}

	triggered_modifier = {
		potential = {
			is_wilderness_empire = yes
		}
		building_time_mult = -0.10
	}

	ai_weight = {
		factor = 75000

		# policy_route = crowded_tall_route
		# source_object = tradition:tr_adaptability_adopt
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 4 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}


# policy_route = crowded_tall_route; source = common/traditions/00_mercantile.txt; parent_ai = parent_ai_partial; source_ai_weight = yes
tr_mercantile_adopt = {
	unlocks_agenda = agenda_open_markets
	modifier = {
		planet_traders_upkeep_mult = -0.2
	}

	tradition_swap = {
		name = tr_mercantile_nomads_adopt
		inherit_icon = yes
		inherit_name = yes
		trigger = {
			is_nomadic = yes
		}
		modifier = {
			planet_traders_upkeep_mult = -0.1
			nomadic_contract_value_mult = 0.15
		}
		weight = {
			factor = 1
		}
	}

	ai_weight = {
		factor = 65000

		# policy_route = crowded_tall_route
		# source_object = tradition:tr_mercantile_adopt
		modifier = { factor = 0 staid_survival_mode = yes }
		modifier = { factor = 0.35 staid_recovery_mode = yes }
		modifier = { factor = 0 NOT = { staid_planetary_capacity_growth_ready = yes } }
		modifier = { factor = 4 staid_planetary_capacity_growth_ready = yes }
		modifier = { factor = 2 years_passed > 44 }
		modifier = { factor = 3 years_passed > 79 }
		modifier = { factor = 5 years_passed > 119 }
		modifier = { factor = 5 years_passed < 30 }
		modifier = { factor = 3 AND = { years_passed > 29 years_passed < 60 } }
		modifier = { factor = 2 AND = { years_passed > 59 years_passed < 100 } }
	}
}

```

## mods/StellarAIDirector/descriptor.mod

```text
version="0.1.0"
tags={
	"Gameplay"
	"Balance"
	"AI"
}
name="Stellar AI Director"
supported_version="v4.4.*"
dependencies={
	"Stellar AI"
	"Gigastructural Engineering & More (4.4)"
	"NSC3"
	"Extra Ship Components NEXT"
	"Starbase Extended 3.0"
	"!!!Universal Resource Patch [2.4+]"
}
```

## mods/StellarAIDirector/events/zzz_staid_load_proof_events.txt

```text
namespace = staid_load_proof

country_event = {
	id = staid_load_proof.1
	title = staid_load_proof.1.name
	desc = staid_load_proof.1.desc
	picture = GFX_evt_grand_speech
	show_sound = event_default
	is_triggered_only = yes
	fire_only_once = yes

	trigger = {
		is_ai = no
	}

	immediate = {
		log = "STELLAR_AI_DIRECTOR_LOAD_PROOF: Stellar AI Director v1 loaded for [Root.GetName]"
	}

	option = {
		name = staid_load_proof.1.a
	}
}
```

## mods/StellarAIDirector/events/zzz_staid_market_and_fleet_safety_events.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Uses vanilla `set_mia = mia_return_home` only after a two-pulse stranded-fleet gate.

namespace = staid_economy_safety

event = {
	id = staid_economy_safety.1
	hide_window = yes
	is_triggered_only = yes

	immediate = {
		every_country = {
			limit = {
				is_ai = yes
				is_nomadic = no
				OR = {
					is_regular_empire = yes
					is_gestalt = yes
					is_hive_empire = yes
					is_virtual_empire = yes
					is_galvanic_empire = yes
				}
			}
			country_event = { id = staid_economy_safety.2 }
			country_event = { id = staid_economy_safety.3 }
		}
	}
}

country_event = {
	id = staid_economy_safety.2
	hide_window = yes
	is_triggered_only = yes

	immediate = {
		if = {
			limit = {
				NOT = { has_deficit = minerals }
				has_monthly_income = { resource = minerals value > 0 }
				resource_stockpile_compare = { resource = minerals value > 50000 }
			}
			set_variable = {
				which = staid_market_trade_value
				value = value:stellarai_market_sell_value|RESOURCE|minerals|AMOUNT|5000|
			}
			if = {
				limit = { check_variable = { which = staid_market_trade_value value > 0 } }
				add_resource = { minerals = -5000 }
				add_resource = { trade = 1 mult = staid_market_trade_value }
			}
			clear_variable = staid_market_trade_value
		}

		if = {
			limit = {
			country_uses_food = yes
				NOT = { has_deficit = food }
				has_monthly_income = { resource = food value > 0 }
				resource_stockpile_compare = { resource = food value > 30000 }
			}
			set_variable = {
				which = staid_market_trade_value
				value = value:stellarai_market_sell_value|RESOURCE|food|AMOUNT|5000|
			}
			if = {
				limit = { check_variable = { which = staid_market_trade_value value > 0 } }
				add_resource = { food = -5000 }
				add_resource = { trade = 1 mult = staid_market_trade_value }
			}
			clear_variable = staid_market_trade_value
		}

		if = {
			limit = {
			country_uses_consumer_goods = yes
				NOT = { has_deficit = consumer_goods }
				has_monthly_income = { resource = consumer_goods value > 0 }
				resource_stockpile_compare = { resource = consumer_goods value > 30000 }
			}
			set_variable = {
				which = staid_market_trade_value
				value = value:stellarai_market_sell_value|RESOURCE|consumer_goods|AMOUNT|2500|
			}
			if = {
				limit = { check_variable = { which = staid_market_trade_value value > 0 } }
				add_resource = { consumer_goods = -2500 }
				add_resource = { trade = 1 mult = staid_market_trade_value }
			}
			clear_variable = staid_market_trade_value
		}

		if = {
			limit = {
				NOT = { has_deficit = volatile_motes }
				has_monthly_income = { resource = volatile_motes value > 0 }
				resource_stockpile_compare = { resource = volatile_motes value > 800 }
			}
			set_variable = {
				which = staid_market_trade_value
				value = value:stellarai_market_sell_value|RESOURCE|volatile_motes|AMOUNT|200|
			}
			if = {
				limit = { check_variable = { which = staid_market_trade_value value > 0 } }
				add_resource = { volatile_motes = -200 }
				add_resource = { trade = 1 mult = staid_market_trade_value }
			}
			clear_variable = staid_market_trade_value
		}

		if = {
			limit = {
				NOT = { has_deficit = exotic_gases }
				has_monthly_income = { resource = exotic_gases value > 0 }
				resource_stockpile_compare = { resource = exotic_gases value > 800 }
			}
			set_variable = {
				which = staid_market_trade_value
				value = value:stellarai_market_sell_value|RESOURCE|exotic_gases|AMOUNT|200|
			}
			if = {
				limit = { check_variable = { which = staid_market_trade_value value > 0 } }
				add_resource = { exotic_gases = -200 }
				add_resource = { trade = 1 mult = staid_market_trade_value }
			}
			clear_variable = staid_market_trade_value
		}

		if = {
			limit = {
				NOT = { has_deficit = rare_crystals }
				has_monthly_income = { resource = rare_crystals value > 0 }
				resource_stockpile_compare = { resource = rare_crystals value > 800 }
			}
			set_variable = {
				which = staid_market_trade_value
				value = value:stellarai_market_sell_value|RESOURCE|rare_crystals|AMOUNT|200|
			}
			if = {
				limit = { check_variable = { which = staid_market_trade_value value > 0 } }
				add_resource = { rare_crystals = -200 }
				add_resource = { trade = 1 mult = staid_market_trade_value }
			}
			clear_variable = staid_market_trade_value
		}

		if = {
			limit = {
				NOT = { has_deficit = sr_dark_matter }
				has_monthly_income = { resource = sr_dark_matter value > 0 }
				resource_stockpile_compare = { resource = sr_dark_matter value > 1000 }
			}
			set_variable = {
				which = staid_market_trade_value
				value = value:stellarai_market_sell_value|RESOURCE|sr_dark_matter|AMOUNT|100|
			}
			if = {
				limit = { check_variable = { which = staid_market_trade_value value > 0 } }
				add_resource = { sr_dark_matter = -100 }
				add_resource = { trade = 1 mult = staid_market_trade_value }
			}
			clear_variable = staid_market_trade_value
		}

		if = {
			limit = {
				NOT = { has_deficit = sr_zro }
				has_monthly_income = { resource = sr_zro value > 0 }
				resource_stockpile_compare = { resource = sr_zro value > 1000 }
			}
			set_variable = {
				which = staid_market_trade_value
				value = value:stellarai_market_sell_value|RESOURCE|sr_zro|AMOUNT|100|
			}
			if = {
				limit = { check_variable = { which = staid_market_trade_value value > 0 } }
				add_resource = { sr_zro = -100 }
				add_resource = { trade = 1 mult = staid_market_trade_value }
			}
			clear_variable = staid_market_trade_value
		}

		if = {
			limit = {
				NOT = { has_deficit = nanites }
				has_monthly_income = { resource = nanites value > 0 }
				resource_stockpile_compare = { resource = nanites value > 1000 }
			}
			set_variable = {
				which = staid_market_trade_value
				value = value:stellarai_market_sell_value|RESOURCE|nanites|AMOUNT|100|
			}
			if = {
				limit = { check_variable = { which = staid_market_trade_value value > 0 } }
				add_resource = { nanites = -100 }
				add_resource = { trade = 1 mult = staid_market_trade_value }
			}
			clear_variable = staid_market_trade_value
		}

		if = {
			limit = {
			has_technology = tech_ehof_sentient_tier_1
				NOT = { has_deficit = giga_sr_sentient_metal }
				has_monthly_income = { resource = giga_sr_sentient_metal value > 0 }
				resource_stockpile_compare = { resource = giga_sr_sentient_metal value > 2500 }
			}
			set_variable = {
				which = staid_market_trade_value
				value = value:stellarai_market_sell_value|RESOURCE|giga_sr_sentient_metal|AMOUNT|250|
			}
			if = {
				limit = { check_variable = { which = staid_market_trade_value value > 0 } }
				add_resource = { giga_sr_sentient_metal = -250 }
				add_resource = { trade = 1 mult = staid_market_trade_value }
			}
			clear_variable = staid_market_trade_value
		}

	}
}

country_event = {
	id = staid_economy_safety.3
	hide_window = yes
	is_triggered_only = yes

	immediate = {
		if = {
			limit = {
				staid_homeland_under_attack = yes
			}
			every_owned_fleet = {
				limit = {
					can_go_mia = yes
					is_fleet_idle = yes
					is_in_combat = no
					fleet_power > 1000
					solar_system = {
						exists = space_owner
						space_owner = { NOT = { is_same_value = root } }
					}
				}
				if = {
					limit = { has_fleet_flag = staid_stranded_fleet_warning }
					remove_fleet_flag = staid_stranded_fleet_warning
					set_mia = mia_return_home
				}
				else = {
					set_timed_fleet_flag = {
						flag = staid_stranded_fleet_warning
						days = 70
					}
				}
			}
		}
		else = {
			every_owned_fleet = {
				limit = { has_fleet_flag = staid_stranded_fleet_warning }
				remove_fleet_flag = staid_stranded_fleet_warning
			}
		}
	}
}
```

## mods/StellarAIDirector/events/zzz_staid_threat_response_events.txt

```text
# Generated by tools/generate_stellar_ai_director_patch.py.
# Source of truth: tools/stellar_ai_director_lib.py threat-response tables.

namespace = staid_tr

country_event = {
	id = staid_tr.1
	hide_window = yes
	is_triggered_only = yes
	trigger = {
		staid_tr_attacker_war_leader = yes
		staid_tr_war_goal_classified = yes
	}
	immediate = {
		if = {
			limit = { staid_tr_is_subjugation_war_goal = yes }
			set_timed_country_flag = { flag = staid_tr_war_goal_subjugation days = 7200 }
		}
		else_if = {
			limit = { staid_tr_is_conquest_war_goal = yes }
			set_timed_country_flag = { flag = staid_tr_war_goal_conquest days = 7200 }
		}
		else_if = {
			limit = { staid_tr_is_humiliation_war_goal = yes }
			set_timed_country_flag = { flag = staid_tr_war_goal_humiliation days = 7200 }
		}
		from = {
			random_defender = {
				save_event_target_as = staid_tr_victim
			}
		}
		every_country = {
			limit = {
				is_country_type = default
				NOT = { is_same_value = root }
				has_communications = root
			}
			country_event = { id = staid_tr.2 }
		}
	}
}

country_event = {
	id = staid_tr.2
	hide_window = yes
	is_triggered_only = yes
	trigger = {
		staid_tr_observer_eligible = yes
		staid_tr_awareness_known = yes
	}
	immediate = {
		remove_opinion_modifier = { who = from modifier = staid_tr_anti_aggressor_low }
		remove_opinion_modifier = { who = from modifier = staid_tr_anti_aggressor_medium }
		remove_opinion_modifier = { who = from modifier = staid_tr_anti_aggressor_high }
		remove_opinion_modifier = { who = from modifier = staid_tr_anti_aggressor_severe }
		remove_opinion_modifier = { who = from modifier = staid_tr_alignment_low }
		remove_opinion_modifier = { who = from modifier = staid_tr_alignment_medium }
		remove_opinion_modifier = { who = from modifier = staid_tr_alignment_high }
		if = {
			limit = { from = { has_country_flag = staid_tr_war_goal_subjugation } }
			add_opinion_modifier = { who = from modifier = staid_tr_anti_aggressor_high }
			set_timed_relation_flag = { who = from flag = staid_tr_anti_aggressor_high days = 7200 }
		}
		else_if = {
			limit = { from = { has_country_flag = staid_tr_war_goal_conquest } }
			add_opinion_modifier = { who = from modifier = staid_tr_anti_aggressor_medium }
			set_timed_relation_flag = { who = from flag = staid_tr_anti_aggressor_medium days = 7200 }
		}
		else_if = {
			limit = { from = { has_country_flag = staid_tr_war_goal_humiliation } }
			add_opinion_modifier = { who = from modifier = staid_tr_anti_aggressor_low }
			set_timed_relation_flag = { who = from flag = staid_tr_anti_aggressor_low days = 7200 }
		}
		if = {
			limit = { exists = event_target:staid_tr_victim }
			add_opinion_modifier = { who = event_target:staid_tr_victim modifier = staid_tr_shared_threat_low }
			set_timed_relation_flag = { who = event_target:staid_tr_victim flag = staid_tr_shared_threat_low days = 7200 }
		}
		if = {
			limit = { staid_tr_foreign_affairs_safe = yes }
			set_timed_country_flag = { flag = staid_tr_defensive_readiness_low days = 7200 }
		}
	}
}
```

## mods/StellarAIDirector/localisation/english/staid_load_proof_l_english.yml

```yaml
﻿l_english:
 staid_load_proof.1.name:0 "Stellar AI Director Loaded"
 staid_load_proof.1.desc:0 "Stellar AI Director v1 is loaded in this playset. If this message appears after starting a new game, the mod's startup proof event, event file, on-action connector, and localization are active."
 staid_load_proof.1.a:0 "Confirmed."
```

## mods/StellarAIDirector/localisation/english/staid_threat_response_l_english.yml

```yaml
﻿l_english:
 staid_tr_anti_aggressor_low:0 "Concerned by Aggression"
 staid_tr_anti_aggressor_low_desc:0 "This empire is reacting to an observed classified war."
 staid_tr_anti_aggressor_medium:0 "Condemns Aggression"
 staid_tr_anti_aggressor_medium_desc:0 "This empire is reacting to an observed classified war."
 staid_tr_anti_aggressor_high:0 "Alarmed by Aggression"
 staid_tr_anti_aggressor_high_desc:0 "This empire is reacting to an observed classified war."
 staid_tr_anti_aggressor_severe:0 "Sees Existential Aggression"
 staid_tr_anti_aggressor_severe_desc:0 "This empire is reacting to an observed classified war."
 staid_tr_shared_threat_low:0 "Shared Threat"
 staid_tr_shared_threat_low_desc:0 "This empire is reacting to an observed classified war."
 staid_tr_shared_threat_medium:0 "Shared Strategic Threat"
 staid_tr_shared_threat_medium_desc:0 "This empire is reacting to an observed classified war."
 staid_tr_shared_threat_high:0 "Shared Existential Threat"
 staid_tr_shared_threat_high_desc:0 "This empire is reacting to an observed classified war."
 staid_tr_alignment_low:0 "Respects Conquest"
 staid_tr_alignment_low_desc:0 "This empire is reacting to an observed classified war."
 staid_tr_alignment_medium:0 "Strategic Alignment"
 staid_tr_alignment_medium_desc:0 "This empire is reacting to an observed classified war."
 staid_tr_alignment_high:0 "Strong Strategic Alignment"
 staid_tr_alignment_high_desc:0 "This empire is reacting to an observed classified war."
```

## mods/StellarAIDirector/notes/conflicts.md

```markdown
# Stellar AI Director Conflict Notes

## Intentional Conflicts

- `common/ai_budget/zzz_staid_alloys_budget.txt` intentionally replaces the upstream `alloys_expenditure_megastructures` object so late-game megastructure reserves obey Director survival, recovery, prep, and commit gates.
- `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` intentionally replaces upstream Gigas special-resource megastructure budget objects: `sentient_metal_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, and `supertensiles_upkeep_megastructures`.
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt` intentionally replaces `basic_economy_plan` with Director high-scale survival economy, mandatory modded unlock research, trade-capacity, fleet-throughput, static-defense, and planetary-capacity targets; despite the historical filename, conflict review must treat it as a Director-owned economic-plan surface.
- `common/technology/zzzz_staid_01_unlock_technology_technology.txt` intentionally replaces copied vanilla/Gigas/NSC3/ESC/Starbase Extended technology objects with Director route AI weights.
- `common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt` and `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` intentionally replace copied AP/tradition objects with Director route AI weights.
- `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` intentionally replaces copied Gigas/vanilla-compatible megastructure starts for economy multipliers, Mega Shipyard, planetcraft, war moon, and systemcraft priority.
- `common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt` intentionally replaces copied ESC starbase reactor support with Director crisis-starbase pressure.
- `common/buildings/zzzz_staid_06_research_infrastructure_buildings.txt` intentionally replaces copied Stellar AI research lab, institute, supercomputer, and archaeostudies objects with Director research-throughput construction coefficients while preserving parent rare-resource guards.
- `common/districts/zzzz_staid_06_research_infrastructure_districts.txt` intentionally replaces copied vanilla `district_hab_science` with Director crowded-tall habitat research construction weight.

## Expected Additive Surfaces

- `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`
- `common/script_values/zzz_staid_roi_values.txt`
- `common/scripted_triggers/zzz_staid_threat_response_triggers.txt`
- `common/script_values/zzz_staid_threat_response_values.txt`
- `common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt`
- `events/zzz_staid_market_and_fleet_safety_events.txt`
- `common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`
- `common/on_actions/zzz_staid_threat_response_on_actions.txt`
- `events/zzz_staid_threat_response_events.txt`
- `localisation/english/staid_threat_response_l_english.yml`

## Threat-Response Boundaries

- V1 threat response is diplomacy/readiness pressure only.
- Unknown or unclassified war goals are inert until manually classified and tested.
- Generated threat-response files must not declare wars, join wars, add casus belli, or override diplomatic actions.
- Third-party readiness economy pressure must remain behind `staid_tr_foreign_affairs_safe`.

## NSC3/ESC Design Policy

- NSC3 and ESC unlock technologies now have copied source-object route AI weights.
- Fleet-throughput economy gates provide the current ship-use path without guessing direct ship-design templates.
- ESC internal component-template `key = ...` overrides and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.

## Review Rules

- Any new full-object override must include an ownership note naming the parent surface and reason.
- Optional-mod references must be omitted or guarded unless the generator proves the referenced object exists.
- Irony conflict results should be classified as intentional Director wins, parent wins required, harmless additive duplicates, unexpected gameplay conflicts, or false positives.

## Irony Analyze Only Review

- Reviewed in Irony Conflict Solver Analyze Only for collection `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`.
- Existing collection order was preserved; `Stellar AI Director` is the only added local mod and is last after `!!!Universal Resource Patch [2.4+]`.
- Reviewed `common\ai_budget` conflicts: `alloys_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, `sentient_metal_expenditure_megastructures`, and `supertensiles_upkeep_megastructures`.
- Each reviewed object resolves to `Stellar AI Director ... (LIOS)` as an intentional Director win.
- No unexplained Director gameplay conflicts were observed in the reviewed Director conflict set.
```

## mods/StellarAIDirector/notes/load-order.md

```markdown
# Stellar AI Director Load Order

Selected collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity
Required parent maximum load position: 115

## Required Position

- Load after Stellar AI.
- Load after Gigastructural Engineering & More (4.4).
- Load after NSC3.
- Load after Extra Ship Components NEXT.
- Load after Starbase Extended 3.0.
- Load after !!!Universal Resource Patch [2.4+].
- Load after parent compatibility patches whose AI/economy behavior the Director intentionally coordinates.
- Load before any future local patch that intentionally overrides the Director.

## Required Parent Evidence

| mod | present | load position |
| --- | --- | ---: |
| Stellar AI | True | 115 |
| Gigastructural Engineering & More (4.4) | True | 62 |
| NSC3 | True | 71 |
| Extra Ship Components NEXT | True | 70 |
| Starbase Extended 3.0 | True | 72 |

## Current Intentional Supersession

- `common/ai_budget/zzz_staid_alloys_budget.txt` intentionally overrides Stellar AI's `alloys_expenditure_megastructures` budget.
- `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` intentionally overrides Gigas `sentient_metal_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, and `supertensiles_upkeep_megastructures` budgets.
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt` intentionally replaces `basic_economy_plan` with Director high-scale survival economy, mandatory modded unlock research, trade-capacity, fleet-throughput, static-defense, and planetary-capacity targets.
- Additive scripted triggers, script values, and economic-plan subplans use the `staid_` namespace and should not conflict with parent object IDs.
```

## mods/StellarAIDirector/notes/observer-test-log.md

```markdown
# Stellar AI Director Observer Test Log

Selected collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity

## Repeatable Setup

- Galaxy size: Tiny Irony-launched smoke save.
- AI count: inferred from save country count (66 initialized countries).
- Difficulty: Cadet smoke setup from launch run notes.
- Crisis settings: inherited selected playset defaults for the smoke save.
- Mod order evidence: required parents are recorded in `notes/load-order.md`; save mod list contains 117 mods.

## Checkpoints

- Early economy stability: short-smoke pass from `stellar-ai-director-observer-smoke-save-summary-2026-07-04.md`.
- First mega-engineering unlock: pending.
- First high-ROI megastructure start: pending.
- First economy multiplier completion: pending.
- Shipyard/fleet payoff behavior: pending.
- Deficit spiral check: no early deficit collapse observed in parsed 2202.01.01 save metrics.
- War interruption behavior: pending.
- Starbase defense investment: pending.

## Threat-Response Checkpoints

- Classified aggressive war deterministic contract: covered by generated tests and validator.
- Threat-response generated files emitted after 2026-07-05 implementation: covered by file audit and validator.
- Unknown/modded war goal inertness: covered by classification data, tests, and validator.
- No forced wars, join-war behavior, or punitive CBs: covered by forbidden-effect tests and validator.
- Runtime launch observation: intentionally out of scope for this deterministic implementation goal.

## Results

Short Irony-launched save summary: `stellar-ai-director-observer-smoke-save-summary-2026-07-04.md`.

- Save date: 2202.07.01.
- Director listed in save mod list: True.
- Short smoke passes: True.
- Player metrics: `{"economy_power": 540.44128, "empire_size": 51.0, "fleet_size": 15.0, "navy_coverage": 0.58823, "num_sapient_pops": 5276.0, "tech_power": 277.5, "used_naval_capacity": 15.0}`.
- Player monthly income: `{"alloys": 15.2, "consumer_goods": 62.602, "energy": 166.524, "engineering_research": 16.728, "food": 119.737, "influence": 4.176, "minerals": 68.246, "physics_research": 21.228, "society_research": 16.728, "trade": 152.165, "unity": 43.527}`.
- High-ROI path observed: False.

This short-smoke evidence is retained as historical context. P15 runtime/observer validation is superseded for this deterministic implementation goal; generated artifacts, tests, validators, and indexed evidence are the acceptance gate.
```

## mods/StellarAIDirector/notes/tuning-notes.md

```markdown
# Stellar AI Director Tuning Notes

Generated thresholds are derived from decision-eligible, resolved ROI rows.

| knob | current value | intent |
| --- | ---: | --- |
| prep stockpile alloys | 15000 | minimum reserve before new megastructure prep |
| prep income alloys | 130 | minimum monthly alloy income for prep |
| commit stockpile alloys | 27000 | reserve for continuing safe projects |
| shipyard stockpile alloys | 12000 | reserve before shipyard payoff exploitation |
| shipyard income alloys | 150 | monthly alloy floor for fleet-production sink |
| fleet buildup stockpile energy | 8000 | energy runway before shipyard/fleet sink can add naval-cap pressure |
| trade capacity income floor | 25 | minimum monthly trade before generic expansion gates are considered safe |
| fleet trade capacity income floor | 75 | minimum monthly trade before fleet-throughput and payoff gates add logistics pressure |
| planetary trade capacity income floor | 50 | minimum monthly trade before planetary-capacity and megastructure-prep gates add logistics pressure |
| surplus trade capacity income floor | 100 | minimum monthly trade before surplus sink pressure can activate |
| fleet buildup naval cap ceiling | 1.05 | stop pushing fleet payoff when naval usage is already above target |
| strategic value horizon year | 2350 | long-lived economic, military, and modifier payoffs are weighted by remaining months before this goal date |
| static-defense stockpile alloys | 3000 | minimum reserve before country-level starbase defense economy target |
| static-defense income alloys | 60 | monthly alloy floor for defensive starbase reserve |
| crisis starbase threat | 50 | threat floor that can activate crisis starbase reserve |
| planetary-capacity stockpile minerals | 5000 | mineral runway before expanded planet/building capacity target activates |
| planetary-capacity stockpile energy | 5000 | energy runway before expanded planet/building capacity target activates |
| planetary-capacity pops target | 400000 | high-scale pop target used by the country-level tall-growth capacity subplan |
| market cap-breaker minerals reserve | 50000 | sell large positive-income mineral overflow before caps void income |
| market cap-breaker food/consumer goods reserve | 30000 | sell large positive-income food/CG overflow while preserving large buffers |
| market cap-breaker strategic reserve | 800-2500 | sell marketable strategic overflow only above high reserves |
| stranded fleet warning duration | 70 days | require a second monthly proof before forcing vanilla MIA return-home |
| threat response relation flag days | 7200 | duration for observer/aggressor and observer/victim threat state |
| threat response economy ratio cap | 20 | maximum share of fleet-throughput reserve available to third-party threat readiness |
| threat readiness alloys cap | 7 | maximum added alloys target from third-party threat readiness |
| threat readiness energy cap | 6 | maximum added energy target from third-party threat readiness |
| threat readiness naval cap | 40 | maximum added naval-cap target from third-party threat readiness |
| eligible ROI rows | 140 | source sample used for threshold generation |

## Static-Defense Policy

- Defensive or high-threat empires get additive starbase reserve subplans only after recovery and short-runway deficit gates are clear.
- Aggressive under-cap empires keep fleet expansion priority unless crisis pressure is high.
- The generated ESC starbase reactor override adds direct crisis-starbase AI weight support; other starbase modules/buildings remain manual-review candidates.

## Trade-Capacity Policy

- Trade is modeled as Stellaris 4.4 logistics/capacity headroom, not as a normal priced ROI resource.
- The generated `basic_economy_plan` includes trade reserve and trade recovery subplans so the Director's full-object replacement keeps trade logistics visible while pushing beyond vanilla/Stellar AI scale.
- Fleet, planetary, megastructure, static-defense, and surplus gates require trade income floors before adding more ship, colony, or resource-imbalance upkeep pressure.

## Market Cap-Breaker Policy

- Capped stockpile waste is treated as an economic emergency, not harmless savings.
- The monthly cap breaker sells only large positive-income overflow for marketable resources with verified market pricing or parent market-value support.
- Alloys, energy, unity, Gigas negative mass, and Gigas megaconstruction are excluded from forced sale because they are strategic reserves or not safely market-priced in source files.

## Fleet-Throughput Policy

- Mega Shipyard readiness becomes an economic-plan subplan only when alloy income, energy income, trade income, alloy stockpile, and energy stockpile are all safe.
- Fleet payoff exploitation is blocked while over-naval-cap upkeep spirals are likely (`used_naval_capacity_percent >= 1.05`).
- Research sink remains first when the Mega Shipyard unlock is missing because `staid_shipyard_expansion_ready` requires `tech_mega_shipyard`.
- Militarist conquest, raiding-pop acquisition, and early hostile-fauna clearance now have separate fleet reserve lanes; military empires are not forced to wait for peaceful surplus-only fleet spending.
- User-directed 2026-07-08 aggression tuning keeps local war aggression above vanilla (`AI_AGGRESSIVENESS_BASE = 50`) but restores vanilla distance penalty (`WAR_DECLARATION_MALUS = 0.05`) and caps war declaration range at 200 jumps to avoid inefficient galaxy-crossing wars.
- Raiding empires prioritize `ap_nihilistic_acquisition`, raiding bombardment, and no-surrender bombardment posture when their setup supports abducting pops as a growth strategy.
- Hostile space fauna clearance is tracked as a dedicated follow-up lane: cheap crystalline/amoeba/drone-style blockers should be cleared early for territory, resources, and event research, while high-risk leviathan targets need separate classification.

## Unlock-Research Policy

- The unlock-research policy is mandatory survival pressure after the opening curve, not a surplus-only luxury; it keeps physics, society, engineering, and unity pressure on until core Mega Engineering, Mega Shipyard, Gigas, NSC3, and ESC unlock paths are reachable.
- Direct technology/AP/tradition route overrides are emitted from copied source objects and trace back to the policy matrix and route override report.

## Mega/Giga Build Priority Policy

- ROI-ready megastructure and gigastructure rows are mapped through generated alloy, special-resource, and economy-plan gates.
- Generated full-object route overrides now cover Dyson Sphere, Mega Shipyard, neutronium gigaforge, Nidavellir forge, Matrioshka brain, planetcraft printer, war moon, and systemcraft starts; generated files preserve parent `@variable` parse context and remove absent optional `pc_magnetar` compatibility references.
- Exotic projects outside those route starts remain inventoried until the core loop is observer-tested against the high-scale crisis benchmark.

## Planetary-Capacity Policy

- Expanded planet/building capacity is covered through a country-level economic-plan subplan once mineral, energy, and trade logistics runway are safe.
- The generated subplan uses supported `pops` and income targets only; do not emit `empire_size`, which Stellaris 4.4.5 rejects in active economic-plan files.
- Direct research infrastructure overrides now cover copied Stellar AI research labs and the habitat science district; broad job automation rewrites remain a required follow-up when a specific missing parent surface is proven.
- Planetary Diversity outpost decisions are copied into generated decision overrides with Director-owned weights for moon, mining, food, energy, and research outposts; the research family strongly favors the capital because the opening strategy treats the capital as the first research hub.
- Planetary Diversity decision availability owns tech, site, and button prerequisites. Director weights do not duplicate those checks; if the button is available and the mineral/energy runway is safe, the AI is pushed to use the matching outpost.
- Permanent and long-lived scaling investments use a 2350 horizon: the same outpost, building, tech, megastructure, or buff is worth far more in 2220 than in 2320 because every remaining year multiplies its payoff.
- Planetary Diversity static modifiers, deposits, and buildings are classified into generated role triggers (`staid_pd_planet_*_value`) so planet specialization can react to research, alloy, mineral, energy, food, trade, unity, growth, and defense value instead of treating PD planets as generic colonies.

## NSC3/ESC Design Policy

- NSC3 and ESC unlock technologies now have copied source-object route AI weights and are paired with fleet-throughput economy gates.
- ESC internal component-template `key = ...` overrides and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.

## Threat-Response Policy

- V1 reacts only to explicitly classified war goals: `wg_conquest`, `wg_subjugation`, and `wg_humiliation`.
- Unknown or unclassified war goals are inert: no punitive opinion, no shared-threat opinion, no alignment opinion, no readiness flag, no economy pressure, no CB, and no forced war.
- Design axes such as moral outrage and regional fear remain generator-owned; runtime files consume only generated values, triggers, flags, events, and opinion modifiers.
- Third-party defensive-readiness economy pressure is gated by `staid_tr_foreign_affairs_safe`, requires no survival/recovery/deficit/war state, and is capped at 20% of the existing fleet-throughput reserve.
- Directly attacked empires remain owned by vanilla/Stellar AI/Director war and survival behavior, not the third-party threat economy path.

## Stranded-Fleet Recovery Policy

- The Director does not attempt normal movement/pathfinding orders from script.
- Idle, out-of-combat, MIA-eligible AI fleets outside their owner's space are marked only while `staid_homeland_under_attack` is true.
- A marked fleet must still satisfy the same stranded gate on a later monthly pulse before `set_mia = mia_return_home` fires.
- The gate is intended for post-war access/pocket failures where a strong fleet is trapped away from a collapsing homeland, not for active offensive fleets.

## Safe Tuning Rules

- Do not lower prep or commit reserves below survival/recovery safety gates.
- Keep research sink before fleet sink until core modded unlocks are available.
- Treat unpriced resources and trade logistics as bottlenecks, not fake scalar value.
- Re-run generator, validator, unit tests, and coverage after every tuning change.
```
