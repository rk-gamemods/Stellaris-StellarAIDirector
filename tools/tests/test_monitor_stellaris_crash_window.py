import time
import tempfile
import unittest
from collections import deque
from unittest.mock import patch

from pathlib import Path

from tools.monitor_stellaris_crash_window import sha256_file, trim_window


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


if __name__ == "__main__":
    unittest.main()
