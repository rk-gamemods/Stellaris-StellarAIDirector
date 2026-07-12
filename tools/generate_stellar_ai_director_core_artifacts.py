#!/usr/bin/env python3
"""Check, diff, or write Stellar AI Director's fixed core AI artifacts."""

from __future__ import annotations

import argparse
import difflib
import sys
from collections.abc import Mapping
from pathlib import Path

from stellar_ai_director_lib import (
    CORE_AI_ARTIFACT_PATHS,
    REPO_ROOT,
    parse_pdx,
    render_core_ai_artifacts,
    write_text_file,
)


def canonicalize_eol(text: str) -> str:
    """Normalize line endings without changing any other text."""

    return text.replace("\r\n", "\n").replace("\r", "\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        choices=("check", "diff", "write"),
        help="Check freshness, print logical diffs, or update stale fixed outputs.",
    )
    return parser.parse_args(argv)


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _validate_artifact_set(artifacts: Mapping[Path, str]) -> None:
    expected = tuple(CORE_AI_ARTIFACT_PATHS)
    actual = tuple(artifacts)
    if len(set(expected)) != len(expected):
        raise ValueError("Core artifact allowlist contains duplicate paths")
    non_paths = [repr(path) for path in actual if not isinstance(path, Path)]
    if non_paths:
        raise TypeError(f"Core artifact renderer returned non-path keys: {non_paths}")
    if set(actual) != set(expected) or len(actual) != len(expected):
        missing = sorted(_display_path(path) for path in set(expected) - set(actual))
        unexpected = sorted(_display_path(path) for path in set(actual) - set(expected))
        raise ValueError(
            "Core artifact renderer violated its fixed output allowlist: "
            f"missing={missing}, unexpected={unexpected}"
        )
    for path in expected:
        text = artifacts[path]
        if not isinstance(text, str):
            raise TypeError(f"Rendered artifact is not text: {_display_path(path)}")
        parse_pdx(text)


def _read_existing_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_bytes().decode("utf-8")


def _logical_diff(path: Path, current: str | None, rendered: str) -> str:
    label = _display_path(path)
    current_lines = canonicalize_eol(current).split("\n") if current is not None else []
    rendered_lines = canonicalize_eol(rendered).split("\n")
    return "\n".join(
        difflib.unified_diff(
            current_lines,
            rendered_lines,
            fromfile=f"{label} (current)" if current is not None else "/dev/null",
            tofile=f"{label} (rendered)",
            lineterm="",
        )
    )


def run(mode: str) -> int:
    artifacts = render_core_ai_artifacts()
    _validate_artifact_set(artifacts)

    existing = {path: _read_existing_text(path) for path in CORE_AI_ARTIFACT_PATHS}
    stale = [
        path
        for path in CORE_AI_ARTIFACT_PATHS
        if existing[path] is None
        or canonicalize_eol(existing[path] or "") != canonicalize_eol(artifacts[path])
    ]

    if mode == "write":
        for path in stale:
            write_text_file(path, artifacts[path])
            print(f"updated core artifact: {_display_path(path)}")
        failed_verification = [
            path
            for path in stale
            if (current := _read_existing_text(path)) is None
            or canonicalize_eol(current) != canonicalize_eol(artifacts[path])
        ]
        if failed_verification:
            raise RuntimeError(
                "post-write verification failed for core artifacts: "
                + ", ".join(_display_path(path) for path in failed_verification)
            )
        if not stale:
            print("core AI artifacts are current")
        return 0

    if mode == "diff":
        for path in stale:
            diff = _logical_diff(path, existing[path], artifacts[path])
            if diff:
                print(diff)
        return 1 if stale else 0

    if mode == "check":
        for path in stale:
            print(f"stale core artifact: {_display_path(path)}")
        if not stale:
            print("core AI artifacts are current")
        return 1 if stale else 0

    raise ValueError(f"Unsupported core artifact mode: {mode}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run(args.mode)
    except Exception as exc:
        print(f"core artifact generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
