#!/usr/bin/env python3
"""Manage the live Stellaris commands_at_date observer-control file."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DEFAULT_STELLARIS_USER_DIR = Path.home() / "Documents" / "Paradox Interactive" / "Stellaris"
DEFAULT_COMMANDS_PATH = DEFAULT_STELLARIS_USER_DIR / "commands_at_date.txt"

OBSERVER_COMMAND_SCHEDULE = """# Observer-loop console command schedule for a manually approved AI benchmark run.
# This file must not remain installed after the observer run ends.
# Use `python tools/manage_stellaris_commands_at_date.py disable` to remove it.
# `game_speed 5` is intentional: in Stellaris 4.4.x it unlocks the dev-only
# higher simulation speed displayed by the UI as GAME_SPEED_6.
# `event giga_menu.1111` is the Gigastructural Engineering startup-confirm
# event used by the active benchmark playset when the preset dialog blocks
# normal UI confirmation.
2200.01.01 = "event giga_menu.1111"
2200.01.01 = "help human_ai"
2200.01.01 = "help observe"
2200.01.01 = "human_ai"
2200.01.01 = "observe"
2200.01.01 = "help game_speed"
2200.01.01 = "game_speed 5"
2200.01.02 = "event giga_menu.1111"
2200.01.02 = "help human_ai"
2200.01.02 = "help observe"
2200.01.02 = "human_ai"
2200.01.02 = "observe"
2200.01.02 = "help game_speed"
2200.01.02 = "game_speed 5"
2250.01.01 = "game_paused"
2300.01.01 = "game_paused"
2325.01.01 = "game_paused"
2350.01.01 = "game_paused"
"""

OBSERVER_MARKERS = (
    "Observer-loop console command schedule",
    "human_ai",
    "observe",
    "game_paused",
)


@dataclass(frozen=True)
class CommandsStatus:
    path: Path
    exists: bool
    managed_observer_schedule: bool
    contains_game_pause: bool
    contains_observer_commands: bool
    size_bytes: int

    def as_dict(self) -> dict[str, object]:
        return {
            "path": str(self.path),
            "exists": self.exists,
            "managed_observer_schedule": self.managed_observer_schedule,
            "contains_game_pause": self.contains_game_pause,
            "contains_observer_commands": self.contains_observer_commands,
            "size_bytes": self.size_bytes,
        }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def commands_status(path: Path = DEFAULT_COMMANDS_PATH) -> CommandsStatus:
    text = read_text(path)
    return CommandsStatus(
        path=path,
        exists=path.exists(),
        managed_observer_schedule=all(marker in text for marker in OBSERVER_MARKERS),
        contains_game_pause="game_paused" in text,
        contains_observer_commands=any(command in text for command in ("human_ai", "observe", "ticks_per_turn")),
        size_bytes=path.stat().st_size if path.exists() else 0,
    )


def enable_observer_schedule(path: Path = DEFAULT_COMMANDS_PATH, *, force: bool = False) -> Path:
    if path.exists() and not force:
        status = commands_status(path)
        raise FileExistsError(
            f"{path} already exists; status={status.as_dict()}. "
            "Disable or archive it first, or pass --force intentionally."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(OBSERVER_COMMAND_SCHEDULE, encoding="utf-8", newline="\n")
    return path


def disable_commands(path: Path = DEFAULT_COMMANDS_PATH, *, archive: bool = True) -> Path | None:
    if not path.exists():
        return None
    if not archive:
        path.unlink()
        return path
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = path.with_name(f"commands_at_date.disabled-by-codex-{stamp}.txt")
    suffix = 1
    while target.exists():
        target = path.with_name(f"commands_at_date.disabled-by-codex-{stamp}-{suffix}.txt")
        suffix += 1
    path.rename(target)
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("status", "enable", "disable"))
    parser.add_argument("--path", type=Path, default=DEFAULT_COMMANDS_PATH, help="Live commands_at_date.txt path.")
    parser.add_argument("--force", action="store_true", help="Allow enable to overwrite an existing command file.")
    parser.add_argument("--delete", action="store_true", help="Delete on disable instead of archiving by rename.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.action == "status":
        payload = commands_status(args.path).as_dict()
    elif args.action == "enable":
        enabled_path = enable_observer_schedule(args.path, force=args.force)
        payload = {"action": "enabled", "path": str(enabled_path), **commands_status(enabled_path).as_dict()}
    else:
        disabled_path = disable_commands(args.path, archive=not args.delete)
        payload = {
            "action": "disabled" if disabled_path is not None else "already_absent",
            "path": str(args.path),
            "disabled_path": str(disabled_path) if disabled_path is not None else None,
            **commands_status(args.path).as_dict(),
        }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
