#!/usr/bin/env python3
"""Generate Stellar AI Director mod files and research artifacts."""

import argparse

from stellar_ai_director_lib import run_all


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    run_all()


if __name__ == "__main__":
    main()

