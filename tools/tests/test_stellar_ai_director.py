import csv
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stellar_ai_director_lib import (
    AI_SUPPORT_MAP_CSV,
    DEPENDENCY_EDGES_CSV,
    EmpireState,
    MOD_ROOT,
    OBJECT_ATLAS_CSV,
    POLICY_MATRIX_CSV,
    RESEARCH_ROOT,
    SNAPSHOT_ROOT,
    block_assignments,
    collect_generated_conflict_rows,
    collect_generated_file_audit_rows,
    collect_generated_reference_rows,
    collect_object_names,
    generated_unresolved_at_variable_rows,
    generate_object_atlas_artifacts,
    generate_route_override_artifacts,
    parse_file,
    resource_waste_pressure,
    research_under_curve,
    surplus_sink_pressure,
    validate_generated_patch,
    validate_object_atlas_artifacts,
)


class GeneratedModValidityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        generate_object_atlas_artifacts(SNAPSHOT_ROOT)
        generate_route_override_artifacts()

    def test_generated_files_are_valid_load_surfaces(self):
        rows = collect_generated_file_audit_rows(MOD_ROOT)
        self.assertTrue(rows, "No generated mod files were found to validate.")
        bad_rows = [row for row in rows if row["status"] != "ok"]
        self.assertEqual(bad_rows, [])

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

    def test_static_validator_reports_no_invalid_references(self):
        self.assertEqual(validate_generated_patch(), [])

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
        for marker in (
            "staid_resource_waste_pressure",
            "resource_stockpile_compare = { resource = minerals value > 50000 }",
            "resource_stockpile_compare = { resource = consumer_goods value > 30000 }",
            "staid_research_under_curve",
            "Stellar AI Director capped stockpile research conversion",
            "Stellar AI Director 2360 engineering catchup",
            "value:stellarai_market_sell_value|RESOURCE|minerals|AMOUNT|5000|",
            "value:stellarai_market_sell_value|RESOURCE|giga_sr_sentient_metal|AMOUNT|250|",
        ):
            self.assertIn(marker, triggers + economy + market_events)

    def test_generated_stranded_fleet_recovery_uses_guarded_vanilla_mia(self):
        on_action_path = MOD_ROOT / "common" / "on_actions" / "zzz_staid_market_and_fleet_safety_on_actions.txt"
        event_path = MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt"
        parse_file(on_action_path)
        parse_file(event_path)
        text = event_path.read_text(encoding="utf-8")
        for marker in (
            "staid_homeland_under_attack = yes",
            "can_go_mia = yes",
            "is_fleet_idle = yes",
            "is_in_combat = no",
            "has_fleet_flag = staid_stranded_fleet_warning",
            "set_timed_fleet_flag",
            "set_mia = mia_return_home",
            "space_owner = { NOT = { is_same_value = root } }",
        ):
            self.assertIn(marker, text)

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
            "planetcraft_route",
            "war_moon_route",
            "systemcraft_route",
            "nsc3_capital_hull_route",
            "esc_component_route",
            "crowded_tall_route",
            "conquest_escape_route",
            "fallen_empire_benchmark_route",
        }
        self.assertTrue(required_routes.issubset(covered_routes))
        for row in rows:
            generated_file = Path(row["generated_file"])
            self.assertTrue(generated_file.exists(), f"Missing route override file: {generated_file}")
            self.assertIn(row["object_id"], generated_file.read_text(encoding="utf-8"))
        self.assertTrue((RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.md").exists())


if __name__ == "__main__":
    unittest.main()
