#!/usr/bin/env python3
"""Generate the Stellar AI Director object atlas and derived knowledge reports."""

from stellar_ai_director_lib import generate_object_atlas_artifacts, validate_object_atlas_artifacts


def main() -> None:
    generate_object_atlas_artifacts()
    errors = validate_object_atlas_artifacts()
    if errors:
        raise SystemExit("Object atlas validation failed:\n" + "\n".join(errors))
    print("Stellar AI Director object atlas generated.")


if __name__ == "__main__":
    main()
