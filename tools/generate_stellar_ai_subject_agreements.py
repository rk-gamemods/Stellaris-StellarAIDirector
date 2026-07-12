#!/usr/bin/env python3
"""Check, diff, or write Director's fixed identity specialist preset artifacts."""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

from stellar_ai_director_lib import (
    REPO_ROOT,
    parse_pdx,
    render_identity_subject_agreement_artifacts,
    write_text_file,
)


def canonicalize_eol(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("check", "diff", "write"))
    return parser.parse_args(argv)


def display_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def run(mode: str) -> int:
    artifacts = render_identity_subject_agreement_artifacts()
    if len(artifacts) != 4 or len(set(artifacts)) != 4:
        raise ValueError("Subject agreement renderer violated its four-file allowlist")
    for text in artifacts.values():
        parse_pdx(text)
    stale: list[Path] = []
    current: dict[Path, str | None] = {}
    for path, rendered in artifacts.items():
        existing = path.read_text(encoding="utf-8") if path.exists() else None
        current[path] = existing
        if existing is None or canonicalize_eol(existing) != canonicalize_eol(rendered):
            stale.append(path)
    if mode == "write":
        for path in stale:
            write_text_file(path, artifacts[path])
            print(f"updated subject agreement artifact: {display_path(path)}")
        for path in stale:
            if canonicalize_eol(path.read_text(encoding="utf-8")) != canonicalize_eol(
                artifacts[path]
            ):
                raise RuntimeError(f"post-write verification failed: {display_path(path)}")
        if not stale:
            print("subject agreement artifacts are current")
        return 0
    if mode == "diff":
        for path in stale:
            before = canonicalize_eol(current[path] or "").splitlines()
            after = canonicalize_eol(artifacts[path]).splitlines()
            print(
                "\n".join(
                    difflib.unified_diff(
                        before,
                        after,
                        fromfile=f"{display_path(path)} (current)",
                        tofile=f"{display_path(path)} (rendered)",
                        lineterm="",
                    )
                )
            )
        return 1 if stale else 0
    for path in stale:
        print(f"stale subject agreement artifact: {display_path(path)}")
    if not stale:
        print("subject agreement artifacts are current")
    return 1 if stale else 0


def main(argv: list[str] | None = None) -> int:
    try:
        return run(parse_args(argv).mode)
    except Exception as exc:
        print(f"subject agreement generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
