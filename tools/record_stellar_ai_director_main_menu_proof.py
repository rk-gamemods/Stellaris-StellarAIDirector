#!/usr/bin/env python3
"""Record a manual main-menu proof marker for the current Stellaris playset mode."""

from stellar_ai_director_lib import MAIN_MENU_PROOF_PATH, record_main_menu_proof_marker


def main() -> None:
    status = record_main_menu_proof_marker()
    print(f"{MAIN_MENU_PROOF_PATH}: main_menu_proven={status['main_menu_proven']}")


if __name__ == "__main__":
    main()
