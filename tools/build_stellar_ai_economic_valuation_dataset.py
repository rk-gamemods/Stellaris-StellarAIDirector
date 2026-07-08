#!/usr/bin/env python3
"""Build the active-stack building/zone/district economic valuation dataset."""

from stellar_ai_director_lib import generate_economic_valuation_dataset


def main() -> None:
    rows = generate_economic_valuation_dataset()
    print(f"generated {len(rows)} economic valuation rows")


if __name__ == "__main__":
    main()
