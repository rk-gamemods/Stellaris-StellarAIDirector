#!/usr/bin/env python3
"""Continuously capture bounded five-minute Stellaris windows on game exit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path


STELLARIS_ROOT = Path.home() / "Documents" / "Paradox Interactive" / "Stellaris"
LOG_ROOT = STELLARIS_ROOT / "logs"
SAVE_ROOT = STELLARIS_ROOT / "save games"
CRASH_ROOT = STELLARIS_ROOT / "crashes"
OUTPUT_ROOT = LOG_ROOT / "codex_rolling_crash_window"
SOURCES = (LOG_ROOT / "error.log", LOG_ROOT / "game.log")
WINDOW_SECONDS = 300
MAX_BYTES_PER_LOG = 8 * 1024 * 1024
MAX_SNAPSHOTS = 3
POLL_SECONDS = 0.5
ABSENT_POLLS_TO_CONFIRM_EXIT = 6
CRASH_ASSOCIATION_GRACE_SECONDS = 60
CRASH_EVIDENCE_FILES = ("exception.txt", "meta.yml", "system.log")


def trim_window(entries: deque[tuple[float, str]], now: float) -> None:
    while entries and now - entries[0][0] > WINDOW_SECONDS:
        entries.popleft()
    total = sum(len(line.encode("utf-8", errors="replace")) for _, line in entries)
    while entries and total > MAX_BYTES_PER_LOG:
        _, removed = entries.popleft()
        total -= len(removed.encode("utf-8", errors="replace"))


def stellaris_running() -> bool:
    result = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq stellaris.exe", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
        check=False,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    return '"stellaris.exe"' in result.stdout.lower()


def newest_file(root: Path, pattern: str) -> Path | None:
    candidates = [path for path in root.rglob(pattern) if path.is_file()] if root.exists() else []
    return max(candidates, key=lambda path: path.stat().st_mtime, default=None)


def directory_names(root: Path) -> set[str]:
    return {path.name for path in root.iterdir() if path.is_dir()} if root.exists() else set()


def select_fresh_crash_directory(
    root: Path,
    known_at_session_start: set[str],
    session_started_epoch: float,
    exit_observed_epoch: float,
) -> Path | None:
    """Return only a crash folder created during the monitored game session."""
    if not root.exists():
        return None
    lower_bound = session_started_epoch - CRASH_ASSOCIATION_GRACE_SECONDS
    upper_bound = exit_observed_epoch + CRASH_ASSOCIATION_GRACE_SECONDS
    candidates = []
    for path in root.iterdir():
        if not path.is_dir() or path.name in known_at_session_start:
            continue
        modified = path.stat().st_mtime
        if lower_bound <= modified <= upper_bound:
            candidates.append(path)
    return max(candidates, key=lambda path: path.stat().st_mtime, default=None)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prune_snapshots() -> None:
    snapshots = sorted(
        (path for path in OUTPUT_ROOT.iterdir() if path.is_dir()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for stale in snapshots[MAX_SNAPSHOTS:]:
        for child in stale.iterdir():
            if child.is_file():
                child.unlink()
        stale.rmdir()


def capture_snapshot(
    *,
    buffers: dict[Path, deque[tuple[float, str]]],
    monitor_started_at: datetime,
    session_started_at: datetime,
    exit_observed_at: datetime,
    known_crashes: set[str],
    run_sequence: int,
    continuous: bool,
    attached_mid_session: bool,
) -> Path:
    fresh_crash = select_fresh_crash_directory(
        CRASH_ROOT,
        known_crashes,
        session_started_at.timestamp(),
        exit_observed_at.timestamp(),
    )
    exit_kind = "crash" if fresh_crash else "normal_exit"
    stamp = exit_observed_at.astimezone().strftime("%Y%m%d_%H%M%S_%f")
    snapshot = OUTPUT_ROOT / f"stellaris_{exit_kind}_{stamp}"
    snapshot.mkdir()

    captured_log_bytes: dict[str, int] = {}
    captured_log_lines: dict[str, int] = {}
    for path, entries in buffers.items():
        text = "".join(line for _, line in entries)
        (snapshot / path.name).write_text(text, encoding="utf-8")
        captured_log_bytes[path.name] = len(text.encode("utf-8", errors="replace"))
        captured_log_lines[path.name] = len(entries)

    copied_crash_evidence: list[str] = []
    if fresh_crash:
        for name in CRASH_EVIDENCE_FILES:
            source = fresh_crash / name
            if source.is_file():
                destination = snapshot / f"crash_{name}"
                shutil.copy2(source, destination)
                copied_crash_evidence.append(destination.name)

    latest_save = newest_file(SAVE_ROOT, "*.sav")
    saved_copy = None
    saved_hash = None
    save_age_seconds = None
    save_is_session_fresh = False
    if latest_save:
        saved_copy = snapshot / latest_save.name
        shutil.copy2(latest_save, saved_copy)
        saved_hash = sha256_file(saved_copy)
        save_modified = datetime.fromtimestamp(latest_save.stat().st_mtime, timezone.utc)
        save_age_seconds = max(0.0, (exit_observed_at - save_modified).total_seconds())
        save_is_session_fresh = save_modified >= session_started_at

    metadata = {
        "monitor_started_utc": monitor_started_at.isoformat(),
        "session_started_utc": session_started_at.isoformat(),
        "process_exit_observed_utc": exit_observed_at.isoformat(),
        "run_sequence": run_sequence,
        "continuous_monitor": continuous,
        "attached_mid_session": attached_mid_session,
        "exit_kind": exit_kind,
        "window_seconds": WINDOW_SECONDS,
        "maximum_bytes_per_log": MAX_BYTES_PER_LOG,
        "maximum_snapshots": MAX_SNAPSHOTS,
        "captured_log_bytes": captured_log_bytes,
        "captured_log_lines": captured_log_lines,
        "known_crash_folder_count_at_session_start": len(known_crashes),
        "fresh_crash_folder": str(fresh_crash) if fresh_crash else None,
        "copied_crash_evidence": copied_crash_evidence,
        "latest_save": str(latest_save) if latest_save else None,
        "captured_save": str(saved_copy) if saved_copy else None,
        "captured_save_sha256": saved_hash,
        "latest_save_mtime_utc": (
            datetime.fromtimestamp(latest_save.stat().st_mtime, timezone.utc).isoformat()
            if latest_save
            else None
        ),
        "latest_save_age_seconds_at_exit": save_age_seconds,
        "latest_save_is_session_fresh": save_is_session_fresh,
    }
    (snapshot / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    prune_snapshots()
    return snapshot


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture bounded, per-session Stellaris logs and saves without adding game log spam."
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Exit after the next observed Stellaris process exit instead of monitoring future runs.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    lock_path = OUTPUT_ROOT / "monitor.pid"
    if lock_path.exists():
        try:
            existing_pid = int(lock_path.read_text(encoding="ascii").strip())
            os.kill(existing_pid, 0)
            raise SystemExit(f"Stellaris crash-window monitor is already running as PID {existing_pid}.")
        except (OSError, ValueError):
            lock_path.unlink(missing_ok=True)
    lock_path.write_text(str(os.getpid()), encoding="ascii")

    offsets = {path: path.stat().st_size if path.exists() else 0 for path in SOURCES}
    monitor_started_at = datetime.now(timezone.utc)
    running_at_monitor_start = stellaris_running()
    run_sequence = 0
    try:
        while True:
            while not stellaris_running():
                time.sleep(POLL_SECONDS)

            run_sequence += 1
            session_started_at = datetime.now(timezone.utc)
            known_crashes = directory_names(CRASH_ROOT)
            buffers = {path: deque() for path in SOURCES}
            absent_polls = 0
            while absent_polls < ABSENT_POLLS_TO_CONFIRM_EXIT:
                running = stellaris_running()
                absent_polls = 0 if running else absent_polls + 1
                now = time.monotonic()
                for path in SOURCES:
                    if not path.exists():
                        continue
                    size = path.stat().st_size
                    if size < offsets[path]:
                        offsets[path] = 0
                        buffers[path].clear()
                    if size > offsets[path]:
                        with path.open("r", encoding="utf-8", errors="replace") as handle:
                            handle.seek(offsets[path])
                            for line in handle:
                                buffers[path].append((now, line))
                            offsets[path] = handle.tell()
                    trim_window(buffers[path], now)
                time.sleep(POLL_SECONDS)

            exit_observed_at = datetime.now(timezone.utc)
            capture_snapshot(
                buffers=buffers,
                monitor_started_at=monitor_started_at,
                session_started_at=session_started_at,
                exit_observed_at=exit_observed_at,
                known_crashes=known_crashes,
                run_sequence=run_sequence,
                continuous=not args.once,
                attached_mid_session=run_sequence == 1 and running_at_monitor_start,
            )
            if args.once:
                break
            offsets = {path: path.stat().st_size if path.exists() else 0 for path in SOURCES}
    finally:
        lock_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
