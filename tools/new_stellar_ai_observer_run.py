#!/usr/bin/env python3
"""Create a standard Stellar AI Director observer-run folder."""

from stellar_ai_observer_loop import create_observer_run


def main() -> None:
    run_dir = create_observer_run()
    print(run_dir)


if __name__ == "__main__":
    main()
