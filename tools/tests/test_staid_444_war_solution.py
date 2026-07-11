#!/usr/bin/env python3
"""Regression tests for the Stellaris 4.4.4 native war replacement package."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from stellar_ai_director_lib import MOD_ROOT, REPO_ROOT  # noqa: E402
from validate_staid_444_war_solution import WAR_FILES, validate  # noqa: E402


class StellarAI444WarSolutionTests(unittest.TestCase):
    def test_focused_validator_passes(self) -> None:
        self.assertEqual(validate(), [])

    def test_no_state_mutating_production_events_are_added(self) -> None:
        forbidden_directories = (
            REPO_ROOT / "mods" / "StellarAIDirector" / "events",
            REPO_ROOT / "mods" / "StellarAIDirector" / "common" / "on_actions",
        )
        packaged = {str((REPO_ROOT / relative).resolve()) for relative in WAR_FILES}
        for directory in forbidden_directories:
            if directory.exists():
                for path in directory.rglob("*"):
                    self.assertNotIn(str(path.resolve()), packaged)

    def test_no_scripted_fleet_orders_exist_anywhere_in_the_live_mod(self) -> None:
        forbidden = ("set_mia =", "set_fleet_order =", "set_fleet_stance =", "move_to =")
        for path in MOD_ROOT.rglob("*.txt"):
            text = path.read_text(encoding="utf-8-sig")
            for marker in forbidden:
                self.assertNotIn(marker, text, f"{marker} in {path}")

    def test_replacement_paths_are_repository_relative(self) -> None:
        for relative in WAR_FILES:
            self.assertFalse(Path(relative).is_absolute(), relative)
            self.assertNotIn("..", Path(relative).parts, relative)
            self.assertTrue((REPO_ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
