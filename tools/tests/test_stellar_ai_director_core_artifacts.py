import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


TOOLS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_ROOT))

import generate_stellar_ai_director_core_artifacts as core_cli  # noqa: E402
import generate_stellar_ai_director_patch as broad_cli  # noqa: E402


class FocusedCoreArtifactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.paths = (
            self.root / "common" / "ai_budget" / "outposts.txt",
            self.root / "common" / "scripted_triggers" / "decisions.txt",
        )
        self.rendered = {
            self.paths[0]: "outpost_budget = { enabled = yes }\n",
            self.paths[1]: "decision_gate = { enabled = yes }\n",
        }

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _run(self, mode: str, rendered: dict[Path, str] | None = None) -> int:
        with (
            mock.patch.object(core_cli, "CORE_AI_ARTIFACT_PATHS", self.paths),
            mock.patch.object(
                core_cli,
                "render_core_ai_artifacts",
                return_value=self.rendered if rendered is None else rendered,
            ),
        ):
            return core_cli.run(mode)

    def test_eol_canonicalization_changes_only_line_endings(self) -> None:
        self.assertEqual(
            core_cli.canonicalize_eol("one\r\ntwo\rthree\n"),
            "one\ntwo\nthree\n",
        )
        self.assertNotEqual(
            core_cli.canonicalize_eol("value = yes \r\n"),
            core_cli.canonicalize_eol("value = yes\n"),
        )

    def test_check_accepts_crlf_without_rewriting(self) -> None:
        for path, text in self.rendered.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
        before = {path: path.read_bytes() for path in self.paths}

        with contextlib.redirect_stdout(io.StringIO()):
            result = self._run("check")

        self.assertEqual(result, 0)
        self.assertEqual(before, {path: path.read_bytes() for path in self.paths})

    def test_check_treats_non_eol_text_changes_as_stale(self) -> None:
        for path, text in self.rendered.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
        self.paths[0].write_text(
            self.rendered[self.paths[0]].replace("enabled = yes", "enabled = yes "),
            encoding="utf-8",
            newline="\n",
        )
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = self._run("check")

        self.assertEqual(result, 1)
        self.assertIn("stale core artifact:", output.getvalue())

    def test_diff_reports_logical_change_without_writing(self) -> None:
        for path, text in self.rendered.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
        self.paths[1].write_text(
            "decision_gate = { enabled = no }\n", encoding="utf-8", newline="\n"
        )
        before = self.paths[1].read_bytes()
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = self._run("diff")

        self.assertEqual(result, 1)
        self.assertIn("-decision_gate = { enabled = no }", output.getvalue())
        self.assertIn("+decision_gate = { enabled = yes }", output.getvalue())
        self.assertEqual(self.paths[1].read_bytes(), before)

    def test_write_updates_only_stale_outputs(self) -> None:
        for path in self.paths:
            path.parent.mkdir(parents=True, exist_ok=True)
        fresh_bytes = self.rendered[self.paths[0]].replace("\n", "\r\n").encode("utf-8")
        self.paths[0].write_bytes(fresh_bytes)
        self.paths[1].write_text(
            "decision_gate = { enabled = no }\n", encoding="utf-8", newline="\n"
        )

        with contextlib.redirect_stdout(io.StringIO()):
            result = self._run("write")

        self.assertEqual(result, 0)
        self.assertEqual(self.paths[0].read_bytes(), fresh_bytes)
        self.assertEqual(
            self.paths[1].read_text(encoding="utf-8"),
            self.rendered[self.paths[1]],
        )

    def test_write_returns_safety_exit_when_post_write_verification_fails(self) -> None:
        for path in self.paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("original = yes\n", encoding="utf-8", newline="\n")
        before = {path: path.read_bytes() for path in self.paths}
        stderr = io.StringIO()

        with (
            mock.patch.object(core_cli, "CORE_AI_ARTIFACT_PATHS", self.paths),
            mock.patch.object(
                core_cli,
                "render_core_ai_artifacts",
                return_value=self.rendered,
            ),
            mock.patch.object(core_cli, "write_text_file"),
            contextlib.redirect_stderr(stderr),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            result = core_cli.main(["write"])

        self.assertEqual(result, 2)
        self.assertIn("post-write verification failed", stderr.getvalue())
        self.assertEqual(before, {path: path.read_bytes() for path in self.paths})

    def test_allowlist_violation_returns_safety_exit_before_writes(self) -> None:
        for path in self.paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("original = yes\n", encoding="utf-8", newline="\n")
        before = {path: path.read_bytes() for path in self.paths}
        stderr = io.StringIO()

        with (
            mock.patch.object(core_cli, "CORE_AI_ARTIFACT_PATHS", self.paths),
            mock.patch.object(
                core_cli,
                "render_core_ai_artifacts",
                return_value={self.paths[0]: self.rendered[self.paths[0]]},
            ),
            contextlib.redirect_stderr(stderr),
        ):
            result = core_cli.main(["write"])

        self.assertEqual(result, 2)
        self.assertIn("fixed output allowlist", stderr.getvalue())
        self.assertEqual(before, {path: path.read_bytes() for path in self.paths})

    def test_parse_failure_returns_render_exit_before_writes(self) -> None:
        for path in self.paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("original = yes\n", encoding="utf-8", newline="\n")
        before = {path: path.read_bytes() for path in self.paths}
        malformed = dict(self.rendered)
        malformed[self.paths[1]] = "decision_gate = {\n"
        stderr = io.StringIO()

        with (
            mock.patch.object(core_cli, "CORE_AI_ARTIFACT_PATHS", self.paths),
            mock.patch.object(
                core_cli, "render_core_ai_artifacts", return_value=malformed
            ),
            contextlib.redirect_stderr(stderr),
        ):
            result = core_cli.main(["write"])

        self.assertEqual(result, 2)
        self.assertIn("Malformed PDXScript", stderr.getvalue())
        self.assertEqual(before, {path: path.read_bytes() for path in self.paths})


class GeneratorArgumentSafetyTests(unittest.TestCase):
    def test_broad_help_exits_before_generation(self) -> None:
        with (
            mock.patch.object(broad_cli, "run_all") as run_all,
            contextlib.redirect_stdout(io.StringIO()),
            self.assertRaises(SystemExit) as raised,
        ):
            broad_cli.main(["--help"])

        self.assertEqual(raised.exception.code, 0)
        run_all.assert_not_called()

    def test_broad_invalid_argument_exits_before_generation(self) -> None:
        with (
            mock.patch.object(broad_cli, "run_all") as run_all,
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit) as raised,
        ):
            broad_cli.main(["--not-a-real-option"])

        self.assertEqual(raised.exception.code, 2)
        run_all.assert_not_called()

    def test_broad_no_argument_path_still_runs_generator(self) -> None:
        with mock.patch.object(broad_cli, "run_all") as run_all:
            broad_cli.main([])

        run_all.assert_called_once_with()

    def test_focused_usage_exits_before_rendering(self) -> None:
        with (
            mock.patch.object(core_cli, "render_core_ai_artifacts") as render,
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit) as raised,
        ):
            core_cli.main(["invalid"])

        self.assertEqual(raised.exception.code, 2)
        render.assert_not_called()


if __name__ == "__main__":
    unittest.main()
