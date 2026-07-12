#!/usr/bin/env python3
"""Regenerate only the hash-locked NSC3 identity fleet-composition artifact."""

from __future__ import annotations

from stellar_ai_director_lib import (
    IDENTITY_FLEET_COMPOSITION_PATH,
    render_identity_fleet_composition_artifact,
    write_text_file,
)


def main() -> int:
    write_text_file(
        IDENTITY_FLEET_COMPOSITION_PATH,
        render_identity_fleet_composition_artifact(),
    )
    print(IDENTITY_FLEET_COMPOSITION_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
