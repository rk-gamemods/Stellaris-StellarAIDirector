from __future__ import annotations

import contextlib
import difflib
import hashlib
import io
import re
import sys
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path
from unittest import mock


TOOLS_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_ROOT))

import generate_stellar_ai_archetype_overlays as overlay_cli  # noqa: E402
from stellar_ai_director_lib import (  # noqa: E402
    ARCHETYPE_OVERLAY_ARTIFACT_PATHS,
    FLEET_ALLOY_BUDGET_PATH,
    FLEET_ARCHETYPE_FACTORS,
    FLEET_THREAT_RESPONSE_FACTOR,
    IDENTITY_CLAIM_BUDGET_PATH,
    IDENTITY_MEGASTRUCTURE_PATH,
    IDENTITY_STATIC_DEFENSE_PATHS,
    IDENTITY_STRATEGY_ROUTE_OVERRIDE_PATHS,
    ROUTE_OVERRIDE_TARGETS,
    TECHNOLOGY_ARCHETYPE_EXCLUDED_OBJECTS,
    TECHNOLOGY_ARCHETYPE_ROUTE_FACTORS,
    TECHNOLOGY_ROUTE_OVERRIDE_PATH,
    collect_object_names,
    extract_top_level_object_text,
    fleet_alloy_budget_text,
    fleet_archetype_budget_modifier,
    fleet_threat_response_budget_modifier,
    render_archetype_consumer_artifacts,
    route_gate_for_target,
    route_override_file_text,
    route_override_target_rows,
    technology_archetype_weight_modifiers,
)


ZERO_OVERLAY_SHA256 = {
    # The technology artifact remains a fixed pre-H08c historical baseline.
    # The fleet budget is intentionally excluded: global, non-archetype budget
    # safety slices are allowed to evolve while archetype_overlay=False.
    TECHNOLOGY_ROUTE_OVERRIDE_PATH: (
        "a2b1e92d11ac8eeb1a2d4a5dd215a8381e47b036986cbb3a64eda6abdaaca0e4"
    ),
}
EXPECTED_SELECTABLE_TECHNOLOGY_IDS = {
    "tech_mega_shipyard",
    "tech_science_nexus",
    "giga_tech_engineering_test_site",
    "giga_tech_macro_scale_weather_manipulation",
    "giga_tech_planetary_computer",
    "tech_robotic_workers",
    "tech_robot_assembly_complex",
    "tech_mega_assembly",
    "tech_cloning",
    "giga_tech_war_moon_1",
    "giga_tech_war_moon_2",
    "giga_tech_war_moon_sections",
    "giga_tech_war_system_2",
    "giga_tech_war_system_3",
    "giga_tech_war_system_4",
    "giga_tech_war_system_5",
    "giga_tech_war_system_6",
    "tech_Carrier_1",
    "tech_Dreadnought_1",
    "tech_Flagship_1",
    "tech_heavycarrier_1",
    "tech_supercarrier_1",
    "esc_tech_dark_matter_power_core_2",
    "esc_tech_strikecraft_5",
    "tech_starbase_6",
}


