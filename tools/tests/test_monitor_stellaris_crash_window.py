import json
import os
import time
import tempfile
import unittest
from collections import deque
from datetime import datetime, timezone
from unittest.mock import patch

from pathlib import Path

from tools.monitor_stellaris_crash_window import (
    capture_snapshot,
    directory_names,
    select_fresh_crash_directory,
    sha256_file,
    trim_window,
)


class StellarisCrashWindowTests(unittest.TestCase):
    def test_trim_window_removes_old_and_over_cap_lines(self):
        now = time.monotonic()
        entries = deque([(now - 301, "old\n"), (now, "12345\n"), (now, "67890\n")])
        with patch("tools.monitor_stellaris_crash_window.MAX_BYTES_PER_LOG", 7):
            trim_window(entries, now)
        self.assertEqual(list(entries), [(now, "67890\n")])

    def test_sha256_file_is_stable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "save.sav"
            path.write_bytes(b"stellaris-save")
            self.assertEqual(
                sha256_file(path),
                "4cb98f59984d8946544f76c10e3fc4fb2732a73d0c34b7b279f444390233da5b",
            )

    def test_select_fresh_crash_directory_rejects_stale_and_known_folders(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            known = root / "stellaris_known"
            stale = root / "stellaris_stale"
            fresh = root / "stellaris_fresh"
            known.mkdir()
            stale.mkdir()
            baseline = directory_names(root)
            fresh.mkdir()
            os.utime(stale, (100.0, 100.0))
            os.utime(fresh, (205.0, 205.0))

            selected = select_fresh_crash_directory(root, baseline, 200.0, 210.0)

            self.assertEqual(selected, fresh)

    def test_select_fresh_crash_directory_returns_none_without_new_session_crash(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            stale = root / "stellaris_stale"
            stale.mkdir()
            os.utime(stale, (100.0, 100.0))

            selected = select_fresh_crash_directory(root, set(), 200.0, 210.0)

            self.assertIsNone(selected)

    def test_capture_snapshot_records_only_fresh_session_evidence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_root = root / "output"
            crash_root = root / "crashes"
            save_root = root / "saves"
            output_root.mkdir()
            crash_root.mkdir()
            save_root.mkdir()
            fresh_crash = crash_root / "stellaris_fresh"
            fresh_crash.mkdir()
            (fresh_crash / "exception.txt").write_text("C0000005\n", encoding="utf-8")
            os.utime(fresh_crash, (205.0, 205.0))
            save = save_root / "autosave.sav"
            save.write_bytes(b"save-data")
            os.utime(save, (208.0, 208.0))
            error_log = root / "error.log"
            game_log = root / "game.log"
            buffers = {
                error_log: deque([(1.0, "error line\n")]),
                game_log: deque([(1.0, "game line\n")]),
            }
            monitor_started = datetime.fromtimestamp(190.0, timezone.utc)
            session_started = datetime.fromtimestamp(200.0, timezone.utc)
            exit_observed = datetime.fromtimestamp(210.0, timezone.utc)

            with (
                patch("tools.monitor_stellaris_crash_window.OUTPUT_ROOT", output_root),
                patch("tools.monitor_stellaris_crash_window.CRASH_ROOT", crash_root),
                patch("tools.monitor_stellaris_crash_window.SAVE_ROOT", save_root),
            ):
                snapshot = capture_snapshot(
                    buffers=buffers,
                    monitor_started_at=monitor_started,
                    session_started_at=session_started,
                    exit_observed_at=exit_observed,
                    known_crashes=set(),
                    run_sequence=2,
                    continuous=True,
                    attached_mid_session=False,
                )

            metadata = json.loads((snapshot / "metadata.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["exit_kind"], "crash")
            self.assertEqual(metadata["run_sequence"], 2)
            self.assertTrue(metadata["latest_save_is_session_fresh"])
            self.assertEqual(metadata["captured_log_lines"], {"error.log": 1, "game.log": 1})
            self.assertEqual(metadata["copied_crash_evidence"], ["crash_exception.txt"])
            self.assertEqual((snapshot / "crash_exception.txt").read_text(encoding="utf-8"), "C0000005\n")


if __name__ == "__main__":
    unittest.main()
