#!/usr/bin/env python3
"""Summarize the latest Stellar AI Director observer-run folder."""

from stellar_ai_observer_loop import latest_observer_run, summarize_observer_run


def main() -> None:
    run_dir = latest_observer_run()
    summarize_observer_run(run_dir)
    print(run_dir)


if __name__ == "__main__":
    main()
