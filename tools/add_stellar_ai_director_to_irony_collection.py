#!/usr/bin/env python3
"""Append Stellar AI Director to the selected Irony collection without reordering existing mods."""

from stellar_ai_director_lib import append_director_to_selected_irony_collection


def main() -> None:
    result = append_director_to_selected_irony_collection()
    print(result)


if __name__ == "__main__":
    main()
