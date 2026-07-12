#!/usr/bin/env python3
"""Regression tests for the legacy economy-model acceptance check."""

from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from manual_checks import check_stellar_ai_economy_model as checker  # noqa: E402


class EconomyModelManualCheckTests(unittest.TestCase):
    def test_support_unsafe_result_fails_acceptance(self) -> None:
        scenario = SimpleNamespace(
            name="unsafe_support",
            bio_ships=False,
            income={"food": 10.0},
        )
        result = {
            "research_to_ordinary_ratio": 2.5,
            "support_safe": False,
            "final_income_food": 10.0,
            "ratio_target_met": True,
        }
        with (
            patch.object(checker, "load_pdx_policy", return_value=SimpleNamespace(source=Path("fixture.plan"))),
            patch.object(checker, "load_scenarios", return_value=[scenario]),
            patch.object(checker, "simulate", return_value=([], result)),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(checker.main(), 1)


if __name__ == "__main__":
    unittest.main()