def logical_sha256(text: str) -> str:
    canonical = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class ArchetypeOverlayContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.production = render_archetype_consumer_artifacts()
        cls.zero = render_archetype_consumer_artifacts(archetype_overlay=False)
        cls.rows = route_override_target_rows()
        cls.technology_rows = [
            row for row in cls.rows if row["object_type"] == "technology"
        ]

    def test_fixed_allowlist_has_exactly_nine_current_artifacts(self) -> None:
        self.assertEqual(
            tuple(self.production),
            ARCHETYPE_OVERLAY_ARTIFACT_PATHS,
        )
        self.assertEqual(len(self.production), 9)
        for path, rendered in self.production.items():
            self.assertEqual(
                path.read_text(encoding="utf-8").replace("\r\n", "\n"),
                rendered.replace("\r\n", "\n"),
            )

    def test_zero_overlay_technology_is_byte_equivalent_to_pre_h08c_head(self) -> None:
        self.assertEqual(
            {path: logical_sha256(self.zero[path]) for path in ZERO_OVERLAY_SHA256},
            ZERO_OVERLAY_SHA256,
        )

    def test_zero_overlay_keeps_global_wartime_budget_without_archetype_markers(self) -> None:
        budget = self.zero[FLEET_ALLOY_BUDGET_PATH]
        self.assertIn("staid_wartime_fleet_surge_ready = yes", budget)
        self.assertNotIn("staid_archetype_hard_", budget)

    def test_identity_strategy_vectors_are_bounded_and_state_free(self) -> None:
        strategy_paths = ARCHETYPE_OVERLAY_ARTIFACT_PATHS[2:]
        production = "\n".join(self.production[path] for path in strategy_paths)
        zero = "\n".join(self.zero[path] for path in strategy_paths)
        for marker in (
            "staid_archetype_research = yes",
            "staid_archetype_diplomatic = yes",
            "staid_archetype_defensive = yes",
            "staid_archetype_conquest = yes",
            "staid_archetype_extermination = yes",
            "staid_archetype_lead_secondary_research = yes",
            "staid_archetype_lead_secondary_diplomatic = yes",
            "staid_identity_megacorp = yes",
            "staid_identity_inward_perfection = yes",
            "staid_identity_barbaric_despoiler = yes",
            "staid_identity_rogue_servitor = yes",
            "staid_identity_assimilator = yes",
        ):
            self.assertIn(marker, production)
            self.assertNotIn(marker, zero)
        self.assertNotIn("staid_archetype_hard_", production)
        identity_lines = [
            line
            for line in production.splitlines()
            if re.search(
                r"staid_(?:archetype_(?:lead_secondary_)?(?:research|diplomatic|defensive|conquest|extermination)|identity_(?:megacorp|inward_perfection|barbaric_despoiler|rogue_servitor|assimilator))",
                line,
            )
        ]
        self.assertTrue(identity_lines)
        for line in identity_lines:
            factor = re.search(r"factor = ([0-9.]+)", line)
            self.assertIsNotNone(factor, line)
            self.assertTrue(1.0 < float(factor.group(1)) <= 1.15)
            for safety in (
                "staid_archetype_identity_conflict = no",
                "staid_archetype_eligible_country = yes",
                "staid_survival_mode = no",
                "staid_recovery_mode = no",
                "staid_catastrophic_collapse_mode = no",
                "staid_core_deficit_short_runway = no",
            ):
                self.assertIn(safety, line)
        inserted = []
        for path in IDENTITY_STRATEGY_ROUTE_OVERRIDE_PATHS:
            before = self.zero[path].replace("\r\n", "\n").splitlines()
            after = self.production[path].replace("\r\n", "\n").splitlines()
            matcher = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
            for tag, _i1, _i2, j1, j2 in matcher.get_opcodes():
                self.assertIn(tag, {"equal", "insert"}, path)
                if tag == "insert":
                    inserted.extend(after[j1:j2])
        delta = "\n".join(inserted)
        for forbidden in ("country_event =", "set_country_flag =", "create_fleet ="):
            self.assertNotIn(forbidden, delta)

    def test_identity_claim_pressure_is_bounded_and_preserves_distance_policy(self) -> None:
        production = self.production[IDENTITY_CLAIM_BUDGET_PATH]
        zero = self.zero[IDENTITY_CLAIM_BUDGET_PATH]
        for marker in (
            "staid_archetype_conquest = yes",
            "staid_archetype_lead_secondary_conquest = yes",
            "staid_identity_barbaric_despoiler = yes",
        ):
            self.assertEqual(production.count(marker), 3)
            self.assertNotIn(marker, zero)
        self.assertNotIn("staid_archetype_extermination = yes", production)
        self.assertNotIn("staid_archetype_hard_", production)
        for line in production.splitlines():
            if not any(
                marker in line
                for marker in (
                    "staid_archetype_conquest = yes",
                    "staid_archetype_lead_secondary_conquest = yes",
                    "staid_identity_barbaric_despoiler = yes",
                )
            ):
                continue
            factor = re.search(r"factor = ([0-9.]+)", line)
            self.assertIsNotNone(factor, line)
            self.assertTrue(1.0 < float(factor.group(1)) <= 1.15)
            for safety in (
                "staid_archetype_identity_conflict = no",
                "staid_archetype_eligible_country = yes",
                "has_potential_claims = yes",
                "staid_basic_economy_runway_safe = yes",
                "is_at_war = no",
                "staid_survival_mode = no",
                "staid_recovery_mode = no",
                "staid_catastrophic_collapse_mode = no",
                "staid_core_deficit_short_runway = no",
            ):
                self.assertIn(safety, line)
        defines = (TOOLS_ROOT.parent / "mods" / "StellarAIDirector" / "common" / "defines" / "zzzz_staid_14_high_scale_ai_defines.txt").read_text(encoding="utf-8")
        self.assertIn("WAR_DECLARATION_MAX_DISTANCE = 300", defines)
        self.assertIn("WAR_DECLARATION_MALUS_DISTANCE = 25", defines)

    def test_identity_static_defense_is_owner_scoped_bounded_and_parent_safe(self) -> None:
        production = "\n".join(
            self.production[path] for path in IDENTITY_STATIC_DEFENSE_PATHS
        )
        zero = "\n".join(self.zero[path] for path in IDENTITY_STATIC_DEFENSE_PATHS)
        expected_objects = sum(
            target["object_type"] in {"starbase_building", "starbase_module"}
            for target in ROUTE_OVERRIDE_TARGETS
        )
        for marker in (
            "staid_archetype_defensive = yes",
            "staid_archetype_lead_secondary_defensive = yes",
            "staid_identity_inward_perfection = yes",
        ):
            self.assertEqual(production.count(marker), expected_objects)
            self.assertNotIn(marker, zero)
        self.assertNotIn("staid_archetype_hard_", production)
        self.assertNotIn("staid_archetype_conquest = yes", production)
        self.assertNotIn("staid_archetype_extermination = yes", production)
        for line in production.splitlines():
            if not any(
                marker in line
                for marker in (
                    "staid_archetype_defensive = yes",
                    "staid_archetype_lead_secondary_defensive = yes",
                    "staid_identity_inward_perfection = yes",
                )
            ):
                continue
            self.assertIn("owner = {", line)
            factor = re.search(r"factor = ([0-9.]+)", line)
            self.assertIsNotNone(factor, line)
            self.assertTrue(1.0 < float(factor.group(1)) <= 1.15)
            for safety in (
                "staid_archetype_identity_conflict = no",
                "staid_archetype_eligible_country = yes",
                "staid_static_defense_investment_ready = yes",
                "staid_survival_mode = no",
                "staid_recovery_mode = no",
                "staid_catastrophic_collapse_mode = no",
                "staid_core_deficit_short_runway = no",
            ):
                self.assertIn(safety, line)
        for forbidden in (
            "starbase_level =",
            "ship_size =",
            "section_template =",
            "country_event =",
        ):
            self.assertNotIn(forbidden, production)

    def test_identity_megastructure_sequencing_is_start_only_and_country_scoped(self) -> None:
        production = self.production[IDENTITY_MEGASTRUCTURE_PATH]
        zero = self.zero[IDENTITY_MEGASTRUCTURE_PATH]
        start_ids = {
            "macro_test_site_0",
            "atmosphere_shredder_0",
            "think_tank_0",
            "planetary_computer_0",
            "ring_world_1",
            "interstellar_habitat_0",
            "stellar_ring_habitat_0",
            "mega_shipyard_0",
            "planetcraft_printer_0",
            "war_moon_0",
            "war_system_0",
            "dyson_sphere_0",
            "orbital_arc_furnace_1",
            "asteroid_manufactory_0",
            "matrioshka_brain_0_g_star",
        }
        expected_markers = {
            **{
                object_id: ("staid_archetype_research = yes",)
                for object_id in {
                    "macro_test_site_0",
                    "atmosphere_shredder_0",
                    "think_tank_0",
                    "planetary_computer_0",
                }
            },
            **{
                object_id: ("staid_archetype_gestalt_growth = yes",)
                for object_id in {
                    "ring_world_1",
                    "interstellar_habitat_0",
                    "stellar_ring_habitat_0",
                }
            },
            **{
                object_id: (
                    "staid_archetype_conquest = yes",
                    "staid_archetype_extermination = yes",
                    "staid_identity_barbaric_despoiler = yes",
                )
                for object_id in {
                    "mega_shipyard_0",
                    "planetcraft_printer_0",
                    "war_moon_0",
                    "war_system_0",
                }
            },
            **{
                object_id: ("staid_identity_megacorp = yes",)
                for object_id in {
                    "dyson_sphere_0",
                    "orbital_arc_furnace_1",
                    "asteroid_manufactory_0",
                    "matrioshka_brain_0_g_star",
                }
            },
        }
        for target in (
            row for row in ROUTE_OVERRIDE_TARGETS if row["object_type"] == "megastructure"
        ):
            block = extract_top_level_object_text(production, target["object_id"])
            zero_block = extract_top_level_object_text(zero, target["object_id"])
            has_identity = "staid_archetype_identity_conflict = no" in block
            self.assertEqual(has_identity, target["object_id"] in start_ids, target["object_id"])
            if has_identity:
                self.assertNotIn("staid_archetype_identity_conflict = no", zero_block)
                for marker in expected_markers[target["object_id"]]:
                    self.assertIn(marker, block)
                if target["object_id"] in {
                    "interstellar_habitat_0",
                    "stellar_ring_habitat_0",
                }:
                    self.assertIn("staid_identity_inward_perfection = yes", block)
                for line in block.splitlines():
                    if "staid_archetype_identity_conflict = no" not in line:
                        continue
                    self.assertIn("from = {", line)
                    factor = re.search(r"factor = ([0-9.]+)", line)
                    self.assertIsNotNone(factor, line)
                    self.assertTrue(1.0 < float(factor.group(1)) <= 1.15)
                    for safety in (
                        "staid_archetype_eligible_country = yes",
                        "staid_basic_economy_runway_safe = yes",
                        "staid_survival_mode = no",
                        "staid_recovery_mode = no",
                        "staid_catastrophic_collapse_mode = no",
                        "staid_core_deficit_short_runway = no",
                    ):
                        self.assertIn(safety, line)
        for excluded in (
            "habitat_central_complex",
            "matrioshka_brain_0_o_star",
            "dyson_sphere_0_o_star",
            "neutronium_gigaforge_0",
            "nidavellir_forge_0",
        ):
            block = extract_top_level_object_text(production, excluded)
            self.assertNotIn("staid_archetype_identity_conflict = no", block)

        # A mixed military identity may combine one primary vector, the other
        # vector's secondary role, and Barbaric Despoiler. Preserve blending,
        # but make its true cumulative ceiling explicit and regression-safe.
        military_block = extract_top_level_object_text(production, "mega_shipyard_0")

        def factor_for(marker: str) -> float:
            line = next(line for line in military_block.splitlines() if marker in line)
            match = re.search(r"factor = ([0-9.]+)", line)
            self.assertIsNotNone(match, line)
            return float(match.group(1))

        military_ceiling = max(
            factor_for("staid_archetype_conquest = yes")
            * factor_for("staid_archetype_lead_secondary_extermination = yes")
            * factor_for("staid_identity_barbaric_despoiler = yes"),
            factor_for("staid_archetype_extermination = yes")
            * factor_for("staid_archetype_lead_secondary_conquest = yes")
            * factor_for("staid_identity_barbaric_despoiler = yes"),
        )
        self.assertAlmostEqual(military_ceiling, 1.32825)
        self.assertLess(military_ceiling, 1.33)

    def test_production_overlay_is_additive_and_has_no_state_mutation(self) -> None:
        inserted: list[str] = []
        for path in ARCHETYPE_OVERLAY_ARTIFACT_PATHS:
            before = self.zero[path].replace("\r\n", "\n").splitlines()
            after = self.production[path].replace("\r\n", "\n").splitlines()
            matcher = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
            for tag, _i1, _i2, j1, j2 in matcher.get_opcodes():
                self.assertIn(tag, {"equal", "insert"}, path)
                if tag == "insert":
                    inserted.extend(after[j1:j2])
        delta = "\n".join(inserted)
        self.assertIn("staid_archetype_hard_", delta)
        for forbidden in (
            "set_country_flag",
            "country_event",
            "on_action",
            "set_variable",
            "change_variable",
            "add_resource",
            "economic_plan",
            "declare_war",
            "set_fleet_order",
        ):
            self.assertNotIn(forbidden, delta)
        self.assertEqual(
            self.production[TECHNOLOGY_ROUTE_OVERRIDE_PATH].count("any_country"),
            self.zero[TECHNOLOGY_ROUTE_OVERRIDE_PATH].count("any_country"),
        )
        self.assertEqual(
            self.production[FLEET_ALLOY_BUDGET_PATH].count("any_country"),
            self.zero[FLEET_ALLOY_BUDGET_PATH].count("any_country")
            + len(FLEET_ARCHETYPE_FACTORS)
            + 1,
        )

    def test_shared_route_renderer_keeps_every_generated_group_current(self) -> None:
        grouped: dict[Path, list[dict[str, object]]] = defaultdict(list)
        for row in self.rows:
            if row["object_type"] in {"building", "district"}:
                continue
            grouped[Path(str(row["generated_file"]))].append(row)
        self.assertEqual(len(grouped), 9)
        object_names = collect_object_names()
        for path, rows in grouped.items():
            rendered = route_override_file_text(rows, object_names)
            self.assertEqual(
                path.read_text(encoding="utf-8").replace("\r\n", "\n"),
                rendered.replace("\r\n", "\n"),
                path,
            )

    def test_ship_overlay_is_hard_anchored_and_emergency_neutral(self) -> None:
        production = extract_top_level_object_text(
            self.production[FLEET_ALLOY_BUDGET_PATH],
            "alloys_expenditure_ships",
        )
        zero = extract_top_level_object_text(
            self.zero[FLEET_ALLOY_BUDGET_PATH],
            "alloys_expenditure_ships",
        )

        for archetype, factor in FLEET_ARCHETYPE_FACTORS.items():
            marker = f"staid_archetype_hard_{archetype} = yes"
            self.assertEqual(production.count(marker), 1)
            block = fleet_archetype_budget_modifier(archetype, factor)
            self.assertIn(block, production)
            for guard in (
                "staid_archetype_identity_conflict = no",
                "staid_archetype_eligible_country = yes",
                "used_naval_capacity_percent < 0.80",
                "is_at_war = no",
                "NOT = { recently_lost_war = yes }",
                "staid_catastrophic_collapse_mode = no",
                "staid_core_deficit_short_runway = no",
                "has_ascension_perk = ap_become_the_crisis",
                "is_crisis_faction = yes",
            ):
                self.assertIn(guard, block)
            self.assertNotIn(f"staid_archetype_{archetype} = yes", block)

        for marker in (
            "factor = 3",
            "factor = 0.75",
            "factor = 0.33",
            "factor = 5",
            "factor = 0.25",
            "staid_peacetime_high_naval_capacity_guard = yes",
        ):
            self.assertEqual(production.count(marker), zero.count(marker))
        self.assertNotIn("Bounded H08c identity bias", zero)

    def test_ship_threat_response_is_bounded_stateless_and_emergency_neutral(self) -> None:
        production = extract_top_level_object_text(
            self.production[FLEET_ALLOY_BUDGET_PATH],
            "alloys_expenditure_ships",
        )
        zero = extract_top_level_object_text(
            self.zero[FLEET_ALLOY_BUDGET_PATH],
            "alloys_expenditure_ships",
        )
        block = fleet_threat_response_budget_modifier()

        self.assertIn(block, production)
        self.assertNotIn(block, zero)
        self.assertIn("factor = 1.10", block)
        for guard in (
            "highest_threat > 50",
            "used_naval_capacity_percent < 0.80",
            "is_at_war = no",
            "NOT = { recently_lost_war = yes }",
            "staid_catastrophic_collapse_mode = no",
            "staid_core_deficit_short_runway = no",
            "has_ascension_perk = ap_become_the_crisis",
            "is_crisis_faction = yes",
        ):
            self.assertIn(guard, block)
        for forbidden in (
            "has_monthly_income",
            "resource_stockpile_compare",
            "set_country_flag",
            "country_event",
            "economic_plan",
        ):
            self.assertNotIn(forbidden, block)
        maximum_overlap = FLEET_THREAT_RESPONSE_FACTOR * max(
            FLEET_ARCHETYPE_FACTORS.values()
        )
        self.assertAlmostEqual(maximum_overlap, 1.232)
        self.assertLessEqual(round(maximum_overlap, 3), 1.232)

    def test_technology_overlay_matches_only_reviewed_selectable_pairs(self) -> None:
        self.assertEqual(len(self.technology_rows), 42)
        seen_pairs: set[tuple[str, str]] = set()
        selectable_targets: set[str] = set()
        for target in self.technology_rows:
            lines = technology_archetype_weight_modifiers(target)
            expected = []
            if target["object_id"] not in TECHNOLOGY_ARCHETYPE_EXCLUDED_OBJECTS:
                for (
                    archetype,
                    route_factors,
                ) in TECHNOLOGY_ARCHETYPE_ROUTE_FACTORS.items():
                    if target["route_id"] in route_factors:
                        expected.append((archetype, route_factors[target["route_id"]]))
            self.assertEqual(len(lines), len(expected), target["object_id"])
            for line, (archetype, factor) in zip(lines, expected, strict=True):
                pair = (target["object_id"], archetype)
                self.assertNotIn(pair, seen_pairs)
                seen_pairs.add(pair)
                selectable_targets.add(target["object_id"])
                self.assertIn(f"factor = {factor}", line)
                self.assertIn(f"staid_archetype_hard_{archetype} = yes", line)
                self.assertIn("staid_archetype_identity_conflict = no", line)
                self.assertIn("staid_archetype_eligible_country = yes", line)
                for guard in (
                    f"{route_gate_for_target(target)} = yes",
                    "staid_survival_mode = no",
                    "staid_recovery_mode = no",
                    "staid_catastrophic_collapse_mode = no",
                    "staid_core_deficit_short_runway = no",
                    "is_at_war = no",
                    "NOT = { recently_lost_war = yes }",
                ):
                    self.assertIn(guard, line)
                self.assertGreater(factor, 1.0)
                self.assertLessEqual(factor, 1.15)
        self.assertEqual(selectable_targets, EXPECTED_SELECTABLE_TECHNOLOGY_IDS)
        self.assertEqual(len(seen_pairs), 45)

    def test_inert_or_event_granted_technologies_receive_no_overlay(self) -> None:
        by_id = {row["object_id"]: row for row in self.technology_rows}
        for object_id in TECHNOLOGY_ARCHETYPE_EXCLUDED_OBJECTS:
            self.assertIn(object_id, by_id)
            self.assertEqual(
                technology_archetype_weight_modifiers(by_id[object_id]),
                [],
            )
            block = extract_top_level_object_text(
                self.production[TECHNOLOGY_ROUTE_OVERRIDE_PATH],
                object_id,
            )
            self.assertNotIn("staid_archetype_hard_", block)

    def test_factor_zero_route_gate_precedes_and_dominates_identity_bias(self) -> None:
        technology = self.production[TECHNOLOGY_ROUTE_OVERRIDE_PATH]
        for target in self.technology_rows:
            lines = technology_archetype_weight_modifiers(target)
            if not lines:
                continue
            block = extract_top_level_object_text(technology, target["object_id"])
            route_veto = f"factor = 0 NOT = {{ {route_gate_for_target(target)} = yes }}"
            self.assertIn(route_veto, block)
            self.assertLess(
                block.index(route_veto),
                block.index("staid_archetype_hard_"),
            )

    def test_balanced_and_conflicted_identities_are_neutral(self) -> None:
        combined = "\n".join(self.production.values())
        self.assertNotIn("staid_archetype_balanced", combined)
        self.assertGreaterEqual(
            combined.count("staid_archetype_identity_conflict = no"),
            len(FLEET_ARCHETYPE_FACTORS),
        )

    def test_nontechnology_routes_and_invalid_factors_fail_safe(self) -> None:
        nontechnology = next(
            target
            for target in ROUTE_OVERRIDE_TARGETS
            if target["object_type"] != "technology"
        )
        self.assertEqual(technology_archetype_weight_modifiers(nontechnology), [])
        technology = next(
            target
            for target in self.technology_rows
            if target["route_id"] == "research_megastructure_core"
        )
        with self.assertRaisesRegex(ValueError, "must be in"):
            technology_archetype_weight_modifiers(
                technology,
                {"research": {"research_megastructure_core": 1.16}},
            )
        with self.assertRaisesRegex(ValueError, "must be in"):
            fleet_alloy_budget_text(archetype_factors={"extermination": 1.16})


class FocusedArchetypeOverlayGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.paths = (self.root / "ships.txt", self.root / "technology.txt")
        self.rendered = {
            self.paths[0]: "ships = { enabled = yes }\n",
            self.paths[1]: "technology = { enabled = yes }\n",
        }

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _run(self, mode: str, rendered: dict[Path, str] | None = None) -> int:
        with (
            mock.patch.object(
                overlay_cli,
                "ARCHETYPE_OVERLAY_ARTIFACT_PATHS",
                self.paths,
            ),
            mock.patch.object(
                overlay_cli,
                "render_archetype_consumer_artifacts",
                return_value=self.rendered if rendered is None else rendered,
            ),
        ):
            return overlay_cli.run(mode)

    def test_check_and_diff_are_read_only(self) -> None:
        for path, text in self.rendered.items():
            path.write_text(text, encoding="utf-8", newline="\n")
        self.paths[1].write_text(
            "technology = { enabled = no }\n",
            encoding="utf-8",
            newline="\n",
        )
        before = {path: path.read_bytes() for path in self.paths}
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self._run("check"), 1)
            self.assertEqual(self._run("diff"), 1)
        self.assertEqual(before, {path: path.read_bytes() for path in self.paths})

    def test_write_updates_only_stale_allowlisted_outputs(self) -> None:
        fresh = self.rendered[self.paths[0]].replace("\n", "\r\n").encode()
        self.paths[0].write_bytes(fresh)
        self.paths[1].write_text("stale = yes\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self._run("write"), 0)
        self.assertEqual(self.paths[0].read_bytes(), fresh)
        self.assertEqual(
            self.paths[1].read_text(encoding="utf-8"),
            self.rendered[self.paths[1]],
        )

    def test_allowlist_violation_and_invalid_cli_stop_before_writes(self) -> None:
        for path in self.paths:
            path.write_text("original = yes\n", encoding="utf-8")
        before = {path: path.read_bytes() for path in self.paths}
        stderr = io.StringIO()
        with (
            mock.patch.object(
                overlay_cli,
                "ARCHETYPE_OVERLAY_ARTIFACT_PATHS",
                self.paths,
            ),
            mock.patch.object(
                overlay_cli,
                "render_archetype_consumer_artifacts",
                return_value={self.paths[0]: self.rendered[self.paths[0]]},
            ),
            contextlib.redirect_stderr(stderr),
        ):
            self.assertEqual(overlay_cli.main(["write"]), 2)
        self.assertIn("fixed output allowlist", stderr.getvalue())
        self.assertEqual(before, {path: path.read_bytes() for path in self.paths})

        with (
            mock.patch.object(
                overlay_cli, "render_archetype_consumer_artifacts"
            ) as render,
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit) as raised,
        ):
            overlay_cli.main(["invalid"])
        self.assertEqual(raised.exception.code, 2)
        render.assert_not_called()


if __name__ == "__main__":
    unittest.main()
