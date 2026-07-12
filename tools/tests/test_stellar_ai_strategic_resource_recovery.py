from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from stellar_ai_director_lib import (  # noqa: E402
    MOD_ROOT,
    ORDINARY_STRATEGIC_RESOURCE_RECOVERY,
    STRATEGIC_RESOURCE_DEFICIT_RECOVERY_PATH,
    economic_plan_text,
    generate_strategic_resource_recovery_artifacts,
    parse_file,
    parse_pdx,
    strategic_resource_deficit_recovery_plan_text,
    strategic_resource_recovery_artifact_errors,
    strategic_resource_recovery_contract_errors,
)


PRIMARY_PLAN_PATH = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"


def _subplan_block(plan_text: str, set_name: str) -> str:
    marker = f'set_name = "{set_name}"'
    marker_index = plan_text.index(marker)
    start = plan_text.rfind("\n\tsubplan = {", 0, marker_index) + 1
    end = plan_text.find("\n\tsubplan = {", marker_index)
    if end < 0:
        end = plan_text.index("\n}", marker_index)
    return plan_text[start:end].rstrip()


class StrategicResourceRecoveryRegressionTests(unittest.TestCase):
    def test_generated_artifacts_match_the_bounded_generator_contract(self):
        primary_generated = economic_plan_text()
        recovery_generated = strategic_resource_deficit_recovery_plan_text(primary_generated)

        self.assertEqual(PRIMARY_PLAN_PATH.read_text(encoding="utf-8"), primary_generated)
        self.assertEqual(STRATEGIC_RESOURCE_DEFICIT_RECOVERY_PATH.read_text(encoding="utf-8"), recovery_generated)
        self.assertEqual(strategic_resource_recovery_contract_errors(primary_generated, recovery_generated), [])
        parse_pdx(primary_generated)
        parse_pdx(recovery_generated)
        parse_file(PRIMARY_PLAN_PATH)
        parse_file(STRATEGIC_RESOURCE_DEFICIT_RECOVERY_PATH)

    def test_recovery_contains_exactly_three_has_deficit_only_plus_one_subplans(self):
        primary = economic_plan_text()
        recovery = strategic_resource_deficit_recovery_plan_text(primary)

        self.assertEqual(recovery.count("\n\tsubplan = {"), 3)
        self.assertEqual(recovery.count("\t\toptional = yes"), 3)
        self.assertEqual(recovery.count("has_deficit ="), 3)
        self.assertNotIn("scaling =", recovery)
        for forbidden in (
            "has_technology",
            "has_monthly_income",
            "resource_stockpile_compare",
            "years_passed",
            "market",
            "staid_phase_",
        ):
            self.assertNotIn(forbidden, recovery)

        for resource, label in ORDINARY_STRATEGIC_RESOURCE_RECOVERY:
            set_name = f"Stellar AI Director actual-deficit recovery - {label}"
            expected = f'''\tsubplan = {{
\t\toptional = yes
\t\tset_name = "{set_name}"
\t\tpotential = {{ has_deficit = {resource} }}
\t\tincome = {{ {resource} = 1 }}
\t}}'''
            self.assertEqual(_subplan_block(recovery, set_name), expected)

        residual = _subplan_block(primary, "Stellar AI Director ESC component resource readiness")
        self.assertIn("optional = yes", residual)
        self.assertNotIn("scaling =", residual)
        for resource, _label in ORDINARY_STRATEGIC_RESOURCE_RECOVERY:
            self.assertNotRegex(residual, rf"(?m)^\s*{resource}\s*=")
        for retained in (
            "sr_dark_matter = 3",
            "sr_zro = 3",
            "nanites = 3",
            "engineering_research = 600",
            "energy = 500",
            "minerals = 400",
            "trade = 150",
        ):
            self.assertIn(retained, residual)

        strategic_resource_root = MOD_ROOT / "common" / "strategic_resources"
        overrides = list(strategic_resource_root.rglob("*.txt")) if strategic_resource_root.exists() else []
        self.assertEqual(overrides, [])

    def test_generator_refuses_broadened_or_scaling_recovery(self):
        primary = economic_plan_text()
        residual = _subplan_block(primary, "Stellar AI Director ESC component resource readiness")
        broadened_residual = residual.replace(
            "\t\toptional = yes",
            "\t\tscaling = yes\n\t\tvolatile_motes = 12",
            1,
        )
        with self.assertRaisesRegex(ValueError, "must remain optional"):
            strategic_resource_deficit_recovery_plan_text(primary.replace(residual, broadened_residual, 1))

        unexpected_residual = residual.replace(
            "\t\t\ttrade = 150\n\t\t}",
            "\t\t\ttrade = 150\n\t\t\tphysics_research = 1\n\t\t}",
            1,
        )
        errors = strategic_resource_recovery_contract_errors(
            primary.replace(residual, unexpected_residual, 1),
            strategic_resource_deficit_recovery_plan_text(primary),
        )
        self.assertTrue(
            any("income target set must remain exact" in error for error in errors),
            errors,
        )

        recovery = strategic_resource_deficit_recovery_plan_text(primary)
        broadened_recovery = recovery.replace("volatile_motes = 1", "volatile_motes = 2", 1)
        errors = strategic_resource_recovery_contract_errors(primary, broadened_recovery)
        self.assertTrue(any("exact +1 has_deficit-only contract" in error for error in errors), errors)

        extra_subplan = '''

\tsubplan = {
\t\tset_name = "Stellar AI Director forbidden extra recovery"
\t\tpotential = { has_deficit = volatile_motes }
\t\tincome = { volatile_motes = 1 }
\t}'''
        errors = strategic_resource_recovery_contract_errors(primary, recovery.replace("\n}\n", extra_subplan + "\n}\n"))
        self.assertTrue(any("exactly three subplans" in error for error in errors), errors)

    def test_artifact_validator_rejects_strategic_resource_object_overrides(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mod_root = Path(temp_dir)
            generated_paths = generate_strategic_resource_recovery_artifacts(mod_root)
            self.assertEqual(
                {path.relative_to(mod_root).as_posix() for path in generated_paths},
                {
                    "common/economic_plans/zzzz_staid_additive_economic_plan.txt",
                    "common/economic_plans/zzzz_staid_21_strategic_resource_deficit_recovery.txt",
                },
            )
            self.assertEqual(strategic_resource_recovery_artifact_errors(mod_root), [])

            overrides = mod_root / "common" / "strategic_resources"
            overrides.mkdir(parents=True)
            (overrides / "forbidden.txt").write_text("volatile_motes = {}\n", encoding="utf-8")
            errors = strategic_resource_recovery_artifact_errors(mod_root)
            self.assertTrue(any("object override is forbidden" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
