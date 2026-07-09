import csv
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stellar_ai_observer_loop import (
    CHECKPOINT_FIELDS,
    checkpoint_save_report_text,
    create_observer_run,
    extract_checkpoint_rows_from_save,
    latest_observer_run,
    summarize_observer_run,
)
from manage_stellaris_commands_at_date import (
    OBSERVER_COMMAND_SCHEDULE,
    commands_status,
    disable_commands,
    enable_observer_schedule,
)


class StellarAiObserverLoopTests(unittest.TestCase):
    def test_commands_at_date_uses_dev_only_game_speed_five(self):
        self.assertIn('2200.01.01 = "game_speed 5"', OBSERVER_COMMAND_SCHEDULE)
        self.assertIn('2200.01.02 = "game_speed 5"', OBSERVER_COMMAND_SCHEDULE)
        self.assertNotIn('game_speed 4"', OBSERVER_COMMAND_SCHEDULE)
        self.assertIn("GAME_SPEED_6", OBSERVER_COMMAND_SCHEDULE)

    def test_commands_at_date_does_not_auto_confirm_gigas_startup(self):
        self.assertNotIn("giga_menu.1111", OBSERVER_COMMAND_SCHEDULE)
        self.assertNotIn("Gigastructural Engineering startup-confirm", OBSERVER_COMMAND_SCHEDULE)

    def test_commands_at_date_observer_schedule_is_explicit_and_removable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            live_path = Path(temp_dir) / "commands_at_date.txt"

            self.assertFalse(commands_status(live_path).exists)
            enable_observer_schedule(live_path)

            enabled_status = commands_status(live_path)
            self.assertTrue(enabled_status.exists)
            self.assertTrue(enabled_status.managed_observer_schedule)
            self.assertTrue(enabled_status.contains_game_pause)
            self.assertTrue(enabled_status.contains_observer_commands)

            disabled_path = disable_commands(live_path)

            self.assertIsNotNone(disabled_path)
            self.assertFalse(live_path.exists())
            self.assertTrue(disabled_path.exists())
            self.assertIn("disabled-by-codex", disabled_path.name)

    def test_commands_at_date_enable_refuses_to_overwrite_existing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            live_path = Path(temp_dir) / "commands_at_date.txt"
            live_path.write_text('2250.01.01 = "some_user_command"\n', encoding="utf-8")

            with self.assertRaises(FileExistsError):
                enable_observer_schedule(live_path)

            self.assertEqual(live_path.read_text(encoding="utf-8"), '2250.01.01 = "some_user_command"\n')

    def test_create_observer_run_writes_standard_layout(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = create_observer_run(root=root, run_id="observer-test")

            for relative_path in (
                "README.md",
                "metadata.json",
                "manual-notes.md",
                "checkpoints.csv",
                "metrics.json",
                "summary.json",
                "summary.md",
                "logs",
                "saves",
                "screenshots",
                "exports",
            ):
                self.assertTrue((run_dir / relative_path).exists(), relative_path)

            metadata = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["run_id"], "observer-test")
            self.assertFalse(metadata["hidden_economic_bonuses"])
            self.assertEqual(metadata["standard_checkpoints"], [2250, 2300, 2325, 2350])

            with (run_dir / "checkpoints.csv").open("r", encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle)
                self.assertEqual(next(reader), CHECKPOINT_FIELDS)

    def test_create_observer_run_refuses_duplicate_run_id(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            create_observer_run(root=root, run_id="observer-test")

            with self.assertRaises(FileExistsError):
                create_observer_run(root=root, run_id="observer-test")

    def test_summarize_observer_run_counts_checkpoint_rows(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = create_observer_run(root=root, run_id="observer-test")
            with (run_dir / "checkpoints.csv").open("a", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=CHECKPOINT_FIELDS)
                writer.writerow(
                    {
                        "run_id": "observer-test",
                        "checkpoint_year": "2250",
                        "date": "2250.01.01",
                        "empire_rank": "1",
                        "empire_name": "Test Empire",
                    }
                )
                writer.writerow(
                    {
                        "run_id": "observer-test",
                        "checkpoint_year": "2250",
                        "date": "2250.01.01",
                        "empire_rank": "median",
                        "empire_name": "Middle Empire",
                    }
                )

            summary = summarize_observer_run(run_dir)

            self.assertEqual(summary["checkpoint_row_count"], 2)
            self.assertEqual(summary["checkpoint_year_counts"], {"2250": 2})
            self.assertEqual(summary["empire_rank_counts"], {"1": 1, "median": 1})
            self.assertTrue((run_dir / "summary.json").exists())
            self.assertTrue((run_dir / "summary.md").exists())

    def test_latest_observer_run_chooses_most_recent_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            older = create_observer_run(root=root, run_id="observer-old")
            newer = create_observer_run(root=root, run_id="observer-new")

            older.touch()
            newer.touch()

            self.assertEqual(latest_observer_run(root=root), newer)

    def test_extract_checkpoint_rows_filters_special_countries(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            save_path = Path(temp_dir) / "checkpoint.sav"
            gamestate = """
date="2250.01.01"
country={
  1={
    initialized=yes
    type=country
    name={ key="Alpha League" }
    economy_power=1200
    tech_power=800
    fleet_size=130
    used_naval_capacity=80
    naval_capacity=96
    num_sapient_pops=1234
    owned_megastructures={
      21 22
    }
    owned_planets={
      7 8 9
    }
    controlled_colonies={
      7 8
    }
    budget={
      current_month={
        income={
          country_base={
            energy=20
            minerals=20
            food=20
            physics_research=10
            society_research=10
            engineering_research=10
            consumer_goods=15
            alloys=5
          }
          planet_jobs={
            energy=30
            minerals=40
            food=-5
            physics_research=3
            society_research=4
            engineering_research=5
            consumer_goods=6
            alloys=7
          }
        }
      }
    }
  }
  2={
    initialized=yes
    type=10
    name={ key="Fallen Outlier" }
    economy_power=30000
    tech_power=1000000
    fleet_size=2500
    used_naval_capacity=2500
    num_sapient_pops=20000
  }
  4={
    initialized=yes
    type=10
    name={ key="Late Regularized Empire" }
    economy_power=4200
    tech_power=9000
    fleet_size=700
    used_naval_capacity=650
    num_sapient_pops=7000
  }
  3={
    initialized=yes
    type=guardian_horror
    economy_power=1
    fleet_size=250
  }
}
"""
            with zipfile.ZipFile(save_path, "w") as archive:
                archive.writestr("gamestate", gamestate)

            rows, summary = extract_checkpoint_rows_from_save(
                save_path,
                run_id="observer-test",
                checkpoint_year=2250,
                evidence_file="saves/checkpoint.sav",
            )

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["empire_name"], "Late Regularized Empire")
            self.assertEqual(rows[1]["empire_name"], "Alpha League")
            self.assertEqual(rows[1]["research"], "42")
            self.assertEqual(rows[1]["energy_income"], "50")
            self.assertEqual(rows[1]["food_income"], "15")
            self.assertEqual(rows[1]["naval_capacity_available"], "96")
            self.assertEqual(rows[1]["colonies"], "2")
            self.assertEqual(rows[1]["megastructures"], "2")
            self.assertEqual(rows[1]["deficits"], "")
            self.assertEqual(summary["eligible_regular_country_count"], 2)
            self.assertEqual(summary["excluded_special_or_outlier_countries"][0]["name"], "Fallen Outlier")
            self.assertIn("Alpha League", checkpoint_save_report_text(summary))


if __name__ == "__main__":
    unittest.main()
