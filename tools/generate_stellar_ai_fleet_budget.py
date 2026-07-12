#!/usr/bin/env python3
"""Regenerate only the Stellar AI Director fleet alloy budget artifact."""

from stellar_ai_director_lib import FLEET_ALLOY_BUDGET_PATH, ai_budget_text, write_text_file


def main() -> None:
    write_text_file(FLEET_ALLOY_BUDGET_PATH, ai_budget_text({}, archetype_overlay=True))
    print(f"generated {FLEET_ALLOY_BUDGET_PATH}")


if __name__ == "__main__":
    main()
