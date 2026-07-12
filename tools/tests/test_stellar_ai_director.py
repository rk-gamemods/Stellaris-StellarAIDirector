import csv
import json
import re
import tempfile
import unittest
from unittest import mock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stellar_ai_director_lib import (
    AI_SUPPORT_MAP_CSV,
    DEPENDENCY_EDGES_CSV,
    ECONOMIC_VALUATION_DATASET_CSV,
    ECONOMIC_VALUATION_DATASET_MD,
    ECONOMIC_VALUATION_EVIDENCE_MD,
    ECONOMIC_VALUATION_CANONICAL_COLUMNS,
    ECONOMIC_VALUATION_SOURCE_FACT_COLUMNS,
    BUILD_PLAN_CONSUMER_POLICY_CSV,
    EmpireState,
    GENERATED_VERSION_INVENTORY_MD,
    MANUAL_STATIC_VALIDATION_MD,
    MARKET_CAP_BREAKER_SALES,
    MOD_ROOT,
    MOD_STACK_COMPATIBILITY_MD,
    OBJECT_ATLAS_CSV,
    POLICY_MATRIX_CSV,
    RESEARCH_ROOT,
    RELATIVE_ECONOMIC_STANDARDS_CSV,
    RELATIVE_ECONOMIC_STANDARDS_MD,
    ROUTE_OVERRIDE_TARGETS,
    SNAPSHOT_ROOT,
    STANDALONE_PARITY_INVENTORY_CSV,
    STANDALONE_PARITY_INVENTORY_MD,
    STRATEGIC_SUBSYSTEM_AUDIT_CSV,
    STRATEGIC_SUBSYSTEM_AUDIT_MD,
    SFT_EQUIVALENCE_AUDIT_CSV,
    SFT_EQUIVALENCE_AUDIT_MD,
    STELLARAI_INLINE_SCRIPT_DEPENDENCIES,
    STANDALONE_AGGRESSION_PERSONALITY_VALUES,
    THREAT_OPINION_VALUES,
    WAR_PLANNING_444_PROVENANCE_CSV,
    STELLARIS_INSTALL_ROOT,
    _collect_job_adds,
    _economic_subplan_block,
    append_child_block_clause,
    ai_budget_text,
    atlas_object_has_ai_signal,
    block_assignments,
    block_contains_assignment,
    collect_generated_conflict_rows,
    collect_generated_file_audit_rows,
    collect_generated_reference_rows,
    collect_object_names,
    collect_variables,
    economic_valuation_evidence_passes,
    economic_valuation_dataset_passes,
    economic_plan_text,
    build_plan_consumer_policy_buildings,
    build_plan_consumer_policy_rows,
    build_plan_consumer_policy_selected_objects,
    build_economic_valuation_dataset,
    dataset_job_pressure_override_rows,
    dataset_ai_resource_production_amounts,
    dataset_job_pressure_family,
    dataset_job_pressure_weight_block,
    director_ai_weight_block,
    extract_assignment_block,
    extract_top_level_object_text,
    extract_megastructure_rows,
    fleet_alloy_budget_text,
    fresh_economic_valuation_source_facts,
    gigas_habitat_ai_weight_block,
    generated_unresolved_at_variable_rows,
    generated_thresholds,
    generate_mod_files,
    generated_colony_root_scope_errors,
    generate_object_atlas_artifacts,
    build_plan_consumer_policy_allows_dataset_object,
    build_plan_consumer_policy_selected_object_rows,
    mod_source_root_for_id,
    NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV,
    NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_MD,
    nonconstruction_economic_valuation_dataset_passes,
    nomad_waystation_budget_text,
    outpost_budget_text,
    parse_file,
    parse_numeric,
    parse_pdx,
    remove_top_level_child_block,
    resource_waste_pressure,
    research_under_curve,
    route_weight_modifiers,
    route_override_evidence_rows,
    route_override_generated_file_path,
    relative_economic_standard_rows,
    read_text,
    repair_gigas_habitat_spawn_effect_params,
    forbidden_generated_surface_errors,
    stale_stellar_ai_dependency_errors,
    surplus_sink_pressure,
    strategic_subsystem_audit_rows,
    triggers_text,
    validate_staid_scripted_trigger_cycles,
    validate_generated_patch,
    validate_object_atlas_artifacts,
    validate_threat_response_contract,
    write_text_file_preserving_generated_timestamp,
)


class ActiveStackEconomicValuationMaintenanceTests(unittest.TestCase):
    def test_job_slot_collection_distinguishes_planet_and_country_modifier_contexts(self):
        parsed = parse_pdx(
            """
            building_source_audit = {
                triggered_country_modifier = {
                    job_capital_trader_add = 200
                }
                triggered_planet_modifier = {
                    job_researcher_add = 100
                }
            }
            """
        )
        building = block_assignments(parsed, "building_source_audit")[0].value

        jobs, missing = _collect_job_adds(building, {})

        self.assertEqual(missing, set())
        self.assertNotIn("job_capital_trader", jobs)
        self.assertEqual(jobs["job_researcher"], 100.0)

    def test_job_slot_collection_ignores_scripted_modifier_job_add_keys(self):
        parsed = parse_pdx(
            """
            building_source_audit = {
                triggered_planet_modifier = {
                    job_healthcare_add = 100
                    job_healthcare_amenities_add = 100
                }
            }
            """
        )
        building = block_assignments(parsed, "building_source_audit")[0].value

        jobs, missing = _collect_job_adds(building, {}, {"job_healthcare_amenities_add"})

        self.assertEqual(missing, set())
        self.assertEqual(jobs, {"job_healthcare": 100.0})

    def test_generated_economic_values_match_current_active_mod_files(self):
        dataset_rows = []
        for path in (ECONOMIC_VALUATION_DATASET_CSV, NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV):
            with path.open("r", encoding="utf-8", newline="") as handle:
                dataset_rows.extend(list(csv.DictReader(handle)))

        fresh_facts = fresh_economic_valuation_source_facts(dataset_rows)
        drift_rows = []
        missing_rows = []
        for row in dataset_rows:
            object_key = (row["object_type"], row["object_id"])
            if row["object_type"] not in {
                "ascension_perk",
                "building",
                "colony_type",
                "decision",
                "deposit",
                "district",
                "edict",
                "policy",
                "pop_job",
                "resource",
                "starbase_building",
                "starbase_module",
                "technology",
                "tradition",
                "zone",
            }:
                continue
            actual = fresh_facts.get(object_key)
            if actual is None:
                missing_rows.append(f"{row['object_type']} `{row['object_id']}` expected at {row['winning_file']}")
                continue
            for column in ECONOMIC_VALUATION_SOURCE_FACT_COLUMNS:
                expected_value = str(row.get(column, ""))
                actual_value = str(actual.get(column, ""))
                if expected_value != actual_value:
                    drift_rows.append(
                        f"{row['object_type']} `{row['object_id']}` column `{column}` drifted: "
                        f"dataset={expected_value[:240]} current={actual_value[:240]} "
                        f"(dataset file {row['winning_file']}, current file {actual.get('winning_file', 'unknown')})"
                    )
                    break

        details = "\n".join([*missing_rows[:25], *drift_rows[:25]])
        overflow = len(missing_rows) + len(drift_rows) - 25
        if overflow > 0:
            details += f"\n... {overflow} more drift rows omitted"
        self.assertFalse(
            missing_rows or drift_rows,
            "Active mod economic source drift detected. Re-run the Stellar AI Director generator after reviewing the changed "
            "mod files; do not hand-edit the generated values.\n"
            + details,
        )


class RouteOverrideUnitTests(unittest.TestCase):
    def test_nihilistic_acquisition_is_not_a_generic_route_target(self):
        self.assertNotIn(
            "ap_nihilistic_acquisition",
            {target["object_id"] for target in ROUTE_OVERRIDE_TARGETS},
        )

    def test_gigas_habitat_route_preserves_parent_scoring_without_global_deadlock(self):
        target = next(
            target
            for target in ROUTE_OVERRIDE_TARGETS
            if target["mod_id"] == "1121692237"
            and target["object_type"] == "megastructure"
            and target["object_id"] == "habitat_central_complex"
        )

        active_gigas_path = Path(
            r"C:\Steam\steamapps\workshop\content\281990\1121692237\common\megastructures\zz_b_habitats.txt"
        )
        active_parent = extract_top_level_object_text(
            active_gigas_path.read_text(encoding="utf-8-sig"),
            "habitat_central_complex",
        )
        text = gigas_habitat_ai_weight_block(active_parent, target)
        parse_pdx(text)

        def factor_zero_modifier_values(container_text, root_key):
            parsed = parse_pdx(container_text)
            root_value = block_assignments(parsed, root_key)[0].value
            ai_weight = (
                root_value
                if root_key == "ai_weight"
                else block_assignments(root_value, "ai_weight")[0].value
            )
            return {
                repr(assignment.value)
                for assignment in block_assignments(ai_weight, "modifier")
                if block_contains_assignment(assignment.value, "factor", "0")
            }

        active_parent_vetoes = factor_zero_modifier_values(
            active_parent, "habitat_central_complex"
        )
        generated_vetoes = factor_zero_modifier_values(
            text, "habitat_central_complex"
        )

        self.assertEqual(target["weight"], 5)
        self.assertEqual(len(active_parent_vetoes), 3)
        self.assertEqual(len(generated_vetoes), 2)
        self.assertIn("ai_weight = {\n        factor = 5", text)
        self.assertIn("factor = 100", text)
        self.assertIn("factor = value:num_orbital_sites", text)
        for marker in (
            "has_country_flag = has_recently_built_habitat",
            "starbase = { NOT = { has_starbase_size >= starbase_starport } }",
        ):
            self.assertIn(marker, active_parent)
            self.assertIn(marker, text)
        self.assertNotIn("any_planet_within_border", text)
        self.assertNotIn("factor = 125000", text)
        self.assertNotIn("years_passed >", text)
        self.assertIn("factor = 0.1", text)
        self.assertIn("ai_colonize_plans > 0", text)
        self.assertIn("factor = 2", text)
        self.assertIn("staid_planetary_capacity_growth_ready = yes", text)

    def test_gigas_habitat_route_fails_on_parent_deadlock_gate_drift(self):
        target = next(
            target
            for target in ROUTE_OVERRIDE_TARGETS
            if target["mod_id"] == "1121692237"
            and target["object_type"] == "megastructure"
            and target["object_id"] == "habitat_central_complex"
        )
        parent_path = Path(
            r"C:\Steam\steamapps\workshop\content\281990\1121692237\common\megastructures\zz_b_habitats.txt"
        )
        parent = extract_top_level_object_text(
            parent_path.read_text(encoding="utf-8-sig"),
            "habitat_central_complex",
        ).replace("is_colony = no", "is_colony = yes", 1)

        with self.assertRaisesRegex(ValueError, "uncolonized-habitat veto"):
            gigas_habitat_ai_weight_block(parent, target)


RESEARCH_CAPACITY_BUILDINGS_CSV = RESEARCH_ROOT / "stellar-ai-director-research-capacity-buildings-2026-07-09.csv"
RESEARCH_CAPACITY_JOBS_CSV = RESEARCH_ROOT / "stellar-ai-director-research-capacity-jobs-2026-07-09.csv"
RESEARCH_CAPACITY_DEVELOPMENT_CSV = RESEARCH_ROOT / "stellar-ai-director-research-capacity-development-2026-07-09.csv"
RESEARCH_CAPACITY_PLAN_CSV = RESEARCH_ROOT / "stellar-ai-director-research-capacity-plan-2026-07-09.csv"
RESEARCH_CAPACITY_INFRASTRUCTURE_CSV = RESEARCH_ROOT / "stellar-ai-director-strategic-infrastructure-targets-2026-07-09.csv"
RESEARCH_CAPACITY_RESOURCE_COVERAGE_CSV = RESEARCH_ROOT / "stellar-ai-director-modeling-resource-coverage-2026-07-09.csv"
RESEARCH_CAPACITY_READINESS_CSV = RESEARCH_ROOT / "stellar-ai-director-build-plan-readiness-2026-07-09.csv"
RESEARCH_CAPACITY_BENEFITS_CSV = RESEARCH_ROOT / "stellar-ai-director-strategic-benefit-taxonomy-2026-07-09.csv"
RESEARCH_CAPACITY_BLOCKERS_CSV = RESEARCH_ROOT / "stellar-ai-director-modeling-blocker-accounting-2026-07-09.csv"
RESEARCH_CAPACITY_CONSUMER_POLICY_CSV = RESEARCH_ROOT / "stellar-ai-director-build-plan-consumer-policy-2026-07-09.csv"
RESEARCH_CAPACITY_ROLES_CSV = RESEARCH_ROOT / "stellar-ai-director-colony-role-targets-2026-07-09.csv"
GIGAS_MODELED_RESOURCE_KEYS = {
    "giga_sr_negative_mass",
    "giga_sr_amb_megaconstruction",
    "giga_sr_iodizium",
    "giga_sr_sentient_metal",
}
REQUIRED_STRATEGIC_BENEFIT_CLASSES = {
    "pop_growth_assembly",
    "migration_resettlement",
    "trade_policy_value",
    "amenities",
    "stability",
    "housing",
    "habitability",
    "planet_capacity",
    "crime_deviancy_control",
    "defense_armies",
    "bombardment_resistance",
    "naval_capacity",
    "shipyard_throughput",
    "starbase_support",
    "diplomacy_envoys",
    "research_speed",
    "empire_country_modifier",
    "megastructure_construction",
    "blocker_district_capacity",
    "direct_resource_support",
}
REQUIRED_EXPANDED_ROLE_FAMILIES = {
    "capital_world",
    "habitat_growth_center",
    "habitat_support_center",
    "ring_world",
    "arcology_world",
    "frameworld",
    "birch_world",
    "gigas_special_world",
}


class NativeOwnershipRegressionTests(unittest.TestCase):
    def test_safety_layer_never_issues_scripted_fleet_orders(self):
        on_action_path = MOD_ROOT / "common" / "on_actions" / "zzz_staid_market_and_fleet_safety_on_actions.txt"
        event_path = MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt"
        parse_file(on_action_path)
        parse_file(event_path)
        text = event_path.read_text(encoding="utf-8")
        self.assertIn("id = staid_economy_safety.2", text)
        self.assertNotIn("id = staid_economy_safety.4", text)
        for marker in (
            "staid_economy_safety.3",
            "staid_stranded_fleet_warning",
            "set_mia =",
            "set_fleet_order =",
            "set_fleet_stance =",
            "move_to =",
        ):
            self.assertNotIn(marker, text)


class HabitatRecoveryRegressionTests(unittest.TestCase):
    def test_generated_habitat_preserves_parent_bounds_without_global_empty_habitat_veto(self):
        path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        parse_file(path)
        block = extract_top_level_object_text(
            path.read_text(encoding="utf-8-sig"),
            "habitat_central_complex",
        )
        target = next(
            target
            for target in ROUTE_OVERRIDE_TARGETS
            if target["mod_id"] == "1121692237"
            and target["object_type"] == "megastructure"
            and target["object_id"] == "habitat_central_complex"
        )
        parent_path = Path(
            r"C:\Steam\steamapps\workshop\content\281990\1121692237\common\megastructures\zz_b_habitats.txt"
        )
        parent = extract_top_level_object_text(
            parent_path.read_text(encoding="utf-8-sig"),
            "habitat_central_complex",
        )
        expected = gigas_habitat_ai_weight_block(
            repair_gigas_habitat_spawn_effect_params(parent, target),
            target,
        )
        self.assertEqual(block.strip(), expected.strip())

        for marker in (
            "ai_weight = {\n        factor = 5",
            "has_country_flag = has_recently_built_habitat",
            "starbase = { NOT = { has_starbase_size >= starbase_starport } }",
            "factor = 100",
            "factor = value:num_orbital_sites",
            "factor = 0.1",
            "ai_colonize_plans > 0",
            "factor = 2",
            "staid_planetary_capacity_growth_ready = yes",
            "count <= value:ai_habitat_cap",
            "on_build_queued = {",
            "on_build_unqueued = {",
            "on_build_cancel = {",
        ):
            self.assertIn(marker, block)
        for marker in (
            "factor = 125000",
            "any_planet_within_border",
            "staid_survival_mode",
            "staid_recovery_mode",
            "years_passed >",
        ):
            self.assertNotIn(marker, block)

        route_csv = RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.csv"
        with route_csv.open(newline="", encoding="utf-8-sig") as handle:
            route_row = next(
                row
                for row in csv.DictReader(handle)
                if row["object_id"] == "habitat_central_complex"
            )
        self.assertEqual(route_row["weight"], "5")

class AlloyBudgetOwnershipTests(unittest.TestCase):
    def test_generic_megastructure_alloy_budget_remains_parent_owned(self):
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzz_staid_alloys_budget.txt"
        parse_file(budget_path)
        artifact = budget_path.read_text(encoding="utf-8")
        generated = ai_budget_text({})

        for text in (artifact, generated):
            self.assertNotRegex(text, r"(?m)^alloys_expenditure_megastructures\s*=")
            self.assertIn("alloys_expenditure_ships = {", text)
            self.assertIn("alloys_expenditure_ship_upgrades = {", text)
            self.assertIn("upstream/parent-owned", text)
        self.assertEqual(artifact, generated)


class OutpostBudgetAvailabilityTests(unittest.TestCase):
    def test_colonization_plan_count_does_not_latch_outpost_budgets(self):
        budget_path = (
            MOD_ROOT / "common" / "ai_budget" / "zzz_staid_outpost_budgets.txt"
        )
        parse_file(budget_path)
        artifact = budget_path.read_text(encoding="utf-8")
        generated = outpost_budget_text()
        vanilla_alloy = extract_top_level_object_text(
            read_text(
                STELLARIS_INSTALL_ROOT
                / "common"
                / "ai_budget"
                / "00_alloys_budget.txt"
            ),
            "alloys_expenditure_starbases_expand",
        )
        expected_alloy_potential = extract_assignment_block(
            vanilla_alloy, "potential"
        ).replace("\t\tNOT = {\n", "\t\tNOR = {\n", 1).replace(
            "\t\t\tai_colonize_plans > 0\n", "", 1
        ).replace("\t\thighest_threat < 50\n", "", 1)
        expected_alloy_weight = extract_assignment_block(vanilla_alloy, "weight")
        vanilla_food = extract_top_level_object_text(
            read_text(
                STELLARIS_INSTALL_ROOT / "common" / "ai_budget" / "00_food_budget.txt"
            ),
            "food_expenditure_starbases_expand",
        )
        expected_food_potential = extract_assignment_block(
            vanilla_food, "potential"
        ).replace("\t\t\t\tai_colonize_plans > 0\n", "", 1).replace(
            "\t\thighest_threat < 50\n", "", 1
        )
        expected_food_weight = extract_assignment_block(vanilla_food, "weight")
        threat_modifier = (
            "\n\t\tmodifier = {\n"
            "\t\t\tfactor = 0.5\n"
            "\t\t\thighest_threat >= 50\n"
            "\t\t}\n"
        )
        expected_alloy_weight = expected_alloy_weight.replace(
            "\n\t}", threat_modifier + "\t}", 1
        )
        expected_food_weight = expected_food_weight.replace(
            "\n\t}", threat_modifier + "\t}", 1
        )

        for text in (artifact, generated):
            alloy = extract_top_level_object_text(
                text, "alloys_expenditure_starbases_expand"
            )
            food = extract_top_level_object_text(
                text, "food_expenditure_starbases_expand"
            )
            for outpost, desired_min in ((alloy, "150"), (food, "300")):
                potential = extract_assignment_block(outpost, "potential")
                weight = extract_assignment_block(outpost, "weight")
                self.assertIn("has_ai_expansion_plan = yes", potential)
                self.assertNotIn("highest_threat < 50", potential)
                self.assertIn("is_country_type = fallen_empire", potential)
                self.assertIn("is_country_type = awakened_fallen_empire", potential)
                self.assertIn(
                    "has_resource = { type = influence amount > 75 }", potential
                )
                self.assertNotIn("ai_colonize_plans", potential)
                self.assertIn("NOR = {", potential)
                self.assertIn("weight = 0.2", weight)
                self.assertIn("factor = 0.5", weight)
                self.assertIn("highest_threat >= 50", weight)
                self.assertNotIn("factor = 0.25", weight)
                self.assertNotIn("ai_colonize_plans", weight)
                self.assertIn(f"base = {desired_min}", outpost)
                self.assertNotIn("clear_orders", outpost)

            self.assertIn("factor = 0.5", extract_assignment_block(alloy, "weight"))
            self.assertIn("country_uses_bio_ships = yes", alloy)
            self.assertIn("country_uses_bio_ships = yes", food)
            self.assertIn("is_wilderness_empire = yes", food)
            self.assertIn("ai_terraform_plans > 0", food)
            self.assertEqual(
                extract_assignment_block(alloy, "potential"),
                expected_alloy_potential,
            )
            self.assertEqual(
                extract_assignment_block(food, "potential"),
                expected_food_potential,
            )
            self.assertEqual(
                extract_assignment_block(alloy, "weight"),
                expected_alloy_weight,
            )
            self.assertEqual(
                extract_assignment_block(food, "weight"),
                expected_food_weight,
            )
        self.assertEqual(artifact, generated)


class NomadWaystationBudgetAvailabilityTests(unittest.TestCase):
    def test_threat_reduces_but_does_not_disable_waystation_funding(self):
        path = (
            MOD_ROOT
            / "common"
            / "ai_budget"
            / "zzzzz_staid_22_nomad_waystation_budgets.txt"
        )
        parse_file(path)
        artifact = path.read_text(encoding="utf-8")
        self.assertEqual(artifact, nomad_waystation_budget_text())
        object_ids = (
            "influence_expenditure_megastructures_waystations",
            "alloys_expenditure_megastructures_waystations",
            "food_expenditure_megastructures_waystations",
        )
        for object_id in object_ids:
            block = extract_top_level_object_text(artifact, object_id)
            potential = extract_assignment_block(block, "potential")
            weight = extract_assignment_block(block, "weight")
            self.assertIn("is_nomadic = yes", potential)
            self.assertIn("has_technology = tech_waystation_1", potential)
            self.assertNotIn("highest_threat < 50", potential)
            self.assertIn("factor = 0.5", weight)
            self.assertIn("highest_threat >= 50", weight)
            self.assertIn("used_starbase_capacity_percent >= 1", weight)
            self.assertIn("used_starbase_capacity_percent >= 1.25", weight)
            self.assertIn("used_starbase_capacity_percent >= 2.0", weight)
            self.assertNotIn("clear_orders", block)
            self.assertNotIn("build_megastructure", block)
        food = extract_top_level_object_text(
            artifact, "food_expenditure_megastructures_waystations"
        )
        alloys = extract_top_level_object_text(
            artifact, "alloys_expenditure_megastructures_waystations"
        )
        self.assertIn("country_uses_bio_ships = yes", food)
        self.assertIn("country_uses_bio_ships = yes", alloys)


class ClaimPressureExpansionPriorityTests(unittest.TestCase):
    def test_claim_acceleration_requires_no_plan_border_or_boxed_pressure(self):
        trigger_path = (
            MOD_ROOT
            / "common"
            / "scripted_triggers"
            / "zzz_staid_decision_state_triggers.txt"
        )
        claim_budget_path = (
            MOD_ROOT
            / "common"
            / "ai_budget"
            / "zzzz_staid_08_site_limited_expansion_ai_budget.txt"
        )
        parse_file(trigger_path)
        parse_file(claim_budget_path)
        artifact = trigger_path.read_text(encoding="utf-8")
        generated = triggers_text(generated_thresholds(extract_megastructure_rows()))
        self.assertEqual(artifact, generated)

        claim_gate = extract_top_level_object_text(
            artifact, "staid_influence_claim_pressure"
        )
        boxed_gate = extract_top_level_object_text(
            artifact, "staid_boxed_in_claim_urgency"
        )
        for marker in (
            "is_nomadic = no",
            "is_at_war = no",
            "NOT = { has_ethic = ethic_pacifist }",
            "NOT = { has_ethic = ethic_fanatic_pacifist }",
            "has_potential_claims = yes",
            "has_resource = { type = influence amount > 500 }",
            "NOT = { has_ai_expansion_plan = yes }",
            "has_bordering_system = no",
            "NOT = { staid_boxed_in_war_pressure = yes }",
        ):
            self.assertEqual(claim_gate.count(marker), 1)
        self.assertNotIn("amount > 900", claim_gate)
        self.assertNotIn("OR = {", claim_gate)
        self.assertEqual(boxed_gate.count("staid_boxed_in_war_pressure = yes"), 1)

        claim_budget = claim_budget_path.read_text(encoding="utf-8")
        expected_objects = {
            "influence_expenditure_claims": ("0.20", "has_crisis_level = crisis_level_2"),
            "influence_expenditure_claims_militarist": (
                "0.10",
                "has_ethic = ethic_militarist",
            ),
            "influence_expenditure_claims_fanatic_militarist": (
                "0.15",
                "has_ethic = ethic_fanatic_militarist",
            ),
        }
        for object_id, (base_weight, potential_marker) in expected_objects.items():
            block = extract_top_level_object_text(claim_budget, object_id)
            potential = extract_assignment_block(block, "potential")
            weight = extract_assignment_block(block, "weight")
            self.assertIn("is_nomadic = no", potential)
            self.assertIn("has_potential_claims = yes", potential)
            self.assertIn(potential_marker, potential)
            self.assertIn(f"weight = {base_weight}", weight)
            self.assertEqual(
                weight.count(
                    "modifier = { factor = 3 staid_influence_claim_pressure = yes }"
                ),
                1,
            )
            self.assertEqual(
                weight.count(
                    "modifier = { factor = 12 staid_boxed_in_claim_urgency = yes }"
                ),
                1,
            )
            self.assertEqual(
                weight.count(
                    "modifier = { factor = 2 has_resource = { type = influence amount > 900 } }"
                ),
                1,
            )


