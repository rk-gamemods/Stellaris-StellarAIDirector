#!/usr/bin/env python3
"""Disable the local Stellar AI Director descriptor in Stellaris dlc_load.json."""

from stellar_ai_director_lib import disable_director_in_dlc_load


def main() -> None:
    print(disable_director_in_dlc_load())


if __name__ == "__main__":
    main()
