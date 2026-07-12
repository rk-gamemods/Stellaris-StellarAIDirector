import csv
import hashlib
import io
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from extract_stellar_ai_expansion_evidence import (  # noqa: E402
    MAX_SAVES,
    build_series,
    main,
    render_csv_tables,
    render_json,
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_save(
    root: Path,
    *,
    date: str,
    include_type_19: bool,
    busy_constructor: bool,
    save_name: str = "Synthetic Expansion Series",
    candidate_system_id: str = "1",
) -> Path:
    suffix = date.replace(".", "-")
    type_19 = (
        """
                strategy=
                {
                    type=19
                    id=100
                    target=0
                    value=50
                }
    """
        if include_type_19
        else ""
    )
    current_order = (
        """
            current_order=
            {
                build_mining_station_fleet_order=
                {
                    target=100
                    can_reach=yes
                    note="quoted brace { does not close the order"
                    # } comment brace does not close it either
                    coordinate={ origin=1 }
                    resources=
                    {
                        alloys=100
                        influence=75
                    }
                }
            }
    """
        if busy_constructor
        else ""
    )
    meta = f'''
version="Pegasus v4.4.4"
version_control_revision=28
name="{save_name}"
date="{date}"
'''
    gamestate = f'''
version="Pegasus v4.4.4"
version_control_revision=28
date="{date}"
country=
{{
    0=
    {{
        type=default
        name={{ key="Synthetic Empire" }}
        fleets_manager=
        {{
            owned_fleets=
            {{
                {{ fleet=10 }}
                {{ fleet=11 }}
            }}
        }}
        ai=
        {{
            strategy=
            {{
                type=1
                id=200
                target=77
                value=21
            }}
            {type_19}
            strategy={{ type=7 id=999 target=0 value=999 }}
        }}
        modules=
        {{
            standard_economy_module=
            {{
                resources={{ alloys=1000 influence=500 energy=250 }}
            }}
        }}
        budget=
        {{
            current_month=
            {{
                income={{ alloys=20 influence=10 }}
                expenses={{ alloys=5 influence=2 }}
                balance={{ alloys=15 influence=8 }}
            }}
        }}
        relations_manager=
        {{
            relation=
            {{
                owner=0
                country=3
                contact=yes
                threat=4.5
                trust=-10
            }}
            relation=
            {{
                owner=0
                country=2
                contact=yes
                threat=0
            }}
        }}
    }}
    16777217=none
}}
fleet=
{{
    10=
    {{
        name={{ key="Busy Constructor" }}
        ships={{ 501 }}
        ship_class=shipclass_constructor
        movement_manager={{ coordinate={{ origin=1 }} }}
        order_id=91
        {current_order}
    }}
    11=
    {{
        name={{ key="Idle Constructor With Stale Order ID" }}
        ships={{ 502 }}
        ship_class=shipclass_constructor
        movement_manager={{ coordinate={{ origin=2 }} }}
        order_id=88
    }}
}}
planets=
{{
    planet=
    {{
        100=
        {{
            planet_class="pc_g_star"
            coordinate={{ origin={candidate_system_id} }}
            surveyed_by=0
        }}
        200=
        {{
            planet_class="pc_continental"
            coordinate={{ origin=2 }}
            surveyed_by=0
        }}
    }}
}}
galactic_object=
{{
    1=
    {{
        name={{ key="Candidate System" }}
        planet=100
        hyperlane={{ {{ to=2 length=10 }} }}
        discovery={{ 0 2 }}
        starbases={{ 4294967295 }}
    }}
    2=
    {{
        name={{ key="Colony System" }}
        planet=200
        hyperlane={{ {{ to=1 length=10 }} }}
        discovery={{ 0 }}
        starbases={{ 700 }}
    }}
}}
'''
    path = root / f"snapshot-{suffix}.sav"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("meta", meta)
        archive.writestr("gamestate", gamestate)
    return path


class StellarAiExpansionEvidenceTests(unittest.TestCase):
    def make_series(self, root: Path) -> tuple[Path, Path, Path]:
        first = make_save(
            root,
            date="2250.01.01",
            include_type_19=True,
            busy_constructor=True,
        )
        second = make_save(
            root,
            date="2251.01.01",
            include_type_19=False,
            busy_constructor=False,
        )
        third = make_save(
            root,
            date="2252.01.01",
            include_type_19=True,
            busy_constructor=True,
        )
        return first, second, third

    def test_resources_and_serialized_strategy_rows_remain_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first, _, _ = self.make_series(Path(temp_dir))
            snapshot = build_series([first], "0")["snapshots"][0]

        resources = snapshot["resources"]
        self.assertEqual(resources["stockpile"]["values"]["alloys"], 1000.0)
        self.assertEqual(resources["income"]["values"]["alloys"], 20.0)
        self.assertEqual(resources["expenses"]["values"]["alloys"], 5.0)
        self.assertEqual(resources["balance"]["values"]["alloys"], 15.0)
        self.assertEqual(
            resources["balance"]["source_path"], "country.budget.current_month.balance"
        )
        rows = snapshot["strategy_interest_rows"]
        self.assertEqual([row["raw_type"] for row in rows], ["1", "19"])
        self.assertEqual(rows[1]["raw_id"], "100")
        self.assertEqual(rows[1]["mapped_system_id"], "1")
        self.assertIn("not proof", rows[1]["semantic_boundary"])

    def test_constructor_busy_state_uses_current_order_not_order_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first, _, _ = self.make_series(Path(temp_dir))
            constructors = build_series([first], "0")["snapshots"][0]["constructors"]

        by_id = {row["fleet_id"]: row for row in constructors}
        self.assertTrue(by_id["10"]["busy_from_current_order"])
        self.assertEqual(
            by_id["10"]["raw_order_kind_keys"], ["build_mining_station_fleet_order"]
        )
        order = by_id["10"]["order_evidence"][0]
        self.assertIsNone(order["outpost_order_classification"])
        self.assertIn("unclassified", order["outpost_order_classification_basis"])
        self.assertEqual(order["raw_scalars"]["target"], "100")
        self.assertEqual(order["raw_scalars"]["can_reach"], "yes")
        self.assertEqual(order["serialized_order_resources"]["alloys"], 100.0)
        self.assertFalse(by_id["11"]["busy_from_current_order"])
        self.assertEqual(by_id["11"]["fleet_order_id_not_busy_signal"], "88")

    def test_multi_save_sorting_episodes_and_csvs_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            first, second, third = self.make_series(Path(temp_dir))
            before = {path: file_sha256(path) for path in (first, second, third)}
            series_a = build_series([third, first, second], "0")
            series_b = build_series([second, third, first], "0")
            after = {path: file_sha256(path) for path in (first, second, third)}

        self.assertEqual(before, after)
        self.assertEqual(render_json(series_a), render_json(series_b))
        self.assertEqual(
            [row["save"]["date"] for row in series_a["snapshots"]],
            ["2250.01.01", "2251.01.01", "2252.01.01"],
        )
        type_19 = [row for row in series_a["episodes"] if row["raw_type"] == "19"]
        self.assertEqual(len(type_19), 2)
        self.assertEqual(type_19[1]["missing_supplied_snapshot_count_before"], 1)
        self.assertFalse(type_19[0]["continuous_engine_presence_proven"])
        self.assertFalse(type_19[0]["present_in_final_snapshot"])
        self.assertTrue(type_19[1]["present_in_final_snapshot"])
        self.assertEqual(
            type_19[1]["evidence_classification"],
            "snapshot_observed_persistence",
        )
        self.assertEqual(
            series_a["campaign_comparability"]["status"],
            "caller_asserted_series_with_consistency_checks",
        )
        self.assertFalse(
            series_a["campaign_comparability"]["common_campaign_lineage_proven"]
        )

        tables_a = render_csv_tables(series_a)
        tables_b = render_csv_tables(series_b)
        self.assertEqual(tables_a, tables_b)
        self.assertEqual(
            set(tables_a),
            {
                "snapshots",
                "candidates",
                "constructors",
                "systems",
                "relations",
                "episodes",
            },
        )
        candidate_rows = list(csv.DictReader(io.StringIO(tables_a["candidates"])))
        self.assertEqual(len(candidate_rows), 5)

    def test_series_caps_and_comparability_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first, second, _ = self.make_series(root)
            other = make_save(
                root,
                date="2253.01.01",
                include_type_19=True,
                busy_constructor=False,
                save_name="Different Campaign",
            )
            with self.assertRaisesRegex(ValueError, "fixed .*save cap"):
                build_series([first] * (MAX_SAVES + 1), "0")
            with self.assertRaisesRegex(ValueError, "duplicate input paths"):
                build_series([first, first], "0")
            duplicate = root / "same-content-different-name.sav"
            shutil.copyfile(first, duplicate)
            with self.assertRaisesRegex(ValueError, "duplicate save content SHA-256"):
                build_series([first, duplicate], "0")
            with self.assertRaisesRegex(ValueError, "campaign comparability"):
                build_series([second, other], "0")
            remapped = make_save(
                root,
                date="2254.01.01",
                include_type_19=True,
                busy_constructor=False,
                candidate_system_id="3",
            )
            with self.assertRaisesRegex(ValueError, "candidate mapping drift"):
                build_series([first, remapped], "0")
            with self.assertRaisesRegex(ValueError, "country ID"):
                build_series([first], "not-an-id")

    def test_cli_writes_json_and_all_normalized_csv_tables(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first, second, third = self.make_series(root)
            json_out = root / "evidence.json"
            csv_dir = root / "tables"
            result = main(
                [
                    str(third),
                    str(first),
                    str(second),
                    "--country-id",
                    "0",
                    "--json-out",
                    str(json_out),
                    "--csv-dir",
                    str(csv_dir),
                ]
            )

            self.assertEqual(result, 0)
            payload = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema"], "stellar-ai-expansion-evidence/v1")
            self.assertEqual(
                {path.name for path in csv_dir.iterdir()},
                {f"{name}.csv" for name in render_csv_tables(payload)},
            )


if __name__ == "__main__":
    unittest.main()