class EconomicPlanBoundednessTests(unittest.TestCase):
    def test_megastructure_pressure_has_no_global_scaling_spam_target(self):
        plan_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        parse_file(plan_path)
        artifact = plan_path.read_text(encoding="utf-8")
        generated = economic_plan_text()

        for text in (artifact, generated):
            self.assertNotIn("Stellar AI Director megastructure spam reserve", text)
            self.assertIn("Stellar AI Director mega alloy reserve", text)
            self.assertIn("Stellar AI Director giga special resource reserve", text)
        self.assertEqual(artifact, generated)


class ShipBudgetAvailabilityTests(unittest.TestCase):
    def test_ship_budget_stays_available_under_bounded_high_cap_dampening(self):
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzz_staid_alloys_budget.txt"
        parse_file(budget_path)
        artifact = budget_path.read_text(encoding="utf-8")
        ships = extract_top_level_object_text(artifact, "alloys_expenditure_ships")
        generated_ships = extract_top_level_object_text(
            fleet_alloy_budget_text(), "alloys_expenditure_ships"
        )

        for text in (ships, generated_ships):
            self.assertIn("potential = {", text)
            self.assertIn("always = yes", text)
            self.assertIn("weight = 0.6", text)
            self.assertIn("recently_lost_war = yes", text)
            self.assertIn("is_at_war = yes", text)
            self.assertIn("factor = 0.33", text)
            self.assertIn("country_uses_bio_ships = yes", text)
            self.assertIn("factor = 0.25", text)
            self.assertIn("staid_peacetime_high_naval_capacity_guard = yes", text)
            self.assertIn("factor = 1.5", text)
            self.assertIn("add = 5000", text)
            self.assertEqual(text.count("staid_wartime_fleet_surge_ready = yes"), 2)
            self.assertNotIn("NOT = { staid_peacetime_high_naval_capacity_guard = yes }", text)
            self.assertNotIn("staid_fleet_buildup_economy_safe = yes", text)
        self.assertEqual(ships, generated_ships)

    def test_wartime_surge_is_bounded_by_runway_cap_and_capital_hull_tech(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(trigger_path)
        triggers = trigger_path.read_text(encoding="utf-8")
        surge = extract_top_level_object_text(triggers, "staid_wartime_fleet_surge_ready")
        for marker in (
            "is_at_war = yes",
            "country_uses_bio_ships = no",
            "NOT = { staid_catastrophic_collapse_mode = yes }",
            "NOT = { staid_core_deficit_short_runway = yes }",
            "staid_energy_two_month_runway_unsafe = no",
            "staid_alloys_two_month_runway_unsafe = no",
            "used_naval_capacity_percent < 0.90",
            "has_technology = tech_battleships",
            "has_technology = tech_Battlecruiser_1",
            "has_technology = tech_Carrier_1",
            "has_technology = tech_Dreadnought_1",
            "resource_stockpile_compare = { resource = alloys value > 5000 }",
        ):
            self.assertIn(marker, surge)
        for forbidden in ("country_event =", "create_fleet", "create_ship", "set_fleet_order"):
            self.assertNotIn(forbidden, surge)
        self.assertNotIn("staid_wartime_fleet_minimum_mode", triggers)

class ShipUpgradeBudgetAvailabilityTests(unittest.TestCase):
    def test_ship_upgrade_budget_uses_native_eligibility_without_runway_veto(self):
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzz_staid_alloys_budget.txt"
        parse_file(budget_path)
        artifact = budget_path.read_text(encoding="utf-8")
        upgrades = extract_top_level_object_text(artifact, "alloys_expenditure_ship_upgrades")
        generated_upgrades = extract_top_level_object_text(
            fleet_alloy_budget_text(), "alloys_expenditure_ship_upgrades"
        )

        for text in (upgrades, generated_upgrades):
            self.assertIn("weight = 0.2", text)
            self.assertIn("is_at_war = no", text)
            self.assertIn("can_be_upgraded = yes", text)
            self.assertNotIn("staid_fleet_buildup_economy_safe = yes", text)
        self.assertEqual(upgrades, generated_upgrades)


class MegastructureSafetyGateTests(unittest.TestCase):
    def test_large_stockpiles_do_not_bypass_megastructure_safety(self):
        trigger_path = (
            MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        )
        parse_file(trigger_path)
        text = trigger_path.read_text(encoding="utf-8")
        generated = triggers_text(generated_thresholds(extract_megastructure_rows()))
        self.assertEqual(text, generated)
        blocks = {
            name: extract_top_level_object_text(text, name)
            for name in (
                "staid_megastructure_prep_ready",
                "staid_megastructure_commit_safe",
                "staid_megastructure_continuation_priority_ready",
                "staid_pause_new_megastructure",
            )
        }

        for block in blocks.values():
            self.assertNotIn("staid_high_scale_snowball_pressure = yes", block)
        self.assertIn("NOT = { staid_recovery_mode = yes }", blocks["staid_megastructure_prep_ready"])
        self.assertIn("staid_basic_economy_runway_safe = yes", blocks["staid_megastructure_prep_ready"])
        self.assertIn("staid_trade_planetary_capacity_safe = yes", blocks["staid_megastructure_prep_ready"])
        self.assertIn(
            "NOT = { staid_core_deficit_short_runway = yes }",
            blocks["staid_megastructure_commit_safe"],
        )
        self.assertIn(
            "NOT = { staid_survival_mode = yes }",
            blocks["staid_megastructure_continuation_priority_ready"],
        )
        self.assertIn(
            "staid_surplus_sink_pressure = yes",
            blocks["staid_megastructure_continuation_priority_ready"],
        )
        self.assertIn("staid_survival_mode = yes", blocks["staid_pause_new_megastructure"])


class MegastructureRouteHighScaleTests(unittest.TestCase):
    def test_high_scale_wealth_does_not_multiply_megastructure_route_weights(self):
        path = (
            MOD_ROOT
            / "common"
            / "megastructures"
            / "zzzz_staid_03_megastructures_megastructures.txt"
        )
        parse_file(path)
        artifact = path.read_text(encoding="utf-8")
        self.assertNotIn(
            "from = { staid_high_scale_snowball_pressure = yes }",
            artifact,
        )

        megastructure_targets = [
            target for target in ROUTE_OVERRIDE_TARGETS if target["object_type"] == "megastructure"
        ]
        self.assertTrue(megastructure_targets)
        for target in megastructure_targets:
            start_modifiers = "\n".join(route_weight_modifiers(target))
            upgrade_modifiers = "\n".join(
                route_weight_modifiers({**target, "megastructure_stage_kind": "upgrade"})
            )
            self.assertNotIn("staid_high_scale_snowball_pressure", start_modifiers)
            self.assertNotIn("staid_high_scale_snowball_pressure", upgrade_modifiers)

        preserved_technology_target = next(
            target
            for target in ROUTE_OVERRIDE_TARGETS
            if target["object_type"] == "technology"
            and target["route_id"] == "early_kilo_economy_core"
        )
        self.assertIn(
            "staid_high_scale_snowball_pressure",
            "\n".join(route_weight_modifiers(preserved_technology_target)),
        )


class GeneratedModReadOnlyValidationTests(unittest.TestCase):
    def test_checked_artifact_validation_does_not_call_generators(self):
        suite = unittest.TestSuite(
            [GeneratedModValidityTests("test_generated_files_are_valid_load_surfaces")]
        )
        result = unittest.TestResult()
        with (
            mock.patch(f"{__name__}.generate_object_atlas_artifacts") as atlas_generator,
            mock.patch(f"{__name__}.generate_mod_files") as mod_generator,
        ):
            suite.run(result)

        self.assertTrue(result.wasSuccessful(), result.errors + result.failures)
        atlas_generator.assert_not_called()
        mod_generator.assert_not_called()


class GeneratedModValidityTests(unittest.TestCase):
    def test_generated_files_are_valid_load_surfaces(self):
        rows = collect_generated_file_audit_rows(MOD_ROOT)
        self.assertTrue(rows, "No generated mod files were found to validate.")
        bad_rows = [row for row in rows if row["status"] != "ok"]
        self.assertEqual(bad_rows, [])

    def test_wartime_colony_budget_cannot_veto_native_colonization_plans(self):
        path = MOD_ROOT / "common" / "ai_budget" / "zzzzz_staid_19_wartime_colony_alloy_budget.txt"
        text = path.read_text(encoding="utf-8")
        parse_file(path)
        self.assertIn("alloys_expenditure_colonies_expand = {", text)
        self.assertIn("ai_colonize_plans > 0", text)
        self.assertIn("is_nomadic = no", text)
        self.assertNotIn("is_at_war", text)
        self.assertNotIn("staid_wartime_colony_expansion_safe", text)
        self.assertNotIn("mid_game_years_passed", text)

    def test_research_worlds_prioritize_zones_that_unlock_research_labs(self):
        path = MOD_ROOT / "common" / "zones" / "zzzzz_staid_20_research_world_zone_priority.txt"
        self.assertTrue(path.exists(), f"{path} was not generated")
        parse_file(path)
        text = path.read_text(encoding="utf-8")
        for zone_id in (
            "zone_research",
            "zone_research_physics",
            "zone_research_society",
            "zone_research_engineering",
        ):
            block = extract_top_level_object_text(text, zone_id)
            self.assertIn("additional_ai_weight = {", block)
            self.assertIn("add = 5", block)
            self.assertNotIn("add = 100000", block)
            self.assertIn("has_designation = col_research", block)
            self.assertIn("owner = { is_ai = yes }", block)
            self.assertNotIn("convert_to", block)
            self.assertNotIn("destroy_trigger", block)
        vanilla_lab = extract_top_level_object_text(
            (STELLARIS_INSTALL_ROOT / "common" / "buildings" / "05_research_buildings.txt").read_text(
                encoding="utf-8"
            ),
            "building_research_lab_1",
        )
        self.assertIn("has_any_research_zone = yes", vanilla_lab)
        vanilla_city = extract_top_level_object_text(
            (STELLARIS_INSTALL_ROOT / "common" / "districts" / "00_urban_districts.txt").read_text(
                encoding="utf-8"
            ),
            "district_city",
        )
        for slot_id in ("slot_city_government", "slot_city_01", "slot_city_02"):
            self.assertEqual(vanilla_city.count(slot_id), 1)

    def test_descriptor_omits_stellar_ai_dependency_after_standalone_parity(self):
        descriptor = (MOD_ROOT / "descriptor.mod").read_text(encoding="utf-8")
        dependency_block = re.search(r"dependencies=\{\n(?P<body>.*?)\n\}", descriptor, re.DOTALL)
        self.assertIsNotNone(dependency_block)
        self.assertNotIn('"Stellar AI"', dependency_block.group("body"))
        self.assertIn('"Gigastructural Engineering & More (4.4)"', dependency_block.group("body"))
        self.assertIn('"NSC3"', dependency_block.group("body"))

        readme = (MOD_ROOT / "README.md").read_text(encoding="utf-8")
        load_order = (MOD_ROOT / "notes" / "load-order.md").read_text(encoding="utf-8")
        self.assertIn("Stellar AI remains a private parity reference", readme)
        self.assertIn("Stellar AI is not a required parent", load_order)
        self.assertEqual(stale_stellar_ai_dependency_errors(), [])

    def test_generated_docs_preserve_strategic_v2_runtime_gates(self):
        readme = (MOD_ROOT / "README.md").read_text(encoding="utf-8")
        load_order = (MOD_ROOT / "notes" / "load-order.md").read_text(encoding="utf-8")
        conflicts = (MOD_ROOT / "notes" / "conflicts.md").read_text(encoding="utf-8")
        observer_log = (MOD_ROOT / "notes" / "observer-test-log.md").read_text(encoding="utf-8")
        tuning = (MOD_ROOT / "notes" / "tuning-notes.md").read_text(encoding="utf-8")

        self.assertIn("building_navel_base", readme)
        self.assertIn("building_navel_command", readme)
        self.assertIn("Planetary Diversity - More Arcologies", load_order)
        self.assertIn("Strategic V2 Compatibility Reviews", conflicts)
        self.assertIn("Fresh Irony UI review has not yet been repeated", conflicts)
        self.assertIn("Generated starbase pressure is guarded", tuning)
        self.assertIn("Nomad/Arkship Compatibility Policy", tuning)
        self.assertIn("Strategic V2 Observer Checkpoints", observer_log)
        self.assertIn("3,000+ total monthly research before 2350", observer_log)
        self.assertIn("final constrained observer run", observer_log)
        self.assertNotIn("P15 runtime/observer validation is superseded", observer_log)
        self.assertNotIn("acceptance gate", observer_log)

    def test_stale_stellar_ai_dependency_validator_rejects_current_requirements(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            mod_root = root / "StellarAIDirector"
            research_root = root / "research" / "stellar-ai"
            (mod_root / "notes").mkdir(parents=True)
            research_root.mkdir(parents=True)
            (mod_root / "descriptor.mod").write_text(
                'name="Stellar AI Director"\ndependencies={\n\t"Stellar AI"\n}\n',
                encoding="utf-8",
            )
            (mod_root / "README.md").write_text("This mod requires Stellar AI.\n", encoding="utf-8")
            (mod_root / "notes" / "load-order.md").write_text(
                "Stellar AI is not a required parent.\n",
                encoding="utf-8",
            )
            (research_root / "README.md").write_text(
                "Stellar AI remains a private parity reference only.\n",
                encoding="utf-8",
            )

            errors = stale_stellar_ai_dependency_errors(mod_root, research_root)

        self.assertTrue(any("descriptor must not require Stellar AI" in error for error in errors))
        self.assertTrue(any("current docs must not imply Stellar AI is required" in error for error in errors))

    def test_forbidden_surface_validator_blocks_unsafe_generated_folders(self):
        self.assertEqual(forbidden_generated_surface_errors(), [])

        with tempfile.TemporaryDirectory() as temp_dir:
            mod_root = Path(temp_dir) / "StellarAIDirector"
            (mod_root / "common" / "country_types").mkdir(parents=True)
            (mod_root / "common" / "diplomatic_actions").mkdir(parents=True)
            (mod_root / "common" / "component_templates").mkdir(parents=True)
            (mod_root / "common" / "ship_designs").mkdir(parents=True)

            errors = forbidden_generated_surface_errors(mod_root)
            strict_errors = forbidden_generated_surface_errors(mod_root, allowed_surfaces=set())

        self.assertEqual(len(errors), 2)
        self.assertTrue(any("diplomatic_actions" in error for error in errors))
        self.assertTrue(any("ship_designs" in error for error in errors))
        self.assertEqual(len(strict_errors), 4)
        self.assertTrue(any("component_templates" in error for error in strict_errors))
        self.assertTrue(any("country_types" in error for error in strict_errors))

    def test_sft_addon_equivalence_preserves_active_ship_build_logic(self):
        addon_equivalence = (
            MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_sft_addon_equivalence.txt"
        ).read_text(encoding="utf-8")
        role_triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zz_SFTt_SHIP_USE_ROLES.txt").read_text(
            encoding="utf-8"
        )
        design_triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zz_SFTt_SHIP_DESIGN.txt").read_text(
            encoding="utf-8"
        )
        design_refresh_on_action = (
            MOD_ROOT / "common" / "on_actions" / "zzzz_staid_sft_design_refresh_on_actions.txt"
        ).read_text(encoding="utf-8")

        self.assertIn("SFTt_ADDON_NEW_SECTION_USE = { always = no }", addon_equivalence)
        self.assertIn("SFTt_ADDON_COMBAT_COM_REST_REMOVED = { always = yes }", addon_equivalence)
        self.assertIn("SFTt_ADDON_COMBAT_COM_REST_REMOVED = yes", role_triggers)
        self.assertIn("SFTt_ADDON_NEW_SECTION_USE = yes", design_triggers)
        self.assertIn("SFT_event_ship_design.400", design_refresh_on_action)
        self.assertTrue((MOD_ROOT / "common" / "component_templates" / "000_SFT_00_utilities_roles.txt").exists())
        sft_section_files = list((MOD_ROOT / "common" / "section_templates").glob("*SFT*"))
        sft_technology_files = list((MOD_ROOT / "common" / "technology").glob("*SFT*"))
        self.assertEqual(sft_section_files, [])
        self.assertEqual(sft_technology_files, [])

    def test_sft_equivalence_audit_documents_included_and_excluded_surfaces(self):
        self.assertTrue(SFT_EQUIVALENCE_AUDIT_CSV.exists())
        self.assertTrue(SFT_EQUIVALENCE_AUDIT_MD.exists())
        with SFT_EQUIVALENCE_AUDIT_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        targets = {row["target"] for row in rows}
        self.assertIn("common/component_templates/000_SFT_00_utilities_roles.txt", targets)
        self.assertIn("common/on_actions/zzzz_staid_sft_design_refresh_on_actions.txt", targets)
        self.assertFalse(any(target.startswith("common/section_templates/") for target in targets))
        self.assertFalse(any(target.startswith("common/technology/") for target in targets))
        audit_text = SFT_EQUIVALENCE_AUDIT_MD.read_text(encoding="utf-8")
        self.assertIn("Disable New Ship Sections", audit_text)
        self.assertIn("Combat Computer Restriction Removal", audit_text)

    def test_standalone_parity_inventory_covers_baseline_surfaces(self):
        self.assertTrue(STANDALONE_PARITY_INVENTORY_CSV.exists())
        self.assertTrue(STANDALONE_PARITY_INVENTORY_MD.exists())
        with STANDALONE_PARITY_INVENTORY_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        surfaces = {row["surface"] for row in rows}
        for surface in {
            "descriptor_dependencies",
            "common/ai_budget",
            "common/economic_plans",
            "buildings/districts/jobs/zones",
            "colony_types_designations_planet_roles",
            "personalities_diplomacy_war",
            "policies_edicts_defines",
            "research_economy_fleet_conversion",
            "generated_conflict_winners",
            "spacefleet_tactica_ship_build_logic",
            "advanced_ship_design_nsc3_esc_gigas_runtime",
        }:
            self.assertIn(surface, surfaces)
        blocked = {row["surface"] for row in rows if row["classification"] == "defer"}
        self.assertIn("advanced_ship_design_nsc3_esc_gigas_runtime", blocked)
        text = STANDALONE_PARITY_INVENTORY_MD.read_text(encoding="utf-8")
        self.assertIn("private local parity reference", text)
        self.assertIn("not a launch dependency", text)

    def test_generated_references_resolve_to_known_objects(self):
        rows = collect_generated_reference_rows(MOD_ROOT, SNAPSHOT_ROOT)
        self.assertTrue(rows, "No generated references were found to validate.")
        missing_rows = [row for row in rows if row["status"] == "missing"]
        self.assertEqual(missing_rows, [])

    def test_generated_ai_budget_overrides_known_budget_objects(self):
        known_budget_objects = collect_object_names(SNAPSHOT_ROOT)["ai_budget"]
        budget_root = MOD_ROOT / "common" / "ai_budget"
        budget_files = sorted(budget_root.glob("*.txt"))
        self.assertTrue(budget_files, "No generated AI budget files were found.")
        unknown = []
        for file_path in budget_files:
            parsed = parse_file(file_path)
            for assignment in block_assignments(parsed):
                if assignment.key not in known_budget_objects:
                    unknown.append((file_path.relative_to(MOD_ROOT).as_posix(), assignment.key))
        self.assertEqual(unknown, [])

    def test_generated_conflict_rows_ignore_source_local_variables(self):
        rows = collect_generated_conflict_rows(MOD_ROOT, SNAPSHOT_ROOT)
        variable_rows = [row for row in rows if row["object_name"].startswith("@")]
        self.assertEqual(variable_rows, [])
        by_object = {(row["object_type"], row["object_name"]): row for row in rows}
        for object_key in (
            ("building", "building_stronghold"),
            ("building", "building_fortress"),
            ("colony_automation_exception", "giga_rogue_ai_planet"),
            ("colony_type", "col_fortress"),
            ("colony_type", "col_habitat_fortress"),
        ):
            self.assertEqual(by_object[object_key]["parent_has_object"], "yes")
            self.assertEqual(by_object[object_key]["classification"], "intentional_director_override")

    def test_active_stack_economic_valuation_dataset_covers_buildings_zones_and_districts(self):
        artifact_paths = (
            ECONOMIC_VALUATION_DATASET_CSV,
            ECONOMIC_VALUATION_DATASET_MD,
        )
        before = {
            path: (path.read_bytes(), path.stat().st_mtime_ns)
            for path in artifact_paths
        }

        rows = build_economic_valuation_dataset()

        after = {
            path: (path.read_bytes(), path.stat().st_mtime_ns)
            for path in artifact_paths
        }
        self.assertEqual(
            after,
            before,
            "Ordinary validation must not refresh checked economic-valuation artifacts.",
        )
        self.assertTrue(rows)
        self.assertTrue(ECONOMIC_VALUATION_DATASET_CSV.exists())
        self.assertTrue(ECONOMIC_VALUATION_DATASET_MD.exists())
        self.assertTrue(economic_valuation_dataset_passes())

        object_types = {row["object_type"] for row in rows}
        self.assertIn("building", object_types)
        self.assertIn("zone", object_types)
        self.assertIn("district", object_types)

        esc_buildings = [
            row
            for row in rows
            if row["object_type"] == "building" and row["winning_mod_id"] == "2648658105"
        ]
        gigas_objects = [
            row
            for row in rows
            if row["object_type"] in {"building", "district"} and row["winning_mod_id"] == "1121692237"
        ]
        self.assertTrue(esc_buildings, "ESC advanced buildings were not captured.")
        self.assertTrue(gigas_objects, "Gigas advanced buildings or districts were not captured.")
        self.assertTrue(any(float(row["jobs_created_total_estimate"]) > 0 for row in rows))
        self.assertTrue(any(float(row["roi_2250_to_2350_estimate"]) > 0 for row in rows))

    def test_research_capacity_model_reconciles_active_winning_buildings(self):
        with OBJECT_ATLAS_CSV.open("r", encoding="utf-8", newline="") as handle:
            atlas_rows = list(csv.DictReader(handle))
        with RESEARCH_CAPACITY_BUILDINGS_CSV.open("r", encoding="utf-8", newline="") as handle:
            modeled_rows = list(csv.DictReader(handle))

        active_winning_buildings = {
            row["object_id"]
            for row in atlas_rows
            if row["object_type"] == "building" and row["load_winner"] == "yes"
        }
        modeled_buildings = {row["building_id"] for row in modeled_rows}

        self.assertGreaterEqual(len(active_winning_buildings), 600)
        self.assertFalse(
            sorted(active_winning_buildings - modeled_buildings)[:25],
            "Every active-stack winning building must be present in the generated research-capacity model.",
        )

    def test_research_capacity_model_promotes_gigas_resource_columns(self):
        with RESEARCH_CAPACITY_BUILDINGS_CSV.open("r", encoding="utf-8", newline="") as handle:
            buildings_reader = csv.DictReader(handle)
            building_rows = list(buildings_reader)
            building_columns = set(buildings_reader.fieldnames or [])
        with RESEARCH_CAPACITY_DEVELOPMENT_CSV.open("r", encoding="utf-8", newline="") as handle:
            development_reader = csv.DictReader(handle)
            development_rows = list(development_reader)
            development_columns = set(development_reader.fieldnames or [])
        with RESEARCH_CAPACITY_INFRASTRUCTURE_CSV.open("r", encoding="utf-8", newline="") as handle:
            infrastructure_reader = csv.DictReader(handle)
            infrastructure_columns = set(infrastructure_reader.fieldnames or [])
        with RESEARCH_CAPACITY_RESOURCE_COVERAGE_CSV.open("r", encoding="utf-8", newline="") as handle:
            coverage_rows = list(csv.DictReader(handle))

        for resource in GIGAS_MODELED_RESOURCE_KEYS:
            self.assertIn(f"total_output_{resource}", building_columns)
            self.assertIn(f"total_upkeep_{resource}", building_columns)
            self.assertIn(f"total_output_{resource}", development_columns)
            self.assertIn(f"total_upkeep_{resource}", development_columns)
            self.assertIn(f"net_{resource}", development_columns)
            self.assertIn(f"direct_output_{resource}", infrastructure_columns)
            self.assertIn(f"direct_upkeep_{resource}", infrastructure_columns)
        for columns in (building_columns, development_columns):
            self.assertIn("total_output_influence", columns)
            self.assertIn("total_upkeep_influence", columns)
        self.assertIn("direct_output_influence", infrastructure_columns)
        self.assertIn("direct_upkeep_influence", infrastructure_columns)

        buildings_with_promoted_gigas_value = [
            row
            for row in building_rows
            if any(
                float(row[f"total_output_{resource}"]) != 0.0
                or float(row[f"total_upkeep_{resource}"]) != 0.0
                for resource in GIGAS_MODELED_RESOURCE_KEYS
            )
        ]
        development_with_promoted_gigas_value = [
            row
            for row in development_rows
            if any(float(row[f"net_{resource}"]) != 0.0 for resource in GIGAS_MODELED_RESOURCE_KEYS)
        ]

        self.assertTrue(buildings_with_promoted_gigas_value)
        self.assertTrue(development_with_promoted_gigas_value)
        self.assertFalse([row for row in coverage_rows if row["normal_column_status"] == "unsupported"])
        promoted_resources = {row["resource_key"] for row in coverage_rows}
        self.assertTrue(GIGAS_MODELED_RESOURCE_KEYS.issubset(promoted_resources))

    def test_research_capacity_model_carries_source_gates(self):
        with RESEARCH_CAPACITY_BUILDINGS_CSV.open("r", encoding="utf-8", newline="") as handle:
            buildings_reader = csv.DictReader(handle)
            building_rows = list(buildings_reader)
            building_columns = set(buildings_reader.fieldnames or [])
        with RESEARCH_CAPACITY_DEVELOPMENT_CSV.open("r", encoding="utf-8", newline="") as handle:
            development_reader = csv.DictReader(handle)
            development_rows = list(development_reader)
            development_columns = set(development_reader.fieldnames or [])

        for columns in (building_columns, development_columns):
            self.assertIn("prerequisites", columns)
            self.assertIn("potential_allow_gates", columns)
            self.assertIn("potential_allow_gate_atoms", columns)
            self.assertIn("event_flags", columns)
            self.assertIn("unlock_flags", columns)

        self.assertTrue([row for row in building_rows if row["prerequisites"]])
        self.assertTrue([row for row in building_rows if row["potential_allow_gates"]])
        self.assertTrue([row for row in building_rows if row["potential_allow_gate_atoms"]])
        self.assertTrue([row for row in development_rows if row["potential_allow_gates"]])

        row_by_building = {row["building_id"]: row for row in building_rows}
        if "building_research_lab_3" in row_by_building:
            self.assertIn("tech", row_by_building["building_research_lab_3"]["prerequisites"])

    def test_research_capacity_model_audits_source_excluded_job_references(self):
        with RESEARCH_CAPACITY_BUILDINGS_CSV.open("r", encoding="utf-8", newline="") as handle:
            building_rows = list(csv.DictReader(handle))
        with RESEARCH_CAPACITY_DEVELOPMENT_CSV.open("r", encoding="utf-8", newline="") as handle:
            development_rows = list(csv.DictReader(handle))

        corporate_clinics = {row["building_id"]: row for row in building_rows}["building_corporate_clinics"]
        self.assertNotIn("job_healthcare_amenities", corporate_clinics["unknown_jobs"])

        corrona_capital = {row["building_id"]: row for row in building_rows}["building_giga_corrona_capital"]
        corrona_exclusions = json.loads(corrona_capital["source_excluded_jobs"])
        self.assertEqual(
            corrona_exclusions["job_tc_arcane_research_job"],
            "inactive_external_thaumstellaris_integration_modeled_zero_effect",
        )

        rows_by_object = {row["object_id"]: row for row in development_rows}
        void_structure_exclusions = json.loads(rows_by_object["district_giga_birch_void_orykta"]["source_excluded_jobs"])
        self.assertEqual(
            void_structure_exclusions["job_acot_enforcer"],
            "inactive_external_acot_integration_modeled_zero_effect",
        )

        interstellar_research_exclusions = json.loads(rows_by_object["district_giga_hab_science"]["source_excluded_jobs"])
        self.assertEqual(
            interstellar_research_exclusions["job_giga_interstellar_researcher"],
            "source_orphan_no_pop_job_definition_modeled_zero_effect",
        )

    def test_research_capacity_model_preserves_resource_scenarios(self):
        with RESEARCH_CAPACITY_JOBS_CSV.open("r", encoding="utf-8", newline="") as handle:
            jobs_reader = csv.DictReader(handle)
            job_columns = set(jobs_reader.fieldnames or [])
        with RESEARCH_CAPACITY_BUILDINGS_CSV.open("r", encoding="utf-8", newline="") as handle:
            buildings_reader = csv.DictReader(handle)
            building_rows = list(buildings_reader)
            building_columns = set(buildings_reader.fieldnames or [])
        with RESEARCH_CAPACITY_DEVELOPMENT_CSV.open("r", encoding="utf-8", newline="") as handle:
            development_reader = csv.DictReader(handle)
            development_rows = list(development_reader)
            development_columns = set(development_reader.fieldnames or [])
        with RESEARCH_CAPACITY_PLAN_CSV.open("r", encoding="utf-8", newline="") as handle:
            plan_reader = csv.DictReader(handle)
            plan_columns = set(plan_reader.fieldnames or [])

        scenario_json_columns = {
            "base_output_json",
            "triggered_output_json",
            "conservative_output_json",
            "optimistic_output_json",
            "base_upkeep_json",
            "triggered_upkeep_json",
            "conservative_upkeep_json",
            "optimistic_upkeep_json",
        }
        for prefix in ("base", "triggered", "optimistic"):
            self.assertIn(f"{prefix}_output_physics_research", job_columns)
            self.assertIn(f"{prefix}_upkeep_consumer_goods", job_columns)
        for columns in (building_columns, development_columns):
            self.assertTrue(scenario_json_columns.issubset(columns))
            self.assertIn("base_output_physics_research", columns)
            self.assertIn("triggered_output_physics_research", columns)
            self.assertIn("conservative_upkeep_consumer_goods", columns)
            self.assertIn("optimistic_upkeep_consumer_goods", columns)
        self.assertIn("base_net_resources_json", development_columns)
        self.assertIn("conservative_net_resources_json", development_columns)
        self.assertIn("optimistic_net_resources_json", development_columns)
        self.assertIn("conservative_research_per_full_colony", plan_columns)
        self.assertIn("optimistic_research_per_full_colony", plan_columns)
        self.assertIn("triggered_output_physics_research", plan_columns)
        self.assertIn("conservative_net_consumer_goods", plan_columns)
        self.assertIn("optimistic_net_consumer_goods", plan_columns)

        def assert_scenario_arithmetic(rows: list[dict[str, str]], row_label: str) -> None:
            self.assertTrue(rows, row_label)
            for sample in rows[:25]:
                for resource in ("physics_research", "society_research", "engineering_research", "consumer_goods"):
                    base = float(sample[f"base_output_{resource}"])
                    triggered = float(sample[f"triggered_output_{resource}"])
                    optimistic = float(sample[f"optimistic_output_{resource}"])
                    self.assertAlmostEqual(base + triggered, optimistic, places=6)
                    self.assertAlmostEqual(float(sample[f"conservative_output_{resource}"]), base, places=6)
                    base_upkeep = float(sample[f"base_upkeep_{resource}"])
                    triggered_upkeep = float(sample[f"triggered_upkeep_{resource}"])
                    optimistic_upkeep = float(sample[f"optimistic_upkeep_{resource}"])
                    self.assertAlmostEqual(base_upkeep + triggered_upkeep, optimistic_upkeep, places=6)
                    self.assertAlmostEqual(float(sample[f"conservative_upkeep_{resource}"]), optimistic_upkeep, places=6)

        assert_scenario_arithmetic(building_rows, "building scenario rows")
        assert_scenario_arithmetic(development_rows, "development scenario rows")

    def test_research_capacity_model_generates_build_plan_readiness_rows(self):
        with RESEARCH_CAPACITY_BUILDINGS_CSV.open("r", encoding="utf-8", newline="") as handle:
            building_rows = list(csv.DictReader(handle))
        with RESEARCH_CAPACITY_READINESS_CSV.open("r", encoding="utf-8", newline="") as handle:
            readiness_reader = csv.DictReader(handle)
            readiness_rows = list(readiness_reader)
            readiness_columns = set(readiness_reader.fieldnames or [])

        expected_columns = {
            "building_id",
            "primary_role",
            "readiness_phase",
            "gate_reasons",
            "build_plan_candidate",
            "capital_tier_gate",
            "fallback_building_id",
            "fallback_reason",
            "prerequisites",
            "potential_allow_gate_atoms",
            "upgrade_terminal",
        }
        self.assertTrue(expected_columns.issubset(readiness_columns))
        self.assertEqual(len(readiness_rows), len(building_rows))

        phases = {row["readiness_phase"] for row in readiness_rows}
        self.assertIn("base_available", phases)
        self.assertIn("after_prerequisite", phases)
        self.assertTrue([row for row in readiness_rows if row["gate_reasons"]])
        self.assertTrue([row for row in readiness_rows if row["build_plan_candidate"] == "yes"])
        self.assertTrue([row for row in readiness_rows if row["fallback_reason"] == "same_role_available_before_target_unlock"])

        by_building = {row["building_id"]: row for row in readiness_rows}
        if "building_research_lab_3" in by_building:
            self.assertEqual(by_building["building_research_lab_3"]["readiness_phase"], "after_prerequisite")
            self.assertIn("technology_prerequisite", by_building["building_research_lab_3"]["gate_reasons"])

    def test_research_capacity_model_generates_strategic_benefit_taxonomy(self):
        with RESEARCH_CAPACITY_BENEFITS_CSV.open("r", encoding="utf-8", newline="") as handle:
            benefits_reader = csv.DictReader(handle)
            benefit_rows = list(benefits_reader)
            benefit_columns = set(benefits_reader.fieldnames or [])

        expected_columns = {
            "benefit_class",
            "object_type",
            "object_id",
            "evidence_kind",
            "valuation_status",
            "formula_status",
            "benefit_amount",
            "source_terms",
            "matched_modifier_keys",
            "priority_score",
            "modeling_decision",
            "formula_or_policy",
            "policy_confidence",
        }
        self.assertTrue(expected_columns.issubset(benefit_columns))
        benefit_classes = {row["benefit_class"] for row in benefit_rows}
        self.assertTrue(REQUIRED_STRATEGIC_BENEFIT_CLASSES.issubset(benefit_classes))
        self.assertTrue([row for row in benefit_rows if row["valuation_status"] == "numeric_value_preserved"])
        self.assertTrue([row for row in benefit_rows if row["valuation_status"] == "detected_unvalued"])
        self.assertTrue([row for row in benefit_rows if row["evidence_kind"] == "no_active_stack_evidence"])
        self.assertTrue([row for row in benefit_rows if row["benefit_class"] == "starbase_support"])
        self.assertTrue([row for row in benefit_rows if row["benefit_class"] == "direct_resource_support"])
        self.assertTrue([row for row in benefit_rows if row["modeling_decision"] == "detected_only_non_scoring_policy"])
        self.assertTrue([row for row in benefit_rows if row["modeling_decision"] == "numeric_formula_defined"])
        self.assertTrue([row for row in benefit_rows if row["modeling_decision"] == "source_backed_zero_effect"])

    def test_research_capacity_model_includes_expanded_role_families(self):
        with RESEARCH_CAPACITY_ROLES_CSV.open("r", encoding="utf-8", newline="") as handle:
            role_rows = list(csv.DictReader(handle))

        roles = {row["role"] for row in role_rows}
        self.assertTrue(REQUIRED_EXPANDED_ROLE_FAMILIES.issubset(roles))
        for role in REQUIRED_EXPANDED_ROLE_FAMILIES:
            family_rows = [row for row in role_rows if row["role"] == role]
            self.assertTrue(family_rows, role)
            self.assertTrue(any(row["selected_objects"] for row in family_rows), role)
        self.assertTrue(
            [row for row in role_rows if row["role"] == "capital_world" and row["source_scope"].startswith("strategic_family")]
        )
        self.assertTrue(
            [row for row in role_rows if row["role"] == "ring_world" and row["source_scope"].startswith("development_family")]
        )

    def test_research_capacity_model_generates_blocker_accounting(self):
        with RESEARCH_CAPACITY_BLOCKERS_CSV.open("r", encoding="utf-8", newline="") as handle:
            blocker_reader = csv.DictReader(handle)
            blocker_rows = list(blocker_reader)
            blocker_columns = set(blocker_reader.fieldnames or [])

        expected_columns = {
            "source_artifact",
            "object_type",
            "object_id",
            "issue_type",
            "issue_key",
            "accounting_status",
            "next_action",
            "source_mod",
            "source_file",
        }
        self.assertTrue(expected_columns.issubset(blocker_columns))
        issue_types = {row["issue_type"] for row in blocker_rows}
        self.assertNotIn("unknown_job", issue_types)
        self.assertNotIn("unresolved_variable", issue_types)
        self.assertNotIn("benefit_formula_status", issue_types)
        self.assertNotIn("data_quality_flag", issue_types)
        self.assertFalse([row for row in blocker_rows if not row["accounting_status"]])
        self.assertFalse([row for row in blocker_rows if not row["next_action"]])

    def test_research_capacity_model_generates_consumer_policy(self):
        with RESEARCH_CAPACITY_CONSUMER_POLICY_CSV.open("r", encoding="utf-8", newline="") as handle:
            policy_reader = csv.DictReader(handle)
            policy_rows = list(policy_reader)
            policy_columns = set(policy_reader.fieldnames or [])

        expected_columns = {
            "row_family",
            "consumer_surface",
            "consumer_proof_status",
            "object_type",
            "object_id",
            "role",
            "source_scope",
            "consumer_modeling_status",
            "can_consume_now",
            "readiness_phase",
            "build_plan_candidate",
            "blocker_count",
            "blocker_issue_types",
            "benefit_numeric_rows",
            "benefit_policy_required_rows",
            "fallback_lifetime",
            "replacement_policy",
            "selected_objects",
            "next_action",
        }
        self.assertTrue(expected_columns.issubset(policy_columns))
        self.assertTrue(policy_rows)
        row_families = {row["row_family"] for row in policy_rows}
        self.assertTrue({"building", "role_target", "benefit_class"}.issubset(row_families))
        self.assertFalse([row for row in policy_rows if not row["consumer_surface"]])
        self.assertFalse([row for row in policy_rows if not row["consumer_proof_status"]])
        self.assertFalse([row for row in policy_rows if "colony_automation" in row["consumer_surface"]])
        self.assertEqual(
            {
                row["consumer_surface"]
                for row in policy_rows
                if row["row_family"] == "building"
            },
            {"building_or_district_ai_resource_production_filter"},
        )
        self.assertEqual(
            {
                row["consumer_proof_status"]
                for row in policy_rows
                if row["row_family"] == "benefit_class"
            },
            {"not_consumed"},
        )
        self.assertFalse([row for row in policy_rows if not row["consumer_modeling_status"]])
        self.assertFalse([row for row in policy_rows if not row["next_action"]])

        blocked_rows = [row for row in policy_rows if int(row["blocker_count"]) > 0]
        self.assertFalse(blocked_rows)
        self.assertFalse([row for row in policy_rows if row["consumer_modeling_status"] == "blocked_unresolved_modeling"])
        self.assertTrue([row for row in policy_rows if row["consumer_modeling_status"] == "scorable_now"])
        self.assertTrue([row for row in policy_rows if row["consumer_modeling_status"] == "gated_scorable_with_conditions"])
        self.assertFalse(
            [
                row
                for row in policy_rows
                if row["row_family"] == "building"
                and row["build_plan_candidate"] == "no"
                and row["can_consume_now"] != "no"
            ]
        )
        fallback_rows = [row for row in policy_rows if row["fallback_building_id"]]
        self.assertTrue(fallback_rows)
        self.assertEqual({row["fallback_lifetime"] for row in fallback_rows}, {"permanent_or_no_regret_only"})
        self.assertEqual(
            {row["replacement_policy"] for row in fallback_rows},
            {"no_proactive_replacement_static_evidence"},
        )
        benefit_rows = [row for row in policy_rows if row["row_family"] == "benefit_class"]
        self.assertTrue(benefit_rows)
        self.assertEqual({row["can_consume_now"] for row in benefit_rows}, {"no"})

    def test_research_capacity_model_artifact_row_counts_are_stable(self):
        expected_counts = {
            RESEARCH_CAPACITY_JOBS_CSV: 501,
            RESEARCH_CAPACITY_BUILDINGS_CSV: 826,
            RESEARCH_CAPACITY_DEVELOPMENT_CSV: 547,
            RESEARCH_CAPACITY_PLAN_CSV: 24,
            RESEARCH_CAPACITY_ROLES_CSV: 247,
            RESEARCH_CAPACITY_INFRASTRUCTURE_CSV: 1335,
            RESEARCH_CAPACITY_RESOURCE_COVERAGE_CSV: 21,
            RESEARCH_CAPACITY_READINESS_CSV: 826,
            RESEARCH_CAPACITY_BENEFITS_CSV: 1924,
            RESEARCH_CAPACITY_BLOCKERS_CSV: 0,
            RESEARCH_CAPACITY_CONSUMER_POLICY_CSV: 1093,
        }
        for path, expected_count in expected_counts.items():
            with path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), expected_count, path.name)

    def test_nonconstruction_economic_valuation_dataset_extends_without_duplicate_construction_surfaces(self):
        self.assertTrue(NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.exists())
        self.assertTrue(NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_MD.exists())
        self.assertTrue(nonconstruction_economic_valuation_dataset_passes())
        self.assertTrue(economic_valuation_evidence_passes())
        self.assertTrue(ECONOMIC_VALUATION_EVIDENCE_MD.exists())

        with NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            self.assertEqual(set(reader.fieldnames or []), set(ECONOMIC_VALUATION_CANONICAL_COLUMNS))
        with ECONOMIC_VALUATION_DATASET_CSV.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            construction_rows = list(reader)
            self.assertEqual(set(reader.fieldnames or []), set(ECONOMIC_VALUATION_CANONICAL_COLUMNS))

        self.assertFalse(
            [
                (row["object_type"], row["object_id"], column)
                for row in [*construction_rows, *rows]
                for column in ECONOMIC_VALUATION_CANONICAL_COLUMNS
                if row.get(column, "") == ""
            ]
        )
        object_types = {row["object_type"] for row in rows}
        self.assertFalse({"building", "zone", "district", "megastructure"} & object_types)
        self.assertTrue(
            {
                "pop_job",
                "decision",
                "edict",
                "deposit",
                "resource",
                "starbase_building",
                "starbase_module",
                "technology",
                "colony_type",
                "policy",
                "ascension_perk",
                "tradition",
            }.issubset(object_types)
        )

        evidence_text = ECONOMIC_VALUATION_EVIDENCE_MD.read_text(encoding="utf-8")
        self.assertIn("Construction Dataset Counts", evidence_text)
        self.assertIn("Nonconstruction Dataset Counts", evidence_text)
        self.assertIn("resource", evidence_text)

    def test_generated_timestamp_writer_preserves_stamp_when_body_is_unchanged(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.md"
            write_text_file_preserving_generated_timestamp(
                report_path,
                "# Report\n\nGenerated: first\n\nBody\n",
            )
            write_text_file_preserving_generated_timestamp(
                report_path,
                "# Report\n\nGenerated: second\n\nBody\n",
            )

            self.assertIn("Generated: first", report_path.read_text(encoding="utf-8"))

            write_text_file_preserving_generated_timestamp(
                report_path,
                "# Report\n\nGenerated: third\n\nChanged body\n",
            )

            updated = report_path.read_text(encoding="utf-8")
            self.assertIn("Generated: third", updated)
            self.assertIn("Changed body", updated)

    def test_dataset_job_pressure_overrides_use_live_valuation_rows(self):
        rows = dataset_job_pressure_override_rows()
        row_ids = {row["object_id"] for row in rows}
        row_by_id = {row["object_id"]: row for row in rows}
        self.assertGreaterEqual(len(rows), 50)
        self.assertTrue(all(float(row["jobs_created_total_estimate"]) > 0 for row in rows))
        self.assertTrue(all(float(row["roi_2250_to_2350_estimate"]) > 0 for row in rows))
        self.assertIn("consumer_goods_repair", {row["pressure_family"] for row in rows})
        self.assertNotIn("military_capacity", {row["pressure_family"] for row in rows})
        self.assertIn("building_negative_mass_factory_2", row_ids)
        self.assertIn("building_giga_pcc_scrap_pile", row_ids)
        self.assertIn("building_sentinel_posts", row_ids)
        self.assertNotIn("building_navel_base", row_ids)
        self.assertNotIn("building_navel_command", row_ids)
        self.assertNotIn("building_pd_rogue_council", row_ids)
        self.assertTrue(all(row["object_type"] != "zone" for row in rows))

        generated_files = [
            MOD_ROOT / "common" / "buildings" / "zzzz_staid_13_dataset_job_pressure_buildings.txt",
            MOD_ROOT / "common" / "districts" / "zzzz_staid_13_dataset_job_pressure_districts.txt",
        ]
        combined_text = ""
        for file_path in generated_files:
            self.assertTrue(file_path.exists(), f"{file_path} was not generated")
            text = file_path.read_text(encoding="utf-8")
            combined_text += text
            self.assertIn("staid_dataset_job_pressure", text)
            self.assertIn("ai_resource_production = {", text)
            parse_file(file_path)
        self.assertIn("family:consumer_goods_repair", combined_text)
        self.assertIn("building_negative_mass_factory_2", combined_text)
        self.assertIn("building_giga_pcc_scrap_pile", combined_text)
        self.assertIn("building_sentinel_posts", combined_text)
        self.assertNotIn("building_pd_rogue_council", combined_text)
        self.assertNotIn("family:military_capacity", combined_text)
        self.assertNotIn("building_navel_base", combined_text)
        self.assertNotIn("building_navel_command", combined_text)
        self.assertNotIn("staid_naval_capacity_expansion_ready", combined_text)
        for invalid_marker in (
            "has_unemployed_pop_of_category",
            "job_acot_",
            "district_giga_frameworld_fortress_bunker",
            "district_generator_uncapped",
            "building_gas_extractors_max",
            "building_mote_harvesters_max",
            "building_crystal_mines_max",
        ):
            self.assertNotIn(invalid_marker, combined_text)
        district_text = generated_files[1].read_text(encoding="utf-8")
        self.assertNotIn("trade_value_add", district_text)

    def test_high_scale_ai_defines_remove_vanilla_construction_and_war_hesitation(self):
        defines_path = MOD_ROOT / "common" / "defines" / "zzzz_staid_14_high_scale_ai_defines.txt"
        self.assertTrue(defines_path.exists(), f"{defines_path} was not generated")
        parse_file(defines_path)
        text = defines_path.read_text(encoding="utf-8")
        for marker in (
            "AI_FREE_JOBS_BUILDING_BUILD_CAP = 5000",
            "AI_FOCUS_SCORE_MULT = 12",
            "AI_POPS_SCORE_MULT = 0.25",
            "AI_RESOURCE_TARGET_EXPIRATION_MONTHS = 6",
            "UNDERDEVELOPED_PLANET_LIMIT = 999",
            "AI_UNBUILT_DISTRICT_BOOST_POP_THRESHOLD = 250",
            "AI_UNBUILT_DISTRICT_BOOST_MULTIPLIER = 20.0",
            "BUILDING_BUILD_THRESHOLD = 0.1",
        ):
            self.assertIn(marker, text)
        for user_tuned_define in (
            "AI_AGGRESSIVENESS_BASE",
            "AI_WAR_PREPARATION_MIN_MONTHS",
            "WAR_DECLARATION_MAX_DISTANCE",
        ):
            self.assertRegex(text, rf"\b{user_tuned_define}\s*=")
        self.assertIn("AI_NAVAL_CAP_SCORE_MULT = 15", text)
        self.assertIn("AI_WAR_PREPARATION_MIN_MONTHS = 12", text)
        self.assertIn("AI_WAR_PREPARATION_MAX_MONTHS = 30", text)
        self.assertIn("AI_AGGRESSIVENESS_BASE = 25", text)
        self.assertIn("AI_AGGRESSIVENESS_PROPAGATOR_BOXED_IN_MULT = 12", text)
        self.assertIn("AI_AGGRESSIVENESS_BOXED_IN_MULT = 8", text)
        self.assertIn("AI_AGGRESSIVENESS_NO_COLONY_TARGET_MULT = 2", text)
        self.assertIn("AUTO_EXPLORE_ATTRACTION_SCORE = 1000", text)
        self.assertIn("AUTO_EXPLORE_COLLABORATION_PENALTY = 2000", text)
        self.assertIn("AUTO_EXPLORE_SYSTEM_OWNED = 100", text)
        self.assertIn("ENEMY_FLEET_POWER_MULT = 1.2", text)
        self.assertIn("AI_HOSTILE_FLEET_DISTANCE = 3", text)
        self.assertIn("BOSS_MILITARY_POWER = 100000", text)
        self.assertIn("ULTRA_BOSS_MILITARY_POWER = 500000", text)
        self.assertIn("WAR_DECLARATION_MALUS_DISTANCE = 25", text)
        self.assertIn("WAR_DECLARATION_MALUS = 0.05", text)
        self.assertIn("WAR_DECLARATION_MINIMUM_SCORE = 0.5", text)
        self.assertIn("WAR_DECLARATION_MAX_DISTANCE = 300", text)
        self.assertIn("OFFENSE_VS_DEFENSE_STRATEGY_ALLOTMENT = 1.0", text)

    def test_default_country_type_removes_preplanner_war_deadlock_gates(self):
        path = MOD_ROOT / "common" / "country_types" / "zzzzz_staid_18_native_war_readiness.txt"
        self.assertTrue(path.exists(), f"{path} was not generated")
        parse_file(path)
        generated = path.read_text(encoding="utf-8")
        generated_block = extract_top_level_object_text(generated, "default")
        vanilla = (
            STELLARIS_INSTALL_ROOT / "common" / "country_types" / "00_country_types.txt"
        ).read_text(encoding="utf-8-sig")
        vanilla_block = extract_top_level_object_text(vanilla, "default")
        expected = re.sub(r"(?m)^\s*min_navy_for_wars\s*=.*(?:\n|$)", "", vanilla_block)
        expected = re.sub(
            r"(?m)^(\s*)min_assault_armies_for_wars\s*=.*$",
            r"\1min_assault_armies_for_wars = 0",
            expected,
            count=1,
        )

        self.assertEqual(generated_block, expected)
        self.assertNotIn("min_navy_for_wars", generated_block)
        self.assertRegex(generated_block, r"(?m)^\s*min_assault_armies_for_wars\s*=\s*0\s*$")
        self.assertRegex(generated_block, r"(?m)^\s*declare_war\s*=\s*yes\s*$")

    def test_standalone_personalities_restore_dependency_aggression_without_forced_wars(self):
        path = MOD_ROOT / "common" / "personalities" / "zzzzz_staid_16_standalone_war_pressure.txt"
        self.assertTrue(path.exists(), f"{path} was not generated")
        parse_file(path)
        text = path.read_text(encoding="utf-8")
        vanilla = (
            STELLARIS_INSTALL_ROOT / "common" / "personalities" / "00_personalities.txt"
        ).read_text(encoding="utf-8-sig")
        reference_root = mod_source_root_for_id("3610149307")
        reference = (reference_root / "common" / "personalities" / "00_personalities.txt").read_text(
            encoding="utf-8-sig"
        )
        reference_variables = collect_variables(
            (reference_root / "common" / "scripted_variables" / "stellarai_scripted_variables.txt").read_text(
                encoding="utf-8-sig"
            )
        )
        for object_id, aggression in STANDALONE_AGGRESSION_PERSONALITY_VALUES.items():
            generated_block = extract_top_level_object_text(text, object_id)
            vanilla_block = extract_top_level_object_text(vanilla, object_id)
            reference_block = extract_top_level_object_text(reference, object_id)
            for field in ("aggressiveness", "bravery", "military_spending"):
                reference_match = re.search(rf"(?m)^\s*{field}\s*=\s*([^\s#]+)", reference_block)
                self.assertIsNotNone(reference_match, f"Missing Stellar AI reference field {object_id}.{field}")
                reference_value = parse_numeric(reference_match.group(1), reference_variables)
                expected = re.escape(f"{float(reference_value):g}")
                self.assertRegex(generated_block, rf"(?m)^\s*{field}\s*=\s*{expected}\s*$")
            self.assertRegex(generated_block, rf"(?m)^\s*aggressiveness\s*=\s*{re.escape(f'{aggression:g}')}\s*$")
            generated_without_war_fields = "\n".join(
                line
                for line in generated_block.splitlines()
                if not any(f"{field} =" in line for field in ("aggressiveness", "bravery", "military_spending"))
            )
            vanilla_without_war_fields = "\n".join(
                line
                for line in vanilla_block.splitlines()
                if not any(f"{field} =" in line for field in ("aggressiveness", "bravery", "military_spending"))
            )
            self.assertEqual(generated_without_war_fields, vanilla_without_war_fields)
        for forbidden in ("declare_war", "create_war", "add_casus_belli", "add_claim"):
            self.assertNotIn(forbidden, text)

    def test_research_buildout_uses_native_quality_weights_and_one_third_soft_cap(self):
        colony_types_path = MOD_ROOT / "common" / "colony_types" / "zzzzz_staid_16_research_buildout_plan.txt"
        events_path = MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt"
        triggers_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        for path in (colony_types_path, events_path, triggers_path):
            self.assertTrue(path.exists(), f"{path} was not generated")
            parse_file(path)
        colony_types = colony_types_path.read_text(encoding="utf-8")
        events = events_path.read_text(encoding="utf-8")
        triggers = triggers_path.read_text(encoding="utf-8")
        research = extract_top_level_object_text(colony_types, "col_research")
        for marker in (
            "add = 15",
            "staid_research_role_candidate = yes",
            "factor = 0.2",
            "staid_research_role_reachable = no",
            "staid_research_role_high_conversion_cost = yes",
            "owner = { staid_research_designation_under_soft_cap = no }",
        ):
            self.assertIn(marker, research)
        for forbidden in (
            "staid_research_plan_claimed",
            "staid_economy_safety.4",
            "staid_research_plan_target",
            "staid_research_plan_current",
            "set_carrier_flag",
            "remove_carrier_flag",
            "add = 100000",
        ):
            self.assertNotIn(forbidden, colony_types + events + triggers)
        for marker in (
            "staid_good_research_candidate = {",
            "staid_research_role_high_conversion_cost = {",
            "staid_research_role_reachable = {",
            "staid_research_designation_under_soft_cap = {",
            "staid_research_role_candidate = {",
            "num_owned_colonies >= 3",
            "num_owned_colonies < 6",
            "count < 1",
            "num_owned_colonies >= 12",
            "num_owned_colonies < 15",
            "count < 4",
            "count_owned_colony = {",
            "limit = { has_designation = col_research }",
            "num_districts = { type = district_city value > 0 }",
            "has_any_generator_zone = no",
            "has_any_trade_zone = no",
            "has_any_agriculture_zone = no",
            "has_any_industrial_zone = no",
            "has_any_unity_zone = no",
            "has_any_fortress_zone = no",
            "num_zones = { type = zone_urban value < 1 }",
            "has_any_generator_zone = yes",
            "num_districts = { type = district_generator value > 3 }",
            "NOT = { staid_catastrophic_collapse_mode = yes }",
            "staid_energy_two_month_runway_unsafe = no",
            "staid_consumer_goods_two_month_runway_unsafe = no",
        ):
            self.assertIn(marker, triggers)
        reachable_block = extract_top_level_object_text(triggers, "staid_research_role_reachable")
        bootstrap_contract = """\tOR = {
\t\tstaid_good_research_candidate = yes
\t\tAND = {
\t\t\tstaid_research_role_high_conversion_cost = no"""
        self.assertIn(bootstrap_contract, reachable_block)
        self.assertEqual(reachable_block.count("staid_research_role_high_conversion_cost = no"), 1)
        self.assertNotIn("staid_research_construction_priority_ready = yes", triggers[
            triggers.index("staid_research_role_candidate = {") :
        ])
        self.assertNotIn("is_scope_type = planet", triggers)

    def test_native_system_restriction_avoids_inaccessible_peacetime_routes_without_disabling_cloaks(self):
        cloak_override = MOD_ROOT / "common" / "component_templates" / "zzzzz_staid_science_cloaking_ai_safety.txt"
        self.assertFalse(cloak_override.exists(), f"Obsolete science-cloak override remains: {cloak_override}")

        route_override = MOD_ROOT / "common" / "game_rules" / "zzzzz_staid_science_route_system_restriction.txt"
        self.assertTrue(route_override.exists(), f"{route_override} was not generated")
        parse_file(route_override)

        source_path = mod_source_root_for_id("3728581560") / "common" / "game_rules" / "scfe_game_rules.txt"
        source_object = extract_top_level_object_text(read_text(source_path), "ai_should_restrict_system")
        generated_text = route_override.read_text(encoding="utf-8")
        generated_object = extract_top_level_object_text(generated_text, "ai_should_restrict_system")
        self.assertEqual(
            [line for line in generated_text.splitlines() if line.startswith("@")],
            [],
        )
        object_marker = "ai_should_restrict_system = {\n    OR = {\n"
        self.assertEqual(source_object.count(object_marker), 1)
        access_branch = '''        AND = {
            root = {
                is_country_type = default
            }
            exists = owner
            owner = {
                NOT = { is_same_value = root }
                has_communications = root
                NOT = { is_at_war_with = root }
            }
            NOT = { has_access_fleet = root }
        }
'''
        expected_object = source_object.replace(object_marker, object_marker + access_branch, 1)
        expected_text = (
            "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
            "# Full-object override copied from the active Forgotten Empires 3728581560 winner.\n"
            "# Only Director delta: default AI empires avoid contacted foreign systems they cannot enter while at peace.\n"
            "# Current access is evaluated by the native game rule; this stores no retry state and does not disable cloaking.\n\n"
            + expected_object
        )

        self.assertEqual(generated_text, expected_text)
        self.assertEqual(generated_object, expected_object)
        self.assertTrue(generated_object.startswith(object_marker + access_branch))
        self.assertNotIn("can_access_system", generated_object)
        self.assertNotIn("giga_ai_should_restrict_system", generated_object)
        for forbidden_runtime_state in (
            "country_event =",
            "fleet_event =",
            "set_country_flag =",
            "set_fleet_flag =",
            "set_variable =",
            "on_monthly_pulse",
        ):
            self.assertNotIn(forbidden_runtime_state, generated_object)

        self.assertEqual(list((MOD_ROOT / "events").glob("*science_route*")), [])
        self.assertEqual(list((MOD_ROOT / "common" / "on_actions").glob("*science_route*")), [])

    def test_all_generated_colony_root_surfaces_scope_planet_flag_operations(self):
        self.assertEqual(generated_colony_root_scope_errors(MOD_ROOT), [])

        with tempfile.TemporaryDirectory() as temp_dir:
            mod_root = Path(temp_dir) / "ScopeRegression"
            colony_type_root = mod_root / "common" / "colony_types"
            district_root = mod_root / "common" / "districts"
            colony_type_root.mkdir(parents=True)
            district_root.mkdir(parents=True)
            (colony_type_root / "scope_regression.txt").write_text(
                """
                col_scope_regression = {
                    potential = {
                        OR = {
                            has_planet_flag = wrong_scope
                            planet = { has_planet_flag = correct_scope }
                        }
                        set_planet_flag = wrong_effect_scope
                        remove_planet_flag = wrong_effect_scope
                    }
                }
                """,
                encoding="utf-8",
            )
            (district_root / "scope_regression.txt").write_text(
                """
                district_scope_regression = {
                    potential = {
                        has_planet_flag = wrong_district_scope
                        planet = { has_planet_flag = correct_district_scope }
                    }
                }
                """,
                encoding="utf-8",
            )

            errors = generated_colony_root_scope_errors(mod_root)

        self.assertEqual(len(errors), 4)
        self.assertTrue(any("planet-only has_planet_flag from colony scope" in error for error in errors))
        self.assertTrue(any("planet-only set_planet_flag from colony scope" in error for error in errors))
        self.assertTrue(any("planet-only remove_planet_flag from colony scope" in error for error in errors))
        self.assertTrue(any("common/districts/scope_regression.txt" in error for error in errors))

    def test_minerals_planet_construction_budget_does_not_starve_other_spending(self):
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_14_minerals_planet_construction_budget.txt"
        self.assertTrue(budget_path.exists(), f"{budget_path} was not generated")
        parse_file(budget_path)
        text = budget_path.read_text(encoding="utf-8")
        for marker in (
            "minerals_expenditure_planets_low = {",
            "minerals_expenditure_planets_med = {",
            "minerals_expenditure_planets_high = {",
            "category = planets",
            "staid_high_scale_snowball_pressure",
            "staid_core_deficit_short_runway",
            "modifier = { factor = 0.65 staid_war_logistics_pressure = yes }",
            "staid_unemployment_construction_pressure = yes",
            "weight = 1.0",
            "weight = 0.8",
            "weight = 0.6",
            "modifier = { add = 0.75 staid_unemployment_construction_pressure = yes }",
            "resource_stockpile_compare = { resource = minerals value > 25000 }",
        ):
            self.assertIn(marker, text)
        for starve_marker in ("weight = 28.0", "factor = 40", "desired_min", "desired_max", "add = 300000"):
            self.assertNotIn(starve_marker, text)

    def test_army_recruitment_uses_native_budget_without_scripted_actions(self):
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_14_army_recruitment_budget.txt"
        event_path = MOD_ROOT / "events" / "zzzz_staid_army_reserve_events.txt"
        on_action_path = MOD_ROOT / "common" / "on_actions" / "zzzz_staid_army_reserve_on_actions.txt"
        self.assertTrue(budget_path.exists(), f"{budget_path} was not generated")
        parse_file(budget_path)
        self.assertFalse(event_path.exists(), "Scripted army creation is forbidden")
        self.assertFalse(on_action_path.exists(), "Scripted army creation is forbidden")

        budget = budget_path.read_text(encoding="utf-8")
        country_type = (
            MOD_ROOT / "common" / "country_types" / "zzzzz_staid_18_native_war_readiness.txt"
        ).read_text(encoding="utf-8")

        self.assertIn("weight = 0.20", budget)
        self.assertIn("weight = 0.10", budget)
        self.assertIn("desired_min = {", budget)
        self.assertIn("base = 200", budget)
        self.assertIn("add = 300", budget)
        self.assertIn("add = 500", budget)
        for marker in (
            "staid_basic_economy_runway_safe = yes",
            "staid_core_deficit_short_runway = no",
            "staid_catastrophic_collapse_mode = no",
            "staid_identity_machine_exterminator = yes",
            "staid_identity_devouring_swarm = yes",
            "staid_identity_assimilator = yes",
        ):
            self.assertIn(marker, budget)
        self.assertNotIn("desired_max", budget)
        self.assertNotIn("country_uses_bio_ships = no", budget)
        self.assertIn("min_assault_armies_for_wars = 0", country_type)
        for forbidden_action in ("create_army", "declare_war", "add_claim", "add_casus_belli"):
            self.assertNotIn(forbidden_action, budget)

    def test_opening_leader_budget_funds_scientists_for_empty_science_ships(self):
        path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_15_opening_leader_recruitment_budget.txt"
        self.assertTrue(path.exists(), f"{path} was not generated")
        parse_file(path)
        text = path.read_text(encoding="utf-8")
        self.assertIn("unity_expenditure_leaders = {", text)
        self.assertIn("category = leaders", text)
        self.assertIn("factor = 5", text)
        self.assertIn("years_passed < 20", text)
        self.assertIn("base = 1000", text)
        for forbidden_action in ("create_leader", "create_ship", "set_fleet_order"):
            self.assertNotIn(forbidden_action, text)

    def test_medical_center_override_breaks_vanilla_upgrade_destroy_loop(self):
        path = MOD_ROOT / "common" / "buildings" / "zzzzz_staid_17_medical_center_churn_fix.txt"
        self.assertTrue(path.exists(), f"{path} was not generated")
        parse_file(path)
        text = path.read_text(encoding="utf-8")
        block = extract_top_level_object_text(text, "building_medical_2")
        parsed = parse_pdx(block)
        medical = block_assignments(parsed, "building_medical_2")[0].value
        destroy = block_assignments(medical, "destroy_trigger")[0].value
        owner = block_assignments(destroy, "owner")[0].value
        self.assertTrue(block_contains_assignment(owner, "is_regular_empire", "no"))
        self.assertNotIn("planet_stability > 70", block)
        self.assertNotIn("free_amenities > 20", block)
        self.assertIn("building_sets = {", block)
        self.assertIn("resources = {", block)
        self.assertIn('"tech_frontier_health"', block)

    def test_colony_automation_exception_targets_preserve_parent_legality(self):
        exception_paths = [
            STELLARIS_INSTALL_ROOT / "common" / "colony_automation_exceptions" / "00_crisis_exceptions.txt",
            SNAPSHOT_ROOT
            / "1121692237-gigastructural-engineering-more-44"
            / "common"
            / "colony_automation_exceptions"
            / "01_giga_exceptions.txt",
            SNAPSHOT_ROOT
            / "1121692237-gigastructural-engineering-more-44"
            / "common"
            / "colony_automation_exceptions"
            / "giga_frameworld_exceptions.txt",
            SNAPSHOT_ROOT
            / "1121692237-gigastructural-engineering-more-44"
            / "common"
            / "colony_automation_exceptions"
            / "giga_rogue_ai.txt",
        ]
        exception_text = "\n".join(read_text(path) for path in exception_paths)
        uncommented = "\n".join(line.split("#", 1)[0] for line in exception_text.splitlines())
        requested_objects = set(re.findall(r"\bbuilding\s*=\s*(building_[A-Za-z0-9_]+)", uncommented))
        requested_objects.update(
            match.group(1)
            for match in re.finditer(r"(?m)^\s*(district_[A-Za-z0-9_]+)\s*$", uncommented)
        )

        def child_value_repr(block_text, object_id, child_key):
            parsed = parse_pdx(block_text)
            object_value = block_assignments(parsed, object_id)[0].value
            children = block_assignments(object_value, child_key)
            return repr(children[0].value) if children else None

        dataset_rows = [
            row for row in dataset_job_pressure_override_rows() if row["object_id"] in requested_objects
        ]
        dataset_object_ids = {row["object_id"] for row in dataset_rows}
        self.assertTrue(
            {"building_colony_shelter", "district_hab_housing"}.issubset(dataset_object_ids),
            "The exception audit must exercise both building and district full-object overrides.",
        )
        for row in dataset_rows:
            source_block = extract_top_level_object_text(read_text(Path(row["source_path"])), row["object_id"])
            generated_block = extract_top_level_object_text(
                read_text(Path(row["generated_file"])), row["object_id"]
            )
            for child_key in ("potential", "allow", "possible"):
                self.assertEqual(
                    child_value_repr(generated_block, row["object_id"], child_key),
                    child_value_repr(source_block, row["object_id"], child_key),
                    f"{row['object_id']} changed {child_key} required by colony automation exceptions.",
                )

        generated_exception_overlaps = {
            row["object_name"]
            for row in collect_generated_conflict_rows(MOD_ROOT, SNAPSHOT_ROOT)
            if row["object_name"] in requested_objects
        }
        self.assertEqual(
            generated_exception_overlaps - dataset_object_ids,
            {"building_medical_2", "building_stronghold"},
            "Every non-dataset override requested by an automation exception needs an explicit compatibility review.",
        )

        medical_source = extract_top_level_object_text(
            read_text(STELLARIS_INSTALL_ROOT / "common" / "buildings" / "07_amenity_buildings.txt"),
            "building_medical_2",
        )
        medical_generated = extract_top_level_object_text(
            read_text(MOD_ROOT / "common" / "buildings" / "zzzzz_staid_17_medical_center_churn_fix.txt"),
            "building_medical_2",
        )
        for child_key in ("potential", "allow", "possible"):
            self.assertEqual(
                child_value_repr(medical_generated, "building_medical_2", child_key),
                child_value_repr(medical_source, "building_medical_2", child_key),
            )

    def test_mod_source_root_falls_back_to_live_workshop_when_snapshot_missing(self):
        root = mod_source_root_for_id("819148835")
        self.assertTrue(root.exists())
        self.assertIn("819148835", str(root))

    def test_working_war_planning_kernel_covers_boxed_army_and_high_cap_failure_modes(self):
        kernel_path = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_20_strategy_kernel_triggers.txt"
        claims_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        policy_path = MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt"
        alloy_path = MOD_ROOT / "common" / "ai_budget" / "zzz_staid_alloys_budget.txt"
        for path in (kernel_path, claims_path, policy_path, alloy_path):
            self.assertTrue(path.exists(), f"Missing native war solution file: {path}")
            parse_file(path)

        kernel = kernel_path.read_text(encoding="utf-8")
        claims = claims_path.read_text(encoding="utf-8")
        policies = policy_path.read_text(encoding="utf-8")
        alloys = alloy_path.read_text(encoding="utf-8")
        for marker in (
            "staid_is_diplomatic_opening_phase = {",
            "years_passed < 40",
            "staid_boxed_in_war_pressure = {",
            "has_bordering_system = no",
            "staid_native_war_posture_active = {",
            "staid_war_logistics_pressure = {",
            "staid_peacetime_high_naval_capacity_guard = {",
            "used_naval_capacity_percent >= 0.80",
        ):
            self.assertIn(marker, kernel)
        self.assertNotRegex(kernel, r"(?m)^\s*has_ai_expansion_plan\s*=")
        boxed_claim = claims[
            claims.index("staid_boxed_in_claim_urgency = {") : claims.index(
                "staid_naval_capacity_expansion_ready = {"
            )
        ]
        self.assertIn("staid_boxed_in_war_pressure = yes", boxed_claim)
        self.assertNotIn("num_owned_planets < 5", boxed_claim)
        self.assertIn("factor = 8 staid_boxed_in_war_pressure = yes", policies)
        self.assertIn("factor = 0 staid_native_war_posture_active = yes", policies)
        self.assertIn("factor = 0.25", alloys)
        self.assertIn("staid_peacetime_high_naval_capacity_guard = yes", alloys)
        self.assertNotIn("NOT = { staid_peacetime_high_naval_capacity_guard = yes }", alloys)
        for forbidden in ("declare_war", "create_war", "create_army", "add_claim", "add_casus_belli"):
            self.assertNotIn(forbidden, kernel + claims + policies + alloys)

    def test_war_planning_full_object_provenance_is_generated(self):
        self.assertTrue(WAR_PLANNING_444_PROVENANCE_CSV.exists())
        with WAR_PLANNING_444_PROVENANCE_CSV.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        object_ids = {row["object_id"] for row in rows}
        self.assertTrue(set(STANDALONE_AGGRESSION_PERSONALITY_VALUES).issubset(object_ids))
        for required in (
            "default",
            "diplomatic_stance",
            "orbital_bombardment",
            "orbital_bombardment_accept_surrender",
            "minerals_expenditure_armies",
            "minerals_expenditure_planets_low",
            "alloys_expenditure_ships",
        ):
            self.assertIn(required, object_ids)
        self.assertTrue(all(row["pegasus_444_vanilla_source"] for row in rows))

    def test_pdx_parser_accepts_anonymous_nested_policy_blocks(self):
        parse_pdx(
            """
            orbital_bombardment = {
                option = {
                    name = "orbital_bombardment_indiscriminate"
                    in_breach_of = {
                        {
                            key = resolution_rulesofwar_independent_tribunals
                        }
                    }
                }
            }
            """
        )

    def test_static_validator_reports_no_invalid_references(self):
        self.assertEqual(validate_generated_patch(), [])

    def test_july7_computed_strategy_kernel_surfaces_are_generated(self):
        opening = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_10_opening_strategy_triggers.txt"
        kernel = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_20_strategy_kernel_triggers.txt"
        doctrine = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_11_fleet_doctrine_triggers.txt"
        for path in (opening, kernel, doctrine):
            self.assertTrue(path.exists(), f"Missing generated July 7 trigger surface: {path}")
            parse_file(path)

        opening_text = opening.read_text(encoding="utf-8")
        for marker in (
            "staid_opening_direct_research",
            "staid_opening_unity_to_research",
            "staid_opening_military_to_pops",
            "staid_opening_defensive_tall_research",
            "staid_opening_trade_to_research",
            "staid_opening_hive_growth_research",
            "staid_opening_machine_growth_research",
            "staid_opening_nomad_arkship_research",
        ):
            self.assertIn(marker, opening_text)

        kernel_text = kernel.read_text(encoding="utf-8")
        for marker in (
            "staid_is_opening_phase",
            "staid_is_midgame_scaling_phase",
            "staid_has_safe_basic_stockpiles",
            "staid_can_afford_research_push",
            "staid_security_threatened",
            "staid_security_existential",
            "staid_megastructure_prereq_release",
            "staid_fleet_strategic_aggression_mode",
        ):
            self.assertIn(marker, kernel_text)

        doctrine_text = doctrine.read_text(encoding="utf-8")
        for marker in (
            "staid_fleet_energy_shield_doctrine",
            "staid_fleet_kinetic_armor_doctrine",
            "staid_fleet_missile_evasion_doctrine",
            "staid_fleet_carrier_strikecraft_doctrine",
            "staid_fleet_balanced_filler_doctrine",
        ):
            self.assertIn(marker, doctrine_text)

    def test_opening_route_trigger_references_resolve_across_generated_surfaces(self):
        opening = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_10_opening_strategy_triggers.txt"
        kernel = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_20_strategy_kernel_triggers.txt"
        opening_text = opening.read_text(encoding="utf-8")
        kernel_text = kernel.read_text(encoding="utf-8")

        defined_opening_routes = set(re.findall(r"(?m)^(staid_opening_[A-Za-z0-9_]+)\s*=\s*\{", opening_text))
        required_opening_routes = {
            "staid_opening_direct_research",
            "staid_opening_unity_to_research",
            "staid_opening_military_to_pops",
            "staid_opening_hostile_fauna_clearance",
            "staid_opening_defensive_tall_research",
            "staid_opening_trade_to_research",
            "staid_opening_hive_growth_research",
            "staid_opening_machine_growth_research",
            "staid_opening_nomad_arkship_research",
            "staid_opening_any_research_route",
        }
        self.assertTrue(required_opening_routes.issubset(defined_opening_routes))

        required_kernel_gates = {
            "staid_is_opening_phase",
            "staid_has_safe_basic_stockpiles",
            "staid_can_afford_research_push",
            "staid_security_existential",
            "staid_opening_route_research_priority",
        }
        defined_kernel_gates = set(re.findall(r"(?m)^(staid_[A-Za-z0-9_]+)\s*=\s*\{", kernel_text))
        self.assertTrue(required_kernel_gates.issubset(defined_kernel_gates))

        generated_common_files = [
            path
            for path in (MOD_ROOT / "common").glob("**/*.txt")
            if path.name.startswith(("zzz_staid_", "zzzz_staid_"))
        ]
        defined_route_surface = defined_opening_routes | defined_kernel_gates
        missing_references = {}
        consumer_paths = set()
        for path in generated_common_files:
            text = path.read_text(encoding="utf-8")
            references = set(re.findall(r"\b(staid_opening_[A-Za-z0-9_]+)\b", text))
            missing = references - defined_route_surface
            if missing:
                missing_references[str(path.relative_to(MOD_ROOT))] = sorted(missing)
            if references and path != opening:
                consumer_paths.add(path.relative_to(MOD_ROOT).as_posix())

        self.assertEqual(missing_references, {})
        self.assertIn("common/economic_plans/zzzz_staid_additive_economic_plan.txt", consumer_paths)
        self.assertIn("common/policies/zzzz_staid_10_opening_growth_policies.txt", consumer_paths)
        self.assertIn("common/edicts/zzzz_staid_10_opening_growth_edicts.txt", consumer_paths)
        self.assertNotRegex(opening_text + kernel_text, r"\b(set|has)_country_flag\s*=\s*staid_opening_")

    def test_july7_policy_and_edict_overrides_are_generated_from_verified_ids(self):
        policy = MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt"
        edicts = MOD_ROOT / "common" / "edicts" / "zzzz_staid_10_opening_growth_edicts.txt"
        for path in (policy, edicts):
            self.assertTrue(path.exists(), f"Missing generated July 7 policy/edict surface: {path}")
            parse_file(path)

        policy_text = policy.read_text(encoding="utf-8")
        diplomatic_text = extract_top_level_object_text(policy_text, "diplomatic_stance")
        self.assertIn("diplo_stance_cooperative", diplomatic_text)
        self.assertIn("diplo_stance_cooperative_nomad", diplomatic_text)
        self.assertNotIn("staid_opening_route_research_priority", diplomatic_text)
        self.assertNotIn("factor = 12", diplomatic_text)
        # Diplomatic opening behavior is intentionally narrower than the
        # Director's long economic opening. Native war posture immediately exits
        # Cooperative/Expansionist opening weights without excluding conqueror,
        # subjugator, or militarist personalities from the object wholesale.
        for marker in (
            "factor = 2",
            "staid_is_diplomatic_opening_phase = yes",
            "staid_opening_any_research_route = yes",
            "NOT = { staid_security_existential = yes }",
            "NOT = { staid_native_war_posture_active = yes }",
            "modifier = { factor = 0 staid_native_war_posture_active = yes }",
            "num_rivals = 0",
        ):
            self.assertIn(marker, diplomatic_text)
        for obsolete_marker in (
            "staid_is_opening_phase = yes",
            "NOT = { staid_militarist_conquest_strategy = yes }",
            "NOT = { has_ai_personality_behaviour = conqueror }",
            "NOT = { has_ai_personality_behaviour = subjugator }",
        ):
            self.assertNotIn(obsolete_marker, diplomatic_text)

        edicts_text = edicts.read_text(encoding="utf-8")
        for marker in (
            "research_subsidies",
            "encourage_free_thought",
            "map_the_stars",
            "capacity_subsidies",
            "mining_subsidies",
            "farming_subsidies",
            "fortify_the_border",
            "staid_security_threatened",
        ):
            self.assertIn(marker, edicts_text)

    def test_planetary_diversity_outpost_decisions_are_director_weighted(self):
        decisions_path = MOD_ROOT / "common" / "decisions" / "zzzz_staid_12_planetary_diversity_outpost_decisions.txt"
        triggers_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        self.assertTrue(decisions_path.exists(), "Missing generated Planetary Diversity decision override file.")
        parse_file(decisions_path)

        decisions_text = decisions_path.read_text(encoding="utf-8")
        triggers_text = triggers_path.read_text(encoding="utf-8")
        economy_text = economy_path.read_text(encoding="utf-8")
        for decision_id in (
            "decision_build_pd_moon_base",
            "decision_build_pd_moon_base_moon_colony",
            "decision_build_pd_mining_base",
            "decision_build_pd_mining_base_2",
            "decision_build_pd_mining_base_3",
            "decision_build_pd_food_base",
            "decision_build_pd_food_base_2",
            "decision_build_pd_food_base_3",
            "decision_build_pd_energy_base",
            "decision_build_pd_energy_base_2",
            "decision_build_pd_energy_base_3",
            "decision_build_pd_research_base",
            "decision_build_pd_research_base_2",
            "decision_build_pd_research_base_3",
        ):
            self.assertIn(f"{decision_id} = {{", decisions_text)

        research_block = decisions_text[
            decisions_text.index("decision_build_pd_research_base = {") : decisions_text.index(
                "decision_build_pd_research_base_2 = {"
            )
        ]
        ai_weight = re.search(r"ai_weight\s*=\s*\{(?P<body>.*?)\n\t\}", research_block, re.S)
        self.assertIsNotNone(ai_weight)
        ai_weight_text = ai_weight.group("body")
        self.assertIn("Availability owns prerequisites", ai_weight_text)
        self.assertIn("Lifetime value formula", ai_weight_text)
        self.assertIn("modifier = { factor = 16 years_passed < 30 }", ai_weight_text)
        self.assertIn("modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }", ai_weight_text)
        self.assertIn("modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }", ai_weight_text)
        self.assertIn("modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }", ai_weight_text)
        self.assertIn("modifier = { factor = 8 owner = { staid_pd_research_outpost_priority_ready = yes } }", ai_weight_text)
        self.assertIn("modifier = { factor = 7 is_capital = yes }", ai_weight_text)
        self.assertNotIn("has_technology", ai_weight_text)
        self.assertNotIn("pd_domed_research_site", ai_weight_text)
        self.assertIn("staid_planetary_diversity_outpost_investment_ready", triggers_text)
        self.assertIn("Stellar AI Director Planetary Diversity outpost reserve", economy_text)

    def test_planetary_diversity_naval_capacity_uses_hard_ai_eligibility(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_12_planetary_diversity_value_triggers.txt"
        building_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_12_planetary_diversity_buildings.txt"
        naval_path = MOD_ROOT / "common" / "buildings" / "zzzzz_staid_14_pd_naval_capacity_hard_gates.txt"
        profile_path = RESEARCH_ROOT / "stellar-ai-director-planetary-diversity-profile-2026-07-07.md"
        self.assertFalse(trigger_path.exists())
        self.assertFalse(building_path.exists())
        self.assertTrue(naval_path.exists())
        parse_file(naval_path)
        naval_text = naval_path.read_text(encoding="utf-8")
        profile_text = profile_path.read_text(encoding="utf-8")
        for marker in (
            "building_navel_base = {",
            "building_navel_command = {",
            "owner = { staid_naval_capacity_expansion_ready = yes }",
            "NOT = { has_research_designation = yes }",
            "has_research_designation = yes",
            "owner = { is_ai = yes }",
        ):
            self.assertIn(marker, naval_text)
        self.assertNotIn("ai_weight = {", naval_text)
        self.assertIn("strategic value horizon year", (MOD_ROOT / "notes" / "tuning-notes.md").read_text(encoding="utf-8"))
        self.assertIn("Hostile Space Fauna Clearance", profile_text)

    def test_append_child_block_clause_preserves_existing_source_logic(self):
        source = """sample = {
\tpotential = {
\t\texists = owner
\t}
\tweight = 2
}
"""
        updated = append_child_block_clause(source, "potential", "\t\towner = { is_ai = no }")
        self.assertIn("\t\texists = owner\n\t\towner = { is_ai = no }\n\t}", updated)
        self.assertIn("\tweight = 2", updated)
        parse_pdx(updated)

    def test_fortress_fleet_and_boxed_in_claim_regression_gates_are_generated(self):
        fortress_paths = (
            MOD_ROOT / "common" / "colony_types" / "zzzzz_staid_15_fortress_economic_hard_gates.txt",
            MOD_ROOT / "common" / "buildings" / "zzzzz_staid_15_fortress_economic_hard_gates.txt",
            MOD_ROOT / "common" / "inline_scripts" / "zones" / "shared_fortress_zone.txt",
        )
        for path in fortress_paths:
            self.assertTrue(path.exists(), f"Missing generated fortress hard gate: {path}")
            parse_file(path)
            text = path.read_text(encoding="utf-8")
            self.assertIn("staid_fortress_designation_ready", text)
            self.assertIn("staid_fortress_planet_strategically_placed", text)
            self.assertIn("owner = { is_ai = no }", text)

        colony_text = fortress_paths[0].read_text(encoding="utf-8")
        building_text = fortress_paths[1].read_text(encoding="utf-8")
        self.assertIn("col_fortress = {", colony_text)
        self.assertIn("col_habitat_fortress = {", colony_text)
        self.assertIn("has_building = building_order_keep", colony_text)
        self.assertIn("has_building = building_order_castle", colony_text)
        self.assertIn("building_stronghold = {", building_text)
        self.assertIn("building_fortress = {", building_text)
        self.assertIn("has_modifier = giga_rogue_ai_computer", building_text)
        self.assertNotIn("ai_weight = {", colony_text + building_text)

    def test_gigas_rogue_ai_automation_handler_is_preserved_and_unblocked(self):
        generated_path = (
            MOD_ROOT
            / "common"
            / "colony_automation_exceptions"
            / "zzzzz_staid_01_gigas_rogue_ai.txt"
        )
        source_path = (
            SNAPSHOT_ROOT
            / "1121692237-gigastructural-engineering-more-44"
            / "common"
            / "colony_automation_exceptions"
            / "giga_rogue_ai.txt"
        )
        active_source_path = (
            Path(r"C:\Steam\steamapps\workshop\content\281990\1121692237")
            / "common"
            / "colony_automation_exceptions"
            / "giga_rogue_ai.txt"
        )
        self.assertTrue(generated_path.exists(), f"Missing generated Gigas rogue-AI handler: {generated_path}")
        self.assertTrue(active_source_path.exists(), f"Missing active Gigas rogue-AI handler: {active_source_path}")
        parse_file(generated_path)
        generated_handler = extract_top_level_object_text(
            generated_path.read_text(encoding="utf-8"), "giga_rogue_ai_planet"
        )
        source_handler = extract_top_level_object_text(source_path.read_text(encoding="utf-8"), "giga_rogue_ai_planet")
        active_source_handler = extract_top_level_object_text(
            active_source_path.read_text(encoding="utf-8"), "giga_rogue_ai_planet"
        )
        self.assertEqual(
            source_handler.rstrip(),
            active_source_handler.rstrip(),
            "Refresh the vetted Gigas snapshot before Director replaces a changed active Workshop handler.",
        )
        self.assertEqual(generated_handler.rstrip(), source_handler.rstrip())
        self.assertIn("building = building_stronghold", generated_handler)
        exception_files = sorted(path.name for path in generated_path.parent.glob("*.txt"))
        self.assertEqual(exception_files, [generated_path.name])
        descriptor_text = (MOD_ROOT / "descriptor.mod").read_text(encoding="utf-8")
        self.assertNotIn('replace_path = "common/colony_automation_exceptions"', descriptor_text)

        building_path = MOD_ROOT / "common" / "buildings" / "zzzzz_staid_15_fortress_economic_hard_gates.txt"
        stronghold = extract_top_level_object_text(
            building_path.read_text(encoding="utf-8"), "building_stronghold"
        )
        self.assertIn("has_modifier = giga_rogue_ai_computer", stronghold)
        self.assertIn("num_buildings = { type = building_stronghold value < 2 }", stronghold)
        self.assertIn("num_buildings = { type = building_fortress value < 2 }", stronghold)
        parsed_stronghold = parse_pdx(stronghold)
        stronghold_value = block_assignments(parsed_stronghold, "building_stronghold")[0].value
        allow_value = block_assignments(stronghold_value, "allow")[0].value
        outer_or = block_assignments(allow_value, "OR")[0].value
        ai_branch = block_assignments(outer_or, "AND")[0].value
        ai_gates = block_assignments(ai_branch, "OR")
        self.assertEqual(len(ai_gates), 2)
        self.assertTrue(block_assignments(ai_gates[0].value, "has_modifier"))
        cap_branch = block_assignments(ai_gates[1].value, "AND")[0].value
        self.assertEqual(len(block_assignments(cap_branch, "num_buildings")), 2)
        fortress = extract_top_level_object_text(
            building_path.read_text(encoding="utf-8"), "building_fortress"
        )
        self.assertIn("has_modifier = giga_rogue_ai_computer", fortress)

        triggers_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        triggers = triggers_path.read_text(encoding="utf-8")
        fortress_trigger = triggers[
            triggers.index("staid_fortress_designation_ready = {") : triggers.index(
                "staid_resource_waste_pressure = {"
            )
        ]
        for marker in (
            "NOT = { has_deficit = alloys }",
            "has_monthly_income = { resource = alloys value > 0 }",
            "num_owned_planets >= 6",
            "used_naval_capacity_percent > 0.70",
            "highest_threat > 50",
        ):
            self.assertIn(marker, fortress_trigger)
        for marker in (
            "staid_research_input_runway_safe = yes",
            "staid_food_runway_safe = yes",
            "staid_mineral_runway_safe = yes",
            "staid_alloy_colony_runway_safe = yes",
            "staid_alloy_runway_safe = yes",
            "staid_energy_runway_safe = yes",
        ):
            self.assertIn(marker, triggers)
        scaled_alloy_colonies = extract_top_level_object_text(triggers, "staid_scaled_alloys_income_safe")
        scaled_alloy_fleet = extract_top_level_object_text(triggers, "staid_scaled_alloy_fleet_income_safe")
        scaled_food_colony = extract_top_level_object_text(triggers, "staid_food_colony_runway_safe")
        scaled_food = extract_top_level_object_text(triggers, "staid_food_runway_safe")
        for marker in (
            "num_owned_planets < 6",
            "has_monthly_income = { resource = alloys value > 75 }",
            "num_owned_planets >= 50",
            "has_monthly_income = { resource = alloys value > 1200 }",
        ):
            self.assertIn(marker, scaled_alloy_colonies)
        for marker in (
            "fleet_power < 10000",
            "fleet_power >= 1000000",
            "has_monthly_income = { resource = alloys value > 2000 }",
        ):
            self.assertIn(marker, scaled_alloy_fleet)
        self.assertIn("has_monthly_income = { resource = food value > 0 }", scaled_food_colony)
        self.assertIn("staid_scaled_food_stockpile_safe = yes", scaled_food_colony)
        self.assertIn("staid_food_colony_runway_safe = yes", scaled_food)
        self.assertIn("NOT = { country_uses_bio_ships = yes }", scaled_food)
        self.assertIn("staid_scaled_bioship_food_fleet_income_safe = yes", scaled_food)
        placement_trigger = triggers[
            triggers.index("staid_fortress_planet_strategically_placed = {") : triggers.index(
                "staid_resource_waste_pressure = {"
            )
        ]
        self.assertIn("exists = owner", placement_trigger)
        self.assertIn("solar_system = { is_bottleneck_system = yes }", placement_trigger)

        alloy_budget_path = MOD_ROOT / "common" / "ai_budget" / "zzz_staid_alloys_budget.txt"
        alloy_budget = alloy_budget_path.read_text(encoding="utf-8")
        for marker in (
            "alloys_expenditure_ships = {",
            "alloys_expenditure_ship_upgrades = {",
            "always = yes",
            "factor = 0.25",
            "can_be_upgraded = yes",
        ):
            self.assertIn(marker, alloy_budget)
        self.assertNotIn("staid_fleet_buildup_economy_safe = yes", alloy_budget)
        self.assertNotIn("staid_emergency_fleet_spending_required = yes", alloy_budget)

        claim_budget = (
            MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_08_site_limited_expansion_ai_budget.txt"
        ).read_text(encoding="utf-8")
        self.assertIn("modifier = { factor = 12 staid_boxed_in_claim_urgency = yes }", claim_budget)
        boxed_in_trigger = triggers[
            triggers.index("staid_boxed_in_claim_urgency = {") : triggers.index(
                "staid_naval_capacity_expansion_ready = {"
            )
        ]
        # The 4.4.4 replacement delegates containment detection to the shared
        # boxed-in war-pressure trigger. Mature empires must not age out of claim
        # pressure through the obsolete five-planet cutoff.
        for marker in (
            "has_potential_claims = yes",
            "staid_boxed_in_war_pressure = yes",
            "has_resource = { type = influence amount > 250 }",
        ):
            self.assertIn(marker, boxed_in_trigger)
        self.assertNotIn("num_owned_planets < 5", boxed_in_trigger)
        self.assertNotIn("NOT = { has_ai_expansion_plan = yes }", boxed_in_trigger)

    def test_relative_economic_standards_scale_by_colonies_and_fleet_burden(self):
        self.assertTrue(RELATIVE_ECONOMIC_STANDARDS_CSV.exists())
        self.assertTrue(RELATIVE_ECONOMIC_STANDARDS_MD.exists())
        rows = relative_economic_standard_rows()
        self.assertEqual(len(rows), 69)
        self.assertFalse(
            [
                row
                for row in rows
                if row["basis"] == "owned_colonies"
                and row["resource"] == "food"
                and row["measure"] == "income"
            ],
            "Ordinary food should scale reserve, not demand a large net monthly surplus.",
        )
        colony_alloy_income = [
            row
            for row in rows
            if row["basis"] == "owned_colonies"
            and row["resource"] == "alloys"
            and row["measure"] == "income"
        ]
        self.assertEqual([row["target"] for row in colony_alloy_income], [75, 150, 300, 600, 1200])
        fleet_alloy_income = [
            row
            for row in rows
            if row["basis"] == "current_fleet_power" and row["measure"] == "income"
        ]
        self.assertEqual([row["target"] for row in fleet_alloy_income], [75, 150, 300, 600, 1200, 2000])
        million_fleet_reserve = next(
            row
            for row in rows
            if row["basis"] == "current_fleet_power"
            and row["measure"] == "stockpile"
            and row["lower_inclusive"] == 1000000
        )
        self.assertEqual(million_fleet_reserve["target"], 20000)
        self.assertLessEqual(
            max(row["target"] for row in rows if row["measure"] == "stockpile"),
            20000,
            "Normal relative standards must remain operating floats, not full replacement warehouses.",
        )
        million_bioship_food_income = next(
            row
            for row in rows
            if row["basis"] == "bio_ship_fleet_power"
            and row["measure"] == "income"
            and row["lower_inclusive"] == 1000000
        )
        self.assertEqual(million_bioship_food_income["target"], 1000)

    def test_militarist_conquest_and_raiding_surfaces_are_generated(self):
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        policies_path = MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt"
        bombardment_path = MOD_ROOT / "common" / "bombardment_stances" / "zzzz_staid_12_militarist_raiding_bombardment.txt"
        ascension_path = MOD_ROOT / "common" / "ascension_perks" / "zzzz_staid_02_perks_traditions_ascension_perks.txt"
        for path in (policies_path, bombardment_path):
            self.assertTrue(path.exists(), f"Missing generated militarist surface: {path}")
            parse_file(path)
        policies = policies_path.read_text(encoding="utf-8")
        bombardment = bombardment_path.read_text(encoding="utf-8")
        ascension_perks = ascension_path.read_text(encoding="utf-8")
        for marker in (
            "staid_militarist_conquest_strategy",
            "staid_raiding_pop_growth_strategy",
            "staid_hostile_fauna_safe_clearance_window",
            "staid_hostile_fauna_clearance_strategy",
            "staid_raiding_pop_acquisition_priority",
        ):
            self.assertIn(marker, triggers)
        conquest_block = extract_top_level_object_text(triggers, "staid_militarist_conquest_strategy")
        raiding_block = extract_top_level_object_text(triggers, "staid_raiding_pop_growth_strategy")
        self.assertIn("used_naval_capacity_percent < 1.40", conquest_block)
        self.assertIn("used_naval_capacity_percent < 2.00", raiding_block)
        self.assertIn("staid_catastrophic_collapse_mode", conquest_block + raiding_block)
        self.assertIn("NOT = { staid_core_deficit_short_runway = yes }", conquest_block)
        self.assertIn("staid_basic_economy_runway_safe = yes", conquest_block)
        self.assertNotIn("staid_survival_mode", conquest_block + raiding_block)
        self.assertNotIn("recently_lost_war", conquest_block + raiding_block)
        for marker in (
            "Stellar AI Director militarist conquest fleet reserve",
            "Stellar AI Director raiding pop acquisition reserve",
            "Stellar AI Director hostile fauna clearance reserve",
        ):
            self.assertIn(marker, economy)
        self.assertIn("staid_militarist_conquest_strategy", policies)
        self.assertIn("orbital_bombardment = {", policies)
        self.assertIn("orbital_bombardment_indiscriminate", policies)
        self.assertNotIn("factor = 24 staid_raiding_pop_growth_strategy = yes", policies)
        self.assertIn("factor = 18 staid_militarist_conquest_strategy = yes", policies)
        self.assertIn("orbital_bombardment_accept_surrender = {", policies)
        self.assertIn("orbital_bombardment_surrender_forbidden", policies)
        self.assertIn("base = 1", policies)
        self.assertIn("factor = 80 staid_raiding_pop_growth_strategy = yes", policies)
        self.assertNotIn("Orbital bombardment policy is documented as a follow-up", policies)
        self.assertIn("raiding = {", bombardment)
        self.assertIn("abduct_pops = yes", bombardment)
        self.assertIn("factor = 60 owner = { staid_raiding_pop_growth_strategy = yes }", bombardment)
        self.assertNotIn("ap_nihilistic_acquisition = {", ascension_perks)
        self.assertIn("has_ascension_perk = ap_nihilistic_acquisition", raiding_block)
        self.assertIn("has_valid_civic = civic_barbaric_despoilers", raiding_block)
        self.assertIn("has_origin = origin_slavers", raiding_block)

    def test_fleet_payoff_routes_bias_economy_without_forcing_wars(self):
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        policies = (MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt").read_text(
            encoding="utf-8"
        )
        bombardment = (
            MOD_ROOT / "common" / "bombardment_stances" / "zzzz_staid_12_militarist_raiding_bombardment.txt"
        ).read_text(encoding="utf-8")
        ascension_perks = (
            MOD_ROOT / "common" / "ascension_perks" / "zzzz_staid_02_perks_traditions_ascension_perks.txt"
        ).read_text(encoding="utf-8")

        def generated_object_block(text, object_name):
            start = text.index(f"{object_name} = {{")
            next_header = text.find("\n\n\n# policy_route =", start + 1)
            return text[start:] if next_header == -1 else text[start:next_header]

        generated_text = "\n".join(
            (
                triggers[
                    triggers.index("staid_militarist_conquest_strategy = {") : triggers.index(
                        "staid_raiding_pop_growth_strategy = {"
                    )
                ],
                triggers[
                    triggers.index("staid_raiding_pop_growth_strategy = {") : triggers.index(
                        "staid_raiding_pop_acquisition_priority = {"
                    )
                ],
                economy[
                    economy.index('set_name = "Stellar AI Director militarist conquest fleet reserve"') : economy.index(
                        'set_name = "Stellar AI Director raiding pop acquisition reserve"'
                    )
                ],
                economy[
                    economy.index('set_name = "Stellar AI Director raiding pop acquisition reserve"') : economy.index(
                        'set_name = "Stellar AI Director hostile fauna clearance reserve"'
                    )
                ],
                policies,
                bombardment,
                generated_object_block(ascension_perks, "ap_lord_of_war"),
            )
        )

        for marker in (
            'set_name = "Stellar AI Director militarist conquest fleet reserve"',
            'set_name = "Stellar AI Director raiding pop acquisition reserve"',
            "alloys = 600",
            "engineering_research = 310",
            "alloys = 650",
            "staid_identity_barbaric_despoiler = yes",
            "factor = 18 staid_militarist_conquest_strategy = yes",
            "factor = 80 staid_raiding_pop_growth_strategy = yes",
            "abduct_pops = yes",
            "ap_nihilistic_acquisition",
        ):
            self.assertIn(marker, generated_text)

        forbidden_forced_war_hooks = (
            "declare_war",
            "set_war_goal",
            "create_war",
            "add_claim",
            "create_claim",
            "add_casus_belli",
            "country_event =",
            "fleet_event =",
            "create_fleet",
        )
        for hook in forbidden_forced_war_hooks:
            self.assertNotIn(hook, generated_text)

    def test_hostile_fauna_reserve_stays_on_safe_clearance_window(self):
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        safe_window_block = triggers[
            triggers.index("staid_hostile_fauna_safe_clearance_window = {") : triggers.index(
                "staid_hostile_fauna_clearance_strategy = {"
            )
        ]
        strategy_block = triggers[
            triggers.index("staid_hostile_fauna_clearance_strategy = {") : triggers.index(
                "staid_site_limited_expansion_ready = {"
            )
        ]
        reserve_block = economy[
            economy.index('set_name = "Stellar AI Director hostile fauna clearance reserve"') : economy.index(
                'set_name = "Stellar AI Director modded unlock research reserve"'
            )
        ]

        self.assertIn("staid_fleet_buildup_economy_safe = yes", safe_window_block)
        self.assertIn("NOT = { staid_security_existential = yes }", safe_window_block)
        self.assertIn("used_naval_capacity_percent < 1.20", safe_window_block)
        self.assertIn("has_monthly_income = { resource = alloys value > 60 }", safe_window_block)
        self.assertIn("staid_hostile_fauna_safe_clearance_window = yes", strategy_block)
        self.assertIn("staid_hostile_fauna_clearance_strategy = yes", reserve_block)

        forbidden_targets = (
            "crystal_station_large",
            "leviathan_01_scavenger_bot",
            "leviathan_01_elder_tiyanki",
            "leviathan_01_voidspawn",
            "reanimated_leviathan_01_elder_tiyanki",
            "reanimated_leviathan_01_voidspawn",
            "reanimated_space_dragon",
            "tech_leviathan_techgenesis",
        )
        forbidden_effects = (
            "fleet_event =",
            "country_event =",
            "create_fleet =",
            "declare_war",
            "every_owned_fleet",
        )
        for block in (safe_window_block, strategy_block, reserve_block):
            for target in forbidden_targets:
                self.assertNotIn(target, block)
            for effect in forbidden_effects:
                self.assertNotIn(effect, block)

    def test_dataset_job_pressure_adds_ai_resource_production(self):
        amounts = dataset_ai_resource_production_amounts(
            {
                "object_id": "building_test_research_jobs",
                "object_type": "building",
                "jobs_created_total_estimate": "3",
                "direct_monthly_output_json": "{}",
                "modifier_keys": "job_researcher_add|planet_researchers_physics_research_produces_add",
                "pressure_family": "research_scaling",
            }
        )
        self.assertEqual(amounts["physics_research"], 1)
        self.assertIn("society_research", amounts)
        self.assertIn("engineering_research", amounts)

        direct_amounts = dataset_ai_resource_production_amounts(
            {
                "object_id": "building_test_factory",
                "object_type": "building",
                "jobs_created_total_estimate": "0",
                "direct_monthly_output_json": '{"consumer_goods":35.0}',
                "modifier_keys": "",
                "pressure_family": "consumer_goods_repair",
            }
        )
        self.assertEqual(direct_amounts, {"consumer_goods": 35})

    def test_dataset_job_pressure_uses_economic_plan_mapping_and_rejects_military_objects(self):
        military_row = {
            "object_id": "building_navel_base",
            "object_type": "building",
            "category": "army",
            "jobs_created_json": '{"job_pd_naval_admin":300.0}',
            "direct_monthly_output_json": "{}",
            "modifier_keys": "",
            "jobs_created_total_estimate": "3",
            "roi_2250_to_2350_estimate": "20000",
            "data_quality_flags": "has_jobs",
        }
        self.assertEqual(dataset_job_pressure_family(military_row), "military_capacity")
        with self.assertRaisesRegex(ValueError, "hard eligibility gates"):
            dataset_job_pressure_weight_block("building_navel_base = {\n}\n", military_row)

        research_row = {
            **military_row,
            "object_id": "building_test_research",
            "category": "research",
            "jobs_created_json": '{"job_researcher":300.0}',
            "pressure_family": "research_scaling",
        }
        source_block = """building_test_research = {
\tai_weight_coefficient = 1.2
\tadditional_ai_weight = 25
}
"""
        research_block = dataset_job_pressure_weight_block(source_block, research_row)
        self.assertIn("ai_resource_production = {", research_block)
        self.assertIn("ai_weight_coefficient = 1.2", research_block)
        self.assertIn("additional_ai_weight = 25", research_block)
        self.assertNotIn("ai_weight = {", research_block)
        self.assertNotIn("owner = { staid_", research_block)

    def test_archetype_economic_plans_are_bounded_and_not_clock_driven(self):
        economy = (
            MOD_ROOT
            / "common"
            / "economic_plans"
            / "zzzz_staid_additive_economic_plan.txt"
        ).read_text(encoding="utf-8")
        retired = (
            "early modded research rush",
            "midgame megastructure rush",
            "crisis-scale giga rush",
            "planetcraft survival curve",
            "pathological snowball reserve",
        )
        for name in retired:
            self.assertNotIn(name, economy)

        primary = (
            "extermination",
            "gestalt_growth",
            "defensive",
            "research",
            "diplomatic",
        )
        secondary = (
            "extermination",
            "conquest",
            "gestalt_growth",
            "defensive",
            "research",
            "diplomatic",
        )
        names = [
            *(f"Stellar AI Director primary {name} economy" for name in primary),
            *(
                f"Stellar AI Director lead secondary {name} economy"
                for name in secondary
            ),
            "Stellar AI Director militarist conquest fleet reserve",
        ]
        for name in names:
            block = _economic_subplan_block(economy, name)
            self.assertTrue(block, name)
            self.assertIn("optional = yes", block)
            self.assertNotIn("scaling = yes", block)
            self.assertIn("staid_basic_economy_runway_safe = yes", block)
            self.assertIn(
                "NOT = { staid_core_deficit_short_runway = yes }", block
            )
            self.assertIn("NOT = { staid_catastrophic_collapse_mode = yes }", block)
            self.assertNotIn("is_at_war", block)
            self.assertNotIn("recently_lost_war", block)
            self.assertNotIn("years_passed", block)
            self.assertNotIn("naval_cap =", block)
            self.assertNotIn("pops =", block)
            self.assertNotIn("consumer_goods =", block)
            if "_research =" in block:
                self.assertIn(
                    "staid_research_construction_priority_ready = yes", block
                )

        for name in (
            "Stellar AI Director modded unlock research reserve",
            "Stellar AI Director ESC component resource readiness",
            "Stellar AI Director NSC3 hull readiness reserve",
        ):
            self.assertNotIn("years_passed", _economic_subplan_block(economy, name))

    def test_defining_identity_economies_replace_broad_archetype_stacking(self):
        economy = (
            MOD_ROOT
            / "common"
            / "economic_plans"
            / "zzzz_staid_additive_economic_plan.txt"
        ).read_text(encoding="utf-8")
        defining = {
            "machine exterminator": "staid_identity_machine_exterminator",
            "rogue servitor": "staid_identity_rogue_servitor",
            "assimilator": "staid_identity_assimilator",
            "devouring swarm": "staid_identity_devouring_swarm",
            "inward perfection": "staid_identity_inward_perfection",
            "megacorp": "staid_identity_megacorp",
        }
        for label, trigger in defining.items():
            block = _economic_subplan_block(
                economy, f"Stellar AI Director defining {label} economy"
            )
            self.assertIn(f"{trigger} = yes", block)
            self.assertIn("optional = yes", block)
            self.assertNotIn("scaling = yes", block)
            self.assertNotIn("years_passed", block)
            self.assertNotIn("is_at_war", block)
            self.assertNotIn("recently_lost_war", block)
            self.assertNotIn("naval_cap =", block)
            self.assertNotIn("pops =", block)
            self.assertIn("staid_basic_economy_runway_safe = yes", block)
            self.assertIn("staid_research_construction_priority_ready = yes", block)

        nomad = _economic_subplan_block(
            economy, "Stellar AI Director defining nomadic economy"
        )
        self.assertIn("staid_identity_nomadic = yes", nomad)
        self.assertIn("staid_research_input_runway_safe = yes", nomad)
        self.assertNotIn("any_owned_planet", nomad)
        self.assertNotIn("staid_archetype_eligible_country", nomad)

        for label in (
            "primary extermination",
            "primary gestalt_growth",
            "primary defensive",
            "primary research",
            "primary diplomatic",
            "lead secondary extermination",
            "lead secondary conquest",
            "lead secondary gestalt_growth",
            "lead secondary defensive",
            "lead secondary research",
            "lead secondary diplomatic",
        ):
            block = _economic_subplan_block(
                economy, f"Stellar AI Director {label} economy"
            )
            self.assertIn("NOR = {", block)
            for trigger in defining.values():
                self.assertIn(f"{trigger} = yes", block)

        raiding = _economic_subplan_block(
            economy, "Stellar AI Director raiding pop acquisition reserve"
        )
        self.assertIn("staid_identity_barbaric_despoiler = yes", raiding)
        self.assertIn("alloys = 650", raiding)
        self.assertNotIn("alloys = 4500", raiding)
        self.assertNotIn("naval_cap =", raiding)

    def test_deficits_suppress_discretionary_research_and_fleet_pressure_but_prioritize_repairs(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        claim_budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_08_site_limited_expansion_ai_budget.txt"
        for path in (trigger_path, economy_path, claim_budget_path):
            parse_file(path)

        triggers = trigger_path.read_text(encoding="utf-8")
        research_gate = extract_top_level_object_text(triggers, "staid_research_construction_priority_ready")
        surplus_gate = extract_top_level_object_text(triggers, "staid_surplus_sink_pressure")
        aggressive_gate = extract_top_level_object_text(triggers, "staid_aggressive_fleet_pressure")
        conquest_gate = extract_top_level_object_text(triggers, "staid_militarist_conquest_strategy")
        naval_gate = extract_top_level_object_text(triggers, "staid_naval_capacity_expansion_ready")
        claim_gate = extract_top_level_object_text(triggers, "staid_influence_claim_pressure")

        self.assertIn("staid_research_minimum_input_runway_safe = yes", research_gate)
        self.assertNotIn("staid_high_scale_snowball_pressure = yes\n\t\tAND", research_gate)
        self.assertIn("NOT = { staid_core_deficit_short_runway = yes }", surplus_gate)
        self.assertIn("staid_basic_economy_runway_safe = yes", aggressive_gate)
        self.assertNotIn("used_naval_capacity_percent < 1.10", aggressive_gate)
        self.assertIn("has_ethic = ethic_militarist", conquest_gate)
        self.assertIn("NOT = { staid_core_deficit_short_runway = yes }", conquest_gate)
        self.assertIn("staid_basic_economy_runway_safe = yes", conquest_gate)
        self.assertNotIn("years_passed > 9", conquest_gate)
        self.assertIn("used_naval_capacity_percent > 0.90", naval_gate)
        self.assertIn("is_at_war = yes", naval_gate)
        self.assertIn("has_potential_claims = yes", claim_gate)
        self.assertIn("amount > 500", claim_gate)
        self.assertIn("NOT = { has_ai_expansion_plan = yes }", claim_gate)

        economy = economy_path.read_text(encoding="utf-8")
        self.assertIn("Stellar AI Director consumer goods income repair 0-5", economy)
        self.assertIn("Stellar AI Director colony alloy income repair 0-5", economy)
        self.assertIn("Stellar AI Director fleet replacement alloy repair 0-9999", economy)
        base_plan = economy[: economy.index("\n\tsubplan = {")]
        self.assertNotIn("physics_research", base_plan)
        approved_naval_subplans = {
            "Stellar AI Director militarist conquest fleet reserve",
            "Stellar AI Director raiding pop acquisition reserve",
            "Stellar AI Director hostile fauna clearance reserve",
        }
        research_runway_subplans = {
            "Stellar AI Director safe research baseline",
            "Stellar AI Director opening direct research route",
            "Stellar AI Director opening trade to research route",
            "Stellar AI Director opening growth to research route",
            "Stellar AI Director primary extermination economy",
            "Stellar AI Director primary gestalt_growth economy",
            "Stellar AI Director primary defensive economy",
            "Stellar AI Director primary research economy",
            "Stellar AI Director primary diplomatic economy",
            "Stellar AI Director lead secondary extermination economy",
            "Stellar AI Director lead secondary research economy",
            "Stellar AI Director lead secondary diplomatic economy",
            "Stellar AI Director militarist conquest fleet reserve",
            "Stellar AI Director raiding pop acquisition reserve",
            "Stellar AI Director defining machine exterminator economy",
            "Stellar AI Director defining rogue servitor economy",
            "Stellar AI Director defining assimilator economy",
            "Stellar AI Director defining devouring swarm economy",
            "Stellar AI Director defining inward perfection economy",
            "Stellar AI Director defining megacorp economy",
            "Stellar AI Director defining nomadic economy",
            "Stellar AI Director modded unlock research reserve",
            "Stellar AI Director ESC component resource readiness",
            "Stellar AI Director capped stockpile research conversion",
            "Stellar AI Director 2360 physics catchup",
            "Stellar AI Director 2360 society catchup",
            "Stellar AI Director 2360 engineering catchup",
            "Stellar AI Director NSC3 hull readiness reserve",
            "Stellar AI Director Planetary Diversity outpost reserve",
        }
        fleet_naval_mixed_subplans = {}
        research_runway_gates = (
            "staid_research_construction_priority_ready = yes",
            "staid_research_input_runway_safe = yes",
            "staid_research_minimum_input_runway_safe = yes",
        )
        subplans = economy.split("\n\tsubplan = {")[1:]
        research_bearing_subplans = {}
        for subplan in subplans:
            name_match = re.search(r'set_name = "([^"]+)"', subplan)
            self.assertIsNotNone(name_match, subplan[:240])
            subplan_name = name_match.group(1)
            if "naval_cap =" in subplan:
                self.assertIn(subplan_name, approved_naval_subplans)
            if any(
                resource in subplan
                for resource in ("physics_research", "society_research", "engineering_research")
            ):
                self.assertNotIn(subplan_name, research_bearing_subplans)
                research_bearing_subplans[subplan_name] = subplan

        expected_research_subplans = research_runway_subplans | set(fleet_naval_mixed_subplans)
        self.assertEqual(
            set(research_bearing_subplans),
            expected_research_subplans,
            "Research-bearing subplans require an explicit purpose classification.",
        )
        for subplan_name in research_runway_subplans:
            subplan = research_bearing_subplans[subplan_name]
            self.assertTrue(
                any(gate in subplan for gate in research_runway_gates),
                subplan_name,
            )
        for subplan_name, strategy in fleet_naval_mixed_subplans.items():
            subplan = research_bearing_subplans[subplan_name]
            self.assertIn(f"{strategy} = yes", subplan)
            strategy_gate = extract_top_level_object_text(triggers, strategy)
            self.assertIn("NOT = { staid_core_deficit_short_runway = yes }", strategy_gate)
            self.assertIn("staid_basic_economy_runway_safe = yes", strategy_gate)
        self.assertFalse(
            [row["object_id"] for row in dataset_job_pressure_override_rows() if row["pressure_family"] == "military_capacity"]
        )
        self.assertIn("staid_alloy_runway_safe = yes", triggers)

        claim_budget = claim_budget_path.read_text(encoding="utf-8")
        general_claims = extract_top_level_object_text(claim_budget, "influence_expenditure_claims")
        self.assertIn("weight = 0.20", general_claims)
        self.assertIn("factor = 3", general_claims)
        self.assertIn("staid_influence_claim_pressure = yes", general_claims)

    def test_dataset_job_pressure_rows_are_build_plan_policy_consumable(self):
        self.assertTrue(BUILD_PLAN_CONSUMER_POLICY_CSV.exists())
        policy_rows = build_plan_consumer_policy_rows()
        building_policy = build_plan_consumer_policy_buildings(policy_rows)
        selected_object_policy_rows = build_plan_consumer_policy_selected_object_rows(policy_rows)
        selected_objects = set(selected_object_policy_rows)

        rows = dataset_job_pressure_override_rows()
        self.assertTrue(rows)
        self.assertTrue([row for row in rows if row["object_type"] == "building"])

        disallowed = []
        for row in rows:
            if not build_plan_consumer_policy_allows_dataset_object(
                row,
                building_policy,
                selected_objects,
                selected_object_policy_rows,
            ):
                disallowed.append(f"{row['object_type']}:{row['object_id']}")

        self.assertFalse(disallowed[:25])

    def test_special_colony_objects_do_not_leak_into_generic_consumer_targets(self):
        special_classes = {"alderson_disk", "birch_world", "frameworld"}
        special_object_class = {}
        for path in (
            ECONOMIC_VALUATION_DATASET_CSV,
            NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV,
        ):
            with path.open(newline="", encoding="utf-8") as handle:
                for row in csv.DictReader(handle):
                    colony_class = row.get("colony_class", "")
                    if colony_class not in special_classes:
                        continue
                    object_id = row.get("object_id", "")
                    object_type = row.get("object_type", "")
                    token = f"{object_type}:{object_id}"
                    special_object_class[token] = colony_class

        leaks = []
        for policy_row in build_plan_consumer_policy_rows():
            if policy_row.get("can_consume_now") != "yes":
                continue
            target_id = policy_row.get("object_id", "")
            for item in str(policy_row.get("selected_objects", "")).split("|"):
                token = item.strip()
                colony_class = special_object_class.get(token)
                if colony_class and not target_id.endswith(f":{colony_class}"):
                    leaks.append(f"{target_id}->{token}:{colony_class}")

        self.assertFalse(leaks[:25])

    def test_high_scale_construction_plan_and_budget_pressure_are_generated(self):
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_14_minerals_planet_construction_budget.txt"
        building_pressure_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_13_dataset_job_pressure_buildings.txt"
        district_pressure_path = MOD_ROOT / "common" / "districts" / "zzzz_staid_13_dataset_job_pressure_districts.txt"
        zone_pressure_path = MOD_ROOT / "common" / "zones" / "zzzz_staid_13_dataset_job_pressure_zones.txt"
        for path in (economy_path, budget_path, building_pressure_path, district_pressure_path):
            self.assertTrue(path.exists(), f"Missing generated high-scale construction surface: {path}")
            parse_file(path)
        self.assertFalse(zone_pressure_path.exists(), "Zone full-object copies are runtime-unsafe and must not load.")
        economy = economy_path.read_text(encoding="utf-8")
        budget = budget_path.read_text(encoding="utf-8")
        pressure = (
            building_pressure_path.read_text(encoding="utf-8")
            + district_pressure_path.read_text(encoding="utf-8")
        )
        for marker in (
            "Stellar AI Director construction spenddown reserve",
            "Stellar AI Director unemployed pop construction catch-up",
            "Stellar AI Director open slot construction catch-up",
            "Stellar AI Director rich empire spend-down construction",
        ):
            self.assertIn(marker, economy)
        self.assertIn("staid_construction_spenddown_pressure = yes", economy)
        self.assertNotIn("empire_size =", economy)
        self.assertIn("staid_construction_spenddown_pressure = {", pressure + (
            MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        ).read_text(encoding="utf-8"))
        self.assertIn("modifier = { add = 0.75 staid_unemployment_construction_pressure = yes }", budget)
        self.assertIn("modifier = { add = 0.50 staid_construction_spenddown_pressure = yes }", budget)
        self.assertIn("resource_stockpile_compare = { resource = minerals value > 25000 }", budget)
        self.assertNotIn("factor = 40", budget)
        self.assertNotIn("factor = 35", budget)
        self.assertIn("ai_resource_production = {", pressure)
        self.assertNotIn("owner = { staid_construction_spenddown_pressure = yes }", pressure)
        self.assertNotIn("owner = { staid_basic_economy_runway_safe = yes", pressure)
        self.assertNotIn("factor = 0 owner = { AND = { staid_survival_mode = yes", pressure)
        trigger_text = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        construction_block = trigger_text[
            trigger_text.index("staid_construction_spenddown_pressure = {") : trigger_text.index(
                "staid_research_under_curve = {"
            )
        ]
        self.assertIn("NOT = { staid_catastrophic_collapse_mode = yes }", construction_block)
        self.assertNotIn("staid_recovery_mode", construction_block)
        unemployment_block = extract_top_level_object_text(
            trigger_text, "staid_unemployment_construction_pressure"
        )
        self.assertIn("any_owned_planet = { num_unemployed > 0 }", unemployment_block)
        self.assertNotIn("free_jobs", unemployment_block)
        unemployed_plan = _economic_subplan_block(
            economy, "Stellar AI Director unemployed pop construction catch-up"
        )
        self.assertIn(
            "staid_unemployment_construction_pressure = yes", unemployed_plan
        )
        self.assertNotIn("free_jobs", unemployed_plan)

    def test_staid_scripted_trigger_graph_has_no_cycles(self):
        self.assertEqual(validate_staid_scripted_trigger_cycles(MOD_ROOT), [])

    def test_scripted_trigger_cycle_validation_crosses_files_and_reports_owners(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mod_root = Path(temp_dir)
            trigger_root = mod_root / "common" / "scripted_triggers"
            trigger_root.mkdir(parents=True)
            (trigger_root / "a.txt").write_text(
                "staid_test_a = { staid_test_b = yes }\n", encoding="utf-8"
            )
            (trigger_root / "nested").mkdir()
            (trigger_root / "nested" / "b.txt").write_text(
                "staid_test_b = { staid_test_a = yes }\n", encoding="utf-8"
            )

            errors = validate_staid_scripted_trigger_cycles(mod_root)

            self.assertEqual(len(errors), 1)
            self.assertIn(
                "staid_test_a -> staid_test_b -> staid_test_a", errors[0]
            )
            self.assertIn("common/scripted_triggers/a.txt", errors[0])
            self.assertIn("common/scripted_triggers/nested/b.txt", errors[0])

    def test_scripted_trigger_cycle_validation_catches_self_cycles_and_duplicates(
        self,
    ):
        with tempfile.TemporaryDirectory() as temp_dir:
            mod_root = Path(temp_dir)
            trigger_root = mod_root / "common" / "scripted_triggers"
            trigger_root.mkdir(parents=True)
            (trigger_root / "one.txt").write_text(
                "staid_self = { staid_self = yes }\n"
                "staid_duplicate = { always = yes }\n",
                encoding="utf-8",
            )
            (trigger_root / "two.txt").write_text(
                "staid_duplicate = { always = no }\n", encoding="utf-8"
            )

            errors = validate_staid_scripted_trigger_cycles(mod_root)

            self.assertTrue(
                any("staid_self -> staid_self" in error for error in errors)
            )
            self.assertTrue(
                any(
                    "Duplicate staid scripted trigger staid_duplicate" in error
                    and "one.txt" in error
                    and "two.txt" in error
                    for error in errors
                )
            )

    def test_july7_inventory_and_static_validation_notes_are_generated(self):
        for path in (GENERATED_VERSION_INVENTORY_MD, MOD_STACK_COMPATIBILITY_MD, MANUAL_STATIC_VALIDATION_MD):
            self.assertTrue(path.exists(), f"Missing generated July 7 note: {path}")
            text = path.read_text(encoding="utf-8")
            self.assertIn("Generated by `tools/generate_stellar_ai_director_patch.py`", text)
        inventory = GENERATED_VERSION_INVENTORY_MD.read_text(encoding="utf-8")
        self.assertIn("4.4.5", inventory)
        self.assertIn("4.4.4", inventory)
        self.assertIn("v4.4.*", inventory)
        compatibility = MOD_STACK_COMPATIBILITY_MD.read_text(encoding="utf-8")
        self.assertIn("computed scripted triggers", compatibility)
        validation = MANUAL_STATIC_VALIDATION_MD.read_text(encoding="utf-8")
        self.assertIn("no Stellaris launch", validation)

    def test_stockpile_waste_and_low_research_activate_surplus_sink(self):
        state = EmpireState(
            incomes={
                "energy": 200,
                "alloys": 80,
                "trade": 20,
                "minerals": 900,
                "food": 300,
                "consumer_goods": 300,
                "physics_research": 500,
                "society_research": 500,
                "engineering_research": 700,
            },
            stockpiles={
                "minerals": 82000,
                "food": 82000,
                "consumer_goods": 65000,
            },
            research_sink_available=True,
        )
        self.assertTrue(resource_waste_pressure(state))
        self.assertTrue(research_under_curve(state, years_passed=165))
        self.assertTrue(surplus_sink_pressure(state))

    def test_generated_research_and_market_safety_surfaces_cover_runtime_failures(self):
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        market_events = (MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt").read_text(
            encoding="utf-8"
        )
        market_values = (MOD_ROOT / "common" / "script_values" / "zzz_staid_roi_values.txt").read_text(
            encoding="utf-8"
        )
        for marker in (
            "staid_resource_waste_pressure",
            "resource_stockpile_compare = { resource = minerals value > 25000 }",
            "resource_stockpile_compare = { resource = consumer_goods value > 18000 }",
            "staid_consumer_goods_runway_safe",
            "staid_energy_runway_safe",
            "staid_mineral_runway_safe",
            "staid_alloy_colony_runway_safe",
            "staid_food_colony_runway_safe",
            "staid_food_runway_safe",
            "staid_energy_two_month_runway_unsafe",
            "has_monthly_income = { resource = energy value <= -500 }",
            "resource_stockpile_compare = { resource = energy value < 1000 }",
            "staid_consumer_goods_two_month_runway_unsafe = yes",
            "staid_research_input_runway_safe",
            "staid_research_minimum_input_runway_safe",
            "staid_research_construction_priority_ready",
            "Stellar AI Director energy income repair 0-5",
            "Stellar AI Director mineral income repair 50+",
            "Stellar AI Director consumer goods income repair 0-5",
            "Stellar AI Director colony alloy income repair 50+",
            "Stellar AI Director food operating-float repair 0-5",
            "Stellar AI Director fleet replacement alloy repair 1000000+",
            "Stellar AI Director bio-ship replacement food repair 1000000+",
            "staid_research_under_curve",
            "Stellar AI Director capped stockpile research conversion",
            "Stellar AI Director 2360 engineering catchup",
            "value:staid_market_sell_value|RESOURCE|minerals|AMOUNT|5000|",
            "value:staid_market_sell_value|RESOURCE|giga_sr_sentient_metal|AMOUNT|250|",
            "staid_market_sell_value = {",
            "trade_type = market_sell",
            "resource_stockpile_percent = { resource = minerals value >= 0.9 }",
            "country_near_tangible_resource_cap = yes",
            "staid_high_scale_snowball_pressure",
        ):
            self.assertIn(marker, triggers + economy + market_events + market_values)

        self.assertNotIn("Stellar AI Director megastructure spam reserve", economy)

        generated_runtime_text = "\n".join(
            path.read_text(encoding="utf-8")
            for root in (MOD_ROOT / "common", MOD_ROOT / "events")
            for path in root.rglob("*.txt")
        )
        self.assertNotIn(
            "stellarai_market_",
            generated_runtime_text,
            "The Director must not depend on the separately authored Stellar AI mod.",
        )
        self.assertNotIn("trade_type = market_buy", generated_runtime_text)
        self.assertNotIn("market_buy_cost", generated_runtime_text)
        self.assertNotIn(
            "resource_stockpile_percent = { resource = nanites",
            market_events,
            "Nanites are non-tradable and have no maximum stockpile in Stellaris 4.4.4.",
        )
        self.assertNotIn(
            "value:staid_market_sell_value|RESOURCE|nanites|",
            market_events,
            "Cap-breaker sales may only include market-tradable resources with a finite maximum.",
        )
        for scripted_outpost_marker in (
            "staid_economy_safety.5",
            "staid_outpost_order_months",
            "staid_outpost_retry_backoff",
            "has_fleet_order = build_orbital_station_order",
        ):
            self.assertNotIn(
                scripted_outpost_marker,
                generated_runtime_text,
                "The Director must leave constructor outpost orders to the native AI planner.",
            )
        repair_section = economy[
            economy.index("# Relative repair plans require both earned monthly income")
            : economy.index('set_name = "Stellar AI Director primary extermination economy"')
        ]
        self.assertNotIn(
            "\t\t\ttrade =",
            repair_section,
            "Core deficit repair must request domestic resource income, not market currency.",
        )

    def test_market_cap_breaker_resources_are_tradable_and_have_finite_caps(self):
        resource_roots = (
            STELLARIS_INSTALL_ROOT / "common" / "strategic_resources",
            mod_source_root_for_id("1121692237") / "common" / "strategic_resources",
        )
        source_text = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for root in resource_roots
            for path in sorted(root.glob("*.txt"))
        )

        for resource, _reserve, _amount, _extra_limit in MARKET_CAP_BREAKER_SALES:
            with self.subTest(resource=resource):
                resource_block = extract_top_level_object_text(source_text, resource)
                self.assertRegex(resource_block, r"(?m)^\s*tradable\s*=\s*yes\s*$")
                self.assertRegex(resource_block, r"(?m)^\s*max\s*=\s*[1-9][0-9]*(?:\.[0-9]+)?\s*$")

    def test_director_does_not_auto_confirm_gigas_startup_settings(self):
        forbidden_paths = (
            MOD_ROOT / "common" / "on_actions" / "zzz_staid_load_proof_on_actions.txt",
            MOD_ROOT / "common" / "on_actions" / "zzzz_staid_gigas_startup_unblock_on_actions.txt",
            MOD_ROOT / "events" / "zzz_staid_load_proof_events.txt",
            MOD_ROOT / "events" / "zzzz_staid_gigas_startup_unblock_events.txt",
            MOD_ROOT / "localisation" / "english" / "staid_load_proof_l_english.yml",
        )
        for path in forbidden_paths:
            self.assertFalse(path.exists(), f"Stellar AI Director must not ship startup test artifacts: {path}")
        forbidden_markers = {
            "giga_preset_gigas_experience",
            "giga_menu.1111",
            "STELLAR_AI_DIRECTOR_GIGAS_STARTUP_UNBLOCK",
            "STELLAR_AI_DIRECTOR_LOAD_PROOF",
            "staid_gigas_startup",
            "staid_load_proof",
        }
        live_text = "\n".join(
            path.read_text(encoding="utf-8")
            for root in (MOD_ROOT / "common", MOD_ROOT / "events")
            for path in root.rglob("*.txt")
        )
        for marker in forbidden_markers:
            self.assertNotIn(marker, live_text)

    def test_mem_surveyor_outpost_gate_preserves_targeted_native_exception_only(self):
        outpost_path = (
            MOD_ROOT / "common" / "ship_sizes" / "zzzzz_staid_17_mem_surveyor_outpost_compat.txt"
        )
        event_path = MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt"
        mem_event_path = Path(r"C:\Steam\steamapps\workshop\content\281990\727000451\events\mem_surveyor.txt")
        active_parent_path = Path(
            r"C:\Steam\steamapps\workshop\content\281990\3250900527\common\ship_sizes\sbx_3_0_starbases.txt"
        )
        parse_file(outpost_path)
        parse_file(event_path)
        outpost = outpost_path.read_text(encoding="utf-8")
        events = event_path.read_text(encoding="utf-8")
        mem_events = mem_event_path.read_text(encoding="utf-8-sig")

        self.assertIn(
            f"# Source: {active_parent_path.as_posix()}",
            outpost,
            "The compatibility override must be generated from the active Starbase Extended winner.",
        )
        generated_block = extract_top_level_object_text(outpost, "starbase_outpost")
        active_parent_block = extract_top_level_object_text(
            active_parent_path.read_text(encoding="utf-8-sig"),
            "starbase_outpost",
        )
        self.assertEqual(
            re.sub(
                r"\s+",
                "",
                remove_top_level_child_block(generated_block, "possible_construction"),
            ),
            re.sub(
                r"\s+",
                "",
                remove_top_level_child_block(active_parent_block, "possible_construction"),
            ),
            "Only possible_construction may differ from the active outpost parent.",
        )

        for marker in (
            "starbase_outpost = {",
            "from = { is_ai = no }",
            "has_star_flag = mem_surveyor_home_system",
            "has_carrier_flag = mem_surveyor_alkree_homeworld",
            "has_modifier = mem_surveyor_alkree_homeworld",
        ):
            self.assertIn(marker, outpost)
        self.assertNotIn("mem_surveyor_found_alkree_homeworld", outpost)
        self.assertNotIn("mem_surveyor_studied_ruins", outpost)
        homeworld_start = mem_events.index("\tid = mem_surveyor.300")
        homeworld_resolution = mem_events[
            homeworld_start : mem_events.index("\tid = mem_surveyor.303", homeworld_start)
        ]
        for marker in (
            "modifier = mem_surveyor_alkree_homeworld",
            "days = -1",
            "id = mem_surveyor.301",
            "has_research_station = yes",
            "days = 3600",
        ):
            self.assertIn(
                marker,
                homeworld_resolution,
                "The targeted construction gate must release on MEM's reachable anomaly-resolution state.",
            )
        for marker in (
            "id = staid_economy_safety.5",
            "has_fleet_order = build_orbital_station_order",
            "staid_outpost_order_months",
            "staid_outpost_retry_backoff",
            "clear_orders = yes",
        ):
            self.assertNotIn(
                marker,
                events,
                "The targeted MEM construction restriction must not grow into a generic order-cancellation watchdog.",
            )

        clear_order_files = [
            path
            for root in (MOD_ROOT / "common", MOD_ROOT / "events")
            for path in root.rglob("*.txt")
            if "clear_orders" in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(clear_order_files, [])

    def test_boss_defeat_escalation_uses_boss_lane_without_weakening_normal_wars(self):
        on_action_path = MOD_ROOT / "common" / "on_actions" / "zzzz_staid_boss_defeat_escalation_on_actions.txt"
        event_path = MOD_ROOT / "events" / "zzzz_staid_boss_defeat_escalation_events.txt"
        defines_path = MOD_ROOT / "common" / "defines" / "zzzz_staid_14_high_scale_ai_defines.txt"
        for path in (on_action_path, event_path, defines_path):
            parse_file(path)

        on_action = on_action_path.read_text(encoding="utf-8")
        event = event_path.read_text(encoding="utf-8")
        defines = defines_path.read_text(encoding="utf-8")
        self.assertIn("on_space_battle_lost = {", on_action)
        self.assertIn("staid_boss_safety.1", on_action)
        self.assertNotIn("on_monthly_pulse", on_action)
        for marker in (
            "is_ai = yes",
            "exists = fromfromfrom",
            "has_fleet_flag = eeloofleet",
            "has_fleet_flag = legendary_guardian_fleet",
            "NOT = { has_fleet_flag = staid_escalated_ultra_boss }",
            "set_fleet_settings = {",
            "spawn_debris = no",
            "is_ultra_boss = yes",
            "set_fleet_flag = staid_escalated_ultra_boss",
        ):
            self.assertIn(marker, event)
        self.assertIn("ENEMY_FLEET_POWER_MULT = 1.2", defines)
        self.assertIn("BOSS_MILITARY_POWER = 100000", defines)
        self.assertIn("ULTRA_BOSS_MILITARY_POWER = 500000", defines)

    def test_route_overrides_carry_source_local_variables(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        technology_text = technology_path.read_text(encoding="utf-8")
        megastructure_text = megastructure_path.read_text(encoding="utf-8")
        for marker in ("@tier4cost4 = 28000", "@tier5weight3 = 20"):
            self.assertIn(marker, technology_text)
        for marker in ("@giga_mega_unity_cost", "@giga_giga_unity_cost"):
            self.assertIn(marker, megastructure_text)
        self.assertEqual(generated_unresolved_at_variable_rows(MOD_ROOT), [])

    def test_megastructure_route_weights_use_country_from_scope(self):
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        parse_file(megastructure_path)
        megastructure_text = megastructure_path.read_text(encoding="utf-8")
        macro_test_site_block = megastructure_text[
            megastructure_text.index("macro_test_site_3 = {") : megastructure_text.index("atmosphere_shredder_0 = {")
        ]
        for marker in (
            "modifier = { factor = 0 from = { staid_survival_mode = yes } }",
            "modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }",
            "modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }",
            "modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }",
            "modifier = { factor = 3 from = { staid_research_under_curve = yes } }",
        ):
            self.assertIn(marker, macro_test_site_block)
        for marker in (
            "modifier = { factor = 0 staid_survival_mode = yes }",
            "modifier = { factor = 0 NOT = { staid_science_kilo_build_priority_ready = yes } }",
            "modifier = { factor = 4 staid_science_kilo_build_priority_ready = yes }",
            "modifier = { factor = 4 has_technology = giga_tech_engineering_test_site }",
            "modifier = { factor = 3 staid_research_under_curve = yes }",
        ):
            self.assertNotIn(marker, macro_test_site_block)

    def test_research_and_pop_assembly_strategy_does_not_emit_inactive_building_ai_weights(self):
        research_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_06_research_infrastructure_buildings.txt"
        research_district_path = MOD_ROOT / "common" / "districts" / "zzzz_staid_06_research_infrastructure_districts.txt"
        pop_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_07_pop_assembly_buildings.txt"
        self.assertFalse(research_path.exists())
        self.assertFalse(research_district_path.exists())
        self.assertFalse(pop_path.exists())
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        economy = economy_path.read_text(encoding="utf-8")
        self.assertIn("Stellar AI Director safe research baseline", economy)
        self.assertIn("staid_research_construction_priority_ready = yes", economy)

    def test_habitat_route_override_repairs_gigas_spawn_effect_parameters(self):
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        parse_file(megastructure_path)
        megastructure_text = megastructure_path.read_text(encoding="utf-8")
        habitat_block = megastructure_text[
            megastructure_text.index("habitat_central_complex = {") : megastructure_text.index(
                "interstellar_habitat_0 = {"
            )
        ]
        self.assertIn("spawn_habitat_effect = {", habitat_block)
        self.assertIn("HABITAT_OWNER = root", habitat_block)
        self.assertIn("TARGET_PLANET = event_target:target_planet", habitat_block)
        self.assertNotIn("spawn_habitat_effect = {\n                DISTANCE =", habitat_block)

    def test_gigas_habitat_compat_effects_fail_closed_on_removed_orbital_ship_sizes(self):
        scripted_effects_path = (
            MOD_ROOT / "common" / "scripted_effects" / "zzz_staid_gigas_habitat_compat_effects.txt"
        )
        parse_file(scripted_effects_path)
        text = scripted_effects_path.read_text(encoding="utf-8")
        for marker in (
            "science_kilo_update_orbital_effect = {",
            "giga_dismantle_science_kilo_effect = {",
            "always = no # removed stale major_orbital_resource ship-size probe",
            "always = no # removed stale minor_orbital_resource ship-size probe",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("is_ship_size = major_orbital_resource", text)
        self.assertNotIn("is_ship_size = minor_orbital_resource", text)
        self.assertNotIn("is_ship_size = major_orbital", text)
        self.assertNotIn("is_ship_size = minor_orbital", text)
        self.assertNotIn("is_ship_size = habitat_major_orbital", text)
        self.assertNotIn("is_ship_size = habitat_minor_orbital", text)

    def test_ai_budget_overrides_do_not_emit_unsupported_ai_weight_blocks(self):
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_08_site_limited_expansion_ai_budget.txt"
        parse_file(budget_path)
        text = budget_path.read_text(encoding="utf-8")
        self.assertIn("influence_expenditure_claims = {", text)
        self.assertIn("weight = {", text)
        self.assertNotIn("ai_weight = {", text)

    def test_starbase_route_weights_use_owner_country_scope(self):
        starbase_path = (
            MOD_ROOT / "common" / "starbase_buildings" / "zzzz_staid_05_starbase_defense_starbase_buildings.txt"
        )
        module_path = MOD_ROOT / "common" / "starbase_modules" / "zzzz_staid_05_starbase_defense_starbase_modules.txt"
        parse_file(starbase_path)
        parse_file(module_path)
        text = starbase_path.read_text(encoding="utf-8")
        module_text = module_path.read_text(encoding="utf-8")
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        self.assertIn("modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }", text)
        self.assertIn("modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }", text)
        self.assertIn("modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }", text)
        self.assertNotIn("modifier = { factor = 0 owner = { staid_survival_mode = yes } }", text)
        self.assertNotIn("modifier = { factor = 0 staid_survival_mode = yes }", text)
        self.assertIn("staid_militarist_conquest_strategy = yes", triggers)
        self.assertIn("staid_static_defense_threat_window = {", triggers)
        self.assertIn("NOT = { staid_core_deficit_short_runway = yes }", triggers)
        self.assertIn("NOT = { staid_recovery_mode = yes }", triggers)
        self.assertIn("staid_starbase_defense_economy_safe = yes", triggers)
        self.assertIn("highest_threat > 25", triggers)
        self.assertIn("staid_homeland_under_attack = yes", triggers)
        self.assertIn("staid_static_defense_threat_window = yes", triggers)
        economy_gate = extract_top_level_object_text(triggers, "staid_starbase_defense_economy_safe")
        threat_window = extract_top_level_object_text(triggers, "staid_static_defense_threat_window")
        defense_ready = extract_top_level_object_text(triggers, "staid_static_defense_investment_ready")
        self.assertIn("NOT = { staid_core_deficit_short_runway = yes }", economy_gate)
        self.assertIn("NOT = { staid_recovery_mode = yes }", economy_gate)
        self.assertIn("staid_security_existential = yes", economy_gate)
        self.assertIn("staid_homeland_under_attack = yes", threat_window)
        self.assertIn("staid_aggressive_fleet_pressure = yes", threat_window)
        self.assertIn("highest_threat > 25", threat_window)
        self.assertIn("staid_starbase_defense_economy_safe = yes", defense_ready)
        self.assertIn("staid_static_defense_threat_window = yes", defense_ready)
        self.assertNotIn("staid_aggressive_fleet_pressure = yes", defense_ready)
        self.assertNotIn("staid_militarist_conquest_strategy = yes", defense_ready)
        self.assertNotIn("staid_high_scale_snowball_pressure = yes", defense_ready)
        self.assertIn("alloys = 2200", economy)
        self.assertNotIn("naval_cap = 1000", economy)
        self.assertIn("Stellar AI Director crisis starbase reserve", economy)
        self.assertIn("staid_starbase_defense_economy_safe = yes", economy)
        for marker in (
            "esc_starbase_reactor = {",
            "adv_starbase_defenses = {",
            "reinforced_defenses = {",
            "strategic_defenses = {",
        ):
            self.assertIn(marker, text)
        for marker in (
            "gun_battery = {",
            "missile_battery = {",
            "hangar_bay = {",
            "large_battery = {",
            "armor_module = {",
            "orbital_ring_gun_battery = {",
            "orbital_ring_missile_battery = {",
            "orbital_ring_hangar_bay = {",
            "orbital_ring_large_gun_battery = {",
            "orbital_ring_armor_module = {",
        ):
            self.assertIn(marker, module_text)
        self.assertIn(
            "modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }",
            module_text,
        )
        self.assertIn("modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }", module_text)
        for object_id in ("gun_battery", "missile_battery", "orbital_ring_gun_battery", "orbital_ring_missile_battery"):
            block = extract_top_level_object_text(module_text, object_id)
            depth = 0
            top_level_potentials = 0
            for line in block.splitlines():
                if depth == 1 and re.match(r"^\s*potential\s*=", line):
                    top_level_potentials += 1
                depth += line.count("{") - line.count("}")
            self.assertEqual(top_level_potentials, 1, f"{object_id} should merge duplicate top-level potential blocks")

    def test_threat_response_stateful_runtime_is_retired(self):
        retired_paths = (
            MOD_ROOT / "common" / "script_values" / "zzz_staid_threat_response_values.txt",
            MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_threat_response_triggers.txt",
            MOD_ROOT / "common" / "on_actions" / "zzz_staid_threat_response_on_actions.txt",
            MOD_ROOT / "events" / "zzz_staid_threat_response_events.txt",
        )
        for path in retired_paths:
            self.assertFalse(path.exists(), f"retired threat-response artifact regenerated: {path}")

        runtime_text = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for root in (MOD_ROOT / "common", MOD_ROOT / "events")
            for path in root.rglob("*.txt")
        )
        for forbidden in (
            "on_war_beginning",
            "namespace = staid_tr",
            "id = staid_tr.1",
            "set_timed_country_flag = { flag = staid_tr_",
            "set_timed_relation_flag = { who = from flag = staid_tr_",
            "has_country_flag = staid_tr_defensive_readiness_low",
            "staid_tr_foreign_affairs_safe",
            "Stellar AI Director threat readiness reserve",
        ):
            self.assertNotIn(forbidden, runtime_text)
        self.assertEqual(validate_threat_response_contract(), [])

    def test_threat_response_save_compatibility_ids_are_inert(self):
        opinion_path = MOD_ROOT / "common" / "opinion_modifiers" / "zzz_staid_threat_response_opinions.txt"
        localisation_path = MOD_ROOT / "localisation" / "english" / "staid_threat_response_l_english.yml"
        parse_file(opinion_path)
        opinions = opinion_path.read_text(encoding="utf-8")
        localisation = localisation_path.read_text(encoding="utf-8-sig")
        self.assertTrue(localisation_path.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertTrue(THREAT_OPINION_VALUES)
        self.assertEqual(set(THREAT_OPINION_VALUES.values()), {0})
        for key in THREAT_OPINION_VALUES:
            block = extract_top_level_object_text(opinions, f"staid_tr_{key}")
            self.assertRegex(block, r"(?m)^\s*opinion\s*=\s*0\s*$")
            self.assertIn(f"staid_tr_{key}:0", localisation)

    def test_gigas_habitat_zone_slot_compat_districts_cover_new_habitat_route(self):
        district_path = (
            MOD_ROOT / "common" / "districts" / "zzzz_staid_09_gigas_habitat_zone_slot_compat_districts.txt"
        )
        parse_file(district_path)
        text = district_path.read_text(encoding="utf-8")
        expected_slots = {
            "district_giga_hab_city": "slot_habitat_01",
            "district_giga_hab_hive": "slot_habitat_01",
            "district_giga_hab_nexus": "slot_habitat_01",
            "district_giga_hab_science": "slot_habitat_research",
            "district_giga_hab_scavenger": "slot_habitat_minerals",
            "district_giga_orbital_farming": "slot_city_01",
            "district_giga_orbital_sanctuary": "slot_city_government",
            "district_giga_orbital_preserve": "slot_city_01",
            "district_giga_orbital_logistics": "slot_city_government",
        }
        for object_id, slot in expected_slots.items():
            block = text[text.index(f"{object_id} = {{") :]
            block = block[: block.find("\n}\n") + 3]
            self.assertIn("zone_slots = {", block)
            self.assertIn(slot, block)
        self.assertNotIn("is_capped_by_modifier", text)

    def test_route_research_weights_do_not_self_gate_unlock_targets(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        technology_text = technology_path.read_text(encoding="utf-8")
        mega_shipyard_block = technology_text[
            technology_text.index("tech_mega_shipyard = {") : technology_text.index("giga_tech_planet_assembly = {")
        ]
        self.assertIn("# policy_route = mega_shipyard_core", mega_shipyard_block)
        self.assertIn("staid_core_unlock_research_priority_ready = yes", mega_shipyard_block)
        self.assertNotIn("staid_shipyard_expansion_ready = yes", mega_shipyard_block)

    def test_gigas_progression_overrides_cover_deep_unlocks_and_build_gates(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        text = (
            technology_path.read_text(encoding="utf-8")
            + megastructure_path.read_text(encoding="utf-8")
            + trigger_path.read_text(encoding="utf-8")
        )
        for marker in (
            "giga_tech_war_moon_1 = {",
            "giga_tech_war_moon_2 = {",
            "giga_tech_war_system_6 = {",
            "tech_nm_utilization_1 = {",
            "staid_war_moon_research_priority_ready = yes",
            "staid_systemcraft_research_priority_ready = yes",
            "staid_gigas_special_resource_unlock_ready = yes",
            "staid_war_moon_build_priority_ready = yes",
            "staid_systemcraft_build_priority_ready = yes",
            "has_ascension_perk = ap_celestial_printing",
        ):
            self.assertIn(marker, text)

    def test_phase_machine_and_modded_conversion_gates_are_generated(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        parse_file(trigger_path)
        parse_file(economy_path)
        economy = economy_path.read_text(encoding="utf-8")
        text = technology_path.read_text(encoding="utf-8") + trigger_path.read_text(encoding="utf-8") + economy
        for marker in (
            "staid_phase_mega_engineering_rush = {",
            "staid_phase_galactic_wonders_entry = {",
            "staid_phase_gigastructural_constructs_rush = {",
            "staid_phase_planetcraft_rush = {",
            "staid_phase_systemcraft_escalation = {",
            "staid_phase_fleet_conversion_repeatables = {",
            "staid_nsc3_capital_hull_unlock_ready = {",
            "staid_esc_component_unlock_ready = {",
            "staid_advanced_component_resource_support_ready = {",
            "staid_modded_fleet_conversion_ready = {",
            "NOT = { staid_core_deficit_short_runway = yes }",
            "staid_trade_fleet_capacity_safe = yes",
            "resource = sr_dark_matter value > 1",
            "resource = giga_sr_sentient_metal value > 1",
            "staid_nsc3_capital_hull_unlock_ready = yes",
            "staid_esc_component_unlock_ready = yes",
            "NOT = { staid_advanced_component_resource_support_ready = yes }",
            "has_technology = tech_Flagship_1",
            "has_technology = esc_tech_dark_matter_power_core_2",
            'set_name = "Stellar AI Director NSC3 hull readiness reserve"',
        ):
            self.assertIn(marker, text)
        nsc3_hull_block = economy[
            economy.index('set_name = "Stellar AI Director NSC3 hull readiness reserve"') : economy.index(
                'set_name = "Stellar AI Director planetary capacity reserve"'
            )
        ]
        for marker in (
            "staid_nsc3_capital_hull_unlock_ready = yes",
            "has_technology = tech_battleships",
            "has_technology = tech_Carrier_1",
            "has_technology = tech_Dreadnought_1",
            "alloys = 900",
            "engineering_research = 900",
        ):
            self.assertIn(marker, nsc3_hull_block)
        self.assertNotIn("naval_cap =", nsc3_hull_block)

    def test_unity_to_research_paths_are_source_backed(self):
        traditions_path = MOD_ROOT / "common" / "traditions" / "zzzz_staid_02_perks_traditions_traditions.txt"
        categories_path = (
            MOD_ROOT
            / "common"
            / "tradition_categories"
            / "zzzz_staid_02_perks_traditions_tradition_categories.txt"
        )
        perks_path = MOD_ROOT / "common" / "ascension_perks" / "zzzz_staid_02_perks_traditions_ascension_perks.txt"
        parse_file(traditions_path)
        parse_file(categories_path)
        parse_file(perks_path)
        traditions_text = traditions_path.read_text(encoding="utf-8")
        categories_text = categories_path.read_text(encoding="utf-8")
        perks_text = perks_path.read_text(encoding="utf-8")
        combined = traditions_text + categories_text + perks_text
        for marker in (
            "# policy_route = research_diplomacy_core; source = common/tradition_categories/00_discovery.txt",
            "tradition_discovery = {",
            "# policy_route = research_diplomacy_core; source = common/tradition_categories/00_diplomacy.txt",
            "tradition_diplomacy = {",
            "tradition_supremacy = {",
            "tradition_prosperity = {",
            "tradition_adaptability = {",
            "tradition_mercantile = {",
            "tr_discovery_science_division = {",
            "tr_discovery_faith_in_science = {",
            "tr_diplomacy_the_federation = {",
            "tr_diplomacy_eminent_diplomats = {",
            "# policy_route = research_diplomacy_core; source = common/ascension_perks/00_ascension_perks.txt",
            "ap_technological_ascendancy = {",
            "# policy_route = economy_megastructure_core; source = common/ascension_perks/00_ascension_perks.txt",
            "ap_master_builders = {",
            "ap_galactic_wonders = {",
            "ap_gigastructural_constructs = {",
            "modifier = { factor = 0 NOT = { staid_research_diplomacy_priority_ready = yes } }",
            "modifier = { factor = 4 staid_research_diplomacy_priority_ready = yes }",
            "modifier = { factor = 0 NOT = { staid_core_unlock_research_priority_ready = yes } }",
        ):
            self.assertIn(marker, combined)

        category_cases = (
            ("tradition_discovery", "00_discovery.txt", "research_diplomacy_core", "staid_research_diplomacy_priority_ready"),
            ("tradition_diplomacy", "00_diplomacy.txt", "research_diplomacy_core", "staid_research_diplomacy_priority_ready"),
            ("tradition_supremacy", "00_supremacy.txt", "conquest_escape_route", "staid_aggressive_fleet_pressure"),
            ("tradition_prosperity", "00_prosperity.txt", "economy_megastructure_core", "staid_core_unlock_research_priority_ready"),
            ("tradition_adaptability", "00_adaptability.txt", "crowded_tall_route", "staid_planetary_capacity_growth_ready"),
            ("tradition_mercantile", "00_commerce.txt", "crowded_tall_route", "staid_planetary_capacity_growth_ready"),
        )
        for object_id, source_file, route_id, route_gate in category_cases:
            generated_block = extract_top_level_object_text(categories_text, object_id)
            source_block = extract_top_level_object_text(
                read_text(STELLARIS_INSTALL_ROOT / "common" / "tradition_categories" / source_file),
                object_id,
            )
            route_comment = f"\t\t# policy_route = {route_id}; preserve vanilla category and node selection\n"
            route_modifier = f"\t\tmodifier = {{ factor = 4 {route_gate} = yes }}\n"
            self.assertIn(route_comment.rstrip(), generated_block)
            self.assertIn(route_modifier.rstrip(), generated_block)
            self.assertEqual(
                "\n".join(
                    line.rstrip()
                    for line in generated_block.replace(route_comment, "").replace(route_modifier, "").splitlines()
                ).rstrip(),
                "\n".join(line.rstrip() for line in source_block.splitlines()).rstrip(),
                f"{object_id} must preserve every parent category rule except the additive route boost.",
            )
            for forbidden in (
                "staid_survival_mode",
                "staid_recovery_mode",
                f"NOT = {{ {route_gate} = yes }}",
                "years_passed >",
            ):
                self.assertNotIn(forbidden, generated_block)

        selectable_node_cases = (
            ("tr_discovery_to_boldly_go", "00_discovery.txt"),
            ("tr_discovery_databank_uplinks", "00_discovery.txt"),
            ("tr_discovery_science_division", "00_discovery.txt"),
            ("tr_discovery_polytechnic_education", "00_discovery.txt"),
            ("tr_discovery_faith_in_science", "00_discovery.txt"),
            ("tr_diplomacy_the_federation", "00_diplomacy.txt"),
            ("tr_diplomacy_entente_coordination", "00_diplomacy.txt"),
            ("tr_diplomacy_diplomatic_networking", "00_diplomacy.txt"),
            ("tr_diplomacy_direct_diplomacy", "00_diplomacy.txt"),
            ("tr_diplomacy_eminent_diplomats", "00_diplomacy.txt"),
        )
        route_comment = "\t\t# policy_route = research_diplomacy_core; preserve vanilla category and node selection\n"
        route_modifier = "\t\tmodifier = { factor = 4 staid_research_diplomacy_priority_ready = yes }\n"
        for object_id, source_file in selectable_node_cases:
            generated_block = extract_top_level_object_text(traditions_text, object_id)
            source_block = extract_top_level_object_text(
                read_text(STELLARIS_INSTALL_ROOT / "common" / "traditions" / source_file),
                object_id,
            )
            self.assertIn(route_comment.rstrip(), generated_block)
            self.assertIn(route_modifier.rstrip(), generated_block)
            self.assertEqual(
                "\n".join(
                    line.rstrip()
                    for line in generated_block.replace(route_comment, "").replace(route_modifier, "").splitlines()
                ).rstrip(),
                "\n".join(line.rstrip() for line in source_block.splitlines()).rstrip(),
                f"{object_id} must preserve every parent rule except the additive route boost.",
            )

        tradition_targets = {
            target["object_id"]
            for target in ROUTE_OVERRIDE_TARGETS
            if target["object_type"] == "tradition"
        }
        self.assertEqual(tradition_targets, {object_id for object_id, _ in selectable_node_cases})
        automatic_rewards = {
            "tr_discovery_adopt",
            "tr_discovery_finish",
            "tr_diplomacy_finish",
            "tr_supremacy_adopt",
            "tr_prosperity_adopt",
            "tr_adaptability_adopt",
            "tr_mercantile_adopt",
        }
        self.assertFalse(tradition_targets & automatic_rewards)
        for object_id in automatic_rewards:
            self.assertNotIn(f"{object_id} = {{", traditions_text)

        discovery_source = parse_pdx(
            read_text(STELLARIS_INSTALL_ROOT / "common" / "traditions" / "00_discovery.txt")
        )
        discovery_finish = block_assignments(discovery_source, "tr_discovery_finish")[0].value
        discovery_node = block_assignments(discovery_source, "tr_discovery_science_division")[0].value
        self.assertFalse(atlas_object_has_ai_signal(discovery_finish, "tradition"))
        self.assertTrue(atlas_object_has_ai_signal(discovery_node, "tradition"))
        with OBJECT_ATLAS_CSV.open(encoding="utf-8", newline="") as handle:
            atlas_by_id = {
                row["object_id"]: row
                for row in csv.DictReader(handle)
                if row["mod_id"] == "vanilla"
                and row["object_id"]
                in {
                    "tr_discovery_finish",
                    "tr_mercantile_adopt",
                    "tr_prosperity_adopt",
                    "tr_discovery_science_division",
                }
            }
        for object_id in ("tr_discovery_finish", "tr_mercantile_adopt", "tr_prosperity_adopt"):
            self.assertEqual(atlas_by_id[object_id]["source_has_ai_weight"], "no")
            self.assertEqual(atlas_by_id[object_id]["parent_ai_support"], "parent_ai_absent")
        self.assertEqual(atlas_by_id["tr_discovery_science_division"]["source_has_ai_weight"], "yes")
        self.assertNotIn(
            "modifier = { factor = 0 NOT = { staid_research_diplomacy_priority_ready = yes } }",
            traditions_text + categories_text,
        )
        self.assertFalse(
            [
                target
                for target in ROUTE_OVERRIDE_TARGETS
                if target["object_id"] == "unity_expenditure_traditions"
            ],
            "A 1-unity legal choice cannot be repaired by changing the tradition budget.",
        )
        vanilla_unity_budget = extract_top_level_object_text(
            read_text(STELLARIS_INSTALL_ROOT / "common" / "ai_budget" / "00_unity_budget.txt"),
            "unity_expenditure_traditions",
        )
        self.assertIn("weight = 0.8", vanilla_unity_budget)
        director_budget_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((MOD_ROOT / "common" / "ai_budget").glob("*.txt"))
        )
        self.assertNotIn("unity_expenditure_traditions = {", director_budget_text)
        reference_rows = collect_generated_reference_rows(MOD_ROOT)
        unresolved = [
            row
            for row in reference_rows
            if row["generated_file"]
            in {
                "common/tradition_categories/zzzz_staid_02_perks_traditions_tradition_categories.txt",
                "common/traditions/zzzz_staid_02_perks_traditions_traditions.txt",
                "common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt",
            }
            and row["reference_name"]
            in {"staid_research_diplomacy_priority_ready", "staid_core_unlock_research_priority_ready"}
            and row["status"] != "ok"
        ]
        self.assertEqual(unresolved, [])
        self.assertNotIn("generic unity hoard", combined.lower())
        self.assertNotIn("tr_discovery_finish = {", traditions_text + categories_text)
        self.assertNotIn("tr_diplomacy_finish = {", traditions_text + categories_text)

    def test_fleet_conversion_gates_require_deficit_safe_economy(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(trigger_path)
        text = trigger_path.read_text(encoding="utf-8")
        shipyard_block = text[
            text.index("staid_shipyard_payoff_ready = {") : text.index("staid_fleet_buildup_economy_safe = {")
        ]
        fleet_block = text[
            text.index("staid_fleet_buildup_economy_safe = {") : text.index("staid_resource_waste_pressure = {")
        ]
        for block in (shipyard_block, fleet_block):
            self.assertIn("NOT = { staid_catastrophic_collapse_mode = yes }", block)
            self.assertNotIn("staid_survival_mode = yes", block)
        self.assertIn("used_naval_capacity_percent < 1.60", shipyard_block)
        self.assertIn("has_monthly_income = { resource = alloys value > 80 }", shipyard_block)
        self.assertNotIn("staid_militarist_conquest_strategy = yes", shipyard_block)
        self.assertNotIn("staid_raiding_pop_growth_strategy = yes", shipyard_block)
        self.assertIn("NOT = { staid_core_deficit_short_runway = yes }", fleet_block)
        self.assertIn("staid_basic_economy_runway_safe = yes", fleet_block)
        self.assertIn("used_naval_capacity_percent < 1.40", fleet_block)
        self.assertNotIn("staid_aggressive_fleet_pressure = yes", fleet_block)
        self.assertNotIn("staid_militarist_conquest_strategy = yes", fleet_block)
        self.assertNotIn("staid_raiding_pop_growth_strategy = yes", fleet_block)
        self.assertNotIn("has_monthly_income = { resource = alloys value > 200 }", shipyard_block)
        self.assertIn("resource_stockpile_compare = { resource = alloys value >", shipyard_block)
        self.assertNotIn("staid_high_scale_snowball_pressure = yes", fleet_block)

    def test_support_economy_bridge_keeps_resource_bottlenecks_first_class(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        parse_file(trigger_path)
        parse_file(economy_path)
        text = trigger_path.read_text(encoding="utf-8")
        economy = economy_path.read_text(encoding="utf-8")
        alloy_block = text[text.index("staid_alloy_runway_safe = {") : text.index("staid_food_runway_safe = {")]
        basic_block = text[text.index("staid_basic_economy_runway_safe = {") : text.index("staid_trade_capacity_safe = {")]
        advanced_block = text[
            text.index("staid_advanced_component_resource_support_ready = {") : text.index(
                "staid_nsc3_capital_hull_unlock_ready = {"
            )
        ]
        megastructure_block = text[
            text.index("staid_megastructure_prep_ready = {") : text.index("staid_megastructure_commit_safe = {")
        ]
        for marker in (
            "staid_research_input_runway_safe = yes",
            "staid_food_runway_safe = yes",
            "staid_mineral_runway_safe = yes",
            "staid_alloy_runway_safe = yes",
        ):
            self.assertIn(marker, basic_block)
        for marker in (
            "staid_alloy_colony_runway_safe = yes",
            "staid_scaled_alloy_fleet_income_safe = yes",
            "staid_scaled_alloy_fleet_stockpile_safe = yes",
        ):
            self.assertIn(marker, alloy_block)
        for marker in (
            "NOT = { staid_core_deficit_short_runway = yes }",
            "staid_basic_economy_runway_safe = yes",
            "staid_trade_fleet_capacity_safe = yes",
            "has_monthly_income = { resource = volatile_motes value > 5 }",
            "has_monthly_income = { resource = sr_dark_matter value > 1 }",
            "has_monthly_income = { resource = giga_sr_negative_mass value > 1 }",
            "has_monthly_income = { resource = giga_sr_amb_megaconstruction value > 1 }",
        ):
            self.assertIn(marker, advanced_block)
        esc_marker = 'set_name = "Stellar AI Director ESC component resource readiness"'
        esc_marker_index = economy.index(esc_marker)
        esc_resource_block = economy[
            economy.rfind("\n\tsubplan = {", 0, esc_marker_index) : economy.index(
                "\n\tsubplan = {", esc_marker_index
            )
        ]
        for marker in (
            "optional = yes",
            "NOT = { staid_advanced_component_resource_support_ready = yes }",
            "has_technology = tech_dark_matter_power_core",
            "has_technology = esc_tech_dark_matter_power_core_2",
            "staid_phase_fleet_conversion_repeatables = yes",
            "sr_dark_matter = 3",
            "sr_zro = 3",
            "nanites = 3",
            "engineering_research = 600",
        ):
            self.assertIn(marker, esc_resource_block)
        self.assertNotIn("scaling =", esc_resource_block)
        for resource in ("volatile_motes", "exotic_gases", "rare_crystals"):
            self.assertNotRegex(esc_resource_block, rf"(?m)^\s*{resource}\s*=")
        self.assertIn("staid_trade_planetary_capacity_safe = yes", megastructure_block)
        self.assertNotIn("staid_high_scale_snowball_pressure = yes", megastructure_block)
        self.assertNotIn("Stellar AI Director generic trade sell", text)
        self.assertNotIn("Stellar AI Director generic trade buy", text)

    def test_research_infrastructure_relies_on_vanilla_hard_zone_gates_and_safe_plan_demand(self):
        buildings_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_06_research_infrastructure_buildings.txt"
        districts_path = MOD_ROOT / "common" / "districts" / "zzzz_staid_06_research_infrastructure_districts.txt"
        self.assertFalse(buildings_path.exists())
        self.assertFalse(districts_path.exists())
        economy = (
            MOD_ROOT
            / "common"
            / "economic_plans"
            / "zzzz_staid_additive_economic_plan.txt"
        ).read_text(encoding="utf-8")
        baseline_start = economy.index('set_name = "Stellar AI Director safe research baseline"')
        baseline_end = economy.find("\n\tsubplan = {", baseline_start)
        baseline = economy[baseline_start:baseline_end]
        self.assertIn("staid_research_construction_priority_ready = yes", baseline)
        self.assertIn("physics_research = 400", baseline)

    def test_packaged_stellarai_inline_script_dependencies_cover_generated_references(self):
        generated_text = "\n".join(path.read_text(encoding="utf-8") for path in (MOD_ROOT / "common").rglob("*.txt"))
        referenced_scripts = set(re.findall(r"script\s*=\s*\"?stellarai/([A-Za-z0-9_/-]+)\"?", generated_text))
        expected_scripts = set(STELLARAI_INLINE_SCRIPT_DEPENDENCIES)
        self.assertTrue(referenced_scripts.issubset(expected_scripts))
        for script_name in referenced_scripts:
            self.assertTrue(
                (MOD_ROOT / "common" / "inline_scripts" / "stellarai" / f"{script_name}.txt").exists(),
                f"Missing packaged Stellar AI inline script dependency: stellarai/{script_name}",
            )

    def test_unresolved_source_local_variables_are_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mod_root = Path(temp_dir)
            common = mod_root / "common" / "technology"
            common.mkdir(parents=True)
            (common / "broken.txt").write_text("tech_test = { cost = @missing_cost }\n", encoding="utf-8")
            self.assertEqual(
                generated_unresolved_at_variable_rows(mod_root),
                [
                    {
                        "generated_file": "common/technology/broken.txt",
                        "line": "1",
                        "variable": "@missing_cost",
                    }
                ],
            )

    def test_object_atlas_artifacts_are_static_valid(self):
        self.assertEqual(validate_object_atlas_artifacts(), [])
        for path in (OBJECT_ATLAS_CSV, DEPENDENCY_EDGES_CSV, AI_SUPPORT_MAP_CSV, POLICY_MATRIX_CSV):
            self.assertTrue(path.exists(), f"Missing generated atlas artifact: {path}")

    def test_object_atlas_contains_required_route_objects(self):
        atlas_text = OBJECT_ATLAS_CSV.read_text(encoding="utf-8")
        for marker in (
            "planetcraft",
            "systemcraft",
            "mega_shipyard",
            "esc_tech_dark_matter_power_core_2",
            "building_research_lab_1",
            "district_hab_science",
        ):
            self.assertIn(marker, atlas_text)

    def test_policy_matrix_references_atlas_objects(self):
        with OBJECT_ATLAS_CSV.open("r", encoding="utf-8", newline="") as handle:
            atlas_rows = list(csv.DictReader(handle))
        with POLICY_MATRIX_CSV.open("r", encoding="utf-8", newline="") as handle:
            policy_rows = list(csv.DictReader(handle))
        atlas_ids = {row["object_id"] for row in atlas_rows if row["validation_status"] == "ok"}
        self.assertTrue(policy_rows, "Policy matrix did not contain any rows.")
        missing = sorted({row["object_id"] for row in policy_rows if row["object_id"] not in atlas_ids})
        self.assertEqual(missing, [])
        obsolete_source_files = {
            "common\\buildings\\zzzz_staid_06_research_infrastructure_buildings.txt",
            "common\\buildings\\zzzz_staid_12_planetary_diversity_buildings.txt",
        }
        self.assertFalse(
            [row for row in policy_rows if row["source_file"] in obsolete_source_files],
            "Benefit policy matrix retained source-winner keys for deleted Director overrides.",
        )

    def test_strategic_subsystem_audit_is_complete_and_consumer_explicit(self):
        self.assertTrue(STRATEGIC_SUBSYSTEM_AUDIT_CSV.exists())
        self.assertTrue(STRATEGIC_SUBSYSTEM_AUDIT_MD.exists())
        rows = strategic_subsystem_audit_rows()
        self.assertEqual(len(rows), 28)
        self.assertEqual(len({row["subsystem_id"] for row in rows}), len(rows))
        required = {
            "data_pipeline",
            "resource_survival",
            "research_capacity",
            "colony_construction",
            "colony_designation",
            "budget_management",
            "influence_market",
            "territorial_expansion",
            "war_selection",
            "diplomacy_personality",
            "fleet_doctrine",
            "hostile_targets",
            "ship_design",
            "technology_routes",
            "ascension_strategy",
            "megastructure_strategy",
            "crisis_response",
            "starbase_defense",
            "invasion_bombardment",
            "machine_hive_gestalt",
            "genocidal_extremes",
            "pacifist_isolationist",
            "megacorp_trade",
            "nomad_arkship",
            "subjects_overlords",
            "special_origins",
            "compatibility_winners",
            "runtime_telemetry",
        }
        by_id = {row["subsystem_id"]: row for row in rows}
        self.assertEqual(set(by_id), required)
        self.assertEqual(by_id["war_selection"]["consumer_authority"], "mixed")
        self.assertEqual(by_id["subjects_overlords"]["consumer_authority"], "absent")
        self.assertEqual(by_id["runtime_telemetry"]["consumer_authority"], "unproven")
        self.assertNotIn("colony_automation", by_id["colony_construction"]["engine_consumer"])
        self.assertFalse([row for row in rows if not row["known_gap"] or not row["next_action"]])

        for row in rows:
            for artifact in (item.strip() for item in row["director_artifacts"].split(";")):
                if artifact == "none":
                    continue
                prefix, relative = artifact.split(":", 1)
                root = MOD_ROOT if prefix == "mod" else RESEARCH_ROOT
                self.assertIn(prefix, {"mod", "research"}, artifact)
                self.assertTrue((root / relative).exists(), f"Missing audit artifact {artifact}")

    def test_route_override_surfaces_cover_required_families(self):
        with (RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.csv").open(
            "r", encoding="utf-8", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        covered_routes = {row["route_id"] for row in rows}
        required_routes = {
            "mega_engineering_core",
            "mega_shipyard_core",
            "economy_megastructure_core",
            "early_kilo_economy_core",
            "science_kilo_snowball_core",
            "research_megastructure_core",
            "planetary_computer_research_core",
            "ring_world_growth_core",
            "storage_cap_core",
            "planetcraft_route",
            "war_moon_route",
            "systemcraft_route",
            "nsc3_capital_hull_route",
            "esc_component_route",
            "crowded_tall_route",
            "conquest_escape_route",
            "apex_site_preservation_core",
            "fallen_empire_benchmark_route",
            "research_diplomacy_core",
        }
        self.assertTrue(required_routes.issubset(covered_routes))
        for row in rows:
            generated_file = route_override_generated_file_path(row)
            self.assertTrue(generated_file.exists(), f"Missing route override file: {generated_file}")
            self.assertIn(row["object_id"], generated_file.read_text(encoding="utf-8"))
        self.assertTrue((RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.md").exists())

    def test_route_override_generated_file_resolution_ignores_captured_worktree_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            current_mod_root = Path(temp_dir) / "mods" / "StellarAIDirector"
            row = {
                "generated_folder": "technology",
                "file_key": "01_unlock_technology",
                "generated_file": (
                    "C:/Users/Admin/Documents/GIT/GameMods/StellarisMods/"
                    "mods/StellarAIDirector/common/technology/old.txt"
                ),
            }

            resolved = route_override_generated_file_path(row, current_mod_root)
            evidence_row = route_override_evidence_rows([row], current_mod_root)[0]

            self.assertEqual(
                resolved,
                current_mod_root
                / "common"
                / "technology"
                / "zzzz_staid_01_unlock_technology_technology.txt",
            )
            self.assertEqual(
                evidence_row["generated_file"],
                "common/technology/zzzz_staid_01_unlock_technology_technology.txt",
            )

    def test_snowball_checkpoint_routes_cover_research_surface_storage_and_early_kilos(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        claim_budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_08_site_limited_expansion_ai_budget.txt"
        federation_path = MOD_ROOT / "common" / "federation_types" / "zzzz_staid_15_research_diplomacy_federation_types.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(technology_path)
        parse_file(megastructure_path)
        parse_file(claim_budget_path)
        parse_file(federation_path)
        parse_file(trigger_path)
        text = (
            technology_path.read_text(encoding="utf-8")
            + megastructure_path.read_text(encoding="utf-8")
            + claim_budget_path.read_text(encoding="utf-8")
            + federation_path.read_text(encoding="utf-8")
            + trigger_path.read_text(encoding="utf-8")
        )
        for marker in (
            "tech_science_nexus = {",
            "tech_ring_world = {",
            "tech_orbital_arc_furnace = {",
            "giga_tech_asteroid_manufactory = {",
            "giga_tech_engineering_test_site = {",
            "giga_tech_macro_scale_weather_manipulation = {",
            "giga_tech_planetary_computer = {",
            "tech_robotic_workers = {",
            "tech_cloning = {",
            "giga_tech_kugelblitz = {",
            "giga_tech_matrioshka_brain_1 = {",
            "giga_tech_neutronium_gigaforge = {",
            "giga_tech_nidavellir = {",
            "giga_tech_interstellar_habitat = {",
            "giga_tech_stellar_ring_habitat = {",
            "think_tank_0 = {",
            "think_tank_3 = {",
            "ring_world_1 = {",
            "ring_world_3_intermediate = {",
            "kugelblitz_0 = {",
            "kugelblitz_3 = {",
            "habitat_central_complex = {",
            "interstellar_habitat_0 = {",
            "stellar_ring_habitat_0 = {",
            "orbital_arc_furnace_1 = {",
            "asteroid_manufactory_0 = {",
            "macro_test_site_0 = {",
            "macro_test_site_3 = {",
            "atmosphere_shredder_0 = {",
            "atmosphere_shredder_3 = {",
            "planetary_computer_0 = {",
            "planetary_computer_1 = {",
            "matrioshka_brain_0_o_star = {",
            "dyson_sphere_0_o_star = {",
            "neutronium_gigaforge_0 = {",
            "nidavellir_forge_0 = {",
            "influence_expenditure_claims = {",
            "influence_expenditure_claims_militarist = {",
            "influence_expenditure_claims_fanatic_militarist = {",
            "research_federation = {",
            "# policy_route = early_kilo_economy_core",
            "# policy_route = science_kilo_snowball_core",
            "# policy_route = research_megastructure_core",
            "# policy_route = planetary_computer_research_core",
            "# policy_route = ring_world_growth_core",
            "# policy_route = storage_cap_core",
            "# policy_route = apex_site_preservation_core",
            "# policy_route = conquest_escape_route",
            "staid_phase_early_kilo_economy = {",
            "staid_phase_science_kilo_snowball = {",
            "staid_phase_pop_assembly_snowball = {",
            "staid_phase_science_nexus_rush = {",
            "staid_phase_planetary_computer_research = {",
            "staid_phase_ring_world_growth = {",
            "staid_phase_storage_cap_expansion = {",
            "staid_phase_boxed_tall_habitat_escape = {",
            "staid_site_limited_expansion_ready = {",
            "staid_apex_site_preservation_ready = {",
            "staid_science_nexus_build_priority_ready = yes",
            "staid_science_kilo_build_priority_ready = yes",
            "staid_planetary_computer_build_priority_ready = yes",
            "staid_pop_assembly_snowball_ready = yes",
            "staid_ring_world_build_priority_ready = yes",
            "staid_storage_cap_build_priority_ready = yes",
            "staid_early_kilo_economy_build_priority_ready = yes",
            "staid_apex_site_preservation_ready = yes",
            "staid_research_diplomacy_priority_ready = {",
        ):
            self.assertIn(marker, text)

    def test_research_federation_weight_is_generated_without_unsafe_diplomacy_overrides(self):
        federation_path = MOD_ROOT / "common" / "federation_types" / "zzzz_staid_15_research_diplomacy_federation_types.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        policy_path = MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt"
        traditions_path = MOD_ROOT / "common" / "traditions" / "zzzz_staid_02_perks_traditions_traditions.txt"
        categories_path = (
            MOD_ROOT
            / "common"
            / "tradition_categories"
            / "zzzz_staid_02_perks_traditions_tradition_categories.txt"
        )
        ascension_path = MOD_ROOT / "common" / "ascension_perks" / "zzzz_staid_02_perks_traditions_ascension_perks.txt"
        parse_file(federation_path)
        parse_file(trigger_path)
        parse_file(policy_path)
        parse_file(traditions_path)
        parse_file(categories_path)
        parse_file(ascension_path)

        text = federation_path.read_text(encoding="utf-8")
        trigger_text = trigger_path.read_text(encoding="utf-8")
        policy_text = policy_path.read_text(encoding="utf-8")
        categories_text = categories_path.read_text(encoding="utf-8")
        ascension_text = ascension_path.read_text(encoding="utf-8")
        generated_common_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((MOD_ROOT / "common").rglob("*.txt"))
        )
        research_federation = extract_top_level_object_text(text, "research_federation")

        self.assertIn("# policy_route = research_diplomacy_core", text)
        self.assertIn("host_has_dlc = Federations", research_federation)
        self.assertIn("research_federation_passive", research_federation)
        self.assertIn("ai_weight = {", research_federation)
        self.assertIn("staid_research_diplomacy_core", research_federation)
        self.assertIn("from = { staid_research_diplomacy_priority_ready = yes }", research_federation)
        self.assertIn("has_active_tradition = tr_discovery_federations_finish", research_federation)
        self.assertIn("staid_research_diplomacy_priority_ready = {", trigger_text)
        self.assertIn("diplo_stance_cooperative", policy_text)
        vanilla_discovery = read_text(
            STELLARIS_INSTALL_ROOT / "common" / "traditions" / "00_discovery.txt"
        )
        self.assertIn("tr_discovery_federations_finish", vanilla_discovery)
        self.assertIn("tradition_discovery = {", categories_text)
        self.assertIn("tradition_diplomacy = {", categories_text)
        self.assertNotIn("tr_discovery_finish = {", categories_text)
        self.assertNotIn("tr_diplomacy_finish = {", categories_text)
        self.assertIn("ap_technological_ascendancy", ascension_text)
        self.assertIn("staid_research_diplomacy_priority_ready = yes", generated_common_text)
        self.assertNotIn("action_form_research_agreement", generated_common_text)

        self.assertFalse((MOD_ROOT / "common" / "diplomatic_actions").exists())
        personality_files = sorted((MOD_ROOT / "common" / "personalities").glob("*.txt"))
        self.assertEqual(
            [path.name for path in personality_files],
            ["zzzzz_staid_16_standalone_war_pressure.txt"],
        )

    def test_megastructure_upgrade_stages_are_prioritized_over_new_starts(self):
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(megastructure_path)
        parse_file(trigger_path)

        text = megastructure_path.read_text(encoding="utf-8")
        trigger_text = trigger_path.read_text(encoding="utf-8")
        self.assertIn("staid_megastructure_continuation_priority_ready = {", trigger_text)
        self.assertIn("staid_unfinished_kugelblitz_exists = {", trigger_text)
        self.assertIn("any_owned_megastructure = {", trigger_text)
        for unfinished_stage in ("kugelblitz_0", "kugelblitz_1", "kugelblitz_2", "kugelblitz_restored"):
            self.assertIn(f"is_megastructure_type = {unfinished_stage}", trigger_text)
        self.assertIn("staid_kugelblitz_new_start_budget_ready = {", trigger_text)
        self.assertIn("NOT = { staid_unfinished_kugelblitz_exists = yes }", trigger_text)
        self.assertIn("NOT = { check_variable = { which = giga_current_kugel value >= 10 } }", trigger_text)

        starter = extract_top_level_object_text(text, "kugelblitz_0")
        first_upgrade = extract_top_level_object_text(text, "kugelblitz_1")
        final_upgrade = extract_top_level_object_text(text, "kugelblitz_3")

        self.assertNotIn("megastructure_continuation_priority = finish_existing_before_new_start", starter)
        self.assertIn("kugelblitz_start_budget = empty_silos_are_capped_storage_not_income", starter)
        self.assertIn("modifier = { factor = 0 from = { check_variable = { which = giga_current_kugel value >= 10 } } }", starter)
        self.assertIn("modifier = { factor = 0 from = { has_country_flag = is_currently_building_kugelblitz } }", starter)
        self.assertIn("modifier = { factor = 0 from = { staid_unfinished_kugelblitz_exists = yes } }", starter)
        self.assertIn("modifier = { factor = 0.02 from = { check_variable = { which = giga_current_kugel value >= 9 } } }", starter)
        for block in (first_upgrade, final_upgrade):
            self.assertIn("upgrade_from = {", block)
            self.assertIn("megastructure_continuation_priority = finish_existing_before_new_start", block)
            self.assertIn("staid_megastructure_continuation_priority_ready = yes", block)
            self.assertIn("modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }", block)
            self.assertNotIn("kugelblitz_start_budget = empty_silos_are_capped_storage_not_income", block)


if __name__ == "__main__":
    unittest.main()
