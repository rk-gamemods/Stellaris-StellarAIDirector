import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from summarize_stellaris_log import render_markdown, summarize_logs


class StellarisLogSummaryTests(unittest.TestCase):
    def test_groups_repeated_single_line_errors_with_volatile_values(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "error.log"
            path.write_text(
                "\n".join(
                    [
                        "[20:30:36][dlc.cpp:339]: Invalid supported_version in  file: mod/ugc_1142142725.mod line: 9",
                        "[20:30:37][dlc.cpp:339]: Invalid supported_version in  file: mod/ugc_1199002146.mod line: 12",
                        "[20:30:38][asset.cpp:11]: Missing texture file: gfx/example.dds",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = summarize_logs([path], sample_limit=1)

        self.assertEqual(summary["total_entries"], 3)
        self.assertEqual(summary["group_count"], 2)
        self.assertEqual(summary["family_count"], 2)
        top_group = summary["groups"][0]
        self.assertEqual(top_group["count"], 2)
        self.assertIn("mod/ugc_<id>.mod", top_group["signature"])
        self.assertEqual(len(top_group["samples"]), 1)

    def test_groups_multiline_script_errors_and_renders_samples(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "error.log"
            path.write_text(
                "\n".join(
                    [
                        "[22:02:01][trigger_impl.cpp:1191]: Script Error: Invalid context switch",
                        "  file: common/megastructures/example.txt line: 10",
                        "  Current Scope: galactic_object",
                        "[22:02:02][trigger_impl.cpp:1191]: Script Error: Invalid context switch",
                        "  file: common/megastructures/example.txt line: 22",
                        "  Current Scope: galactic_object",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = summarize_logs([path], sample_limit=2)
            markdown = render_markdown(summary, top=5)

        self.assertEqual(summary["total_entries"], 2)
        self.assertEqual(summary["group_count"], 1)
        self.assertEqual(summary["family_count"], 1)
        self.assertIn("2x `trigger_impl.cpp:<line>`", markdown)
        self.assertIn("Current Scope: galactic_object", markdown)

    def test_families_collapse_wrong_scope_errors_across_source_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "error.log"
            path.write_text(
                "\n".join(
                    [
                        "[20:32:19][trigger.cpp:1034]: Wrong scope for trigger 'uses_ship_category' at file_a.txt:10",
                        "Current scope: ship_growth_stage",
                        "Supported Scopes: country",
                        "[20:32:19][trigger.cpp:1034]: Wrong scope for trigger 'uses_ship_category' at file_b.txt:20",
                        "Current scope: ship_growth_stage",
                        "Supported Scopes: country",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = summarize_logs([path], sample_limit=1)

        self.assertEqual(summary["group_count"], 2)
        self.assertEqual(summary["family_count"], 1)
        self.assertEqual(summary["families"][0]["count"], 2)
        self.assertEqual(summary["families"][0]["severity"], "error")


if __name__ == "__main__":
    unittest.main()
