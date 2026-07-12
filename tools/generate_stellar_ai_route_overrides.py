#!/usr/bin/env python3
"""Regenerate only the fixed Stellar AI Director route-override artifacts."""

from stellar_ai_director_lib import generate_route_override_artifacts


def main() -> None:
    rows = generate_route_override_artifacts()
    print(f"generated {len(rows)} route override rows")


if __name__ == "__main__":
    main()
