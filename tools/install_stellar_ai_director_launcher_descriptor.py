#!/usr/bin/env python3
"""Install the local Stellar AI Director descriptor for the Paradox launcher."""

from stellar_ai_director_lib import install_launcher_descriptor


def main() -> None:
    print(install_launcher_descriptor())


if __name__ == "__main__":
    main()
