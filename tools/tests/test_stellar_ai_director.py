import unittest
from pathlib import Path
import sys
import csv
import json
import os
import runpy
import tempfile
import zipfile
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_active_playset_snapshot
import build_ai_roi_matrix
import add_stellar_ai_director_to_irony_collection
import build_stellar_ai_director_dependency_audit
import build_stellar_ai_director_irony_order_proof
import build_stellar_ai_director_file_audit
import build_stellar_ai_director_integration_policy_audit
import build_stellar_ai_director_roi_quality_audit
import build_stellar_ai_director_reference_audit
import build_stellar_ai_director_plan_status
import build_stellar_ai_director_launch_comparison
import build_stellar_ai_director_observer_save_summary
import disable_stellar_ai_director_in_dlc_load
import enable_stellar_ai_director_in_dlc_load
import generate_stellar_ai_director_patch
import install_stellar_ai_director_launcher_descriptor
import record_stellar_ai_director_main_menu_proof
import validate_stellar_ai_director_patch
import build_mod_snapshot_inventory
import stellar_ai_director_lib as staid
from stellar_ai_director_lib import (
    EmpireState,
    MarketPrice,
    PDXAtom,
    PDXBlock,
    PDXParseError,
    ai_budget_text,
    append_director_to_selected_irony_collection,
    atom_value,
    block_assignments,
    block_atoms,
    block_contains_assignment,
    choose_decision_state,
    classify_director_log_line,
    classify_data_quality,
    classify_priority,
    classify_plan_phase_status,
    collect_load_proof_contract,
    collect_launcher_installation_state,
    collect_generated_conflict_rows,
    collect_dependency_audit_rows,
    collect_generated_file_audit_rows,
    collect_integration_policy_audit_rows,
    collect_integration_surface_rows,
    collect_launch_comparison_evidence,
    collect_launch_validation_evidence,
    collect_director_log_summary,
    collect_launch_log_file_state,
    collect_main_menu_proof_marker,
    collect_irony_order_proof,
    collect_market_prices,
    collect_megastructure_features,
    collect_observer_save_summary,
    collect_plan_completion_status,
    collect_roi_quality_rows,
    collect_generated_reference_rows,
    collect_variables,
    compact_resource_map,
    compare_irony_order_with_director,
    core_deficit_with_short_runway,
    descriptor_text,
    dependency_audit_report_text,
    dependency_status,
    descriptor_dependencies,
    director_build_gate,
    director_strategy_role,
    director_surplus_sink_priority,
    director_surplus_sink_role,
    director_weight_basis,
    economic_plan_text,
    disable_director_in_dlc_load,
    enable_director_in_dlc_load,
    eval_macro_expression,
    expand_inline_script,
    extract_megastructure_rows,
    extract_completion_checklist_items,
    extract_assignment_block,
    generate_conflict_classification_artifacts,
    generate_dependency_audit_artifacts,
    generate_file_audit_artifacts,
    generate_integration_surface_artifacts,
    generate_integration_policy_audit_artifacts,
    generate_irony_order_proof_artifacts,
    generate_launch_comparison_artifacts,
    generate_launch_validation_artifacts,
    generate_observer_save_summary_artifacts,
    generate_plan_status_artifacts,
    generate_reference_audit_artifacts,
    generate_roi_quality_audit_artifacts,
    generated_thresholds,
    generated_conflict_report_text,
    generated_file_audit_report_text,
    generated_file_path_status,
    generated_reference_report_text,
    generated_top_level_objects,
    gigas_resource_budget_text,
    implementation_notes_text,
    integration_policy_recommendation,
    integration_policy_audit_report_text,
    integration_policy_audit_status,
    integration_policy_priority_band,
    integration_surface_report_text,
    iter_numbered_child_blocks,
    irony_conflict_scan_artifact_passes,
    irony_order_proof_artifact_passes,
    irony_order_proof_report_text,
    launch_comparison_artifact_passes,
    launch_comparison_report_text,
    load_order_note_text,
    launch_validation_report_text,
    load_stellaris_save_gamestate,
    inline_bool_value,
    inline_float_value,
    inline_script_params,
    inline_script_value,
    install_launcher_descriptor,
    is_decision_eligible,
    launcher_descriptor_path,
    launcher_descriptor_text,
    market_resource_value,
    market_price_rows,
    mega_giga_policy_artifact_passes,
    merge_main_menu_proof_marker,
    merge_resource_maps,
    munch_preflight_artifact_passes,
    conflicts_note_text,
    nsc3_esc_policy_artifact_passes,
    normalize_macro_expressions,
    numeric_or_zero,
    parse_pdx,
    parse_file,
    parse_numeric,
    percentile,
    planetary_capacity_policy_artifact_passes,
    plan_completion_report_text,
    plan_phase_artifact_rows,
    priority_rank,
    read_text,
    read_main_menu_proof_status,
    readme_text,
    observer_save_summary_report_text,
    record_main_menu_proof_marker,
    resolve_inline_script_path,
    roi_quality_audit_report_text,
    roi_quality_status,
    resource_block_to_dict,
    roi_model_artifact_passes,
    round_to,
    safe_mod_id,
    script_values_text,
    serialize_pdx_value,
    set_director_enabled_in_dlc_load,
    shipyard_strategic_values,
    shipyard_policy_artifact_passes,
    sortable_payback,
    source_corpus_artifact_passes,
    starbase_policy_artifact_passes,
    stockpile_runway_months,
    strip_comments,
    substitute_inline_params,
    surplus_sink_pressure,
    trade_capacity_pressure,
    decision_tree_artifact_passes,
    documentation_artifact_passes,
    generated_surface_artifact_passes,
    tokenize,
    triggers_text,
    tuning_notes_text,
    unresolved_template_placeholder_count,
    observer_test_log_text,
    unlock_priority_policy_artifact_passes,
    unresolved_symbols,
    validator_artifact_passes,
    validate_generated_patch,
    weighted_resource_value,
    write_csv,
    write_json,
    write_text_file,
)


