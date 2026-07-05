#!/usr/bin/env python3
"""Build the Stellar AI Director baseline-vs-Director launch comparison report."""

from stellar_ai_director_lib import generate_launch_comparison_artifacts


def main() -> None:
    generate_launch_comparison_artifacts()


if __name__ == "__main__":
    main()
