from __future__ import annotations

import tempfile
import unittest
import json
import subprocess
from pathlib import Path
import sys


TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from stellar_ai_fleet_economy_model import (  # noqa: E402
    FleetEconomyState,
    REPORT_PATH,
    evaluate_completion_tranche,
    modeled_scenarios,
    policy_recurring_resource_union,
    render_recurring_income_triggers,
    scan_ship_economy_roots,
)


class FleetEconomyModelTests(unittest.TestCase):
    def test_checked_active_stack_report_matches_production_policy_union(self) -> None:
        report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
        recurring: set[str] = set()
        construction: set[str] = set()
        for inventory in report["active_stack_inventory"].values():
            recurring.update(inventory["upkeep"])
            recurring.update(inventory["logistics"])
            construction.update(inventory["construction"])
        self.assertEqual(recurring, policy_recurring_resource_union())
        rendered = render_recurring_income_triggers()
        for construction_only in construction - recurring:
            self.assertNotIn(f"resource = {construction_only}", rendered)

    def test_package_import_supports_external_model_consumers(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "from tools.stellar_ai_fleet_economy_model import "
                    "scan_ship_economy_roots; assert scan_ship_economy_roots({}) == {}"
                ),
            ],
            cwd=TOOLS_ROOT.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_external_model_covers_ten_adversarial_scenarios(self) -> None:
        scenarios = {row["name"]: row for row in modeled_scenarios()}
        self.assertEqual(len(scenarios), 10)
        self.assertTrue(
            scenarios["construction_only_zro_does_not_gate_sustainability"][
                "decision"
            ]["allowed"]
        )
        for blocked in (
            "sft_food_pressure_on_standard_hull",
            "peace_does_not_surge",
            "naval_capacity_boundary_does_not_surge",
            "war_shock_optional_resource_negative",
        ):
            self.assertFalse(scenarios[blocked]["decision"]["allowed"])

    def test_scanner_separates_construction_from_recurring_pressure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            components = root / "common" / "component_templates"
            components.mkdir(parents=True)
            (components / "fixture.txt").write_text(
                """
weapon_component_template = {
    key = fixture
    resources = {
        category = ship_components
        cost = { alloys = 100 sr_zro = 5 }
        upkeep = { energy = 2 minerals = 1 }
    }
}
ship_size = {
    resources = {
        category = ships
        upkeep = { alloys = 3 influence = 0.5 }
        logistics = { trade = 4 }
    }
}
""",
                encoding="utf-8",
            )

            report = scan_ship_economy_roots({"fixture": root})["fixture"]

        self.assertEqual(report["construction"], ["alloys", "sr_zro"])
        self.assertEqual(report["upkeep"], ["alloys", "energy", "influence", "minerals"])
        self.assertEqual(report["logistics"], ["trade"])

    def test_zero_stockpile_is_not_part_of_the_wartime_contract(self) -> None:
        decision = evaluate_completion_tranche(
            FleetEconomyState(
                at_war=True,
                naval_capacity_fraction=0.50,
                monthly_net={"energy": 20, "alloys": 10, "trade": 10},
            ),
            {"energy": 1, "alloys": 1, "trade": 1},
            biological=False,
        )
        self.assertTrue(decision.allowed)

    def test_bio_lane_requires_post_completion_food_surplus(self) -> None:
        decision = evaluate_completion_tranche(
            FleetEconomyState(
                at_war=True,
                naval_capacity_fraction=0.50,
                monthly_net={"energy": 20, "alloys": 10, "trade": 10, "food": 5},
            ),
            {"food": 5},
            biological=True,
        )
        self.assertFalse(decision.allowed)
        self.assertIn("food", decision.blocking_resources)

    def test_optional_component_resource_zero_is_safe_until_consumed(self) -> None:
        state = FleetEconomyState(
            at_war=True,
            naval_capacity_fraction=0.50,
            monthly_net={"energy": 20, "alloys": 10, "trade": 10, "minerals": 0},
        )
        self.assertTrue(
            evaluate_completion_tranche(state, {}, biological=False).allowed
        )
        decision = evaluate_completion_tranche(
            state, {"minerals": 1}, biological=False
        )
        self.assertFalse(decision.allowed)
        self.assertIn("minerals", decision.blocking_resources)

    def test_balanced_optional_resource_with_current_expense_is_not_safe(self) -> None:
        decision = evaluate_completion_tranche(
            FleetEconomyState(
                at_war=True,
                naval_capacity_fraction=0.50,
                monthly_net={"energy": 20, "alloys": 10, "trade": 10, "minerals": 0},
                monthly_expenses={"minerals": 1},
            ),
            {},
            biological=False,
        )
        self.assertFalse(decision.allowed)
        self.assertIn("minerals", decision.blocking_resources)

    def test_standard_hull_food_component_pressure_is_observed(self) -> None:
        decision = evaluate_completion_tranche(
            FleetEconomyState(
                at_war=True,
                naval_capacity_fraction=0.50,
                monthly_net={"energy": 20, "alloys": 10, "trade": 10, "food": 0},
                monthly_expenses={"food": 1},
            ),
            {"food": 1},
            biological=False,
        )
        self.assertFalse(decision.allowed)
        self.assertIn("food", decision.blocking_resources)

    def test_completion_tranche_catches_positive_current_income_overshoot(self) -> None:
        decision = evaluate_completion_tranche(
            FleetEconomyState(
                at_war=True,
                naval_capacity_fraction=0.50,
                monthly_net={"energy": 20, "alloys": 100, "trade": 100},
            ),
            {"energy": 21},
            biological=False,
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.projected_net["energy"], -1)

    def test_rendered_native_gate_monitors_recurring_not_construction_resources(self) -> None:
        text = render_recurring_income_triggers()
        for resource in (
            "energy",
            "alloys",
            "trade",
            "food",
            "minerals",
            "giga_sr_sentient_metal",
            "influence",
        ):
            self.assertIn(f"resource = {resource}", text)
        for construction_only in (
            "volatile_motes",
            "exotic_gases",
            "sr_dark_matter",
            "sr_zro",
            "nanites",
            "sr_living_metal",
            "giga_sr_negative_mass",
        ):
            self.assertNotIn(f"resource = {construction_only}", text)
        self.assertNotIn("resource_stockpile_compare", text)
        self.assertIn("resource_expenses_compare", text)


if __name__ == "__main__":
    unittest.main()