class PDXParserTests(unittest.TestCase):
    def test_nested_blocks_and_inline_resources(self):
        parsed = parse_pdx('mega = { cost = { alloys = 1000 energy = @energy_cost } ai_weight = { weight = 5 } }')
        self.assertEqual(len(parsed.items), 1)

    def test_comments_are_ignored(self):
        parsed = parse_pdx('# ignored = { broken\nreal = { value = 1 # inline comment\n }')
        self.assertEqual(parsed.items[0].key, "real")

    def test_variables_are_preserved_symbolically(self):
        parsed = parse_pdx("@cost = 100\nthing = { cost = { alloys = @cost } }")
        self.assertEqual(parsed.items[0].key, "@cost")

    def test_malformed_braces_fail_clearly(self):
        with self.assertRaises(PDXParseError):
            parse_pdx("thing = { cost = { alloys = 1 }")

    def test_missing_value_after_assignment_fails_clearly(self):
        with self.assertRaises(PDXParseError):
            parse_pdx("thing =")

    def test_unexpected_closing_brace_fails_clearly(self):
        with self.assertRaises(PDXParseError):
            parse_pdx("thing = }")
        with self.assertRaises(PDXParseError):
            parse_pdx("}")

    def test_top_level_atom_is_preserved_for_loose_tokens(self):
        parsed = parse_pdx("loose_token")
        self.assertEqual(parsed.items[0].value, "loose_token")

    def test_parse_file_reports_source_path_on_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.txt"
            path.write_text("thing = {", encoding="utf-8")
            with self.assertRaisesRegex(PDXParseError, "broken.txt"):
                parse_file(path)

    def test_read_text_falls_back_to_cp1252(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "encoded.txt"
            path.write_bytes("name = caf\xe9".encode("cp1252"))
            self.assertIn("café", read_text(path))

    def test_strip_comments_preserves_hash_inside_quotes(self):
        text = strip_comments('name = "value # kept" # removed')
        self.assertIn('"value # kept"', text)
        self.assertNotIn("removed", text)

    def test_tokenize_preserves_comparators_and_atoms(self):
        self.assertEqual(tokenize("value >= 5 other < 9"), ["value", ">=", "5", "other", "<", "9"])

    def test_block_helpers_walk_nested_assignments(self):
        parsed = parse_pdx("outer = { inner = { token = yes list = { a b } } }")
        outer = block_assignments(parsed, "outer")[0].value
        self.assertIsInstance(outer, PDXBlock)
        self.assertEqual(atom_value(block_assignments(outer, "missing")[0].value) if block_assignments(outer, "missing") else None, None)
        self.assertIn("a", block_atoms(block_assignments(block_assignments(outer, "inner")[0].value, "list")[0].value))
        self.assertTrue(block_contains_assignment(outer, "token", "yes"))
        self.assertEqual([item.key for item in block_assignments(parsed)], ["outer"])


class ResourceHelperTests(unittest.TestCase):
    def test_market_price_properties_cover_fee_and_bounds(self):
        price = MarketPrice("alloys", 100, 400, True)
        self.assertEqual(price.base_energy, 4)
        self.assertAlmostEqual(price.min_sell_energy, 0.8)
        self.assertEqual(price.max_buy_energy, 20)
        self.assertEqual(price.default_fee_base_buy_energy, 5.2)
        self.assertAlmostEqual(price.default_fee_floor_sell_energy, 0.56)
        self.assertEqual(price.default_fee_ceiling_buy_energy, 26)

    def test_collect_market_prices_skips_missing_bad_and_non_block_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            strategic = root / "common" / "strategic_resources"
            strategic.mkdir(parents=True)
            (strategic / "bad.txt").write_text("broken = {", encoding="utf-8")
            (strategic / "scalar.txt").write_text("not_a_block = yes", encoding="utf-8")
            (strategic / "good.txt").write_text(
                "test_resource = { tradable = yes market_amount = 10 market_price = 20 }",
                encoding="utf-8",
            )
            prices = collect_market_prices([root], vanilla_common_root=root / "missing-common")
            self.assertEqual(prices["test_resource"].base_energy, 2)
            common = root / "common"
            prices_from_common = collect_market_prices([common], vanilla_common_root=common)
            self.assertIn("test_resource", prices_from_common)

    def test_collect_variables_ignores_comments_and_non_numbers(self):
        self.assertEqual(collect_variables("@a = 12\n# @b = 99\n@c = text"), {"@a": 12.0})

    def test_macro_expressions_evaluate_safe_math_only(self):
        variables = {"@base": 100.0, "@mult": 2.0}
        self.assertEqual(eval_macro_expression("@[base * mult + 50]", variables), 250.0)
        self.assertIsNone(eval_macro_expression("@[__import__('os')]", variables))
        self.assertIsNone(eval_macro_expression("@[1 / 0]", variables))
        self.assertEqual(normalize_macro_expressions("cost = @[base * mult]", variables), "cost = 200")

    def test_resource_block_to_dict_handles_multiplier_and_negative_sentinel(self):
        block = parse_pdx('cost = { multiplier = "RESOURCE|alloys|AMOUNT|250|" alloys = -1 energy = @e }').items[0].value
        self.assertEqual(resource_block_to_dict(block, {"@e": 50.0}), {"alloys": 250.0, "energy": 50.0})

    def test_parse_numeric_paths(self):
        self.assertEqual(parse_numeric("@cost", {"@cost": 42.0}), 42.0)
        self.assertEqual(parse_numeric("@[cost * 2]", {"@cost": 42.0}), 84.0)
        self.assertEqual(parse_numeric("not_numeric"), "not_numeric")
        self.assertEqual(parse_numeric(None), 0.0)
        self.assertEqual(numeric_or_zero("symbolic"), 0.0)

    def test_inline_value_helpers(self):
        block = parse_pdx("root = { amount = 2.5 enabled = yes disabled = no }").items[0].value
        self.assertEqual(inline_float_value(block, "amount"), 2.5)
        self.assertTrue(inline_bool_value(block, "enabled"))
        self.assertFalse(inline_bool_value(block, "disabled"))
        self.assertIsNone(inline_bool_value(block, "missing"))

    def test_weighted_and_market_values_preserve_unpriced_resources(self):
        resources = {"alloys": 10.0, "energy": 20.0, "trade": 12.0, "unknown": 3.0}
        self.assertEqual(weighted_resource_value(resources), 15.0)
        self.assertEqual(market_resource_value({"alloys": 0.0}, {"alloys": MarketPrice("alloys", 100, 400, True)}, "base_buy"), (0.0, {}))
        total, unpriced = market_resource_value(resources, {"alloys": MarketPrice("alloys", 100, 400, True)}, "fee_base_buy")
        self.assertEqual(total, 72.0)
        self.assertEqual(unpriced, {"trade": 12.0, "unknown": 3.0})
        fee_sell_total, _ = market_resource_value({"alloys": 10.0}, {"alloys": MarketPrice("alloys", 100, 400, True)}, "fee_min_sell")
        self.assertAlmostEqual(fee_sell_total, 5.6)
        with self.assertRaises(ValueError):
            market_resource_value({"alloys": 1.0}, {"alloys": MarketPrice("alloys", 100, 400, True)}, "bad_mode")

    def test_shipyard_values_and_resource_maps(self):
        prices = {"alloys": MarketPrice("alloys", 100, 400, True)}
        values = shipyard_strategic_values(10, 0.5, prices)
        self.assertEqual(values["strategic_shipyard_effective_slots"], 15)
        self.assertEqual(values["strategic_shipyard_annual_alloy_throughput"], 6750)
        self.assertEqual(shipyard_strategic_values(0, 0, prices)["strategic_shipyard_effective_slots"], 0)
        target = {"alloys": 10.0, "energy": "symbol"}
        merge_resource_maps(target, {"alloys": 30.0, "energy": 5.0})
        self.assertEqual(target, {"alloys": 30.0, "energy": 5.0})
        self.assertEqual(unresolved_symbols({"a": "@x", "b": "$param$", "c": 1.0}), {"@x", "$param$"})
        self.assertFalse(block_contains_assignment(PDXAtom("nope"), "token", "yes"))

    def test_inline_script_expansion_and_serialization(self):
        with tempfile.TemporaryDirectory() as tmp:
            inline_root = Path(tmp)
            (inline_root / "outer.txt").write_text(
                "inline_script = { script = inner value = $amount$ }", encoding="utf-8"
            )
            (inline_root / "inner.txt").write_text("cost = { alloys = $value$ }", encoding="utf-8")
            block = parse_pdx("inline_script = { script = outer amount = 75 }").items[0].value
            self.assertEqual(inline_script_value(block, "script"), "outer")
            self.assertEqual(inline_script_params(block), {"amount": "75"})
            self.assertEqual(substitute_inline_params("alloys = $amount$ missing = $none$", {"amount": "75"}), "alloys = 75 missing = ")
            self.assertEqual(resolve_inline_script_path(inline_root, "outer"), inline_root / "outer.txt")
            expanded = expand_inline_script(block, {}, inline_root)
            self.assertIsInstance(expanded, PDXBlock)
            self.assertIn("cost =", serialize_pdx_value(expanded))
            self.assertEqual(serialize_pdx_value(PDXAtom("token")), "token")
            self.assertEqual(serialize_pdx_value(PDXBlock([PDXAtom("token")])), "{ token }")
            self.assertIsNone(expand_inline_script(parse_pdx("inline_script = { script = missing }").items[0].value, {}, inline_root))
            self.assertIsNone(expand_inline_script(PDXBlock(), {}, inline_root))
            self.assertIsNone(expand_inline_script(block, {}, inline_root, depth=9))
            (inline_root / "bad.txt").write_text("broken = {", encoding="utf-8")
            self.assertIsNone(expand_inline_script(parse_pdx("inline_script = { script = bad }").items[0].value, {}, inline_root))

    def test_inline_params_serialize_block_values(self):
        block = parse_pdx("inline_script = { script = sample nested = { alloys = 5 } }").items[0].value
        self.assertEqual(inline_script_params(block)["nested"], "{ alloys = 5 }")

    def test_feature_collection_and_quality_classification(self):
        with tempfile.TemporaryDirectory() as tmp:
            inline_root = Path(tmp)
            (inline_root / "bonus.txt").write_text("produces = { physics_research = 25 } ai_weight = { weight = 1 }", encoding="utf-8")
            block = parse_pdx(
                "mega = { cost = { alloys = 100 } upkeep = { energy = 5 } "
                "station_modifier = { starbase_shipyard_capacity_add = 2 } "
                "prerequisites = { tech_a } upgrade_from = { old_mega } "
                "inline_script = { script = bonus } }"
            ).items[0].value
            features = collect_megastructure_features(block, {}, inline_root)
            self.assertEqual(features["cost"], {"alloys": 100.0})
            self.assertEqual(features["produces"], {"physics_research": 25.0})
            self.assertEqual(features["modifiers"], {"starbase_shipyard_capacity_add": 2.0})
            self.assertEqual(features["prereqs"], ["tech_a"])
            self.assertEqual(features["upgrade_from"], ["old_mega"])
            self.assertTrue(features["has_ai_weight"])
            self.assertEqual(classify_data_quality({}, {}, {}, ["missing"], []), "template_wrapper_no_direct_resources")
            self.assertEqual(classify_data_quality({}, {}, {}, [], []), "no_resource_effect")
            self.assertEqual(classify_data_quality({"alloys": "@x"}, {}, {}, [], ["@x"]), "symbolic_unresolved")
            self.assertEqual(compact_resource_map({"alloys": 1.0, "token": "x"}), "alloys=1;token=x")
            self.assertEqual(collect_megastructure_features(PDXAtom("nope"), {}, inline_root)["cost"], {})
            bio_cost = parse_pdx("mega = { cost = { country_uses_bio_ships = yes alloys = 999 } }").items[0].value
            self.assertEqual(collect_megastructure_features(bio_cost, {}, inline_root)["cost"], {})
            missing_inline = parse_pdx("mega = { inline_script = { script = missing } }").items[0].value
            self.assertEqual(collect_megastructure_features(missing_inline, {}, inline_root)["inline_scripts"], ["missing"])


class StrategyClassificationTests(unittest.TestCase):
    def test_director_roles_gates_basis_and_sink_priorities(self):
        self.assertEqual(director_strategy_role("mega_shipyard_3", 20, 0, True), "fleet_production_sink")
        self.assertEqual(director_strategy_role("dyson_sphere_5", 0, 1000, True), "economy_multiplier")
        self.assertEqual(director_strategy_role("matrioshka_brain_1", 0, 1000, True), "research_multiplier")
        self.assertEqual(director_strategy_role("minor_project", 0, 1000, True), "resource_or_modifier_project")
        self.assertEqual(director_strategy_role("minor_project", 0, 0, True), "infrastructure_project")
        self.assertEqual(director_strategy_role("broken_project", 0, 0, False), "audit_only")
        self.assertEqual(director_build_gate("unknown"), "requires_manual_policy_review")
        self.assertEqual(director_weight_basis("fleet_production_sink"), "strategic_shipyard_throughput")
        self.assertEqual(director_weight_basis("unknown"), "unmodeled_infrastructure_value")
        self.assertEqual(director_surplus_sink_role("matrioshka", 0, {}, True), "research_sink")
        self.assertEqual(director_surplus_sink_role("shipyard", 0, {}, True), "fleet_sink")
        self.assertEqual(director_surplus_sink_role("unity_project", 0, {"unity": 5.0}, True), "unity_sink")
        self.assertEqual(director_surplus_sink_role("audit", 0, {}, False), "not_surplus_sink")
        self.assertEqual(director_surplus_sink_priority("unity_sink"), 3)
        self.assertEqual(director_surplus_sink_priority("none"), "")

    def test_priority_sorting_threshold_helpers_and_eligibility(self):
        self.assertEqual(classify_priority("shipyard", 10001, "", True), "shipyard_multiplier")
        self.assertEqual(classify_priority("dyson", 1, "", True), "economy_multiplier")
        self.assertEqual(classify_priority("matrioshka", 1, "", True), "research_multiplier")
        self.assertEqual(classify_priority("fast", 1, 9.9, True), "high_roi")
        self.assertEqual(classify_priority("blocked", 100, 1.0, False), "observe_only")
        self.assertEqual(priority_rank("missing"), 99)
        self.assertEqual(sortable_payback({"priority_tier": "shipyard_multiplier", "strategic_shipyard_payback_years": 2}), 2)
        self.assertEqual(sortable_payback({"market_deficit_payback_years": 3}), 3)
        self.assertEqual(sortable_payback({}), 9999.0)
        self.assertEqual(percentile([], 0.5), 0.0)
        self.assertEqual(percentile([1, 10, 100], 0.5), 10)
        self.assertEqual(round_to(11, 10), 20)
        self.assertEqual(round_to(11, 0), 11)
        self.assertFalse(is_decision_eligible("ruined_thing", {"alloys": 1.0}, 0, "resolved"))
        self.assertFalse(is_decision_eligible("thing", {"alloys": 1.0}, 0, "symbolic_unresolved"))
        self.assertTrue(is_decision_eligible("thing", {}, 1, "resolved"))

    def test_decision_state_helper_edges(self):
        stable = EmpireState(incomes={"energy": 1}, stockpiles={"energy": 0})
        deficit = EmpireState(incomes={"energy": -10}, stockpiles={"energy": 100})
        surplus = EmpireState(incomes={"alloys": 300, "energy": 300}, stockpiles={"alloys": 20000})
        self.assertEqual(stockpile_runway_months(stable, "energy"), float("inf"))
        self.assertEqual(stockpile_runway_months(deficit, "energy"), 10)
        self.assertTrue(core_deficit_with_short_runway(deficit))
        self.assertFalse(core_deficit_with_short_runway(stable))
        self.assertTrue(surplus_sink_pressure(surplus))
        self.assertFalse(surplus_sink_pressure(deficit))
        trade_deficit = EmpireState(incomes={"trade": -20}, stockpiles={"trade": 200})
        self.assertTrue(trade_capacity_pressure(trade_deficit))
        self.assertTrue(core_deficit_with_short_runway(trade_deficit))
        self.assertEqual(choose_decision_state(trade_deficit), "survival_mode")
        self.assertFalse(
            surplus_sink_pressure(
                EmpireState(incomes={"alloys": 400, "energy": 400, "trade": 40}, stockpiles={"alloys": 30000})
            )
        )
        self.assertFalse(surplus_sink_pressure(EmpireState(incomes={"alloys": 300, "energy": -1}, stockpiles={"alloys": 30000, "energy": 99999})))
        self.assertEqual(choose_decision_state(EmpireState(recently_lost_war=True)), "recovery_mode")
        self.assertEqual(
            choose_decision_state(EmpireState(at_war=True, used_naval_capacity_percent=0.8, incomes={"alloys": 400, "energy": 400}, stockpiles={"alloys": 30000}, wants_fleet_buildup=True)),
            "recovery_mode",
        )
        self.assertEqual(
            choose_decision_state(EmpireState(at_war=True, used_naval_capacity_percent=0.9, incomes={"alloys": 350, "energy": 350}, stockpiles={"alloys": 25000}, shipyard_capacity_bottleneck=True, wants_fleet_buildup=True)),
            "shipyard_expansion_mode",
        )
        self.assertEqual(
            choose_decision_state(
                EmpireState(
                    at_war=True,
                    used_naval_capacity_percent=0.9,
                    incomes={"alloys": 350, "energy": 350, "trade": 10},
                    stockpiles={"alloys": 25000, "trade": 10000},
                    shipyard_capacity_bottleneck=True,
                    wants_fleet_buildup=True,
                )
            ),
            "survival_mode",
        )
        self.assertEqual(
            choose_decision_state(EmpireState(has_megastructure_prereqs=True, highest_threat=60, used_naval_capacity_percent=0.8, incomes={"alloys": 200}, stockpiles={"alloys": 20000})),
            "normal_growth_mode",
        )


class GeneratedTextAndWriterTests(unittest.TestCase):
    def setUp(self):
        self.thresholds = {
            "prep_stockpile_alloys": 16000,
            "prep_income_alloys": 140,
            "commit_stockpile_alloys": 30000,
            "desired_base_alloys": 26000,
            "desired_mega_engineering_add": 52000,
            "desired_prep_add": 76000,
            "desired_commit_add": 110000,
            "shipyard_stockpile_alloys": 12000,
            "shipyard_income_alloys": 160,
            "eligible_roi_rows": 125,
        }
        self.playset = {
            "collection_name": "Test Collection",
            "patch_mod_enabled": False,
            "mod_count": 2,
            "required_mods": {
                "1": {"name": "Present", "present": True, "load_position": 1},
                "2": {"name": "Missing", "present": False, "load_position": None},
            },
        }

    def test_generated_descriptor_and_pdx_text_contains_required_contracts(self):
        self.assertIn('supported_version="v4.4.*"', descriptor_text())
        triggers = triggers_text(self.thresholds)
        self.assertIn("value > 16000", triggers)
        self.assertIn("value > 140", triggers)
        self.assertIn("staid_static_defense_investment_ready", triggers)
        self.assertIn("staid_aggressive_fleet_pressure = yes", triggers)
        self.assertIn("highest_threat > 50", triggers)
        self.assertIn("staid_fleet_buildup_economy_safe", triggers)
        self.assertIn("used_naval_capacity_percent < 1.05", triggers)
        self.assertIn("staid_fleet_payoff_exploitation_ready", triggers)
        self.assertIn("staid_planetary_capacity_growth_ready", triggers)
        self.assertIn("has_deficit = trade", triggers)
        self.assertIn("staid_trade_capacity_safe", triggers)
        self.assertIn("staid_trade_fleet_capacity_safe = yes", triggers)
        self.assertIn("has_monthly_income = { resource = trade value > 75 }", triggers)
        self.assertIn("resource_stockpile_compare = { resource = minerals value > 5000 }", triggers)
        self.assertIn("staid_core_unlock_research_priority_ready", triggers)
        self.assertIn("has_technology = tech_mega_engineering", triggers)
        self.assertIn("has_technology = tech_mega_shipyard", triggers)
        self.assertEqual(parse_pdx(triggers).items[0].key, "staid_core_deficit_short_runway")
        budget = ai_budget_text(self.thresholds)
        self.assertIn("Full-object override", budget)
        self.assertIn("base = 26000", budget)
        self.assertEqual(parse_pdx(budget).items[0].key, "alloys_expenditure_megastructures")
        gigas_budget = gigas_resource_budget_text()
        parsed_gigas_budget = parse_pdx(gigas_budget)
        self.assertEqual(
            [assignment.key for assignment in block_assignments(parsed_gigas_budget)],
            [
                "sentient_metal_expenditure_megastructures",
                "negative_mass_expenditure_megastructures",
                "supertensiles_upkeep_megastructures",
            ],
        )
        self.assertIn("giga_sr_sentient_metal", gigas_budget)
        self.assertIn("giga_sr_negative_mass", gigas_budget)
        self.assertIn("giga_sr_amb_megaconstruction", gigas_budget)
        economy = economic_plan_text()
        self.assertIn("giga_sr_sentient_metal", economy)
        self.assertIn("Stellar AI Director trade capacity reserve", economy)
        self.assertIn("Stellar AI Director trade deficit recovery", economy)
        self.assertIn("trade = 150", economy)
        self.assertIn("Stellar AI Director defensive starbase reserve", economy)
        self.assertIn("staid_static_defense_investment_ready = yes", economy)
        self.assertIn("Stellar AI Director crisis starbase reserve", economy)
        self.assertIn("staid_crisis_starbase_pressure = yes", economy)
        self.assertIn("Stellar AI Director fleet throughput reserve", economy)
        self.assertIn("staid_shipyard_expansion_ready = yes", economy)
        self.assertIn("trade = 75", economy)
        self.assertIn("staid_fleet_payoff_exploitation_ready = yes", economy)
        self.assertIn("naval_cap = 200", economy)
        self.assertIn("Stellar AI Director planetary capacity reserve", economy)
        self.assertIn("staid_planetary_capacity_growth_ready = yes", economy)
        self.assertIn("trade = 50", economy)
        self.assertIn("pops = 250000", economy)
        self.assertNotIn("empire_size =", economy)
        self.assertIn("Stellar AI Director modded unlock research reserve", economy)
        self.assertIn("staid_core_unlock_research_priority_ready = yes", economy)
        self.assertIn("engineering_research = 160", economy)
        self.assertEqual(parse_pdx(economy).items[0].key, "basic_economy_plan")
        values = script_values_text(self.thresholds)
        self.assertIn("staid_roi_matrix_eligible_rows = 125", values)

    def test_generated_docs_describe_missing_mods_and_thresholds(self):
        readme = readme_text(self.playset)
        self.assertIn("Missing", readme)
        self.assertIn("Test Collection", readme)
        self.assertIn("Load Order", readme)
        self.assertIn("Stellar AI Director Loaded", readme)
        notes = implementation_notes_text(self.playset, self.thresholds)
        self.assertIn("Required Parent Detection", notes)
        self.assertIn("zzz_staid_gigas_resource_budgets.txt", notes)
        self.assertIn("| eligible_roi_rows | 125 |", notes)
        load_order = load_order_note_text(self.playset)
        self.assertIn("Required parent maximum load position: 1", load_order)
        self.assertIn("Stellar AI", load_order)
        self.assertIn("sentient_metal_expenditure_megastructures", load_order)
        conflicts = conflicts_note_text()
        self.assertIn("alloys_expenditure_megastructures", conflicts)
        self.assertIn("negative_mass_expenditure_megastructures", conflicts)
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(staid, "OBSERVER_SMOKE_SAVE_SUMMARY_JSON", Path(tmp) / "missing-summary.json"):
                self.assertIn("not run yet", observer_test_log_text(self.playset))
        tuning = tuning_notes_text(self.thresholds)
        self.assertIn("| eligible ROI rows | 125 |", tuning)
        self.assertIn("Trade-Capacity Policy", tuning)
        self.assertIn("trade logistics", tuning)
        self.assertIn("do not emit `empire_size`", tuning)
        self.assertIn("Re-run generator", tuning)

    def test_observer_log_retains_save_summary_as_historical_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary_json = Path(tmp) / "summary.json"
            summary_md = Path(tmp) / "summary.md"
            summary_json.write_text(
                json.dumps(
                    {
                        "initialized_country_count": 2,
                        "mod_count": 4,
                        "date": "2202.01.01",
                        "required_mods_present": {"Stellar AI Director": True},
                        "short_smoke_passes": True,
                        "player_metrics": {"economy_power": 540.2},
                        "player_monthly_income": {"energy": 25.0},
                        "high_roi_path_observed": False,
                    }
                ),
                encoding="utf-8",
            )
            with patch.object(staid, "OBSERVER_SMOKE_SAVE_SUMMARY_JSON", summary_json):
                with patch.object(staid, "OBSERVER_SMOKE_SAVE_SUMMARY_MD", summary_md):
                    log = observer_test_log_text(self.playset)
        self.assertIn("Short Irony-launched save summary", log)
        self.assertIn("Short smoke passes: True", log)
        self.assertIn("P15 runtime/observer validation is superseded", log)
        self.assertIn("High-ROI path observed: False", log)

    def test_write_helpers_create_parent_directories_and_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_csv(root / "nested" / "rows.csv", [{"a": 1, "b": "x"}])
            write_json(root / "nested" / "data.json", {"b": 2, "a": 1})
            write_text_file(root / "nested" / "text.txt", "hello\n")
            with (root / "nested" / "rows.csv").open(encoding="utf-8") as handle:
                self.assertEqual(list(csv.DictReader(handle))[0]["b"], "x")
            self.assertEqual(json.loads((root / "nested" / "data.json").read_text(encoding="utf-8")), {"a": 1, "b": 2})
            self.assertEqual((root / "nested" / "text.txt").read_text(encoding="utf-8"), "hello\n")

    def test_launcher_descriptor_installation_state_and_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            launcher_root = root / "launcher_mods"
            dlc_load = root / "dlc_load.json"
            mod_root = root / "StellarAIDirector"
            mod_root.mkdir()
            (mod_root / "descriptor.mod").write_text(descriptor_text(), encoding="utf-8")
            descriptor = launcher_descriptor_text(mod_root)
            self.assertIn('name="Stellar AI Director"', descriptor)
            self.assertIn(mod_root.resolve().as_posix(), descriptor)
            self.assertEqual(launcher_descriptor_path(launcher_root), launcher_root / "StellarAIDirector.mod")
            missing = collect_launcher_installation_state(launcher_root, mod_root, dlc_load)
            self.assertFalse(missing["descriptor_exists"])
            self.assertFalse(missing["enabled_in_dlc_load"])
            installed = install_launcher_descriptor(launcher_root, mod_root)
            self.assertEqual(installed, launcher_root / "StellarAIDirector.mod")
            dlc_load.write_text('{"disabled_dlcs":[],"enabled_mods":["mod/ugc_parent.mod"]}', encoding="utf-8")
            enabled_path = enable_director_in_dlc_load(dlc_load)
            enable_director_in_dlc_load(dlc_load)
            self.assertEqual(enabled_path, dlc_load)
            self.assertEqual(json.loads(dlc_load.read_text(encoding="utf-8"))["enabled_mods"].count("mod/StellarAIDirector.mod"), 1)
            state = collect_launcher_installation_state(launcher_root, mod_root, dlc_load)
            self.assertTrue(state["descriptor_exists"])
            self.assertTrue(state["source_descriptor_exists"])
            self.assertTrue(state["descriptor_points_to_source"])
            self.assertTrue(state["enabled_in_dlc_load"])
            set_director_enabled_in_dlc_load(False, dlc_load)
            disabled = json.loads(dlc_load.read_text(encoding="utf-8"))["enabled_mods"]
            self.assertEqual(disabled, ["mod/ugc_parent.mod"])
            disable_director_in_dlc_load(dlc_load)
            self.assertEqual(json.loads(dlc_load.read_text(encoding="utf-8"))["enabled_mods"], ["mod/ugc_parent.mod"])
            enable_director_in_dlc_load(dlc_load)
            installed.write_text('path="C:/wrong/path"\n', encoding="utf-8")
            wrong = collect_launcher_installation_state(launcher_root, mod_root, dlc_load)
            self.assertFalse(wrong["descriptor_points_to_source"])


class CommandWrapperTests(unittest.TestCase):
    def test_generate_wrapper_calls_run_all(self):
        with patch.object(generate_stellar_ai_director_patch, "run_all") as run_all:
            generate_stellar_ai_director_patch.main()
            run_all.assert_called_once_with()

    def test_roi_wrapper_calls_generate_roi_artifacts(self):
        with patch.object(build_ai_roi_matrix, "generate_roi_artifacts") as generate:
            build_ai_roi_matrix.main()
            generate.assert_called_once_with()

    def test_active_playset_wrapper_writes_snapshot(self):
        with patch.object(build_active_playset_snapshot, "build_active_playset_snapshot", return_value={"ok": True}) as build:
            with patch.object(build_active_playset_snapshot, "write_json") as write:
                build_active_playset_snapshot.main()
        build.assert_called_once_with()
        self.assertEqual(write.call_args.args[1], {"ok": True})

    def test_validate_wrapper_prints_success_and_exits_on_errors(self):
        with patch.object(validate_stellar_ai_director_patch, "validate_generated_patch", return_value=[]):
            with patch("builtins.print") as printed:
                validate_stellar_ai_director_patch.main()
        printed.assert_called_once_with("Stellar AI Director validation passed.")
        with patch.object(validate_stellar_ai_director_patch, "validate_generated_patch", return_value=["bad"]):
            with self.assertRaises(SystemExit):
                validate_stellar_ai_director_patch.main()

    def test_install_launcher_descriptor_wrapper_prints_descriptor_path(self):
        with patch.object(install_stellar_ai_director_launcher_descriptor, "install_launcher_descriptor", return_value=Path("x.mod")):
            with patch("builtins.print") as printed:
                install_stellar_ai_director_launcher_descriptor.main()
        printed.assert_called_once_with(Path("x.mod"))

    def test_enable_director_in_dlc_load_wrapper_prints_path(self):
        with patch.object(enable_stellar_ai_director_in_dlc_load, "enable_director_in_dlc_load", return_value=Path("dlc_load.json")):
            with patch("builtins.print") as printed:
                enable_stellar_ai_director_in_dlc_load.main()
        printed.assert_called_once_with(Path("dlc_load.json"))

    def test_add_director_to_irony_collection_wrapper_prints_result(self):
        sample = {"status": "updated"}
        with patch.object(
            add_stellar_ai_director_to_irony_collection,
            "append_director_to_selected_irony_collection",
            return_value=sample,
        ) as append:
            with patch("builtins.print") as printed:
                add_stellar_ai_director_to_irony_collection.main()
        append.assert_called_once_with()
        printed.assert_called_once_with(sample)

    def test_disable_director_in_dlc_load_wrapper_prints_path(self):
        with patch.object(disable_stellar_ai_director_in_dlc_load, "disable_director_in_dlc_load", return_value=Path("dlc_load.json")):
            with patch("builtins.print") as printed:
                disable_stellar_ai_director_in_dlc_load.main()
        printed.assert_called_once_with(Path("dlc_load.json"))

    def test_launch_comparison_wrapper_calls_generator(self):
        with patch.object(build_stellar_ai_director_launch_comparison, "generate_launch_comparison_artifacts") as generate:
            build_stellar_ai_director_launch_comparison.main()
        generate.assert_called_once_with()

    def test_observer_save_summary_wrapper_calls_generator(self):
        with patch.object(
            build_stellar_ai_director_observer_save_summary, "generate_observer_save_summary_artifacts"
        ) as generate:
            build_stellar_ai_director_observer_save_summary.main()
        generate.assert_called_once_with()

    def test_dependency_audit_wrapper_calls_generator(self):
        with patch.object(build_stellar_ai_director_dependency_audit, "generate_dependency_audit_artifacts") as generate:
            build_stellar_ai_director_dependency_audit.main()
        generate.assert_called_once_with()

    def test_irony_order_proof_wrapper_calls_generator(self):
        with patch.object(build_stellar_ai_director_irony_order_proof, "generate_irony_order_proof_artifacts") as generate:
            build_stellar_ai_director_irony_order_proof.main()
        generate.assert_called_once_with()

    def test_file_audit_wrapper_calls_generator(self):
        with patch.object(build_stellar_ai_director_file_audit, "generate_file_audit_artifacts") as generate:
            build_stellar_ai_director_file_audit.main()
        generate.assert_called_once_with()

    def test_integration_policy_audit_wrapper_calls_generator(self):
        with patch.object(
            build_stellar_ai_director_integration_policy_audit, "generate_integration_policy_audit_artifacts"
        ) as generate:
            build_stellar_ai_director_integration_policy_audit.main()
        generate.assert_called_once_with()

    def test_roi_quality_audit_wrapper_calls_generator(self):
        with patch.object(
            build_stellar_ai_director_roi_quality_audit, "generate_roi_quality_audit_artifacts"
        ) as generate:
            build_stellar_ai_director_roi_quality_audit.main()
        generate.assert_called_once_with()

    def test_plan_status_wrapper_calls_generator(self):
        with patch.object(build_stellar_ai_director_plan_status, "generate_plan_status_artifacts") as generate:
            build_stellar_ai_director_plan_status.main()
        generate.assert_called_once_with()

    def test_reference_audit_wrapper_calls_generator(self):
        with patch.object(build_stellar_ai_director_reference_audit, "generate_reference_audit_artifacts") as generate:
            build_stellar_ai_director_reference_audit.main()
        generate.assert_called_once_with()

    def test_main_menu_proof_wrapper_calls_recorder(self):
        sample = {"main_menu_proven": False}
        with patch.object(record_stellar_ai_director_main_menu_proof, "record_main_menu_proof_marker", return_value=sample) as record:
            with patch("builtins.print") as printed:
                record_stellar_ai_director_main_menu_proof.main()
        record.assert_called_once_with()
        self.assertIn("main_menu_proven=False", printed.call_args.args[0])

    def test_main_guards_execute_for_thin_wrappers(self):
        with patch.object(staid, "run_all") as run_all:
            runpy.run_path(str(Path("tools/generate_stellar_ai_director_patch.py")), run_name="__main__")
            run_all.assert_called_once_with()
        with patch.object(staid, "generate_roi_artifacts") as generate:
            runpy.run_path(str(Path("tools/build_ai_roi_matrix.py")), run_name="__main__")
            generate.assert_called_once_with()
        with patch.object(staid, "generate_integration_policy_audit_artifacts") as generate:
            runpy.run_path(str(Path("tools/build_stellar_ai_director_integration_policy_audit.py")), run_name="__main__")
            generate.assert_called_once_with()
        with patch.object(staid, "generate_roi_quality_audit_artifacts") as generate:
            runpy.run_path(str(Path("tools/build_stellar_ai_director_roi_quality_audit.py")), run_name="__main__")
            generate.assert_called_once_with()
        with patch.object(staid, "build_active_playset_snapshot", return_value={"ok": True}):
            with patch.object(staid, "write_json") as write:
                runpy.run_path(str(Path("tools/build_active_playset_snapshot.py")), run_name="__main__")
        self.assertEqual(write.call_args.args[1], {"ok": True})
        with patch.object(staid, "validate_generated_patch", return_value=[]):
            with patch("builtins.print"):
                runpy.run_path(str(Path("tools/validate_stellar_ai_director_patch.py")), run_name="__main__")
        with patch.object(staid, "install_launcher_descriptor", return_value=Path("StellarAIDirector.mod")) as install:
            with patch("builtins.print") as printed:
                runpy.run_path(str(Path("tools/install_stellar_ai_director_launcher_descriptor.py")), run_name="__main__")
        install.assert_called_once_with()
        printed.assert_called_once_with(Path("StellarAIDirector.mod"))
        with patch.object(staid, "enable_director_in_dlc_load", return_value=Path("dlc_load.json")) as enable:
            with patch("builtins.print") as printed:
                runpy.run_path(str(Path("tools/enable_stellar_ai_director_in_dlc_load.py")), run_name="__main__")
        enable.assert_called_once_with()
        printed.assert_called_once_with(Path("dlc_load.json"))
        with patch.object(staid, "disable_director_in_dlc_load", return_value=Path("dlc_load.json")) as disable:
            with patch("builtins.print") as printed:
                runpy.run_path(str(Path("tools/disable_stellar_ai_director_in_dlc_load.py")), run_name="__main__")
        disable.assert_called_once_with()
        printed.assert_called_once_with(Path("dlc_load.json"))
        with patch.object(staid, "generate_launch_comparison_artifacts") as generate_comparison:
            runpy.run_path(str(Path("tools/build_stellar_ai_director_launch_comparison.py")), run_name="__main__")
            generate_comparison.assert_called_once_with()
        with patch.object(staid, "generate_observer_save_summary_artifacts") as generate_observer_summary:
            runpy.run_path(str(Path("tools/build_stellar_ai_director_observer_save_summary.py")), run_name="__main__")
            generate_observer_summary.assert_called_once_with()
        with patch.object(staid, "generate_dependency_audit_artifacts") as generate_dependency_audit:
            runpy.run_path(str(Path("tools/build_stellar_ai_director_dependency_audit.py")), run_name="__main__")
            generate_dependency_audit.assert_called_once_with()
        with patch.object(staid, "generate_irony_order_proof_artifacts") as generate_irony_order:
            runpy.run_path(str(Path("tools/build_stellar_ai_director_irony_order_proof.py")), run_name="__main__")
            generate_irony_order.assert_called_once_with()
        with patch.object(staid, "generate_file_audit_artifacts") as generate_file_audit:
            runpy.run_path(str(Path("tools/build_stellar_ai_director_file_audit.py")), run_name="__main__")
            generate_file_audit.assert_called_once_with()
        with patch.object(staid, "generate_plan_status_artifacts") as generate_plan_status:
            runpy.run_path(str(Path("tools/build_stellar_ai_director_plan_status.py")), run_name="__main__")
            generate_plan_status.assert_called_once_with()
        with patch.object(staid, "generate_reference_audit_artifacts") as generate_reference_audit:
            runpy.run_path(str(Path("tools/build_stellar_ai_director_reference_audit.py")), run_name="__main__")
            generate_reference_audit.assert_called_once_with()
        with patch.object(staid, "record_main_menu_proof_marker", return_value={"main_menu_proven": True}) as record:
            with patch("builtins.print") as printed:
                runpy.run_path(str(Path("tools/record_stellar_ai_director_main_menu_proof.py")), run_name="__main__")
        record.assert_called_once_with()
        self.assertIn("main_menu_proven=True", printed.call_args.args[0])


class SnapshotInventoryBuilderTests(unittest.TestCase):
    def test_build_inventory_outputs_descriptor_file_object_and_ai_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "snapshot-manifest.csv").write_text("id,slug,name,version\n1,test-mod,Manifest Name,0.1\n", encoding="utf-8")
            mod = root / "1-test-mod"
            (mod / "common" / "technology").mkdir(parents=True)
            (mod / "descriptor.mod").write_text(
                'name="Descriptor Name"\nversion="1.0"\nsupported_version="v4.4.*"\nremote_file_id="1"\n',
                encoding="utf-8",
            )
            (mod / "common" / "technology" / "tech.txt").write_text(
                "tech_test = { ai_weight = { weight = 1 } potential = { always = yes } }\n",
                encoding="utf-8",
            )
            (mod / "thumbnail.png").write_bytes(b"\x89PNG\r\n")
            build_mod_snapshot_inventory.build(root)
            with (root / "descriptor-inventory.csv").open(encoding="utf-8-sig") as handle:
                descriptors = list(csv.DictReader(handle))
            with (root / "pdx-object-inventory.csv").open(encoding="utf-8-sig") as handle:
                objects = list(csv.DictReader(handle))
            with (root / "ai-surface-inventory.csv").open(encoding="utf-8-sig") as handle:
                ai_rows = list(csv.DictReader(handle))
            with (root / "ai-marker-summary.csv").open(encoding="utf-8-sig") as handle:
                summary = list(csv.DictReader(handle))
            self.assertEqual(descriptors[0]["name"], "Descriptor Name")
            self.assertEqual(objects[0]["object_name"], "tech_test")
            self.assertEqual(ai_rows[0]["ai_weight"], "1")
            self.assertEqual(summary[0]["ai_weight"], "1")

    def test_inventory_helpers_cover_missing_descriptor_and_manifest_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertTrue(build_mod_snapshot_inventory.is_text_file(root / "x.txt"))
            self.assertFalse(build_mod_snapshot_inventory.is_text_file(root / "x.png"))
            self.assertEqual(build_mod_snapshot_inventory.parse_descriptor(root), {
                "name": "",
                "version": "",
                "supported_version": "",
                "remote_file_id": "",
            })
            with self.assertRaises(FileNotFoundError):
                build_mod_snapshot_inventory.read_manifest(root)
            encoded = root / "encoded.txt"
            encoded.write_bytes("caf\xe9".encode("cp1252"))
            self.assertIn("café", build_mod_snapshot_inventory.read_text(encoded))

    def test_inventory_main_uses_resolved_snapshot_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "snapshot-manifest.csv").write_text("id,slug,name,version\n1,test,Test,1\n", encoding="utf-8")
            (root / "1-test").mkdir()
            with patch.object(sys, "argv", ["build_mod_snapshot_inventory.py", str(root)]):
                build_mod_snapshot_inventory.main()
            self.assertTrue((root / "file-inventory.csv").exists())
            with patch.object(sys, "argv", ["build_mod_snapshot_inventory.py", str(root)]):
                runpy.run_path(str(Path("tools/build_mod_snapshot_inventory.py")), run_name="__main__")


