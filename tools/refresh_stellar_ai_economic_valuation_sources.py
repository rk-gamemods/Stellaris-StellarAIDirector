#!/usr/bin/env python3
"""Refresh only the two active-stack economic valuation source snapshots."""

from stellar_ai_director_lib import (
    ECONOMIC_VALUATION_DATASET_CSV,
    NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV,
    generate_economic_valuation_dataset,
    normalize_nonconstruction_economic_valuation_dataset_file,
)


def main() -> None:
    construction_rows = generate_economic_valuation_dataset()
    normalize_nonconstruction_economic_valuation_dataset_file(
        NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV
    )
    print(
        "refreshed economic valuation snapshots: "
        f"{ECONOMIC_VALUATION_DATASET_CSV.name} ({len(construction_rows)} rows), "
        f"{NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.name}"
    )


if __name__ == "__main__":
    main()
