import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from simulate_stellar_ai_economy import load_scenarios, simulate  # noqa: E402


class StellarAIEconomySimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenarios = {scenario.name: scenario for scenario in load_scenarios()}

    def result(self, name):
        return simulate(self.scenarios[name])[1]

    def test_food_surplus_never_receives_more_investment(self):
        result = self.result("food_surplus_trap")
        self.assertEqual(result["investment_food"], 0)
        self.assertTrue(result["ratio_target_met"])

    def test_food_deficit_is_repaired_without_becoming_a_surplus_sink(self):
        result = self.result("food_deficit_recovery")
        self.assertGreater(result["investment_food"], 0)
        self.assertLessEqual(result["final_income_food"], 50)
        self.assertFalse(result["food_overproduction"])

    def test_research_support_deficits_interrupt_then_recover(self):
        for scenario in ("research_cg_constrained", "research_energy_constrained"):
            result = self.result(scenario)
            self.assertTrue(result["support_safe"], scenario)
            self.assertTrue(result["ratio_target_met"], scenario)

    def test_every_scenario_reaches_ratio_with_safe_support(self):
        for name in self.scenarios:
            result = self.result(name)
            self.assertTrue(result["ratio_target_met"], name)
            self.assertTrue(result["support_safe"], name)

    def test_phase_and_war_shift_investment_from_minerals_to_alloys(self):
        early = self.result("early_expansion")
        mid = self.result("midgame_fleet_pivot")
        self.assertGreater(early["investment_minerals"], early["investment_alloys"])
        self.assertGreater(mid["investment_alloys"], mid["investment_minerals"])

    def test_normal_scenarios_keep_food_below_the_normal_ceiling(self):
        for name, scenario in self.scenarios.items():
            if not scenario.bio_ships and scenario.income["food"] <= 50:
                result = self.result(name)
                self.assertLessEqual(result["final_income_food"], 50, name)


if __name__ == "__main__":
    unittest.main()
