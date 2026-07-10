#!/usr/bin/env python3
"""Focused static validation for the Stellaris 4.4.4 native war-planning replacement."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

from stellar_ai_director_lib import (
    MOD_ROOT,
    REPO_ROOT,
    STANDALONE_AGGRESSION_PERSONALITY_VALUES,
    WAR_PLANNING_444_PROVENANCE_CSV,
    army_recruitment_budget_text,
    extract_top_level_object_text,
    high_scale_ai_defines_text,
    minerals_planet_construction_budget_text,
    parse_file,
    strategy_kernel_triggers_text,
)


WAR_FILES = (
    "mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt",
    "mods/StellarAIDirector/common/ai_budget/zzzz_staid_14_army_recruitment_budget.txt",
    "mods/StellarAIDirector/common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt",
    "mods/StellarAIDirector/common/country_types/zzzzz_staid_18_native_war_readiness.txt",
    "mods/StellarAIDirector/common/defines/zzzz_staid_14_high_scale_ai_defines.txt",
    "mods/StellarAIDirector/common/personalities/zzzzz_staid_16_standalone_war_pressure.txt",
    "mods/StellarAIDirector/common/policies/zzzz_staid_10_opening_growth_policies.txt",
    "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt",
    "mods/StellarAIDirector/common/scripted_triggers/zzzz_staid_20_strategy_kernel_triggers.txt",
)

EXPECTED_PROVENANCE_IDS = {
    *STANDALONE_AGGRESSION_PERSONALITY_VALUES,
    "default",
    "diplomatic_stance",
    "orbital_bombardment",
    "orbital_bombardment_accept_surrender",
    "minerals_expenditure_armies",
    "minerals_expenditure_armies_threatened",
    "minerals_expenditure_planets_low",
    "minerals_expenditure_planets_med",
    "minerals_expenditure_planets_high",
    "alloys_expenditure_megastructures",
    "alloys_expenditure_ships",
    "alloys_expenditure_ship_upgrades",
    "NAI",
}

FORBIDDEN_EFFECT_ASSIGNMENTS = (
    "create_war",
    "create_army",
    "add_claim",
    "add_casus_belli",
    "add_resource",
    "set_mia",
    "set_fleet_stance",
    "set_fleet_order",
    "move_to",
)


def _read(relative: str) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8-sig")


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _validate_required_files(errors: list[str]) -> None:
    for relative in WAR_FILES:
        path = REPO_ROOT / relative
        _require(path.is_file(), f"missing required replacement file: {relative}", errors)
        if path.is_file():
            try:
                parse_file(path)
            except Exception as exc:  # noqa: BLE001 - validation must report every parser failure.
                errors.append(f"PDX parse failure in {relative}: {exc}")


def _validate_native_only(errors: list[str]) -> None:
    effect_re = re.compile(
        rf"(?mi)^\s*(?:{'|'.join(map(re.escape, FORBIDDEN_EFFECT_ASSIGNMENTS))})\s*="
    )
    for relative in WAR_FILES:
        text = _read(relative)
        match = effect_re.search(text)
        _require(match is None, f"state-mutating shortcut in {relative}: {match.group(0).strip() if match else ''}", errors)

    country_text = _read(WAR_FILES[3])
    # This is the country-type capability field, not a scripted declaration effect.
    _require(re.search(r"(?m)^\s*declare_war\s*=\s*yes\s*$", country_text) is not None,
             "default country type lost declare_war = yes capability", errors)


def _validate_country_type(errors: list[str]) -> None:
    text = _read(WAR_FILES[3])
    default = extract_top_level_object_text(text, "default")
    _require("min_navy_for_wars" not in default, "default country type still has min_navy_for_wars", errors)
    _require(re.search(r"(?m)^\s*min_assault_armies_for_wars\s*=\s*0\s*$", default) is not None,
             "default country type does not set min_assault_armies_for_wars = 0", errors)


def _validate_defines(errors: list[str]) -> None:
    relative = WAR_FILES[4]
    text = _read(relative)
    expected = {
        "AI_WAR_PREPARATION_MIN_MONTHS": "12",
        "AI_WAR_PREPARATION_MAX_MONTHS": "30",
        "AI_AGGRESSIVENESS_BASE": "25",
        "AI_AGGRESSIVENESS_PROPAGATOR_BOXED_IN_MULT": "12",
        "AI_AGGRESSIVENESS_BOXED_IN_MULT": "8",
        "AI_AGGRESSIVENESS_NO_COLONY_TARGET_MULT": "2",
        "ENEMY_FLEET_POWER_MULT": "1.2",
        "WAR_DECLARATION_MAX_DISTANCE": "50",
        "WAR_DECLARATION_MALUS_DISTANCE": "25",
        "WAR_DECLARATION_MALUS": "0.05",
        "WAR_DECLARATION_MINIMUM_SCORE": "0.5",
        "OFFENSE_VS_DEFENSE_STRATEGY_ALLOTMENT": "1.0",
        "AI_NAVAL_CAP_SCORE_MULT": "15",
    }
    for key, value in expected.items():
        _require(re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*{re.escape(value)}\s*$", text) is not None,
                 f"define mismatch: expected {key} = {value}", errors)
    for stale in (
        "AI_AGGRESSIVENESS_BASE = 50",
        "AI_AGGRESSIVENESS_BOXED_IN_MULT = 18",
        "ENEMY_FLEET_POWER_MULT = 0.55",
        "WAR_DECLARATION_MAX_DISTANCE = 200",
        "OFFENSE_VS_DEFENSE_STRATEGY_ALLOTMENT = 3.0",
        "AI_NAVAL_CAP_SCORE_MULT = 25",
    ):
        _require(stale not in text, f"obsolete contradictory war define remains: {stale}", errors)


def _validate_army_and_planet_budgets(errors: list[str]) -> None:
    army = _read(WAR_FILES[1])
    armies = extract_top_level_object_text(army, "minerals_expenditure_armies")
    threatened = extract_top_level_object_text(army, "minerals_expenditure_armies_threatened")
    _require("desired_min" in armies, "army budget has no native desired_min reserve", errors)
    _require("desired_max" not in armies and "desired_max" not in threatened,
             "army budget imposes a recruitment cap through desired_max", errors)
    _require("staid_boxed_in_war_pressure = yes" in armies,
             "army reserve has no boxed-in logistics pressure", errors)
    _require("is_at_war = yes" in armies, "army reserve has no wartime native budget lane", errors)
    _require("country_uses_bio_ships = no" not in army,
             "army budget still excludes biological-ship empires", errors)
    _require("min_assault_armies_for_wars" not in army,
             "army budget incorrectly encodes a declaration prerequisite", errors)

    planets = _read(WAR_FILES[2])
    for object_id, base in (
        ("minerals_expenditure_planets_low", "1.0"),
        ("minerals_expenditure_planets_med", "0.8"),
        ("minerals_expenditure_planets_high", "0.6"),
    ):
        block = extract_top_level_object_text(planets, object_id)
        _require(re.search(rf"(?m)^\s*weight\s*=\s*{re.escape(base)}\s*$", block) is not None,
                 f"{object_id} did not preserve vanilla base weight {base}", errors)
        _require("factor = 0.65 staid_war_logistics_pressure = yes" in block,
                 f"{object_id} does not yield budget share during war logistics", errors)
        _require("desired_min" not in block and "desired_max" not in block,
                 f"{object_id} reserves minerals through a competing desired_min/desired_max", errors)


def _validate_high_capacity_workaround(errors: list[str]) -> None:
    alloys = _read(WAR_FILES[0])
    ships = extract_top_level_object_text(alloys, "alloys_expenditure_ships")
    upgrades = extract_top_level_object_text(alloys, "alloys_expenditure_ship_upgrades")
    _require("staid_peacetime_high_naval_capacity_guard = yes" in ships,
             "ship budget is missing the 4.4.4 high-naval-capacity workaround", errors)
    _require("staid_emergency_fleet_spending_required = yes" in ships,
             "ship budget lost emergency bypass", errors)
    _require("staid_fleet_buildup_economy_safe = yes" in ships,
             "ship budget lost Director economy-safety gate", errors)
    _require("can_be_upgraded = yes" in upgrades,
             "ship-upgrade budget no longer checks for upgradeable fleets", errors)

    kernel = _read(WAR_FILES[8])
    guard = extract_top_level_object_text(kernel, "staid_peacetime_high_naval_capacity_guard")
    _require("used_naval_capacity_percent >= 0.80" in guard,
             "high-naval-capacity guard threshold is not 80 percent", errors)
    _require("is_at_war = no" in guard, "high-capacity guard is not peacetime-only", errors)
    _require("NOT = { staid_security_existential = yes }" in guard,
             "high-capacity guard does not clear for existential defense", errors)


def _validate_boxed_in_and_policy_exit(errors: list[str]) -> None:
    kernel = _read(WAR_FILES[8])
    boxed = extract_top_level_object_text(kernel, "staid_boxed_in_war_pressure")
    _require("has_ai_expansion_plan = no" in boxed, "boxed-in pressure is not tied to no expansion plan", errors)
    _require("has_ai_personality_behaviour = propagator" in boxed,
             "boxed-in pressure lost propagator behavior", errors)
    _require("has_ai_personality_behaviour = conqueror" in boxed,
             "boxed-in pressure lost conqueror behavior", errors)
    _require("has_ai_personality_behaviour = subjugator" in boxed,
             "boxed-in pressure lost subjugator behavior", errors)
    _require("has_ai_personality_behaviour = opportunist" in boxed,
             "boxed-in pressure lost opportunist behavior", errors)
    _require("num_owned_planets < 5" not in boxed,
             "obsolete small-empire cutoff still suppresses mature boxed-in empires", errors)

    policies = _read(WAR_FILES[6])
    diplomatic = extract_top_level_object_text(policies, "diplomatic_stance")
    for required in (
        "factor = 8 staid_boxed_in_war_pressure = yes",
        "factor = 0 staid_native_war_posture_active = yes",
        "factor = 0.25 staid_native_war_posture_active = yes",
        "factor = 6 staid_native_war_posture_active = yes",
    ):
        _require(required in diplomatic, f"diplomatic stance is missing native phase/boxed modifier: {required}", errors)
    _require("factor = 12 staid_opening_route_research_priority = yes" not in diplomatic,
             "obsolete long-lived 12x Cooperative research multiplier remains", errors)

    claims_triggers = _read(WAR_FILES[7])
    claim = extract_top_level_object_text(claims_triggers, "staid_boxed_in_claim_urgency")
    _require("staid_boxed_in_war_pressure = yes" in claim,
             "boxed-in claim urgency is not driven by the replacement pressure trigger", errors)
    _require("num_owned_planets < 5" not in claim,
             "boxed-in claim urgency still expires for mature empires", errors)


def _validate_personalities(errors: list[str]) -> None:
    text = _read(WAR_FILES[5])
    for object_id, aggression in STANDALONE_AGGRESSION_PERSONALITY_VALUES.items():
        block = extract_top_level_object_text(text, object_id)
        _require(re.search(rf"(?m)^\s*aggressiveness\s*=\s*{re.escape(f'{aggression:g}')}\s*$", block) is not None,
                 f"personality {object_id} lost working-reference aggressiveness {aggression:g}", errors)
        for field in ("bravery", "military_spending", "behaviour"):
            _require(re.search(rf"(?m)^\s*{field}\s*=", block) is not None,
                     f"personality {object_id} is missing required full-object field {field}", errors)
    for forbidden in ("create_war", "create_army", "add_casus_belli", "add_claim"):
        _require(forbidden not in text, f"personality output contains forbidden shortcut {forbidden}", errors)


def _validate_provenance(errors: list[str]) -> None:
    _require(WAR_PLANNING_444_PROVENANCE_CSV.is_file(),
             f"missing provenance CSV: {WAR_PLANNING_444_PROVENANCE_CSV.relative_to(REPO_ROOT)}", errors)
    if not WAR_PLANNING_444_PROVENANCE_CSV.is_file():
        return
    with WAR_PLANNING_444_PROVENANCE_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    actual_ids = {row["object_id"] for row in rows}
    _require(len(rows) == 33, f"expected 33 provenance rows, found {len(rows)}", errors)
    _require(EXPECTED_PROVENANCE_IDS == actual_ids,
             f"provenance object coverage mismatch; missing={sorted(EXPECTED_PROVENANCE_IDS-actual_ids)}, extra={sorted(actual_ids-EXPECTED_PROVENANCE_IDS)}", errors)
    for row in rows:
        _require(bool(row.get("pegasus_444_vanilla_source")),
                 f"provenance row lacks vanilla source: {row.get('object_id')}", errors)
        _require(bool(row.get("replacement_policy")),
                 f"provenance row lacks replacement policy: {row.get('object_id')}", errors)



def _validate_generator_and_docs(errors: list[str]) -> None:
    library = (REPO_ROOT / "tools" / "stellar_ai_director_lib.py").read_text(encoding="utf-8")
    generate_start = library.index("def generate_mod_files(")
    generate_end = library.index("\n\ndef war_planning_444_provenance_rows", generate_start)
    generate_block = library[generate_start:generate_end]
    _require("write_war_planning_444_provenance()" in generate_block,
             "main generator does not regenerate the 4.4.4 full-object provenance CSV", errors)

    readme_path = MOD_ROOT / "README.md"
    tuning_path = MOD_ROOT / "notes" / "tuning-notes.md"
    note_path = MOD_ROOT / "notes" / "war-planning-444-working-solution.md"
    for path in (readme_path, tuning_path, note_path):
        _require(path.is_file(), f"missing generated/documentation file: {path.relative_to(REPO_ROOT)}", errors)
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        for marker in (
            "working Stellar AI 0.10",
            "sub-40-year peaceful opening",
            "modest uncapped reserve",
            "ship spending pauses at 80% used capacity",
            "validate_staid_444_war_solution.py",
        ):
            _require(marker in readme, f"README is missing replacement-system marker: {marker}", errors)
    if tuning_path.is_file():
        tuning = tuning_path.read_text(encoding="utf-8")
        for stale in (
            "AI_AGGRESSIVENESS_BASE = 50",
            "ENEMY_FLEET_POWER_MULT = 0.55",
            "range at 200",
        ):
            _require(stale not in tuning, f"tuning notes retain obsolete war value: {stale}", errors)
        for marker in (
            "0.80 used naval capacity",
            "200 minerals base; +300 boxed",
            "12–30 months",
        ):
            _require(marker in tuning, f"tuning notes are missing replacement marker: {marker}", errors)

def _validate_deterministic_source_matches(errors: list[str]) -> None:
    expected = {
        WAR_FILES[4]: high_scale_ai_defines_text(),
        WAR_FILES[2]: minerals_planet_construction_budget_text(),
        WAR_FILES[1]: army_recruitment_budget_text(),
        WAR_FILES[8]: strategy_kernel_triggers_text(),
    }
    for relative, generated in expected.items():
        _require(_read(relative) == generated, f"generated file drifted from generator source: {relative}", errors)


def validate() -> list[str]:
    errors: list[str] = []
    _validate_required_files(errors)
    if errors:
        return errors
    _validate_native_only(errors)
    _validate_country_type(errors)
    _validate_defines(errors)
    _validate_army_and_planet_budgets(errors)
    _validate_high_capacity_workaround(errors)
    _validate_boxed_in_and_policy_exit(errors)
    _validate_personalities(errors)
    _validate_provenance(errors)
    _validate_generator_and_docs(errors)
    _validate_deterministic_source_matches(errors)
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Stellar AI Director 4.4.4 war solution validation FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Stellar AI Director 4.4.4 native war solution validation passed.")
    print(f"Validated {len(WAR_FILES)} PDXScript files and 33 full-object/define provenance rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
