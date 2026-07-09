import csv
import re
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stellar_ai_director_lib import (
    AI_SUPPORT_MAP_CSV,
    DEPENDENCY_EDGES_CSV,
    ECONOMIC_VALUATION_DATASET_CSV,
    ECONOMIC_VALUATION_DATASET_MD,
    ECONOMIC_VALUATION_EVIDENCE_MD,
    ECONOMIC_VALUATION_CANONICAL_COLUMNS,
    ECONOMIC_VALUATION_SOURCE_FACT_COLUMNS,
    EmpireState,
    GENERATED_VERSION_INVENTORY_MD,
    MANUAL_STATIC_VALIDATION_MD,
    MOD_ROOT,
    MOD_STACK_COMPATIBILITY_MD,
    OBJECT_ATLAS_CSV,
    POLICY_MATRIX_CSV,
    RESEARCH_ROOT,
    SNAPSHOT_ROOT,
    STANDALONE_PARITY_INVENTORY_CSV,
    STANDALONE_PARITY_INVENTORY_MD,
    block_assignments,
    collect_generated_conflict_rows,
    collect_generated_file_audit_rows,
    collect_generated_reference_rows,
    collect_object_names,
    economic_valuation_evidence_passes,
    economic_valuation_dataset_passes,
    dataset_job_pressure_override_rows,
    dataset_ai_resource_production_amounts,
    extract_top_level_object_text,
    fresh_economic_valuation_source_facts,
    generated_unresolved_at_variable_rows,
    generate_economic_valuation_dataset,
    generate_mod_files,
    generate_object_atlas_artifacts,
    mod_source_root_for_id,
    NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV,
    NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_MD,
    nonconstruction_economic_valuation_dataset_passes,
    parse_file,
    parse_pdx,
    resource_waste_pressure,
    research_under_curve,
    forbidden_generated_surface_errors,
    stale_stellar_ai_dependency_errors,
    surplus_sink_pressure,
    validate_staid_scripted_trigger_cycles,
    validate_generated_patch,
    validate_object_atlas_artifacts,
    write_text_file_preserving_generated_timestamp,
)


class ActiveStackEconomicValuationMaintenanceTests(unittest.TestCase):
    def test_generated_economic_values_match_current_active_mod_files(self):
        dataset_rows = []
        for path in (ECONOMIC_VALUATION_DATASET_CSV, NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV):
            with path.open("r", encoding="utf-8", newline="") as handle:
                dataset_rows.extend(list(csv.DictReader(handle)))

        fresh_facts = fresh_economic_valuation_source_facts(dataset_rows)
        drift_rows = []
        missing_rows = []
        for row in dataset_rows:
            object_key = (row["object_type"], row["object_id"])
            if row["object_type"] not in {
                "ascension_perk",
                "building",
                "colony_type",
                "decision",
                "deposit",
                "district",
                "edict",
                "policy",
                "pop_job",
                "resource",
                "starbase_building",
                "starbase_module",
                "technology",
                "tradition",
                "zone",
            }:
                continue
            actual = fresh_facts.get(object_key)
            if actual is None:
                missing_rows.append(f"{row['object_type']} `{row['object_id']}` expected at {row['winning_file']}")
                continue
            for column in ECONOMIC_VALUATION_SOURCE_FACT_COLUMNS:
                expected_value = str(row.get(column, ""))
                actual_value = str(actual.get(column, ""))
                if expected_value != actual_value:
                    drift_rows.append(
                        f"{row['object_type']} `{row['object_id']}` column `{column}` drifted: "
                        f"dataset={expected_value[:240]} current={actual_value[:240]} "
                        f"(dataset file {row['winning_file']}, current file {actual.get('winning_file', 'unknown')})"
                    )
                    break

        details = "\n".join([*missing_rows[:25], *drift_rows[:25]])
        overflow = len(missing_rows) + len(drift_rows) - 25
        if overflow > 0:
            details += f"\n... {overflow} more drift rows omitted"
        self.assertFalse(
            missing_rows or drift_rows,
            "Active mod economic source drift detected. Re-run the Stellar AI Director generator after reviewing the changed "
            "mod files; do not hand-edit the generated values.\n"
            + details,
        )


class GeneratedModValidityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        generate_object_atlas_artifacts(SNAPSHOT_ROOT)
        generate_mod_files()

    def test_generated_files_are_valid_load_surfaces(self):
        rows = collect_generated_file_audit_rows(MOD_ROOT)
        self.assertTrue(rows, "No generated mod files were found to validate.")
        bad_rows = [row for row in rows if row["status"] != "ok"]
        self.assertEqual(bad_rows, [])

    def test_descriptor_omits_stellar_ai_dependency_after_standalone_parity(self):
        descriptor = (MOD_ROOT / "descriptor.mod").read_text(encoding="utf-8")
        dependency_block = re.search(r"dependencies=\{\n(?P<body>.*?)\n\}", descriptor, re.DOTALL)
        self.assertIsNotNone(dependency_block)
        self.assertNotIn('"Stellar AI"', dependency_block.group("body"))
        self.assertIn('"Gigastructural Engineering & More (4.4)"', dependency_block.group("body"))
        self.assertIn('"NSC3"', dependency_block.group("body"))

        readme = (MOD_ROOT / "README.md").read_text(encoding="utf-8")
        load_order = (MOD_ROOT / "notes" / "load-order.md").read_text(encoding="utf-8")
        self.assertIn("Stellar AI remains a private parity reference", readme)
        self.assertIn("Stellar AI is not a required parent", load_order)
        self.assertEqual(stale_stellar_ai_dependency_errors(), [])

    def test_stale_stellar_ai_dependency_validator_rejects_current_requirements(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            mod_root = root / "StellarAIDirector"
            research_root = root / "research" / "stellar-ai"
            (mod_root / "notes").mkdir(parents=True)
            research_root.mkdir(parents=True)
            (mod_root / "descriptor.mod").write_text(
                'name="Stellar AI Director"\ndependencies={\n\t"Stellar AI"\n}\n',
                encoding="utf-8",
            )
            (mod_root / "README.md").write_text("This mod requires Stellar AI.\n", encoding="utf-8")
            (mod_root / "notes" / "load-order.md").write_text(
                "Stellar AI is not a required parent.\n",
                encoding="utf-8",
            )
            (research_root / "README.md").write_text(
                "Stellar AI remains a private parity reference only.\n",
                encoding="utf-8",
            )

            errors = stale_stellar_ai_dependency_errors(mod_root, research_root)

        self.assertTrue(any("descriptor must not require Stellar AI" in error for error in errors))
        self.assertTrue(any("current docs must not imply Stellar AI is required" in error for error in errors))

    def test_forbidden_surface_validator_blocks_unsafe_generated_folders(self):
        self.assertEqual(forbidden_generated_surface_errors(), [])

        with tempfile.TemporaryDirectory() as temp_dir:
            mod_root = Path(temp_dir) / "StellarAIDirector"
            (mod_root / "common" / "diplomatic_actions").mkdir(parents=True)
            (mod_root / "common" / "ship_designs").mkdir(parents=True)

            errors = forbidden_generated_surface_errors(mod_root)

        self.assertEqual(len(errors), 2)
        self.assertTrue(any("diplomatic_actions" in error for error in errors))
        self.assertTrue(any("ship_designs" in error for error in errors))

    def test_standalone_parity_inventory_covers_baseline_surfaces(self):
        self.assertTrue(STANDALONE_PARITY_INVENTORY_CSV.exists())
        self.assertTrue(STANDALONE_PARITY_INVENTORY_MD.exists())
        with STANDALONE_PARITY_INVENTORY_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        surfaces = {row["surface"] for row in rows}
        for surface in {
            "descriptor_dependencies",
            "common/ai_budget",
            "common/economic_plans",
            "buildings/districts/jobs/zones",
            "colony_types_designations_planet_roles",
            "personalities_diplomacy_war",
            "policies_edicts_defines",
            "research_economy_fleet_conversion",
            "generated_conflict_winners",
            "advanced_ship_design_nsc3_esc_gigas_runtime",
        }:
            self.assertIn(surface, surfaces)
        blocked = {row["surface"] for row in rows if row["classification"] == "defer"}
        self.assertIn("advanced_ship_design_nsc3_esc_gigas_runtime", blocked)
        text = STANDALONE_PARITY_INVENTORY_MD.read_text(encoding="utf-8")
        self.assertIn("private local parity reference", text)
        self.assertIn("not a launch dependency", text)

    def test_generated_references_resolve_to_known_objects(self):
        rows = collect_generated_reference_rows(MOD_ROOT, SNAPSHOT_ROOT)
        self.assertTrue(rows, "No generated references were found to validate.")
        missing_rows = [row for row in rows if row["status"] == "missing"]
        self.assertEqual(missing_rows, [])

    def test_generated_ai_budget_overrides_known_budget_objects(self):
        known_budget_objects = collect_object_names(SNAPSHOT_ROOT)["ai_budget"]
        budget_root = MOD_ROOT / "common" / "ai_budget"
        budget_files = sorted(budget_root.glob("*.txt"))
        self.assertTrue(budget_files, "No generated AI budget files were found.")
        unknown = []
        for file_path in budget_files:
            parsed = parse_file(file_path)
            for assignment in block_assignments(parsed):
                if assignment.key not in known_budget_objects:
                    unknown.append((file_path.relative_to(MOD_ROOT).as_posix(), assignment.key))
        self.assertEqual(unknown, [])

    def test_generated_conflict_rows_ignore_source_local_variables(self):
        rows = collect_generated_conflict_rows(MOD_ROOT, SNAPSHOT_ROOT)
        variable_rows = [row for row in rows if row["object_name"].startswith("@")]
        self.assertEqual(variable_rows, [])

    def test_active_stack_economic_valuation_dataset_covers_buildings_zones_and_districts(self):
        rows = generate_economic_valuation_dataset()
        self.assertTrue(rows)
        self.assertTrue(ECONOMIC_VALUATION_DATASET_CSV.exists())
        self.assertTrue(ECONOMIC_VALUATION_DATASET_MD.exists())
        self.assertTrue(economic_valuation_dataset_passes())

        object_types = {row["object_type"] for row in rows}
        self.assertIn("building", object_types)
        self.assertIn("zone", object_types)
        self.assertIn("district", object_types)

        esc_buildings = [
            row
            for row in rows
            if row["object_type"] == "building" and row["winning_mod_id"] == "2648658105"
        ]
        gigas_objects = [
            row
            for row in rows
            if row["object_type"] in {"building", "district"} and row["winning_mod_id"] == "1121692237"
        ]
        self.assertTrue(esc_buildings, "ESC advanced buildings were not captured.")
        self.assertTrue(gigas_objects, "Gigas advanced buildings or districts were not captured.")
        self.assertTrue(any(float(row["jobs_created_total_estimate"]) > 0 for row in rows))
        self.assertTrue(any(float(row["roi_2250_to_2350_estimate"]) > 0 for row in rows))

    def test_nonconstruction_economic_valuation_dataset_extends_without_duplicate_construction_surfaces(self):
        self.assertTrue(NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.exists())
        self.assertTrue(NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_MD.exists())
        self.assertTrue(nonconstruction_economic_valuation_dataset_passes())
        self.assertTrue(economic_valuation_evidence_passes())
        self.assertTrue(ECONOMIC_VALUATION_EVIDENCE_MD.exists())

        with NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            self.assertEqual(set(reader.fieldnames or []), set(ECONOMIC_VALUATION_CANONICAL_COLUMNS))
        with ECONOMIC_VALUATION_DATASET_CSV.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            construction_rows = list(reader)
            self.assertEqual(set(reader.fieldnames or []), set(ECONOMIC_VALUATION_CANONICAL_COLUMNS))

        self.assertFalse(
            [
                (row["object_type"], row["object_id"], column)
                for row in [*construction_rows, *rows]
                for column in ECONOMIC_VALUATION_CANONICAL_COLUMNS
                if row.get(column, "") == ""
            ]
        )
        object_types = {row["object_type"] for row in rows}
        self.assertFalse({"building", "zone", "district", "megastructure"} & object_types)
        self.assertTrue(
            {
                "pop_job",
                "decision",
                "edict",
                "deposit",
                "resource",
                "starbase_building",
                "starbase_module",
                "technology",
                "colony_type",
                "policy",
                "ascension_perk",
                "tradition",
            }.issubset(object_types)
        )

        evidence_text = ECONOMIC_VALUATION_EVIDENCE_MD.read_text(encoding="utf-8")
        self.assertIn("Construction Dataset Counts", evidence_text)
        self.assertIn("Nonconstruction Dataset Counts", evidence_text)
        self.assertIn("resource", evidence_text)

    def test_generated_timestamp_writer_preserves_stamp_when_body_is_unchanged(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.md"
            write_text_file_preserving_generated_timestamp(
                report_path,
                "# Report\n\nGenerated: first\n\nBody\n",
            )
            write_text_file_preserving_generated_timestamp(
                report_path,
                "# Report\n\nGenerated: second\n\nBody\n",
            )

            self.assertIn("Generated: first", report_path.read_text(encoding="utf-8"))

            write_text_file_preserving_generated_timestamp(
                report_path,
                "# Report\n\nGenerated: third\n\nChanged body\n",
            )

            updated = report_path.read_text(encoding="utf-8")
            self.assertIn("Generated: third", updated)
            self.assertIn("Changed body", updated)

    def test_dataset_job_pressure_overrides_use_live_valuation_rows(self):
        rows = dataset_job_pressure_override_rows()
        self.assertGreaterEqual(len(rows), 50)
        self.assertTrue(all(float(row["jobs_created_total_estimate"]) > 0 for row in rows))
        self.assertTrue(all(float(row["roi_2250_to_2350_estimate"]) > 0 for row in rows))
        self.assertIn("consumer_goods_repair", {row["pressure_family"] for row in rows})

        generated_files = [
            MOD_ROOT / "common" / "buildings" / "zzzz_staid_13_dataset_job_pressure_buildings.txt",
            MOD_ROOT / "common" / "districts" / "zzzz_staid_13_dataset_job_pressure_districts.txt",
        ]
        combined_text = ""
        for file_path in generated_files:
            self.assertTrue(file_path.exists(), f"{file_path} was not generated")
            text = file_path.read_text(encoding="utf-8")
            combined_text += text
            self.assertIn("staid_dataset_job_pressure", text)
            self.assertIn("num_unemployed > 0", text)
            self.assertIn("free_jobs < 1", text)
            self.assertIn("ai_weight_coefficient", text)
            parse_file(file_path)
        self.assertIn("family:consumer_goods_repair", combined_text)
        self.assertIn("staid_high_scale_snowball_pressure", combined_text)
        self.assertIn(
            "owner = { country_uses_consumer_goods = yes NOT = { staid_consumer_goods_runway_safe = yes } }",
            combined_text,
        )
        self.assertNotIn("factor = 0.35 owner = { staid_core_deficit_short_runway = yes }", combined_text)
        for invalid_marker in (
            "has_unemployed_pop_of_category",
            "job_acot_",
            "district_giga_frameworld_fortress_bunker",
            "district_generator_uncapped",
            "building_gas_extractors_max",
            "building_mote_harvesters_max",
            "building_crystal_mines_max",
        ):
            self.assertNotIn(invalid_marker, combined_text)
        district_text = generated_files[1].read_text(encoding="utf-8")
        self.assertNotIn("trade_value_add", district_text)

    def test_high_scale_ai_defines_remove_vanilla_construction_and_war_hesitation(self):
        defines_path = MOD_ROOT / "common" / "defines" / "zzzz_staid_14_high_scale_ai_defines.txt"
        self.assertTrue(defines_path.exists(), f"{defines_path} was not generated")
        parse_file(defines_path)
        text = defines_path.read_text(encoding="utf-8")
        for marker in (
            "AI_FREE_JOBS_BUILDING_BUILD_CAP = 5000",
            "AI_FOCUS_SCORE_MULT = 12",
            "AI_POPS_SCORE_MULT = 0.25",
            "AI_RESOURCE_TARGET_EXPIRATION_MONTHS = 6",
            "UNDERDEVELOPED_PLANET_LIMIT = 999",
            "BUILDING_BUILD_THRESHOLD = 0.1",
        ):
            self.assertIn(marker, text)
        for user_tuned_define in (
            "AI_AGGRESSIVENESS_BASE",
            "AI_WAR_PREPARATION_MIN_MONTHS",
            "WAR_DECLARATION_MAX_DISTANCE",
        ):
            self.assertRegex(text, rf"\b{user_tuned_define}\s*=")

    def test_minerals_planet_construction_budget_spends_harder_when_rich_or_crowded(self):
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_14_minerals_planet_construction_budget.txt"
        self.assertTrue(budget_path.exists(), f"{budget_path} was not generated")
        parse_file(budget_path)
        text = budget_path.read_text(encoding="utf-8")
        for marker in (
            "minerals_expenditure_planets_low = {",
            "minerals_expenditure_planets_med = {",
            "minerals_expenditure_planets_high = {",
            "category = planets",
            "staid_high_scale_snowball_pressure",
            "staid_core_deficit_short_runway",
            "any_owned_planet = { num_unemployed > 0 free_jobs < 1 }",
            "weight = 28.0",
            "modifier = { factor = 40 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }",
            "modifier = { add = 300000 any_owned_planet = { free_building_slots > 0 num_unemployed > 0 } }",
            "resource_stockpile_compare = { resource = minerals value > 25000 }",
        ):
            self.assertIn(marker, text)

    def test_mod_source_root_falls_back_to_live_workshop_when_snapshot_missing(self):
        root = mod_source_root_for_id("819148835")
        self.assertTrue(root.exists())
        self.assertIn("819148835", str(root))

    def test_pdx_parser_accepts_anonymous_nested_policy_blocks(self):
        parse_pdx(
            """
            orbital_bombardment = {
                option = {
                    name = "orbital_bombardment_indiscriminate"
                    in_breach_of = {
                        {
                            key = resolution_rulesofwar_independent_tribunals
                        }
                    }
                }
            }
            """
        )

    def test_static_validator_reports_no_invalid_references(self):
        self.assertEqual(validate_generated_patch(), [])

    def test_july7_computed_strategy_kernel_surfaces_are_generated(self):
        opening = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_10_opening_strategy_triggers.txt"
        kernel = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_20_strategy_kernel_triggers.txt"
        doctrine = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_11_fleet_doctrine_triggers.txt"
        for path in (opening, kernel, doctrine):
            self.assertTrue(path.exists(), f"Missing generated July 7 trigger surface: {path}")
            parse_file(path)

        opening_text = opening.read_text(encoding="utf-8")
        for marker in (
            "staid_opening_direct_research",
            "staid_opening_unity_to_research",
            "staid_opening_military_to_pops",
            "staid_opening_defensive_tall_research",
            "staid_opening_trade_to_research",
            "staid_opening_hive_growth_research",
            "staid_opening_machine_growth_research",
            "staid_opening_nomad_arkship_research",
        ):
            self.assertIn(marker, opening_text)

        kernel_text = kernel.read_text(encoding="utf-8")
        for marker in (
            "staid_is_opening_phase",
            "staid_is_midgame_scaling_phase",
            "staid_has_safe_basic_stockpiles",
            "staid_can_afford_research_push",
            "staid_security_threatened",
            "staid_security_existential",
            "staid_megastructure_prereq_release",
            "staid_fleet_strategic_aggression_mode",
        ):
            self.assertIn(marker, kernel_text)

        doctrine_text = doctrine.read_text(encoding="utf-8")
        for marker in (
            "staid_fleet_energy_shield_doctrine",
            "staid_fleet_kinetic_armor_doctrine",
            "staid_fleet_missile_evasion_doctrine",
            "staid_fleet_carrier_strikecraft_doctrine",
            "staid_fleet_balanced_filler_doctrine",
        ):
            self.assertIn(marker, doctrine_text)

    def test_opening_route_trigger_references_resolve_across_generated_surfaces(self):
        opening = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_10_opening_strategy_triggers.txt"
        kernel = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_20_strategy_kernel_triggers.txt"
        opening_text = opening.read_text(encoding="utf-8")
        kernel_text = kernel.read_text(encoding="utf-8")

        defined_opening_routes = set(re.findall(r"(?m)^(staid_opening_[A-Za-z0-9_]+)\s*=\s*\{", opening_text))
        required_opening_routes = {
            "staid_opening_direct_research",
            "staid_opening_unity_to_research",
            "staid_opening_military_to_pops",
            "staid_opening_hostile_fauna_clearance",
            "staid_opening_defensive_tall_research",
            "staid_opening_trade_to_research",
            "staid_opening_hive_growth_research",
            "staid_opening_machine_growth_research",
            "staid_opening_nomad_arkship_research",
            "staid_opening_any_research_route",
        }
        self.assertTrue(required_opening_routes.issubset(defined_opening_routes))

        required_kernel_gates = {
            "staid_is_opening_phase",
            "staid_has_safe_basic_stockpiles",
            "staid_can_afford_research_push",
            "staid_security_existential",
            "staid_opening_route_research_priority",
        }
        defined_kernel_gates = set(re.findall(r"(?m)^(staid_[A-Za-z0-9_]+)\s*=\s*\{", kernel_text))
        self.assertTrue(required_kernel_gates.issubset(defined_kernel_gates))

        generated_common_files = [
            path
            for path in (MOD_ROOT / "common").glob("**/*.txt")
            if path.name.startswith(("zzz_staid_", "zzzz_staid_"))
        ]
        defined_route_surface = defined_opening_routes | defined_kernel_gates
        missing_references = {}
        consumer_paths = set()
        for path in generated_common_files:
            text = path.read_text(encoding="utf-8")
            references = set(re.findall(r"\b(staid_opening_[A-Za-z0-9_]+)\b", text))
            missing = references - defined_route_surface
            if missing:
                missing_references[str(path.relative_to(MOD_ROOT))] = sorted(missing)
            if references and path != opening:
                consumer_paths.add(path.relative_to(MOD_ROOT).as_posix())

        self.assertEqual(missing_references, {})
        self.assertIn("common/economic_plans/zzzz_staid_additive_economic_plan.txt", consumer_paths)
        self.assertIn("common/policies/zzzz_staid_10_opening_growth_policies.txt", consumer_paths)
        self.assertIn("common/edicts/zzzz_staid_10_opening_growth_edicts.txt", consumer_paths)
        self.assertNotRegex(opening_text + kernel_text, r"\b(set|has)_country_flag\s*=\s*staid_opening_")

    def test_july7_policy_and_edict_overrides_are_generated_from_verified_ids(self):
        policy = MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt"
        edicts = MOD_ROOT / "common" / "edicts" / "zzzz_staid_10_opening_growth_edicts.txt"
        for path in (policy, edicts):
            self.assertTrue(path.exists(), f"Missing generated July 7 policy/edict surface: {path}")
            parse_file(path)

        policy_text = policy.read_text(encoding="utf-8")
        self.assertIn("diplomatic_stance", policy_text)
        self.assertIn("diplo_stance_cooperative", policy_text)
        self.assertIn("staid_opening_route_research_priority", policy_text)
        self.assertIn("diplo_stance_cooperative_nomad", policy_text)

        edicts_text = edicts.read_text(encoding="utf-8")
        for marker in (
            "research_subsidies",
            "encourage_free_thought",
            "map_the_stars",
            "capacity_subsidies",
            "mining_subsidies",
            "farming_subsidies",
            "fortify_the_border",
            "staid_security_threatened",
        ):
            self.assertIn(marker, edicts_text)

    def test_planetary_diversity_outpost_decisions_are_director_weighted(self):
        decisions_path = MOD_ROOT / "common" / "decisions" / "zzzz_staid_12_planetary_diversity_outpost_decisions.txt"
        triggers_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        self.assertTrue(decisions_path.exists(), "Missing generated Planetary Diversity decision override file.")
        parse_file(decisions_path)

        decisions_text = decisions_path.read_text(encoding="utf-8")
        triggers_text = triggers_path.read_text(encoding="utf-8")
        economy_text = economy_path.read_text(encoding="utf-8")
        for decision_id in (
            "decision_build_pd_moon_base",
            "decision_build_pd_moon_base_moon_colony",
            "decision_build_pd_mining_base",
            "decision_build_pd_mining_base_2",
            "decision_build_pd_mining_base_3",
            "decision_build_pd_food_base",
            "decision_build_pd_food_base_2",
            "decision_build_pd_food_base_3",
            "decision_build_pd_energy_base",
            "decision_build_pd_energy_base_2",
            "decision_build_pd_energy_base_3",
            "decision_build_pd_research_base",
            "decision_build_pd_research_base_2",
            "decision_build_pd_research_base_3",
        ):
            self.assertIn(f"{decision_id} = {{", decisions_text)

        research_block = decisions_text[
            decisions_text.index("decision_build_pd_research_base = {") : decisions_text.index(
                "decision_build_pd_research_base_2 = {"
            )
        ]
        ai_weight = re.search(r"ai_weight\s*=\s*\{(?P<body>.*?)\n\t\}", research_block, re.S)
        self.assertIsNotNone(ai_weight)
        ai_weight_text = ai_weight.group("body")
        self.assertIn("Availability owns prerequisites", ai_weight_text)
        self.assertIn("Lifetime value formula", ai_weight_text)
        self.assertIn("modifier = { factor = 16 years_passed < 30 }", ai_weight_text)
        self.assertIn("modifier = { factor = 13 AND = { years_passed > 29 years_passed < 60 } }", ai_weight_text)
        self.assertIn("modifier = { factor = 9 AND = { years_passed > 59 years_passed < 100 } }", ai_weight_text)
        self.assertIn("modifier = { factor = 3 AND = { years_passed > 99 years_passed < 150 } }", ai_weight_text)
        self.assertIn("modifier = { factor = 8 owner = { staid_pd_research_outpost_priority_ready = yes } }", ai_weight_text)
        self.assertIn("modifier = { factor = 7 is_capital = yes }", ai_weight_text)
        self.assertNotIn("has_technology", ai_weight_text)
        self.assertNotIn("pd_domed_research_site", ai_weight_text)
        self.assertIn("staid_planetary_diversity_outpost_investment_ready", triggers_text)
        self.assertIn("Stellar AI Director Planetary Diversity outpost reserve", economy_text)

    def test_planetary_diversity_modifier_profiles_drive_building_roles(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_12_planetary_diversity_value_triggers.txt"
        building_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_12_planetary_diversity_buildings.txt"
        profile_path = RESEARCH_ROOT / "stellar-ai-director-planetary-diversity-profile-2026-07-07.md"
        for path in (trigger_path, building_path):
            self.assertTrue(path.exists(), f"Missing generated PD profile surface: {path}")
            parse_file(path)

        trigger_text = trigger_path.read_text(encoding="utf-8")
        building_text = building_path.read_text(encoding="utf-8")
        profile_text = profile_path.read_text(encoding="utf-8")
        for marker in (
            "staid_pd_planet_research_value",
            "staid_pd_planet_alloys_value",
            "staid_pd_planet_minerals_value",
            "staid_pd_planet_energy_value",
            "staid_pd_planet_growth_value",
        ):
            self.assertIn(marker, trigger_text)
        self.assertIn("building_megalfora_lab", building_text)
        self.assertIn("pd_economic_role = research", building_text)
        self.assertIn("strategic value horizon year", (MOD_ROOT / "notes" / "tuning-notes.md").read_text(encoding="utf-8"))
        self.assertIn("Hostile Space Fauna Clearance", profile_text)

    def test_militarist_conquest_and_raiding_surfaces_are_generated(self):
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        policies_path = MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt"
        bombardment_path = MOD_ROOT / "common" / "bombardment_stances" / "zzzz_staid_12_militarist_raiding_bombardment.txt"
        ascension_path = MOD_ROOT / "common" / "ascension_perks" / "zzzz_staid_02_perks_traditions_ascension_perks.txt"
        for path in (policies_path, bombardment_path):
            self.assertTrue(path.exists(), f"Missing generated militarist surface: {path}")
            parse_file(path)
        policies = policies_path.read_text(encoding="utf-8")
        bombardment = bombardment_path.read_text(encoding="utf-8")
        ascension_perks = ascension_path.read_text(encoding="utf-8")
        for marker in (
            "staid_militarist_conquest_strategy",
            "staid_raiding_pop_growth_strategy",
            "staid_hostile_fauna_safe_clearance_window",
            "staid_hostile_fauna_clearance_strategy",
            "staid_raiding_pop_acquisition_priority",
        ):
            self.assertIn(marker, triggers)
        conquest_block = triggers[
            triggers.index("staid_militarist_conquest_strategy = {") : triggers.index(
                "staid_raiding_pop_growth_strategy = {"
            )
        ]
        raiding_block = triggers[
            triggers.index("staid_raiding_pop_growth_strategy = {") : triggers.index(
                "staid_raiding_pop_acquisition_priority = {"
            )
        ]
        self.assertIn("used_naval_capacity_percent < 1.95", conquest_block)
        self.assertIn("used_naval_capacity_percent < 2.00", raiding_block)
        self.assertIn("staid_catastrophic_collapse_mode", conquest_block + raiding_block)
        self.assertNotIn("staid_core_deficit_short_runway", conquest_block + raiding_block)
        self.assertNotIn("staid_survival_mode", conquest_block + raiding_block)
        self.assertNotIn("recently_lost_war", conquest_block + raiding_block)
        for marker in (
            "Stellar AI Director militarist conquest fleet reserve",
            "Stellar AI Director raiding pop acquisition reserve",
            "Stellar AI Director hostile fauna clearance reserve",
        ):
            self.assertIn(marker, economy)
        self.assertIn("staid_militarist_conquest_strategy", policies)
        self.assertIn("orbital_bombardment = {", policies)
        self.assertIn("orbital_bombardment_indiscriminate", policies)
        self.assertNotIn("factor = 24 staid_raiding_pop_growth_strategy = yes", policies)
        self.assertIn("factor = 18 staid_militarist_conquest_strategy = yes", policies)
        self.assertIn("orbital_bombardment_accept_surrender = {", policies)
        self.assertIn("orbital_bombardment_surrender_forbidden", policies)
        self.assertIn("base = 1", policies)
        self.assertIn("factor = 80 staid_raiding_pop_growth_strategy = yes", policies)
        self.assertNotIn("Orbital bombardment policy is documented as a follow-up", policies)
        self.assertIn("raiding = {", bombardment)
        self.assertIn("abduct_pops = yes", bombardment)
        self.assertIn("factor = 60 owner = { staid_raiding_pop_growth_strategy = yes }", bombardment)
        self.assertIn("ap_nihilistic_acquisition", ascension_perks)
        self.assertIn("staid_raiding_pop_acquisition_priority", ascension_perks)

    def test_hostile_fauna_reserve_stays_on_safe_clearance_window(self):
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        safe_window_block = triggers[
            triggers.index("staid_hostile_fauna_safe_clearance_window = {") : triggers.index(
                "staid_hostile_fauna_clearance_strategy = {"
            )
        ]
        strategy_block = triggers[
            triggers.index("staid_hostile_fauna_clearance_strategy = {") : triggers.index(
                "staid_site_limited_expansion_ready = {"
            )
        ]
        reserve_block = economy[
            economy.index('set_name = "Stellar AI Director hostile fauna clearance reserve"') : economy.index(
                'set_name = "Stellar AI Director modded unlock research reserve"'
            )
        ]

        self.assertIn("staid_fleet_buildup_economy_safe = yes", safe_window_block)
        self.assertIn("NOT = { staid_security_existential = yes }", safe_window_block)
        self.assertIn("used_naval_capacity_percent < 1.20", safe_window_block)
        self.assertIn("has_monthly_income = { resource = alloys value > 60 }", safe_window_block)
        self.assertIn("staid_hostile_fauna_safe_clearance_window = yes", strategy_block)
        self.assertIn("staid_hostile_fauna_clearance_strategy = yes", reserve_block)

        forbidden_targets = (
            "crystal_station_large",
            "leviathan_01_scavenger_bot",
            "leviathan_01_elder_tiyanki",
            "leviathan_01_voidspawn",
            "reanimated_leviathan_01_elder_tiyanki",
            "reanimated_leviathan_01_voidspawn",
            "reanimated_space_dragon",
            "tech_leviathan_techgenesis",
        )
        forbidden_effects = (
            "fleet_event =",
            "country_event =",
            "create_fleet =",
            "declare_war",
            "every_owned_fleet",
        )
        for block in (safe_window_block, strategy_block, reserve_block):
            for target in forbidden_targets:
                self.assertNotIn(target, block)
            for effect in forbidden_effects:
                self.assertNotIn(effect, block)

    def test_dataset_job_pressure_adds_ai_resource_production(self):
        amounts = dataset_ai_resource_production_amounts(
            {
                "object_id": "building_test_research_jobs",
                "object_type": "building",
                "jobs_created_total_estimate": "300",
                "direct_monthly_output_json": "{}",
                "modifier_keys": "job_researcher_add|planet_researchers_physics_research_produces_add",
                "pressure_family": "research_scaling",
            }
        )
        self.assertEqual(amounts["physics_research"], 1)
        self.assertIn("society_research", amounts)
        self.assertIn("engineering_research", amounts)

        direct_amounts = dataset_ai_resource_production_amounts(
            {
                "object_id": "building_test_factory",
                "object_type": "building",
                "jobs_created_total_estimate": "0",
                "direct_monthly_output_json": '{"consumer_goods":35.0}',
                "modifier_keys": "",
                "pressure_family": "consumer_goods_repair",
            }
        )
        self.assertEqual(direct_amounts, {"consumer_goods": 35})

    def test_high_scale_construction_plan_and_budget_pressure_are_generated(self):
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_14_minerals_planet_construction_budget.txt"
        building_pressure_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_13_dataset_job_pressure_buildings.txt"
        district_pressure_path = MOD_ROOT / "common" / "districts" / "zzzz_staid_13_dataset_job_pressure_districts.txt"
        zone_pressure_path = MOD_ROOT / "common" / "zones" / "zzzz_staid_13_dataset_job_pressure_zones.txt"
        for path in (economy_path, budget_path, building_pressure_path, district_pressure_path):
            self.assertTrue(path.exists(), f"Missing generated high-scale construction surface: {path}")
            parse_file(path)
        self.assertFalse(zone_pressure_path.exists(), "Zone full-object copies are runtime-unsafe and must not load.")
        economy = economy_path.read_text(encoding="utf-8")
        budget = budget_path.read_text(encoding="utf-8")
        pressure = (
            building_pressure_path.read_text(encoding="utf-8")
            + district_pressure_path.read_text(encoding="utf-8")
        )
        for marker in (
            "Stellar AI Director construction spenddown reserve",
            "Stellar AI Director unemployed pop construction catch-up",
            "Stellar AI Director open slot construction catch-up",
            "Stellar AI Director rich empire spend-down construction",
        ):
            self.assertIn(marker, economy)
        self.assertIn("staid_construction_spenddown_pressure = yes", economy)
        self.assertNotIn("empire_size =", economy)
        self.assertIn("staid_construction_spenddown_pressure = {", pressure + (
            MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        ).read_text(encoding="utf-8"))
        self.assertIn("modifier = { factor = 40 any_owned_planet = { num_unemployed > 0 free_jobs < 1 } }", budget)
        self.assertIn("modifier = { factor = 35 staid_construction_spenddown_pressure = yes }", budget)
        self.assertIn("resource_stockpile_compare = { resource = minerals value > 25000 }", budget)
        self.assertIn("ai_resource_production = {", pressure)
        self.assertIn("owner = { staid_construction_spenddown_pressure = yes }", pressure)
        self.assertNotIn("factor = 0 owner = { AND = { staid_survival_mode = yes", pressure)
        trigger_text = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        construction_block = trigger_text[
            trigger_text.index("staid_construction_spenddown_pressure = {") : trigger_text.index(
                "staid_research_under_curve = {"
            )
        ]
        self.assertIn("NOT = { staid_catastrophic_collapse_mode = yes }", construction_block)
        self.assertNotIn("staid_recovery_mode", construction_block)

    def test_staid_scripted_trigger_graph_has_no_cycles(self):
        self.assertEqual(validate_staid_scripted_trigger_cycles(MOD_ROOT), [])

    def test_july7_inventory_and_static_validation_notes_are_generated(self):
        for path in (GENERATED_VERSION_INVENTORY_MD, MOD_STACK_COMPATIBILITY_MD, MANUAL_STATIC_VALIDATION_MD):
            self.assertTrue(path.exists(), f"Missing generated July 7 note: {path}")
            text = path.read_text(encoding="utf-8")
            self.assertIn("Generated by `tools/generate_stellar_ai_director_patch.py`", text)
        inventory = GENERATED_VERSION_INVENTORY_MD.read_text(encoding="utf-8")
        self.assertIn("4.4.5", inventory)
        self.assertIn("v4.4.*", inventory)
        compatibility = MOD_STACK_COMPATIBILITY_MD.read_text(encoding="utf-8")
        self.assertIn("computed scripted triggers", compatibility)
        validation = MANUAL_STATIC_VALIDATION_MD.read_text(encoding="utf-8")
        self.assertIn("no Stellaris launch", validation)

    def test_stockpile_waste_and_low_research_activate_surplus_sink(self):
        state = EmpireState(
            incomes={
                "energy": 200,
                "alloys": 80,
                "trade": 20,
                "minerals": 900,
                "food": 300,
                "consumer_goods": 300,
                "physics_research": 500,
                "society_research": 500,
                "engineering_research": 700,
            },
            stockpiles={
                "minerals": 82000,
                "food": 82000,
                "consumer_goods": 65000,
            },
            research_sink_available=True,
        )
        self.assertTrue(resource_waste_pressure(state))
        self.assertTrue(research_under_curve(state, years_passed=165))
        self.assertTrue(surplus_sink_pressure(state))

    def test_generated_research_and_market_safety_surfaces_cover_runtime_failures(self):
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        market_events = (MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt").read_text(
            encoding="utf-8"
        )
        for marker in (
            "staid_resource_waste_pressure",
            "resource_stockpile_compare = { resource = minerals value > 25000 }",
            "resource_stockpile_compare = { resource = consumer_goods value > 18000 }",
            "staid_consumer_goods_runway_safe",
            "staid_food_runway_safe",
            "staid_research_input_runway_safe",
            "Stellar AI Director consumer goods runway repair",
            "Stellar AI Director food break-even repair",
            "staid_research_under_curve",
            "Stellar AI Director capped stockpile research conversion",
            "Stellar AI Director 2360 engineering catchup",
            "value:stellarai_market_sell_value|RESOURCE|minerals|AMOUNT|5000|",
            "value:stellarai_market_sell_value|RESOURCE|giga_sr_sentient_metal|AMOUNT|250|",
            "staid_high_scale_snowball_pressure",
            "Stellar AI Director pathological snowball reserve",
            "Stellar AI Director megastructure spam reserve",
        ):
            self.assertIn(marker, triggers + economy + market_events)

    def test_generated_stranded_fleet_recovery_uses_guarded_vanilla_mia(self):
        on_action_path = MOD_ROOT / "common" / "on_actions" / "zzz_staid_market_and_fleet_safety_on_actions.txt"
        event_path = MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt"
        parse_file(on_action_path)
        parse_file(event_path)
        text = event_path.read_text(encoding="utf-8")
        for marker in (
            "staid_homeland_under_attack = yes",
            "can_go_mia = yes",
            "is_fleet_idle = yes",
            "is_in_combat = no",
            "has_fleet_flag = staid_stranded_fleet_warning",
            "set_timed_fleet_flag",
            "set_mia = mia_return_home",
            "space_owner = { NOT = { is_same_value = root } }",
        ):
            self.assertIn(marker, text)

    def test_route_overrides_carry_source_local_variables(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        technology_text = technology_path.read_text(encoding="utf-8")
        megastructure_text = megastructure_path.read_text(encoding="utf-8")
        for marker in ("@tier4cost4 = 28000", "@tier5weight3 = 20"):
            self.assertIn(marker, technology_text)
        for marker in ("@giga_mega_unity_cost", "@giga_giga_unity_cost"):
            self.assertIn(marker, megastructure_text)
        self.assertEqual(generated_unresolved_at_variable_rows(MOD_ROOT), [])

    def test_megastructure_route_weights_use_country_from_scope(self):
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        parse_file(megastructure_path)
        megastructure_text = megastructure_path.read_text(encoding="utf-8")
        macro_test_site_block = megastructure_text[
            megastructure_text.index("macro_test_site_3 = {") : megastructure_text.index("atmosphere_shredder_0 = {")
        ]
        for marker in (
            "modifier = { factor = 0 from = { staid_survival_mode = yes } }",
            "modifier = { factor = 0 from = { NOT = { staid_science_kilo_build_priority_ready = yes } } }",
            "modifier = { factor = 4 from = { staid_science_kilo_build_priority_ready = yes } }",
            "modifier = { factor = 4 from = { has_technology = giga_tech_engineering_test_site } }",
            "modifier = { factor = 3 from = { staid_research_under_curve = yes } }",
        ):
            self.assertIn(marker, macro_test_site_block)
        for marker in (
            "modifier = { factor = 0 staid_survival_mode = yes }",
            "modifier = { factor = 0 NOT = { staid_science_kilo_build_priority_ready = yes } }",
            "modifier = { factor = 4 staid_science_kilo_build_priority_ready = yes }",
            "modifier = { factor = 4 has_technology = giga_tech_engineering_test_site }",
            "modifier = { factor = 3 staid_research_under_curve = yes }",
        ):
            self.assertNotIn(marker, macro_test_site_block)

    def test_research_and_pop_assembly_buildings_have_owner_economy_gates(self):
        research_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_06_research_infrastructure_buildings.txt"
        research_district_path = MOD_ROOT / "common" / "districts" / "zzzz_staid_06_research_infrastructure_districts.txt"
        pop_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_07_pop_assembly_buildings.txt"
        parse_file(research_path)
        parse_file(research_district_path)
        parse_file(pop_path)
        research_text = research_path.read_text(encoding="utf-8")
        research_district_text = research_district_path.read_text(encoding="utf-8")
        pop_text = pop_path.read_text(encoding="utf-8")
        self.assertIn(
            "modifier = { factor = 0 owner = { NOT = { staid_research_input_runway_safe = yes } } }",
            research_text,
        )
        for marker in (
            "modifier = { factor = 5 owner = { staid_research_under_curve = yes } }",
            "modifier = { factor = 4 owner = { staid_opening_route_research_priority = yes } }",
            "modifier = { factor = 3 owner = { staid_surplus_sink_pressure = yes } }",
        ):
            self.assertIn(marker, research_text)
        self.assertIn(
            "modifier = { factor = 0 owner = { NOT = { staid_planetary_capacity_growth_ready = yes } } }",
            research_district_text,
        )
        self.assertIn(
            "modifier = { factor = 3 owner = { staid_research_under_curve = yes } }",
            research_district_text,
        )
        self.assertIn(
            "modifier = { factor = 0 owner = { NOT = { staid_pop_assembly_snowball_ready = yes } } }",
            pop_text,
        )
        for marker in (
            "modifier = { factor = 6 owner = { OR = { has_origin = origin_mechanists has_country_flag = synthetic_empire } } }",
            "modifier = { factor = 4 owner = { is_materialist = yes } }",
            "modifier = { factor = 7 owner = { OR = { is_machine_empire = yes is_individual_machine = yes } } }",
            "modifier = { factor = 5 owner = { OR = { has_technology = tech_cloning has_cloning_tradition = yes } } }",
            "modifier = { factor = 3 owner = { has_ascension_perk = ap_engineered_evolution } }",
            "modifier = { factor = 6 owner = { is_hive_empire = yes } }",
            "modifier = { factor = 0 owner = { has_origin = origin_progenitor_hive } }",
            "modifier = { factor = 8 owner = { has_origin = origin_progenitor_hive } }",
        ):
            self.assertIn(marker, pop_text)
        for marker in (
            "is_regular_empire = yes",
            "NOT = { has_policy_flag = robots_outlawed }",
            "OR = {\n\t\t\t\tis_machine_empire = yes\n\t\t\t\tis_individual_machine = yes",
            "is_hive_empire = yes",
            "NOT = { has_origin = origin_progenitor_hive }",
            "has_origin = origin_progenitor_hive",
        ):
            self.assertIn(marker, pop_text)

    def test_habitat_route_override_repairs_gigas_spawn_effect_parameters(self):
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        parse_file(megastructure_path)
        megastructure_text = megastructure_path.read_text(encoding="utf-8")
        habitat_block = megastructure_text[
            megastructure_text.index("habitat_central_complex = {") : megastructure_text.index(
                "interstellar_habitat_0 = {"
            )
        ]
        self.assertIn("spawn_habitat_effect = {", habitat_block)
        self.assertIn("HABITAT_OWNER = root", habitat_block)
        self.assertIn("TARGET_PLANET = event_target:target_planet", habitat_block)
        self.assertNotIn("spawn_habitat_effect = {\n                DISTANCE =", habitat_block)

    def test_gigas_habitat_compat_effects_fail_closed_on_removed_orbital_ship_sizes(self):
        scripted_effects_path = (
            MOD_ROOT / "common" / "scripted_effects" / "zzz_staid_gigas_habitat_compat_effects.txt"
        )
        parse_file(scripted_effects_path)
        text = scripted_effects_path.read_text(encoding="utf-8")
        for marker in (
            "science_kilo_update_orbital_effect = {",
            "giga_dismantle_science_kilo_effect = {",
            "always = no # removed stale major_orbital_resource ship-size probe",
            "always = no # removed stale minor_orbital_resource ship-size probe",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("is_ship_size = major_orbital_resource", text)
        self.assertNotIn("is_ship_size = minor_orbital_resource", text)
        self.assertNotIn("is_ship_size = major_orbital", text)
        self.assertNotIn("is_ship_size = minor_orbital", text)
        self.assertNotIn("is_ship_size = habitat_major_orbital", text)
        self.assertNotIn("is_ship_size = habitat_minor_orbital", text)

    def test_ai_budget_overrides_do_not_emit_unsupported_ai_weight_blocks(self):
        budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_08_site_limited_expansion_ai_budget.txt"
        parse_file(budget_path)
        text = budget_path.read_text(encoding="utf-8")
        self.assertIn("influence_expenditure_claims = {", text)
        self.assertIn("weight = {", text)
        self.assertNotIn("ai_weight = {", text)

    def test_starbase_route_weights_use_owner_country_scope(self):
        starbase_path = (
            MOD_ROOT / "common" / "starbase_buildings" / "zzzz_staid_05_starbase_defense_starbase_buildings.txt"
        )
        module_path = MOD_ROOT / "common" / "starbase_modules" / "zzzz_staid_05_starbase_defense_starbase_modules.txt"
        parse_file(starbase_path)
        parse_file(module_path)
        text = starbase_path.read_text(encoding="utf-8")
        module_text = module_path.read_text(encoding="utf-8")
        triggers = (MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").read_text(
            encoding="utf-8"
        )
        economy = (MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt").read_text(
            encoding="utf-8"
        )
        self.assertIn("modifier = { factor = 1.5 owner = { staid_survival_mode = yes } }", text)
        self.assertIn("modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }", text)
        self.assertIn("modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }", text)
        self.assertNotIn("modifier = { factor = 0 owner = { staid_survival_mode = yes } }", text)
        self.assertNotIn("modifier = { factor = 0 staid_survival_mode = yes }", text)
        self.assertIn("staid_militarist_conquest_strategy = yes", triggers)
        self.assertNotIn("NOT = { staid_aggressive_fleet_pressure = yes }", triggers)
        self.assertIn("alloys = 2200", economy)
        self.assertIn("naval_cap = 1000", economy)
        for marker in (
            "esc_starbase_reactor = {",
            "adv_starbase_defenses = {",
            "reinforced_defenses = {",
            "strategic_defenses = {",
        ):
            self.assertIn(marker, text)
        for marker in (
            "gun_battery = {",
            "missile_battery = {",
            "hangar_bay = {",
            "large_battery = {",
            "armor_module = {",
            "orbital_ring_gun_battery = {",
            "orbital_ring_missile_battery = {",
            "orbital_ring_hangar_bay = {",
            "orbital_ring_large_gun_battery = {",
            "orbital_ring_armor_module = {",
        ):
            self.assertIn(marker, module_text)
        self.assertIn(
            "modifier = { factor = 0 owner = { NOT = { staid_static_defense_investment_ready = yes } } }",
            module_text,
        )
        self.assertIn("modifier = { factor = 4 owner = { staid_static_defense_investment_ready = yes } }", module_text)
        for object_id in ("gun_battery", "missile_battery", "orbital_ring_gun_battery", "orbital_ring_missile_battery"):
            block = extract_top_level_object_text(module_text, object_id)
            depth = 0
            top_level_potentials = 0
            for line in block.splitlines():
                if depth == 1 and re.match(r"^\s*potential\s*=", line):
                    top_level_potentials += 1
                depth += line.count("{") - line.count("}")
            self.assertEqual(top_level_potentials, 1, f"{object_id} should merge duplicate top-level potential blocks")

    def test_threat_response_war_goal_checks_use_block_syntax(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_threat_response_triggers.txt"
        parse_file(trigger_path)
        text = trigger_path.read_text(encoding="utf-8")
        self.assertIn("using_war_goal = { type = wg_conquest owner = root }", text)
        self.assertIn("using_war_goal = { type = wg_subjugation owner = root }", text)
        self.assertIn("using_war_goal = { type = wg_humiliation owner = root }", text)
        self.assertNotIn("using_war_goal = wg_", text)

    def test_threat_response_observer_event_reads_attacker_war_goal_flags(self):
        event_path = MOD_ROOT / "events" / "zzz_staid_threat_response_events.txt"
        parse_file(event_path)
        text = event_path.read_text(encoding="utf-8")
        for marker in (
            "set_timed_country_flag = { flag = staid_tr_war_goal_subjugation",
            "set_timed_country_flag = { flag = staid_tr_war_goal_conquest",
            "set_timed_country_flag = { flag = staid_tr_war_goal_humiliation",
            "limit = { from = { has_country_flag = staid_tr_war_goal_subjugation } }",
            "limit = { from = { has_country_flag = staid_tr_war_goal_conquest } }",
            "limit = { from = { has_country_flag = staid_tr_war_goal_humiliation } }",
        ):
            self.assertIn(marker, text)
        observer_event = text[text.index("id = staid_tr.2") :]
        self.assertNotIn("staid_tr_is_subjugation_war_goal", observer_event)
        self.assertNotIn("staid_tr_is_conquest_war_goal", observer_event)
        self.assertNotIn("staid_tr_is_humiliation_war_goal", observer_event)

    def test_gigas_habitat_zone_slot_compat_districts_cover_new_habitat_route(self):
        district_path = (
            MOD_ROOT / "common" / "districts" / "zzzz_staid_09_gigas_habitat_zone_slot_compat_districts.txt"
        )
        parse_file(district_path)
        text = district_path.read_text(encoding="utf-8")
        expected_slots = {
            "district_giga_hab_city": "slot_habitat_01",
            "district_giga_hab_hive": "slot_habitat_01",
            "district_giga_hab_nexus": "slot_habitat_01",
            "district_giga_hab_science": "slot_habitat_research",
            "district_giga_hab_scavenger": "slot_habitat_minerals",
            "district_giga_orbital_farming": "slot_city_01",
            "district_giga_orbital_sanctuary": "slot_city_government",
            "district_giga_orbital_preserve": "slot_city_01",
            "district_giga_orbital_logistics": "slot_city_government",
        }
        for object_id, slot in expected_slots.items():
            block = text[text.index(f"{object_id} = {{") :]
            block = block[: block.find("\n}\n") + 3]
            self.assertIn("zone_slots = {", block)
            self.assertIn(slot, block)
        self.assertNotIn("is_capped_by_modifier", text)

    def test_route_research_weights_do_not_self_gate_unlock_targets(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        technology_text = technology_path.read_text(encoding="utf-8")
        mega_shipyard_block = technology_text[
            technology_text.index("tech_mega_shipyard = {") : technology_text.index("giga_tech_planet_assembly = {")
        ]
        self.assertIn("# policy_route = mega_shipyard_core", mega_shipyard_block)
        self.assertIn("staid_core_unlock_research_priority_ready = yes", mega_shipyard_block)
        self.assertNotIn("staid_shipyard_expansion_ready = yes", mega_shipyard_block)

    def test_gigas_progression_overrides_cover_deep_unlocks_and_build_gates(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        text = (
            technology_path.read_text(encoding="utf-8")
            + megastructure_path.read_text(encoding="utf-8")
            + trigger_path.read_text(encoding="utf-8")
        )
        for marker in (
            "giga_tech_war_moon_1 = {",
            "giga_tech_war_moon_2 = {",
            "giga_tech_war_system_6 = {",
            "tech_nm_utilization_1 = {",
            "staid_war_moon_research_priority_ready = yes",
            "staid_systemcraft_research_priority_ready = yes",
            "staid_gigas_special_resource_unlock_ready = yes",
            "staid_war_moon_build_priority_ready = yes",
            "staid_systemcraft_build_priority_ready = yes",
            "has_ascension_perk = ap_celestial_printing",
        ):
            self.assertIn(marker, text)

    def test_phase_machine_and_modded_conversion_gates_are_generated(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        parse_file(trigger_path)
        parse_file(economy_path)
        economy = economy_path.read_text(encoding="utf-8")
        text = technology_path.read_text(encoding="utf-8") + trigger_path.read_text(encoding="utf-8") + economy
        for marker in (
            "staid_phase_mega_engineering_rush = {",
            "staid_phase_galactic_wonders_entry = {",
            "staid_phase_gigastructural_constructs_rush = {",
            "staid_phase_planetcraft_rush = {",
            "staid_phase_systemcraft_escalation = {",
            "staid_phase_fleet_conversion_repeatables = {",
            "staid_nsc3_capital_hull_unlock_ready = {",
            "staid_esc_component_unlock_ready = {",
            "staid_advanced_component_resource_support_ready = {",
            "staid_modded_fleet_conversion_ready = {",
            "NOT = { staid_core_deficit_short_runway = yes }",
            "staid_trade_fleet_capacity_safe = yes",
            "resource = sr_dark_matter value > 1",
            "resource = giga_sr_sentient_metal value > 1",
            "staid_nsc3_capital_hull_unlock_ready = yes",
            "staid_esc_component_unlock_ready = yes",
            "NOT = { staid_advanced_component_resource_support_ready = yes }",
            "has_technology = tech_Flagship_1",
            "has_technology = esc_tech_dark_matter_power_core_2",
            'set_name = "Stellar AI Director NSC3 hull readiness reserve"',
        ):
            self.assertIn(marker, text)
        nsc3_hull_block = economy[
            economy.index('set_name = "Stellar AI Director NSC3 hull readiness reserve"') : economy.index(
                'set_name = "Stellar AI Director threat readiness reserve"'
            )
        ]
        for marker in (
            "staid_nsc3_capital_hull_unlock_ready = yes",
            "has_technology = tech_battleships",
            "has_technology = tech_Carrier_1",
            "has_technology = tech_Dreadnought_1",
            "alloys = 900",
            "engineering_research = 900",
            "naval_cap = 1200",
        ):
            self.assertIn(marker, nsc3_hull_block)

    def test_unity_to_research_paths_are_source_backed(self):
        traditions_path = MOD_ROOT / "common" / "traditions" / "zzzz_staid_02_perks_traditions_traditions.txt"
        perks_path = MOD_ROOT / "common" / "ascension_perks" / "zzzz_staid_02_perks_traditions_ascension_perks.txt"
        parse_file(traditions_path)
        parse_file(perks_path)
        traditions_text = traditions_path.read_text(encoding="utf-8")
        perks_text = perks_path.read_text(encoding="utf-8")
        combined = traditions_text + perks_text
        for marker in (
            "# policy_route = research_diplomacy_core; source = common/traditions/00_discovery.txt",
            "tr_discovery_adopt = {",
            "tr_discovery_finish = {",
            "# policy_route = research_diplomacy_core; source = common/traditions/00_diplomacy.txt",
            "tr_diplomacy_finish = {",
            "# policy_route = research_diplomacy_core; source = common/ascension_perks/00_ascension_perks.txt",
            "ap_technological_ascendancy = {",
            "# policy_route = economy_megastructure_core; source = common/ascension_perks/00_ascension_perks.txt",
            "ap_master_builders = {",
            "ap_galactic_wonders = {",
            "ap_gigastructural_constructs = {",
            "modifier = { factor = 0 NOT = { staid_research_diplomacy_priority_ready = yes } }",
            "modifier = { factor = 4 staid_research_diplomacy_priority_ready = yes }",
            "modifier = { factor = 0 NOT = { staid_core_unlock_research_priority_ready = yes } }",
        ):
            self.assertIn(marker, combined)
        reference_rows = collect_generated_reference_rows(MOD_ROOT)
        unresolved = [
            row
            for row in reference_rows
            if row["generated_file"]
            in {
                "common/traditions/zzzz_staid_02_perks_traditions_traditions.txt",
                "common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt",
            }
            and row["reference_name"]
            in {"staid_research_diplomacy_priority_ready", "staid_core_unlock_research_priority_ready"}
            and row["status"] != "ok"
        ]
        self.assertEqual(unresolved, [])
        self.assertNotIn("generic unity hoard", combined.lower())

    def test_fleet_conversion_gates_have_income_pressure_lane(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(trigger_path)
        text = trigger_path.read_text(encoding="utf-8")
        shipyard_block = text[
            text.index("staid_shipyard_payoff_ready = {") : text.index("staid_fleet_buildup_economy_safe = {")
        ]
        fleet_block = text[
            text.index("staid_fleet_buildup_economy_safe = {") : text.index("staid_resource_waste_pressure = {")
        ]
        for block in (shipyard_block, fleet_block):
            self.assertIn("NOT = { staid_catastrophic_collapse_mode = yes }", block)
            self.assertNotIn("staid_survival_mode = yes", block)
            self.assertNotIn("staid_core_deficit_short_runway = yes", block)
        self.assertIn("used_naval_capacity_percent < 1.60", shipyard_block)
        self.assertIn("has_monthly_income = { resource = alloys value > 80 }", shipyard_block)
        self.assertNotIn("staid_militarist_conquest_strategy = yes", shipyard_block)
        self.assertNotIn("staid_raiding_pop_growth_strategy = yes", shipyard_block)
        self.assertIn("used_naval_capacity_percent < 1.85", fleet_block)
        self.assertIn("has_monthly_income = { resource = alloys value > 40 }", fleet_block)
        self.assertIn("has_monthly_income = { resource = energy value > 40 }", fleet_block)
        self.assertNotIn("staid_aggressive_fleet_pressure = yes", fleet_block)
        self.assertNotIn("staid_militarist_conquest_strategy = yes", fleet_block)
        self.assertNotIn("staid_raiding_pop_growth_strategy = yes", fleet_block)
        self.assertNotIn("has_monthly_income = { resource = alloys value > 200 }", shipyard_block)
        self.assertIn("resource_stockpile_compare = { resource = alloys value >", shipyard_block)
        self.assertIn("resource_stockpile_compare = { resource = energy value > 8000 }", fleet_block)

    def test_support_economy_bridge_keeps_resource_bottlenecks_first_class(self):
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        economy_path = MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
        parse_file(trigger_path)
        parse_file(economy_path)
        text = trigger_path.read_text(encoding="utf-8")
        economy = economy_path.read_text(encoding="utf-8")
        basic_block = text[text.index("staid_basic_economy_runway_safe = {") : text.index("staid_trade_capacity_safe = {")]
        advanced_block = text[
            text.index("staid_advanced_component_resource_support_ready = {") : text.index(
                "staid_nsc3_capital_hull_unlock_ready = {"
            )
        ]
        megastructure_block = text[
            text.index("staid_megastructure_prep_ready = {") : text.index("staid_megastructure_commit_safe = {")
        ]
        for marker in (
            "staid_research_input_runway_safe = yes",
            "staid_food_runway_safe = yes",
            "NOT = { has_deficit = minerals }",
            "NOT = { has_deficit = alloys }",
            "has_monthly_income = { resource = minerals value > 100 }",
            "has_monthly_income = { resource = alloys value > 75 }",
        ):
            self.assertIn(marker, basic_block)
        for marker in (
            "NOT = { staid_core_deficit_short_runway = yes }",
            "staid_basic_economy_runway_safe = yes",
            "staid_trade_fleet_capacity_safe = yes",
            "has_monthly_income = { resource = volatile_motes value > 5 }",
            "has_monthly_income = { resource = sr_dark_matter value > 1 }",
            "has_monthly_income = { resource = giga_sr_negative_mass value > 1 }",
            "has_monthly_income = { resource = giga_sr_amb_megaconstruction value > 1 }",
        ):
            self.assertIn(marker, advanced_block)
        esc_resource_block = economy[
            economy.index('set_name = "Stellar AI Director ESC component resource readiness"') : economy.index(
                'set_name = "Stellar AI Director capped stockpile research conversion"'
            )
        ]
        for marker in (
            "NOT = { staid_advanced_component_resource_support_ready = yes }",
            "has_technology = tech_dark_matter_power_core",
            "has_technology = esc_tech_dark_matter_power_core_2",
            "staid_phase_fleet_conversion_repeatables = yes",
            "volatile_motes = 12",
            "exotic_gases = 12",
            "rare_crystals = 12",
            "sr_dark_matter = 3",
            "sr_zro = 3",
            "nanites = 3",
            "engineering_research = 600",
        ):
            self.assertIn(marker, esc_resource_block)
        self.assertIn("staid_trade_planetary_capacity_safe = yes", megastructure_block)
        self.assertNotIn("Stellar AI Director generic trade sell", text)
        self.assertNotIn("Stellar AI Director generic trade buy", text)

    def test_research_infrastructure_overrides_drive_labs_and_habitat_science(self):
        buildings_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_06_research_infrastructure_buildings.txt"
        districts_path = MOD_ROOT / "common" / "districts" / "zzzz_staid_06_research_infrastructure_districts.txt"
        parse_file(buildings_path)
        parse_file(districts_path)
        buildings_text = buildings_path.read_text(encoding="utf-8")
        districts_text = districts_path.read_text(encoding="utf-8")
        for marker in (
            "# policy_route = research_throughput_infrastructure",
            "building_research_lab_1 = {",
            "building_research_lab_2 = {",
            "building_research_lab_3 = {",
            "building_institute = {",
            "building_supercomputer = {",
            "building_archaeostudies_faculty = {",
            "ai_weight_coefficient = 12",
            "additional_ai_weight = 1200",
            "script = stellarai/rare_resource_guard_modifiers",
        ):
            self.assertIn(marker, buildings_text)
        for marker in (
            "# policy_route = crowded_tall_route",
            "district_hab_science = {",
            "ai_weight_coefficient = 4",
            "additional_ai_weight = 500",
        ):
            self.assertIn(marker, districts_text)

    def test_unresolved_source_local_variables_are_reported(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mod_root = Path(temp_dir)
            common = mod_root / "common" / "technology"
            common.mkdir(parents=True)
            (common / "broken.txt").write_text("tech_test = { cost = @missing_cost }\n", encoding="utf-8")
            self.assertEqual(
                generated_unresolved_at_variable_rows(mod_root),
                [
                    {
                        "generated_file": "common/technology/broken.txt",
                        "line": "1",
                        "variable": "@missing_cost",
                    }
                ],
            )

    def test_object_atlas_artifacts_are_static_valid(self):
        self.assertEqual(validate_object_atlas_artifacts(), [])
        for path in (OBJECT_ATLAS_CSV, DEPENDENCY_EDGES_CSV, AI_SUPPORT_MAP_CSV, POLICY_MATRIX_CSV):
            self.assertTrue(path.exists(), f"Missing generated atlas artifact: {path}")

    def test_object_atlas_contains_required_route_objects(self):
        atlas_text = OBJECT_ATLAS_CSV.read_text(encoding="utf-8")
        for marker in (
            "planetcraft",
            "systemcraft",
            "mega_shipyard",
            "esc_tech_dark_matter_power_core_2",
            "building_research_lab_1",
            "district_hab_science",
        ):
            self.assertIn(marker, atlas_text)

    def test_policy_matrix_references_atlas_objects(self):
        with OBJECT_ATLAS_CSV.open("r", encoding="utf-8", newline="") as handle:
            atlas_rows = list(csv.DictReader(handle))
        with POLICY_MATRIX_CSV.open("r", encoding="utf-8", newline="") as handle:
            policy_rows = list(csv.DictReader(handle))
        atlas_ids = {row["object_id"] for row in atlas_rows if row["validation_status"] == "ok"}
        self.assertTrue(policy_rows, "Policy matrix did not contain any rows.")
        missing = sorted({row["object_id"] for row in policy_rows if row["object_id"] not in atlas_ids})
        self.assertEqual(missing, [])

    def test_route_override_surfaces_cover_required_families(self):
        with (RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.csv").open(
            "r", encoding="utf-8", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        covered_routes = {row["route_id"] for row in rows}
        required_routes = {
            "mega_engineering_core",
            "mega_shipyard_core",
            "economy_megastructure_core",
            "early_kilo_economy_core",
            "science_kilo_snowball_core",
            "research_megastructure_core",
            "planetary_computer_research_core",
            "pop_assembly_snowball_core",
            "ring_world_growth_core",
            "storage_cap_core",
            "planetcraft_route",
            "war_moon_route",
            "systemcraft_route",
            "nsc3_capital_hull_route",
            "esc_component_route",
            "crowded_tall_route",
            "conquest_escape_route",
            "apex_site_preservation_core",
            "fallen_empire_benchmark_route",
            "research_throughput_infrastructure",
            "research_diplomacy_core",
        }
        self.assertTrue(required_routes.issubset(covered_routes))
        for row in rows:
            generated_file = Path(row["generated_file"])
            self.assertTrue(generated_file.exists(), f"Missing route override file: {generated_file}")
            self.assertIn(row["object_id"], generated_file.read_text(encoding="utf-8"))
        self.assertTrue((RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.md").exists())

    def test_snowball_checkpoint_routes_cover_research_surface_storage_and_early_kilos(self):
        technology_path = MOD_ROOT / "common" / "technology" / "zzzz_staid_01_unlock_technology_technology.txt"
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        buildings_path = MOD_ROOT / "common" / "buildings" / "zzzz_staid_07_pop_assembly_buildings.txt"
        districts_path = MOD_ROOT / "common" / "districts" / "zzzz_staid_06_research_infrastructure_districts.txt"
        claim_budget_path = MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_08_site_limited_expansion_ai_budget.txt"
        federation_path = MOD_ROOT / "common" / "federation_types" / "zzzz_staid_15_research_diplomacy_federation_types.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(technology_path)
        parse_file(megastructure_path)
        parse_file(buildings_path)
        parse_file(districts_path)
        parse_file(claim_budget_path)
        parse_file(federation_path)
        parse_file(trigger_path)
        text = (
            technology_path.read_text(encoding="utf-8")
            + megastructure_path.read_text(encoding="utf-8")
            + buildings_path.read_text(encoding="utf-8")
            + districts_path.read_text(encoding="utf-8")
            + claim_budget_path.read_text(encoding="utf-8")
            + federation_path.read_text(encoding="utf-8")
            + trigger_path.read_text(encoding="utf-8")
        )
        for marker in (
            "tech_science_nexus = {",
            "tech_ring_world = {",
            "tech_orbital_arc_furnace = {",
            "giga_tech_asteroid_manufactory = {",
            "giga_tech_engineering_test_site = {",
            "giga_tech_macro_scale_weather_manipulation = {",
            "giga_tech_planetary_computer = {",
            "tech_robotic_workers = {",
            "tech_cloning = {",
            "giga_tech_kugelblitz = {",
            "giga_tech_matrioshka_brain_1 = {",
            "giga_tech_neutronium_gigaforge = {",
            "giga_tech_nidavellir = {",
            "giga_tech_interstellar_habitat = {",
            "giga_tech_stellar_ring_habitat = {",
            "think_tank_0 = {",
            "think_tank_3 = {",
            "ring_world_1 = {",
            "ring_world_3_intermediate = {",
            "kugelblitz_0 = {",
            "kugelblitz_3 = {",
            "habitat_central_complex = {",
            "interstellar_habitat_0 = {",
            "stellar_ring_habitat_0 = {",
            "orbital_arc_furnace_1 = {",
            "asteroid_manufactory_0 = {",
            "macro_test_site_0 = {",
            "macro_test_site_3 = {",
            "atmosphere_shredder_0 = {",
            "atmosphere_shredder_3 = {",
            "planetary_computer_0 = {",
            "planetary_computer_1 = {",
            "matrioshka_brain_0_o_star = {",
            "dyson_sphere_0_o_star = {",
            "neutronium_gigaforge_0 = {",
            "nidavellir_forge_0 = {",
            "district_giga_pcc_science = {",
            "building_robot_assembly_plant = {",
            "building_clone_vats = {",
            "building_spawning_pool = {",
            "influence_expenditure_claims = {",
            "influence_expenditure_claims_militarist = {",
            "influence_expenditure_claims_fanatic_militarist = {",
            "research_federation = {",
            "# policy_route = early_kilo_economy_core",
            "# policy_route = science_kilo_snowball_core",
            "# policy_route = research_megastructure_core",
            "# policy_route = planetary_computer_research_core",
            "# policy_route = pop_assembly_snowball_core",
            "# policy_route = ring_world_growth_core",
            "# policy_route = storage_cap_core",
            "# policy_route = apex_site_preservation_core",
            "# policy_route = conquest_escape_route",
            "staid_phase_early_kilo_economy = {",
            "staid_phase_science_kilo_snowball = {",
            "staid_phase_pop_assembly_snowball = {",
            "staid_phase_science_nexus_rush = {",
            "staid_phase_planetary_computer_research = {",
            "staid_phase_ring_world_growth = {",
            "staid_phase_storage_cap_expansion = {",
            "staid_phase_boxed_tall_habitat_escape = {",
            "staid_site_limited_expansion_ready = {",
            "staid_apex_site_preservation_ready = {",
            "staid_science_nexus_build_priority_ready = yes",
            "staid_science_kilo_build_priority_ready = yes",
            "staid_planetary_computer_build_priority_ready = yes",
            "staid_pop_assembly_snowball_ready = yes",
            "staid_ring_world_build_priority_ready = yes",
            "staid_storage_cap_build_priority_ready = yes",
            "staid_early_kilo_economy_build_priority_ready = yes",
            "staid_apex_site_preservation_ready = yes",
            "staid_research_diplomacy_priority_ready = {",
        ):
            self.assertIn(marker, text)

    def test_research_federation_weight_is_generated_without_unsafe_diplomacy_overrides(self):
        federation_path = MOD_ROOT / "common" / "federation_types" / "zzzz_staid_15_research_diplomacy_federation_types.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        policy_path = MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt"
        traditions_path = MOD_ROOT / "common" / "traditions" / "zzzz_staid_02_perks_traditions_traditions.txt"
        ascension_path = MOD_ROOT / "common" / "ascension_perks" / "zzzz_staid_02_perks_traditions_ascension_perks.txt"
        parse_file(federation_path)
        parse_file(trigger_path)
        parse_file(policy_path)
        parse_file(traditions_path)
        parse_file(ascension_path)

        text = federation_path.read_text(encoding="utf-8")
        trigger_text = trigger_path.read_text(encoding="utf-8")
        policy_text = policy_path.read_text(encoding="utf-8")
        traditions_text = traditions_path.read_text(encoding="utf-8")
        ascension_text = ascension_path.read_text(encoding="utf-8")
        generated_common_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((MOD_ROOT / "common").rglob("*.txt"))
        )
        research_federation = extract_top_level_object_text(text, "research_federation")

        self.assertIn("# policy_route = research_diplomacy_core", text)
        self.assertIn("host_has_dlc = Federations", research_federation)
        self.assertIn("research_federation_passive", research_federation)
        self.assertIn("ai_weight = {", research_federation)
        self.assertIn("staid_research_diplomacy_core", research_federation)
        self.assertIn("from = { staid_research_diplomacy_priority_ready = yes }", research_federation)
        self.assertIn("has_active_tradition = tr_discovery_federations_finish", research_federation)
        self.assertIn("staid_research_diplomacy_priority_ready = {", trigger_text)
        self.assertIn("diplo_stance_cooperative", policy_text)
        self.assertIn("tr_discovery_federations_finish", traditions_text)
        self.assertIn("tr_diplomacy_finish", traditions_text)
        self.assertIn("ap_technological_ascendancy", ascension_text)
        self.assertIn("staid_research_diplomacy_priority_ready = yes", generated_common_text)
        self.assertNotIn("action_form_research_agreement", generated_common_text)

        self.assertFalse((MOD_ROOT / "common" / "diplomatic_actions").exists())
        self.assertFalse((MOD_ROOT / "common" / "personalities").exists())

    def test_megastructure_upgrade_stages_are_prioritized_over_new_starts(self):
        megastructure_path = MOD_ROOT / "common" / "megastructures" / "zzzz_staid_03_megastructures_megastructures.txt"
        trigger_path = MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
        parse_file(megastructure_path)
        parse_file(trigger_path)

        text = megastructure_path.read_text(encoding="utf-8")
        trigger_text = trigger_path.read_text(encoding="utf-8")
        self.assertIn("staid_megastructure_continuation_priority_ready = {", trigger_text)
        self.assertIn("staid_unfinished_kugelblitz_exists = {", trigger_text)
        self.assertIn("any_owned_megastructure = {", trigger_text)
        for unfinished_stage in ("kugelblitz_0", "kugelblitz_1", "kugelblitz_2", "kugelblitz_restored"):
            self.assertIn(f"is_megastructure_type = {unfinished_stage}", trigger_text)
        self.assertIn("staid_kugelblitz_new_start_budget_ready = {", trigger_text)
        self.assertIn("NOT = { staid_unfinished_kugelblitz_exists = yes }", trigger_text)
        self.assertIn("NOT = { check_variable = { which = giga_current_kugel value >= 10 } }", trigger_text)

        starter = extract_top_level_object_text(text, "kugelblitz_0")
        first_upgrade = extract_top_level_object_text(text, "kugelblitz_1")
        final_upgrade = extract_top_level_object_text(text, "kugelblitz_3")

        self.assertNotIn("megastructure_continuation_priority = finish_existing_before_new_start", starter)
        self.assertIn("kugelblitz_start_budget = empty_silos_are_capped_storage_not_income", starter)
        self.assertIn("modifier = { factor = 0 from = { check_variable = { which = giga_current_kugel value >= 10 } } }", starter)
        self.assertIn("modifier = { factor = 0 from = { has_country_flag = is_currently_building_kugelblitz } }", starter)
        self.assertIn("modifier = { factor = 0 from = { staid_unfinished_kugelblitz_exists = yes } }", starter)
        self.assertIn("modifier = { factor = 0.02 from = { check_variable = { which = giga_current_kugel value >= 9 } } }", starter)
        for block in (first_upgrade, final_upgrade):
            self.assertIn("upgrade_from = {", block)
            self.assertIn("megastructure_continuation_priority = finish_existing_before_new_start", block)
            self.assertIn("staid_megastructure_continuation_priority_ready = yes", block)
            self.assertIn("modifier = { factor = 35 from = { staid_megastructure_continuation_priority_ready = yes } }", block)
            self.assertNotIn("kugelblitz_start_budget = empty_silos_are_capped_storage_not_income", block)


if __name__ == "__main__":
    unittest.main()