class ArtifactGenerationAndValidationTests(unittest.TestCase):
    def sample_rows(self):
        return [
            {
                "decision_eligible": "yes",
                "data_quality": "resolved",
                "build_cost_value": 20000.0,
                "priority_tier": "economy_multiplier",
                "object_name": "dyson_sphere_5",
                "mod_name": "Gigas",
                "market_deficit_cost_energy": 100000.0,
                "market_deficit_annual_payoff_energy": 50000.0,
                "market_deficit_payback_years": 2.0,
                "strategic_shipyard_annual_alloy_throughput": 0.0,
                "strategic_shipyard_payback_years": "",
                "director_strategy_role": "economy_multiplier",
                "director_build_gate": "when_survival_clear_and_megastructure_reserve_safe",
                "director_surplus_sink_priority": "",
                "director_surplus_sink_role": "not_surplus_sink",
                "shipyard_capacity": 0.0,
                "build_speed": 0.0,
                "source_has_ai_weight": True,
                "produces": "energy=1000",
                "market_unpriced_resources": "",
            },
            {
                "decision_eligible": "yes",
                "data_quality": "resolved",
                "build_cost_value": 50000.0,
                "priority_tier": "shipyard_multiplier",
                "object_name": "mega_shipyard_3",
                "mod_name": "NSC3",
                "market_deficit_cost_energy": 250000.0,
                "market_deficit_annual_payoff_energy": 0.0,
                "market_deficit_payback_years": "",
                "strategic_shipyard_annual_alloy_throughput": 45000.0,
                "strategic_shipyard_payback_years": 0.5,
                "director_strategy_role": "fleet_production_sink",
                "director_build_gate": "after_research_sink_when_alloy_energy_surplus_needs_fleet_sink",
                "director_surplus_sink_priority": 2,
                "director_surplus_sink_role": "fleet_sink",
                "shipyard_capacity": 100.0,
                "build_speed": 0.0,
                "source_has_ai_weight": False,
                "produces": "",
                "market_unpriced_resources": "",
            },
        ]

    def test_integration_surface_inventory_covers_p6_to_p11_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_csv(
                root / "snapshot-manifest.csv",
                [
                    {"id": "1121692237", "name": "Gigas", "snapshot_path": str(root / "gigas")},
                    {"id": "683230077", "name": "NSC3", "snapshot_path": str(root / "nsc3")},
                    {"id": "2648658105", "name": "ESC", "snapshot_path": str(root / "esc")},
                    {"id": "3250900527", "name": "Starbase Extended", "snapshot_path": str(root / "starbase_no_common")},
                ],
            )
            fixtures = {
                "gigas/common/technology/tech.txt": "@weight = 20\ntech_ehof_sentient_tier_1 = { ai_weight = { weight = @weight } }",
                "gigas/common/technology/bad.txt": "broken = {",
                "gigas/common/ascension_perks/ap.txt": "ap_gigastructural_constructs = { ai_weight = { weight = 5 } }",
                "gigas/common/traditions/trad.txt": "tr_giga_test = { }",
                "gigas/common/megastructures/mega.txt": "giga_dyson_test = { ai_weight = { weight = 1 } }",
                "nsc3/common/ship_sizes/ships.txt": "nsc_battlecruiser = { ai_weight = { weight = 1 } }",
                "esc/common/component_templates/components.txt": "ESC_LASER_TEST = { ai_weight = { weight = 1 } }",
            }
            for relative, text in fixtures.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            surface_rows = collect_integration_surface_rows(root)
            names = {row["object_name"]: row for row in surface_rows}
            self.assertEqual(names["tech_ehof_sentient_tier_1"]["policy_recommendation"], "mega_giga_unlock_priority")
            self.assertEqual(names["ESC_LASER_TEST"]["minimum_v1_intervention"], "defer_direct_override_parent_ai_weight_present")
            report = integration_surface_report_text(surface_rows)
            self.assertIn("Surface Counts", report)
            self.assertIn("tech_ehof_sentient_tier_1", report)
            self.assertNotIn("@weight", names)
            self.assertEqual(
                integration_policy_recommendation("683230077", "technology", "nsc_shipyard_unlock", False),
                ("shipyard_and_ship_size_unlock_priority", "candidate_tech_weight_surface"),
            )
            policy_cases = [
                (("1121692237", "component_template", "COMPONENT_NO_AI", False), ("preserve_parent_design_ai", "audit_parent_gap")),
                (("1121692237", "megastructure", "unknown_path_special", False), ("observe_for_exotic_or_path_specific_gate", "defer_until_roi_candidate")),
                (("2648658105", "technology", "esc_unlock", False), ("component_unlock_priority", "candidate_tech_weight_surface")),
                (("3250900527", "technology", "starbase_unlock", False), ("defensive_starbase_unlock_priority", "candidate_tech_weight_surface")),
                (("1121692237", "technology", "unrelated_unlock", False), ("audit_unlock_chain", "defer_unless_core_path")),
                (("3250900527", "starbase_module", "sb_ext_bastion", False), ("defensive_or_shipyard_starbase_policy", "candidate_starbase_weight_surface")),
                (("1121692237", "building", "building_capacity", False), ("planetary_capacity_audit", "defer_broad_planet_automation_override")),
                (("1121692237", "unknown", "unknown", False), ("audit_only", "defer")),
            ]
            for args, expected in policy_cases:
                self.assertEqual(integration_policy_recommendation(*args), expected)

    def test_generate_roi_artifacts_writes_csvs_and_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp)
            with patch.object(staid, "RESEARCH_ROOT", research):
                with patch.object(staid, "extract_megastructure_rows", return_value=self.sample_rows()):
                    with patch.object(staid, "market_price_rows", return_value=[{"resource": "alloys", "market_amount": 100}]):
                        with patch.object(staid, "generate_roi_quality_audit_artifacts", return_value=[]) as audit:
                            with patch.object(staid, "generate_integration_surface_artifacts", return_value=[]):
                                rows = staid.generate_roi_artifacts()
            self.assertEqual(rows, self.sample_rows())
            audit.assert_called_once_with(self.sample_rows())
            self.assertTrue((research / "stellar-ai-director-roi-matrix-2026-07-04.csv").exists())
            report = (research / "stellar-ai-director-roi-matrix-2026-07-04.md").read_text(encoding="utf-8")
            self.assertIn("Top Decision-Eligible Rows", report)
            self.assertIn("dyson_sphere_5", report)

    def test_roi_quality_status_classifies_failures_warnings_and_unknown_checks(self):
        row = dict(self.sample_rows()[0])
        self.assertEqual(roi_quality_status(row, "decision_eligible_data_quality")[0], "ok")
        self.assertEqual(roi_quality_status(row, "decision_eligible_cost")[0], "ok")
        self.assertEqual(roi_quality_status(row, "decision_eligible_unresolved_symbols")[0], "ok")
        row["data_quality"] = "symbolic_unresolved"
        self.assertEqual(roi_quality_status(row, "decision_eligible_data_quality")[0], "fail")
        row["data_quality"] = "resolved"
        row["build_cost_value"] = 0.0
        self.assertEqual(roi_quality_status(row, "decision_eligible_cost")[0], "fail")
        row["build_cost_value"] = 1.0
        row["unresolved_symbols"] = "@missing"
        self.assertEqual(roi_quality_status(row, "decision_eligible_unresolved_symbols")[0], "fail")
        row["unresolved_symbols"] = ""
        row["market_unpriced_resources"] = "unity=1000"
        self.assertEqual(roi_quality_status(row, "decision_eligible_market_unpriced_resources")[0], "warning")
        with self.assertRaises(ValueError):
            roi_quality_status(row, "not_a_check")

    def test_collect_roi_quality_rows_checks_rows_and_threshold_count(self):
        rows = self.sample_rows()
        audit_rows = collect_roi_quality_rows(rows)
        self.assertEqual(len(audit_rows), len(rows) * 4 + 1)
        self.assertEqual(audit_rows[-1]["check"], "threshold_eligible_count")
        self.assertEqual(audit_rows[-1]["status"], "ok")
        self.assertIn("audit counted 2", audit_rows[-1]["reason"])
        bad = dict(rows[0], data_quality="symbolic_unresolved", build_cost_value=0.0, unresolved_symbols="@bad")
        bad_rows = collect_roi_quality_rows([bad])
        failures = [row for row in bad_rows if row["status"] == "fail"]
        self.assertEqual({row["check"] for row in failures}, {
            "decision_eligible_data_quality",
            "decision_eligible_cost",
            "decision_eligible_unresolved_symbols",
        })

    def test_generate_roi_quality_audit_artifacts_writes_csv_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp)
            with patch.object(staid, "ROI_QUALITY_AUDIT_CSV", research / "roi-quality.csv"):
                with patch.object(staid, "ROI_QUALITY_AUDIT_MD", research / "roi-quality.md"):
                    rows = generate_roi_quality_audit_artifacts(self.sample_rows())
            self.assertTrue((research / "roi-quality.csv").exists())
            report = (research / "roi-quality.md").read_text(encoding="utf-8")
            self.assertIn("Stellar AI Director ROI Quality Audit", report)
            self.assertIn("Status Counts", report)
            self.assertEqual(rows[-1]["check"], "threshold_eligible_count")

    def test_roi_quality_audit_report_lists_non_ok_rows(self):
        audit_rows = collect_roi_quality_rows([dict(self.sample_rows()[0], market_unpriced_resources="unity=100")])
        report = roi_quality_audit_report_text(audit_rows)
        self.assertIn("warning", report)
        self.assertIn("unity=100", report)

    def test_generate_integration_surface_artifacts_writes_csv_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp)
            sample = [
                {
                    "phase": "P6",
                    "mod_id": "1121692237",
                    "mod_name": "Gigas",
                    "object_type": "technology",
                    "object_name": "tech_ehof_sentient_tier_1",
                    "source_file": "common/technology/tech.txt",
                    "source_has_ai_weight": "yes",
                    "policy_recommendation": "mega_giga_unlock_priority",
                    "minimum_v1_intervention": "candidate_tech_weight_surface",
                    "validation_basis": "parsed_source_object_exists",
                }
            ]
            with patch.object(staid, "RESEARCH_ROOT", research):
                with patch.object(staid, "collect_integration_surface_rows", return_value=sample):
                    with patch.object(staid, "generate_integration_policy_audit_artifacts", return_value=[]) as audit:
                        rows = generate_integration_surface_artifacts()
            self.assertEqual(rows, sample)
            audit.assert_called_once_with(sample)
            self.assertTrue((research / "stellar-ai-director-integration-surfaces-2026-07-04.csv").exists())
            report = (research / "stellar-ai-director-integration-surfaces-2026-07-04.md").read_text(encoding="utf-8")
            self.assertIn("tech_ehof_sentient_tier_1", report)

    def integration_policy_sample_row(self, root: Path) -> dict[str, str]:
        write_csv(
            root / "snapshot-manifest.csv",
            [{"id": "1121692237", "name": "Gigas", "snapshot_path": str(root / "gigas")}],
        )
        source = root / "gigas" / "common" / "technology"
        source.mkdir(parents=True)
        (source / "tech.txt").write_text("tech_ehof_sentient_tier_1 = { ai_weight = { weight = 1 } }", encoding="utf-8")
        return {
            "phase": "P6",
            "mod_id": "1121692237",
            "mod_name": "Gigas",
            "object_type": "technology",
            "object_name": "tech_ehof_sentient_tier_1",
            "source_file": "common/technology/tech.txt",
            "source_has_ai_weight": "yes",
            "policy_recommendation": "mega_giga_unlock_priority",
            "minimum_v1_intervention": "candidate_tech_weight_surface",
            "validation_basis": "parsed_source_object_exists",
        }

    def test_integration_policy_priority_band_maps_plan_surfaces(self):
        cases = [
            ({"policy_recommendation": "component_unlock_priority"}, "advanced_military_component_unlocks"),
            ({"policy_recommendation": "mega_giga_unlock_priority"}, "mega_giga_unlock_chain"),
            ({"policy_recommendation": "shipyard_and_ship_size_unlock_priority"}, "shipyard_fleet_throughput_unlocks"),
            ({"policy_recommendation": "defensive_starbase_unlock_priority"}, "defensive_starbase_unlocks"),
            ({"policy_recommendation": "roi_driven_build_priority"}, "roi_driven_mega_giga_builds"),
            ({"policy_recommendation": "defensive_or_shipyard_starbase_policy"}, "defensive_or_shipyard_starbase_policy"),
            ({"policy_recommendation": "planetary_capacity_audit"}, "planetary_and_building_capacity"),
            ({"policy_recommendation": "preserve_parent_design_ai"}, "nsc3_esc_parent_design_ai_preservation"),
            ({"policy_recommendation": "unlock_path_audit", "object_type": "ascension_perk"}, "ap_tradition_unlock_path"),
            ({"policy_recommendation": "unknown"}, "audit_only"),
        ]
        for row, expected in cases:
            self.assertEqual(integration_policy_priority_band(row), expected)

    def test_collect_integration_policy_audit_rows_validates_source_existence_and_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ready = self.integration_policy_sample_row(root)
            warning = dict(ready, object_name="tech_gap", minimum_v1_intervention="audit_parent_gap")
            deferred = dict(ready, object_name="tech_defer", minimum_v1_intervention="defer_unless_core_path")
            unknown = dict(ready, object_name="tech_unknown", minimum_v1_intervention="new_intervention")
            missing_source = dict(ready, object_name="tech_missing", source_file="common/technology/missing.txt")
            bad_basis = dict(ready, object_name="tech_bad_basis", validation_basis="unchecked")
            rows = collect_integration_policy_audit_rows(
                [ready, warning, deferred, unknown, missing_source, bad_basis],
                snapshot_root=root,
            )
        by_name = {row["object_name"]: row for row in rows}
        self.assertEqual(by_name["tech_ehof_sentient_tier_1"]["status"], "ready")
        self.assertEqual(by_name["tech_gap"]["status"], "warning")
        self.assertEqual(by_name["tech_defer"]["status"], "deferred")
        self.assertEqual(by_name["tech_unknown"]["status"], "warning")
        self.assertIn("unrecognized intervention", by_name["tech_unknown"]["reason"])
        self.assertEqual(by_name["tech_missing"]["status"], "fail")
        self.assertEqual(by_name["tech_missing"]["source_exists"], "no")
        self.assertEqual(by_name["tech_bad_basis"]["status"], "fail")

    def test_integration_policy_audit_status_fails_missing_fields_and_snapshot(self):
        status, reason, source_exists = integration_policy_audit_status({}, {})
        self.assertEqual(status, "fail")
        self.assertIn("missing required fields", reason)
        self.assertFalse(source_exists)
        row = {
            "phase": "P6",
            "mod_id": "missing",
            "object_type": "technology",
            "object_name": "tech_missing",
            "source_file": "common/technology/tech.txt",
            "validation_basis": "parsed_source_object_exists",
        }
        status, reason, source_exists = integration_policy_audit_status(row, {})
        self.assertEqual(status, "fail")
        self.assertIn("missing source snapshot", reason)
        self.assertFalse(source_exists)

    def test_generate_integration_policy_audit_artifacts_writes_csv_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            research = root / "research"
            row = self.integration_policy_sample_row(root)
            with patch.object(staid, "INTEGRATION_POLICY_AUDIT_CSV", research / "policy.csv"):
                with patch.object(staid, "INTEGRATION_POLICY_AUDIT_MD", research / "policy.md"):
                    audit_rows = generate_integration_policy_audit_artifacts([row], snapshot_root=root)
            self.assertEqual(audit_rows[0]["status"], "ready")
            self.assertTrue((research / "policy.csv").exists())
            report = (research / "policy.md").read_text(encoding="utf-8")
            self.assertIn("Integration Policy Audit", report)
            self.assertIn("mega_giga_unlock_chain", report)

    def test_integration_policy_audit_report_lists_attention_rows(self):
        report = integration_policy_audit_report_text(
            [
                {
                    "phase": "P11",
                    "status": "warning",
                    "priority_band": "nsc3_esc_parent_design_ai_preservation",
                    "object_name": "COMPONENT_TEST",
                    "object_type": "component_template",
                    "reason": "parent object lacks AI weight",
                }
            ]
        )
        self.assertIn("COMPONENT_TEST", report)
        self.assertIn("parent object lacks AI weight", report)

    def test_generated_conflict_classifier_labels_override_additive_and_collision(self):
        with tempfile.TemporaryDirectory() as tmp:
            mod_root = Path(tmp) / "mod"
            with patch.object(staid, "collect_object_names", return_value={}):
                self.assertEqual(collect_generated_conflict_rows(mod_root, Path(tmp) / "snapshots"), [])
            budget = mod_root / "common" / "ai_budget"
            budget.mkdir(parents=True)
            (budget / "override.txt").write_text(
                "# Full-object override: test ownership.\nknown_budget = { resource = alloys type = expenditure category = megastructures }",
                encoding="utf-8",
            )
            (budget / "additive.txt").write_text(
                "staid_new_budget = { resource = alloys type = expenditure category = megastructures }",
                encoding="utf-8",
            )
            (budget / "collision.txt").write_text(
                "known_without_note = { resource = alloys type = expenditure category = megastructures }",
                encoding="utf-8",
            )
            (budget / "bad.txt").write_text("broken = {", encoding="utf-8")
            with patch.object(staid, "collect_object_names", return_value={"ai_budget": {"known_budget", "known_without_note"}}):
                rows = collect_generated_conflict_rows(mod_root, Path(tmp) / "snapshots")
            by_name = {row["object_name"]: row for row in rows}
            self.assertEqual(by_name["known_budget"]["classification"], "intentional_director_override")
            self.assertEqual(by_name["staid_new_budget"]["classification"], "additive_director_object")
            self.assertEqual(by_name["known_without_note"]["classification"], "unexpected_parent_object_collision")
            self.assertNotIn("broken", by_name)
            report = generated_conflict_report_text(rows)
            self.assertIn("known_without_note", report)

    def test_generate_conflict_classification_artifacts_writes_csv_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp)
            sample = [
                {
                    "object_type": "ai_budget",
                    "object_name": "known_budget",
                    "generated_file": "common/ai_budget/test.txt",
                    "parent_has_object": "yes",
                    "classification": "intentional_director_override",
                    "reason": "generated file declares full-object override ownership",
                }
            ]
            with patch.object(staid, "RESEARCH_ROOT", research):
                with patch.object(staid, "collect_generated_conflict_rows", return_value=sample):
                    rows = generate_conflict_classification_artifacts()
            self.assertEqual(rows, sample)
            self.assertTrue((research / "stellar-ai-director-generated-conflicts-2026-07-04.csv").exists())
            report = (research / "stellar-ai-director-generated-conflicts-2026-07-04.md").read_text(encoding="utf-8")
            self.assertIn("known_budget", report)

    def test_observer_save_summary_parses_mods_country_metrics_and_income(self):
        gamestate = '''version="Pegasus v4.4.4"
name="United Nations of Earth"
date="2202.01.01"
mods=
{
    "Stellar AI Director"
    "Gigastructural Engineering & More (4.4)"
    "NSC3"
    "Extra Ship Components NEXT"
}
player=
{
    {
        name="unknown"
        country=0
    }
}
country=
{
    0=
    {
        initialized=yes
        budget=
        {
            current_month=
            {
                income=
                {
                    country_base={ energy=20 minerals=30 alloys=4 }
                    jobs={ energy=5 engineering_research=12 }
                }
            }
        }
        economy_power=540.2
        tech_power=277.5
        fleet_size=15
        used_naval_capacity=15
        empire_size=51
        num_sapient_pops=5261
    }
    1=
    {
        initialized=yes
        economy_power=400
    }
}
'''
        with tempfile.TemporaryDirectory() as tmp:
            save_path = Path(tmp) / "autosave_2202.01.01.sav"
            with zipfile.ZipFile(save_path, "w") as archive:
                archive.writestr("gamestate", gamestate)
                archive.writestr("meta", "name=smoke\n")
            self.assertIn("Stellar AI Director", load_stellaris_save_gamestate(save_path))
            country_block = extract_assignment_block(gamestate, "country")
            self.assertEqual([country_id for country_id, _ in iter_numbered_child_blocks(country_block)], ["0", "1"])
            summary = collect_observer_save_summary(save_path)
        self.assertTrue(summary["short_smoke_passes"])
        self.assertFalse(summary["high_roi_path_observed"])
        self.assertEqual(summary["date"], "2202.01.01")
        self.assertEqual(summary["player_country"], "0")
        self.assertEqual(summary["initialized_country_count"], 2)
        self.assertEqual(summary["player_metrics"]["economy_power"], 540.2)
        self.assertEqual(summary["player_monthly_income"]["energy"], 25.0)
        self.assertEqual(summary["player_monthly_income"]["engineering_research"], 12.0)

    def test_observer_save_summary_report_and_artifact_writer_keep_runtime_context(self):
        summary = {
            "save_path": "C:/save/autosave_2202.01.01.sav",
            "date": "2202.01.01",
            "version": "Pegasus v4.4.4",
            "name": "United Nations of Earth",
            "short_smoke_passes": True,
            "high_roi_path_observed": False,
            "required_mods_present": {"Stellar AI Director": True},
            "mod_count": 1,
            "player_country": "0",
            "country_count": 2,
            "initialized_country_count": 2,
            "player_metrics": {"economy_power": 540.2},
            "player_monthly_income": {"energy": 25.0},
            "short_smoke_checks": {"director_mod_listed": True},
            "p15_completion_note": "Short Irony-launched save evidence is retained as historical context; P15 runtime/observer validation is superseded for this deterministic implementation goal.",
        }
        report = observer_save_summary_report_text(summary)
        self.assertIn("Short smoke passes: True", report)
        self.assertIn("P15 runtime/observer validation is superseded", report)
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "summary.json"
            md_path = Path(tmp) / "summary.md"
            with patch.object(staid, "OBSERVER_SMOKE_SAVE_SUMMARY_JSON", json_path):
                with patch.object(staid, "OBSERVER_SMOKE_SAVE_SUMMARY_MD", md_path):
                    with patch.object(staid, "collect_observer_save_summary", return_value=summary):
                        generated = generate_observer_save_summary_artifacts(Path("save.sav"))
            self.assertEqual(generated["short_smoke_passes"], True)
            self.assertEqual(json.loads(json_path.read_text(encoding="utf-8"))["high_roi_path_observed"], False)
            self.assertIn("High-ROI path observed: False", md_path.read_text(encoding="utf-8"))

    def test_generated_file_audit_classifies_path_parse_empty_and_placeholders(self):
        with tempfile.TemporaryDirectory() as tmp:
            mod_root = Path(tmp) / "mod"
            self.assertEqual(collect_generated_file_audit_rows(mod_root), [])
            good = mod_root / "common" / "scripted_triggers" / "good.txt"
            good.parent.mkdir(parents=True)
            good.write_text("staid_good = { always = yes }\n", encoding="utf-8")
            unsupported = mod_root / "common" / "unsupported_folder" / "bad.txt"
            unsupported.parent.mkdir(parents=True)
            unsupported.write_text("bad = { always = yes }\n", encoding="utf-8")
            suffix = mod_root / "common" / "script_values" / "bad.json"
            suffix.parent.mkdir(parents=True)
            suffix.write_text("bad = { value = 1 }\n", encoding="utf-8")
            broken = mod_root / "common" / "ai_budget" / "broken.txt"
            broken.parent.mkdir(parents=True)
            broken.write_text("broken = {\n", encoding="utf-8")
            empty = mod_root / "common" / "economic_plans" / "empty.txt"
            empty.parent.mkdir(parents=True)
            empty.write_text("# no objects\n", encoding="utf-8")
            placeholder = mod_root / "common" / "script_values" / "placeholder.txt"
            placeholder.write_text("staid_placeholder = $VALUE$\n# TODO\n", encoding="utf-8")

            self.assertEqual(unresolved_template_placeholder_count("x = $VALUE$\nTODO\n__PLACEHOLDER_X__"), 3)
            self.assertEqual(generated_file_path_status(good, mod_root), ("ok", "scripted_triggers"))
            self.assertEqual(generated_file_path_status(Path(tmp) / "outside.txt", mod_root), ("outside_mod_root", ""))
            self.assertEqual(generated_file_path_status(mod_root / "descriptor.mod", mod_root), ("outside_common", ""))
            rows = collect_generated_file_audit_rows(mod_root)
            by_file = {row["generated_file"]: row for row in rows}
            self.assertEqual(by_file["common/scripted_triggers/good.txt"]["status"], "ok")
            self.assertEqual(by_file["common/unsupported_folder/bad.txt"]["status"], "unsupported_common_folder")
            self.assertEqual(by_file["common/script_values/bad.json"]["status"], "unsupported_suffix")
            self.assertEqual(by_file["common/ai_budget/broken.txt"]["status"], "parse_error")
            self.assertEqual(by_file["common/economic_plans/empty.txt"]["status"], "empty_generated_file")
            self.assertEqual(by_file["common/script_values/placeholder.txt"]["status"], "unresolved_placeholder")
            report = generated_file_audit_report_text(rows)
            self.assertIn("unsupported_common_folder", report)
            self.assertIn("placeholder.txt", report)

    def test_generate_file_audit_artifacts_writes_csv_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp)
            sample = [
                {
                    "generated_file": "common/scripted_triggers/good.txt",
                    "folder": "scripted_triggers",
                    "object_type": "scripted_trigger",
                    "path_status": "ok",
                    "parse_status": "ok",
                    "top_level_object_count": 1,
                    "unresolved_placeholder_count": 0,
                    "status": "ok",
                    "reason": "valid generated PDXScript surface",
                }
            ]
            with patch.object(staid, "FILE_AUDIT_CSV", research / "file-audit.csv"):
                with patch.object(staid, "FILE_AUDIT_MD", research / "file-audit.md"):
                    with patch.object(staid, "collect_generated_file_audit_rows", return_value=sample):
                        rows = generate_file_audit_artifacts()
            self.assertEqual(rows, sample)
            self.assertTrue((research / "file-audit.csv").exists())
            self.assertIn("good.txt", (research / "file-audit.md").read_text(encoding="utf-8"))

    def test_dependency_audit_compares_descriptor_and_playset_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            mod_root = Path(tmp) / "mod"
            mod_root.mkdir()
            dependency_lines = "\n".join(
                [
                    '"Stellar AI"',
                    '"Gigastructural Engineering & More (4.4)"',
                    '"NSC3"',
                    '"Extra Ship Components NEXT"',
                    '"Starbase Extended 3.0"',
                    '"!!!Universal Resource Patch [2.4+]"',
                ]
            )
            (mod_root / "descriptor.mod").write_text(f"dependencies={{\n{dependency_lines}\n}}\n", encoding="utf-8")
            playset = {
                "mods": [
                    {"steam_id": "3610149307", "name": "Stellar AI", "position": 10},
                    {"steam_id": "1121692237", "name": "Gigastructural Engineering & More (4.4)", "position": 20},
                    {"steam_id": "683230077", "name": "NSC3", "position": 30},
                    {"steam_id": "2648658105", "name": "Extra Ship Components NEXT", "position": 40},
                    {"steam_id": "3250900527", "name": "Starbase Extended 3.0", "position": 50},
                    {"steam_id": "1595876588", "name": "!!!Universal Resource Patch [2.4+]", "position": 60},
                ]
            }
            self.assertEqual(descriptor_dependencies((mod_root / "descriptor.mod").read_text(encoding="utf-8"))[-1], "!!!Universal Resource Patch [2.4+]")
            rows = collect_dependency_audit_rows(mod_root, playset)
            self.assertEqual({row["status"] for row in rows}, {"ok"})
            self.assertEqual(rows[0]["dependency_type"], "compatibility_dependency")
            report = dependency_audit_report_text(rows)
            self.assertIn("Stellar AI", report)
            self.assertEqual(dependency_status(False, True, True), "missing_descriptor_dependency")
            self.assertEqual(dependency_status(True, False, True), "missing_playset_dependency")
            self.assertEqual(dependency_status(True, True, False), "name_mismatch")

            broken_playset = {
                "mods": [
                    {"steam_id": "3610149307", "name": "Stellar AI - Renamed", "position": 10},
                    {"steam_id": "1121692237", "name": "Gigastructural Engineering & More (4.4)", "position": 20},
                ]
            }
            broken_rows = collect_dependency_audit_rows(mod_root, broken_playset)
            by_name = {row["expected_name"]: row for row in broken_rows}
            self.assertEqual(by_name["Stellar AI"]["status"], "name_mismatch")
            self.assertEqual(by_name["NSC3"]["status"], "missing_playset_dependency")

            (mod_root / "descriptor.mod").write_text('dependencies={\n"Stellar AI"\n}\n', encoding="utf-8")
            missing_descriptor = collect_dependency_audit_rows(mod_root, playset)
            self.assertEqual({row["status"] for row in missing_descriptor if row["expected_name"] == "NSC3"}, {"missing_descriptor_dependency"})
            self.assertEqual(descriptor_dependencies("name=\"No dependencies\""), [])

    def test_generate_dependency_audit_artifacts_writes_csv_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp)
            sample = [
                {
                    "dependency_type": "required_parent",
                    "steam_id": "1",
                    "expected_name": "Parent",
                    "descriptor_present": "yes",
                    "playset_present": "yes",
                    "actual_playset_name": "Parent",
                    "load_position": 1,
                    "status": "ok",
                }
            ]
            with patch.object(staid, "DEPENDENCY_AUDIT_CSV", research / "dependency.csv"):
                with patch.object(staid, "DEPENDENCY_AUDIT_MD", research / "dependency.md"):
                    with patch.object(staid, "collect_dependency_audit_rows", return_value=sample):
                        rows = generate_dependency_audit_artifacts()
            self.assertEqual(rows, sample)
            self.assertTrue((research / "dependency.csv").exists())
            self.assertIn("Parent", (research / "dependency.md").read_text(encoding="utf-8"))

    def test_generated_reference_audit_reports_ok_and_missing_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            mod_root = Path(tmp) / "mod"
            self.assertEqual(generated_top_level_objects(mod_root)["scripted_trigger"], set())
            with patch.object(staid, "collect_object_names", return_value={}):
                self.assertEqual(collect_generated_reference_rows(mod_root, Path(tmp) / "snapshots"), [])
            ai_budget = mod_root / "common" / "ai_budget"
            triggers = mod_root / "common" / "scripted_triggers"
            values = mod_root / "common" / "script_values"
            ai_budget.mkdir(parents=True)
            triggers.mkdir(parents=True)
            values.mkdir(parents=True)
            (triggers / "triggers.txt").write_text("staid_generated_gate = { always = yes }\n", encoding="utf-8")
            (values / "values.txt").write_text("staid_generated_value = 5\n", encoding="utf-8")
            (ai_budget / "budget.txt").write_text(
                "test_budget = { "
                "resource = alloys "
                "has_deficit = missing_resource "
                "has_technology = known_tech "
                "has_technology = missing_tech "
                "staid_generated_gate = yes "
                "staid_missing_gate = yes "
                "stellarai_parent_gate = yes "
                "value = staid_generated_value "
                "add = staid_missing_value "
                "}\n",
                encoding="utf-8",
            )
            object_names = {
                "technology": {"known_tech"},
                "resource": {"alloys"},
                "scripted_trigger": {"stellarai_parent_gate"},
                "scripted_value": set(),
            }
            with patch.object(staid, "collect_object_names", return_value=object_names):
                rows = collect_generated_reference_rows(mod_root, Path(tmp) / "snapshots")
            by_key = {(row["reference_type"], row["reference_name"]): row for row in rows}
            self.assertEqual(generated_top_level_objects(mod_root)["scripted_trigger"], {"staid_generated_gate"})
            self.assertEqual(by_key[("technology", "known_tech")]["status"], "ok")
            self.assertEqual(by_key[("resource", "alloys")]["status"], "ok")
            self.assertEqual(by_key[("scripted_trigger", "staid_generated_gate")]["status"], "ok")
            self.assertEqual(by_key[("scripted_trigger", "stellarai_parent_gate")]["status"], "ok")
            self.assertEqual(by_key[("scripted_value", "staid_generated_value")]["status"], "ok")
            self.assertEqual(by_key[("technology", "missing_tech")]["status"], "missing")
            self.assertEqual(by_key[("resource", "missing_resource")]["status"], "missing")
            self.assertEqual(by_key[("scripted_trigger", "staid_missing_gate")]["status"], "missing")
            self.assertEqual(by_key[("scripted_value", "staid_missing_value")]["status"], "missing")
            report = generated_reference_report_text(rows)
            self.assertIn("scripted_trigger", report)
            self.assertIn("missing_tech", report)

    def test_generate_reference_audit_artifacts_writes_csv_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp)
            sample = [
                {
                    "reference_type": "technology",
                    "reference_name": "known_tech",
                    "source_key": "has_technology",
                    "generated_file": "common/ai_budget/test.txt",
                    "status": "ok",
                    "reason": "reference exists in source or generated inventory",
                }
            ]
            with patch.object(staid, "REFERENCE_AUDIT_CSV", research / "reference.csv"):
                with patch.object(staid, "REFERENCE_AUDIT_MD", research / "reference.md"):
                    with patch.object(staid, "collect_generated_reference_rows", return_value=sample):
                        rows = generate_reference_audit_artifacts()
            self.assertEqual(rows, sample)
            self.assertTrue((research / "reference.csv").exists())
            self.assertIn("known_tech", (research / "reference.md").read_text(encoding="utf-8"))

    def test_launch_validation_evidence_classifies_fresh_and_stale_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install = root / "install"
            logs = root / "logs"
            mod_root = root / "mod"
            (mod_root / "common" / "scripted_triggers").mkdir(parents=True)
            (mod_root / "common" / "ai_budget").mkdir(parents=True)
            (install).mkdir()
            logs.mkdir()
            exe = install / "stellaris.exe"
            exe.write_text("stub", encoding="utf-8")
            runtime = mod_root / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
            runtime.write_text("staid_survival_mode = { always = no }", encoding="utf-8")
            budget_runtime = mod_root / "common" / "ai_budget" / "zzz_staid_known_budget.txt"
            budget_runtime.write_text("known_budget = { resource = alloys }", encoding="utf-8")
            error_log = logs / "error.log"
            game_log = logs / "game.log"
            error_log.write_text(
                "Object with key: known_budget already exists, using the one at file: common/ai_budget/zzz_staid_known_budget.txt line: 5\n"
                "Error: missing staid_survival_mode in zzz_staid_decision_state_triggers.txt\n",
                encoding="utf-8",
            )
            game_log.write_text("Loaded Stellar AI Director\n", encoding="utf-8")
            os.utime(runtime, ns=(100, 100))
            os.utime(budget_runtime, ns=(100, 100))
            os.utime(error_log, ns=(200, 200))
            os.utime(game_log, ns=(200, 200))
            with patch.object(
                staid,
                "collect_generated_conflict_rows",
                return_value=[
                    {
                        "object_name": "known_budget",
                        "generated_file": "common/ai_budget/zzz_staid_known_budget.txt",
                        "classification": "intentional_director_override",
                    }
                ],
            ):
                evidence = collect_launch_validation_evidence(install, logs, mod_root, root / "missing-proof.json")
            self.assertTrue(evidence["game_executable_exists"])
            self.assertEqual(evidence["launch_evidence_status"], "fresh_logs_present")
            self.assertFalse(evidence["main_menu_proven"])
            self.assertEqual(evidence["logs"][0]["director_expected_line_count"], 1)
            self.assertEqual(evidence["logs"][0]["director_problem_line_count"], 1)
            self.assertEqual(evidence["logs"][0]["director_unclassified_line_count"], 0)
            self.assertEqual(evidence["logs"][1]["director_unclassified_line_count"], 1)
            report = launch_validation_report_text(evidence)
            self.assertIn("fresh_logs_present", report)
            self.assertIn("missing staid_survival_mode", report)

            os.utime(runtime, ns=(300, 300))
            with patch.object(staid, "collect_generated_conflict_rows", return_value=[]):
                stale = collect_launch_validation_evidence(install, logs, mod_root, root / "missing-proof.json")
            self.assertEqual(stale["launch_evidence_status"], "stale_or_missing_logs")

    def test_director_log_line_classifier_uses_intentional_override_registry(self):
        overrides = {("known_budget", "common/ai_budget/zzz_staid_known_budget.txt")}
        self.assertEqual(
            classify_director_log_line(
                "Object with key: known_budget already exists, using the one at file: common/ai_budget/zzz_staid_known_budget.txt line: 5",
                overrides,
            ),
            "expected_intentional_override",
        )
        self.assertEqual(classify_director_log_line("Error: missing staid_trigger", overrides), "problem")
        self.assertEqual(classify_director_log_line("Loaded Stellar AI Director", overrides), "unclassified")

    def test_director_log_summary_and_launch_comparison_are_generated_from_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mod_root = root / "mod"
            (mod_root / "common" / "ai_budget").mkdir(parents=True)
            (mod_root / "common" / "ai_budget" / "zzz_staid_known_budget.txt").write_text(
                "known_budget = { resource = alloys }",
                encoding="utf-8",
            )
            baseline_error = root / "baseline-error.log"
            baseline_game = root / "baseline-game.log"
            director_error = root / "director-error.log"
            director_game = root / "director-game.log"
            baseline_error.write_text("baseline parent warning only\n", encoding="utf-8")
            baseline_game.write_text("Game Version: Pegasus v4.4.4\n", encoding="utf-8")
            director_error.write_text(
                "Object with key: known_budget already exists, using the one at file: common/ai_budget/zzz_staid_known_budget.txt line: 5\n",
                encoding="utf-8",
            )
            director_game.write_text("Game Version: Pegasus v4.4.4\n", encoding="utf-8")
            overrides = {("known_budget", "common/ai_budget/zzz_staid_known_budget.txt")}
            missing_summary = collect_director_log_summary(root / "missing.log", {"staid_"}, overrides)
            self.assertFalse(missing_summary["exists"])
            with patch.object(
                staid,
                "collect_generated_conflict_rows",
                return_value=[
                    {
                        "object_name": "known_budget",
                        "generated_file": "common/ai_budget/zzz_staid_known_budget.txt",
                        "classification": "intentional_director_override",
                    }
                ],
            ):
                evidence = collect_launch_comparison_evidence(
                    baseline_error,
                    baseline_game,
                    director_error,
                    director_game,
                    mod_root,
                    root / "missing-proof.json",
                )
            self.assertEqual(evidence["baseline_director_match_count"], 0)
            self.assertEqual(evidence["with_director_match_count"], 1)
            self.assertEqual(evidence["with_director_expected_override_line_count"], 1)
            self.assertEqual(evidence["director_delta_status"], "expected_only")
            self.assertFalse(evidence["main_menu_proven"])
            report = launch_comparison_report_text(evidence)
            self.assertIn("expected_only", report)
            self.assertIn("known_budget", report)
            self.assertIn("does not yet prove", report)

    def test_main_menu_proof_marker_requires_confirmation_and_hashes_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            launcher = root / "launcher"
            logs = root / "logs"
            mod_root = root / "StellarAIDirector"
            dlc_load = root / "dlc_load.json"
            launcher.mkdir()
            logs.mkdir()
            mod_root.mkdir()
            (mod_root / "descriptor.mod").write_text(descriptor_text(), encoding="utf-8")
            (logs / "error.log").write_text("no director errors\n", encoding="utf-8")
            (logs / "game.log").write_text("main menu visible\n", encoding="utf-8")
            dlc_load.write_text('{"enabled_mods":["mod/parent.mod"]}', encoding="utf-8")
            self.assertIsNone(staid.file_sha256(logs / "missing.log"))
            with self.assertRaises(FileNotFoundError):
                staid.current_main_menu_mode(root / "missing-dlc-load.json")

            with self.assertRaises(PermissionError):
                collect_main_menu_proof_marker(
                    log_root=logs,
                    mod_root=mod_root,
                    launcher_mod_root=launcher,
                    dlc_load_path=dlc_load,
                    environment={},
                )

            marker = collect_main_menu_proof_marker(
                log_root=logs,
                mod_root=mod_root,
                launcher_mod_root=launcher,
                dlc_load_path=dlc_load,
                environment={staid.MAIN_MENU_CONFIRMATION_ENV: "yes"},
            )
            self.assertTrue(marker["confirmed"])
            self.assertEqual(marker["mode"], "baseline_without_director")
            self.assertEqual(len(marker["logs"]), 2)
            self.assertEqual(len(marker["logs"][0]["sha256"]), 64)
            self.assertFalse(marker["launcher_installation"]["enabled_in_dlc_load"])

            dlc_load.write_text('{"enabled_mods":["mod/StellarAIDirector.mod"]}', encoding="utf-8")
            director_marker = collect_main_menu_proof_marker(
                log_root=logs,
                mod_root=mod_root,
                launcher_mod_root=launcher,
                dlc_load_path=dlc_load,
                environment={staid.MAIN_MENU_CONFIRMATION_ENV: "YES"},
            )
            self.assertEqual(director_marker["mode"], "with_director")

    def test_record_main_menu_proof_marker_merges_required_modes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            logs = root / "logs"
            mod_root = root / "mod"
            dlc_load = root / "dlc_load.json"
            proof = root / "proof.json"
            logs.mkdir()
            mod_root.mkdir()
            (logs / "error.log").write_text("baseline errors\n", encoding="utf-8")
            (logs / "game.log").write_text("baseline game\n", encoding="utf-8")
            dlc_load.write_text('{"enabled_mods":["mod/parent.mod"]}', encoding="utf-8")

            status = record_main_menu_proof_marker(
                proof_path=proof,
                log_root=logs,
                mod_root=mod_root,
                launcher_mod_root=root / "launcher",
                dlc_load_path=dlc_load,
                environment={staid.MAIN_MENU_CONFIRMATION_ENV: "yes"},
            )
            self.assertFalse(status["main_menu_proven"])
            self.assertEqual(status["missing_modes"], ["with_director"])
            self.assertEqual(read_main_menu_proof_status(proof)["missing_modes"], ["with_director"])

            dlc_load.write_text('{"enabled_mods":["mod/StellarAIDirector.mod"]}', encoding="utf-8")
            status = record_main_menu_proof_marker(
                proof_path=proof,
                log_root=logs,
                mod_root=mod_root,
                launcher_mod_root=root / "launcher",
                dlc_load_path=dlc_load,
                environment={staid.MAIN_MENU_CONFIRMATION_ENV: "yes"},
            )
            self.assertTrue(status["main_menu_proven"])
            self.assertEqual(status["missing_modes"], [])
            self.assertIn("baseline_without_director", status["modes"])
            self.assertIn("with_director", read_main_menu_proof_status(proof)["main_menu_evidence"])
            self.assertTrue(merge_main_menu_proof_marker(status, {})["main_menu_proven"])

    def test_launch_comparison_uses_manual_main_menu_proof_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mod_root = root / "mod"
            (mod_root / "common" / "ai_budget").mkdir(parents=True)
            (mod_root / "common" / "ai_budget" / "zzz_staid_known_budget.txt").write_text(
                "known_budget = { resource = alloys }",
                encoding="utf-8",
            )
            baseline_error = root / "baseline-error.log"
            baseline_game = root / "baseline-game.log"
            director_error = root / "director-error.log"
            director_game = root / "director-game.log"
            for path in (baseline_error, baseline_game, director_error, director_game):
                path.write_text("Game Version: Pegasus v4.4.4\n", encoding="utf-8")
            proof = merge_main_menu_proof_marker(
                {},
                {"confirmed": True, "mode": "baseline_without_director", "timestamp_utc": "2026-07-04T00:00:00+00:00"},
            )
            proof = merge_main_menu_proof_marker(
                proof,
                {"confirmed": True, "mode": "with_director", "timestamp_utc": "2026-07-04T00:01:00+00:00"},
            )
            write_json(root / "proof.json", proof)

            evidence = collect_launch_comparison_evidence(
                baseline_error,
                baseline_game,
                director_error,
                director_game,
                mod_root,
                root / "proof.json",
                "irony_launcher",
            )
            self.assertEqual(evidence["launch_surface"], "irony_launcher")
            self.assertTrue(evidence["main_menu_proven"])
            self.assertIn("manual main-menu proof markers recorded", launch_comparison_report_text(evidence))

    def test_launch_comparison_artifact_gate_verifies_p14_when_clean_and_proven(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            research = root / "research" / "stellar-ai"
            research.mkdir(parents=True)
            self.assertFalse(launch_comparison_artifact_passes(root))
            comparison = {
                "launch_surface": "direct_executable_probe",
                "director_delta_status": "expected_only",
                "main_menu_proven": True,
                "with_director_problem_line_count": 0,
                "with_director_unclassified_line_count": 0,
            }
            write_json(research / "stellar-ai-director-launch-comparison-2026-07-04.json", comparison)
            self.assertFalse(launch_comparison_artifact_passes(root))
            self.assertEqual(
                classify_plan_phase_status(
                    "P14",
                    [{"path": "comparison.json", "exists": True, "size_bytes": 2}],
                    [],
                    {"main_menu_proven": True},
                    "",
                    root,
                ),
                "superseded",
            )
            report = launch_comparison_report_text(
                {
                    "launch_surface": "direct_executable_probe",
                    "baseline_logs": [],
                    "with_director_logs": [],
                    "baseline_director_match_count": 0,
                    "with_director_match_count": 4,
                    "with_director_problem_line_count": 0,
                    "with_director_unclassified_line_count": 0,
                    "with_director_expected_override_line_count": 4,
                    "director_delta_status": "expected_only",
                    "main_menu_proven": True,
                    "main_menu_evidence": "manual main-menu proof markers recorded",
                }
            )
            self.assertIn("direct_executable_probe", report)
            self.assertIn("not an Irony or launcher-resolved playset launch", report)

            comparison["launch_surface"] = "irony_launcher"
            write_json(research / "stellar-ai-director-launch-comparison-2026-07-04.json", comparison)
            self.assertTrue(launch_comparison_artifact_passes(root))
            self.assertEqual(
                classify_plan_phase_status(
                    "P14",
                    [{"path": "comparison.json", "exists": True, "size_bytes": 2}],
                    [],
                    {"main_menu_proven": True},
                    "",
                    root,
                ),
                "superseded",
            )
            report = launch_comparison_report_text(
                {
                    "launch_surface": "irony_launcher",
                    "baseline_logs": [],
                    "with_director_logs": [],
                    "baseline_director_match_count": 0,
                    "with_director_match_count": 4,
                    "with_director_problem_line_count": 0,
                    "with_director_unclassified_line_count": 0,
                    "with_director_expected_override_line_count": 4,
                    "director_delta_status": "expected_only",
                    "main_menu_proven": True,
                    "main_menu_evidence": "manual main-menu proof markers recorded",
                }
            )
            self.assertIn("P14 launch validation is satisfied", report)

            comparison["with_director_problem_line_count"] = 1
            write_json(research / "stellar-ai-director-launch-comparison-2026-07-04.json", comparison)
            self.assertFalse(launch_comparison_artifact_passes(root))

    def test_irony_order_comparison_allows_only_director_insertion(self):
        before = [
            {"steam_id": "1", "name": "First", "path": "a"},
            {"steam_id": "2", "name": "Second", "path": "b"},
        ]
        after = [
            {"steam_id": "1", "name": "First", "path": "a"},
            {"steam_id": "2", "name": "Second", "path": "b"},
            {"steam_id": "", "name": "Stellar AI Director", "path": "mods/StellarAIDirector"},
        ]
        self.assertEqual(compare_irony_order_with_director(before, after)["status"], "ok")
        reordered = [after[1], after[0], after[2]]
        result = compare_irony_order_with_director(before, reordered)
        self.assertEqual(result["status"], "fail")
        self.assertFalse(result["existing_mod_order_preserved"])

    def test_append_director_to_selected_irony_collection_preserves_existing_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db = root / "Database_1.26.json"
            db.write_text(
                json.dumps(
                    [
                        {
                            "Name": "ModCollection",
                            "Value": [
                                {
                                    "Name": "selected",
                                    "IsSelected": True,
                                    "Mods": ["mod/ugc_1.mod", "mod/ugc_2.mod"],
                                    "ModIds": [
                                        {"ParadoxId": None, "SteamId": 1},
                                        {"ParadoxId": None, "SteamId": 2},
                                    ],
                                    "ModNames": ["First", "Second"],
                                    "ModPaths": ["a", "b"],
                                }
                            ],
                        }
                    ]
                ),
                encoding="utf-8",
            )
            result = append_director_to_selected_irony_collection(
                db,
                root / "mods" / "StellarAIDirector",
                root / "research",
            )
            self.assertEqual(result["status"], "updated")
            self.assertEqual(result["order_check"]["status"], "ok")
            data = json.loads(db.read_text(encoding="utf-8"))
            collection = data[0]["Value"][0]
            self.assertEqual(collection["ModNames"], ["First", "Second", "Stellar AI Director"])
            self.assertEqual(collection["Mods"][-1], "mod/StellarAIDirector.mod")
            self.assertEqual(collection["ModIds"][-1], {"ParadoxId": None, "SteamId": None})

    def test_irony_order_proof_requires_only_director_added_after_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            research = root / "research"
            mod_root = root / "mod"
            research.mkdir()
            mod_root.mkdir()
            (mod_root / "descriptor.mod").write_text(descriptor_text(), encoding="utf-8")
            before_mods = [
                {"steam_id": "3610149307", "name": "Stellar AI", "path": "a"},
                {"steam_id": "1595876588", "name": "!!!Universal Resource Patch [2.4+]", "path": "b"},
            ]
            before_snapshot = research / "irony-selected-collection-before-director-20260705T000000Z.json"
            write_json(before_snapshot, {"collection_name": "selected", "mods": before_mods})
            playset = {
                "collection_name": "selected",
                "mods": [
                    {"steam_id": "3610149307", "name": "Stellar AI", "path": "a", "position": 1},
                    {"steam_id": "1121692237", "name": "Gigastructural Engineering & More (4.4)", "path": "g", "position": 2},
                    {"steam_id": "683230077", "name": "NSC3", "path": "n", "position": 3},
                    {"steam_id": "2648658105", "name": "Extra Ship Components NEXT", "path": "e", "position": 4},
                    {"steam_id": "3250900527", "name": "Starbase Extended 3.0", "path": "s", "position": 5},
                    {"steam_id": "1595876588", "name": "!!!Universal Resource Patch [2.4+]", "path": "b", "position": 6},
                    {"steam_id": "", "name": "Stellar AI Director", "path": "mods/StellarAIDirector", "position": 7},
                ],
            }
            before_mods[:] = [row for row in playset["mods"][:-1]]
            write_json(before_snapshot, {"collection_name": "selected", "mods": before_mods})
            proof = collect_irony_order_proof(before_snapshot, playset, mod_root, research)
            self.assertEqual(proof["status"], "ok")
            self.assertEqual(proof["director_position"], 7)
            self.assertIn("existing_mod_order_preserved: True", irony_order_proof_report_text(proof))

            with patch.object(staid, "RESEARCH_ROOT", root / "research" / "stellar-ai"):
                with patch.object(staid, "collect_irony_order_proof", return_value=proof):
                    self.assertEqual(generate_irony_order_proof_artifacts()["status"], "ok")
            self.assertTrue(irony_order_proof_artifact_passes(root))
            self.assertEqual(
                classify_plan_phase_status(
                    "P2",
                    [{"path": "proof.json", "exists": True, "size_bytes": 2}],
                    [],
                    {"main_menu_proven": False},
                    "",
                    root,
                ),
                "verified",
            )

            reordered = dict(playset)
            reordered["mods"] = [playset["mods"][1], playset["mods"][0], *playset["mods"][2:]]
            failed = collect_irony_order_proof(before_snapshot, reordered, mod_root, research)
            self.assertEqual(failed["status"], "fail")
            self.assertFalse(failed["order_check"]["existing_mod_order_preserved"])

    def test_irony_conflict_scan_artifact_requires_reviewed_analyze_only_conflicts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            research = root / "research" / "stellar-ai"
            research.mkdir(parents=True)
            reviewed_objects = [
                "alloys_expenditure_megastructures",
                "negative_mass_expenditure_megastructures",
                "sentient_metal_expenditure_megastructures",
                "supertensiles_upkeep_megastructures",
            ]
            scan_text = (
                "# Stellar AI Director Irony Conflict Scan\n\n"
                "Surface: Irony Conflict Solver Analyze Only.\n"
                "Collection: 4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity.\n"
                "Filter: common\\ai_budget.\n"
                "Conflict Count: 3000.\n"
                "Load order: !!!Universal Resource Patch [2.4+] at 116, Stellar AI Director at 117.\n"
                "Resolution: Stellar AI Director ... (LIOS) is an intentional Director win.\n"
                "No unexplained Director gameplay conflicts were observed.\n"
                + "\n".join(f"- {object_name}" for object_name in reviewed_objects)
            )
            (research / "stellar-ai-director-irony-conflict-scan-2026-07-04.md").write_text(
                scan_text,
                encoding="utf-8",
            )
            (research / "stellar-ai-director-irony-order-proof-2026-07-04.md").write_text(
                "Status: ok\nDirector position: 117\nLatest dependency position: 116\nexisting_mod_order_preserved: True\n",
                encoding="utf-8",
            )
            write_csv(
                research / "stellar-ai-director-generated-conflicts-2026-07-04.csv",
                [
                    {
                        "object_type": "ai_budget",
                        "object_name": object_name,
                        "classification": "intentional_director_override",
                    }
                    for object_name in reviewed_objects
                ],
            )
            self.assertTrue(irony_conflict_scan_artifact_passes(root))
            self.assertEqual(
                classify_plan_phase_status(
                    "P13",
                    [{"path": "scan.md", "exists": True, "size_bytes": 2}],
                    [],
                    {"main_menu_proven": True},
                    "",
                    root,
                ),
                "verified",
            )

            (research / "stellar-ai-director-irony-conflict-scan-2026-07-04.md").write_text(
                scan_text.replace("supertensiles_upkeep_megastructures", ""),
                encoding="utf-8",
            )
            self.assertFalse(irony_conflict_scan_artifact_passes(root))

    def test_load_proof_contract_validates_connector_event_and_localization(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "common" / "on_actions").mkdir(parents=True)
            (root / "events").mkdir(parents=True)
            (root / "localisation" / "english").mkdir(parents=True)
            (root / "common" / "on_actions" / "zzz_staid_load_proof_on_actions.txt").write_text(
                "on_game_start_country = { events = { staid_load_proof.1 } }",
                encoding="utf-8",
            )
            (root / "events" / "zzz_staid_load_proof_events.txt").write_text(
                """
namespace = staid_load_proof
country_event = {
    id = staid_load_proof.1
    title = staid_load_proof.1.name
    desc = staid_load_proof.1.desc
    picture = GFX_evt_grand_speech
    show_sound = event_default
    is_triggered_only = yes
    fire_only_once = yes
    trigger = { is_ai = no }
    immediate = { log = "STELLAR_AI_DIRECTOR_LOAD_PROOF: loaded" }
    option = { name = staid_load_proof.1.a }
}
""",
                encoding="utf-8",
            )
            (root / "localisation" / "english" / "staid_load_proof_l_english.yml").write_bytes(
                b'\xef\xbb\xbfl_english:\n staid_load_proof.1.name:0 "Stellar AI Director Loaded"\n'
                b' staid_load_proof.1.desc:0 "Loaded."\n staid_load_proof.1.a:0 "Confirmed."\n'
            )
            self.assertEqual(collect_load_proof_contract(root)["status"], "ok")

            (root / "common" / "on_actions" / "zzz_staid_load_proof_on_actions.txt").write_text(
                "on_game_start_country = { events = { wrong_event.1 } }",
                encoding="utf-8",
            )
            result = collect_load_proof_contract(root)
            self.assertEqual(result["status"], "fail")
            self.assertTrue(any("does not reference staid_load_proof.1" in error for error in result["errors"]))

    def test_plan_completion_status_parses_and_classifies_current_evidence(self):
        plan_text = (
            "## Completion Checklist For V1\n\n"
            "- [ ] P0 Munch gate passes.\n"
            "- [ ] P14 Stellaris reaches main menu with the patch enabled.\n"
            "- [ ] P15 observer smoke test confirms at least one useful high-ROI AI path.\n"
        )
        self.assertEqual(
            extract_completion_checklist_items(plan_text),
            [
                {"phase": "P0", "requirement": "Munch gate passes"},
                {"phase": "P14", "requirement": "Stellaris reaches main menu with the patch enabled"},
                {"phase": "P15", "requirement": "observer smoke test confirms at least one useful high-ROI AI path"},
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = root / "plan.md"
            plan.write_text(plan_text, encoding="utf-8")
            (root / "research" / "stellar-ai").mkdir(parents=True)
            (root / "research" / "stellar-ai" / "stellar-ai-director-launch-comparison-2026-07-04.json").write_text(
                "{}\n",
                encoding="utf-8",
            )
            for relative in staid.PLAN_PHASE_EVIDENCE["P14"][:3]:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("generated\n", encoding="utf-8")
            observer = root / "mods" / "StellarAIDirector" / "notes" / "observer-test-log.md"
            observer.parent.mkdir(parents=True)
            observer.write_text("Observer test not run yet.\n", encoding="utf-8")
            for relative in staid.PLAN_PHASE_EVIDENCE["P15"][1:]:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("generated\n", encoding="utf-8")
            rows = plan_phase_artifact_rows("P14", root)
            self.assertTrue(rows[0]["exists"])
            for relative in staid.PLAN_PHASE_EVIDENCE["P5"]:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("generated\n", encoding="utf-8")
            p5_paths = [row["path"] for row in plan_phase_artifact_rows("P5", root)]
            self.assertIn("mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt", p5_paths)
            self.assertTrue(all(row["exists"] for row in plan_phase_artifact_rows("P5", root)))
            self.assertEqual(
                classify_plan_phase_status(
                    "P99",
                    [{"path": "missing.txt", "exists": False, "size_bytes": 0}],
                    [],
                    {"main_menu_proven": True},
                    "",
                ),
                "missing",
            )
            self.assertEqual(
                classify_plan_phase_status("P12", [], ["bad reference"], {"main_menu_proven": True}, ""),
                "failing",
            )
            self.assertEqual(
                classify_plan_phase_status("P99", [], [], {"main_menu_proven": True}, "observer complete"),
                "verified",
            )
            self.assertEqual(
                classify_plan_phase_status("P3", [], [], {"main_menu_proven": True}, "observer complete", root),
                "partial",
            )
            status = collect_plan_completion_status(
                plan_path=plan,
                repo_root=root,
                mod_root=root / "mods" / "StellarAIDirector",
                main_menu_proof_path=root / "missing-proof.json",
                validation_errors=[],
            )
            by_phase = {phase["phase"]: phase for phase in status["phases"]}
            self.assertEqual(status["overall_status"], "not_complete")
            self.assertEqual(by_phase["P0"]["status"], "missing")
            self.assertEqual(by_phase["P14"]["status"], "superseded")
            self.assertEqual(by_phase["P15"]["status"], "superseded")
            self.assertEqual(status["main_menu_missing_modes"], ["baseline_without_director", "with_director"])
            self.assertEqual(
                classify_plan_phase_status(
                    "P14",
                    [{"path": "comparison.json", "exists": True, "size_bytes": 2}],
                    [],
                    {"main_menu_proven": False},
                    "",
                    root,
                ),
                "superseded",
            )
            report = plan_completion_report_text(status)
            self.assertIn("Overall status: not_complete", report)
            self.assertIn("stellar-ai-director-launch-comparison-2026-07-04.json=present", report)

    def test_starbase_policy_artifact_passes_only_when_generated_contract_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            economy = root / "mods" / "StellarAIDirector" / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
            triggers = root / "mods" / "StellarAIDirector" / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
            tuning = root / "mods" / "StellarAIDirector" / "notes" / "tuning-notes.md"
            economy.parent.mkdir(parents=True)
            triggers.parent.mkdir(parents=True)
            tuning.parent.mkdir(parents=True)
            thresholds = {
                "prep_stockpile_alloys": 16000,
                "prep_income_alloys": 140,
                "commit_stockpile_alloys": 30000,
                "desired_base_alloys": 26000,
                "desired_mega_engineering_add": 52000,
                "desired_prep_add": 76000,
                "desired_commit_add": 110000,
                "shipyard_stockpile_alloys": 12000,
                "shipyard_income_alloys": 160,
                "eligible_roi_rows": 125,
            }
            economy.write_text(economic_plan_text(), encoding="utf-8")
            triggers.write_text(triggers_text(thresholds), encoding="utf-8")
            tuning.write_text(tuning_notes_text(thresholds), encoding="utf-8")
            self.assertTrue(starbase_policy_artifact_passes(root))
            tuning.write_text("# incomplete\n", encoding="utf-8")
            self.assertFalse(starbase_policy_artifact_passes(root))

    def test_shipyard_policy_artifact_passes_only_when_generated_contract_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            economy = root / "mods" / "StellarAIDirector" / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
            triggers = root / "mods" / "StellarAIDirector" / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
            tuning = root / "mods" / "StellarAIDirector" / "notes" / "tuning-notes.md"
            economy.parent.mkdir(parents=True)
            triggers.parent.mkdir(parents=True)
            tuning.parent.mkdir(parents=True)
            thresholds = {
                "prep_stockpile_alloys": 16000,
                "prep_income_alloys": 140,
                "commit_stockpile_alloys": 30000,
                "desired_base_alloys": 26000,
                "desired_mega_engineering_add": 52000,
                "desired_prep_add": 76000,
                "desired_commit_add": 110000,
                "shipyard_stockpile_alloys": 12000,
                "shipyard_income_alloys": 160,
                "eligible_roi_rows": 125,
            }
            economy.write_text(economic_plan_text(), encoding="utf-8")
            triggers.write_text(triggers_text(thresholds), encoding="utf-8")
            tuning.write_text(tuning_notes_text(thresholds), encoding="utf-8")
            self.assertTrue(shipyard_policy_artifact_passes(root))
            economy.write_text(economic_plan_text().replace("naval_cap = 200", ""), encoding="utf-8")
            self.assertFalse(shipyard_policy_artifact_passes(root))

    def test_planetary_capacity_policy_artifact_passes_only_with_no_building_reference_rationale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            economy = root / "mods" / "StellarAIDirector" / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
            triggers = root / "mods" / "StellarAIDirector" / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
            tuning = root / "mods" / "StellarAIDirector" / "notes" / "tuning-notes.md"
            economy.parent.mkdir(parents=True)
            triggers.parent.mkdir(parents=True)
            tuning.parent.mkdir(parents=True)
            thresholds = {
                "prep_stockpile_alloys": 16000,
                "prep_income_alloys": 140,
                "commit_stockpile_alloys": 30000,
                "desired_base_alloys": 26000,
                "desired_mega_engineering_add": 52000,
                "desired_prep_add": 76000,
                "desired_commit_add": 110000,
                "shipyard_stockpile_alloys": 12000,
                "shipyard_income_alloys": 160,
                "eligible_roi_rows": 125,
            }
            economy.write_text(economic_plan_text(), encoding="utf-8")
            triggers.write_text(triggers_text(thresholds), encoding="utf-8")
            tuning.write_text(tuning_notes_text(thresholds), encoding="utf-8")
            self.assertTrue(planetary_capacity_policy_artifact_passes(root))
            tuning.write_text(tuning_notes_text(thresholds).replace("No generated building/job references", "Building references exist"), encoding="utf-8")
            self.assertFalse(planetary_capacity_policy_artifact_passes(root))

    def test_nsc3_esc_policy_artifact_passes_requires_no_failed_audit_rows_and_rationale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            audit = root / "research" / "stellar-ai" / "stellar-ai-director-integration-policy-audit-2026-07-04.csv"
            tuning = root / "mods" / "StellarAIDirector" / "notes" / "tuning-notes.md"
            conflicts = root / "mods" / "StellarAIDirector" / "notes" / "conflicts.md"
            audit.parent.mkdir(parents=True)
            tuning.parent.mkdir(parents=True)
            conflicts.parent.mkdir(parents=True, exist_ok=True)
            write_csv(
                audit,
                [
                    {
                        "phase": "P11",
                        "status": "warning",
                        "priority_band": "nsc3_esc_parent_design_ai_preservation",
                        "object_name": "nsc_test_ship",
                    }
                ],
            )
            tuning.write_text(
                "## NSC3/ESC Design Policy\n\n"
                "Direct NSC3/ESC ship and component design overrides are deferred until observer evidence proves parent AI cannot use the new hulls or components.\n",
                encoding="utf-8",
            )
            conflicts.write_text(
                "## NSC3/ESC Design Policy\n\n"
                "Direct NSC3/ESC ship and component design overrides are deferred until observer evidence proves parent AI cannot use the new hulls or components.\n",
                encoding="utf-8",
            )
            self.assertTrue(nsc3_esc_policy_artifact_passes(root))
            write_csv(
                audit,
                [
                    {
                        "phase": "P11",
                        "status": "fail",
                        "priority_band": "nsc3_esc_parent_design_ai_preservation",
                        "object_name": "bad",
                    }
                ],
            )
            self.assertFalse(nsc3_esc_policy_artifact_passes(root))

    def test_unlock_priority_policy_artifact_passes_requires_valid_reference_audit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            economy = root / "mods" / "StellarAIDirector" / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
            triggers = root / "mods" / "StellarAIDirector" / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
            tuning = root / "mods" / "StellarAIDirector" / "notes" / "tuning-notes.md"
            reference_audit = root / "research" / "stellar-ai" / "stellar-ai-director-generated-reference-audit-2026-07-04.csv"
            economy.parent.mkdir(parents=True)
            triggers.parent.mkdir(parents=True)
            tuning.parent.mkdir(parents=True)
            reference_audit.parent.mkdir(parents=True)
            thresholds = {
                "prep_stockpile_alloys": 16000,
                "prep_income_alloys": 140,
                "commit_stockpile_alloys": 30000,
                "desired_base_alloys": 26000,
                "desired_mega_engineering_add": 52000,
                "desired_prep_add": 76000,
                "desired_commit_add": 110000,
                "shipyard_stockpile_alloys": 12000,
                "shipyard_income_alloys": 160,
                "eligible_roi_rows": 125,
            }
            economy.write_text(economic_plan_text(), encoding="utf-8")
            triggers.write_text(triggers_text(thresholds), encoding="utf-8")
            tuning.write_text(tuning_notes_text(thresholds), encoding="utf-8")
            write_csv(reference_audit, [{"reference_type": "technology", "reference_name": "tech_mega_engineering", "status": "ok"}])
            self.assertTrue(unlock_priority_policy_artifact_passes(root))
            write_csv(reference_audit, [{"reference_type": "technology", "reference_name": "missing_tech", "status": "missing"}])
            self.assertFalse(unlock_priority_policy_artifact_passes(root))

    def test_mega_giga_policy_artifact_passes_requires_ready_roi_and_no_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            alloy_budget = root / "mods" / "StellarAIDirector" / "common" / "ai_budget" / "zzz_staid_alloys_budget.txt"
            gigas_budget = root / "mods" / "StellarAIDirector" / "common" / "ai_budget" / "zzz_staid_gigas_resource_budgets.txt"
            economy = root / "mods" / "StellarAIDirector" / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
            tuning = root / "mods" / "StellarAIDirector" / "notes" / "tuning-notes.md"
            policy_audit = root / "research" / "stellar-ai" / "stellar-ai-director-integration-policy-audit-2026-07-04.csv"
            roi_quality = root / "research" / "stellar-ai" / "stellar-ai-director-roi-quality-audit-2026-07-04.csv"
            for path in (alloy_budget, gigas_budget, economy, tuning, policy_audit, roi_quality):
                path.parent.mkdir(parents=True, exist_ok=True)
            thresholds = {
                "prep_stockpile_alloys": 16000,
                "prep_income_alloys": 140,
                "commit_stockpile_alloys": 30000,
                "desired_base_alloys": 26000,
                "desired_mega_engineering_add": 52000,
                "desired_prep_add": 76000,
                "desired_commit_add": 110000,
                "shipyard_stockpile_alloys": 12000,
                "shipyard_income_alloys": 160,
                "eligible_roi_rows": 125,
            }
            alloy_budget.write_text(ai_budget_text(thresholds), encoding="utf-8")
            gigas_budget.write_text(gigas_resource_budget_text(), encoding="utf-8")
            economy.write_text(economic_plan_text(), encoding="utf-8")
            tuning.write_text(tuning_notes_text(thresholds), encoding="utf-8")
            write_csv(
                policy_audit,
                [{"phase": "P7", "status": "ready", "priority_band": "roi_driven_mega_giga_builds"}],
            )
            write_csv(roi_quality, [{"status": "ok", "check": "threshold_eligible_count"}])
            self.assertTrue(mega_giga_policy_artifact_passes(root))
            write_csv(roi_quality, [{"status": "fail", "check": "decision_eligible_cost"}])
            self.assertFalse(mega_giga_policy_artifact_passes(root))

    def test_roi_model_artifact_passes_requires_broad_parent_coverage_and_quality(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            research = root / "research" / "stellar-ai"
            research.mkdir(parents=True)
            roi = research / "stellar-ai-director-roi-matrix-2026-07-04.csv"
            market = research / "stellar-ai-director-market-values-2026-07-04.csv"
            quality = research / "stellar-ai-director-roi-quality-audit-2026-07-04.csv"
            report = research / "stellar-ai-director-roi-matrix-2026-07-04.md"
            required_objects = [
                "mega_shipyard_2",
                "mega_shipyard_3",
                "mega_shipyard_restored",
                "neutronium_gigaforge_3",
                "nidavellir_forge_4",
                "hrae_mc_4",
            ]
            roles = ["economy_multiplier", "research_multiplier", "fleet_production_sink"]
            rows = []
            for index in range(140):
                rows.append(
                    {
                        "mod_name": "Gigastructural Engineering & More (4.4)" if index < 139 else "NSC3",
                        "object_name": required_objects[index] if index < len(required_objects) else f"roi_object_{index}",
                        "decision_eligible": "yes",
                        "director_strategy_role": roles[index % len(roles)],
                        "data_quality": "resolved",
                        "build_cost_value": "1000.0",
                        "market_unpriced_resources": "unity=100" if index == 0 else "",
                    }
                )
            write_csv(roi, rows)
            write_csv(
                market,
                [
                    {"resource": "alloys"},
                    {"resource": "energy"},
                    {"resource": "minerals"},
                    {"resource": "consumer_goods"},
                ],
            )
            write_csv(quality, [{"status": "ok", "check": "decision_eligible_cost"}])
            report.write_text("Rows marked `decision_eligible = no` are kept for auditability.\n", encoding="utf-8")
            self.assertTrue(roi_model_artifact_passes(root))
            rows[0]["build_cost_value"] = "0.0"
            write_csv(roi, rows)
            self.assertFalse(roi_model_artifact_passes(root))

    def test_source_corpus_artifact_passes_requires_snapshots_indexes_and_munch_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            snapshot = root / "research" / "mod-source-snapshots" / "2026-07-04"
            note = root / "research" / "stellar-ai" / "stellar-ai-director-corpus-status-2026-07-04.md"
            snapshot.mkdir(parents=True)
            note.parent.mkdir(parents=True)
            parents = [
                "Stellar AI",
                "Gigastructural Engineering & More (4.4)",
                "NSC3",
                "Extra Ship Components NEXT",
                "Starbase Extended 3.0",
            ]
            write_csv(
                snapshot / "snapshot-manifest.csv",
                [{"name": name, "snapshot_path": f"C:/snapshot/{index}"} for index, name in enumerate(parents)],
            )
            write_csv(
                snapshot / "descriptor-inventory.csv",
                [{"name": name, "snapshot_path": f"C:/snapshot/{index}"} for index, name in enumerate(parents)],
            )
            required_dirs = [
                "ai_budget",
                "economic_plans",
                "megastructures",
                "technology",
                "ascension_perks",
                "traditions",
                "starbase_modules",
                "starbase_buildings",
                "buildings",
                "ship_sizes",
                "component_templates",
                "scripted_triggers",
                "script_values",
                "on_actions",
            ]
            object_rows = [{"second_dir": required_dirs[index % len(required_dirs)]} for index in range(35000)]
            write_csv(snapshot / "pdx-object-inventory.csv", object_rows)
            ai_rows = [
                {
                    "ai_weight": "1",
                    "economic_plan": "1",
                    "megastructure": "1",
                    "technology": "1",
                    "ship_size": "1",
                    "component": "1",
                    "starbase": "1",
                }
                for _ in range(1600)
            ]
            write_csv(snapshot / "ai-surface-inventory.csv", ai_rows)
            note.write_text(
                "JDocMunch repo `local/StellarisMods-docs-2026-07-04`; "
                "`verify_index` reported 0 drift, 0 missing, and 0 errors. "
                "JCodeMunch repo `local/StellarisMods-223b92bc`. "
                "JDataMunch indexed and validated. "
                "`pdx-object-inventory.csv`: 35991 rows. "
                "`ai-surface-inventory.csv`: 1696 rows.\n",
                encoding="utf-8",
            )
            self.assertTrue(source_corpus_artifact_passes(root))
            note.write_text("missing Munch evidence\n", encoding="utf-8")
            self.assertFalse(source_corpus_artifact_passes(root))

    def test_munch_preflight_artifact_passes_requires_all_guides_and_script_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            preflight = root / "research" / "stellar-ai" / "stellar-ai-director-munch-preflight-2026-07-04.md"
            preflight.parent.mkdir(parents=True)
            preflight.write_text(
                "`jdocmunch_guide` returned content. "
                "`jcodemunch_guide` returned content. "
                "`jdatamunch_guide` returned content. "
                "`MUNCH_PREFLIGHT_PASS`. "
                "Active-thread guide calls succeeded.\n",
                encoding="utf-8",
            )
            self.assertTrue(munch_preflight_artifact_passes(root))
            preflight.write_text("Only one guide returned content.\n", encoding="utf-8")
            self.assertFalse(munch_preflight_artifact_passes(root))

    def test_decision_tree_artifact_passes_requires_trigger_mapping_and_safe_tuning_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            triggers = root / "mods" / "StellarAIDirector" / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
            tuning = root / "mods" / "StellarAIDirector" / "notes" / "tuning-notes.md"
            triggers.parent.mkdir(parents=True)
            tuning.parent.mkdir(parents=True)
            thresholds = {
                "prep_stockpile_alloys": 16000,
                "prep_income_alloys": 140,
                "commit_stockpile_alloys": 30000,
                "desired_base_alloys": 26000,
                "desired_mega_engineering_add": 52000,
                "desired_prep_add": 76000,
                "desired_commit_add": 110000,
                "shipyard_stockpile_alloys": 12000,
                "shipyard_income_alloys": 160,
                "eligible_roi_rows": 125,
            }
            triggers.write_text(triggers_text(thresholds), encoding="utf-8")
            tuning.write_text(tuning_notes_text(thresholds), encoding="utf-8")
            self.assertTrue(decision_tree_artifact_passes(root))
            triggers.write_text(triggers_text(thresholds).replace("used_naval_capacity_percent < 1.05", ""), encoding="utf-8")
            self.assertFalse(decision_tree_artifact_passes(root))

    def test_generated_surface_artifact_passes_requires_valid_files_references_and_ownership(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            common = root / "mods" / "StellarAIDirector" / "common"
            research = root / "research" / "stellar-ai"
            tuning = root / "mods" / "StellarAIDirector" / "notes" / "tuning-notes.md"
            thresholds = {
                "prep_stockpile_alloys": 16000,
                "prep_income_alloys": 140,
                "commit_stockpile_alloys": 30000,
                "desired_base_alloys": 26000,
                "desired_mega_engineering_add": 52000,
                "desired_prep_add": 76000,
                "desired_commit_add": 110000,
                "shipyard_stockpile_alloys": 12000,
                "shipyard_income_alloys": 160,
                "eligible_roi_rows": 125,
            }
            generated_files = {
                "common/ai_budget/zzz_staid_alloys_budget.txt": ai_budget_text(thresholds),
                "common/ai_budget/zzz_staid_gigas_resource_budgets.txt": gigas_resource_budget_text(),
                "common/economic_plans/zzzz_staid_additive_economic_plan.txt": economic_plan_text(),
                "common/on_actions/zzz_staid_load_proof_on_actions.txt": "on_game_start_country = { events = { staid_load_proof.1 } }\n",
                "common/on_actions/zzz_staid_threat_response_on_actions.txt": staid.threat_response_on_actions_text(),
                "common/opinion_modifiers/zzz_staid_threat_response_opinions.txt": staid.threat_response_opinions_text(),
                "common/script_values/zzz_staid_roi_values.txt": script_values_text(thresholds),
                "common/script_values/zzz_staid_threat_response_values.txt": staid.threat_response_script_values_text(),
                "common/scripted_triggers/zzz_staid_decision_state_triggers.txt": triggers_text(thresholds),
                "common/scripted_triggers/zzz_staid_threat_response_triggers.txt": staid.threat_response_triggers_text(),
            }
            for relative, content in generated_files.items():
                path = common / relative.removeprefix("common/")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            tuning.parent.mkdir(parents=True)
            tuning.write_text(tuning_notes_text(thresholds), encoding="utf-8")
            research.mkdir(parents=True)
            write_csv(
                research / "stellar-ai-director-generated-file-audit-2026-07-04.csv",
                [{"generated_file": relative, "status": "ok"} for relative in generated_files],
            )
            write_csv(
                research / "stellar-ai-director-generated-reference-audit-2026-07-04.csv",
                [{"reference_type": "resource", "reference_name": "alloys", "status": "ok"}],
            )
            write_csv(
                research / "stellar-ai-director-generated-conflicts-2026-07-04.csv",
                [
                    {"classification": "additive_director_object"},
                    {"classification": "intentional_director_override"},
                ],
            )
            self.assertTrue(generated_surface_artifact_passes(root))
            write_csv(
                research / "stellar-ai-director-generated-reference-audit-2026-07-04.csv",
                [{"reference_type": "resource", "reference_name": "missing", "status": "missing"}],
            )
            self.assertFalse(generated_surface_artifact_passes(root))

    def test_validator_artifact_passes_requires_all_audits_clean_and_irony_order_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            research = root / "research" / "stellar-ai"
            research.mkdir(parents=True)
            write_csv(research / "stellar-ai-director-generated-file-audit-2026-07-04.csv", [{"status": "ok"}])
            write_csv(research / "stellar-ai-director-generated-reference-audit-2026-07-04.csv", [{"status": "ok"}])
            write_csv(
                research / "stellar-ai-director-generated-conflicts-2026-07-04.csv",
                [{"classification": "intentional_director_override"}],
            )
            write_csv(research / "stellar-ai-director-dependency-audit-2026-07-04.csv", [{"status": "ok"}])
            write_csv(research / "stellar-ai-director-roi-quality-audit-2026-07-04.csv", [{"status": "ok"}])
            write_csv(research / "stellar-ai-director-integration-policy-audit-2026-07-04.csv", [{"status": "ready"}])
            (research / "stellar-ai-director-irony-order-proof-2026-07-04.json").write_text("{}", encoding="utf-8")
            with patch.object(staid, "irony_order_proof_artifact_passes", return_value=True):
                self.assertTrue(validator_artifact_passes([], root))
                self.assertFalse(validator_artifact_passes(["bad reference"], root))

    def test_documentation_artifact_passes_requires_operator_facing_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = [
                root / "mods" / "StellarAIDirector" / "README.md",
                root / "mods" / "StellarAIDirector" / "notes" / "load-order.md",
                root / "mods" / "StellarAIDirector" / "notes" / "conflicts.md",
                root / "mods" / "StellarAIDirector" / "notes" / "observer-test-log.md",
                root / "mods" / "StellarAIDirector" / "notes" / "tuning-notes.md",
            ]
            content = (
                "Stellar AI Director Loaded. Irony load order validation. "
                "Gigastructural Engineering & More (4.4), Extra Ship Components NEXT, NSC3, "
                "!!!Universal Resource Patch [2.4+]. Stellar AI Director validation, intentional conflicts, "
                "tuning workflow, and observer workflow."
            )
            for path in docs:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            self.assertTrue(documentation_artifact_passes(root))
            docs[3].unlink()
            self.assertFalse(documentation_artifact_passes(root))

    def test_generate_plan_status_artifacts_writes_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp)
            sample = {
                "overall_status": "complete",
                "phase_count": 1,
                "validation_error_count": 0,
                "main_menu_proven": False,
                "main_menu_missing_modes": ["with_director"],
                "phases": [
                    {
                        "phase": "P14",
                        "status": "superseded",
                        "requirement": "Stellaris reaches main menu with the patch enabled",
                        "open_reason": "Superseded for this goal: user/runtime launch validation is intentionally out of scope.",
                        "artifacts": [{"path": "launch.json", "exists": True, "size_bytes": 2}],
                    }
                ],
            }
            with patch.object(staid, "PLAN_STATUS_JSON", research / "status.json"):
                with patch.object(staid, "PLAN_STATUS_MD", research / "status.md"):
                    with patch.object(staid, "collect_plan_completion_status", return_value=sample):
                        status = generate_plan_status_artifacts()
            self.assertEqual(status, sample)
            self.assertTrue((research / "status.json").exists())
            self.assertIn("runtime launch validation is intentionally out of scope", (research / "status.md").read_text(encoding="utf-8"))

    def test_generate_launch_comparison_artifacts_writes_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp)
            sample = {
                "baseline_logs": [],
                "with_director_logs": [],
                "baseline_director_match_count": 0,
                "with_director_match_count": 0,
                "with_director_problem_line_count": 0,
                "with_director_unclassified_line_count": 0,
                "with_director_expected_override_line_count": 0,
                "director_delta_status": "needs_review",
                "main_menu_proven": False,
                "main_menu_evidence": "manual marker required",
            }
            with patch.object(staid, "RESEARCH_ROOT", research):
                with patch.object(staid, "collect_launch_comparison_evidence", return_value=sample):
                    evidence = generate_launch_comparison_artifacts()
            self.assertEqual(evidence, sample)
            self.assertTrue((research / "stellar-ai-director-launch-comparison-2026-07-04.json").exists())
            report = (research / "stellar-ai-director-launch-comparison-2026-07-04.md").read_text(encoding="utf-8")
            self.assertIn("manual marker required", report)

    def test_generate_launch_validation_artifacts_writes_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp)
            sample = {
                "game_executable": "C:/Steam/steamapps/common/Stellaris/stellaris.exe",
                "game_executable_exists": True,
                "launcher_installation": {
                    "descriptor_path": "StellarAIDirector.mod",
                    "descriptor_exists": True,
                    "source_mod_path": "C:/repo/mods/StellarAIDirector",
                    "source_descriptor_exists": True,
                    "descriptor_points_to_source": True,
                    "descriptor_path_value": "C:/repo/mods/StellarAIDirector",
                    "dlc_load_path": "dlc_load.json",
                    "dlc_load_exists": True,
                    "enabled_mod_entry": "mod/StellarAIDirector.mod",
                    "enabled_in_dlc_load": True,
                },
                "runtime_file_count": 1,
                "latest_runtime_mtime_ns": 100,
                "logs": [
                    {
                        "name": "error.log",
                        "path": "error.log",
                        "exists": True,
                        "size_bytes": 0,
                        "mtime_ns": 200,
                        "newer_than_generated": True,
                        "director_line_count": 0,
                        "director_expected_line_count": 0,
                        "director_problem_line_count": 0,
                        "director_unclassified_line_count": 0,
                        "sample_director_lines": [],
                    }
                ],
                "launch_evidence_status": "fresh_logs_present",
                "main_menu_proven": False,
                "main_menu_evidence": "manual main-menu marker required",
            }
            with patch.object(staid, "RESEARCH_ROOT", research):
                with patch.object(staid, "collect_launch_validation_evidence", return_value=sample):
                    evidence = generate_launch_validation_artifacts()
            self.assertEqual(evidence, sample)
            self.assertTrue((research / "stellar-ai-director-launch-validation-2026-07-04.json").exists())
            report = (research / "stellar-ai-director-launch-validation-2026-07-04.md").read_text(encoding="utf-8")
            self.assertIn("manual main-menu marker required", report)

    def test_generate_mod_files_writes_all_runtime_and_research_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mod_root = root / "mod"
            research = root / "research"
            playset = {
                "collection_name": "Generated Test",
                "patch_mod_enabled": True,
                "mod_count": 1,
                "required_mods": {"1": {"name": "Parent", "present": True, "load_position": 1}},
            }
            with patch.object(staid, "MOD_ROOT", mod_root), patch.object(staid, "RESEARCH_ROOT", research):
                with patch.object(staid, "build_active_playset_snapshot", return_value=playset):
                    with patch.object(staid, "generate_dependency_audit_artifacts", return_value=[]):
                        with patch.object(staid, "generate_file_audit_artifacts", return_value=[]):
                            with patch.object(staid, "generate_conflict_classification_artifacts", return_value=[]):
                                with patch.object(staid, "generate_reference_audit_artifacts", return_value=[]):
                                    with patch.object(staid, "generate_launch_validation_artifacts", return_value={}):
                                        staid.generate_mod_files(self.sample_rows())
            self.assertTrue((mod_root / "descriptor.mod").exists())
            self.assertTrue((mod_root / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt").exists())
            self.assertTrue((mod_root / "common" / "scripted_triggers" / "zzz_staid_threat_response_triggers.txt").exists())
            self.assertTrue((mod_root / "common" / "script_values" / "zzz_staid_threat_response_values.txt").exists())
            self.assertTrue((mod_root / "common" / "opinion_modifiers" / "zzz_staid_threat_response_opinions.txt").exists())
            self.assertTrue((mod_root / "common" / "on_actions" / "zzz_staid_threat_response_on_actions.txt").exists())
            self.assertTrue((mod_root / "events" / "zzz_staid_threat_response_events.txt").exists())
            self.assertTrue((mod_root / "localisation" / "english" / "staid_threat_response_l_english.yml").exists())
            self.assertTrue((research / "stellar-ai-director-threat-response-feasibility-2026-07-05.md").exists())
            self.assertTrue((research / "stellar-ai-director-threat-response-war-goal-classification-2026-07-05.csv").exists())
            self.assertTrue((mod_root / "common" / "ai_budget" / "zzz_staid_gigas_resource_budgets.txt").exists())
            self.assertTrue((research / "stellar-ai-director-active-playset-2026-07-04.json").exists())
            self.assertIn("Generated Test", (mod_root / "README.md").read_text(encoding="utf-8"))
            self.assertTrue((mod_root / "notes" / "load-order.md").exists())
            self.assertTrue((mod_root / "notes" / "conflicts.md").exists())
            self.assertTrue((mod_root / "notes" / "observer-test-log.md").exists())
            self.assertTrue((mod_root / "notes" / "tuning-notes.md").exists())
            self.assertIn("Generated Test", (mod_root / "notes" / "load-order.md").read_text(encoding="utf-8"))

    def test_run_all_exits_when_validation_reports_errors(self):
        with patch.object(staid, "generate_roi_artifacts", return_value=self.sample_rows()):
            with patch.object(staid, "generate_mod_files") as generate:
                with patch.object(staid, "validate_generated_patch", return_value=["bad reference"]):
                    with self.assertRaises(SystemExit):
                        staid.run_all()
        generate.assert_called_once_with(self.sample_rows())

    def test_validate_generated_patch_reports_missing_files_and_bad_references(self):
        playset = {"required_mods": {"1": {"name": "Missing Parent", "present": False}}}
        objects = {
            "scripted_trigger": set(),
            "technology": {"known_tech"},
            "resource": {"alloys"},
            "ai_budget": {"known_budget"},
        }
        with tempfile.TemporaryDirectory() as tmp:
            mod_root = Path(tmp) / "StellarAIDirector"
            with patch.object(staid, "MOD_ROOT", mod_root):
                with patch.object(staid, "build_active_playset_snapshot", return_value=playset):
                    with patch.object(staid, "collect_object_names", return_value=objects):
                        errors = staid.validate_generated_patch()
            self.assertIn("No generated PDXScript files found", "\n".join(errors))

            budget_dir = mod_root / "common" / "ai_budget"
            budget_dir.mkdir(parents=True)
            (budget_dir / "bad_budget.txt").write_text(
                "bad_budget = { resource = missing_resource potential = { has_technology = missing_tech } }",
                encoding="utf-8",
            )
            (budget_dir / "known_collision.txt").write_text(
                "known_budget = { resource = alloys type = expenditure category = megastructures }",
                encoding="utf-8",
            )
            (budget_dir / "broken.txt").write_text("broken = {", encoding="utf-8")
            with patch.object(staid, "MOD_ROOT", mod_root):
                with patch.object(staid, "build_active_playset_snapshot", return_value={"required_mods": {}}):
                    with patch.object(staid, "collect_object_names", return_value=objects):
                        with patch.object(staid, "collect_roi_quality_rows", return_value=[]):
                            with patch.object(staid, "collect_integration_policy_audit_rows", return_value=[]):
                                errors = staid.validate_generated_patch()
            joined = "\n".join(errors)
            self.assertIn("broken.txt", joined)
            self.assertIn("lacks ownership note", joined)
            self.assertIn("Generated object collision lacks ownership note", joined)
            self.assertIn("does not override a known budget", joined)
            self.assertIn("missing technology reference missing_tech", joined)
            self.assertIn("missing resource reference missing_resource", joined)

    def test_validate_generated_patch_reports_roi_quality_failures(self):
        objects = {
            "scripted_trigger": set(),
            "technology": set(),
            "resource": {"alloys"},
            "ai_budget": {"known_budget"},
        }
        bad_roi = [
            {
                "status": "fail",
                "check": "decision_eligible_cost",
                "object_name": "bad_mega",
                "reason": "bad_mega is decision-eligible with non-positive build_cost_value=0.0",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            mod_root = Path(tmp) / "StellarAIDirector"
            budget_dir = mod_root / "common" / "ai_budget"
            budget_dir.mkdir(parents=True)
            (budget_dir / "known_budget.txt").write_text(
                "# Full-object override\nknown_budget = { resource = alloys }",
                encoding="utf-8",
            )
            with patch.object(staid, "MOD_ROOT", mod_root):
                with patch.object(staid, "build_active_playset_snapshot", return_value={"required_mods": {}}):
                    with patch.object(staid, "collect_object_names", return_value=objects):
                        with patch.object(staid, "collect_roi_quality_rows", return_value=bad_roi):
                            with patch.object(staid, "collect_integration_policy_audit_rows", return_value=[]):
                                errors = staid.validate_generated_patch()
        self.assertIn("ROI quality audit failed for decision_eligible_cost bad_mega", "\n".join(errors))

    def test_validate_generated_patch_reports_integration_policy_failures(self):
        objects = {
            "scripted_trigger": set(),
            "technology": set(),
            "resource": {"alloys"},
            "ai_budget": {"known_budget"},
        }
        bad_policy = [
            {
                "status": "fail",
                "phase": "P6",
                "object_type": "technology",
                "object_name": "missing_tech",
                "reason": "referenced source file does not exist",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            mod_root = Path(tmp) / "StellarAIDirector"
            budget_dir = mod_root / "common" / "ai_budget"
            budget_dir.mkdir(parents=True)
            (budget_dir / "known_budget.txt").write_text(
                "# Full-object override\nknown_budget = { resource = alloys }",
                encoding="utf-8",
            )
            with patch.object(staid, "MOD_ROOT", mod_root):
                with patch.object(staid, "build_active_playset_snapshot", return_value={"required_mods": {}}):
                    with patch.object(staid, "collect_object_names", return_value=objects):
                        with patch.object(staid, "collect_roi_quality_rows", return_value=[]):
                            with patch.object(staid, "collect_integration_policy_audit_rows", return_value=bad_policy):
                                errors = staid.validate_generated_patch()
        self.assertIn("Integration policy audit failed for P6 technology missing_tech", "\n".join(errors))

    def test_collect_object_names_skips_missing_common_bad_files_and_variables(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            no_common = root / "no-common"
            no_common.mkdir()
            source = root / "source"
            tech = source / "common" / "technology"
            tech.mkdir(parents=True)
            (tech / "bad.txt").write_text("broken = {", encoding="utf-8")
            (tech / "tech.txt").write_text("@ignored = 1\ntech_real = { cost = 1 }", encoding="utf-8")
            with patch.object(staid, "object_inventory_roots", return_value=[no_common, source]):
                names = staid.collect_object_names(root)
            self.assertIn("tech_real", names["technology"])
            self.assertNotIn("@ignored", names["technology"])

    def test_collect_object_names_reads_vanilla_branch_when_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake_vanilla = Path(tmp) / "vanilla-common"
            tech = fake_vanilla / "technology"
            tech.mkdir(parents=True)
            (tech / "bad.txt").write_text("broken = {", encoding="utf-8")
            (tech / "tech.txt").write_text("@ignored = 1\ntech_vanilla = { cost = 1 }", encoding="utf-8")

            def fake_path(value):
                if value == r"C:\Steam\steamapps\common\Stellaris\common":
                    return fake_vanilla
                return Path(value)

            with patch.object(staid, "object_inventory_roots", return_value=[]):
                with patch.object(staid, "Path", side_effect=fake_path):
                    names = staid.collect_object_names(Path(tmp))
            self.assertIn("tech_vanilla", names["technology"])
            self.assertNotIn("@ignored", names["technology"])

    def test_extract_megastructure_rows_skips_dummy_and_bad_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            giga = root / "1121692237-gigas"
            nsc = root / "683230077-nsc"
            for source in (giga, nsc):
                mega = source / "common" / "megastructures"
                mega.mkdir(parents=True)
                (mega / "dummy_megastructure.txt").write_text("dyson_dummy = { cost = { alloys = 1 } }", encoding="utf-8")
                (mega / "bad_megastructure.txt").write_text("dyson_bad = {", encoding="utf-8")
            (root / "snapshot-manifest.csv").write_text(
                "id,name,snapshot_path\n"
                f"1121692237,Gigas,{giga}\n"
                f"683230077,NSC3,{nsc}\n",
                encoding="utf-8",
            )
            rows = extract_megastructure_rows(root)
            self.assertEqual(rows, [])

    def test_irony_database_resolution_and_selected_collection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            db = root / "Database_test.json"
            db.write_text(
                json.dumps([
                    {
                        "Name": "ModCollection",
                        "Value": [
                            {
                                "Name": "Selected",
                                "IsSelected": True,
                                "ModIds": [{"SteamId": 1}],
                                "ModNames": ["Parent"],
                                "ModPaths": ["C:/mods/parent"],
                            }
                        ],
                    }
                ]),
                encoding="utf-8",
            )
            with patch.object(staid, "IRONY_DATA_ROOT", root):
                self.assertEqual(staid.resolve_irony_database(), db)
                collection = staid.selected_irony_collection()
            self.assertEqual(collection["Name"], "Selected")
            self.assertEqual(safe_mod_id(None), "")
            self.assertEqual(safe_mod_id(123), "123")

    def test_selected_collection_errors_when_no_selected_collection_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "Database.json"
            db.write_text(json.dumps([{"Name": "ModCollection", "Value": []}]), encoding="utf-8")
            with self.assertRaises(ValueError):
                staid.selected_irony_collection(db)
            with self.assertRaises(FileNotFoundError):
                with patch.object(staid, "IRONY_DATA_ROOT", Path(tmp) / "empty"):
                    staid.resolve_irony_database(Path(tmp) / "missing.json")
            with patch.object(staid, "resolve_irony_database", return_value=Path(tmp) / "deleted.json"):
                with self.assertRaises(FileNotFoundError):
                    staid.selected_irony_collection()


class ROIMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = extract_megastructure_rows()
        cls.by_name = {row["object_name"]: row for row in cls.rows}

    def test_gigas_mega_shipyard_extracts_capacity(self):
        matching = [row for row in self.rows if row["object_name"] == "mega_shipyard_3"]
        self.assertTrue(matching)
        self.assertGreaterEqual(max(row["shipyard_capacity"] for row in matching), 20)

    def test_nsc3_mega_shipyard_extracts_capacity_stages(self):
        capacities = [row["shipyard_capacity"] for row in self.rows if row["source_file"].endswith("11_mega_shipyard.txt")]
        self.assertIn(50, capacities)
        self.assertIn(75, capacities)
        self.assertIn(100, capacities)

    def test_nsc3_mega_shipyard_has_strategic_throughput_without_source_ai_weight(self):
        rows = [
            row
            for row in self.rows
            if row["object_name"] == "mega_shipyard_3"
            and row["source_file"].endswith("11_mega_shipyard.txt")
        ]
        self.assertTrue(rows)
        row = rows[0]
        self.assertEqual(row["source_has_ai_weight"], False)
        self.assertEqual(row["strategic_shipyard_effective_slots"], 200.0)
        self.assertEqual(row["strategic_shipyard_annual_alloy_throughput"], 90000.0)
        self.assertEqual(row["strategic_shipyard_annual_fleet_value_energy"], 1800000.0)
        self.assertEqual(row["strategic_shipyard_payback_years"], 0.11)
        self.assertEqual(row["priority_tier"], "shipyard_multiplier")
        self.assertEqual(row["director_strategy_role"], "fleet_production_sink")
        self.assertEqual(row["director_weight_basis"], "strategic_shipyard_throughput")
        self.assertEqual(
            row["director_build_gate"],
            "after_research_sink_when_alloy_energy_surplus_needs_fleet_sink",
        )
        self.assertEqual(row["director_surplus_sink_role"], "fleet_sink")
        self.assertEqual(row["director_surplus_sink_priority"], 2)

    def test_roi_rows_do_not_expose_ambiguous_has_ai_weight_column(self):
        self.assertNotIn("has_ai_weight", self.rows[0])

    def test_gigaforge_nidavellir_hrae_are_present(self):
        names = " ".join(self.by_name)
        self.assertIn("neutronium_gigaforge", names)
        self.assertIn("nidavellir", names)
        self.assertIn("hrae", names)

    def test_gigas_ai_savings_dynamic_costs_are_extracted(self):
        rows = [
            row
            for row in self.rows
            if row["object_name"] == "neutronium_gigaforge_0"
            and row["source_file"].endswith("zz_e_neutronium_gigaforge.txt")
        ]
        self.assertTrue(rows)
        self.assertGreater(rows[0]["build_cost_value"], 3000)

    def test_gigas_inline_script_alloy_costs_are_extracted(self):
        rows = [row for row in self.rows if row["object_name"] == "neutronium_gigaforge_2"]
        self.assertTrue(rows)
        self.assertGreater(rows[0]["build_cost_value"], 4000)

    def test_dyson_symbolic_variables_are_resolved(self):
        rows = [
            row
            for row in self.rows
            if row["object_name"] == "dyson_sphere_2"
            and row["source_file"].endswith("zz_e_dyson_sphere.txt")
        ]
        self.assertTrue(rows)
        self.assertGreater(rows[0]["build_cost_value"], 10000)
        self.assertGreater(rows[0]["annual_payoff_value"], 0)
        self.assertEqual(rows[0]["data_quality"], "resolved")

    def test_dyson_scaling_wrappers_are_resolved_from_templates(self):
        rows = [row for row in self.rows if row["object_name"] == "dyson_sphere_2_b_star"]
        self.assertTrue(rows)
        self.assertGreater(rows[0]["build_cost_value"], 25000)
        self.assertGreater(rows[0]["annual_payoff_value"], 0)
        self.assertEqual(rows[0]["data_quality"], "resolved")
        self.assertEqual(rows[0]["decision_eligible"], "yes")

    def test_dyson_stage_one_wrapper_has_real_cost(self):
        row = self.by_name["dyson_sphere_1_b_star"]
        self.assertIn("alloys=25000", row["cost"])
        self.assertGreater(row["build_cost_value"], 30000)
        self.assertEqual(row["data_quality"], "resolved")
        self.assertEqual(row["decision_eligible"], "yes")

    def test_disabled_dyson_site_wrapper_is_not_decision_eligible(self):
        row = self.by_name["dyson_sphere_0_b_star"]
        self.assertEqual(row["build_cost_value"], 0)
        self.assertEqual(row["decision_eligible"], "no")

    def test_most_roi_rows_are_resolved_after_inline_expansion(self):
        unresolved = [row for row in self.rows if row["decision_eligible"] == "yes" and row["data_quality"] != "resolved"]
        self.assertEqual(unresolved, [])
        self.assertGreaterEqual(len([row for row in self.rows if row["decision_eligible"] == "yes"]), 120)

    def test_generated_thresholds_use_resolved_eligible_rows(self):
        thresholds = generated_thresholds(self.rows)
        self.assertGreaterEqual(thresholds["eligible_roi_rows"], 120)
        self.assertGreaterEqual(thresholds["prep_stockpile_alloys"], 15000)
        self.assertGreaterEqual(thresholds["desired_commit_add"], thresholds["desired_prep_add"])

    def test_market_values_extract_alloy_base_and_ceiling(self):
        prices = {row["resource"]: row for row in market_price_rows()}
        self.assertEqual(prices["alloys"]["base_energy_per_unit"], 4.0)
        self.assertEqual(prices["alloys"]["max_buy_energy_per_unit_no_fee"], 20.0)
        self.assertEqual(prices["minerals"]["min_sell_energy_per_unit_no_fee"], 0.2)
        self.assertEqual(prices["alloys"]["ceiling_buy_energy_per_unit_default_fee"], 26.0)

    def test_market_stress_conversion_matches_mineral_to_alloy_concern(self):
        prices = {row["resource"]: row for row in market_price_rows()}
        minerals_per_alloy = (
            prices["alloys"]["max_buy_energy_per_unit_no_fee"]
            / prices["minerals"]["min_sell_energy_per_unit_no_fee"]
        )
        self.assertEqual(minerals_per_alloy, 100.0)

    def test_roi_rows_include_market_deficit_columns(self):
        row = self.by_name["dyson_sphere_5_o_star"]
        self.assertEqual(row["market_deficit_cost_energy"], 900000.0)
        self.assertEqual(row["market_deficit_annual_payoff_energy"], 240000.0)
        self.assertEqual(row["market_deficit_payback_years"], 3.75)

    def test_unpriced_gigas_resources_are_preserved(self):
        row = self.by_name["matrioshka_brain_1_b_star"]
        self.assertIn("unity=25000", row["market_unpriced_resources"])
        self.assertIn("physics_research=125", row["market_unpriced_resources"])


class DecisionTreeTests(unittest.TestCase):
    def test_stable_rich_empire_chooses_investment_prep(self):
        state = EmpireState(
            has_megastructure_prereqs=True,
            incomes={"alloys": 150, "energy": 150, "minerals": 100},
            stockpiles={"alloys": 20000},
            used_naval_capacity_percent=0.9,
        )
        self.assertEqual(choose_decision_state(state), "investment_prep_mode")

    def test_weak_empire_enters_recovery(self):
        state = EmpireState(incomes={"energy": -5, "minerals": 20, "alloys": 20}, stockpiles={"energy": 2000})
        self.assertEqual(choose_decision_state(state), "recovery_mode")

    def test_short_runway_deficit_enters_survival(self):
        state = EmpireState(incomes={"energy": -100, "alloys": 10}, stockpiles={"energy": 500})
        self.assertEqual(choose_decision_state(state), "survival_mode")

    def test_war_during_prep_pauses_investment(self):
        state = EmpireState(
            at_war=True,
            used_naval_capacity_percent=0.6,
            has_megastructure_prereqs=True,
            incomes={"alloys": 180, "energy": 180, "minerals": 100},
            stockpiles={"alloys": 30000},
        )
        self.assertEqual(choose_decision_state(state), "recovery_mode")

    def test_near_complete_project_can_continue_when_safe(self):
        state = EmpireState(
            at_war=True,
            used_naval_capacity_percent=0.9,
            project_progress=0.8,
            incomes={"alloys": 50, "energy": 50, "minerals": 50},
            stockpiles={"alloys": 10000, "energy": 10000},
        )
        self.assertEqual(choose_decision_state(state), "investment_commit_mode")

    def test_lost_half_economy_enters_survival(self):
        state = EmpireState(lost_economy_fraction=0.5, incomes={"alloys": 80}, stockpiles={"alloys": 10000})
        self.assertEqual(choose_decision_state(state), "survival_mode")

    def test_completed_shipyard_needs_alloy_support(self):
        state = EmpireState(has_completed_shipyard_multiplier=True, incomes={"alloys": 40, "energy": 200})
        self.assertEqual(choose_decision_state(state), "recovery_mode")

    def test_completed_shipyard_triggers_payoff_when_supported(self):
        state = EmpireState(
            has_completed_shipyard_multiplier=True,
            incomes={"alloys": 200, "energy": 200},
            stockpiles={"alloys": 12000},
        )
        self.assertEqual(choose_decision_state(state), "payoff_exploitation_mode")

    def test_surplus_research_sink_takes_priority_before_fleet_sink(self):
        state = EmpireState(
            research_sink_available=True,
            wants_fleet_buildup=True,
            alloy_stockpile_near_cap=True,
            incomes={"alloys": 600, "energy": 500, "minerals": 100},
            stockpiles={"alloys": 90000},
            used_naval_capacity_percent=0.9,
        )
        self.assertEqual(choose_decision_state(state), "research_expansion_mode")

    def test_surplus_fleet_sink_does_not_require_shipyard_bottleneck(self):
        state = EmpireState(
            shipyard_capacity_bottleneck=False,
            wants_fleet_buildup=True,
            alloy_stockpile_near_cap=True,
            incomes={"alloys": 350, "energy": 350, "minerals": 100},
            stockpiles={"alloys": 90000},
            used_naval_capacity_percent=0.9,
        )
        self.assertEqual(choose_decision_state(state), "shipyard_expansion_mode")

    def test_surplus_unity_sink_is_after_research_and_fleet(self):
        state = EmpireState(
            unity_sink_available=True,
            incomes={"alloys": 350, "energy": 350, "minerals": 100},
            stockpiles={"alloys": 25000},
            used_naval_capacity_percent=0.9,
        )
        self.assertEqual(choose_decision_state(state), "unity_expansion_mode")

    def test_legacy_shipyard_expansion_path_still_accepts_explicit_bottleneck(self):
        state = EmpireState(
            shipyard_capacity_bottleneck=True,
            wants_fleet_buildup=True,
            incomes={"alloys": 350, "energy": 350, "minerals": 100},
            stockpiles={"alloys": 25000},
            used_naval_capacity_percent=0.9,
        )
        self.assertEqual(choose_decision_state(state), "shipyard_expansion_mode")

    def test_surplus_with_fleet_signal_chooses_shipyard_without_bottleneck(self):
        state = EmpireState(
            shipyard_capacity_bottleneck=False,
            wants_fleet_buildup=True,
            incomes={"alloys": 350, "energy": 350, "minerals": 100},
            stockpiles={"alloys": 25000},
            used_naval_capacity_percent=0.9,
        )
        self.assertEqual(choose_decision_state(state), "shipyard_expansion_mode")

    def test_shipyard_expansion_not_chosen_without_surplus(self):
        state = EmpireState(
            shipyard_capacity_bottleneck=True,
            wants_fleet_buildup=True,
            incomes={"alloys": 120, "energy": 350, "minerals": 100},
            stockpiles={"alloys": 25000},
            used_naval_capacity_percent=0.9,
        )
        self.assertEqual(choose_decision_state(state), "normal_growth_mode")


class ThreatResponseTests(unittest.TestCase):
    def test_threat_response_ethic_vectors_and_fanatic_ratio_are_stable(self):
        self.assertEqual(
            staid.THREAT_RESPONSE_AXES,
            (
                "moral_outrage",
                "regional_fear",
                "shared_threat_cooperation",
                "conquest_respect",
                "punitive_pressure",
                "defensive_readiness",
                "opportunism",
            ),
        )
        normal = {row["ethic"]: row for row in staid.threat_normal_ethic_rows()}
        fanatic = {row["ethic"]: row for row in staid.threat_fanatic_ethic_rows()}
        for ethic, row in normal.items():
            fanatic_row = fanatic[ethic.replace("ethic_", "ethic_fanatic_", 1)]
            for axis in staid.THREAT_RESPONSE_AXES:
                self.assertEqual(fanatic_row[axis], row[axis] * staid.THREAT_FANATIC_MULTIPLIER)
        self.assertEqual(staid.THREAT_CIVIC_AXIS_CAP, 1)
        self.assertEqual(staid.THREAT_TOTAL_CIVIC_AXIS_CAP, 2)
        self.assertEqual(staid.axis_vector(staid.THREAT_GESTALT_VECTORS["homicidal"])["moral_outrage"], 0)

    def test_threat_scores_ranges_and_scenario_matrix_outputs(self):
        pacifist = staid.axis_vector(staid.THREAT_NORMAL_ETHIC_VECTORS["ethic_pacifist"])
        militarist_authoritarian = {
            axis: staid.axis_vector(staid.THREAT_NORMAL_ETHIC_VECTORS["ethic_militarist"])[axis]
            + staid.axis_vector(staid.THREAT_NORMAL_ETHIC_VECTORS["ethic_authoritarian"])[axis]
            for axis in staid.THREAT_RESPONSE_AXES
        }
        pacifist_scores = staid.threat_scores(pacifist, severity=2)
        conqueror_scores = staid.threat_scores(militarist_authoritarian, severity=2)
        self.assertGreaterEqual(pacifist_scores["anti_aggressor_score"], 45)
        self.assertGreater(conqueror_scores["alignment_with_aggressor_score"], pacifist_scores["alignment_with_aggressor_score"])
        for name, score in {**pacifist_scores, **conqueror_scores}.items():
            lower, upper = staid.THREAT_SCORE_LIMITS[name]
            self.assertGreaterEqual(score, lower)
            self.assertLessEqual(score, upper)

    def test_war_goal_classification_unknown_is_inert(self):
        self.assertEqual(staid.classify_threat_war_goal("wg_conquest")["severity"], 2)
        unknown = staid.classify_threat_war_goal("wg_unseen_mod_goal")
        self.assertEqual(unknown["severity"], 0)
        self.assertEqual(unknown["punitive_outputs_allowed"], "no")
        self.assertEqual(unknown["readiness_outputs_allowed"], "no")
        self.assertEqual(unknown["forced_war_allowed"], "no")
        self.assertEqual(unknown["status"], "unknown_inert")

    def test_third_party_threat_economy_pressure_is_capped_and_fail_closed(self):
        self.assertEqual(
            staid.third_party_threat_economy_pressure(foreign_affairs_safe=True, readiness_flag=True),
            {"alloys": 7, "energy": 6, "naval_cap": 40},
        )
        for blocked in ("at_war", "survival", "recovery", "deficit"):
            kwargs = {"foreign_affairs_safe": True, "readiness_flag": True, blocked: True}
            self.assertEqual(staid.third_party_threat_economy_pressure(**kwargs), {"alloys": 0, "energy": 0, "naval_cap": 0})
        self.assertEqual(
            staid.third_party_threat_economy_pressure(foreign_affairs_safe=False, readiness_flag=True),
            {"alloys": 0, "energy": 0, "naval_cap": 0},
        )
        for resource, value in staid.THREAT_ECONOMY_MAX.items():
            self.assertLessEqual(value, staid.THREAT_FLEET_RESERVE_BASE[resource] * staid.THREAT_ECONOMY_RATIO_CAP)

    def test_generated_threat_response_text_contains_required_contracts(self):
        triggers = staid.threat_response_triggers_text()
        events = staid.threat_response_events_text()
        economy = economic_plan_text()
        for term in (
            "NOT = { staid_core_deficit_short_runway = yes }",
            "NOT = { staid_survival_mode = yes }",
            "NOT = { staid_recovery_mode = yes }",
            "is_at_war = no",
            "has_communications = from",
        ):
            self.assertIn(term, triggers)
        self.assertIn("staid_tr_attacker_war_leader = yes", events)
        self.assertIn("staid_tr_war_goal_classified = yes", events)
        self.assertIn("remove_opinion_modifier", events)
        self.assertIn("add_opinion_modifier", events)
        for forbidden in staid.THREAT_FORBIDDEN_EFFECTS:
            self.assertNotIn(forbidden, events)
        self.assertIn("Stellar AI Director threat readiness reserve", economy)
        self.assertIn("alloys = 7", economy)
        self.assertIn("energy = 6", economy)
        self.assertIn("naval_cap = 40", economy)

    def test_validate_threat_response_contract_reports_seeded_breaks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mod_root = root / "StellarAIDirector"
            research = root / "research"
            with patch.object(staid, "MOD_ROOT", mod_root), patch.object(staid, "RESEARCH_ROOT", research):
                staid.generate_threat_response_artifacts()
                economy_path = mod_root / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
                economy_path.parent.mkdir(parents=True)
                economy_path.write_text(economic_plan_text(), encoding="utf-8")
                self.assertEqual(staid.validate_threat_response_contract(mod_root), [])
                events_path = mod_root / "events" / "zzz_staid_threat_response_events.txt"
                events_path.write_text(events_path.read_text(encoding="utf-8") + "\ndeclare_war = from\n", encoding="utf-8")
                errors = staid.validate_threat_response_contract(mod_root)
        self.assertIn("forbidden V1 effect: declare_war", "\n".join(errors))


class PatchValidationTests(unittest.TestCase):
    def test_generated_patch_validates_when_present(self):
        mod_root = Path("mods/StellarAIDirector/common")
        if not mod_root.exists():
            self.skipTest("generated mod has not been created yet")
        self.assertEqual(validate_generated_patch(), [])


if __name__ == "__main__":
    unittest.main()
