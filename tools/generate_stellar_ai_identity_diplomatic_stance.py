#!/usr/bin/env python3
"""Check, diff, or write the fixed H08 identity diplomatic-stance artifact."""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

from stellar_ai_director_lib import (
    IDENTITY_DIPLOMATIC_STANCE_PATH,
    REPO_ROOT,
    parse_pdx,
    render_identity_diplomatic_stance_artifacts,
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
    artifacts = render_identity_diplomatic_stance_artifacts()
    if tuple(artifacts) != (IDENTITY_DIPLOMATIC_STANCE_PATH,):
        raise ValueError("identity diplomatic stance output allowlist drifted")
    rendered = artifacts[IDENTITY_DIPLOMATIC_STANCE_PATH]
    parse_pdx(rendered)
    current = (
        IDENTITY_DIPLOMATIC_STANCE_PATH.read_text(encoding="utf-8")
        if IDENTITY_DIPLOMATIC_STANCE_PATH.exists()
        else None
    )
    stale = current is None or canonicalize_eol(current) != canonicalize_eol(rendered)
    if mode == "write":
        if stale:
            write_text_file(IDENTITY_DIPLOMATIC_STANCE_PATH, rendered)
            if canonicalize_eol(IDENTITY_DIPLOMATIC_STANCE_PATH.read_text(encoding="utf-8")) != canonicalize_eol(rendered):
                raise RuntimeError("post-write identity diplomatic stance verification failed")
            print(f"updated identity diplomatic stance: {display_path(IDENTITY_DIPLOMATIC_STANCE_PATH)}")
        else:
            print("identity diplomatic stance artifact is current")
        return 0
    if mode == "diff":
        if stale:
            print(
                "\n".join(
                    difflib.unified_diff(
                        canonicalize_eol(current or "").splitlines(),
                        canonicalize_eol(rendered).splitlines(),
                        fromfile=f"{display_path(IDENTITY_DIPLOMATIC_STANCE_PATH)} (current)",
                        tofile=f"{display_path(IDENTITY_DIPLOMATIC_STANCE_PATH)} (rendered)",
                        lineterm="",
                    )
                )
            )
        return 1 if stale else 0
    if mode == "check":
        if stale:
            print(f"stale identity diplomatic stance: {display_path(IDENTITY_DIPLOMATIC_STANCE_PATH)}")
        else:
            print("identity diplomatic stance artifact is current")
        return 1 if stale else 0
    raise ValueError(f"unsupported mode: {mode}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run(args.mode)
    except Exception as exc:
        print(f"identity diplomatic stance generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
