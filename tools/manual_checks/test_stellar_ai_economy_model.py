"""Focused regression tests for the opt-in economy simulator."""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from simulate_stellar_ai_economy import (  # noqa: E402
    LEGACY_RESOURCES,
    ORDINARY,
    STRATEGIC,
    load_pdx_policy,
    load_scenarios,
    simulate,
    strategic_band_for_year,
    strategic_recovery_triggered,
)


LEGACY_TIMELINE_SHA256 = "3f87050368c141351f44a29e369cccc3e936df93220fc99ee7970a610ecd0cf6"
LEGACY_SUMMARY_SHA256 = "414cc63fd0038c5b16c1611b3f3f0ceaa6820119283cbdb46bb23be7f1850a57"
LEGACY_TIMELINE_FIELDS = (
    "scenario",
    "month",
    *(f"income_{resource}" for resource in LEGACY_RESOURCES),
    *(f"target_{resource}" for resource in LEGACY_RESOURCES),
    "research_to_ordinary_ratio",
)
LEGACY_SUMMARY_FIELDS = (
    "scenario",
    "phase",
    "months",
    "research_to_ordinary_ratio",
    "ratio_target_met",
    "food_overproduction",
    "support_safe",
    "pdx_source",
    *(f"final_income_{resource}" for resource in LEGACY_RESOURCES),
    *(f"investment_{resource}" for resource in LEGACY_RESOURCES),
    *(f"minimum_stockpile_{resource}" for resource in ORDINARY),
)


def _canonical_sha256(rows: list[dict[str, object]]) -> str:
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(payload).hexdigest()


def _project(rows: list[dict[str, object]], fields: tuple[str, ...]) -> list[dict[str, object]]:
    return [{field: row[field] for field in fields} for row in rows]


def _replace_map(scenario, field: str, key: str, value):
    updated = dict(getattr(scenario, field))
    updated[key] = value
    return replace(scenario, **{field: updated})


class StellarAIEconomyModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = load_pdx_policy()
        cls.loaded = load_scenarios()
        cls.scenarios = {scenario.name: scenario for scenario in cls.loaded}

    def test_policy_parses_exact_bands_and_source_year_windows(self) -> None:
        expected = {
            ("opening", "volatile_motes"): (0, 44, 1.0, 40.0, 3.0),
            ("opening", "exotic_gases"): (0, 44, 2.0, 60.0, 4.0),
            ("opening", "rare_crystals"): (0, 44, 1.0, 40.0, 3.0),
            ("advanced", "volatile_motes"): (45, 79, 2.0, 90.0, 6.0),
            ("advanced", "exotic_gases"): (45, 79, 4.0, 140.0, 8.0),
            ("advanced", "rare_crystals"): (45, 79, 2.0, 90.0, 6.0),
            ("endgame", "volatile_motes"): (80, 119, 4.0, 180.0, 12.0),
            ("endgame", "exotic_gases"): (80, 119, 8.0, 280.0, 16.0),
            ("endgame", "rare_crystals"): (80, 119, 4.0, 180.0, 12.0),
            ("beyond endgame", "volatile_motes"): (120, None, 8.0, 360.0, 24.0),
            ("beyond endgame", "exotic_gases"): (120, None, 16.0, 560.0, 32.0),
            ("beyond endgame", "rare_crystals"): (120, None, 8.0, 360.0, 24.0),
        }
        actual = {
            key: (
                band.min_years,
                band.max_years,
                band.income_floor,
                band.stockpile_floor,
                band.target,
            )
            for key, band in self.policy.strategic_recovery.items()
        }
        self.assertEqual(actual, expected)

        boundaries = {44: "opening", 45: "advanced", 79: "advanced", 80: "endgame", 119: "endgame", 120: "beyond endgame"}
        for year, expected_phase in boundaries.items():
            for resource in STRATEGIC:
                self.assertEqual(strategic_band_for_year(self.policy, year, resource).phase, expected_phase)

    def test_trigger_truth_table_preserves_native_comparisons(self) -> None:
        scenario = self.scenarios["strategic_gas_save_2290"]
        resource = "exotic_gases"
        band = strategic_band_for_year(self.policy, scenario.years_passed, resource)
        no_deficit = _replace_map(scenario, "strategic_deficit", resource, False)

        self.assertTrue(strategic_recovery_triggered(scenario, band, resource, 20.0, 1000.0))
        self.assertTrue(strategic_recovery_triggered(no_deficit, band, resource, 8.0, 1000.0))
        self.assertFalse(strategic_recovery_triggered(no_deficit, band, resource, 8.001, 1000.0))
        self.assertTrue(strategic_recovery_triggered(no_deficit, band, resource, 20.0, 279.999))
        self.assertFalse(strategic_recovery_triggered(no_deficit, band, resource, 20.0, 280.0))
        unavailable = _replace_map(scenario, "strategic_available", resource, False)
        self.assertFalse(strategic_recovery_triggered(unavailable, band, resource, -200.0, 0.0))

    def test_all_legacy_months_and_summary_fields_are_bit_for_bit_unchanged(self) -> None:
        timeline_rows: list[dict[str, object]] = []
        summary_rows: list[dict[str, object]] = []
        controls = [scenario for scenario in self.loaded if scenario.control]
        self.assertEqual(len(controls), 10)
        for scenario in controls:
            timeline, summary = simulate(scenario, self.policy)
            timeline_rows.extend(timeline)
            summary_rows.append(summary)
            for resource in STRATEGIC:
                self.assertEqual(summary[f"investment_{resource}"], 0, f"{scenario.name}:{resource}")
        self.assertEqual(len(timeline_rows), 1320)
        self.assertEqual(
            _canonical_sha256(_project(timeline_rows, LEGACY_TIMELINE_FIELDS)),
            LEGACY_TIMELINE_SHA256,
        )
        self.assertEqual(
            _canonical_sha256(_project(summary_rows, LEGACY_SUMMARY_FIELDS)),
            LEGACY_SUMMARY_SHA256,
        )

    def test_save_calibrated_gas_shock_requires_market_bridge_then_recovers(self) -> None:
        scenario = self.scenarios["strategic_gas_save_2290"]
        self.assertAlmostEqual(scenario.production["exotic_gases"], 209.341, places=3)
        self.assertAlmostEqual(scenario.upkeep["exotic_gases"], 348.608, places=3)
        self.assertAlmostEqual(scenario.income["exotic_gases"], -139.267, places=3)
        self.assertAlmostEqual(scenario.stockpile["exotic_gases"], 721.753, places=3)

        timeline, result = simulate(scenario, self.policy)

        self.assertEqual(result["investment_exotic_gases"], 13)
        self.assertEqual(result["completed_projects_exotic_gases"], 13)
        self.assertEqual(result["months_to_nonnegative_exotic_gases"], 17)
        self.assertTrue(all(row["projects_completed_exotic_gases"] == 0 for row in timeline[:16]))
        self.assertEqual(timeline[16]["projects_completed_exotic_gases"], 13)
        self.assertEqual(sum(row["projects_started_exotic_gases"] for row in timeline), 13)
        self.assertAlmostEqual(result["final_income_exotic_gases"], 25.826, places=3)
        self.assertAlmostEqual(result["bridge_required_exotic_gases"], 1506.519, places=3)
        self.assertAlmostEqual(result["total_strategic_construction_minerals"], 6500.0, places=3)
        self.assertAlmostEqual(result["total_strategic_completion_energy_upkeep"], 39.0, places=3)
        self.assertFalse(result["strategic_construction_only_survives"])
        self.assertTrue(result["strategic_eventual_recovery"])
        self.assertTrue(result["strategic_market_bridge_affordable"])
        self.assertTrue(result["strategic_recovery_financed"])
        self.assertAlmostEqual(result["bridge_market_cost_exotic_gases"], 97923.735, places=3)
        self.assertLess(result["bridge_market_cost_exotic_gases"], result["market_currency_reserve"])
        recovery_month = next(row["month"] for row in timeline if row["raw_stockpile_exotic_gases"] >= 0 and row["month"] > 16)
        self.assertEqual(recovery_month, 75)
        self.assertAlmostEqual(timeline[-1]["raw_stockpile_exotic_gases"], 2728.909, places=3)
        self.assertEqual(result["investment_volatile_motes"], 0)
        self.assertEqual(result["investment_rare_crystals"], 0)

    def test_restored_handler_is_causal_not_cosmetic(self) -> None:
        scenario = self.scenarios["strategic_gas_save_2290"]
        no_handler = replace(self.policy, strategic_recovery={})
        _, result = simulate(scenario, no_handler)
        self.assertEqual(result["investment_exotic_gases"], 0)
        self.assertAlmostEqual(result["final_income_exotic_gases"], -139.267, places=3)
        self.assertAlmostEqual(result["bridge_required_exotic_gases"], 24346.307, places=3)
        self.assertFalse(result["eventual_recovery_exotic_gases"])
        self.assertFalse(result["strategic_eventual_recovery"])

    def test_proactive_income_floor_prevents_the_gradual_deficit(self) -> None:
        scenario = self.scenarios["strategic_gas_prevention_growth"]
        timeline, result = simulate(scenario, self.policy)
        first_active = next(row["month"] for row in timeline if row["recovery_active_exotic_gases"])
        first_start = next(row["month"] for row in timeline if row["projects_started_exotic_gases"])
        first_completion = next(row["month"] for row in timeline if row["projects_completed_exotic_gases"])
        self.assertEqual(first_active, 30)
        self.assertEqual(first_start, 30)
        self.assertEqual(first_completion, 46)
        self.assertEqual(result["investment_exotic_gases"], 1)
        self.assertEqual(result["bridge_required_exotic_gases"], 0.0)
        self.assertGreater(result["minimum_raw_stockpile_exotic_gases"], 0)
        self.assertTrue(result["construction_only_survives_exotic_gases"])
        self.assertTrue(result["eventual_recovery_exotic_gases"])
        self.assertTrue(result["strategic_recovery_financed"])

    def test_upkeep_growth_sensitivity_is_explicit(self) -> None:
        scenario = self.scenarios["strategic_gas_growth_sensitivity"]
        _, result = simulate(scenario, self.policy)
        self.assertEqual(result["investment_exotic_gases"], 13)
        self.assertAlmostEqual(result["bridge_required_exotic_gases"], 1511.143, places=3)
        self.assertAlmostEqual(result["final_income_exotic_gases"], 19.706, places=3)
        self.assertTrue(result["strategic_recovery_financed"])

    def test_isolated_and_compound_shortages_do_not_touch_healthy_siblings(self) -> None:
        expected = {
            "strategic_motes_deficit": {"volatile_motes"},
            "strategic_crystals_deficit": {"rare_crystals"},
            "strategic_compound_deficit": set(STRATEGIC),
        }
        for name, shortages in expected.items():
            _, result = simulate(self.scenarios[name], self.policy)
            self.assertTrue(result["strategic_eventual_recovery"], name)
            self.assertTrue(result["strategic_recovery_financed"], name)
            for resource in STRATEGIC:
                if resource in shortages:
                    self.assertGreater(result[f"investment_{resource}"], 0, f"{name}:{resource}")
                    self.assertGreaterEqual(result[f"final_income_{resource}"], 0, f"{name}:{resource}")
                else:
                    self.assertEqual(result[f"investment_{resource}"], 0, f"{name}:{resource}")

    def test_total_capacity_is_not_reused_as_fake_concurrent_slots(self) -> None:
        scenario = self.scenarios["strategic_gas_save_2290"]
        scenario = _replace_map(scenario, "strategic_max_projects", "exotic_gases", 12)
        _, result = simulate(scenario, self.policy)
        self.assertEqual(result["investment_exotic_gases"], 12)
        self.assertAlmostEqual(result["final_income_exotic_gases"], 13.126, places=3)
        self.assertTrue(result["capacity_exhausted_exotic_gases"])
        self.assertFalse(result["eventual_recovery_exotic_gases"])


if __name__ == "__main__":
    unittest.main()
