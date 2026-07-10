#!/usr/bin/env python3
"""Capture a bounded five-minute Stellaris log window when the game exits."""

from __future__ import annotations

import json
import hashlib
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


def newest_directory(root: Path) -> Path | None:
    candidates = [path for path in root.iterdir() if path.is_dir()] if root.exists() else []
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


def main() -> None:
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
    buffers = {path: deque() for path in SOURCES}
    observed_running = False
    absent_polls = 0
    started_at = datetime.now(timezone.utc)
    try:
        while True:
            running = stellaris_running()
            observed_running = observed_running or running
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
            if observed_running and absent_polls >= 6:
                break
            time.sleep(POLL_SECONDS)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot = OUTPUT_ROOT / f"stellaris_exit_{stamp}"
        snapshot.mkdir()
        for path, entries in buffers.items():
            (snapshot / path.name).write_text("".join(line for _, line in entries), encoding="utf-8")
        latest_save = newest_file(SAVE_ROOT, "*.sav")
        latest_crash = newest_directory(CRASH_ROOT)
        saved_copy = None
        saved_hash = None
        if latest_save:
            saved_copy = snapshot / latest_save.name
            shutil.copy2(latest_save, saved_copy)
            saved_hash = sha256_file(saved_copy)
        metadata = {
            "monitor_started_utc": started_at.isoformat(),
            "process_exit_observed_utc": datetime.now(timezone.utc).isoformat(),
            "window_seconds": WINDOW_SECONDS,
            "maximum_bytes_per_log": MAX_BYTES_PER_LOG,
            "latest_save": str(latest_save) if latest_save else None,
            "captured_save": str(saved_copy) if saved_copy else None,
            "captured_save_sha256": saved_hash,
            "latest_save_mtime_utc": (
                datetime.fromtimestamp(latest_save.stat().st_mtime, timezone.utc).isoformat()
                if latest_save
                else None
            ),
            "latest_crash_folder": str(latest_crash) if latest_crash else None,
        }
        (snapshot / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        prune_snapshots()
    finally:
        lock_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
