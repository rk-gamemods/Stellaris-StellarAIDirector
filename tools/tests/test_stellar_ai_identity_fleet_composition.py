from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLS_ROOT = Path(__file__).resolve().parents[1]
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from stellar_ai_director_lib import (  # noqa: E402
    IDENTITY_FLEET_COMPOSITION_PATH,
    IDENTITY_FLEET_COMPOSITION_SOURCES,
    NSC3_WORKSHOP_ROOT,
    extract_top_level_object_text,
    identity_fleet_composition_object_text,
    normalize_text_file_content,
    read_text,
    render_identity_fleet_composition_artifact,
    route_override_file_variables,
)


class IdentityFleetCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rendered = render_identity_fleet_composition_artifact()

    def test_exact_nine_object_allowlist_and_checked_artifact_are_current(self) -> None:
        expected = {
            "corvette",
            "frigate",
            "destroyer",
            "cruiser",
            "battleship",
            "StrikeCruiser",
            "Battlecruiser",
            "Carrier",
            "Dreadnought",
        }
        self.assertEqual(
            {object_id for rows in IDENTITY_FLEET_COMPOSITION_SOURCES.values() for object_id in rows},
            expected,
        )
        self.assertEqual(self.rendered.count("# source_object_sha256 = "), 9)
        self.assertEqual(
            normalize_text_file_content(
                IDENTITY_FLEET_COMPOSITION_PATH.read_text(encoding="utf-8")
            ),
            normalize_text_file_content(self.rendered),
        )

    def test_every_full_object_preserves_parent_content_outside_ai_ship_data(self) -> None:
        for source_file, object_hashes in IDENTITY_FLEET_COMPOSITION_SOURCES.items():
            source_text = read_text(
                NSC3_WORKSHOP_ROOT / "common" / "ship_sizes" / source_file
            )
            for object_id in object_hashes:
                source = extract_top_level_object_text(source_text, object_id)
                generated = extract_top_level_object_text(self.rendered, object_id)
                source_ai = extract_top_level_object_text(source, "ai_ship_data")
                generated_ai = extract_top_level_object_text(generated, "ai_ship_data")
                self.assertEqual(
                    source.replace(source_ai, "__AI_SHIP_DATA__", 1),
                    generated.replace(generated_ai, "__AI_SHIP_DATA__", 1),
                    object_id,
                )
                inserted = (
                    "\t\t\tmodifier = { factor = 0 "
                    "has_technology = tech_battleships }\n"
                )
                if object_id in {
                    "corvette",
                    "frigate",
                    "destroyer",
                    "cruiser",
                    "StrikeCruiser",
                    "Battlecruiser",
                }:
                    self.assertEqual(generated_ai.count(inserted.rstrip()), 1, object_id)
                    generated_ai = generated_ai.replace(inserted, "", 1)
                self.assertEqual(
                    normalize_text_file_content(generated_ai),
                    normalize_text_file_content(source_ai),
                    f"unrelated ai_ship_data drift in {object_id}",
                )

    def test_referenced_source_local_variables_are_copied_exactly(self) -> None:
        source_rows = [
            {
                "source_path": str(
                    NSC3_WORKSHOP_ROOT / "common" / "ship_sizes" / source_file
                ),
                "object_id": object_id,
            }
            for source_file, object_hashes in IDENTITY_FLEET_COMPOSITION_SOURCES.items()
            for object_id in object_hashes
        ]
        expected = route_override_file_variables(source_rows)
        actual = [line for line in self.rendered.splitlines() if line.startswith("@")]
        self.assertEqual(actual, expected)

    def test_source_hash_drift_fails_closed(self) -> None:
        source_file = "00_ship_sizes.txt"
        object_id = "corvette"
        source_text = read_text(
            NSC3_WORKSHOP_ROOT / "common" / "ship_sizes" / source_file
        ).replace("size_multiplier = 5", "size_multiplier = 6", 1)
        with self.assertRaisesRegex(ValueError, "Active NSC3 ship size drifted"):
            identity_fleet_composition_object_text(
                source_text,
                object_id,
                IDENTITY_FLEET_COMPOSITION_SOURCES[source_file][object_id],
            )

    def test_every_sub_battleship_hull_reaches_zero_after_battleships(self) -> None:
        for object_id in {
            "corvette",
            "frigate",
            "destroyer",
            "cruiser",
            "StrikeCruiser",
            "Battlecruiser",
        }:
            block = extract_top_level_object_text(self.rendered, object_id)
            identity_lines = [
                line for line in block.splitlines()
                if "factor = 0 has_technology = tech_battleships" in line
            ]
            self.assertEqual(len(identity_lines), 1, object_id)

        for object_id in {"battleship", "Carrier", "Dreadnought"}:
            block = extract_top_level_object_text(self.rendered, object_id)
            self.assertNotIn(
                "factor = 0 has_technology = tech_battleships",
                block,
                object_id,
            )

    def test_save_unlock_model_requests_only_battleships_or_larger(self) -> None:
        # Neutral standard-fleet weights after the parent NSC3 save-unlock
        # modifiers (Battleship + StrikeCruiser + Battlecruiser) are applied.
        parent = {
            "corvette": (1.5, 5),
            "frigate": (5.0, 8),
            "destroyer": (3.75, 10),
            "cruiser": (12.5, 20),
            "battleship": (50.0, 40),
            "StrikeCruiser": (10.0, 25),
            "Battlecruiser": (25.0, 30),
        }
        factors = {
            hull: (
                0.0
                if "factor = 0 has_technology = tech_battleships"
                in extract_top_level_object_text(self.rendered, hull)
                else 1.0
            )
            for hull in parent
        }

        def modeled_entity_count(weights: dict[str, float], cap: float = 509.0) -> float:
            total = sum(weights.values())
            return sum(
                cap * weights[hull] / total / parent[hull][1]
                for hull in weights
            )

        before = {hull: weight for hull, (weight, _size) in parent.items()}
        after = {hull: before[hull] * factors[hull] for hull in before}
        self.assertLess(modeled_entity_count(after), modeled_entity_count(before))
        self.assertEqual(
            {hull for hull, value in after.items() if value > 0},
            {"battleship"},
        )

    def test_no_forced_minima_events_orders_or_nonstandard_hulls(self) -> None:
        for object_id in {
            "corvette",
            "frigate",
            "destroyer",
            "cruiser",
            "battleship",
            "StrikeCruiser",
            "Battlecruiser",
            "Carrier",
            "Dreadnought",
        }:
            ai_ship_data = extract_top_level_object_text(
                extract_top_level_object_text(self.rendered, object_id),
                "ai_ship_data",
            )
            self.assertNotRegex(ai_ship_data, r"(?m)^\s*min\s*=")
        for forbidden in (
            "country_event",
            "on_action",
            "set_fleet_order",
            "create_ship",
            "add_resource",
            "bioship",
            "arkship",
        ):
            self.assertNotIn(forbidden, self.rendered.lower())


if __name__ == "__main__":
    unittest.main()
