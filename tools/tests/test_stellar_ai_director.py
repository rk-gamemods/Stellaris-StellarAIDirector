import csv
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stellar_ai_director_lib import (
    AI_SUPPORT_MAP_CSV,
    DEPENDENCY_EDGES_CSV,
    MOD_ROOT,
    OBJECT_ATLAS_CSV,
    POLICY_MATRIX_CSV,
    RESEARCH_ROOT,
    SNAPSHOT_ROOT,
    block_assignments,
    collect_generated_file_audit_rows,
    collect_generated_reference_rows,
    collect_object_names,
    generate_object_atlas_artifacts,
    generate_route_override_artifacts,
    parse_file,
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

    def test_static_validator_reports_no_invalid_references(self):
        self.assertEqual(validate_generated_patch(), [])

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
