#!/usr/bin/env python3
"""Write the selected Irony collection snapshot for Stellar AI Director."""

from stellar_ai_director_lib import RESEARCH_ROOT, build_active_playset_snapshot, write_json


def main() -> None:
    write_json(RESEARCH_ROOT / "stellar-ai-director-active-playset-2026-07-04.json", build_active_playset_snapshot())


if __name__ == "__main__":
    main()

