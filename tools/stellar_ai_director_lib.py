#!/usr/bin/env python3
"""Deterministic tooling for the Stellar AI Director patch mod.

This module intentionally keeps Stellaris PDXScript parsing lightweight and
local. It extracts enough structure for AI-budget, economic-plan, technology,
and megastructure validation without pretending to be a full game compiler.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_ROOT = REPO_ROOT / "research" / "mod-source-snapshots" / "2026-07-04"
IRONY_DATA_ROOT = Path(r"C:\Users\Admin\AppData\Roaming\Mario")
STELLARIS_INSTALL_ROOT = Path(r"C:\Steam\steamapps\common\Stellaris")
STELLARIS_LOG_ROOT = Path(r"C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs")
STELLARIS_SAVE_ROOT = Path(r"C:\Users\Admin\Documents\Paradox Interactive\Stellaris\save games")
PARADOX_MOD_ROOT = Path(r"C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod")
DLC_LOAD_PATH = Path(r"C:\Users\Admin\Documents\Paradox Interactive\Stellaris\dlc_load.json")
MOD_ROOT = REPO_ROOT / "mods" / "StellarAIDirector"
RESEARCH_ROOT = REPO_ROOT / "research" / "stellar-ai"
DIRECTOR_DLC_LOAD_ENTRY = "mod/StellarAIDirector.mod"
BASELINE_ERROR_LOG = RESEARCH_ROOT / "baseline-without-director-error-2026-07-04.log"
BASELINE_GAME_LOG = RESEARCH_ROOT / "baseline-without-director-game-2026-07-04.log"
WITH_DIRECTOR_ERROR_LOG = RESEARCH_ROOT / "with-director-error-2026-07-04.log"
WITH_DIRECTOR_GAME_LOG = RESEARCH_ROOT / "with-director-game-2026-07-04.log"
MAIN_MENU_PROOF_PATH = RESEARCH_ROOT / "stellar-ai-director-main-menu-proof-2026-07-04.json"
MAIN_MENU_CONFIRMATION_ENV = "STELLAR_AI_DIRECTOR_MAIN_MENU_CONFIRMED"
LAUNCH_SURFACE_ENV = "STELLAR_AI_DIRECTOR_LAUNCH_SURFACE"
MAIN_MENU_REQUIRED_MODES = ("baseline_without_director", "with_director")
LOAD_PROOF_EVENT_ID = "staid_load_proof.1"
LOAD_PROOF_LOG_MARKER = "STELLAR_AI_DIRECTOR_LOAD_PROOF"
LOAD_PROOF_TITLE = "Stellar AI Director Loaded"
PLAN_PATH = REPO_ROOT / "plans" / "stellar-ai-director-v1-remaining-plan.md"
PLAN_STATUS_JSON = RESEARCH_ROOT / "stellar-ai-director-v1-plan-status-2026-07-04.json"
PLAN_STATUS_MD = RESEARCH_ROOT / "stellar-ai-director-v1-plan-status-2026-07-04.md"
REFERENCE_AUDIT_CSV = RESEARCH_ROOT / "stellar-ai-director-generated-reference-audit-2026-07-04.csv"
REFERENCE_AUDIT_MD = RESEARCH_ROOT / "stellar-ai-director-generated-reference-audit-2026-07-04.md"
DEPENDENCY_AUDIT_CSV = RESEARCH_ROOT / "stellar-ai-director-dependency-audit-2026-07-04.csv"
DEPENDENCY_AUDIT_MD = RESEARCH_ROOT / "stellar-ai-director-dependency-audit-2026-07-04.md"
IRONY_ORDER_PROOF_JSON = RESEARCH_ROOT / "stellar-ai-director-irony-order-proof-2026-07-04.json"
IRONY_ORDER_PROOF_MD = RESEARCH_ROOT / "stellar-ai-director-irony-order-proof-2026-07-04.md"
IRONY_CONFLICT_SCAN_MD = RESEARCH_ROOT / "stellar-ai-director-irony-conflict-scan-2026-07-04.md"
IRONY_REVIEWED_CONFLICT_OBJECTS = {
    "alloys_expenditure_megastructures",
    "negative_mass_expenditure_megastructures",
    "sentient_metal_expenditure_megastructures",
    "supertensiles_upkeep_megastructures",
}
FILE_AUDIT_CSV = RESEARCH_ROOT / "stellar-ai-director-generated-file-audit-2026-07-04.csv"
FILE_AUDIT_MD = RESEARCH_ROOT / "stellar-ai-director-generated-file-audit-2026-07-04.md"
ROI_QUALITY_AUDIT_CSV = RESEARCH_ROOT / "stellar-ai-director-roi-quality-audit-2026-07-04.csv"
ROI_QUALITY_AUDIT_MD = RESEARCH_ROOT / "stellar-ai-director-roi-quality-audit-2026-07-04.md"
INTEGRATION_POLICY_AUDIT_CSV = RESEARCH_ROOT / "stellar-ai-director-integration-policy-audit-2026-07-04.csv"
INTEGRATION_POLICY_AUDIT_MD = RESEARCH_ROOT / "stellar-ai-director-integration-policy-audit-2026-07-04.md"
OBSERVER_SMOKE_SAVE_SUMMARY_JSON = RESEARCH_ROOT / "stellar-ai-director-observer-smoke-save-summary-2026-07-04.json"
OBSERVER_SMOKE_SAVE_SUMMARY_MD = RESEARCH_ROOT / "stellar-ai-director-observer-smoke-save-summary-2026-07-04.md"
OBJECT_ATLAS_ROOT = RESEARCH_ROOT / "object-atlas"
OBJECT_ATLAS_SCHEMA_MD = OBJECT_ATLAS_ROOT / "schema.md"
OBJECT_ATLAS_CSV = OBJECT_ATLAS_ROOT / "object-atlas-2026-07-06.csv"
DEPENDENCY_EDGES_CSV = OBJECT_ATLAS_ROOT / "dependency-edges-2026-07-06.csv"
AI_SUPPORT_MAP_CSV = OBJECT_ATLAS_ROOT / "parent-ai-support-map-2026-07-06.csv"
POLICY_MATRIX_CSV = OBJECT_ATLAS_ROOT / "policy-matrix-2026-07-06.csv"
OBJECT_ATLAS_COVERAGE_MD = OBJECT_ATLAS_ROOT / "coverage-report-2026-07-06.md"
ROUTE_REPORT_MD = OBJECT_ATLAS_ROOT / "route-reports-2026-07-06.md"

REQUIRED_MODS = {
    "3610149307": "Stellar AI",
    "1121692237": "Gigastructural Engineering & More (4.4)",
    "683230077": "NSC3",
    "2648658105": "Extra Ship Components NEXT",
    "3250900527": "Starbase Extended 3.0",
}

UNIVERSAL_RESOURCE_PATCH_NAME = "!!!Universal Resource Patch [2.4+]"

OPTIONAL_MOD_NAME_MARKERS = {
    "Universal Resource Patch": "Universal Resource Patch",
    "Smarter Hyper Relays": "Smarter Hyper Relays",
    "Spacefleet Tactica": "Spacefleet Tactica",
    "Planetary Diversity": "Planetary Diversity",
    "Guilli": "Guilli's Planet Modifiers and Features",
}

RESOURCE_VALUES = {
    "alloys": 1.0,
    "minerals": 0.35,
    "energy": 0.25,
    "consumer_goods": 0.75,
    "unity": 0.50,
    "physics_research": 0.75,
    "society_research": 0.75,
    "engineering_research": 0.75,
    "volatile_motes": 4.0,
    "exotic_gases": 4.0,
    "rare_crystals": 4.0,
    "sr_dark_matter": 8.0,
    "sr_zro": 8.0,
    "nanites": 8.0,
    "giga_sr_sentient_metal": 10.0,
    "giga_sr_negative_mass": 10.0,
    "giga_sr_amb_megaconstruction": 10.0,
    "giga_sr_iodizium": 10.0,
}

VANILLA_COMMON_ROOT = Path(r"C:\Steam\steamapps\common\Stellaris\common")
MARKET_TRADE_FEE_BASE = 0.30
MARKET_MIN_FLUCTUATION_FROM_BASE_PRICE = -80.0
MARKET_MAX_FLUCTUATION_FROM_BASE_PRICE = 400.0
SHIPYARD_SLOT_ANNUAL_ALLOY_THROUGHPUT = 450.0

ROI_TARGETS = [
    "mega_shipyard",
    "equatorial_shipyard",
    "neutronium_gigaforge",
    "gigaforge",
    "nidavellir",
    "hrae",
    "dyson",
    "matrioshka",
    "strategic_factory",
    "flagship",
    "headquarters",
]

INTEGRATION_SURFACE_FOLDERS = {
    "technology": ("technology", "P6"),
    "ascension_perks": ("ascension_perk", "P6"),
    "traditions": ("tradition", "P6"),
    "megastructures": ("megastructure", "P7"),
    "starbase_modules": ("starbase_module", "P9"),
    "starbase_buildings": ("starbase_building", "P9"),
    "buildings": ("building", "P10"),
    "ship_sizes": ("ship_size", "P11"),
    "component_templates": ("component_template", "P11"),
}

ATLAS_COMMON_SURFACES = {
    "technology": "technology",
    "technologies": "technology",
    "ascension_perks": "ascension_perk",
    "traditions": "tradition",
    "megastructures": "megastructure",
    "buildings": "building",
    "districts": "district",
    "pop_jobs": "pop_job",
    "resources": "resource",
    "strategic_resources": "resource",
    "deposits": "deposit",
    "ship_sizes": "ship_size",
    "component_templates": "component_template",
    "section_templates": "section_template",
    "starbase_modules": "starbase_module",
    "starbase_buildings": "starbase_building",
    "edicts": "edict",
    "policies": "policy",
    "decisions": "decision",
    "scripted_triggers": "scripted_trigger",
    "scripted_effects": "scripted_effect",
    "script_values": "scripted_value",
    "ai_budget": "ai_budget",
    "economic_plans": "economic_plan",
    "personalities": "personality",
    "country_types": "country_type",
}

ATLAS_AI_SIGNAL_KEYS = {
    "ai_weight",
    "ai_weight_modifier",
    "ai_will_do",
    "ai_chance",
    "ai_allow",
    "ai_budget",
    "ai_resource_production",
    "weight",
}

ROUTE_OBJECT_HINTS = {
    "mega_engineering_core": ("mega_engineering", "mega_shipyard", "megastructure"),
    "mega_shipyard_core": ("mega_shipyard", "shipyard", "headquarters"),
    "economy_megastructure_core": ("dyson", "gigaforge", "nidavellir", "matrioshka", "strategic_factory"),
    "gigas_special_resource_core": ("sentient_metal", "negative_mass", "megaconstruction", "supertensiles", "dark_matter"),
    "research_throughput_infrastructure": ("research_lab", "research", "institute", "supercomputer", "archaeostudies", "science"),
    "planetcraft_route": ("planetcraft", "planet_assembly", "planet_behemoth", "celestial_printing"),
    "war_moon_route": ("war_moon", "attack_moon", "lunar"),
    "systemcraft_route": ("systemcraft", "war_system", "planet_behemoth", "celestial_printing"),
    "nsc3_capital_hull_route": ("dreadnought", "carrier", "flagship", "supercapital", "headquarters"),
    "esc_component_route": ("esc_", "dark_matter_power_core", "strikecraft_5", "reactor", "shield"),
    "crowded_tall_route": ("habitat", "orbital", "district", "building", "capacity"),
    "conquest_escape_route": ("claim", "subjugation", "war", "fleet", "naval_cap"),
    "fallen_empire_benchmark_route": ("fallen", "awakened", "crisis", "systemcraft", "planetcraft"),
}

GENERATED_SURFACE_FOLDERS = {
    "ai_budget": "ai_budget",
    "ascension_perks": "ascension_perk",
    "component_templates": "component_template",
    "buildings": "building",
    "districts": "district",
    "economic_plans": "economic_plan",
    "megastructures": "megastructure",
    "opinion_modifiers": "opinion_modifier",
    "on_actions": "on_action",
    "scripted_triggers": "scripted_trigger",
    "script_values": "scripted_value",
    "ship_sizes": "ship_size",
    "starbase_buildings": "starbase_building",
    "starbase_modules": "starbase_module",
    "technology": "technology",
    "traditions": "tradition",
}
GENERATED_AUXILIARY_COMMON_FOLDERS: set[str] = set()

RESEARCH_RESOURCES = ("physics_research", "society_research", "engineering_research")
SURPLUS_WASTE_STOCKPILE_THRESHOLDS = {
    "minerals": 50000.0,
    "food": 30000.0,
    "consumer_goods": 30000.0,
    "volatile_motes": 800.0,
    "exotic_gases": 800.0,
    "rare_crystals": 800.0,
    "sr_dark_matter": 1000.0,
    "sr_zro": 1000.0,
    "nanites": 1000.0,
    "giga_sr_sentient_metal": 2500.0,
}

MARKET_CAP_BREAKER_SALES = [
    ("minerals", 50000, 5000, ""),
    ("food", 30000, 5000, "country_uses_food = yes"),
    ("consumer_goods", 30000, 2500, "country_uses_consumer_goods = yes"),
    ("volatile_motes", 800, 200, ""),
    ("exotic_gases", 800, 200, ""),
    ("rare_crystals", 800, 200, ""),
    ("sr_dark_matter", 1000, 100, ""),
    ("sr_zro", 1000, 100, ""),
    ("nanites", 1000, 100, ""),
    ("giga_sr_sentient_metal", 2500, 250, "has_technology = tech_ehof_sentient_tier_1"),
]

ROUTE_OVERRIDE_TARGETS = [
    # Core unlock techs and high-scale research chains.
    {"object_id": "tech_mega_engineering", "object_type": "technology", "mod_id": "vanilla", "route_id": "mega_engineering_core", "weight": 200000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_mega_shipyard", "object_type": "technology", "mod_id": "vanilla", "route_id": "mega_shipyard_core", "weight": 180000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_planet_assembly", "object_type": "technology", "mod_id": "1121692237", "route_id": "planetcraft_route", "weight": 160000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_lunar_assembly", "object_type": "technology", "mod_id": "1121692237", "route_id": "war_moon_route", "weight": 135000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_war_moon_1", "object_type": "technology", "mod_id": "1121692237", "route_id": "war_moon_route", "weight": 155000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_war_moon_2", "object_type": "technology", "mod_id": "1121692237", "route_id": "war_moon_route", "weight": 180000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_war_moon_sections", "object_type": "technology", "mod_id": "1121692237", "route_id": "war_moon_route", "weight": 150000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_war_system_1", "object_type": "technology", "mod_id": "1121692237", "route_id": "systemcraft_route", "weight": 150000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_war_system_2", "object_type": "technology", "mod_id": "1121692237", "route_id": "systemcraft_route", "weight": 170000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_war_system_3", "object_type": "technology", "mod_id": "1121692237", "route_id": "systemcraft_route", "weight": 190000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_war_system_4", "object_type": "technology", "mod_id": "1121692237", "route_id": "systemcraft_route", "weight": 210000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_war_system_5", "object_type": "technology", "mod_id": "1121692237", "route_id": "systemcraft_route", "weight": 230000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_war_system_6", "object_type": "technology", "mod_id": "1121692237", "route_id": "systemcraft_route", "weight": 250000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_ehof_sentient_tier_1", "object_type": "technology", "mod_id": "1121692237", "route_id": "gigas_special_resource_core", "weight": 140000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_nm_utilization_1", "object_type": "technology", "mod_id": "1121692237", "route_id": "gigas_special_resource_core", "weight": 140000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_amb_supertensiles", "object_type": "technology", "mod_id": "1121692237", "route_id": "gigas_special_resource_core", "weight": 140000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_Carrier_1", "object_type": "technology", "mod_id": "683230077", "route_id": "nsc3_capital_hull_route", "weight": 125000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_Dreadnought_1", "object_type": "technology", "mod_id": "683230077", "route_id": "nsc3_capital_hull_route", "weight": 150000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_Flagship_1", "object_type": "technology", "mod_id": "683230077", "route_id": "nsc3_capital_hull_route", "weight": 170000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_heavycarrier_1", "object_type": "technology", "mod_id": "683230077", "route_id": "nsc3_capital_hull_route", "weight": 130000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_supercarrier_1", "object_type": "technology", "mod_id": "683230077", "route_id": "nsc3_capital_hull_route", "weight": 145000, "file_key": "01_unlock_technology"},
    {"object_id": "esc_tech_dark_matter_power_core_2", "object_type": "technology", "mod_id": "2648658105", "route_id": "esc_component_route", "weight": 150000, "file_key": "01_unlock_technology"},
    {"object_id": "esc_tech_strikecraft_5", "object_type": "technology", "mod_id": "2648658105", "route_id": "esc_component_route", "weight": 140000, "file_key": "01_unlock_technology"},
    {"object_id": "esc_tech_dreadnought_computer", "object_type": "technology", "mod_id": "2648658105", "route_id": "esc_component_route", "weight": 130000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_starbase_6", "object_type": "technology", "mod_id": "3250900527", "route_id": "fallen_empire_benchmark_route", "weight": 135000, "file_key": "01_unlock_technology"},
    # AP and tradition pressure for routes that Stellaris otherwise treats as optional flavor.
    {"object_id": "ap_gigastructural_constructs", "object_type": "ascension_perk", "mod_id": "1121692237", "route_id": "economy_megastructure_core", "weight": 120000, "file_key": "02_perks_traditions"},
    {"object_id": "ap_celestial_printing", "object_type": "ascension_perk", "mod_id": "1121692237", "route_id": "planetcraft_route", "weight": 180000, "file_key": "02_perks_traditions"},
    {"object_id": "ap_lord_of_war", "object_type": "ascension_perk", "mod_id": "vanilla", "route_id": "conquest_escape_route", "weight": 80000, "file_key": "02_perks_traditions"},
    {"object_id": "tr_supremacy_adopt", "object_type": "tradition", "mod_id": "vanilla", "route_id": "conquest_escape_route", "weight": 90000, "file_key": "02_perks_traditions"},
    {"object_id": "tr_prosperity_adopt", "object_type": "tradition", "mod_id": "vanilla", "route_id": "economy_megastructure_core", "weight": 85000, "file_key": "02_perks_traditions"},
    {"object_id": "tr_adaptability_adopt", "object_type": "tradition", "mod_id": "vanilla", "route_id": "crowded_tall_route", "weight": 75000, "file_key": "02_perks_traditions"},
    {"object_id": "tr_mercantile_adopt", "object_type": "tradition", "mod_id": "vanilla", "route_id": "crowded_tall_route", "weight": 65000, "file_key": "02_perks_traditions"},
    # Direct research-throughput infrastructure for the observed low-tech/high-stockpile failure mode.
    {"object_id": "building_research_lab_1", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 140000, "coefficient": "8", "additional_weight": "600", "file_key": "06_research_infrastructure"},
    {"object_id": "building_research_lab_2", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 160000, "coefficient": "10", "additional_weight": "900", "file_key": "06_research_infrastructure"},
    {"object_id": "building_research_lab_3", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 180000, "coefficient": "12", "additional_weight": "1200", "file_key": "06_research_infrastructure"},
    {"object_id": "building_institute", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 150000, "coefficient": "8", "additional_weight": "800", "file_key": "06_research_infrastructure"},
    {"object_id": "building_supercomputer", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 150000, "coefficient": "8", "additional_weight": "800", "file_key": "06_research_infrastructure"},
    {"object_id": "building_archaeostudies_faculty", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 130000, "coefficient": "6", "additional_weight": "500", "file_key": "06_research_infrastructure"},
    {"object_id": "district_hab_science", "object_type": "district", "mod_id": "vanilla", "source_file": "common/districts/03_habitat_districts.txt", "route_id": "crowded_tall_route", "weight": 110000, "coefficient": "4", "additional_weight": "500", "file_key": "06_research_infrastructure"},
    # Concrete build-priority objects for economy multipliers, Mega Shipyard, planetcraft, war moons, and systemcraft.
    {"object_id": "dyson_sphere_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_dyson_sphere.txt", "route_id": "economy_megastructure_core", "weight": 130000, "file_key": "03_megastructures"},
    {"object_id": "mega_shipyard_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_mega_shipyard.txt", "route_id": "mega_shipyard_core", "weight": 150000, "file_key": "03_megastructures"},
    {"object_id": "neutronium_gigaforge_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_neutronium_gigaforge.txt", "route_id": "economy_megastructure_core", "weight": 135000, "file_key": "03_megastructures"},
    {"object_id": "nidavellir_forge_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_i_nidavellir_forge.txt", "route_id": "economy_megastructure_core", "weight": 140000, "file_key": "03_megastructures"},
    {"object_id": "matrioshka_brain_0_g_star", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_i_matrioshka_brain_revised.txt", "route_id": "economy_megastructure_core", "weight": 145000, "file_key": "03_megastructures"},
    {"object_id": "planetcraft_printer_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_i_behemoth_assembly_plant.txt", "route_id": "planetcraft_route", "weight": 180000, "file_key": "03_megastructures"},
    {"object_id": "war_moon_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_attack_moon.txt", "route_id": "war_moon_route", "weight": 165000, "file_key": "03_megastructures"},
    {"object_id": "war_system_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_i_stellar_systemcraft.txt", "route_id": "systemcraft_route", "weight": 200000, "file_key": "03_megastructures"},
    # Parent design surfaces that need direct pressure when AI weights are partial or wrong-goal.
    # NSC3 hull and ESC component-template usage is covered through unlock tech, fleet economy,
    # and starbase support here because the current atlas does not model ESC internal `key =`
    # component-template entries as top-level load-order objects.
    {"object_id": "esc_starbase_reactor", "object_type": "starbase_building", "mod_id": "2648658105", "route_id": "fallen_empire_benchmark_route", "weight": 75000, "file_key": "05_starbase_defense"},
]

THREAT_RESPONSE_AXES = (
    "moral_outrage",
    "regional_fear",
    "shared_threat_cooperation",
    "conquest_respect",
    "punitive_pressure",
    "defensive_readiness",
    "opportunism",
)
THREAT_FANATIC_MULTIPLIER = 3
THREAT_SCORE_LIMITS = {
    "anti_aggressor_score": (0, 100),
    "alignment_with_aggressor_score": (0, 60),
    "defensive_readiness_score": (0, 50),
}
THREAT_TIER_CUTOFFS = {
    "anti_aggressor_low": 25,
    "anti_aggressor_medium": 45,
    "anti_aggressor_high": 65,
    "anti_aggressor_severe": 85,
    "alignment_low": 20,
    "alignment_medium": 35,
    "alignment_high": 50,
    "defensive_readiness_low": 25,
    "defensive_readiness_high": 40,
}
THREAT_OPINION_VALUES = {
    "anti_aggressor_low": -30,
    "anti_aggressor_medium": -60,
    "anti_aggressor_high": -120,
    "anti_aggressor_severe": -200,
    "shared_threat_low": 15,
    "shared_threat_medium": 30,
    "shared_threat_high": 60,
    "alignment_low": 10,
    "alignment_medium": 25,
    "alignment_high": 40,
}
THREAT_RELATION_FLAG_DAYS = 7200
THREAT_COUNTRY_FLAG_DAYS = THREAT_RELATION_FLAG_DAYS
THREAT_ECONOMY_RATIO_CAP = 0.20
THREAT_FLEET_RESERVE_BASE = {"alloys": 35, "energy": 30, "naval_cap": 200}
THREAT_ECONOMY_MAX = {
    key: int(value * THREAT_ECONOMY_RATIO_CAP)
    for key, value in THREAT_FLEET_RESERVE_BASE.items()
}
THREAT_FORBIDDEN_EFFECTS = (
    "declare_war",
    "join_war",
    "add_casus_belli",
    "attacker_war_goal",
)
THREAT_NORMAL_ETHIC_VECTORS = {
    "ethic_pacifist": (3, 1, 2, -2, 1, 2, 0),
    "ethic_egalitarian": (2, 1, 2, -1, 1, 1, 0),
    "ethic_xenophile": (1, 1, 3, -1, 1, 1, 0),
    "ethic_militarist": (-1, 2, 0, 2, 1, 2, 1),
    "ethic_authoritarian": (-1, 1, -1, 2, 0, 1, 2),
    "ethic_xenophobe": (0, 3, -2, 1, 2, 2, 1),
    "ethic_materialist": (0, 2, 1, 0, 1, 1, 1),
    "ethic_spiritualist": (1, 1, 1, 0, 1, 1, 0),
}
THREAT_GESTALT_VECTORS = {
    "gestalt_standard": (0, 2, 0, 0, 1, 2, 0),
    "gestalt_empath": (2, 2, 2, 0, 1, 2, 0),
    "homicidal": (0, 2, -3, 3, 0, 2, 2),
}
THREAT_CIVIC_AXIS_CAP = 1
THREAT_TOTAL_CIVIC_AXIS_CAP = 2
WAR_GOAL_THREAT_CLASSES = {
    "wg_conquest": {
        "war_goal": "wg_conquest",
        "classification": "conquest",
        "severity": 2,
        "source": "Stellaris 4.4.4 vanilla",
        "source_path": "C:/Steam/steamapps/common/Stellaris/common/war_goals/00_war_goals.txt",
        "mod_or_vanilla": "vanilla",
        "punitive_outputs_allowed": "yes",
        "readiness_outputs_allowed": "yes",
        "forced_war_allowed": "no",
        "status": "classified",
        "notes": "Initial V1 allowlist aggressive conquest goal.",
    },
    "wg_subjugation": {
        "war_goal": "wg_subjugation",
        "classification": "subjugation",
        "severity": 3,
        "source": "Stellaris 4.4.4 vanilla",
        "source_path": "C:/Steam/steamapps/common/Stellaris/common/war_goals/00_war_goals.txt",
        "mod_or_vanilla": "vanilla",
        "punitive_outputs_allowed": "yes",
        "readiness_outputs_allowed": "yes",
        "forced_war_allowed": "no",
        "status": "classified",
        "notes": "Initial V1 allowlist aggressive subjugation goal.",
    },
    "wg_humiliation": {
        "war_goal": "wg_humiliation",
        "classification": "humiliation",
        "severity": 1,
        "source": "Stellaris 4.4.4 vanilla",
        "source_path": "C:/Steam/steamapps/common/Stellaris/common/war_goals/00_war_goals.txt",
        "mod_or_vanilla": "vanilla",
        "punitive_outputs_allowed": "yes",
        "readiness_outputs_allowed": "yes",
        "forced_war_allowed": "no",
        "status": "classified",
        "notes": "Initial V1 allowlist lower-severity humiliation goal.",
    },
}
THREAT_FEASIBILITY_NOTE_NAME = "stellar-ai-director-threat-response-feasibility-2026-07-05.md"
THREAT_CLASSIFICATION_CSV_NAME = "stellar-ai-director-threat-response-war-goal-classification-2026-07-05.csv"

PLAN_PHASE_EVIDENCE = {
    "P0": ("research/stellar-ai/stellar-ai-director-munch-preflight-2026-07-04.md",),
    "P1": (
        "research/mod-source-snapshots/2026-07-04/snapshot-manifest.csv",
        "research/mod-source-snapshots/2026-07-04/descriptor-inventory.csv",
        "research/mod-source-snapshots/2026-07-04/pdx-object-inventory.csv",
        "research/mod-source-snapshots/2026-07-04/ai-surface-inventory.csv",
        "research/stellar-ai/stellar-ai-director-corpus-status-2026-07-04.md",
    ),
    "P2": (
        "research/stellar-ai/stellar-ai-director-active-playset-2026-07-04.json",
        "mods/StellarAIDirector/notes/load-order.md",
        "research/stellar-ai/stellar-ai-director-dependency-audit-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-irony-order-proof-2026-07-04.json",
    ),
    "P3": (
        "research/stellar-ai/stellar-ai-director-roi-matrix-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-market-values-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-roi-quality-audit-2026-07-04.csv",
    ),
    "P4": ("mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt",),
    "P5": (
        "mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt",
        "mods/StellarAIDirector/common/ai_budget/zzz_staid_gigas_resource_budgets.txt",
        "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt",
        "mods/StellarAIDirector/common/script_values/zzz_staid_roi_values.txt",
        "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt",
        "mods/StellarAIDirector/common/on_actions/zzz_staid_load_proof_on_actions.txt",
        "mods/StellarAIDirector/notes/tuning-notes.md",
    ),
    "P6": (
        "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt",
        "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt",
        "mods/StellarAIDirector/notes/tuning-notes.md",
        "research/stellar-ai/stellar-ai-director-integration-surfaces-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-generated-reference-audit-2026-07-04.csv",
    ),
    "P7": (
        "mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt",
        "mods/StellarAIDirector/common/ai_budget/zzz_staid_gigas_resource_budgets.txt",
        "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt",
        "mods/StellarAIDirector/notes/tuning-notes.md",
        "research/stellar-ai/stellar-ai-director-roi-matrix-2026-07-04.md",
        "research/stellar-ai/stellar-ai-director-roi-quality-audit-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-integration-policy-audit-2026-07-04.csv",
    ),
    "P8": (
        "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt",
        "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt",
        "mods/StellarAIDirector/notes/tuning-notes.md",
        "research/stellar-ai/stellar-ai-director-roi-matrix-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-integration-policy-audit-2026-07-04.csv",
    ),
    "P9": (
        "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt",
        "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt",
        "mods/StellarAIDirector/notes/tuning-notes.md",
        "research/stellar-ai/stellar-ai-director-integration-surfaces-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-integration-policy-audit-2026-07-04.csv",
    ),
    "P10": (
        "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt",
        "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt",
        "mods/StellarAIDirector/notes/tuning-notes.md",
        "research/stellar-ai/stellar-ai-director-integration-surfaces-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-integration-policy-audit-2026-07-04.csv",
    ),
    "P11": (
        "mods/StellarAIDirector/notes/tuning-notes.md",
        "mods/StellarAIDirector/notes/conflicts.md",
        "research/stellar-ai/stellar-ai-director-integration-surfaces-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-integration-policy-audit-2026-07-04.csv",
    ),
    "P12": (
        "research/stellar-ai/stellar-ai-director-generated-file-audit-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-generated-conflicts-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-generated-reference-audit-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-dependency-audit-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-roi-quality-audit-2026-07-04.csv",
        "research/stellar-ai/stellar-ai-director-integration-policy-audit-2026-07-04.csv",
    ),
    "P13": (
        "research/stellar-ai/stellar-ai-director-generated-conflicts-2026-07-04.md",
        "research/stellar-ai/stellar-ai-director-irony-conflict-scan-2026-07-04.md",
    ),
    "P14": (
        "mods/StellarAIDirector/common/on_actions/zzz_staid_load_proof_on_actions.txt",
        "mods/StellarAIDirector/events/zzz_staid_load_proof_events.txt",
        "mods/StellarAIDirector/localisation/english/staid_load_proof_l_english.yml",
        "research/stellar-ai/stellar-ai-director-launch-comparison-2026-07-04.json",
        "research/stellar-ai/stellar-ai-director-main-menu-proof-2026-07-04.json",
        "research/stellar-ai/baseline-without-director-screenshot-2026-07-04.png",
        "research/stellar-ai/with-director-screenshot-2026-07-04.png",
        "research/stellar-ai/baseline-without-director-error-2026-07-04.log",
        "research/stellar-ai/with-director-error-2026-07-04.log",
    ),
    "P15": (
        "mods/StellarAIDirector/notes/observer-test-log.md",
        "research/stellar-ai/stellar-ai-director-observer-smoke-save-summary-2026-07-04.json",
        "research/stellar-ai/stellar-ai-director-observer-smoke-save-summary-2026-07-04.md",
    ),
    "P16": (
        "mods/StellarAIDirector/README.md",
        "mods/StellarAIDirector/notes/load-order.md",
        "mods/StellarAIDirector/notes/conflicts.md",
        "mods/StellarAIDirector/notes/observer-test-log.md",
        "mods/StellarAIDirector/notes/tuning-notes.md",
    ),
}

PLAN_PHASE_OPEN_REASONS = {
    "P0": "Munch preflight requires recorded active-thread guide calls and startup-script pass evidence.",
    "P1": "Source corpus requires current snapshot manifests, object inventories, AI-surface inventories, and recorded Munch refresh evidence.",
    "P2": "Dependency names and final load-order position require a passing Irony order proof.",
    "P3": "ROI artifacts require broad parent-mod coverage, bottleneck preservation, and no failed quality rows.",
    "P4": "Decision helpers require generated trigger mapping for emergency exits, prep/commit, and surplus sinks.",
    "P5": "Generated surfaces require validated files, references, conflict ownership, and documentation.",
    "P6": "Unlock priority policy requires generated research/unity mapping and validated tech/AP/tradition references.",
    "P7": "Mega/giga build priority requires ready ROI rows, generated budget gates, and explicit deferral of unsafe per-object overrides.",
    "P8": "Shipyard/fleet sink policy requires generated economy-plan mapping plus anti-death-spiral gates.",
    "P9": "Starbase policy requires generated static-defense subplans plus explicit notes for unsafe direct starbase object control.",
    "P10": "Planet/building capacity policy requires generated economy-plan coverage or an explicit no-direct-building-reference rationale.",
    "P11": "NSC3/ESC direct design overrides require explicit preservation rationale and no failed audit rows.",
    "P12": "Validator requires missing-reference, quality, dependency, load-order, and ownership gates to pass.",
    "P13": "Irony conflict scan has not been recorded.",
    "P16": "Docs require dependency, load-order, conflict, tuning, validation, and observer-test workflow coverage.",
}

PLAN_PHASE_SUPERSEDED_REASONS = {
    "P14": "Superseded for this goal: user/runtime launch validation is intentionally out of scope; deterministic validation is the acceptance gate.",
    "P15": "Superseded for this goal: observer runtime validation is intentionally out of scope; deterministic validation is the acceptance gate.",
}

TEXT_SUFFIXES = {".txt", ".mod", ".asset", ".gfx", ".gui", ".yml", ".yaml", ".csv", ".json"}


class PDXParseError(ValueError):
    """Raised when a PDXScript source cannot be tokenized or parsed."""


@dataclass(slots=True)
class MarketPrice:
    resource: str
    market_amount: float
    market_price: float
    tradable: bool

    @property
    def base_energy(self) -> float:
        return self.market_price / self.market_amount

    @property
    def min_sell_energy(self) -> float:
        return self.base_energy * (1.0 + MARKET_MIN_FLUCTUATION_FROM_BASE_PRICE / 100.0)

    @property
    def max_buy_energy(self) -> float:
        return self.base_energy * (1.0 + MARKET_MAX_FLUCTUATION_FROM_BASE_PRICE / 100.0)

    @property
    def default_fee_base_buy_energy(self) -> float:
        return self.base_energy * (1.0 + MARKET_TRADE_FEE_BASE)

    @property
    def default_fee_floor_sell_energy(self) -> float:
        return self.min_sell_energy * (1.0 - MARKET_TRADE_FEE_BASE)

    @property
    def default_fee_ceiling_buy_energy(self) -> float:
        return self.max_buy_energy * (1.0 + MARKET_TRADE_FEE_BASE)


@dataclass(slots=True)
class PDXAtom:
    value: str


@dataclass(slots=True)
class PDXAssignment:
    key: str
    value: "PDXValue"


@dataclass(slots=True)
class PDXBlock:
    items: list[PDXAssignment | PDXAtom] = field(default_factory=list)


PDXValue = PDXAtom | PDXBlock


TOKEN_RE = re.compile(
    r"""
    "(?:\\.|[^"\\])*"
    |[{}=]
    |[<>]=?
    |[^\s{}=<>#]+
    """,
    re.VERBOSE,
)


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return ""  # pragma: no cover - latin-1 fallback decodes arbitrary bytes.


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        in_quote = False
        escaped = False
        out = []
        for char in line:
            if char == "\\" and in_quote and not escaped:
                escaped = True
                out.append(char)
                continue
            if char == '"' and not escaped:
                in_quote = not in_quote
            if char == "#" and not in_quote:
                break
            out.append(char)
            escaped = False
        lines.append("".join(out))
    return "\n".join(lines)


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(strip_comments(text))


def parse_pdx(text: str) -> PDXBlock:
    tokens = tokenize(text)
    index = 0

    def parse_value() -> PDXValue:
        nonlocal index
        if index >= len(tokens):
            raise PDXParseError("Unexpected end of file while parsing value")
        token = tokens[index]
        if token == "{":
            index += 1
            block = PDXBlock()
            while index < len(tokens) and tokens[index] != "}":
                if index + 1 < len(tokens) and tokens[index + 1] == "=":
                    key = tokens[index]
                    index += 2
                    block.items.append(PDXAssignment(key, parse_value()))
                else:
                    block.items.append(PDXAtom(tokens[index]))
                    index += 1
            if index >= len(tokens) or tokens[index] != "}":
                raise PDXParseError("Malformed PDXScript: missing closing brace")
            index += 1
            return block
        if token == "}":
            raise PDXParseError("Malformed PDXScript: unexpected closing brace")
        index += 1
        return PDXAtom(token)

    root = PDXBlock()
    while index < len(tokens):
        if tokens[index] == "}":
            raise PDXParseError("Malformed PDXScript: unexpected closing brace at top level")
        if index + 1 < len(tokens) and tokens[index + 1] == "=":
            key = tokens[index]
            index += 2
            root.items.append(PDXAssignment(key, parse_value()))
        else:
            root.items.append(PDXAtom(tokens[index]))
            index += 1
    return root


def parse_file(path: Path) -> PDXBlock:
    try:
        return parse_pdx(read_text(path))
    except PDXParseError as exc:
        raise PDXParseError(f"{path}: {exc}") from exc


def atom_value(value: PDXValue) -> str | None:
    return value.value.strip('"') if isinstance(value, PDXAtom) else None


def block_assignments(block: PDXBlock, key: str | None = None) -> list[PDXAssignment]:
    rows = [item for item in block.items if isinstance(item, PDXAssignment)]
    if key is not None:
        rows = [item for item in rows if item.key == key]
    return rows


def iter_assignments(value: PDXValue) -> Iterable[PDXAssignment]:
    if isinstance(value, PDXBlock):
        for item in value.items:
            if isinstance(item, PDXAssignment):
                yield item
                yield from iter_assignments(item.value)


def block_atoms(block: PDXBlock) -> list[str]:
    return [item.value.strip('"') for item in block.items if isinstance(item, PDXAtom)]


def collect_variables(text: str) -> dict[str, float]:
    variables: dict[str, float] = {}
    for token, value in re.findall(r"(?m)^\s*(@[A-Za-z0-9_.~!:+-]+)\s*=\s*([0-9.]+)\s*$", strip_comments(text)):
        variables[token] = float(value)
    return variables


def collect_global_variables(roots: Iterable[Path]) -> dict[str, float]:
    variables: dict[str, float] = {}
    for root in roots:
        scripted_variables = root / "common" / "scripted_variables"
        if not scripted_variables.exists():
            continue
        for path in iter_text_files(scripted_variables):
            variables.update(collect_variables(read_text(path)))
    return variables


def collect_market_prices(roots: Iterable[Path], vanilla_common_root: Path = VANILLA_COMMON_ROOT) -> dict[str, MarketPrice]:
    prices: dict[str, MarketPrice] = {}
    candidate_roots = [vanilla_common_root.parent if vanilla_common_root.name == "common" else vanilla_common_root]
    candidate_roots.extend(roots)
    for root in candidate_roots:
        strategic_resources = root / "common" / "strategic_resources"
        if root.name == "common":
            strategic_resources = root / "strategic_resources"
        if not strategic_resources.exists():
            continue
        for path in iter_text_files(strategic_resources):
            try:
                parsed = parse_file(path)
            except PDXParseError:
                continue
            for assignment in block_assignments(parsed):
                if not isinstance(assignment.value, PDXBlock):
                    continue
                resource = assignment.key
                tradable = inline_bool_value(assignment.value, "tradable")
                amount = inline_float_value(assignment.value, "market_amount")
                price = inline_float_value(assignment.value, "market_price")
                if tradable is True and amount and price and amount > 0 and price > 0:
                    prices[resource] = MarketPrice(resource, amount, price, tradable=True)
    return prices


def eval_macro_expression(value: str, variables: dict[str, float]) -> float | None:
    value = value.strip().strip('"')
    if not (value.startswith("@[") and value.endswith("]")):
        return None
    expr = value[2:-1].strip()
    expr = re.sub(
        r"\b[A-Za-z_][A-Za-z0-9_]*\b",
        lambda match: str(variables.get(f"@{match.group(0)}", match.group(0))),
        expr,
    )
    if not re.fullmatch(r"[0-9.\s+*/()-]+", expr):
        return None
    try:
        result = eval(expr, {"__builtins__": {}}, {})
    except Exception:
        return None
    return float(result) if isinstance(result, (int, float)) and math.isfinite(result) else None


def normalize_macro_expressions(text: str, variables: dict[str, float]) -> str:
    def replace(match: re.Match[str]) -> str:
        parsed = eval_macro_expression(match.group(0), variables)
        if parsed is None:
            return match.group(0)
        return f"{parsed:g}"

    return re.sub(r"@\[[^\]]+\]", replace, text)


def resource_block_to_dict(value: PDXValue, variables: dict[str, float] | None = None) -> dict[str, float | str]:
    resources: dict[str, float | str] = {}
    variables = variables or {}
    if not isinstance(value, PDXBlock):
        return resources
    multiplier_resource = None
    multiplier_amount: float | str | None = None
    for assignment in block_assignments(value, "multiplier"):
        multiplier = atom_value(assignment.value) or ""
        match = re.search(r"RESOURCE\|([^|]+)\|AMOUNT\|([^|]+)\|", multiplier)
        if match:
            multiplier_resource = match.group(1)
            multiplier_amount = parse_numeric(match.group(2), variables)
    for assignment in block_assignments(value):
        if assignment.key in {"multiplier", "trigger"}:
            continue
        parsed = parse_numeric(atom_value(assignment.value), variables)
        if isinstance(parsed, (int, float)) and parsed < 0:
            if assignment.key == multiplier_resource and multiplier_amount is not None:
                resources[assignment.key] = multiplier_amount
            continue
        resources[assignment.key] = parsed
    return resources


def parse_numeric(value: str | None, variables: dict[str, float] | None = None) -> float | str:
    if value is None:
        return 0.0
    value = value.strip('"')
    variables = variables or {}
    if value in variables:
        return variables[value]
    macro_value = eval_macro_expression(value, variables)
    if macro_value is not None:
        return macro_value
    try:
        return float(value)
    except ValueError:
        return value


def numeric_or_zero(value: float | str) -> float:
    return value if isinstance(value, (int, float)) and math.isfinite(value) else 0.0


def inline_float_value(block: PDXBlock, key: str) -> float | None:
    for assignment in block_assignments(block, key):
        value = parse_numeric(atom_value(assignment.value))
        if isinstance(value, (int, float)) and math.isfinite(value):
            return float(value)
    return None


def inline_bool_value(block: PDXBlock, key: str) -> bool | None:
    value = inline_script_value(block, key)
    if value == "yes":
        return True
    if value == "no":
        return False
    return None


def weighted_resource_value(resources: dict[str, float | str], monthly: bool = False) -> float:
    total = 0.0
    for resource, amount in resources.items():
        mult = RESOURCE_VALUES.get(resource, 0.0)
        total += numeric_or_zero(amount) * mult
    return total * (12.0 if monthly else 1.0)


def market_resource_value(
    resources: dict[str, float | str],
    market_prices: dict[str, MarketPrice],
    price_mode: str,
    monthly: bool = False,
) -> tuple[float, dict[str, float | str]]:
    total = 0.0
    unpriced: dict[str, float | str] = {}
    for resource, amount in resources.items():
        numeric = numeric_or_zero(amount)
        if numeric == 0:
            continue
        if resource == "energy":
            total += numeric
            continue
        price = market_prices.get(resource)
        if price is None:
            unpriced[resource] = amount
            continue
        if price_mode == "base_buy":
            total += numeric * price.base_energy
        elif price_mode == "max_buy":
            total += numeric * price.max_buy_energy
        elif price_mode == "min_sell":
            total += numeric * price.min_sell_energy
        elif price_mode == "fee_base_buy":
            total += numeric * price.default_fee_base_buy_energy
        elif price_mode == "fee_max_buy":
            total += numeric * price.default_fee_ceiling_buy_energy
        elif price_mode == "fee_min_sell":
            total += numeric * price.default_fee_floor_sell_energy
        else:
            raise ValueError(f"Unknown market price mode: {price_mode}")
    return (total * (12.0 if monthly else 1.0), unpriced)


def shipyard_strategic_values(
    shipyard_capacity: float,
    build_speed: float,
    market_prices: dict[str, MarketPrice],
) -> dict[str, float]:
    if shipyard_capacity <= 0:
        return {
            "strategic_shipyard_effective_slots": 0.0,
            "strategic_shipyard_annual_alloy_throughput": 0.0,
            "strategic_shipyard_annual_fleet_value_energy": 0.0,
        }
    effective_slots = shipyard_capacity * (1.0 + max(build_speed, 0.0))
    alloy_price = market_prices.get("alloys")
    alloy_ceiling = alloy_price.max_buy_energy if alloy_price else 20.0
    annual_throughput = effective_slots * SHIPYARD_SLOT_ANNUAL_ALLOY_THROUGHPUT
    return {
        "strategic_shipyard_effective_slots": effective_slots,
        "strategic_shipyard_annual_alloy_throughput": annual_throughput,
        "strategic_shipyard_annual_fleet_value_energy": annual_throughput * alloy_ceiling,
    }


def unresolved_symbols(resources: dict[str, float | str]) -> set[str]:
    symbols: set[str] = set()
    for value in resources.values():
        if isinstance(value, str) and (value.startswith("@") or "$" in value or value.startswith("@[")):
            symbols.add(value)
    return symbols


def merge_resource_maps(target: dict[str, float | str], source: dict[str, float | str]) -> None:
    for resource, value in source.items():
        existing = target.get(resource)
        if isinstance(existing, (int, float)) and isinstance(value, (int, float)):
            target[resource] = max(float(existing), float(value))
        else:
            target[resource] = value


def block_contains_assignment(value: PDXValue, key: str, atom: str) -> bool:
    if not isinstance(value, PDXBlock):
        return False
    for assignment in iter_assignments(value):
        if assignment.key == key and atom_value(assignment.value) == atom:
            return True
    return False


def safe_mod_id(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def read_snapshot_manifest(snapshot_root: Path = SNAPSHOT_ROOT) -> dict[str, dict[str, str]]:
    path = snapshot_root / "snapshot-manifest.csv"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["id"]: row for row in csv.DictReader(handle)}


def resolve_irony_database(database: Path | None = None) -> Path:
    if database and database.exists():
        return database
    candidates = sorted(IRONY_DATA_ROOT.rglob("Database*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    if candidates:
        return candidates[0]
    expected = IRONY_DATA_ROOT / "IronyModManager" / "Database_1.26.json"
    raise FileNotFoundError(f"Irony database not found. Checked {expected} and Database*.json under {IRONY_DATA_ROOT}")


def selected_irony_collection(database: Path | None = None) -> dict[str, Any]:
    database = resolve_irony_database(database)
    if not database.exists():
        raise FileNotFoundError(f"Irony database not found: {database}")
    data = json.loads(read_text(database))
    for entry in data:
        if entry.get("Name") != "ModCollection":
            continue
        for collection in entry.get("Value", []):
            if collection.get("IsSelected"):
                return collection
    raise ValueError(f"No selected Irony collection found in {database}")


def build_active_playset_snapshot() -> dict[str, Any]:
    collection = selected_irony_collection()
    mod_ids = [safe_mod_id(item.get("SteamId") or item.get("ParadoxId")) for item in collection.get("ModIds", [])]
    names = collection.get("ModNames", [])
    paths = collection.get("ModPaths", [])
    mods = []
    for index, mod_id in enumerate(mod_ids):
        mods.append(
            {
                "position": index + 1,
                "steam_id": mod_id,
                "name": names[index] if index < len(names) else "",
                "path": paths[index] if index < len(paths) else "",
            }
        )
    present_ids = set(mod_ids)
    present_names = {name.lower() for name in names}
    return {
        "collection_name": collection.get("Name", ""),
        "patch_mod_enabled": bool(collection.get("PatchModEnabled")),
        "mod_count": len(mods),
        "mods": mods,
        "required_mods": {
            mod_id: {
                "name": name,
                "present": mod_id in present_ids,
                "load_position": mod_ids.index(mod_id) + 1 if mod_id in present_ids else None,
            }
            for mod_id, name in REQUIRED_MODS.items()
        },
        "optional_integrations": {
            label: any(marker.lower() in name for name in present_names)
            for marker, label in OPTIONAL_MOD_NAME_MARKERS.items()
        },
    }


def irony_mod_identity(mod: dict[str, Any]) -> str:
    steam_id = safe_mod_id(mod.get("steam_id") or mod.get("SteamId") or mod.get("ParadoxId"))
    if steam_id:
        return f"id:{steam_id}"
    path = str(mod.get("path") or mod.get("Path") or "").lower()
    name = str(mod.get("name") or mod.get("Name") or "").lower()
    return f"local:{name}|{path}"


def compare_irony_order_with_director(before_mods: list[dict[str, Any]], after_mods: list[dict[str, Any]]) -> dict[str, Any]:
    director_indexes = [
        index
        for index, mod in enumerate(after_mods)
        if mod.get("name") == "Stellar AI Director" or "stellaraidirector" in str(mod.get("path", "")).lower()
    ]
    before_identities = [irony_mod_identity(mod) for mod in before_mods]
    after_existing_identities = [
        irony_mod_identity(mod)
        for index, mod in enumerate(after_mods)
        if index not in director_indexes
    ]
    return {
        "director_count": len(director_indexes),
        "director_position": director_indexes[0] + 1 if director_indexes else None,
        "director_is_final_entry": bool(director_indexes and director_indexes[0] == len(after_mods) - 1),
        "existing_mod_order_preserved": before_identities == after_existing_identities,
        "expected_mod_count": len(before_mods) + 1,
        "actual_mod_count": len(after_mods),
        "status": "ok"
        if len(director_indexes) == 1
        and director_indexes[0] == len(after_mods) - 1
        and before_identities == after_existing_identities
        and len(after_mods) == len(before_mods) + 1
        else "fail",
    }


def selected_collection_mod_rows(collection: dict[str, Any]) -> list[dict[str, Any]]:
    mod_ids = collection.get("ModIds", [])
    names = collection.get("ModNames", [])
    paths = collection.get("ModPaths", [])
    mods = collection.get("Mods", [])
    rows = []
    for index in range(max(len(mod_ids), len(names), len(paths), len(mods))):
        mod_id = mod_ids[index] if index < len(mod_ids) else {}
        rows.append(
            {
                "position": index + 1,
                "steam_id": safe_mod_id(mod_id.get("SteamId") if isinstance(mod_id, dict) else ""),
                "paradox_id": safe_mod_id(mod_id.get("ParadoxId") if isinstance(mod_id, dict) else ""),
                "name": names[index] if index < len(names) else "",
                "path": paths[index] if index < len(paths) else "",
                "descriptor": mods[index] if index < len(mods) else "",
            }
        )
    return rows


def append_director_to_selected_irony_collection(
    database: Path | None = None,
    mod_root: Path = MOD_ROOT,
    research_root: Path = RESEARCH_ROOT,
) -> dict[str, Any]:
    database = resolve_irony_database(database)
    data = json.loads(read_text(database))
    selected: dict[str, Any] | None = None
    for entry in data:
        if entry.get("Name") != "ModCollection":
            continue
        for collection in entry.get("Value", []):
            if collection.get("IsSelected"):
                selected = collection
                break
    if selected is None:
        raise ValueError(f"No selected Irony collection found in {database}")

    before_rows = selected_collection_mod_rows(selected)
    if any(row["name"] == "Stellar AI Director" or "stellaraidirector" in row["path"].lower() for row in before_rows):
        return {
            "status": "already_present",
            "database": str(database),
            "collection_name": selected.get("Name", ""),
            "mod_count": len(before_rows),
            "order_check": compare_irony_order_with_director(before_rows[:-1], before_rows),
        }

    snapshot = {
        "database": str(database),
        "collection_name": selected.get("Name", ""),
        "mods": before_rows,
    }
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snapshot_path = research_root / f"irony-selected-collection-before-director-{stamp}.json"
    write_json(snapshot_path, snapshot)

    selected.setdefault("Mods", []).append("mod/StellarAIDirector.mod")
    selected.setdefault("ModIds", []).append({"ParadoxId": None, "SteamId": None})
    selected.setdefault("ModNames", []).append("Stellar AI Director")
    selected.setdefault("ModPaths", []).append(str(mod_root).lower())
    after_rows = selected_collection_mod_rows(selected)
    order_check = compare_irony_order_with_director(before_rows, after_rows)
    if order_check["status"] != "ok":
        raise ValueError(f"Irony Director insertion would not preserve order: {order_check}")

    database.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return {
        "status": "updated",
        "database": str(database),
        "collection_name": selected.get("Name", ""),
        "before_snapshot": str(snapshot_path),
        "mod_count_before": len(before_rows),
        "mod_count_after": len(after_rows),
        "order_check": order_check,
    }


def latest_irony_before_snapshot(research_root: Path = RESEARCH_ROOT) -> Path | None:
    snapshots = sorted(
        research_root.glob("irony-selected-collection-before-director-*.json"),
        key=lambda path: path.stat().st_mtime_ns,
        reverse=True,
    )
    return snapshots[0] if snapshots else None


def collect_irony_order_proof(
    before_snapshot: Path | None = None,
    playset: dict[str, Any] | None = None,
    mod_root: Path = MOD_ROOT,
    research_root: Path = RESEARCH_ROOT,
) -> dict[str, Any]:
    before_snapshot_supplied = before_snapshot is not None
    before_snapshot = before_snapshot or latest_irony_before_snapshot(research_root)
    if before_snapshot is None or not before_snapshot.exists():
        return {
            "status": "missing_before_snapshot",
            "before_snapshot": str(before_snapshot) if before_snapshot else "",
            "errors": ["No pre-Director Irony collection snapshot was found."],
        }

    before_data = json.loads(read_text(before_snapshot))
    before_mods = before_data.get("mods", [])
    playset = build_active_playset_snapshot() if playset is None else playset
    after_mods = playset.get("mods", [])
    order_check = compare_irony_order_with_director(before_mods, after_mods)
    proof_mode = "pre_director_snapshot"
    warnings: list[str] = []
    if order_check["status"] != "ok" and not before_snapshot_supplied:
        current_without_director = [
            mod
            for mod in after_mods
            if not (mod.get("name") == "Stellar AI Director" or "stellaraidirector" in str(mod.get("path", "")).lower())
        ]
        current_order_check = compare_irony_order_with_director(current_without_director, after_mods)
        if current_order_check["status"] == "ok":
            before_mods = current_without_director
            order_check = current_order_check
            proof_mode = "current_collection_without_director"
            warnings.append(
                "The historical pre-Director snapshot no longer matches the selected collection; "
                "validated the current collection by removing the single final Director entry."
            )
    dependency_rows = collect_dependency_audit_rows(mod_root, playset)
    dependency_errors = [row for row in dependency_rows if row["status"] != "ok"]
    director_position = order_check["director_position"]
    required_positions = [
        int(row["load_position"])
        for row in dependency_rows
        if row["status"] == "ok" and str(row["load_position"]).isdigit()
    ]
    latest_required_position = max(required_positions, default=0)
    errors: list[str] = []
    if order_check["status"] != "ok":
        errors.append(f"Irony order check failed: {order_check}")
    if dependency_errors:
        errors.append(f"Dependency audit has non-ok rows: {dependency_errors}")
    if director_position is None:
        errors.append("Stellar AI Director is not present in the selected Irony collection.")
    elif director_position <= latest_required_position:
        errors.append(
            f"Stellar AI Director position {director_position} is not after latest dependency position "
            f"{latest_required_position}."
        )
    elif director_position != len(after_mods):
        errors.append(
            f"Stellar AI Director position {director_position} is not the final selected collection entry "
            f"{len(after_mods)}."
        )
    return {
        "status": "ok" if not errors else "fail",
        "errors": errors,
        "warnings": warnings,
        "before_snapshot": str(before_snapshot),
        "proof_mode": proof_mode,
        "collection_name": playset.get("collection_name", ""),
        "mod_count_before": len(before_mods),
        "mod_count_after": len(after_mods),
        "latest_dependency_position": latest_required_position,
        "director_position": director_position,
        "order_check": order_check,
        "dependency_status_counts": {
            status: sum(1 for row in dependency_rows if row["status"] == status)
            for status in sorted({row["status"] for row in dependency_rows})
        },
    }


def irony_order_proof_report_text(proof: dict[str, Any]) -> str:
    lines = [
        "# Stellar AI Director Irony Order Proof",
        "",
        f"Status: {proof['status']}",
        f"Collection: {proof.get('collection_name', '')}",
        f"Before snapshot: `{proof.get('before_snapshot', '')}`",
        f"Mod count before: {proof.get('mod_count_before', '')}",
        f"Mod count after: {proof.get('mod_count_after', '')}",
        f"Director position: {proof.get('director_position', '')}",
        f"Latest dependency position: {proof.get('latest_dependency_position', '')}",
        "",
        "## Order Check",
        "",
    ]
    order_check = proof.get("order_check", {})
    for key in (
        "status",
        "director_count",
        "director_position",
        "director_is_final_entry",
        "existing_mod_order_preserved",
        "expected_mod_count",
        "actual_mod_count",
    ):
        lines.append(f"- {key}: {order_check.get(key, '')}")
    if proof.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in proof["warnings"])
    lines.extend(["", "## Dependency Status Counts", ""])
    for status, count in proof.get("dependency_status_counts", {}).items():
        lines.append(f"- {status}: {count}")
    if proof.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in proof["errors"])
    return "\n".join(lines) + "\n"


def generate_irony_order_proof_artifacts() -> dict[str, Any]:
    proof = collect_irony_order_proof()
    write_json(RESEARCH_ROOT / "stellar-ai-director-irony-order-proof-2026-07-04.json", proof)
    write_text_file(
        RESEARCH_ROOT / "stellar-ai-director-irony-order-proof-2026-07-04.md",
        irony_order_proof_report_text(proof),
    )
    return proof


def irony_order_proof_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    proof_path = repo_root / "research/stellar-ai/stellar-ai-director-irony-order-proof-2026-07-04.json"
    if not proof_path.exists():
        return False
    proof = json.loads(read_text(proof_path))
    return proof.get("status") == "ok" and proof.get("order_check", {}).get("existing_mod_order_preserved") is True


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def object_inventory_roots(snapshot_root: Path = SNAPSHOT_ROOT) -> list[Path]:
    manifest = read_snapshot_manifest(snapshot_root)
    return [Path(row["snapshot_path"]) for row in manifest.values() if Path(row["snapshot_path"]).exists()]


def collect_object_names(snapshot_root: Path = SNAPSHOT_ROOT) -> dict[str, set[str]]:
    buckets = {
        "megastructure": set(),
        "technology": set(),
        "ascension_perk": set(),
        "scripted_trigger": set(),
        "scripted_value": set(),
        "resource": set(),
        "starbase_module": set(),
        "starbase_building": set(),
        "ai_budget": set(),
        "economic_plan": set(),
        "planet_class": set(),
    }
    folder_map = {
        "megastructures": "megastructure",
        "technology": "technology",
        "ascension_perks": "ascension_perk",
        "scripted_triggers": "scripted_trigger",
        "script_values": "scripted_value",
        "strategic_resources": "resource",
        "starbase_modules": "starbase_module",
        "starbase_buildings": "starbase_building",
        "ai_budget": "ai_budget",
        "economic_plans": "economic_plan",
        "planet_classes": "planet_class",
    }
    for root in object_inventory_roots(snapshot_root):
        common = root / "common"
        if not common.exists():
            continue
        for folder, bucket in folder_map.items():
            folder_path = common / folder
            if not folder_path.exists():
                continue
            for file_path in iter_text_files(folder_path):
                try:
                    parsed = parse_file(file_path)
                except PDXParseError:
                    continue
                for assignment in block_assignments(parsed):
                    if not assignment.key.startswith("@"):
                        buckets[bucket].add(assignment.key)
    vanilla = Path(r"C:\Steam\steamapps\common\Stellaris\common")
    if vanilla.exists():
        for folder, bucket in folder_map.items():
            folder_path = vanilla / folder
            if not folder_path.exists():
                continue
            for file_path in iter_text_files(folder_path):
                try:
                    parsed = parse_file(file_path)
                except PDXParseError:
                    continue
                for assignment in block_assignments(parsed):
                    if not assignment.key.startswith("@"):
                        buckets[bucket].add(assignment.key)
    return buckets


def block_has_assignment(value: PDXValue, key: str) -> bool:
    return isinstance(value, PDXBlock) and any(assignment.key == key for assignment in iter_assignments(value))


def integration_policy_recommendation(mod_id: str, object_type: str, name: str, has_ai_weight: bool) -> tuple[str, str]:
    lowered = name.lower()
    if object_type in {"component_template", "ship_size"}:
        return ("preserve_parent_design_ai", "defer_direct_override_parent_ai_weight_present" if has_ai_weight else "audit_parent_gap")
    if object_type == "megastructure":
        if any(token in lowered for token in ROI_TARGETS):
            return ("roi_driven_build_priority", "candidate_megastructure_weight_surface")
        return ("observe_for_exotic_or_path_specific_gate", "defer_until_roi_candidate")
    if object_type == "technology":
        if mod_id == "2648658105":
            return ("component_unlock_priority", "candidate_tech_weight_surface")
        if mod_id == "683230077":
            return ("shipyard_and_ship_size_unlock_priority", "candidate_tech_weight_surface")
        if mod_id == "3250900527":
            return ("defensive_starbase_unlock_priority", "candidate_tech_weight_surface")
        if any(token in lowered for token in ("mega", "giga", "ehof", "sentient", "negative", "amb", "shipyard")):
            return ("mega_giga_unlock_priority", "candidate_tech_weight_surface")
        return ("audit_unlock_chain", "defer_unless_core_path")
    if object_type in {"ascension_perk", "tradition"}:
        return ("unlock_path_audit", "candidate_weight_surface" if has_ai_weight else "document_parent_or_engine_surface")
    if object_type in {"starbase_module", "starbase_building"}:
        return ("defensive_or_shipyard_starbase_policy", "candidate_starbase_weight_surface")
    if object_type == "building":
        return ("planetary_capacity_audit", "defer_broad_planet_automation_override")
    return ("audit_only", "defer")


def integration_policy_priority_band(row: dict[str, Any]) -> str:
    recommendation = row.get("policy_recommendation", "")
    object_type = row.get("object_type", "")
    if recommendation == "component_unlock_priority":
        return "advanced_military_component_unlocks"
    if recommendation == "mega_giga_unlock_priority":
        return "mega_giga_unlock_chain"
    if recommendation == "shipyard_and_ship_size_unlock_priority":
        return "shipyard_fleet_throughput_unlocks"
    if recommendation == "defensive_starbase_unlock_priority":
        return "defensive_starbase_unlocks"
    if recommendation == "roi_driven_build_priority":
        return "roi_driven_mega_giga_builds"
    if recommendation == "defensive_or_shipyard_starbase_policy":
        return "defensive_or_shipyard_starbase_policy"
    if recommendation == "planetary_capacity_audit":
        return "planetary_and_building_capacity"
    if recommendation == "preserve_parent_design_ai":
        return "nsc3_esc_parent_design_ai_preservation"
    if object_type in {"ascension_perk", "tradition"}:
        return "ap_tradition_unlock_path"
    return "audit_only"


def integration_policy_audit_status(
    row: dict[str, Any],
    manifest: dict[str, dict[str, str]],
) -> tuple[str, str, bool]:
    required = ("phase", "mod_id", "object_type", "object_name", "source_file", "validation_basis")
    missing = [key for key in required if not row.get(key)]
    if missing:
        return "fail", f"missing required fields: {', '.join(missing)}", False
    mod_row = manifest.get(str(row["mod_id"]))
    if not mod_row:
        return "fail", f"missing source snapshot for mod_id={row['mod_id']}", False
    source_path = Path(mod_row["snapshot_path"]) / str(row["source_file"])
    source_exists = source_path.exists()
    if not source_exists:
        return "fail", f"referenced source file does not exist: {row['source_file']}", False
    if row.get("validation_basis") != "parsed_source_object_exists":
        return "fail", f"unexpected validation basis: {row.get('validation_basis')}", True
    intervention = str(row.get("minimum_v1_intervention", ""))
    if intervention in {
        "candidate_tech_weight_surface",
        "candidate_weight_surface",
        "candidate_megastructure_weight_surface",
        "candidate_starbase_weight_surface",
    }:
        return "ready", "candidate source exists and is eligible for a later scoped generated policy", True
    if intervention == "audit_parent_gap":
        return "warning", "parent object lacks AI weight; audit before overriding parent design logic", True
    if intervention in {
        "defer_direct_override_parent_ai_weight_present",
        "defer_until_roi_candidate",
        "defer_unless_core_path",
        "defer_broad_planet_automation_override",
        "document_parent_or_engine_surface",
    }:
        return "deferred", f"minimum V1 intervention is {intervention}", True
    return "warning", f"unrecognized intervention classification: {intervention}", True


def collect_integration_policy_audit_rows(
    rows: list[dict[str, Any]] | None = None,
    snapshot_root: Path = SNAPSHOT_ROOT,
) -> list[dict[str, Any]]:
    rows = rows if rows is not None else collect_integration_surface_rows(snapshot_root)
    manifest = read_snapshot_manifest(snapshot_root)
    audit_rows: list[dict[str, Any]] = []
    for row in rows:
        status, reason, source_exists = integration_policy_audit_status(row, manifest)
        audit_rows.append(
            {
                "phase": row.get("phase", ""),
                "mod_id": row.get("mod_id", ""),
                "mod_name": row.get("mod_name", ""),
                "object_type": row.get("object_type", ""),
                "object_name": row.get("object_name", ""),
                "source_file": row.get("source_file", ""),
                "source_exists": "yes" if source_exists else "no",
                "source_has_ai_weight": row.get("source_has_ai_weight", ""),
                "policy_recommendation": row.get("policy_recommendation", ""),
                "priority_band": integration_policy_priority_band(row),
                "minimum_v1_intervention": row.get("minimum_v1_intervention", ""),
                "status": status,
                "reason": reason,
            }
        )
    audit_rows.sort(
        key=lambda row: (
            row["phase"],
            row["status"],
            row["object_type"],
            row["priority_band"],
            row["object_name"],
        )
    )
    return audit_rows


def integration_policy_audit_report_text(rows: list[dict[str, Any]]) -> str:
    status_counts: dict[tuple[str, str], int] = {}
    band_counts: dict[tuple[str, str, str], int] = {}
    for row in rows:
        status_counts[(row["phase"], row["status"])] = status_counts.get((row["phase"], row["status"]), 0) + 1
        key = (row["phase"], row["priority_band"], row["status"])
        band_counts[key] = band_counts.get(key, 0) + 1
    lines = [
        "# Stellar AI Director Integration Policy Audit",
        "",
        "Generated from parsed P6-P11 parent source objects. This is a readiness and reference-existence gate, not a broad override emitter.",
        "",
        "## Status Counts",
        "",
        "| phase | status | rows |",
        "| --- | --- | ---: |",
        *[f"| {phase} | {status} | {count} |" for (phase, status), count in sorted(status_counts.items())],
        "",
        "## Priority Bands",
        "",
        "| phase | priority band | status | rows |",
        "| --- | --- | --- | ---: |",
        *[
            f"| {phase} | {band} | {status} | {count} |"
            for (phase, band, status), count in sorted(band_counts.items())
        ],
        "",
        "## Attention Rows",
        "",
        "| phase | object | type | status | priority band | reason |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    attention = [row for row in rows if row["status"] in {"fail", "warning"}]
    if not attention:
        lines.append("| summary |  |  | ok |  | No warnings or failures. |")
    for row in attention[:120]:
        lines.append(
            f"| {row['phase']} | `{row['object_name']}` | {row['object_type']} | {row['status']} | "
            f"{row['priority_band']} | {row['reason']} |"
        )
    return "\n".join(lines) + "\n"


def generate_integration_policy_audit_artifacts(
    rows: list[dict[str, Any]] | None = None,
    snapshot_root: Path = SNAPSHOT_ROOT,
) -> list[dict[str, Any]]:
    audit_rows = collect_integration_policy_audit_rows(rows, snapshot_root)
    write_csv(INTEGRATION_POLICY_AUDIT_CSV, audit_rows)
    write_text_file(INTEGRATION_POLICY_AUDIT_MD, integration_policy_audit_report_text(audit_rows))
    return audit_rows


def collect_integration_surface_rows(snapshot_root: Path = SNAPSHOT_ROOT) -> list[dict[str, Any]]:
    manifest = read_snapshot_manifest(snapshot_root)
    rows: list[dict[str, Any]] = []
    for mod_id, expected_name in REQUIRED_MODS.items():
        mod_row = manifest.get(mod_id)
        if not mod_row:
            continue
        root = Path(mod_row["snapshot_path"])
        common = root / "common"
        if not common.exists():
            continue
        for folder, (object_type, phase) in INTEGRATION_SURFACE_FOLDERS.items():
            folder_path = common / folder
            if not folder_path.exists():
                continue
            for file_path in iter_text_files(folder_path):
                try:
                    parsed = parse_file(file_path)
                except PDXParseError:
                    continue
                source_file = file_path.relative_to(root).as_posix()
                for assignment in block_assignments(parsed):
                    if assignment.key.startswith("@"):
                        continue
                    has_ai_weight = block_has_assignment(assignment.value, "ai_weight")
                    recommendation, intervention = integration_policy_recommendation(
                        mod_id, object_type, assignment.key, has_ai_weight
                    )
                    rows.append(
                        {
                            "phase": phase,
                            "mod_id": mod_id,
                            "mod_name": mod_row.get("name", expected_name),
                            "object_type": object_type,
                            "object_name": assignment.key,
                            "source_file": source_file,
                            "source_has_ai_weight": "yes" if has_ai_weight else "no",
                            "policy_recommendation": recommendation,
                            "minimum_v1_intervention": intervention,
                            "validation_basis": "parsed_source_object_exists",
                        }
                    )
    rows.sort(key=lambda row: (row["phase"], row["object_type"], row["mod_id"], row["object_name"]))
    return rows


def atlas_source_roots(snapshot_root: Path = SNAPSHOT_ROOT) -> list[dict[str, Any]]:
    roots = [
        {
            "mod_id": "vanilla",
            "mod_name": "Stellaris vanilla 4.4.4",
            "source_root": STELLARIS_INSTALL_ROOT,
            "coverage_status": "available" if STELLARIS_INSTALL_ROOT.exists() else "missing",
        }
    ]
    manifest = read_snapshot_manifest(snapshot_root)
    for mod_id, expected_name in REQUIRED_MODS.items():
        row = manifest.get(mod_id)
        path = Path(row["snapshot_path"]) if row else Path()
        roots.append(
            {
                "mod_id": mod_id,
                "mod_name": row.get("name", expected_name) if row else expected_name,
                "source_root": path,
                "coverage_status": "available" if path.exists() else "missing_snapshot",
            }
        )
    if not any(UNIVERSAL_RESOURCE_PATCH_NAME.lower() in root["mod_name"].lower() for root in roots):
        roots.append(
            {
                "mod_id": "universal_resource_patch",
                "mod_name": UNIVERSAL_RESOURCE_PATCH_NAME,
                "source_root": Path(),
                "coverage_status": "missing_snapshot",
            }
        )
    return roots


def atlas_common_folder(root: Path, folder: str) -> Path:
    return root / "common" / folder


def atlas_events_folder(root: Path) -> Path:
    return root / "events"


def block_has_any_assignment(value: PDXValue, keys: set[str]) -> bool:
    return isinstance(value, PDXBlock) and any(assignment.key in keys for assignment in iter_assignments(value))


def assignment_atoms(value: PDXValue) -> list[str]:
    if isinstance(value, PDXAtom):
        return [value.value]
    return block_atoms(value)


def compact_list(values: Iterable[str]) -> str:
    return ";".join(sorted({value for value in values if value}))


def object_route_ids(object_id: str, object_type: str) -> list[str]:
    haystack = f"{object_id} {object_type}".lower()
    return [
        route_id
        for route_id, hints in ROUTE_OBJECT_HINTS.items()
        if any(hint in haystack for hint in hints)
    ]


def strategic_role_for_object(object_id: str, object_type: str) -> str:
    lowered = object_id.lower()
    if object_type in {"technology", "ascension_perk", "tradition"}:
        return "mandatory_unlock" if object_route_ids(object_id, object_type) else "prerequisite_only"
    if object_type == "megastructure":
        if any(token in lowered for token in ("dyson", "gigaforge", "nidavellir", "matrioshka")):
            return "economy_multiplier"
        if any(token in lowered for token in ("planetcraft", "war_moon", "attack_moon", "systemcraft")):
            return "direct_combat_power"
        return "prerequisite_only" if object_route_ids(object_id, object_type) else "unknown_manual_review"
    if object_type in {"ship_size", "component_template", "section_template"}:
        return "direct_combat_power" if object_route_ids(object_id, object_type) else "flavor_low_impact"
    if object_type in {"starbase_module", "starbase_building"}:
        return "defensive_infrastructure"
    if object_type in {"building", "district", "pop_job", "deposit"}:
        if any(token in lowered for token in ("habitat", "orbital", "capacity", "assembly", "growth")):
            return "tall_scaling"
        return "flavor_low_impact"
    if object_type == "resource":
        if any(token in lowered for token in ("sentient", "negative", "dark_matter", "megaconstruction", "supertensile")):
            return "special_resource_producer"
        return "flavor_low_impact"
    if object_type in {"ai_budget", "economic_plan", "scripted_trigger", "scripted_effect", "scripted_value"}:
        return "prerequisite_only"
    if object_type == "event":
        return "unknown_manual_review" if object_route_ids(object_id, object_type) else "flavor_low_impact"
    return "unknown_manual_review"


def strategic_tier_for_object(object_id: str, object_type: str) -> str:
    lowered = object_id.lower()
    if any(token in lowered for token in ("systemcraft", "war_system")):
        return "systemcraft"
    if any(token in lowered for token in ("planetcraft", "planet_behemoth", "war_moon", "attack_moon")):
        return "planetcraft"
    if any(token in lowered for token in ("mega", "giga", "shipyard", "dark_matter", "strikecraft_5")):
        return "midgame"
    if object_type in {"building", "district", "pop_job"}:
        return "fallback"
    return "manual_review" if strategic_role_for_object(object_id, object_type) == "unknown_manual_review" else "opening"


def parent_ai_support_status(source_has_ai_weight: str, strategic_role: str) -> str:
    if source_has_ai_weight == "yes":
        if strategic_role in {"flavor_low_impact", "defensive_infrastructure"}:
            return "parent_ai_complete"
        return "parent_ai_partial"
    if strategic_role == "unknown_manual_review":
        return "parent_ai_unknown"
    return "parent_ai_absent"


def director_action_for_object(object_type: str, strategic_role: str, support_status: str) -> str:
    if strategic_role == "flavor_low_impact":
        return "observe"
    if strategic_role == "unknown_manual_review":
        return "manual_review"
    if support_status == "parent_ai_complete":
        return "supplement_prerequisites"
    if object_type in {"technology", "ascension_perk", "tradition"}:
        return "research"
    if object_type in {"megastructure", "building", "district", "starbase_module", "starbase_building"}:
        return "build"
    if object_type in {"ship_size", "component_template", "section_template"}:
        return "design_ship"
    if object_type == "resource":
        return "increase_income"
    return "observe"


def first_child_assignment(value: PDXValue, key: str) -> PDXAssignment | None:
    if not isinstance(value, PDXBlock):
        return None
    assignments = block_assignments(value, key)
    return assignments[0] if assignments else None


def atlas_object_row(
    *,
    root: dict[str, Any],
    object_type: str,
    object_id: str,
    source_file: str,
    value: PDXValue,
    load_winner: str,
    variables: dict[str, float],
) -> dict[str, Any]:
    cost_assignment = first_child_assignment(value, "cost")
    upkeep_assignment = first_child_assignment(value, "upkeep")
    produces_assignment = first_child_assignment(value, "produces")
    cost = resource_block_to_dict(cost_assignment.value, variables) if cost_assignment else {}
    upkeep = resource_block_to_dict(upkeep_assignment.value, variables) if upkeep_assignment else {}
    produces = resource_block_to_dict(produces_assignment.value, variables) if produces_assignment else {}
    prereqs: list[str] = []
    upgrade_from: list[str] = []
    unlocks: list[str] = []
    event_flags: list[str] = []
    potential_allow_gates: list[str] = []
    if isinstance(value, PDXBlock):
        for assignment in iter_assignments(value):
            if assignment.key == "prerequisites":
                prereqs.extend(assignment_atoms(assignment.value))
            elif assignment.key == "upgrade_from":
                upgrade_from.extend(assignment_atoms(assignment.value))
            elif assignment.key in {"feature_flags", "feature_flag", "show_tech_unlock_if"}:
                unlocks.extend(assignment_atoms(assignment.value))
            elif assignment.key in {"has_country_flag", "set_country_flag", "has_global_flag", "set_global_flag"}:
                event_flags.extend(assignment_atoms(assignment.value))
            elif assignment.key in {"potential", "allow", "possible", "trigger"}:
                potential_allow_gates.append(assignment.key)
    strategic_role = strategic_role_for_object(object_id, object_type)
    support_status = parent_ai_support_status("yes" if block_has_any_assignment(value, ATLAS_AI_SIGNAL_KEYS) else "no", strategic_role)
    route_ids = object_route_ids(object_id, object_type)
    director_action = director_action_for_object(object_type, strategic_role, support_status)
    return {
        "object_id": object_id,
        "object_type": object_type,
        "mod_id": root["mod_id"],
        "mod_name": root["mod_name"],
        "source_file": source_file,
        "load_winner": load_winner,
        "source_has_ai_weight": "yes" if block_has_any_assignment(value, ATLAS_AI_SIGNAL_KEYS) else "no",
        "ai_weight_summary": "ai_signal_present" if block_has_any_assignment(value, ATLAS_AI_SIGNAL_KEYS) else "",
        "cost": compact_resource_map(cost),
        "upkeep": compact_resource_map(upkeep),
        "produces": compact_resource_map(produces),
        "prerequisites": compact_list(prereqs),
        "potential_allow_gates": compact_list(potential_allow_gates),
        "event_flags": compact_list(event_flags),
        "upgrade_from": compact_list(upgrade_from),
        "upgrades_to": "",
        "unlocks": compact_list(unlocks),
        "strategic_role": strategic_role,
        "strategic_tier": strategic_tier_for_object(object_id, object_type),
        "route_ids": compact_list(route_ids),
        "parent_ai_support": support_status,
        "policy_status": "needs_route_policy" if route_ids and strategic_role != "flavor_low_impact" else "parent_ai_ok",
        "director_action": director_action,
        "validation_status": "ok",
    }


def event_object_id(value: PDXValue, fallback: str) -> str:
    if isinstance(value, PDXBlock):
        for assignment in block_assignments(value, "id"):
            atom = atom_value(assignment.value)
            if atom:
                return atom
    return fallback


def collect_object_atlas_rows(snapshot_root: Path = SNAPSHOT_ROOT) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_roots = [root for root in atlas_source_roots(snapshot_root) if root["coverage_status"] == "available"]
    for root in source_roots:
        source_root = Path(root["source_root"])
        global_variables = collect_global_variables([source_root])
        for folder, object_type in ATLAS_COMMON_SURFACES.items():
            folder_path = atlas_common_folder(source_root, folder)
            if not folder_path.exists():
                continue
            for file_path in iter_text_files(folder_path):
                source_file = file_path.relative_to(source_root).as_posix()
                try:
                    parsed = parse_file(file_path)
                except PDXParseError as exc:
                    rows.append(
                        {
                            "object_id": file_path.stem,
                            "object_type": f"{object_type}_parser_gap",
                            "mod_id": root["mod_id"],
                            "mod_name": root["mod_name"],
                            "source_file": source_file,
                            "load_winner": "unknown",
                            "source_has_ai_weight": "unknown",
                            "ai_weight_summary": "",
                            "cost": "",
                            "upkeep": "",
                            "produces": "",
                            "prerequisites": "",
                            "potential_allow_gates": "",
                            "event_flags": "",
                            "upgrade_from": "",
                            "upgrades_to": "",
                            "unlocks": "",
                            "strategic_role": "unknown_manual_review",
                            "strategic_tier": "manual_review",
                            "route_ids": "",
                            "parent_ai_support": "parent_ai_unknown",
                            "policy_status": "unknown",
                            "director_action": "manual_review",
                            "validation_status": f"parser_gap:{exc}",
                        }
                    )
                    continue
                for assignment in block_assignments(parsed):
                    if assignment.key.startswith("@"):
                        continue
                    rows.append(
                        atlas_object_row(
                            root=root,
                            object_type=object_type,
                            object_id=assignment.key,
                            source_file=source_file,
                            value=assignment.value,
                            load_winner="pending",
                            variables=global_variables,
                        )
                    )
        event_root = atlas_events_folder(source_root)
        if event_root.exists():
            for file_path in iter_text_files(event_root):
                source_file = file_path.relative_to(source_root).as_posix()
                try:
                    parsed = parse_file(file_path)
                except PDXParseError as exc:
                    rows.append(
                        {
                            "object_id": file_path.stem,
                            "object_type": "event_parser_gap",
                            "mod_id": root["mod_id"],
                            "mod_name": root["mod_name"],
                            "source_file": source_file,
                            "load_winner": "unknown",
                            "source_has_ai_weight": "unknown",
                            "ai_weight_summary": "",
                            "cost": "",
                            "upkeep": "",
                            "produces": "",
                            "prerequisites": "",
                            "potential_allow_gates": "",
                            "event_flags": "",
                            "upgrade_from": "",
                            "upgrades_to": "",
                            "unlocks": "",
                            "strategic_role": "unknown_manual_review",
                            "strategic_tier": "manual_review",
                            "route_ids": "",
                            "parent_ai_support": "parent_ai_unknown",
                            "policy_status": "unknown",
                            "director_action": "manual_review",
                            "validation_status": f"parser_gap:{exc}",
                        }
                    )
                    continue
                for assignment in block_assignments(parsed):
                    if not assignment.key.endswith("_event"):
                        continue
                    object_id = event_object_id(assignment.value, f"{file_path.stem}:{assignment.key}")
                    rows.append(
                        atlas_object_row(
                            root=root,
                            object_type="event",
                            object_id=object_id,
                            source_file=source_file,
                            value=assignment.value,
                            load_winner="pending",
                            variables=global_variables,
                        )
                    )
    winning_signature_by_key: dict[tuple[str, str], tuple[str, str]] = {}
    for row in rows:
        if row["validation_status"] == "ok":
            winning_signature_by_key[(row["object_type"], row["object_id"])] = (row["mod_id"], row["source_file"])
    for row in rows:
        key = (row["object_type"], row["object_id"])
        signature = (row["mod_id"], row["source_file"])
        if row["validation_status"] == "ok":
            row["load_winner"] = "yes" if winning_signature_by_key.get(key) == signature else "no"
    upgrade_edges = collect_dependency_edges(rows)
    upgrades_by_source: dict[str, set[str]] = {}
    for edge in upgrade_edges:
        if edge["edge_type"] == "upgrades_to":
            upgrades_by_source.setdefault(edge["source_id"], set()).add(edge["target_id"])
    for row in rows:
        row["upgrades_to"] = compact_list(upgrades_by_source.get(row["object_id"], set()))
    rows.sort(key=lambda row: (row["object_type"], row["object_id"], row["mod_id"], row["source_file"]))
    return rows


def collect_dependency_edges(atlas_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    valid_nodes = {(row["object_type"], row["object_id"]) for row in atlas_rows if row["validation_status"] == "ok"}
    valid_ids = {row["object_id"] for row in atlas_rows if row["validation_status"] == "ok"}

    def add_edge(row: dict[str, Any], edge_type: str, target_id: str, target_type: str, evidence: str) -> None:
        target_status = "ok" if target_id in valid_ids or (target_type, target_id) in valid_nodes else "manual_or_external"
        edges.append(
            {
                "source_id": row["object_id"],
                "source_type": row["object_type"],
                "edge_type": edge_type,
                "target_id": target_id,
                "target_type": target_type,
                "target_status": target_status,
                "source_file": row["source_file"],
                "evidence": evidence,
            }
        )

    row_by_id = {row["object_id"]: row for row in atlas_rows if row["validation_status"] == "ok"}
    for row in atlas_rows:
        if row["validation_status"] != "ok":
            continue
        for prereq in row["prerequisites"].split(";") if row["prerequisites"] else []:
            add_edge(row, "requires_technology", prereq, "technology", "prerequisites")
        for resource in re.findall(r"([^=;]+)=", row["cost"]):
            add_edge(row, "requires_resource_stockpile", resource, "resource", "cost")
        for resource in re.findall(r"([^=;]+)=", row["upkeep"]):
            add_edge(row, "requires_resource_income", resource, "resource", "upkeep")
        for resource in re.findall(r"([^=;]+)=", row["produces"]):
            add_edge(row, "produces_resource", resource, "resource", "produces")
        for upstream in row["upgrade_from"].split(";") if row["upgrade_from"] else []:
            add_edge(row, "upgrades_from", upstream, row["object_type"], "upgrade_from")
            upstream_row = row_by_id.get(upstream)
            if upstream_row:
                add_edge(upstream_row, "upgrades_to", row["object_id"], row["object_type"], "upgrade_from")
        for flag in row["event_flags"].split(";") if row["event_flags"] else []:
            add_edge(row, "flag_gate_or_effect", flag, "flag", "event_flags")
        for unlocked in row["unlocks"].split(";") if row["unlocks"] else []:
            add_edge(row, "unlocks_object", unlocked, "object", "unlocks")
        for route_id in row["route_ids"].split(";") if row["route_ids"] else []:
            add_edge(row, "belongs_to_route", route_id, "route", "route_hint")
    edges.sort(key=lambda edge: (edge["edge_type"], edge["source_type"], edge["source_id"], edge["target_id"]))
    return edges


def collect_parent_ai_support_rows(atlas_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "object_id": row["object_id"],
            "object_type": row["object_type"],
            "mod_id": row["mod_id"],
            "mod_name": row["mod_name"],
            "source_file": row["source_file"],
            "source_has_ai_weight": row["source_has_ai_weight"],
            "parent_ai_support": row["parent_ai_support"],
            "strategic_role": row["strategic_role"],
            "route_ids": row["route_ids"],
            "director_requirement": row["director_action"],
        }
        for row in atlas_rows
        if row["validation_status"] == "ok"
    ]
    rows.sort(key=lambda row: (row["parent_ai_support"], row["object_type"], row["object_id"]))
    return rows


def collect_policy_matrix_rows(atlas_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in atlas_rows:
        if row["validation_status"] != "ok":
            continue
        route_ids = row["route_ids"].split(";") if row["route_ids"] else []
        if not route_ids and row["strategic_role"] in {"flavor_low_impact", "prerequisite_only"}:
            continue
        for route_id in route_ids or ["manual_review"]:
            parent_strategy = "reuse"
            if row["parent_ai_support"] == "parent_ai_absent":
                parent_strategy = "override"
            elif row["parent_ai_support"] in {"parent_ai_partial", "parent_ai_present_but_wrong_goal"}:
                parent_strategy = "supplement"
            priority = "high" if route_id != "manual_review" else "medium"
            if row["strategic_role"] == "unknown_manual_review":
                priority = "manual_review"
            rows.append(
                {
                    "object_id": row["object_id"],
                    "object_type": row["object_type"],
                    "route_id": route_id,
                    "priority_band": priority,
                    "timing": row["strategic_tier"],
                    "empire_context": "high_scale_supported_playset",
                    "prereq_state": "see_dependency_edges",
                    "desired_action": row["director_action"],
                    "weight_formula": "",
                    "safety_gates": "no_core_deficit;route_prerequisites_resolved",
                    "parent_ai_strategy": parent_strategy,
                    "source_file": row["source_file"],
                    "notes": f"{row['strategic_role']} with {row['parent_ai_support']}",
                }
            )
    rows.sort(key=lambda row: (row["route_id"], row["priority_band"], row["object_type"], row["object_id"]))
    return rows


def object_atlas_schema_text() -> str:
    fields = [
        "object_id",
        "object_type",
        "mod_id",
        "mod_name",
        "source_file",
        "load_winner",
        "source_has_ai_weight",
        "ai_weight_summary",
        "cost",
        "upkeep",
        "produces",
        "prerequisites",
        "potential_allow_gates",
        "event_flags",
        "upgrade_from",
        "upgrades_to",
        "unlocks",
        "strategic_role",
        "strategic_tier",
        "route_ids",
        "parent_ai_support",
        "policy_status",
        "director_action",
        "validation_status",
    ]
    return (
        "# Stellar AI Director Object Atlas Schema\n\n"
        "Generated by `tools/generate_stellar_ai_director_patch.py`. The atlas is the source of truth for "
        "dependency edges, parent-AI support classification, route policy rows, and later generated AI weights.\n\n"
        "## Fields\n\n"
        + "\n".join(f"- `{field}`" for field in fields)
        + "\n\n## Rules\n\n"
        "- Parser gaps are retained as rows with `validation_status` beginning `parser_gap`.\n"
        "- Policy rows may reference only object IDs present in this atlas.\n"
        "- Broad gameplay weights must not be generated from objects that lack a policy row.\n"
    )


def object_atlas_coverage_text(
    atlas_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    support_rows: list[dict[str, Any]],
    policy_rows: list[dict[str, Any]],
    snapshot_root: Path = SNAPSHOT_ROOT,
) -> str:
    source_roots = atlas_source_roots(snapshot_root)
    counts: dict[tuple[str, str], int] = {}
    parser_gaps = [row for row in atlas_rows if row["validation_status"].startswith("parser_gap")]
    for row in atlas_rows:
        counts[(row["mod_name"], row["object_type"])] = counts.get((row["mod_name"], row["object_type"]), 0) + 1
    lines = [
        "# Stellar AI Director Object Atlas Coverage",
        "",
        "Static coverage for the first real AI knowledge layer. This report is not runtime proof.",
        "",
        "## Source Coverage",
        "",
        "| mod | status | source root |",
        "| --- | --- | --- |",
    ]
    for root in source_roots:
        lines.append(f"| {root['mod_name']} | {root['coverage_status']} | `{root['source_root']}` |")
    lines.extend(
        [
            "",
            "## Artifact Counts",
            "",
            f"- Atlas rows: {len(atlas_rows)}",
            f"- Dependency edges: {len(edge_rows)}",
            f"- Parent-AI support rows: {len(support_rows)}",
            f"- Policy rows: {len(policy_rows)}",
            f"- Parser gaps: {len(parser_gaps)}",
            "",
            "## Counts By Mod And Type",
            "",
            "| mod | object type | rows |",
            "| --- | --- | ---: |",
        ]
    )
    for (mod_name, object_type), count in sorted(counts.items()):
        lines.append(f"| {mod_name} | {object_type} | {count} |")
    if parser_gaps:
        lines.extend(["", "## Parser Gaps", "", "| object | type | file | status |", "| --- | --- | --- | --- |"])
        for row in parser_gaps[:80]:
            lines.append(
                f"| `{row['object_id']}` | {row['object_type']} | `{row['source_file']}` | {row['validation_status']} |"
            )
    return "\n".join(lines) + "\n"


def route_reports_text(
    atlas_rows: list[dict[str, Any]],
    edge_rows: list[dict[str, Any]],
    policy_rows: list[dict[str, Any]],
) -> str:
    lines = [
        "# Stellar AI Director Route Reports",
        "",
        "Generated from atlas route hints, dependency edges, and policy rows. This is a static planning report.",
    ]
    for route_id in ROUTE_OBJECT_HINTS:
        route_objects = [row for row in atlas_rows if route_id in row["route_ids"].split(";")]
        route_edges = [edge for edge in edge_rows if edge["source_id"] in {row["object_id"] for row in route_objects}]
        route_policy = [row for row in policy_rows if row["route_id"] == route_id]
        unresolved = [edge for edge in route_edges if edge["target_status"] != "ok" and edge["target_type"] != "route"]
        lines.extend(
            [
                "",
                f"## {route_id}",
                "",
                f"- Objects: {len(route_objects)}",
                f"- Dependency edges: {len(route_edges)}",
                f"- Policy rows: {len(route_policy)}",
                f"- Manual/external dependency targets: {len(unresolved)}",
                "",
                "| object | type | support | action | source |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for row in route_objects[:40]:
            lines.append(
                f"| `{row['object_id']}` | {row['object_type']} | {row['parent_ai_support']} | "
                f"{row['director_action']} | `{row['source_file']}` |"
            )
    return "\n".join(lines) + "\n"


def validate_object_atlas_artifacts() -> list[str]:
    errors: list[str] = []
    required = [
        OBJECT_ATLAS_SCHEMA_MD,
        OBJECT_ATLAS_CSV,
        DEPENDENCY_EDGES_CSV,
        AI_SUPPORT_MAP_CSV,
        POLICY_MATRIX_CSV,
        OBJECT_ATLAS_COVERAGE_MD,
        ROUTE_REPORT_MD,
    ]
    for path in required:
        if not path.exists():
            errors.append(f"Missing object atlas artifact: {path.relative_to(REPO_ROOT).as_posix()}")
    if errors:
        return errors
    atlas_rows = _read_csv_rows(OBJECT_ATLAS_CSV)
    edge_rows = _read_csv_rows(DEPENDENCY_EDGES_CSV)
    policy_rows = _read_csv_rows(POLICY_MATRIX_CSV)
    atlas_ids = {row["object_id"] for row in atlas_rows if row["validation_status"] == "ok"}
    if not atlas_rows:
        errors.append("Object atlas has no rows.")
    if not edge_rows:
        errors.append("Dependency edge file has no rows.")
    missing_policy_objects = [row["object_id"] for row in policy_rows if row["object_id"] not in atlas_ids]
    if missing_policy_objects:
        errors.append(f"Policy rows reference unknown atlas objects: {', '.join(sorted(set(missing_policy_objects))[:20])}")
    missing_edge_sources = [row["source_id"] for row in edge_rows if row["source_id"] not in atlas_ids]
    if missing_edge_sources:
        errors.append(f"Dependency edges reference unknown source nodes: {', '.join(sorted(set(missing_edge_sources))[:20])}")
    route_policy = [row for row in policy_rows if row["route_id"] != "manual_review"]
    if not route_policy:
        errors.append("Policy matrix has no route-scoped rows.")
    return errors


def generate_object_atlas_artifacts(snapshot_root: Path = SNAPSHOT_ROOT) -> dict[str, list[dict[str, Any]]]:
    atlas_rows = collect_object_atlas_rows(snapshot_root)
    edge_rows = collect_dependency_edges(atlas_rows)
    support_rows = collect_parent_ai_support_rows(atlas_rows)
    policy_rows = collect_policy_matrix_rows(atlas_rows)
    write_text_file(OBJECT_ATLAS_SCHEMA_MD, object_atlas_schema_text())
    write_csv(OBJECT_ATLAS_CSV, atlas_rows)
    write_csv(DEPENDENCY_EDGES_CSV, edge_rows)
    write_csv(AI_SUPPORT_MAP_CSV, support_rows)
    write_csv(POLICY_MATRIX_CSV, policy_rows)
    write_text_file(
        OBJECT_ATLAS_COVERAGE_MD,
        object_atlas_coverage_text(atlas_rows, edge_rows, support_rows, policy_rows, snapshot_root),
    )
    write_text_file(ROUTE_REPORT_MD, route_reports_text(atlas_rows, edge_rows, policy_rows))
    return {
        "atlas": atlas_rows,
        "edges": edge_rows,
        "support": support_rows,
        "policy": policy_rows,
    }


def extract_megastructure_rows(snapshot_root: Path = SNAPSHOT_ROOT) -> list[dict[str, Any]]:
    manifest = read_snapshot_manifest(snapshot_root)
    rows: list[dict[str, Any]] = []
    snapshot_paths = [Path(row["snapshot_path"]) for row in manifest.values()]
    global_variables = collect_global_variables(snapshot_paths)
    market_prices = collect_market_prices(snapshot_paths)
    for mod_id in ("1121692237", "683230077"):
        mod_row = manifest[mod_id]
        mega_root = Path(mod_row["snapshot_path"]) / "common" / "megastructures"
        for file_path in iter_text_files(mega_root):
            if "dummy" in file_path.name.lower():
                continue
            text_path = file_path.relative_to(Path(mod_row["snapshot_path"])).as_posix()
            file_text = read_text(file_path)
            variables = {**global_variables, **collect_variables(file_text)}
            inline_root = Path(mod_row["snapshot_path"]) / "common" / "inline_scripts"
            try:
                parsed = parse_pdx(file_text)
            except PDXParseError:
                continue
            for object_block in block_assignments(parsed):
                name = object_block.key
                lowered = name.lower()
                if not any(target in lowered or target in text_path.lower() for target in ROI_TARGETS):
                    continue
                if not isinstance(object_block.value, PDXBlock):
                    continue
                features = collect_megastructure_features(object_block.value, variables, inline_root)
                cost = features["cost"]
                upkeep = features["upkeep"]
                produces = features["produces"]
                modifiers = features["modifiers"]
                prereqs = features["prereqs"]
                upgrade_from = features["upgrade_from"]
                inline_scripts = features["inline_scripts"]
                has_ai_weight = features["has_ai_weight"]
                build_cost_value = weighted_resource_value(cost)
                upkeep_value = weighted_resource_value(upkeep, monthly=True)
                annual_payoff_value = weighted_resource_value(produces, monthly=True)
                market_base_cost, unpriced_cost = market_resource_value(cost, market_prices, "base_buy")
                market_deficit_cost, unpriced_cost_deficit = market_resource_value(cost, market_prices, "max_buy")
                market_deficit_upkeep, unpriced_upkeep = market_resource_value(upkeep, market_prices, "max_buy", monthly=True)
                market_deficit_payoff, unpriced_produces = market_resource_value(
                    produces, market_prices, "max_buy", monthly=True
                )
                market_surplus_payoff, _ = market_resource_value(produces, market_prices, "min_sell", monthly=True)
                market_fee_deficit_cost, _ = market_resource_value(cost, market_prices, "fee_max_buy")
                market_fee_deficit_payoff, _ = market_resource_value(produces, market_prices, "fee_max_buy", monthly=True)
                unresolved = sorted(unresolved_symbols(cost) | unresolved_symbols(upkeep) | unresolved_symbols(produces))
                shipyard_capacity = numeric_or_zero(modifiers.get("starbase_shipyard_capacity_add", 0.0))
                naval_cap = numeric_or_zero(modifiers.get("country_naval_cap_add", 0.0))
                build_speed = numeric_or_zero(modifiers.get("starbase_shipyard_build_speed_mult", 0.0))
                shipyard_values = shipyard_strategic_values(shipyard_capacity, build_speed, market_prices)
                annual_payoff_value += shipyard_capacity * 450.0
                annual_payoff_value += build_speed * 2500.0
                annual_payoff_value += naval_cap * 2.0
                payback = (build_cost_value + upkeep_value) / annual_payoff_value if annual_payoff_value > 0 else ""
                market_deficit_payback = (
                    (market_deficit_cost + market_deficit_upkeep) / market_deficit_payoff
                    if market_deficit_payoff > 0
                    else ""
                )
                market_surplus_payback = (
                    (market_base_cost + market_deficit_upkeep) / market_surplus_payoff
                    if market_surplus_payoff > 0
                    else ""
                )
                strategic_shipyard_payback = (
                    (market_deficit_cost + market_deficit_upkeep)
                    / shipyard_values["strategic_shipyard_annual_fleet_value_energy"]
                    if shipyard_values["strategic_shipyard_annual_fleet_value_energy"] > 0
                    else ""
                )
                data_quality = classify_data_quality(cost, upkeep, produces, inline_scripts, unresolved)
                decision_eligible = is_decision_eligible(name, cost, annual_payoff_value, data_quality)
                role = director_strategy_role(name, shipyard_capacity, annual_payoff_value, decision_eligible)
                sink_role = director_surplus_sink_role(name, shipyard_capacity, produces, decision_eligible)
                unpriced_resources = {
                    **unpriced_cost,
                    **unpriced_cost_deficit,
                    **unpriced_upkeep,
                    **unpriced_produces,
                }
                rows.append(
                    {
                        "mod_id": mod_id,
                        "mod_name": mod_row["name"],
                        "source_file": text_path,
                        "object_name": name,
                        "cost": compact_resource_map(cost),
                        "upkeep": compact_resource_map(upkeep),
                        "produces": compact_resource_map(produces),
                        "shipyard_capacity": shipyard_capacity,
                        "naval_cap": naval_cap,
                        "build_speed": build_speed,
                        "build_cost_value": round(build_cost_value, 2),
                        "annual_upkeep_value": round(upkeep_value, 2),
                        "annual_payoff_value": round(annual_payoff_value, 2),
                        "payback_years": round(payback, 2) if isinstance(payback, float) else "",
                        "market_base_cost_energy": round(market_base_cost, 2),
                        "market_deficit_cost_energy": round(market_deficit_cost, 2),
                        "market_deficit_annual_upkeep_energy": round(market_deficit_upkeep, 2),
                        "market_deficit_annual_payoff_energy": round(market_deficit_payoff, 2),
                        "market_deficit_payback_years": (
                            round(market_deficit_payback, 2) if isinstance(market_deficit_payback, float) else ""
                        ),
                        "market_surplus_annual_payoff_energy": round(market_surplus_payoff, 2),
                        "market_surplus_payback_years": (
                            round(market_surplus_payback, 2) if isinstance(market_surplus_payback, float) else ""
                        ),
                        "market_fee_deficit_cost_energy": round(market_fee_deficit_cost, 2),
                        "market_fee_deficit_annual_payoff_energy": round(market_fee_deficit_payoff, 2),
                        "market_unpriced_resources": compact_resource_map(unpriced_resources),
                        "strategic_shipyard_effective_slots": round(
                            shipyard_values["strategic_shipyard_effective_slots"], 2
                        ),
                        "strategic_shipyard_annual_alloy_throughput": round(
                            shipyard_values["strategic_shipyard_annual_alloy_throughput"], 2
                        ),
                        "strategic_shipyard_annual_fleet_value_energy": round(
                            shipyard_values["strategic_shipyard_annual_fleet_value_energy"], 2
                        ),
                        "strategic_shipyard_payback_years": (
                            round(strategic_shipyard_payback, 2)
                            if isinstance(strategic_shipyard_payback, float)
                            else ""
                        ),
                        "priority_tier": classify_priority(name, annual_payoff_value, payback, decision_eligible),
                        "source_has_ai_weight": has_ai_weight,
                        "director_strategy_role": role,
                        "director_weight_basis": director_weight_basis(role),
                        "director_build_gate": director_build_gate(role),
                        "director_surplus_sink_role": sink_role,
                        "director_surplus_sink_priority": director_surplus_sink_priority(sink_role),
                        "decision_eligible": "yes" if decision_eligible else "no",
                        "data_quality": data_quality,
                        "unresolved_symbols": " ".join(unresolved),
                        "inline_scripts": " ".join(inline_scripts),
                        "prerequisites": " ".join(prereqs),
                        "upgrade_from": " ".join(upgrade_from),
                    }
                )
    rows.sort(
        key=lambda row: (
            priority_rank(row["priority_tier"]),
            sortable_payback(row),
            row["object_name"],
        )
    )
    return rows


def inline_script_value(block: PDXBlock, key: str) -> str | None:
    for assignment in block_assignments(block, key):
        return atom_value(assignment.value)
    return None


def inline_script_params(block: PDXBlock) -> dict[str, str]:
    params: dict[str, str] = {}
    for assignment in block_assignments(block):
        if assignment.key == "script":
            continue
        value = atom_value(assignment.value)
        if value is None:
            value = serialize_pdx_value(assignment.value)
        params[assignment.key] = value
    return params


def serialize_pdx_value(value: PDXValue) -> str:
    if isinstance(value, PDXAtom):
        return value.value
    parts = ["{"]
    for item in value.items:
        if isinstance(item, PDXAssignment):
            parts.append(f"{item.key} = {serialize_pdx_value(item.value)}")
        else:
            parts.append(item.value)
    parts.append("}")
    return " ".join(parts)


def resolve_inline_script_path(inline_root: Path, script_name: str) -> Path | None:
    script_path = inline_root / f"{script_name}.txt"
    return script_path if script_path.exists() else None


def substitute_inline_params(text: str, params: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        return params.get(match.group(1), "")

    return re.sub(r"\$([A-Za-z0-9_.~!:+-]+)\$", replace, text)


def expand_inline_script(
    block: PDXBlock,
    variables: dict[str, float],
    inline_root: Path,
    depth: int = 0,
) -> PDXBlock | None:
    if depth > 8:
        return None
    script_name = inline_script_value(block, "script")
    if not script_name:
        return None
    script_path = resolve_inline_script_path(inline_root, script_name)
    if script_path is None:
        return None
    expanded_text = substitute_inline_params(read_text(script_path), inline_script_params(block))
    expanded_text = normalize_macro_expressions(expanded_text, variables)
    try:
        parsed = parse_pdx(expanded_text)
    except PDXParseError:
        return None
    top_assignments = block_assignments(parsed)
    if len(top_assignments) == 1 and top_assignments[0].key == "inline_script" and isinstance(top_assignments[0].value, PDXBlock):
        return expand_inline_script(top_assignments[0].value, variables, inline_root, depth + 1)
    return parsed


def collect_megastructure_features(
    value: PDXValue,
    variables: dict[str, float],
    inline_root: Path,
    depth: int = 0,
) -> dict[str, Any]:
    features: dict[str, Any] = {
        "cost": {},
        "upkeep": {},
        "produces": {},
        "modifiers": {},
        "prereqs": [],
        "upgrade_from": [],
        "inline_scripts": [],
        "has_ai_weight": False,
    }
    if not isinstance(value, PDXBlock):
        return features
    for assignment in iter_assignments(value):
        if assignment.key == "cost":
            if block_contains_assignment(assignment.value, "country_uses_bio_ships", "yes"):
                continue
            merge_resource_maps(features["cost"], resource_block_to_dict(assignment.value, variables))
        elif assignment.key == "upkeep":
            merge_resource_maps(features["upkeep"], resource_block_to_dict(assignment.value, variables))
        elif assignment.key == "produces":
            merge_resource_maps(features["produces"], resource_block_to_dict(assignment.value, variables))
        elif assignment.key in {"station_modifier", "country_modifier", "planet_modifier"} and isinstance(
            assignment.value, PDXBlock
        ):
            merge_resource_maps(features["modifiers"], resource_block_to_dict(assignment.value, variables))
        elif assignment.key == "prerequisites" and isinstance(assignment.value, PDXBlock):
            features["prereqs"].extend(block_atoms(assignment.value))
        elif assignment.key == "upgrade_from" and isinstance(assignment.value, PDXBlock):
            features["upgrade_from"].extend(block_atoms(assignment.value))
        elif assignment.key == "ai_weight":
            features["has_ai_weight"] = True
        elif assignment.key == "inline_script" and isinstance(assignment.value, PDXBlock):
            script_name = inline_script_value(assignment.value, "script")
            if script_name:
                features["inline_scripts"].append(script_name)
            expanded = expand_inline_script(assignment.value, variables, inline_root, depth)
            if expanded is None:
                continue
            expanded_features = collect_megastructure_features(expanded, variables, inline_root, depth + 1)
            for key in ("cost", "upkeep", "produces", "modifiers"):
                merge_resource_maps(features[key], expanded_features[key])
            for key in ("prereqs", "upgrade_from", "inline_scripts"):
                features[key].extend(expanded_features[key])
            features["has_ai_weight"] = bool(features["has_ai_weight"] or expanded_features["has_ai_weight"])
    features["prereqs"] = sorted(set(features["prereqs"]))
    features["upgrade_from"] = sorted(set(features["upgrade_from"]))
    features["inline_scripts"] = sorted(set(features["inline_scripts"]))
    return features


def classify_data_quality(
    cost: dict[str, float | str],
    upkeep: dict[str, float | str],
    produces: dict[str, float | str],
    inline_scripts: list[str],
    unresolved: list[str],
) -> str:
    if unresolved:
        return "symbolic_unresolved"
    if not cost and not upkeep and not produces and inline_scripts:
        return "template_wrapper_no_direct_resources"
    if not cost and not upkeep and not produces:
        return "no_resource_effect"
    return "resolved"


def compact_resource_map(resources: dict[str, float | str]) -> str:
    return ";".join(f"{key}={value:g}" if isinstance(value, float) else f"{key}={value}" for key, value in resources.items())


def is_decision_eligible(
    name: str,
    cost: dict[str, float | str],
    payoff: float,
    data_quality: str,
) -> bool:
    lowered = name.lower()
    if data_quality != "resolved":
        return False
    if any(token in lowered for token in ("ruined", "restored")):
        return False
    return bool(cost or payoff > 0)


def director_strategy_role(name: str, shipyard_capacity: float, payoff: float, decision_eligible: bool) -> str:
    if not decision_eligible:
        return "audit_only"
    lowered = name.lower()
    if shipyard_capacity > 0 or "shipyard" in lowered:
        return "fleet_production_sink"
    if any(token in lowered for token in ("gigaforge", "nidavellir", "dyson", "hrae")) and payoff > 0:
        return "economy_multiplier"
    if "matrioshka" in lowered and payoff > 0:
        return "research_multiplier"
    if payoff > 0:
        return "resource_or_modifier_project"
    return "infrastructure_project"


def director_build_gate(role: str) -> str:
    return {
        "fleet_production_sink": "after_research_sink_when_alloy_energy_surplus_needs_fleet_sink",
        "economy_multiplier": "when_survival_clear_and_megastructure_reserve_safe",
        "research_multiplier": "when_research_chain_unlocked_and_economy_can_absorb_upkeep",
        "resource_or_modifier_project": "when_matching_resource_or_modifier_is_current_bottleneck",
        "infrastructure_project": "requires_manual_policy_review",
        "audit_only": "not_a_direct_build_candidate",
    }.get(role, "requires_manual_policy_review")


def director_weight_basis(role: str) -> str:
    return {
        "fleet_production_sink": "strategic_shipyard_throughput",
        "economy_multiplier": "market_deficit_payback_and_resource_bottleneck",
        "research_multiplier": "research_output_and_unlock_chain_value",
        "resource_or_modifier_project": "resource_or_modifier_bottleneck_value",
        "infrastructure_project": "unmodeled_infrastructure_value",
        "audit_only": "not_weighted",
    }.get(role, "unmodeled_infrastructure_value")


def director_surplus_sink_role(
    name: str,
    shipyard_capacity: float,
    produces: dict[str, float | str],
    decision_eligible: bool,
) -> str:
    if not decision_eligible:
        return "not_surplus_sink"
    lowered = name.lower()
    production_keys = set(produces)
    if production_keys & {"physics_research", "society_research", "engineering_research"} or "matrioshka" in lowered:
        return "research_sink"
    if shipyard_capacity > 0 or "shipyard" in lowered:
        return "fleet_sink"
    if "unity" in production_keys:
        return "unity_sink"
    return "not_surplus_sink"


def director_surplus_sink_priority(role: str) -> int | str:
    return {
        "research_sink": 1,
        "fleet_sink": 2,
        "unity_sink": 3,
    }.get(role, "")


def classify_priority(name: str, payoff: float, payback: float | str, decision_eligible: bool = True) -> str:
    if not decision_eligible:
        return "observe_only"
    lowered = name.lower()
    if "shipyard" in lowered and payoff > 10000:
        return "shipyard_multiplier"
    if any(token in lowered for token in ("gigaforge", "nidavellir", "dyson", "hrae")) and payoff > 0:
        return "economy_multiplier"
    if "matrioshka" in lowered and payoff > 0:
        return "research_multiplier"
    if isinstance(payback, float) and payback <= 10:
        return "high_roi"
    return "observe_only"


def priority_rank(tier: str) -> int:
    return {
        "economy_multiplier": 1,
        "shipyard_multiplier": 2,
        "research_multiplier": 3,
        "high_roi": 4,
        "observe_only": 9,
    }.get(tier, 99)


def sortable_payback(row: dict[str, Any]) -> float:
    if row.get("priority_tier") == "shipyard_multiplier" and isinstance(row.get("strategic_shipyard_payback_years"), (int, float)):
        return float(row["strategic_shipyard_payback_years"])
    for key in ("market_deficit_payback_years", "payback_years"):
        value = row.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    return 9999.0


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * fraction)))
    return ordered[index]


def round_to(value: float, step: int) -> int:
    if step <= 0:
        return int(round(value))
    return int(math.ceil(value / step) * step)


def generated_thresholds(rows: list[dict[str, Any]]) -> dict[str, int]:
    eligible = [
        row
        for row in rows
        if row.get("decision_eligible") == "yes"
        and row.get("data_quality") == "resolved"
        and isinstance(row.get("build_cost_value"), (int, float))
        and row["build_cost_value"] > 0
    ]
    economy_costs = [
        float(row["build_cost_value"])
        for row in eligible
        if row.get("priority_tier") in {"economy_multiplier", "research_multiplier", "high_roi"}
        and float(row["build_cost_value"]) <= 300000
    ]
    shipyard_costs = [
        float(row["build_cost_value"])
        for row in eligible
        if row.get("priority_tier") == "shipyard_multiplier" and float(row["build_cost_value"]) <= 300000
    ]
    prep_stockpile = round_to(max(15000.0, percentile(economy_costs, 0.25)), 1000)
    prep_income = round_to(max(120.0, prep_stockpile / 120.0), 10)
    commit_reserve = round_to(max(prep_stockpile * 1.75, percentile(economy_costs, 0.50)), 1000)
    desired_base = round_to(max(25000.0, percentile(economy_costs, 0.25)), 1000)
    desired_mega = round_to(max(50000.0, percentile(economy_costs, 0.50)), 1000)
    desired_prep = round_to(max(75000.0, percentile(economy_costs, 0.75)), 1000)
    desired_commit = round_to(max(100000.0, percentile(economy_costs + shipyard_costs, 0.85)), 1000)
    shipyard_stockpile = round_to(max(10000.0, percentile(shipyard_costs, 0.25)), 1000)
    shipyard_income = round_to(max(150.0, shipyard_stockpile / 120.0), 10)
    return {
        "prep_stockpile_alloys": prep_stockpile,
        "prep_income_alloys": prep_income,
        "commit_stockpile_alloys": commit_reserve,
        "desired_base_alloys": desired_base,
        "desired_mega_engineering_add": desired_mega,
        "desired_prep_add": desired_prep,
        "desired_commit_add": desired_commit,
        "shipyard_stockpile_alloys": shipyard_stockpile,
        "shipyard_income_alloys": shipyard_income,
        "eligible_roi_rows": len(eligible),
    }


def market_price_rows(snapshot_root: Path = SNAPSHOT_ROOT) -> list[dict[str, Any]]:
    manifest = read_snapshot_manifest(snapshot_root)
    prices = collect_market_prices(Path(row["snapshot_path"]) for row in manifest.values())
    rows = []
    for price in sorted(prices.values(), key=lambda item: item.resource):
        rows.append(
            {
                "resource": price.resource,
                "market_amount": price.market_amount,
                "market_price": price.market_price,
                "base_energy_per_unit": round(price.base_energy, 4),
                "min_sell_energy_per_unit_no_fee": round(price.min_sell_energy, 4),
                "max_buy_energy_per_unit_no_fee": round(price.max_buy_energy, 4),
                "base_buy_energy_per_unit_default_fee": round(price.default_fee_base_buy_energy, 4),
                "floor_sell_energy_per_unit_default_fee": round(price.default_fee_floor_sell_energy, 4),
                "ceiling_buy_energy_per_unit_default_fee": round(price.default_fee_ceiling_buy_energy, 4),
            }
        )
    return rows


def roi_quality_status(row: dict[str, Any], check: str) -> tuple[str, str]:
    eligible = row.get("decision_eligible") == "yes"
    object_name = row.get("object_name", "<unknown>")
    if check == "decision_eligible_data_quality":
        quality = row.get("data_quality", "")
        if eligible and quality != "resolved":
            return "fail", f"{object_name} is decision-eligible with data_quality={quality!r}"
        return "ok", "decision eligibility matches resolved data quality"
    if check == "decision_eligible_cost":
        cost = row.get("build_cost_value")
        if eligible and (not isinstance(cost, (int, float)) or float(cost) <= 0):
            return "fail", f"{object_name} is decision-eligible with non-positive build_cost_value={cost!r}"
        return "ok", "decision-eligible rows have positive build cost or the row is audit-only"
    if check == "decision_eligible_unresolved_symbols":
        unresolved = str(row.get("unresolved_symbols", "") or "").strip()
        if eligible and unresolved:
            return "fail", f"{object_name} is decision-eligible with unresolved symbols: {unresolved}"
        return "ok", "decision-eligible row has no unresolved symbols"
    if check == "decision_eligible_market_unpriced_resources":
        unpriced = str(row.get("market_unpriced_resources", "") or "").strip()
        if eligible and unpriced:
            return "warning", f"{object_name} keeps non-market resources as bottleneck notes: {unpriced}"
        return "ok", "no unpriced market resources requiring audit note"
    raise ValueError(f"Unknown ROI quality check: {check}")


def collect_roi_quality_rows(rows: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    rows = rows if rows is not None else extract_megastructure_rows()
    audit_rows: list[dict[str, Any]] = []
    checks = (
        "decision_eligible_data_quality",
        "decision_eligible_cost",
        "decision_eligible_unresolved_symbols",
        "decision_eligible_market_unpriced_resources",
    )
    for row in rows:
        for check in checks:
            status, reason = roi_quality_status(row, check)
            audit_rows.append(
                {
                    "scope": "row",
                    "check": check,
                    "status": status,
                    "object_name": row.get("object_name", ""),
                    "source_file": row.get("source_file", ""),
                    "decision_eligible": row.get("decision_eligible", ""),
                    "data_quality": row.get("data_quality", ""),
                    "build_cost_value": row.get("build_cost_value", ""),
                    "unresolved_symbols": row.get("unresolved_symbols", ""),
                    "market_unpriced_resources": row.get("market_unpriced_resources", ""),
                    "reason": reason,
                }
            )
    thresholds = generated_thresholds(rows)
    eligible_rows = [
        row
        for row in rows
        if row.get("decision_eligible") == "yes"
        and row.get("data_quality") == "resolved"
        and isinstance(row.get("build_cost_value"), (int, float))
        and row["build_cost_value"] > 0
    ]
    threshold_status = "ok" if thresholds["eligible_roi_rows"] == len(eligible_rows) else "fail"
    audit_rows.append(
        {
            "scope": "summary",
            "check": "threshold_eligible_count",
            "status": threshold_status,
            "object_name": "",
            "source_file": "",
            "decision_eligible": len(eligible_rows),
            "data_quality": "",
            "build_cost_value": "",
            "unresolved_symbols": "",
            "market_unpriced_resources": "",
            "reason": (
                f"generated thresholds use {thresholds['eligible_roi_rows']} eligible rows; "
                f"audit counted {len(eligible_rows)}"
            ),
        }
    )
    return audit_rows


def roi_quality_audit_report_text(audit_rows: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for row in audit_rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    lines = [
        "# Stellar AI Director ROI Quality Audit",
        "",
        "Generated from the ROI matrix inputs. `fail` rows block validation; `warning` rows document non-market resources kept as bottleneck notes instead of invented prices.",
        "",
        "## Status Counts",
        "",
        "| status | rows |",
        "| --- | ---: |",
        *[f"| {status} | {count} |" for status, count in sorted(counts.items())],
        "",
        "## Non-OK Rows",
        "",
        "| scope | check | status | object | reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    non_ok_rows = [row for row in audit_rows if row["status"] != "ok"]
    if not non_ok_rows:
        lines.append("| summary | all_checks | ok |  | No warnings or failures. |")
    for row in non_ok_rows[:80]:
        lines.append(
            f"| {row['scope']} | {row['check']} | {row['status']} | `{row['object_name']}` | {row['reason']} |"
        )
    return "\n".join(lines) + "\n"


def generate_roi_quality_audit_artifacts(rows: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    audit_rows = collect_roi_quality_rows(rows)
    write_csv(ROI_QUALITY_AUDIT_CSV, audit_rows)
    write_text_file(ROI_QUALITY_AUDIT_MD, roi_quality_audit_report_text(audit_rows))
    return audit_rows


@dataclass(slots=True)
class EmpireState:
    at_war: bool = False
    recently_lost_war: bool = False
    lost_economy_fraction: float = 0.0
    used_naval_capacity_percent: float = 0.8
    highest_threat: float = 0.0
    incomes: dict[str, float] = field(default_factory=dict)
    stockpiles: dict[str, float] = field(default_factory=dict)
    has_megastructure_prereqs: bool = False
    project_progress: float = 0.0
    has_completed_shipyard_multiplier: bool = False
    shipyard_capacity_bottleneck: bool = False
    wants_fleet_buildup: bool = False
    alloy_stockpile_near_cap: bool = False
    research_sink_available: bool = False
    unity_sink_available: bool = False
    personality: str = "balanced"


TRADE_CAPACITY_RESOURCE = "trade"
TRADE_MIN_MONTHLY_INCOME = 25.0
TRADE_FLEET_MONTHLY_INCOME = 75.0
TRADE_PLANETARY_MONTHLY_INCOME = 50.0
TRADE_SURPLUS_MONTHLY_INCOME = 100.0


def stockpile_runway_months(state: EmpireState, resource: str) -> float:
    income = state.incomes.get(resource, 0.0)
    if income >= 0:
        return math.inf
    return state.stockpiles.get(resource, 0.0) / abs(income) if income < 0 else math.inf


def trade_capacity_known(state: EmpireState) -> bool:
    return TRADE_CAPACITY_RESOURCE in state.incomes or TRADE_CAPACITY_RESOURCE in state.stockpiles


def trade_capacity_pressure(state: EmpireState) -> bool:
    if not trade_capacity_known(state):
        return False
    trade_income = state.incomes.get(TRADE_CAPACITY_RESOURCE, 0.0)
    if trade_income < 0 and stockpile_runway_months(state, TRADE_CAPACITY_RESOURCE) < 24:
        return True
    expansion_pressure = (
        state.wants_fleet_buildup
        or state.has_completed_shipyard_multiplier
        or state.has_megastructure_prereqs
        or state.used_naval_capacity_percent >= 0.95
    )
    return trade_income < TRADE_MIN_MONTHLY_INCOME and expansion_pressure


def trade_capacity_safe(state: EmpireState, minimum_income: float = TRADE_MIN_MONTHLY_INCOME) -> bool:
    if not trade_capacity_known(state):
        return True
    if trade_capacity_pressure(state):
        return False
    return state.incomes.get(TRADE_CAPACITY_RESOURCE, 0.0) >= minimum_income


def core_deficit_with_short_runway(state: EmpireState) -> bool:
    for resource in ("energy", "minerals", "consumer_goods", "food", "alloys", TRADE_CAPACITY_RESOURCE):
        if state.incomes.get(resource, 0.0) < 0 and stockpile_runway_months(state, resource) < 24:
            return True
    return False


def resource_waste_pressure(state: EmpireState) -> bool:
    if core_deficit_with_short_runway(state):
        return False
    for resource, threshold in SURPLUS_WASTE_STOCKPILE_THRESHOLDS.items():
        if state.stockpiles.get(resource, 0.0) >= threshold and state.incomes.get(resource, 0.0) > 0:
            return True
    return False


def research_under_curve(state: EmpireState, years_passed: float = 119.0) -> bool:
    total_research = sum(state.incomes.get(resource, 0.0) for resource in RESEARCH_RESOURCES)
    if years_passed >= 119 and total_research < 3500:
        return True
    if years_passed >= 79 and total_research < 2500:
        return True
    if years_passed >= 44 and total_research < 1200:
        return True
    return False


def surplus_sink_pressure(state: EmpireState) -> bool:
    if core_deficit_with_short_runway(state):
        return False
    if state.incomes.get("energy", 0.0) < 0 or state.incomes.get("alloys", 0.0) < 0:
        return False
    if resource_waste_pressure(state) or research_under_curve(state):
        return True
    if not trade_capacity_safe(state, TRADE_SURPLUS_MONTHLY_INCOME):
        return False
    income_surplus = state.incomes.get("alloys", 0.0) >= 300 and state.incomes.get("energy", 0.0) >= 300
    stockpile_surplus = state.stockpiles.get("alloys", 0.0) >= 20000 or state.alloy_stockpile_near_cap
    return income_surplus and stockpile_surplus


def choose_decision_state(state: EmpireState) -> str:
    if core_deficit_with_short_runway(state) or trade_capacity_pressure(state) or state.lost_economy_fraction >= 0.35:
        return "survival_mode"
    if state.recently_lost_war or any(state.incomes.get(res, 0.0) < 0 for res in ("energy", "minerals", "alloys", TRADE_CAPACITY_RESOURCE)):
        return "recovery_mode"
    if state.at_war and state.used_naval_capacity_percent < 0.85 and state.project_progress < 0.75:
        return "recovery_mode"
    if state.project_progress >= 0.75 and not core_deficit_with_short_runway(state):
        return "investment_commit_mode"
    if state.has_completed_shipyard_multiplier:
        if (
            state.incomes.get("alloys", 0.0) >= 150
            and state.incomes.get("energy", 0.0) >= 100
            and trade_capacity_safe(state, TRADE_FLEET_MONTHLY_INCOME)
        ):
            return "payoff_exploitation_mode"
        return "recovery_mode"
    if surplus_sink_pressure(state):
        if state.research_sink_available:
            return "research_expansion_mode"
        if state.wants_fleet_buildup or state.alloy_stockpile_near_cap or state.incomes.get("alloys", 0.0) >= 500:
            if not state.at_war or state.used_naval_capacity_percent >= 0.85:
                return "shipyard_expansion_mode"
        if state.unity_sink_available:
            return "unity_expansion_mode"
    if (
        state.has_megastructure_prereqs
        and state.incomes.get("alloys", 0.0) >= 120
        and state.stockpiles.get("alloys", 0.0) >= 15000
        and trade_capacity_safe(state, TRADE_PLANETARY_MONTHLY_INCOME)
    ):
        if state.highest_threat < 45 or state.used_naval_capacity_percent >= 0.9:
            return "investment_prep_mode"
    return "normal_growth_mode"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def mod_source_root_for_id(mod_id: str, snapshot_root: Path = SNAPSHOT_ROOT) -> Path:
    if mod_id == "vanilla":
        return STELLARIS_INSTALL_ROOT
    manifest = read_snapshot_manifest(snapshot_root)
    row = manifest.get(mod_id)
    if not row:
        raise ValueError(f"No source snapshot found for mod id {mod_id}")
    return Path(row["snapshot_path"])


def generated_common_folder_for_type(object_type: str) -> str:
    for folder, mapped_type in GENERATED_SURFACE_FOLDERS.items():
        if mapped_type == object_type:
            return folder
    raise ValueError(f"Unsupported generated override type: {object_type}")


def _brace_delta(line: str) -> int:
    in_quote = False
    escaped = False
    delta = 0
    for char in line:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_quote = not in_quote
            continue
        if in_quote:
            continue
        if char == "#":
            break
        if char == "{":
            delta += 1
        elif char == "}":
            delta -= 1
    return delta


def extract_top_level_object_text(source_text: str, object_id: str) -> str:
    pattern = re.compile(rf"(?m)^[ \t]*{re.escape(object_id)}[ \t]*=[ \t]*\{{")
    match = pattern.search(source_text)
    if not match:
        raise ValueError(f"Could not find top-level object {object_id}")
    depth = 0
    start = match.start()
    position = start
    while position < len(source_text):
        line_end = source_text.find("\n", position)
        if line_end == -1:
            line_end = len(source_text)
        line = source_text[position:line_end]
        depth += _brace_delta(line)
        if depth == 0 and position > start:
            return source_text[start : line_end + 1]
        position = line_end + 1
    raise ValueError(f"Could not find closing brace for {object_id}")


def replace_top_level_child_block(block_text: str, child_key: str, replacement_text: str) -> str:
    lines = block_text.rstrip().splitlines()
    output: list[str] = []
    depth = 0
    index = 0
    child_pattern = re.compile(rf"^[ \t]*{re.escape(child_key)}[ \t]*=")
    while index < len(lines):
        line = lines[index]
        if depth == 1 and child_pattern.match(line):
            depth += _brace_delta(line)
            index += 1
            while index < len(lines) and depth > 1:
                depth += _brace_delta(lines[index])
                index += 1
            continue
        output.append(line)
        depth += _brace_delta(line)
        index += 1
    closing_index = len(output) - 1
    while closing_index >= 0 and not re.match(r"^[ \t]*}\s*$", output[closing_index]):
        closing_index -= 1
    if closing_index < 0:
        raise ValueError("Generated block has no final closing brace")
    output[closing_index:closing_index] = ["", *replacement_text.rstrip().splitlines()]
    return "\n".join(output) + "\n"


def replace_or_insert_top_level_scalar(block_text: str, child_key: str, replacement_line: str) -> str:
    lines = block_text.rstrip().splitlines()
    output: list[str] = []
    depth = 0
    replaced = False
    child_pattern = re.compile(rf"^[ \t]*{re.escape(child_key)}[ \t]*=")
    for line in lines:
        if depth == 1 and child_pattern.match(line):
            output.append(replacement_line)
            replaced = True
        else:
            output.append(line)
        depth += _brace_delta(line)
    if replaced:
        return "\n".join(output) + "\n"

    closing_index = len(output) - 1
    while closing_index >= 0 and not re.match(r"^[ \t]*}\s*$", output[closing_index]):
        closing_index -= 1
    if closing_index < 0:
        raise ValueError(f"Generated block has no final closing brace for scalar {child_key}")
    output[closing_index:closing_index] = [replacement_line]
    return "\n".join(output) + "\n"


def director_infrastructure_weight_block(block: str, target: dict[str, Any]) -> str:
    coefficient = str(target.get("coefficient", "4"))
    additional_weight = str(target.get("additional_weight", "400"))
    block = replace_or_insert_top_level_scalar(block, "ai_weight_coefficient", f"\tai_weight_coefficient = {coefficient}")
    return replace_or_insert_top_level_scalar(
        block,
        "additional_ai_weight",
        f"\tadditional_ai_weight = {additional_weight}",
    )


ROUTE_RESEARCH_GATES = {
    "mega_engineering_core": "staid_core_unlock_research_priority_ready",
    "mega_shipyard_core": "staid_core_unlock_research_priority_ready",
    "economy_megastructure_core": "staid_core_unlock_research_priority_ready",
    "gigas_special_resource_core": "staid_gigas_special_resource_unlock_ready",
    "planetcraft_route": "staid_planetcraft_research_priority_ready",
    "war_moon_route": "staid_war_moon_research_priority_ready",
    "systemcraft_route": "staid_systemcraft_research_priority_ready",
    "nsc3_capital_hull_route": "staid_fleet_payoff_exploitation_ready",
    "esc_component_route": "staid_fleet_payoff_exploitation_ready",
    "crowded_tall_route": "staid_planetary_capacity_growth_ready",
    "conquest_escape_route": "staid_aggressive_fleet_pressure",
    "fallen_empire_benchmark_route": "staid_crisis_starbase_pressure",
}

ROUTE_BUILD_GATES = {
    "mega_engineering_core": "staid_core_unlock_research_priority_ready",
    "mega_shipyard_core": "staid_mega_shipyard_build_priority_ready",
    "economy_megastructure_core": "staid_economy_megastructure_build_priority_ready",
    "gigas_special_resource_core": "staid_megastructure_commit_safe",
    "planetcraft_route": "staid_planetcraft_build_priority_ready",
    "war_moon_route": "staid_war_moon_build_priority_ready",
    "systemcraft_route": "staid_systemcraft_build_priority_ready",
    "nsc3_capital_hull_route": "staid_fleet_payoff_exploitation_ready",
    "esc_component_route": "staid_fleet_payoff_exploitation_ready",
    "crowded_tall_route": "staid_planetary_capacity_growth_ready",
    "conquest_escape_route": "staid_aggressive_fleet_pressure",
    "fallen_empire_benchmark_route": "staid_crisis_starbase_pressure",
}

ROUTE_TIMING_FACTORS = {
    "mega_shipyard_core": (3, 5, 8),
    "economy_megastructure_core": (3, 5, 8),
    "gigas_special_resource_core": (3, 5, 8),
    "planetcraft_route": (3, 6, 10),
    "war_moon_route": (3, 6, 10),
    "systemcraft_route": (4, 8, 12),
}

ROUTE_EXTRA_MODIFIERS = {
    "planetcraft_route": [
        "\tmodifier = { factor = 4 has_technology = giga_tech_planet_assembly }",
        "\tmodifier = { factor = 3 has_ascension_perk = ap_celestial_printing }",
    ],
    "war_moon_route": [
        "\tmodifier = { factor = 4 has_technology = giga_tech_war_moon_1 }",
        "\tmodifier = { factor = 6 has_technology = giga_tech_war_moon_2 }",
    ],
    "systemcraft_route": [
        "\tmodifier = { factor = 3 has_ascension_perk = ap_celestial_printing }",
        "\tmodifier = { factor = 4 has_technology = giga_tech_war_system_1 }",
        "\tmodifier = { factor = 5 has_technology = giga_tech_war_system_2 }",
        "\tmodifier = { factor = 6 has_technology = giga_tech_war_system_3 }",
        "\tmodifier = { factor = 8 has_technology = giga_tech_war_system_6 }",
    ],
    "gigas_special_resource_core": [
        "\tmodifier = { factor = 4 has_technology = tech_ehof_sentient_tier_1 }",
        "\tmodifier = { factor = 4 has_technology = tech_nm_utilization_1 }",
        "\tmodifier = { factor = 4 has_technology = giga_tech_amb_supertensiles }",
    ],
}


def route_gate_for_target(target: dict[str, Any]) -> str:
    route_id = str(target["route_id"])
    if target["object_type"] in {"technology", "ascension_perk", "tradition"}:
        return ROUTE_RESEARCH_GATES.get(route_id, "staid_surplus_sink_pressure")
    return ROUTE_BUILD_GATES.get(route_id, "staid_surplus_sink_pressure")


def route_weight_modifiers(target: dict[str, Any]) -> list[str]:
    route_id = str(target["route_id"])
    route_gate = route_gate_for_target(target)
    mid_factor, late_factor, crisis_factor = ROUTE_TIMING_FACTORS.get(route_id, (2, 3, 5))
    lines = [
        "\tmodifier = { factor = 0 staid_survival_mode = yes }",
        "\tmodifier = { factor = 0.35 staid_recovery_mode = yes }",
        f"\tmodifier = {{ factor = 4 {route_gate} = yes }}",
        f"\tmodifier = {{ factor = {mid_factor} years_passed > 44 }}",
        f"\tmodifier = {{ factor = {late_factor} years_passed > 79 }}",
        f"\tmodifier = {{ factor = {crisis_factor} years_passed > 119 }}",
    ]
    lines.extend(ROUTE_EXTRA_MODIFIERS.get(route_id, []))
    return lines


def director_ai_weight_block(target: dict[str, Any]) -> str:
    lines = [
        "\tai_weight = {",
        f"\t\tfactor = {target['weight']}",
        "",
        f"\t\t# policy_route = {target['route_id']}",
        f"\t\t# source_object = {target['object_type']}:{target['object_id']}",
    ]
    lines.extend(line.replace("\t", "\t\t", 1) for line in route_weight_modifiers(target))
    lines.append("\t}")
    return "\n".join(lines) + "\n"


AT_VARIABLE_RE = re.compile(r"(?<![\w])@[A-Za-z0-9_]+(?![\w])")
AT_VARIABLE_DEFINITION_RE = re.compile(r"^[ \t]*(?P<name>@[A-Za-z0-9_]+)[ \t]*=[ \t]*(?P<value>.*)$")


def source_file_variable_definitions(source_text: str) -> dict[str, str]:
    variables: dict[str, str] = {}
    for line in source_text.splitlines():
        match = AT_VARIABLE_DEFINITION_RE.match(line.split("#", 1)[0].rstrip())
        if not match:
            continue
        name = match.group("name")
        variables.setdefault(name, line.rstrip())
    return variables


def used_at_variables_in_text(text: str) -> set[str]:
    used: set[str] = set()
    for raw_line in text.splitlines():
        code = raw_line.split("#", 1)[0]
        definition = AT_VARIABLE_DEFINITION_RE.match(code.rstrip())
        if definition:
            code = definition.group("value")
        used.update(AT_VARIABLE_RE.findall(code))
    return used


def common_scripted_variable_definitions(common_root: Path) -> dict[str, str]:
    variables: dict[str, str] = {}
    scripted_variables = common_root / "scripted_variables"
    if not scripted_variables.exists():
        return variables
    for file_path in iter_text_files(scripted_variables):
        variables.update(source_file_variable_definitions(read_text(file_path)))
    return variables


def source_common_root(source_path: Path) -> Path:
    for parent in source_path.parents:
        if parent.name == "common":
            return parent
    raise ValueError(f"Could not find common/ root for {source_path}")


def route_override_file_variables(file_rows: list[dict[str, Any]]) -> list[str]:
    variables: dict[str, str] = {}
    required: set[str] = set()
    for row in file_rows:
        source_text = read_text(Path(row["source_path"]))
        required.update(used_at_variables_in_text(extract_top_level_object_text(source_text, row["object_id"])))
        for definition_source in (
            source_file_variable_definitions(source_text),
            common_scripted_variable_definitions(source_common_root(Path(row["source_path"]))),
            common_scripted_variable_definitions(STELLARIS_INSTALL_ROOT / "common"),
        ):
            for name, line in definition_source.items():
                if name in required and name not in variables:
                    variables[name] = line
    missing = sorted(required - set(variables))
    if missing:
        raise ValueError(
            f"Missing source-local variable definitions for generated route override file "
            f"{file_rows[0]['generated_file']}: {', '.join(missing)}"
        )
    return [variables[name] for name in sorted(variables)]


def strip_optional_absent_planet_classes(block: str, object_names: dict[str, set[str]]) -> str:
    if "pc_magnetar" in object_names.get("planet_class", set()):
        return block
    # Gigastructural Engineering includes optional Real Space magnetar placement
    # checks in some source megastructures. Director must not make that optional
    # compatibility reference the final load-order owner when Real Space is absent.
    return re.sub(r"[ \t]*is_planet_class[ \t]*=[ \t]*pc_magnetar", "", block)


def generated_unresolved_at_variable_rows(mod_root: Path = MOD_ROOT) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    common = mod_root / "common"
    if not common.exists():
        return rows
    for file_path in iter_text_files(common):
        defined: set[str] = set()
        uses: list[tuple[int, str]] = []
        for line_number, raw_line in enumerate(read_text(file_path).splitlines(), start=1):
            code = raw_line.split("#", 1)[0]
            definition = AT_VARIABLE_DEFINITION_RE.match(code.rstrip())
            if definition:
                defined.add(definition.group("name"))
                code = definition.group("value")
            for variable in AT_VARIABLE_RE.findall(code):
                uses.append((line_number, variable))
        for line_number, variable in uses:
            if variable not in defined:
                rows.append(
                    {
                        "generated_file": file_path.relative_to(mod_root).as_posix(),
                        "line": str(line_number),
                        "variable": variable,
                    }
                )
    return rows


def route_override_target_rows(snapshot_root: Path = SNAPSHOT_ROOT) -> list[dict[str, Any]]:
    atlas_rows = _read_csv_rows(OBJECT_ATLAS_CSV) if OBJECT_ATLAS_CSV.exists() else collect_object_atlas_rows(snapshot_root)
    resolved: list[dict[str, Any]] = []
    for target in ROUTE_OVERRIDE_TARGETS:
        candidates = [
            row
            for row in atlas_rows
            if row["object_id"] == target["object_id"]
            and row["object_type"] == target["object_type"]
            and row["mod_id"] == target["mod_id"]
            and row["validation_status"] == "ok"
        ]
        if target.get("source_file"):
            candidates = [row for row in candidates if row["source_file"] == target["source_file"]]
        candidates.sort(key=lambda row: (row["source_has_ai_weight"] != "yes", row["source_file"]))
        if not candidates:
            raise ValueError(f"No atlas source row found for route override target {target}")
        row = {**candidates[0], **target}
        source_root = mod_source_root_for_id(row["mod_id"], snapshot_root)
        source_path = source_root / row["source_file"]
        if not source_path.exists():
            raise ValueError(f"Missing source file for route override {row['object_id']}: {source_path}")
        row["source_path"] = str(source_path)
        row["generated_folder"] = generated_common_folder_for_type(row["object_type"])
        row.setdefault("coefficient", "")
        row.setdefault("additional_weight", "")
        row["generated_file"] = (
            MOD_ROOT
            / "common"
            / row["generated_folder"]
            / f"zzzz_staid_{row['file_key']}_{row['generated_folder']}.txt"
        ).as_posix()
        resolved.append(row)
    return resolved


def route_override_file_header(folder: str) -> str:
    return (
        "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
        "# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.\n"
        "# Required source-local @variables are copied into this file to preserve parent parse context.\n"
        "# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.\n\n"
        f"# Generated surface: common/{folder}\n\n"
    )


def route_override_object_text(target: dict[str, Any], object_names: dict[str, set[str]] | None = None) -> str:
    source_text = read_text(Path(target["source_path"]))
    block = extract_top_level_object_text(source_text, target["object_id"])
    if target["object_type"] == "megastructure" and object_names is not None:
        block = strip_optional_absent_planet_classes(block, object_names)
    if target["object_type"] in {"building", "district"}:
        block = director_infrastructure_weight_block(block, target)
    else:
        block = replace_top_level_child_block(block, "ai_weight", director_ai_weight_block(target))
    block = "\n".join(line.rstrip() for line in block.splitlines()) + "\n"
    return (
        f"# policy_route = {target['route_id']}; source = {target['source_file']}; "
        f"parent_ai = {target['parent_ai_support']}; source_ai_weight = {target['source_has_ai_weight']}\n"
        + block
    )


def route_override_report_text(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Stellar AI Director Route Override Report",
        "",
        "Generated full-object override surfaces. These are actual mod behavior changes, not atlas-only evidence.",
        "",
        "Load-safety guard: generated override files copy required source-local `@variables` from parent/vanilla scripted variables and strip optional absent `pc_magnetar` placement references from copied Gigas megastructure starts when that Real Space planet class is not present in the supported source inventory.",
        "",
        "| route | object | type | parent strategy | source AI | generated file | source |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        generated_file = Path(row["generated_file"]).relative_to(MOD_ROOT).as_posix()
        lines.append(
            f"| {row['route_id']} | `{row['object_id']}` | {row['object_type']} | "
            f"{row['parent_ai_support']} | {row['source_has_ai_weight']} | `{generated_file}` | `{row['source_file']}` |"
        )
    lines.extend(
        [
            "",
            "## Manual Review Blockers",
            "",
            "- ESC component templates use internal `key = ...` entries in `common/component_templates`; the current atlas does not model those as top-level loader objects, so this generator does not emit guessed component-template overrides.",
            "- NSC3 hull usage is implemented through technology weights, Mega Shipyard/fleet-throughput economy, and reserve pressure until a source-verified ship-design override surface is added.",
            "- Runtime proof still requires an explicit observer run; static validation proves load-safety and reference integrity only.",
        ]
    )
    return "\n".join(lines) + "\n"


def generate_route_override_artifacts() -> list[dict[str, Any]]:
    rows = route_override_target_rows()
    object_names = collect_object_names()
    grouped: dict[Path, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(Path(row["generated_file"]), []).append(row)
    for file_path, file_rows in grouped.items():
        body = [route_override_file_header(file_rows[0]["generated_folder"])]
        variables = route_override_file_variables(file_rows)
        if variables:
            body.append("# Source-local variables required by copied parent objects.")
            body.extend(variables)
            body.append("")
        for row in file_rows:
            body.append(route_override_object_text(row, object_names))
            body.append("")
        write_text_file(file_path, "\n".join(body))
    write_csv(RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.csv", rows)
    write_text_file(
        RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.md",
        route_override_report_text(rows),
    )
    return rows


def axis_vector(values: tuple[int, ...]) -> dict[str, int]:
    return dict(zip(THREAT_RESPONSE_AXES, values, strict=True))


def threat_normal_ethic_rows() -> list[dict[str, Any]]:
    rows = []
    for ethic, values in THREAT_NORMAL_ETHIC_VECTORS.items():
        rows.append({"ethic": ethic, **axis_vector(values)})
    return rows


def threat_fanatic_ethic_rows() -> list[dict[str, Any]]:
    rows = []
    for ethic, values in THREAT_NORMAL_ETHIC_VECTORS.items():
        fanatic = ethic.replace("ethic_", "ethic_fanatic_", 1)
        rows.append({"ethic": fanatic, **axis_vector(tuple(value * THREAT_FANATIC_MULTIPLIER for value in values))})
    return rows


def threat_gestalt_rows() -> list[dict[str, Any]]:
    return [{"path": path, **axis_vector(values)} for path, values in THREAT_GESTALT_VECTORS.items()]


def clamp_score(name: str, value: int) -> int:
    lower, upper = THREAT_SCORE_LIMITS[name]
    return max(lower, min(upper, value))


def threat_scores(vector: dict[str, int], severity: int) -> dict[str, int]:
    anti = (
        severity * 10
        + vector["moral_outrage"] * 5
        + vector["regional_fear"] * 5
        + vector["shared_threat_cooperation"] * 4
        + vector["punitive_pressure"] * 6
        - vector["conquest_respect"] * 5
        - vector["opportunism"] * 3
    )
    alignment = (
        vector["conquest_respect"] * 6
        + vector["opportunism"] * 5
        - vector["moral_outrage"] * 7
        - vector["regional_fear"] * 3
    )
    readiness = severity * 5 + vector["regional_fear"] * 5 + vector["defensive_readiness"] * 5
    return {
        "anti_aggressor_score": clamp_score("anti_aggressor_score", anti),
        "alignment_with_aggressor_score": clamp_score("alignment_with_aggressor_score", alignment),
        "defensive_readiness_score": clamp_score("defensive_readiness_score", readiness),
    }


def classify_threat_war_goal(war_goal: str) -> dict[str, Any]:
    if war_goal in WAR_GOAL_THREAT_CLASSES:
        return dict(WAR_GOAL_THREAT_CLASSES[war_goal])
    return {
        "war_goal": war_goal,
        "classification": "unknown",
        "severity": 0,
        "source": "not allowlisted",
        "source_path": "",
        "mod_or_vanilla": "unknown",
        "punitive_outputs_allowed": "no",
        "readiness_outputs_allowed": "no",
        "forced_war_allowed": "no",
        "status": "unknown_inert",
        "notes": "Unknown or unclassified war goals are inert until manually classified and tested.",
    }


def threat_response_classification_rows() -> list[dict[str, Any]]:
    return [dict(row) for row in WAR_GOAL_THREAT_CLASSES.values()]


def threat_feasibility_note_path(research_root: Path = RESEARCH_ROOT) -> Path:
    return research_root / THREAT_FEASIBILITY_NOTE_NAME


def threat_classification_csv_path(research_root: Path = RESEARCH_ROOT) -> Path:
    return research_root / THREAT_CLASSIFICATION_CSV_NAME


def third_party_threat_economy_pressure(
    *,
    foreign_affairs_safe: bool,
    readiness_flag: bool,
    at_war: bool = False,
    survival: bool = False,
    recovery: bool = False,
    deficit: bool = False,
) -> dict[str, int]:
    if not foreign_affairs_safe or not readiness_flag or at_war or survival or recovery or deficit:
        return {key: 0 for key in THREAT_ECONOMY_MAX}
    return dict(THREAT_ECONOMY_MAX)


def _threat_header() -> str:
    return "# Generated by tools/generate_stellar_ai_director_patch.py.\n# Source of truth: tools/stellar_ai_director_lib.py threat-response tables.\n\n"


def threat_response_script_values_text() -> str:
    lines = [
        _threat_header().rstrip(),
        "staid_tr_anti_aggressor_score_min = 0",
        "staid_tr_anti_aggressor_score_max = 100",
        "staid_tr_alignment_score_min = 0",
        "staid_tr_alignment_score_max = 60",
        "staid_tr_defensive_readiness_score_min = 0",
        "staid_tr_defensive_readiness_score_max = 50",
        f"staid_tr_relation_flag_days = {THREAT_RELATION_FLAG_DAYS}",
        f"staid_tr_country_flag_days = {THREAT_COUNTRY_FLAG_DAYS}",
        f"staid_tr_economy_ratio_cap_percent = {int(THREAT_ECONOMY_RATIO_CAP * 100)}",
        f"staid_tr_economy_alloys_cap = {THREAT_ECONOMY_MAX['alloys']}",
        f"staid_tr_economy_energy_cap = {THREAT_ECONOMY_MAX['energy']}",
        f"staid_tr_economy_naval_cap = {THREAT_ECONOMY_MAX['naval_cap']}",
    ]
    for key, value in THREAT_TIER_CUTOFFS.items():
        lines.append(f"staid_tr_{key}_cutoff = {value}")
    return "\n".join(lines) + "\n"


def threat_response_triggers_text() -> str:
    war_goal_checks = "\n".join(
        f"staid_tr_is_{row['classification']}_war_goal = {{\n\tfrom = {{ using_war_goal = {row['war_goal']} }}\n}}\n"
        for row in WAR_GOAL_THREAT_CLASSES.values()
    )
    return (
        _threat_header()
        + war_goal_checks
        + """staid_tr_war_goal_classified = {
\tOR = {
\t\tstaid_tr_is_conquest_war_goal = yes
\t\tstaid_tr_is_subjugation_war_goal = yes
\t\tstaid_tr_is_humiliation_war_goal = yes
\t}
}

staid_tr_attacker_war_leader = {
\tfrom = {
\t\tany_attacker = {
\t\t\tis_same_value = root
\t\t\tis_war_leader = yes
\t\t}
\t}
}

staid_tr_observer_eligible = {
\tis_country_type = default
\tNOT = { is_same_value = from }
\tfrom = { NOT = { is_war_participant = root } }
\tfromfrom = { NOT = { is_war_participant = root } }
}

staid_tr_awareness_known = {
\thas_communications = from
}

staid_tr_foreign_affairs_safe = {
\tNOT = { staid_core_deficit_short_runway = yes }
\tNOT = { staid_survival_mode = yes }
\tNOT = { staid_recovery_mode = yes }
\tis_at_war = no
\thas_monthly_income = { resource = alloys value > 120 }
\thas_monthly_income = { resource = energy value > 100 }
\tresource_stockpile_compare = { resource = alloys value > 8000 }
\tresource_stockpile_compare = { resource = energy value > 5000 }
}

staid_tr_anti_aggressor_low = { check_variable_arithmetic = { which = staid_tr_score value >= 25 } }
staid_tr_anti_aggressor_medium = { check_variable_arithmetic = { which = staid_tr_score value >= 45 } }
staid_tr_anti_aggressor_high = { check_variable_arithmetic = { which = staid_tr_score value >= 65 } }
staid_tr_anti_aggressor_severe = { check_variable_arithmetic = { which = staid_tr_score value >= 85 } }
staid_tr_alignment_low = { check_variable_arithmetic = { which = staid_tr_alignment value >= 20 } }
staid_tr_alignment_medium = { check_variable_arithmetic = { which = staid_tr_alignment value >= 35 } }
staid_tr_alignment_high = { check_variable_arithmetic = { which = staid_tr_alignment value >= 50 } }
staid_tr_defensive_readiness_low = { check_variable_arithmetic = { which = staid_tr_readiness value >= 25 } }
staid_tr_defensive_readiness_high = { check_variable_arithmetic = { which = staid_tr_readiness value >= 40 } }

staid_tr_can_apply_readiness = {
\tstaid_tr_foreign_affairs_safe = yes
\tOR = {
\t\tstaid_tr_defensive_readiness_low = yes
\t\tstaid_tr_defensive_readiness_high = yes
\t}
}
"""
    )


def threat_response_opinions_text() -> str:
    lines = [_threat_header().rstrip()]
    for key, value in THREAT_OPINION_VALUES.items():
        lines.extend(
            [
                f"staid_tr_{key} = {{",
                f"\topinion = {value}",
                "\tdecay = 1",
                "\taccumulative = no",
                "}",
                "",
            ]
        )
    return "\n".join(lines)


def threat_response_on_actions_text() -> str:
    return _threat_header() + """on_war_beginning = {
\tevents = {
\t\tstaid_tr.1
\t}
}
"""


def threat_response_events_text() -> str:
    return _threat_header() + f"""namespace = staid_tr

country_event = {{
\tid = staid_tr.1
\thide_window = yes
\tis_triggered_only = yes
\ttrigger = {{
\t\tstaid_tr_attacker_war_leader = yes
\t\tstaid_tr_war_goal_classified = yes
\t}}
\timmediate = {{
\t\tfrom = {{
\t\t\trandom_defender = {{
\t\t\t\tsave_event_target_as = staid_tr_victim
\t\t\t}}
\t\t}}
\t\tevery_country = {{
\t\t\tlimit = {{
\t\t\t\tis_country_type = default
\t\t\t\tNOT = {{ is_same_value = root }}
\t\t\t\thas_communications = root
\t\t\t}}
\t\t\tcountry_event = {{ id = staid_tr.2 }}
\t\t}}
\t}}
}}

country_event = {{
\tid = staid_tr.2
\thide_window = yes
\tis_triggered_only = yes
\ttrigger = {{
\t\tstaid_tr_observer_eligible = yes
\t\tstaid_tr_awareness_known = yes
\t}}
\timmediate = {{
\t\tremove_opinion_modifier = {{ who = from modifier = staid_tr_anti_aggressor_low }}
\t\tremove_opinion_modifier = {{ who = from modifier = staid_tr_anti_aggressor_medium }}
\t\tremove_opinion_modifier = {{ who = from modifier = staid_tr_anti_aggressor_high }}
\t\tremove_opinion_modifier = {{ who = from modifier = staid_tr_anti_aggressor_severe }}
\t\tremove_opinion_modifier = {{ who = from modifier = staid_tr_alignment_low }}
\t\tremove_opinion_modifier = {{ who = from modifier = staid_tr_alignment_medium }}
\t\tremove_opinion_modifier = {{ who = from modifier = staid_tr_alignment_high }}
\t\tif = {{
\t\t\tlimit = {{ staid_tr_is_subjugation_war_goal = yes }}
\t\t\tadd_opinion_modifier = {{ who = from modifier = staid_tr_anti_aggressor_high }}
\t\t\tset_timed_relation_flag = {{ who = from flag = staid_tr_anti_aggressor_high days = {THREAT_RELATION_FLAG_DAYS} }}
\t\t}}
\t\telse_if = {{
\t\t\tlimit = {{ staid_tr_is_conquest_war_goal = yes }}
\t\t\tadd_opinion_modifier = {{ who = from modifier = staid_tr_anti_aggressor_medium }}
\t\t\tset_timed_relation_flag = {{ who = from flag = staid_tr_anti_aggressor_medium days = {THREAT_RELATION_FLAG_DAYS} }}
\t\t}}
\t\telse_if = {{
\t\t\tlimit = {{ staid_tr_is_humiliation_war_goal = yes }}
\t\t\tadd_opinion_modifier = {{ who = from modifier = staid_tr_anti_aggressor_low }}
\t\t\tset_timed_relation_flag = {{ who = from flag = staid_tr_anti_aggressor_low days = {THREAT_RELATION_FLAG_DAYS} }}
\t\t}}
\t\tif = {{
\t\t\tlimit = {{ exists = event_target:staid_tr_victim }}
\t\t\tadd_opinion_modifier = {{ who = event_target:staid_tr_victim modifier = staid_tr_shared_threat_low }}
\t\t\tset_timed_relation_flag = {{ who = event_target:staid_tr_victim flag = staid_tr_shared_threat_low days = {THREAT_RELATION_FLAG_DAYS} }}
\t\t}}
\t\tif = {{
\t\t\tlimit = {{ staid_tr_foreign_affairs_safe = yes }}
\t\t\tset_timed_country_flag = {{ flag = staid_tr_defensive_readiness_low days = {THREAT_COUNTRY_FLAG_DAYS} }}
\t\t}}
\t}}
}}
"""


def threat_response_localisation_text() -> str:
    lines = ["\ufeffl_english:"]
    labels = {
        "anti_aggressor_low": "Concerned by Aggression",
        "anti_aggressor_medium": "Condemns Aggression",
        "anti_aggressor_high": "Alarmed by Aggression",
        "anti_aggressor_severe": "Sees Existential Aggression",
        "shared_threat_low": "Shared Threat",
        "shared_threat_medium": "Shared Strategic Threat",
        "shared_threat_high": "Shared Existential Threat",
        "alignment_low": "Respects Conquest",
        "alignment_medium": "Strategic Alignment",
        "alignment_high": "Strong Strategic Alignment",
    }
    for key, label in labels.items():
        lines.append(f' staid_tr_{key}:0 "{label}"')
        lines.append(f' staid_tr_{key}_desc:0 "This empire is reacting to an observed classified war."')
    return "\n".join(lines) + "\n"


def threat_response_feasibility_note_text() -> str:
    return """# Stellar AI Director Threat Response Feasibility

Target game version: Stellaris PC 4.4.4 stable.
Local install inspected: `C:/Steam/steamapps/common/Stellaris`.

## Verified Primitives

- `on_war_beginning` from vanilla on-actions.
- `any_attacker`, `any_defender`, `random_defender`, `is_war_leader`, and `using_war_goal` for war context.
- `has_communications` for observer awareness.
- `set_timed_country_flag`, `set_timed_relation_flag`, `add_opinion_modifier`, `remove_opinion_modifier`, `decay`, and `accumulative`.
- Existing Director gates: `staid_core_deficit_short_runway`, `staid_survival_mode`, `staid_recovery_mode`, `staid_fleet_buildup_economy_safe`, and `staid_starbase_defense_economy_safe`.

## Intentional Non-Use

- No forced wars, join-war behavior, punitive casus belli, diplomatic-action overrides, or forced `wg_*` dispatch.
- No raw generator axes are consumed as Stellaris runtime concepts.
- No uncertain visibility model beyond verified communications.

## Compatibility Position

V1 reacts only from eligible third-party default countries with communications. Direct victims, participants, uncertain country types, and unknown war goals remain outside the third-party economy path. Modded war goals are inert until explicitly classified with evidence and tests.

## Test Steps

Run unit tests, regenerate the patch, validate generated output, run `git diff --check`, refresh the docs index, and verify the generated CSV evidence. Runtime/main-menu/observer launch validation is intentionally out of scope for this deterministic implementation goal unless a separate user-approved runtime task is opened.

## Recommendation

Proceed with the bounded V1 implementation as opinion, relation/country flag, and capped economy pressure only.
"""


def generate_threat_response_artifacts() -> None:
    write_text_file(
        MOD_ROOT / "common" / "script_values" / "zzz_staid_threat_response_values.txt",
        threat_response_script_values_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_threat_response_triggers.txt",
        threat_response_triggers_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "opinion_modifiers" / "zzz_staid_threat_response_opinions.txt",
        threat_response_opinions_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "on_actions" / "zzz_staid_threat_response_on_actions.txt",
        threat_response_on_actions_text(),
    )
    write_text_file(MOD_ROOT / "events" / "zzz_staid_threat_response_events.txt", threat_response_events_text())
    write_text_file(
        MOD_ROOT / "localisation" / "english" / "staid_threat_response_l_english.yml",
        threat_response_localisation_text(),
    )
    write_text_file(threat_feasibility_note_path(RESEARCH_ROOT), threat_response_feasibility_note_text())
    write_csv(threat_classification_csv_path(RESEARCH_ROOT), threat_response_classification_rows())


def threat_response_generated_paths(mod_root: Path = MOD_ROOT) -> dict[str, Path]:
    return {
        "values": mod_root / "common" / "script_values" / "zzz_staid_threat_response_values.txt",
        "triggers": mod_root / "common" / "scripted_triggers" / "zzz_staid_threat_response_triggers.txt",
        "opinions": mod_root / "common" / "opinion_modifiers" / "zzz_staid_threat_response_opinions.txt",
        "on_actions": mod_root / "common" / "on_actions" / "zzz_staid_threat_response_on_actions.txt",
        "events": mod_root / "events" / "zzz_staid_threat_response_events.txt",
        "localisation": mod_root / "localisation" / "english" / "staid_threat_response_l_english.yml",
    }


def validate_threat_response_contract(mod_root: Path = MOD_ROOT) -> list[str]:
    errors: list[str] = []
    paths = threat_response_generated_paths(mod_root)
    for label, path in paths.items():
        if not path.exists():
            errors.append(f"Threat-response {label} file is missing: {path}")
            continue
        if label == "localisation":
            raw = path.read_bytes()
            text = read_text(path)
            if not raw.startswith(b"\xef\xbb\xbf"):
                errors.append(f"Threat-response localisation must be UTF-8 BOM encoded: {path}")
            for key in THREAT_OPINION_VALUES:
                if f"staid_tr_{key}:" not in text:
                    errors.append(f"Threat-response localisation is missing staid_tr_{key}")
            continue
        try:
            parse_file(path)
        except PDXParseError as exc:
            errors.append(f"Threat-response {label} parse failed: {exc}")

    existing_texts = {label: read_text(path) for label, path in paths.items() if path.exists()}
    runtime_text = "\n".join(
        text for label, text in existing_texts.items() if label in {"values", "triggers", "opinions", "on_actions", "events"}
    )
    for forbidden in THREAT_FORBIDDEN_EFFECTS:
        if forbidden in runtime_text:
            errors.append(f"Threat-response generated files contain forbidden V1 effect: {forbidden}")
    if "common/diplomatic_actions" in runtime_text:
        errors.append("Threat-response generated files must not add diplomatic-action overrides")
    for axis in THREAT_RESPONSE_AXES:
        if re.search(rf"\b{re.escape(axis)}\b", runtime_text):
            errors.append(f"Generator-owned axis leaked into runtime generated file: {axis}")

    triggers = existing_texts.get("triggers", "")
    required_gate_terms = (
        "NOT = { staid_core_deficit_short_runway = yes }",
        "NOT = { staid_survival_mode = yes }",
        "NOT = { staid_recovery_mode = yes }",
        "is_at_war = no",
        "has_monthly_income = { resource = alloys value > 120 }",
        "has_monthly_income = { resource = energy value > 100 }",
        "resource_stockpile_compare = { resource = alloys value > 8000 }",
        "resource_stockpile_compare = { resource = energy value > 5000 }",
    )
    for term in required_gate_terms:
        if term not in triggers:
            errors.append(f"Threat-response foreign-affairs safety is missing required gate: {term}")

    events = existing_texts.get("events", "")
    required_event_terms = (
        "namespace = staid_tr",
        "id = staid_tr.1",
        "staid_tr_attacker_war_leader = yes",
        "staid_tr_war_goal_classified = yes",
        "every_country",
        "staid_tr_observer_eligible = yes",
        "staid_tr_awareness_known = yes",
        "remove_opinion_modifier",
        "add_opinion_modifier",
        "staid_tr_foreign_affairs_safe = yes",
    )
    for term in required_event_terms:
        if term not in events:
            errors.append(f"Threat-response event flow is missing required fragment: {term}")

    economy_path = mod_root / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
    if economy_path.exists():
        economy = read_text(economy_path)
        for term in (
            "Stellar AI Director threat readiness reserve",
            "has_country_flag = staid_tr_defensive_readiness_low",
            "staid_tr_foreign_affairs_safe = yes",
            "alloys = 7",
            "energy = 6",
            "naval_cap = 40",
        ):
            if term not in economy:
                errors.append(f"Threat-response economy integration is missing required fragment: {term}")

    classification_csv = threat_classification_csv_path(RESEARCH_ROOT)
    if not classification_csv.exists():
        errors.append(f"Threat-response classification CSV is missing: {classification_csv}")
    else:
        rows = _read_csv_rows(classification_csv)
        by_goal = {row.get("war_goal"): row for row in rows}
        for goal, expected in WAR_GOAL_THREAT_CLASSES.items():
            row = by_goal.get(goal)
            if row is None:
                errors.append(f"Threat-response classification CSV is missing allowlisted goal: {goal}")
                continue
            if str(row.get("severity")) != str(expected["severity"]):
                errors.append(f"Threat-response classification CSV has wrong severity for {goal}: {row.get('severity')}")
            if row.get("forced_war_allowed") != "no":
                errors.append(f"Threat-response classification CSV must forbid forced war for {goal}")
    return errors


def load_stellaris_save_gamestate(save_path: Path) -> str:
    with zipfile.ZipFile(save_path) as archive:
        if "gamestate" not in archive.namelist():
            raise ValueError(f"Stellaris save is missing gamestate entry: {save_path}")
        return archive.read("gamestate").decode("utf-8", "replace")


def latest_stellaris_save(save_root: Path = STELLARIS_SAVE_ROOT) -> Path:
    saves = [path for path in save_root.rglob("*.sav") if path.is_file()]
    if not saves:
        raise FileNotFoundError(f"No Stellaris .sav files found under {save_root}")
    return max(saves, key=lambda path: path.stat().st_mtime)


def _find_assignment_value_start(text: str, key: str, start: int = 0) -> int:
    match = re.search(rf"(^|\n)\s*{re.escape(key)}\s*=\s*", text[start:])
    if not match:
        return -1
    return start + match.end()


def _extract_balanced_block_at(text: str, brace_index: int) -> str:
    if brace_index < 0 or brace_index >= len(text) or text[brace_index] != "{":
        raise ValueError("balanced block extraction requires a starting brace")
    depth = 0
    in_quote = False
    escaped = False
    for index in range(brace_index, len(text)):
        char = text[index]
        if char == "\\" and in_quote and not escaped:
            escaped = True
            continue
        if char == '"' and not escaped:
            in_quote = not in_quote
        elif not in_quote and char == "{":
            depth += 1
        elif not in_quote and char == "}":
            depth -= 1
            if depth == 0:
                return text[brace_index : index + 1]
        escaped = False
    raise ValueError("Malformed Stellaris save block: missing closing brace")


def extract_assignment_block(text: str, key: str, start: int = 0) -> str:
    match = re.search(rf"(^|\n)\s*{re.escape(key)}\s*=\s*\{{", text[start:])
    if not match:
        return ""
    brace_index = start + match.end() - 1
    return _extract_balanced_block_at(text, brace_index)


def iter_numbered_child_blocks(block_text: str) -> list[tuple[str, str]]:
    if not block_text:
        return []
    first_brace = block_text.find("{")
    if first_brace == -1:
        return []
    inner = _extract_balanced_block_at(block_text, first_brace)[1:-1]
    rows: list[tuple[str, str]] = []
    index = 0
    while index < len(inner):
        while index < len(inner) and inner[index].isspace():
            index += 1
        key_start = index
        while index < len(inner) and inner[index].isdigit():
            index += 1
        if key_start == index:
            index += 1
            continue
        child_id = inner[key_start:index]
        while index < len(inner) and inner[index].isspace():
            index += 1
        if index >= len(inner) or inner[index] != "=":
            index += 1
            continue
        index += 1
        while index < len(inner) and inner[index].isspace():
            index += 1
        if index >= len(inner) or inner[index] != "{":
            continue
        child_block = _extract_balanced_block_at(inner, index)
        rows.append((child_id, child_block))
        index += len(child_block)
    return rows


def save_scalar(text: str, key: str) -> str:
    value_start = _find_assignment_value_start(text, key)
    if value_start == -1:
        return ""
    newline = text.find("\n", value_start)
    end = newline if newline != -1 else len(text)
    return text[value_start:end].strip().strip('"')


def numeric_assignment(text: str, key: str) -> float | None:
    match = re.search(rf"(^|\n)\s*{re.escape(key)}\s*=\s*(-?\d+(?:\.\d+)?)\b", text)
    return float(match.group(2)) if match else None


def sum_resource_assignments(block_text: str) -> dict[str, float]:
    totals: dict[str, float] = {}
    for match in re.finditer(r"\b([A-Za-z][A-Za-z0-9_]+)\s*=\s*(-?\d+(?:\.\d+)?)\b", block_text):
        resource = match.group(1)
        if resource in {"current_month", "income", "expenses", "budget"}:
            continue
        totals[resource] = totals.get(resource, 0.0) + float(match.group(2))
    return {resource: round(value, 3) for resource, value in sorted(totals.items())}


def collect_observer_save_summary(save_path: Path) -> dict[str, Any]:
    gamestate = load_stellaris_save_gamestate(save_path)
    mods = re.findall(r'"([^"]+)"', extract_assignment_block(gamestate, "mods"))
    player_block = extract_assignment_block(gamestate, "player")
    player_country_match = re.search(r"\bcountry\s*=\s*(\d+)", player_block)
    player_country = player_country_match.group(1) if player_country_match else ""
    country_blocks = dict(iter_numbered_child_blocks(extract_assignment_block(gamestate, "country")))
    initialized_countries = {
        country_id: block
        for country_id, block in country_blocks.items()
        if re.search(r"(^|\n)\s*initialized\s*=\s*yes\b", block)
    }
    player_block_text = country_blocks.get(player_country, "")
    budget_block = extract_assignment_block(player_block_text, "budget")
    current_month_block = extract_assignment_block(budget_block, "current_month")
    income_block = extract_assignment_block(current_month_block, "income")
    metric_keys = (
        "economy_power",
        "tech_power",
        "fleet_size",
        "used_naval_capacity",
        "empire_size",
        "num_sapient_pops",
        "navy_coverage",
    )
    metrics = {key: numeric_assignment(player_block_text, key) for key in metric_keys}
    metrics = {key: value for key, value in metrics.items() if value is not None}
    required_mods_present = {
        "Stellar AI Director": "Stellar AI Director" in mods,
        "Gigastructural Engineering & More (4.4)": "Gigastructural Engineering & More (4.4)" in mods,
        "NSC3": "NSC3" in mods,
        "Extra Ship Components NEXT": "Extra Ship Components NEXT" in mods,
    }
    short_smoke_checks = {
        "save_reaches_2202_01_01": save_scalar(gamestate, "date") >= "2202.01.01",
        "director_mod_listed": required_mods_present["Stellar AI Director"],
        "player_country_found": bool(player_country and player_block_text),
        "initialized_country_count_positive": len(initialized_countries) > 0,
        "player_metrics_found": bool(metrics),
    }
    return {
        "save_path": str(save_path),
        "save_mtime_utc": datetime.fromtimestamp(save_path.stat().st_mtime, timezone.utc).isoformat(),
        "version": save_scalar(gamestate, "version"),
        "name": save_scalar(gamestate, "name"),
        "date": save_scalar(gamestate, "date"),
        "mod_count": len(mods),
        "required_mods_present": required_mods_present,
        "player_country": player_country,
        "country_count": len(country_blocks),
        "initialized_country_count": len(initialized_countries),
        "player_metrics": metrics,
        "player_monthly_income": sum_resource_assignments(income_block),
        "short_smoke_checks": short_smoke_checks,
        "short_smoke_passes": all(short_smoke_checks.values()),
        "high_roi_path_observed": False,
        "p15_completion_note": "Short Irony-launched save evidence is retained as historical context; P15 runtime/observer validation is superseded for this deterministic implementation goal.",
    }


def observer_save_summary_report_text(summary: dict[str, Any]) -> str:
    lines = [
        "# Stellar AI Director Observer Smoke Save Summary",
        "",
        f"Save: `{summary['save_path']}`",
        f"Date: {summary['date']}",
        f"Version: {summary['version']}",
        f"Empire: {summary['name']}",
        f"Short smoke passes: {summary['short_smoke_passes']}",
        f"High-ROI path observed: {summary['high_roi_path_observed']}",
        "",
        "## Required Mods",
        "",
    ]
    for name, present in summary["required_mods_present"].items():
        lines.append(f"- {name}: {'present' if present else 'missing'}")
    lines.extend(
        [
            "",
            "## Save Metrics",
            "",
            f"- Mod count: {summary['mod_count']}",
            f"- Player country: {summary['player_country'] or 'missing'}",
            f"- Country count: {summary['country_count']}",
            f"- Initialized countries: {summary['initialized_country_count']}",
            f"- Player metrics: {json.dumps(summary['player_metrics'], sort_keys=True)}",
            f"- Player monthly income: {json.dumps(summary['player_monthly_income'], sort_keys=True)}",
            "",
            "## Checks",
            "",
        ]
    )
    for check, passed in summary["short_smoke_checks"].items():
        lines.append(f"- {check}: {'pass' if passed else 'fail'}")
    lines.extend(["", summary["p15_completion_note"], ""])
    return "\n".join(lines)


def generate_observer_save_summary_artifacts(save_path: Path | None = None) -> dict[str, Any]:
    summary = collect_observer_save_summary(save_path or latest_stellaris_save())
    write_json(OBSERVER_SMOKE_SAVE_SUMMARY_JSON, summary)
    write_text_file(OBSERVER_SMOKE_SAVE_SUMMARY_MD, observer_save_summary_report_text(summary))
    return summary


def integration_surface_report_text(rows: list[dict[str, Any]]) -> str:
    counts: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (row["phase"], row["object_type"])
        counts[key] = counts.get(key, 0) + 1
    lines = [
        "# Stellar AI Director Integration Surface Inventory",
        "",
        "Generated from required parent source snapshots. Rows are evidence for P6-P11 policy work; direct PDX overrides are emitted only from separately validated generated files.",
        "",
        "## Surface Counts",
        "",
        "| phase | object type | count |",
        "| --- | --- | ---: |",
    ]
    for (phase, object_type), count in sorted(counts.items()):
        lines.append(f"| {phase} | {object_type} | {count} |")
    lines.extend(
        [
            "",
            "## Candidate Intervention Samples",
            "",
            "| phase | object | mod | recommendation | minimum V1 intervention | source has AI weight |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows[:80]:
        lines.append(
            f"| {row['phase']} | `{row['object_name']}` | {row['mod_name']} | "
            f"{row['policy_recommendation']} | {row['minimum_v1_intervention']} | {row['source_has_ai_weight']} |"
        )
    return "\n".join(lines) + "\n"


def generate_integration_surface_artifacts() -> list[dict[str, Any]]:
    rows = collect_integration_surface_rows()
    write_csv(RESEARCH_ROOT / "stellar-ai-director-integration-surfaces-2026-07-04.csv", rows)
    generate_integration_policy_audit_artifacts(rows)
    write_text_file(
        RESEARCH_ROOT / "stellar-ai-director-integration-surfaces-2026-07-04.md",
        integration_surface_report_text(rows),
    )
    return rows


def generated_conflict_report_text(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Stellar AI Director Generated Conflict Classification",
        "",
        "Generated by parsing this mod's generated `common/` files and comparing top-level objects against parent and vanilla source inventories.",
        "",
        "| object type | object | file | classification | reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['object_type']} | `{row['object_name']}` | `{row['generated_file']}` | "
            f"{row['classification']} | {row['reason']} |"
        )
    return "\n".join(lines) + "\n"


def collect_generated_conflict_rows(
    mod_root: Path = MOD_ROOT,
    snapshot_root: Path = SNAPSHOT_ROOT,
) -> list[dict[str, Any]]:
    object_names = collect_object_names(snapshot_root)
    rows: list[dict[str, Any]] = []
    common = mod_root / "common"
    if not common.exists():
        return rows
    for folder, object_type in GENERATED_SURFACE_FOLDERS.items():
        folder_path = common / folder
        if not folder_path.exists():
            continue
        for file_path in iter_text_files(folder_path):
            text = read_text(file_path)
            try:
                parsed = parse_pdx(text)
            except PDXParseError:
                continue
            generated_file = file_path.relative_to(mod_root).as_posix()
            for assignment in block_assignments(parsed):
                if assignment.key.startswith("@"):
                    continue
                parent_has_object = assignment.key in object_names.get(object_type, set())
                if parent_has_object and "Full-object override" in text:
                    classification = "intentional_director_override"
                    reason = "generated file declares full-object override ownership"
                elif parent_has_object:
                    classification = "unexpected_parent_object_collision"
                    reason = "generated object matches known parent or vanilla object without override ownership note"
                else:
                    classification = "additive_director_object"
                    reason = "generated object name is new in validated source inventory"
                rows.append(
                    {
                        "object_type": object_type,
                        "object_name": assignment.key,
                        "generated_file": generated_file,
                        "parent_has_object": "yes" if parent_has_object else "no",
                        "classification": classification,
                        "reason": reason,
                    }
                )
    rows.sort(key=lambda row: (row["classification"], row["object_type"], row["object_name"]))
    return rows


def generate_conflict_classification_artifacts() -> list[dict[str, Any]]:
    rows = collect_generated_conflict_rows()
    write_csv(RESEARCH_ROOT / "stellar-ai-director-generated-conflicts-2026-07-04.csv", rows)
    write_text_file(
        RESEARCH_ROOT / "stellar-ai-director-generated-conflicts-2026-07-04.md",
        generated_conflict_report_text(rows),
    )
    return rows


def generated_top_level_objects(mod_root: Path = MOD_ROOT) -> dict[str, set[str]]:
    objects: dict[str, set[str]] = {object_type: set() for object_type in GENERATED_SURFACE_FOLDERS.values()}
    common = mod_root / "common"
    if not common.exists():
        return objects
    for folder, object_type in GENERATED_SURFACE_FOLDERS.items():
        folder_path = common / folder
        if not folder_path.exists():
            continue
        for file_path in iter_text_files(folder_path):
            try:
                parsed = parse_file(file_path)
            except PDXParseError:
                continue
            objects[object_type].update(assignment.key for assignment in block_assignments(parsed) if not assignment.key.startswith("@"))
    return objects


def collect_generated_reference_rows(
    mod_root: Path = MOD_ROOT,
    snapshot_root: Path = SNAPSHOT_ROOT,
) -> list[dict[str, Any]]:
    object_names = collect_object_names(snapshot_root)
    generated_objects = generated_top_level_objects(mod_root)
    allowed = {
        "technology": object_names.get("technology", set()),
        "resource": object_names.get("resource", set()) | set(RESOURCE_VALUES) | {"food", "energy", "minerals", "alloys", "consumer_goods"},
        "scripted_trigger": object_names.get("scripted_trigger", set()) | generated_objects["scripted_trigger"],
        "scripted_value": object_names.get("scripted_value", set()) | generated_objects["scripted_value"],
    }
    rows: list[dict[str, Any]] = []

    def add_row(file_path: Path, reference_type: str, reference_name: str, source_key: str) -> None:
        exists = reference_name in allowed[reference_type]
        rows.append(
            {
                "reference_type": reference_type,
                "reference_name": reference_name,
                "source_key": source_key,
                "generated_file": file_path.relative_to(mod_root).as_posix(),
                "status": "ok" if exists else "missing",
                "reason": "reference exists in source or generated inventory" if exists else "reference missing from source and generated inventories",
            }
        )

    common = mod_root / "common"
    if not common.exists():
        return rows
    for file_path in iter_text_files(common):
        try:
            parsed = parse_file(file_path)
        except PDXParseError:
            continue
        for assignment in iter_assignments(parsed):
            value = atom_value(assignment.value)
            if assignment.key == "has_technology" and value:
                add_row(file_path, "technology", value, assignment.key)
            elif assignment.key in {"resource", "has_deficit"} and value:
                add_row(file_path, "resource", value, assignment.key)
            elif value in {"yes", "no"} and assignment.key.startswith(("staid_", "stellarai_")):
                add_row(file_path, "scripted_trigger", assignment.key, assignment.key)
            elif value and value.startswith("staid_") and assignment.key in {"value", "add", "factor"}:
                add_row(file_path, "scripted_value", value, assignment.key)
    rows.sort(key=lambda row: (row["status"], row["reference_type"], row["reference_name"], row["generated_file"]))
    return rows


def generated_reference_report_text(rows: list[dict[str, Any]]) -> str:
    counts: dict[tuple[str, str], int] = {}
    for row in rows:
        key = (row["reference_type"], row["status"])
        counts[key] = counts.get(key, 0) + 1
    lines = [
        "# Stellar AI Director Generated Reference Audit",
        "",
        "Generated by parsing this mod's generated `common/` files and checking explicit technology, resource, scripted-trigger, and scripted-value references against source inventories.",
        "",
        "## Counts",
        "",
        "| reference type | status | count |",
        "| --- | --- | ---: |",
    ]
    for (reference_type, status), count in sorted(counts.items()):
        lines.append(f"| {reference_type} | {status} | {count} |")
    lines.extend(
        [
            "",
            "## References",
            "",
            "| type | reference | file | source key | status | reason |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['reference_type']} | `{row['reference_name']}` | `{row['generated_file']}` | "
            f"`{row['source_key']}` | {row['status']} | {row['reason']} |"
        )
    return "\n".join(lines) + "\n"


def generate_reference_audit_artifacts() -> list[dict[str, Any]]:
    rows = collect_generated_reference_rows()
    write_csv(REFERENCE_AUDIT_CSV, rows)
    write_text_file(REFERENCE_AUDIT_MD, generated_reference_report_text(rows))
    return rows


def descriptor_dependencies(text: str) -> list[str]:
    match = re.search(r"(?ms)^\s*dependencies\s*=\s*\{(?P<body>.*?)^\s*\}", text)
    if not match:
        return []
    return re.findall(r'"([^"]+)"', match.group("body"))


def playset_mod_by_id(playset: dict[str, Any], steam_id: str) -> dict[str, Any] | None:
    for mod in playset.get("mods", []):
        if safe_mod_id(mod.get("steam_id")) == steam_id:
            return mod
    return None


def playset_mod_by_name(playset: dict[str, Any], name: str) -> dict[str, Any] | None:
    for mod in playset.get("mods", []):
        if mod.get("name") == name:
            return mod
    return None


def dependency_status(descriptor_present: bool, playset_present: bool, name_matches: bool) -> str:
    if not descriptor_present:
        return "missing_descriptor_dependency"
    if not playset_present:
        return "missing_playset_dependency"
    if not name_matches:
        return "name_mismatch"
    return "ok"


def collect_dependency_audit_rows(
    mod_root: Path = MOD_ROOT,
    playset: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    playset = build_active_playset_snapshot() if playset is None else playset
    descriptor_path = mod_root / "descriptor.mod"
    descriptor_deps = set(descriptor_dependencies(read_text(descriptor_path)) if descriptor_path.exists() else [])
    rows: list[dict[str, Any]] = []
    for steam_id, expected_name in REQUIRED_MODS.items():
        actual = playset_mod_by_id(playset, steam_id)
        actual_name = actual.get("name", "") if actual else ""
        descriptor_present = expected_name in descriptor_deps
        playset_present = actual is not None
        name_matches = actual_name == expected_name
        rows.append(
            {
                "dependency_type": "required_parent",
                "steam_id": steam_id,
                "expected_name": expected_name,
                "descriptor_present": "yes" if descriptor_present else "no",
                "playset_present": "yes" if playset_present else "no",
                "actual_playset_name": actual_name,
                "load_position": actual.get("position", "") if actual else "",
                "status": dependency_status(descriptor_present, playset_present, name_matches),
            }
        )
    universal = playset_mod_by_name(playset, UNIVERSAL_RESOURCE_PATCH_NAME)
    descriptor_present = UNIVERSAL_RESOURCE_PATCH_NAME in descriptor_deps
    playset_present = universal is not None
    rows.append(
        {
            "dependency_type": "compatibility_dependency",
            "steam_id": safe_mod_id(universal.get("steam_id")) if universal else "",
            "expected_name": UNIVERSAL_RESOURCE_PATCH_NAME,
            "descriptor_present": "yes" if descriptor_present else "no",
            "playset_present": "yes" if playset_present else "no",
            "actual_playset_name": universal.get("name", "") if universal else "",
            "load_position": universal.get("position", "") if universal else "",
            "status": dependency_status(descriptor_present, playset_present, playset_present),
        }
    )
    rows.sort(key=lambda row: (row["dependency_type"], row["expected_name"]))
    return rows


def dependency_audit_report_text(rows: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    lines = [
        "# Stellar AI Director Dependency Audit",
        "",
        "Generated by comparing `mods/StellarAIDirector/descriptor.mod` dependency names against the selected Irony playset snapshot.",
        "",
        "## Counts",
        "",
        "| status | count |",
        "| --- | ---: |",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"| {status} | {count} |")
    lines.extend(
        [
            "",
            "## Dependencies",
            "",
            "| type | expected name | descriptor | playset | actual playset name | load position | status |",
            "| --- | --- | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['dependency_type']} | {row['expected_name']} | {row['descriptor_present']} | "
            f"{row['playset_present']} | {row['actual_playset_name']} | {row['load_position']} | {row['status']} |"
        )
    return "\n".join(lines) + "\n"


def generate_dependency_audit_artifacts() -> list[dict[str, Any]]:
    rows = collect_dependency_audit_rows()
    write_csv(DEPENDENCY_AUDIT_CSV, rows)
    write_text_file(DEPENDENCY_AUDIT_MD, dependency_audit_report_text(rows))
    return rows


def unresolved_template_placeholder_count(text: str) -> int:
    patterns = [
        r"\$[A-Za-z0-9_.:-]+\$",
        r"__PLACEHOLDER_[A-Za-z0-9_]+__",
        r"\bTODO\b",
        r"\bPLACEHOLDER\b",
    ]
    return sum(len(re.findall(pattern, text)) for pattern in patterns)


def generated_file_path_status(path: Path, mod_root: Path = MOD_ROOT) -> tuple[str, str]:
    try:
        relative = path.relative_to(mod_root)
    except ValueError:
        return ("outside_mod_root", "")
    parts = relative.parts
    if len(parts) >= 2 and parts[0] == "events":
        return ("ok", "events") if path.suffix.lower() == ".txt" else ("unsupported_suffix", "events")
    if len(parts) >= 3 and parts[0] == "localisation" and parts[1] == "english":
        return ("ok", "localisation") if path.suffix.lower() in {".yml", ".yaml"} else ("unsupported_suffix", "localisation")
    if len(parts) < 3 or parts[0] != "common":
        return ("outside_common", "")
    folder = parts[1]
    if folder not in GENERATED_SURFACE_FOLDERS and folder not in GENERATED_AUXILIARY_COMMON_FOLDERS:
        return ("unsupported_common_folder", folder)
    if path.suffix.lower() != ".txt":
        return ("unsupported_suffix", folder)
    return ("ok", folder)


def collect_generated_file_audit_rows(mod_root: Path = MOD_ROOT) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    roots = [
        mod_root / "common",
        mod_root / "events",
        mod_root / "localisation" / "english",
    ]
    existing_roots = [root for root in roots if root.exists()]
    if not existing_roots:
        return rows
    for file_path in sorted(path for root in existing_roots for path in root.rglob("*") if path.is_file()):
        path_status, folder = generated_file_path_status(file_path, mod_root)
        object_type = GENERATED_SURFACE_FOLDERS.get(folder, folder if folder in {"events", "localisation"} else "")
        text = read_text(file_path)
        placeholder_count = unresolved_template_placeholder_count(text)
        parse_status = "not_checked"
        top_level_object_count = 0
        if folder == "localisation":
            parse_status = "ok"
            top_level_object_count = len(re.findall(r"^\s+[A-Za-z0-9_.:-]+:", text, flags=re.MULTILINE))
        else:
            try:
                parsed = parse_pdx(text)
                parse_status = "ok"
                top_level_object_count = len(block_assignments(parsed))
            except PDXParseError as exc:
                parse_status = f"parse_error: {exc}"
        status = "ok"
        reason = "valid generated PDXScript surface"
        if path_status != "ok":
            status = path_status
            reason = "generated file is not in a supported Stellaris common surface"
        elif parse_status != "ok":
            status = "parse_error"
            reason = "generated PDXScript failed parser validation"
        elif top_level_object_count == 0:
            status = "empty_generated_file"
            reason = "generated PDXScript file has no top-level objects"
        elif placeholder_count:
            status = "unresolved_placeholder"
            reason = "generated file contains unresolved template placeholders"
        rows.append(
            {
                "generated_file": file_path.relative_to(mod_root).as_posix(),
                "folder": folder,
                "object_type": object_type,
                "path_status": path_status,
                "parse_status": parse_status,
                "top_level_object_count": top_level_object_count,
                "unresolved_placeholder_count": placeholder_count,
                "status": status,
                "reason": reason,
            }
        )
    rows.sort(key=lambda row: (row["status"], row["generated_file"]))
    return rows


def generated_file_audit_report_text(rows: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    lines = [
        "# Stellar AI Director Generated File Audit",
        "",
        "Generated by scanning `mods/StellarAIDirector/common/` for generated files and checking Stellaris surface path, suffix, parser status, top-level object count, and unresolved placeholders.",
        "",
        "## Counts",
        "",
        "| status | count |",
        "| --- | ---: |",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"| {status} | {count} |")
    lines.extend(
        [
            "",
            "## Files",
            "",
            "| file | folder | object type | path | parse | objects | placeholders | status | reason |",
            "| --- | --- | --- | --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['generated_file']}` | {row['folder']} | {row['object_type']} | {row['path_status']} | "
            f"{row['parse_status']} | {row['top_level_object_count']} | {row['unresolved_placeholder_count']} | "
            f"{row['status']} | {row['reason']} |"
        )
    return "\n".join(lines) + "\n"


def generate_file_audit_artifacts() -> list[dict[str, Any]]:
    rows = collect_generated_file_audit_rows()
    write_csv(FILE_AUDIT_CSV, rows)
    write_text_file(FILE_AUDIT_MD, generated_file_audit_report_text(rows))
    return rows


def classify_director_log_line(line: str, intentional_overrides: set[tuple[str, str]]) -> str:
    lowered = line.lower()
    if "already exists" in lowered and "using the one at" in lowered:
        for object_name, generated_file in intentional_overrides:
            if object_name in line and Path(generated_file).name in line:
                return "expected_intentional_override"
    if any(token in lowered for token in ("error", "missing", "exception", "failed", "fatal")):
        return "problem"
    return "unclassified"


def director_log_terms(runtime_files: list[Path]) -> set[str]:
    terms = {path.name for path in runtime_files}
    terms.update({"Stellar AI Director", "staid_", "zzz_staid", "zzzz_staid"})
    return terms


def collect_director_log_summary(
    path: Path,
    terms: set[str],
    intentional_overrides: set[tuple[str, str]],
    latest_runtime_mtime: int | None = None,
) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "name": path.name,
        "path": str(path),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else 0,
        "mtime_ns": path.stat().st_mtime_ns if path.exists() else None,
        "newer_than_generated": bool(path.exists() and latest_runtime_mtime and path.stat().st_mtime_ns >= latest_runtime_mtime),
        "director_line_count": 0,
        "director_expected_line_count": 0,
        "director_problem_line_count": 0,
        "director_unclassified_line_count": 0,
        "sample_director_lines": [],
    }
    if not path.exists():
        return entry
    director_lines = []
    expected_lines = []
    problem_lines = []
    unclassified_lines = []
    for line in read_text(path).splitlines():
        if any(term in line for term in terms):
            trimmed = line[:240]
            director_lines.append(trimmed)
            classification = classify_director_log_line(line, intentional_overrides)
            if classification == "expected_intentional_override":
                expected_lines.append(trimmed)
            elif classification == "problem":
                problem_lines.append(trimmed)
            else:
                unclassified_lines.append(trimmed)
    entry["director_line_count"] = len(director_lines)
    entry["director_expected_line_count"] = len(expected_lines)
    entry["director_problem_line_count"] = len(problem_lines)
    entry["director_unclassified_line_count"] = len(unclassified_lines)
    entry["sample_director_lines"] = [
        *[f"expected_intentional_override: {line}" for line in expected_lines[:10]],
        *[f"problem: {line}" for line in problem_lines[:10]],
        *[f"unclassified: {line}" for line in unclassified_lines[:10]],
    ][:10]
    return entry


def file_sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def current_main_menu_mode(dlc_load_path: Path = DLC_LOAD_PATH) -> str:
    if not dlc_load_path.exists():
        raise FileNotFoundError(f"dlc_load.json not found: {dlc_load_path}")
    enabled_mods = json.loads(read_text(dlc_load_path)).get("enabled_mods", [])
    return "with_director" if DIRECTOR_DLC_LOAD_ENTRY in enabled_mods else "baseline_without_director"


def collect_launch_log_file_state(log_root: Path = STELLARIS_LOG_ROOT) -> list[dict[str, Any]]:
    rows = []
    for log_name in ("error.log", "game.log"):
        path = log_root / log_name
        rows.append(
            {
                "name": log_name,
                "path": str(path),
                "exists": path.exists(),
                "size_bytes": path.stat().st_size if path.exists() else 0,
                "mtime_ns": path.stat().st_mtime_ns if path.exists() else None,
                "sha256": file_sha256(path),
            }
        )
    return rows


def collect_main_menu_proof_marker(
    *,
    log_root: Path = STELLARIS_LOG_ROOT,
    mod_root: Path = MOD_ROOT,
    launcher_mod_root: Path = PARADOX_MOD_ROOT,
    dlc_load_path: Path = DLC_LOAD_PATH,
    confirmation_env: str = MAIN_MENU_CONFIRMATION_ENV,
    environment: dict[str, str] | None = None,
) -> dict[str, Any]:
    environment = environment if environment is not None else os.environ
    confirmation = environment.get(confirmation_env, "")
    if confirmation.lower() != "yes":
        raise PermissionError(
            f"Set {confirmation_env}=yes only after visually confirming Stellaris reached the main menu."
        )
    mode = current_main_menu_mode(dlc_load_path)
    return {
        "confirmed": True,
        "mode": mode,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "confirmation_env": confirmation_env,
        "confirmation_value": confirmation,
        "launcher_installation": collect_launcher_installation_state(launcher_mod_root, mod_root, dlc_load_path),
        "logs": collect_launch_log_file_state(log_root),
    }


def merge_main_menu_proof_marker(existing: dict[str, Any], marker: dict[str, Any]) -> dict[str, Any]:
    markers = [row for row in existing.get("markers", []) if isinstance(row, dict)]
    if marker:
        markers.append(marker)
    by_mode: dict[str, dict[str, Any]] = {}
    for row in markers:
        if row.get("confirmed") is True and row.get("mode") in MAIN_MENU_REQUIRED_MODES:
            by_mode[row["mode"]] = row
    missing_modes = [mode for mode in MAIN_MENU_REQUIRED_MODES if mode not in by_mode]
    return {
        "required_modes": list(MAIN_MENU_REQUIRED_MODES),
        "main_menu_proven": not missing_modes,
        "missing_modes": missing_modes,
        "modes": by_mode,
        "markers": markers,
    }


def read_main_menu_proof_status(proof_path: Path = MAIN_MENU_PROOF_PATH) -> dict[str, Any]:
    if not proof_path.exists():
        return {
            "proof_path": str(proof_path),
            "main_menu_proven": False,
            "missing_modes": list(MAIN_MENU_REQUIRED_MODES),
            "main_menu_evidence": "manual main-menu proof markers are missing for baseline_without_director and with_director",
        }
    data = json.loads(read_text(proof_path))
    merged = merge_main_menu_proof_marker(data, {})
    modes = sorted(merged["modes"])
    if merged["main_menu_proven"]:
        evidence = f"manual main-menu proof markers recorded for {', '.join(modes)}"
    else:
        evidence = f"manual main-menu proof markers missing for {', '.join(merged['missing_modes'])}"
    return {
        "proof_path": str(proof_path),
        "main_menu_proven": merged["main_menu_proven"],
        "missing_modes": merged["missing_modes"],
        "main_menu_evidence": evidence,
    }


def record_main_menu_proof_marker(
    *,
    proof_path: Path = MAIN_MENU_PROOF_PATH,
    log_root: Path = STELLARIS_LOG_ROOT,
    mod_root: Path = MOD_ROOT,
    launcher_mod_root: Path = PARADOX_MOD_ROOT,
    dlc_load_path: Path = DLC_LOAD_PATH,
    confirmation_env: str = MAIN_MENU_CONFIRMATION_ENV,
    environment: dict[str, str] | None = None,
) -> dict[str, Any]:
    marker = collect_main_menu_proof_marker(
        log_root=log_root,
        mod_root=mod_root,
        launcher_mod_root=launcher_mod_root,
        dlc_load_path=dlc_load_path,
        confirmation_env=confirmation_env,
        environment=environment,
    )
    existing = json.loads(read_text(proof_path)) if proof_path.exists() else {}
    merged = merge_main_menu_proof_marker(existing, marker)
    write_json(proof_path, merged)
    return merged


def collect_launch_validation_evidence(
    install_root: Path = STELLARIS_INSTALL_ROOT,
    log_root: Path = STELLARIS_LOG_ROOT,
    mod_root: Path = MOD_ROOT,
    main_menu_proof_path: Path = MAIN_MENU_PROOF_PATH,
) -> dict[str, Any]:
    runtime_files = sorted((mod_root / "common").rglob("*.txt")) if (mod_root / "common").exists() else []
    latest_runtime_mtime = max((path.stat().st_mtime_ns for path in runtime_files), default=None)
    generated_terms = director_log_terms(runtime_files)
    intentional_overrides = {
        (row["object_name"], row["generated_file"])
        for row in collect_generated_conflict_rows(mod_root)
        if row["classification"] == "intentional_director_override"
    }
    logs = []
    for log_name in ("error.log", "game.log"):
        path = log_root / log_name
        logs.append(collect_director_log_summary(path, generated_terms, intentional_overrides, latest_runtime_mtime))
    fresh_logs = bool(logs and all(log["exists"] and log["newer_than_generated"] for log in logs))
    launcher_state = collect_launcher_installation_state(mod_root=mod_root)
    main_menu_status = read_main_menu_proof_status(main_menu_proof_path)
    return {
        "game_executable": str(install_root / "stellaris.exe"),
        "game_executable_exists": (install_root / "stellaris.exe").exists(),
        "launcher_installation": launcher_state,
        "runtime_file_count": len(runtime_files),
        "latest_runtime_mtime_ns": latest_runtime_mtime,
        "logs": logs,
        "launch_evidence_status": "fresh_logs_present" if fresh_logs else "stale_or_missing_logs",
        "main_menu_proven": main_menu_status["main_menu_proven"],
        "main_menu_evidence": main_menu_status["main_menu_evidence"],
        "main_menu_missing_modes": main_menu_status["missing_modes"],
        "main_menu_proof_path": main_menu_status["proof_path"],
    }


def launch_validation_report_text(evidence: dict[str, Any]) -> str:
    lines = [
        "# Stellar AI Director Launch Validation Evidence",
        "",
        f"Game executable exists: {evidence['game_executable_exists']}",
        f"Game executable: `{evidence['game_executable']}`",
        f"Launcher descriptor exists: {evidence['launcher_installation']['descriptor_exists']}",
        f"Launcher descriptor points to source: {evidence['launcher_installation']['descriptor_points_to_source']}",
        f"Enabled in dlc_load.json: {evidence['launcher_installation']['enabled_in_dlc_load']}",
        f"Generated runtime files: {evidence['runtime_file_count']}",
        f"Launch evidence status: {evidence['launch_evidence_status']}",
        f"Main menu proven: {evidence['main_menu_proven']}",
        f"Main menu evidence: {evidence['main_menu_evidence']}",
        "",
        "## Log Review",
        "",
        "| log | exists | newer than generated files | bytes | Director lines | expected override lines | Director problem lines | unclassified lines |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for log in evidence["logs"]:
        lines.append(
            f"| {log['name']} | {log['exists']} | {log['newer_than_generated']} | {log['size_bytes']} | "
            f"{log['director_line_count']} | {log['director_expected_line_count']} | "
            f"{log['director_problem_line_count']} | {log['director_unclassified_line_count']} |"
        )
    lines.extend(["", "## Director Line Samples", ""])
    for log in evidence["logs"]:
        lines.append(f"### {log['name']}")
        if not log["sample_director_lines"]:
            lines.append("")
            lines.append("No Director-specific lines found in this log.")
            lines.append("")
            continue
        lines.append("")
        for line in log["sample_director_lines"]:
            lines.append(f"- `{line}`")
        lines.append("")
    return "\n".join(lines)


def generate_launch_validation_artifacts() -> dict[str, Any]:
    evidence = collect_launch_validation_evidence()
    write_json(RESEARCH_ROOT / "stellar-ai-director-launch-validation-2026-07-04.json", evidence)
    write_text_file(
        RESEARCH_ROOT / "stellar-ai-director-launch-validation-2026-07-04.md",
        launch_validation_report_text(evidence),
    )
    return evidence


def collect_launch_comparison_evidence(
    baseline_error_log: Path = BASELINE_ERROR_LOG,
    baseline_game_log: Path = BASELINE_GAME_LOG,
    with_director_error_log: Path = WITH_DIRECTOR_ERROR_LOG,
    with_director_game_log: Path = WITH_DIRECTOR_GAME_LOG,
    mod_root: Path = MOD_ROOT,
    main_menu_proof_path: Path = MAIN_MENU_PROOF_PATH,
    launch_surface: str | None = None,
) -> dict[str, Any]:
    runtime_files = sorted((mod_root / "common").rglob("*.txt")) if (mod_root / "common").exists() else []
    terms = director_log_terms(runtime_files)
    intentional_overrides = {
        (row["object_name"], row["generated_file"])
        for row in collect_generated_conflict_rows(mod_root)
        if row["classification"] == "intentional_director_override"
    }
    baseline_logs = [
        collect_director_log_summary(baseline_error_log, terms, intentional_overrides),
        collect_director_log_summary(baseline_game_log, terms, intentional_overrides),
    ]
    director_logs = [
        collect_director_log_summary(with_director_error_log, terms, intentional_overrides),
        collect_director_log_summary(with_director_game_log, terms, intentional_overrides),
    ]
    baseline_matches = sum(log["director_line_count"] for log in baseline_logs)
    director_matches = sum(log["director_line_count"] for log in director_logs)
    director_problem_lines = sum(log["director_problem_line_count"] for log in director_logs)
    director_unclassified_lines = sum(log["director_unclassified_line_count"] for log in director_logs)
    main_menu_status = read_main_menu_proof_status(main_menu_proof_path)
    return {
        "launch_surface": launch_surface or os.environ.get(LAUNCH_SURFACE_ENV, "direct_executable_probe"),
        "baseline_logs": baseline_logs,
        "with_director_logs": director_logs,
        "baseline_director_match_count": baseline_matches,
        "with_director_match_count": director_matches,
        "with_director_problem_line_count": director_problem_lines,
        "with_director_unclassified_line_count": director_unclassified_lines,
        "with_director_expected_override_line_count": sum(log["director_expected_line_count"] for log in director_logs),
        "director_delta_status": (
            "expected_only"
            if baseline_matches == 0 and director_matches > 0 and director_problem_lines == 0 and director_unclassified_lines == 0
            else "needs_review"
        ),
        "main_menu_proven": main_menu_status["main_menu_proven"],
        "main_menu_evidence": main_menu_status["main_menu_evidence"],
        "main_menu_missing_modes": main_menu_status["missing_modes"],
        "main_menu_proof_path": main_menu_status["proof_path"],
    }


def launch_comparison_report_text(evidence: dict[str, Any]) -> str:
    launch_surface = evidence.get("launch_surface", "unknown")
    real_playset_surface = launch_surface in {"irony_launcher", "paradox_launcher"}
    if real_playset_surface and evidence["main_menu_proven"] and evidence["director_delta_status"] == "expected_only":
        conclusion = (
            "The comparison shows both required main-menu proof markers are present and the "
            "Director-specific log delta is limited to expected intentional override lines for "
            "the launcher-resolved playset."
        )
        next_step = (
            "P14 launch validation is satisfied for the preserved baseline and Director-enabled "
            "probes; continue with observer testing and longer-run tuning validation."
        )
    elif evidence["main_menu_proven"] and evidence["director_delta_status"] == "expected_only":
        conclusion = (
            "The comparison shows main-menu proof markers and an expected-only Director log "
            f"delta, but the recorded launch surface is `{launch_surface}`, not an Irony or "
            "launcher-resolved playset launch."
        )
        next_step = (
            "Next validation must launch the actual parent playset through Irony or another "
            "launcher-resolved playset surface before P14 can be marked complete."
        )
    else:
        conclusion = (
            "The comparison proves only that the Director-specific log delta is expected-only for "
            "the preserved timed probes. It does not yet prove that both the parent playset and "
            "the Director-enabled playset reached the main menu."
        )
        next_step = (
            "Next validation must use a visible/manual or otherwise main-menu-detectable launch "
            "method before P14 can be marked complete."
        )
    lines = [
        "# Stellar AI Director Launch Comparison",
        "",
        "Generated from preserved baseline and Director-enabled launch logs.",
        "",
        f"Launch surface: {launch_surface}",
        f"Director delta status: {evidence['director_delta_status']}",
        f"Main menu proven: {evidence['main_menu_proven']}",
        f"Main menu evidence: {evidence['main_menu_evidence']}",
        "",
        "## Summary",
        "",
        "| probe | Director matches | expected override lines | problem lines | unclassified lines |",
        "| --- | ---: | ---: | ---: | ---: |",
        (
            f"| baseline without Director | {evidence['baseline_director_match_count']} | "
            "0 | 0 | 0 |"
        ),
        (
            f"| with Director | {evidence['with_director_match_count']} | "
            f"{evidence['with_director_expected_override_line_count']} | "
            f"{evidence['with_director_problem_line_count']} | "
            f"{evidence['with_director_unclassified_line_count']} |"
        ),
        "",
        "## Baseline Logs",
        "",
        "| log | exists | bytes | Director lines |",
        "| --- | --- | ---: | ---: |",
    ]
    for log in evidence["baseline_logs"]:
        lines.append(f"| `{log['path']}` | {log['exists']} | {log['size_bytes']} | {log['director_line_count']} |")
    lines.extend(
        [
            "",
            "## Director-Enabled Logs",
            "",
            "| log | exists | bytes | Director lines | expected override lines | problem lines | unclassified lines |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for log in evidence["with_director_logs"]:
        lines.append(
            f"| `{log['path']}` | {log['exists']} | {log['size_bytes']} | {log['director_line_count']} | "
            f"{log['director_expected_line_count']} | {log['director_problem_line_count']} | "
            f"{log['director_unclassified_line_count']} |"
        )
    lines.extend(["", "## Director Line Samples", ""])
    for log in evidence["with_director_logs"]:
        lines.append(f"### {Path(log['path']).name}")
        lines.append("")
        if not log["sample_director_lines"]:
            lines.append("No Director-specific lines found in this log.")
            lines.append("")
            continue
        for line in log["sample_director_lines"]:
            lines.append(f"- `{line}`")
        lines.append("")
    lines.extend(["", "## Current Conclusion", "", conclusion, "", next_step])
    return "\n".join(lines) + "\n"


def generate_launch_comparison_artifacts() -> dict[str, Any]:
    evidence = collect_launch_comparison_evidence()
    write_json(RESEARCH_ROOT / "stellar-ai-director-launch-comparison-2026-07-04.json", evidence)
    write_text_file(
        RESEARCH_ROOT / "stellar-ai-director-launch-comparison-2026-07-04.md",
        launch_comparison_report_text(evidence),
    )
    return evidence


def extract_completion_checklist_items(plan_text: str) -> list[dict[str, str]]:
    items = []
    for match in re.finditer(r"(?m)^- \[ \] (P\d+) (.+?)\.$", plan_text):
        items.append({"phase": match.group(1), "requirement": match.group(2)})
    return items


def plan_phase_artifact_rows(phase: str, repo_root: Path = REPO_ROOT) -> list[dict[str, Any]]:
    rows = []
    for relative in PLAN_PHASE_EVIDENCE.get(phase, ()):
        path = repo_root / relative
        rows.append(
            {
                "path": relative,
                "exists": path.exists(),
                "size_bytes": path.stat().st_size if path.exists() else 0,
            }
        )
    return rows


def launch_comparison_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    comparison_path = repo_root / "research/stellar-ai/stellar-ai-director-launch-comparison-2026-07-04.json"
    if not comparison_path.exists():
        return False
    evidence = json.loads(read_text(comparison_path))
    return (
        evidence.get("launch_surface") in {"irony_launcher", "paradox_launcher"}
        and evidence.get("director_delta_status") == "expected_only"
        and evidence.get("main_menu_proven") is True
        and evidence.get("with_director_problem_line_count") == 0
        and evidence.get("with_director_unclassified_line_count") == 0
    )


def starbase_policy_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    economy_path = repo_root / "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt"
    triggers_path = repo_root / "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt"
    tuning_path = repo_root / "mods/StellarAIDirector/notes/tuning-notes.md"
    required_economy_terms = {
        "Stellar AI Director defensive starbase reserve",
        "Stellar AI Director crisis starbase reserve",
        "staid_static_defense_investment_ready = yes",
        "staid_crisis_starbase_pressure = yes",
    }
    required_trigger_terms = {
        "staid_defensive_starbase_strategy",
        "staid_crisis_starbase_pressure",
        "staid_aggressive_fleet_pressure",
        "staid_static_defense_investment_ready",
        "staid_recovery_mode = yes",
    }
    required_note_terms = {
        "static-defense",
        "esc starbase reactor override",
    }
    if not (economy_path.exists() and triggers_path.exists() and tuning_path.exists()):
        return False
    try:
        parse_file(economy_path)
        parse_file(triggers_path)
    except PDXParseError:
        return False
    economy = read_text(economy_path)
    triggers = read_text(triggers_path)
    tuning = read_text(tuning_path).lower()
    return (
        all(term in economy for term in required_economy_terms)
        and all(term in triggers for term in required_trigger_terms)
        and all(term in tuning for term in required_note_terms)
    )


def shipyard_policy_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    economy_path = repo_root / "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt"
    triggers_path = repo_root / "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt"
    tuning_path = repo_root / "mods/StellarAIDirector/notes/tuning-notes.md"
    required_economy_terms = {
        "Stellar AI Director fleet throughput reserve",
        "Stellar AI Director payoff exploitation alloys",
        "staid_shipyard_expansion_ready = yes",
        "staid_fleet_payoff_exploitation_ready = yes",
        "naval_cap = 800",
        "alloys = 500",
    }
    required_trigger_terms = {
        "staid_fleet_buildup_economy_safe",
        "staid_shipyard_expansion_ready",
        "staid_fleet_payoff_exploitation_ready",
        "used_naval_capacity_percent < 1.05",
        "staid_core_deficit_short_runway = yes",
    }
    required_note_terms = {
        "fleet-throughput policy",
        "over-naval-cap upkeep spirals",
    }
    if not (economy_path.exists() and triggers_path.exists() and tuning_path.exists()):
        return False
    try:
        parse_file(economy_path)
        parse_file(triggers_path)
    except PDXParseError:
        return False
    economy = read_text(economy_path)
    triggers = read_text(triggers_path)
    tuning = read_text(tuning_path).lower()
    return (
        all(term in economy for term in required_economy_terms)
        and all(term in triggers for term in required_trigger_terms)
        and all(term in tuning for term in required_note_terms)
    )


def planetary_capacity_policy_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    economy_path = repo_root / "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt"
    triggers_path = repo_root / "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt"
    tuning_path = repo_root / "mods/StellarAIDirector/notes/tuning-notes.md"
    buildings_path = repo_root / "mods/StellarAIDirector/common/buildings/zzzz_staid_06_research_infrastructure_buildings.txt"
    districts_path = repo_root / "mods/StellarAIDirector/common/districts/zzzz_staid_06_research_infrastructure_districts.txt"
    required_economy_terms = {
        "Stellar AI Director planetary capacity reserve",
        "staid_planetary_capacity_growth_ready = yes",
        "pops = 400000",
        "minerals = 500",
    }
    required_trigger_terms = {
        "staid_planetary_capacity_growth_ready",
        "staid_core_deficit_short_runway = yes",
        "resource_stockpile_compare = { resource = minerals value > 5000 }",
        "has_monthly_income = { resource = minerals value > 100 }",
    }
    required_note_terms = {
        "planetary-capacity policy",
        "direct research infrastructure overrides",
    }
    if not (
        economy_path.exists()
        and triggers_path.exists()
        and tuning_path.exists()
        and buildings_path.exists()
        and districts_path.exists()
    ):
        return False
    try:
        parse_file(economy_path)
        parse_file(triggers_path)
        parse_file(buildings_path)
        parse_file(districts_path)
    except PDXParseError:
        return False
    economy = read_text(economy_path)
    triggers = read_text(triggers_path)
    tuning = (read_text(tuning_path) + "\n" + read_text(buildings_path) + "\n" + read_text(districts_path)).lower()
    return (
        all(term in economy for term in required_economy_terms)
        and all(term in triggers for term in required_trigger_terms)
        and all(term in tuning for term in required_note_terms)
        and "building_research_lab_3" in tuning
        and "district_hab_science" in tuning
    )


def nsc3_esc_policy_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    audit_path = repo_root / "research/stellar-ai/stellar-ai-director-integration-policy-audit-2026-07-04.csv"
    tuning_path = repo_root / "mods/StellarAIDirector/notes/tuning-notes.md"
    conflicts_path = repo_root / "mods/StellarAIDirector/notes/conflicts.md"
    technology_path = repo_root / "mods/StellarAIDirector/common/technology/zzzz_staid_01_unlock_technology_technology.txt"
    if not (audit_path.exists() and tuning_path.exists() and conflicts_path.exists() and technology_path.exists()):
        return False
    with audit_path.open(encoding="utf-8", newline="") as handle:
        p11_rows = [row for row in csv.DictReader(handle) if row.get("phase") == "P11"]
    if not p11_rows or any(row.get("status") == "fail" for row in p11_rows):
        return False
    if not all(row.get("priority_band") == "nsc3_esc_parent_design_ai_preservation" for row in p11_rows):
        return False
    notes = (read_text(tuning_path) + "\n" + read_text(conflicts_path) + "\n" + read_text(technology_path)).lower()
    required_terms = {
        "nsc3/esc design policy",
        "nsc3 and esc unlock technologies now have copied source-object route ai weights",
        "tech_dreadnought_1",
        "esc_tech_dark_matter_power_core_2",
    }
    return all(term in notes for term in required_terms)


def unlock_priority_policy_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    economy_path = repo_root / "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt"
    triggers_path = repo_root / "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt"
    tuning_path = repo_root / "mods/StellarAIDirector/notes/tuning-notes.md"
    technology_path = repo_root / "mods/StellarAIDirector/common/technology/zzzz_staid_01_unlock_technology_technology.txt"
    ascension_path = repo_root / "mods/StellarAIDirector/common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt"
    traditions_path = repo_root / "mods/StellarAIDirector/common/traditions/zzzz_staid_02_perks_traditions_traditions.txt"
    reference_audit_path = repo_root / "research/stellar-ai/stellar-ai-director-generated-reference-audit-2026-07-04.csv"
    required_paths = [economy_path, triggers_path, tuning_path, reference_audit_path, technology_path, ascension_path, traditions_path]
    if not all(path.exists() for path in required_paths):
        return False
    try:
        for path in (economy_path, triggers_path, technology_path, ascension_path, traditions_path):
            parse_file(path)
    except PDXParseError:
        return False
    with reference_audit_path.open(encoding="utf-8", newline="") as handle:
        if any(row.get("status") == "missing" for row in csv.DictReader(handle)):
            return False
    economy = read_text(economy_path)
    triggers = read_text(triggers_path)
    tuning = (read_text(tuning_path) + "\n" + read_text(technology_path) + "\n" + read_text(ascension_path) + "\n" + read_text(traditions_path)).lower()
    return (
        "Stellar AI Director modded unlock research reserve" in economy
        and "staid_core_unlock_research_priority_ready = yes" in economy
        and "staid_core_unlock_research_priority_ready" in triggers
        and "has_technology = tech_mega_engineering" in triggers
        and "has_technology = tech_mega_shipyard" in triggers
        and "unlock-research policy" in tuning
        and "direct technology/ap/tradition route overrides are emitted" in tuning
        and "tech_mega_engineering" in tuning
        and "ap_celestial_printing" in tuning
        and "tr_supremacy_adopt" in tuning
    )


def mega_giga_policy_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    alloy_budget_path = repo_root / "mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt"
    gigas_budget_path = repo_root / "mods/StellarAIDirector/common/ai_budget/zzz_staid_gigas_resource_budgets.txt"
    economy_path = repo_root / "mods/StellarAIDirector/common/economic_plans/zzzz_staid_additive_economic_plan.txt"
    megastructure_path = repo_root / "mods/StellarAIDirector/common/megastructures/zzzz_staid_03_megastructures_megastructures.txt"
    tuning_path = repo_root / "mods/StellarAIDirector/notes/tuning-notes.md"
    policy_audit_path = repo_root / "research/stellar-ai/stellar-ai-director-integration-policy-audit-2026-07-04.csv"
    roi_quality_path = repo_root / "research/stellar-ai/stellar-ai-director-roi-quality-audit-2026-07-04.csv"
    required_paths = [alloy_budget_path, gigas_budget_path, economy_path, megastructure_path, tuning_path, policy_audit_path, roi_quality_path]
    if not all(path.exists() for path in required_paths):
        return False
    try:
        parse_file(alloy_budget_path)
        parse_file(gigas_budget_path)
        parse_file(economy_path)
        parse_file(megastructure_path)
    except PDXParseError:
        return False
    with policy_audit_path.open(encoding="utf-8", newline="") as handle:
        p7_rows = [row for row in csv.DictReader(handle) if row.get("phase") == "P7"]
    if not p7_rows or any(row.get("status") == "fail" for row in p7_rows):
        return False
    if not any(row.get("status") == "ready" and row.get("priority_band") == "roi_driven_mega_giga_builds" for row in p7_rows):
        return False
    with roi_quality_path.open(encoding="utf-8", newline="") as handle:
        if any(row.get("status") == "fail" for row in csv.DictReader(handle)):
            return False
    combined = "\n".join(read_text(path) for path in (alloy_budget_path, gigas_budget_path, economy_path, megastructure_path, tuning_path)).lower()
    required_terms = {
        "staid_pause_new_megastructure",
        "staid_megastructure_prep_ready",
        "staid_megastructure_commit_safe",
        "stellar ai director mega alloy reserve",
        "stellar ai director giga special resource reserve",
        "generated full-object route overrides",
        "observer-tested against the high-scale crisis benchmark",
    }
    return all(term in combined for term in required_terms)


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def munch_preflight_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    preflight_path = repo_root / "research/stellar-ai/stellar-ai-director-munch-preflight-2026-07-04.md"
    if not preflight_path.exists():
        return False
    text = read_text(preflight_path).lower()
    required_terms = {
        "jdocmunch_guide` returned content",
        "jcodemunch_guide` returned content",
        "jdatamunch_guide` returned content",
        "munch_preflight_pass",
        "active-thread guide calls succeeded",
    }
    return all(term in text for term in required_terms)


def source_corpus_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    snapshot_root = repo_root / "research/mod-source-snapshots/2026-07-04"
    manifest_path = snapshot_root / "snapshot-manifest.csv"
    descriptor_path = snapshot_root / "descriptor-inventory.csv"
    object_inventory_path = snapshot_root / "pdx-object-inventory.csv"
    ai_surface_path = snapshot_root / "ai-surface-inventory.csv"
    corpus_note_path = repo_root / "research/stellar-ai/stellar-ai-director-corpus-status-2026-07-04.md"
    if not all(path.exists() for path in (manifest_path, descriptor_path, object_inventory_path, ai_surface_path, corpus_note_path)):
        return False
    manifest_rows = _read_csv_rows(manifest_path)
    descriptor_rows = _read_csv_rows(descriptor_path)
    object_rows = _read_csv_rows(object_inventory_path)
    ai_rows = _read_csv_rows(ai_surface_path)
    required_parent_names = {
        "Stellar AI",
        "Gigastructural Engineering & More (4.4)",
        "NSC3",
        "Extra Ship Components NEXT",
        "Starbase Extended 3.0",
    }
    manifest_names = {row.get("name", "") for row in manifest_rows}
    descriptor_names = {row.get("name", "") for row in descriptor_rows}
    required_object_dirs = {
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
    }
    object_dirs = {row.get("second_dir", "") for row in object_rows}
    ai_columns = set(ai_rows[0].keys()) if ai_rows else set()
    required_ai_columns = {"ai_weight", "economic_plan", "megastructure", "technology", "ship_size", "component", "starbase"}
    note = read_text(corpus_note_path).lower()
    required_note_terms = {
        "jdocmunch repo `local/stellarismods-docs-2026-07-04`",
        "verify_index` reported 0 drift, 0 missing, and 0 errors",
        "jcodemunch repo `local/stellarismods-223b92bc`",
        "jdatamunch indexed and validated",
        "pdx-object-inventory.csv`: 35991 rows",
        "ai-surface-inventory.csv`: 1696 rows",
    }
    return (
        len(manifest_rows) == 5
        and len(descriptor_rows) == 5
        and len(object_rows) >= 35000
        and len(ai_rows) >= 1600
        and required_parent_names.issubset(manifest_names)
        and required_parent_names.issubset(descriptor_names)
        and required_object_dirs.issubset(object_dirs)
        and required_ai_columns.issubset(ai_columns)
        and all(row.get("snapshot_path") for row in manifest_rows)
        and all(term in note for term in required_note_terms)
    )


def roi_model_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    roi_path = repo_root / "research/stellar-ai/stellar-ai-director-roi-matrix-2026-07-04.csv"
    market_path = repo_root / "research/stellar-ai/stellar-ai-director-market-values-2026-07-04.csv"
    quality_path = repo_root / "research/stellar-ai/stellar-ai-director-roi-quality-audit-2026-07-04.csv"
    report_path = repo_root / "research/stellar-ai/stellar-ai-director-roi-matrix-2026-07-04.md"
    if not all(path.exists() for path in (roi_path, market_path, quality_path, report_path)):
        return False
    roi_rows = _read_csv_rows(roi_path)
    market_rows = _read_csv_rows(market_path)
    quality_rows = _read_csv_rows(quality_path)
    eligible_rows = [row for row in roi_rows if row.get("decision_eligible") == "yes"]
    required_objects = {
        "mega_shipyard_2",
        "mega_shipyard_3",
        "mega_shipyard_restored",
        "neutronium_gigaforge_3",
        "nidavellir_forge_4",
        "hrae_mc_4",
    }
    required_roles = {"economy_multiplier", "research_multiplier", "fleet_production_sink"}
    required_market_resources = {"alloys", "energy", "minerals", "consumer_goods"}
    object_names = {row.get("object_name", "") for row in roi_rows}
    roles = {row.get("director_strategy_role", "") for row in roi_rows}
    mod_names = {row.get("mod_name", "") for row in roi_rows}
    market_resources = {row.get("resource", "") for row in market_rows}
    eligible_bottlenecks = [row for row in eligible_rows if row.get("market_unpriced_resources")]
    return (
        len(eligible_rows) >= 140
        and {"Gigastructural Engineering & More (4.4)", "NSC3"}.issubset(mod_names)
        and required_objects.issubset(object_names)
        and required_roles.issubset(roles)
        and required_market_resources.issubset(market_resources)
        and bool(eligible_bottlenecks)
        and not any(row.get("status") == "fail" for row in quality_rows)
        and all(row.get("data_quality") == "resolved" for row in eligible_rows)
        and all(row.get("build_cost_value") not in {"", "0", "0.0"} for row in eligible_rows)
        and "Rows marked `decision_eligible = no` are kept for auditability" in read_text(report_path)
    )


def decision_tree_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    triggers_path = repo_root / "mods/StellarAIDirector/common/scripted_triggers/zzz_staid_decision_state_triggers.txt"
    tuning_path = repo_root / "mods/StellarAIDirector/notes/tuning-notes.md"
    if not (triggers_path.exists() and tuning_path.exists()):
        return False
    try:
        parse_file(triggers_path)
    except PDXParseError:
        return False
    triggers = read_text(triggers_path)
    tuning = read_text(tuning_path).lower()
    required_trigger_terms = {
        "staid_survival_mode",
        "staid_recovery_mode",
        "staid_core_deficit_short_runway",
        "staid_surplus_sink_pressure",
        "staid_pause_new_megastructure",
        "staid_megastructure_prep_ready",
        "staid_megastructure_commit_safe",
        "staid_research_sink_priority_ready",
        "staid_unity_sink_priority_ready",
        "staid_core_unlock_research_priority_ready",
        "staid_shipyard_expansion_ready",
        "staid_fleet_payoff_exploitation_ready",
        "staid_static_defense_investment_ready",
        "staid_planetary_capacity_growth_ready",
        "staid_resource_waste_pressure",
        "staid_research_under_curve",
        "staid_homeland_under_attack",
        "has_deficit = energy",
        "has_deficit = minerals",
        "has_deficit = consumer_goods",
        "used_naval_capacity_percent < 1.05",
    }
    required_note_terms = {
        "safe tuning rules",
        "do not lower prep or commit reserves below survival/recovery safety gates",
        "keep research sink before fleet sink",
    }
    return all(term in triggers for term in required_trigger_terms) and all(term in tuning for term in required_note_terms)


def generated_surface_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    file_audit_path = repo_root / "research/stellar-ai/stellar-ai-director-generated-file-audit-2026-07-04.csv"
    reference_audit_path = repo_root / "research/stellar-ai/stellar-ai-director-generated-reference-audit-2026-07-04.csv"
    conflict_audit_path = repo_root / "research/stellar-ai/stellar-ai-director-generated-conflicts-2026-07-04.csv"
    tuning_path = repo_root / "mods/StellarAIDirector/notes/tuning-notes.md"
    required_generated_files = {
        "common/ai_budget/zzz_staid_alloys_budget.txt",
        "common/ai_budget/zzz_staid_gigas_resource_budgets.txt",
        "common/economic_plans/zzzz_staid_additive_economic_plan.txt",
        "common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt",
        "events/zzz_staid_market_and_fleet_safety_events.txt",
        "common/on_actions/zzz_staid_load_proof_on_actions.txt",
        "common/on_actions/zzz_staid_threat_response_on_actions.txt",
        "common/opinion_modifiers/zzz_staid_threat_response_opinions.txt",
        "common/script_values/zzz_staid_roi_values.txt",
        "common/script_values/zzz_staid_threat_response_values.txt",
        "common/scripted_triggers/zzz_staid_decision_state_triggers.txt",
        "common/scripted_triggers/zzz_staid_threat_response_triggers.txt",
    }
    file_rows = _read_csv_rows(file_audit_path)
    reference_rows = _read_csv_rows(reference_audit_path)
    conflict_rows = _read_csv_rows(conflict_audit_path)
    if not (file_rows and reference_rows and conflict_rows and tuning_path.exists()):
        return False
    audited_files = {row.get("generated_file", "") for row in file_rows}
    if not required_generated_files.issubset(audited_files):
        return False
    generated_common_root = repo_root / "mods/StellarAIDirector/common"
    for relative in required_generated_files:
        path = generated_common_root / relative.removeprefix("common/")
        if not path.exists():
            return False
        try:
            parse_file(path)
        except PDXParseError:
            return False
    classifications = {row.get("classification", "") for row in conflict_rows}
    tuning = read_text(tuning_path).lower()
    return (
        not any(row.get("status") != "ok" for row in file_rows)
        and not any(row.get("status") == "missing" for row in reference_rows)
        and not any(row.get("classification") == "unexpected_parent_object_collision" for row in conflict_rows)
        and {"additive_director_object", "intentional_director_override"}.issubset(classifications)
        and "generated full-object route overrides now cover" in tuning
        and "direct technology/ap/tradition route overrides are emitted" in tuning
        and "esc starbase reactor override" in tuning
    )


def irony_conflict_scan_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    scan_path = repo_root / "research/stellar-ai/stellar-ai-director-irony-conflict-scan-2026-07-04.md"
    conflict_audit_path = repo_root / "research/stellar-ai/stellar-ai-director-generated-conflicts-2026-07-04.csv"
    order_proof_path = repo_root / "research/stellar-ai/stellar-ai-director-irony-order-proof-2026-07-04.md"
    if not all(path.exists() for path in (scan_path, conflict_audit_path, order_proof_path)):
        return False
    scan_text = read_text(scan_path).lower()
    order_text = read_text(order_proof_path).lower()
    required_scan_terms = {
        "irony conflict solver",
        "analyze only",
        "4.4 stellaris mod collection w/load order: nsc3, planetary diversity",
        "common\\ai_budget",
        "conflict count: 3000",
        "!!!universal resource patch [2.4+]",
        "stellar ai director",
        "lios",
        "intentional director win",
        "no unexplained director gameplay conflicts",
    }
    required_order_terms = {
        "status: ok",
        "existing_mod_order_preserved: true",
    }
    if not all(term in scan_text for term in required_scan_terms):
        return False
    if not all(term in order_text for term in required_order_terms):
        return False
    if not all(object_name in scan_text for object_name in IRONY_REVIEWED_CONFLICT_OBJECTS):
        return False
    conflict_rows = _read_csv_rows(conflict_audit_path)
    reviewed_rows = [
        row
        for row in conflict_rows
        if row.get("object_name") in IRONY_REVIEWED_CONFLICT_OBJECTS
        and row.get("classification") == "intentional_director_override"
        and row.get("object_type") == "ai_budget"
    ]
    return (
        len({row.get("object_name") for row in reviewed_rows}) == len(IRONY_REVIEWED_CONFLICT_OBJECTS)
        and not any(row.get("classification") == "unexpected_parent_object_collision" for row in conflict_rows)
    )


def validator_artifact_passes(validation_errors: list[str], repo_root: Path = REPO_ROOT) -> bool:
    if validation_errors:
        return False
    audit_paths = [
        repo_root / "research/stellar-ai/stellar-ai-director-generated-file-audit-2026-07-04.csv",
        repo_root / "research/stellar-ai/stellar-ai-director-generated-reference-audit-2026-07-04.csv",
        repo_root / "research/stellar-ai/stellar-ai-director-generated-conflicts-2026-07-04.csv",
        repo_root / "research/stellar-ai/stellar-ai-director-dependency-audit-2026-07-04.csv",
        repo_root / "research/stellar-ai/stellar-ai-director-roi-quality-audit-2026-07-04.csv",
        repo_root / "research/stellar-ai/stellar-ai-director-integration-policy-audit-2026-07-04.csv",
        repo_root / "research/stellar-ai/stellar-ai-director-irony-order-proof-2026-07-04.json",
    ]
    if not all(path.exists() for path in audit_paths):
        return False
    file_rows = _read_csv_rows(audit_paths[0])
    reference_rows = _read_csv_rows(audit_paths[1])
    conflict_rows = _read_csv_rows(audit_paths[2])
    dependency_rows = _read_csv_rows(audit_paths[3])
    roi_quality_rows = _read_csv_rows(audit_paths[4])
    integration_rows = _read_csv_rows(audit_paths[5])
    return (
        file_rows
        and reference_rows
        and conflict_rows
        and dependency_rows
        and roi_quality_rows
        and integration_rows
        and all(row.get("status") == "ok" for row in file_rows)
        and not any(row.get("status") == "missing" for row in reference_rows)
        and not any(row.get("classification") == "unexpected_parent_object_collision" for row in conflict_rows)
        and all(row.get("status") == "ok" for row in dependency_rows)
        and not any(row.get("status") == "fail" for row in roi_quality_rows)
        and not any(row.get("status") == "fail" for row in integration_rows)
        and irony_order_proof_artifact_passes(repo_root)
    )


def documentation_artifact_passes(repo_root: Path = REPO_ROOT) -> bool:
    readme_path = repo_root / "mods/StellarAIDirector/README.md"
    load_order_path = repo_root / "mods/StellarAIDirector/notes/load-order.md"
    conflicts_path = repo_root / "mods/StellarAIDirector/notes/conflicts.md"
    observer_path = repo_root / "mods/StellarAIDirector/notes/observer-test-log.md"
    tuning_path = repo_root / "mods/StellarAIDirector/notes/tuning-notes.md"
    if not all(path.exists() for path in (readme_path, load_order_path, conflicts_path, observer_path, tuning_path)):
        return False
    combined = "\n".join(read_text(path).lower() for path in (readme_path, load_order_path, conflicts_path, observer_path, tuning_path))
    required_terms = {
        "gigastructural engineering & more (4.4)",
        "extra ship components next",
        "nsc3",
        "!!!universal resource patch [2.4+]",
        "stellar ai director",
        "validation",
        "load order",
        "intentional",
        "tuning",
        "observer",
        "stellar ai director loaded",
        "irony",
    }
    return all(term in combined for term in required_terms)


def classify_plan_phase_status(
    phase: str,
    artifacts: list[dict[str, Any]],
    validation_errors: list[str],
    main_menu_status: dict[str, Any],
    observer_log_text: str,
    repo_root: Path = REPO_ROOT,
) -> str:
    if phase in PLAN_PHASE_SUPERSEDED_REASONS:
        return "superseded"
    if any(not artifact["exists"] for artifact in artifacts):
        return "missing"
    if phase == "P0" and munch_preflight_artifact_passes(repo_root):
        return "verified"
    if phase == "P0":
        return "external_gate"
    if phase == "P2" and irony_order_proof_artifact_passes(repo_root):
        return "verified"
    if phase == "P1" and source_corpus_artifact_passes(repo_root):
        return "verified"
    if phase == "P3" and roi_model_artifact_passes(repo_root):
        return "verified"
    if phase == "P4" and decision_tree_artifact_passes(repo_root):
        return "verified"
    if phase == "P5" and generated_surface_artifact_passes(repo_root):
        return "verified"
    if phase == "P12" and validation_errors:
        return "failing"
    if phase == "P12" and validator_artifact_passes(validation_errors, repo_root):
        return "verified"
    if phase == "P13" and irony_conflict_scan_artifact_passes(repo_root):
        return "verified"
    if phase == "P6" and unlock_priority_policy_artifact_passes(repo_root):
        return "verified"
    if phase == "P7" and mega_giga_policy_artifact_passes(repo_root):
        return "verified"
    if phase == "P8" and shipyard_policy_artifact_passes(repo_root):
        return "verified"
    if phase == "P9" and starbase_policy_artifact_passes(repo_root):
        return "verified"
    if phase == "P10" and planetary_capacity_policy_artifact_passes(repo_root):
        return "verified"
    if phase == "P11" and nsc3_esc_policy_artifact_passes(repo_root):
        return "verified"
    if phase == "P16" and documentation_artifact_passes(repo_root):
        return "verified"
    if phase in PLAN_PHASE_OPEN_REASONS:
        return "partial"
    return "verified"


def collect_plan_completion_status(
    plan_path: Path = PLAN_PATH,
    repo_root: Path = REPO_ROOT,
    mod_root: Path = MOD_ROOT,
    main_menu_proof_path: Path = MAIN_MENU_PROOF_PATH,
    validation_errors: list[str] | None = None,
) -> dict[str, Any]:
    checklist = extract_completion_checklist_items(read_text(plan_path))
    validation_errors = validate_generated_patch() if validation_errors is None else validation_errors
    main_menu_status = read_main_menu_proof_status(main_menu_proof_path)
    observer_log_path = mod_root / "notes" / "observer-test-log.md"
    observer_text = read_text(observer_log_path) if observer_log_path.exists() else ""
    phases = []
    for item in checklist:
        phase = item["phase"]
        artifacts = plan_phase_artifact_rows(phase, repo_root)
        status = classify_plan_phase_status(phase, artifacts, validation_errors, main_menu_status, observer_text, repo_root)
        phases.append(
            {
                **item,
                "status": status,
                "open_reason": (
                    ""
                    if status == "verified"
                    else PLAN_PHASE_SUPERSEDED_REASONS.get(phase, PLAN_PHASE_OPEN_REASONS.get(phase, ""))
                ),
                "artifacts": artifacts,
            }
        )
    counts: dict[str, int] = {}
    for phase in phases:
        counts[phase["status"]] = counts.get(phase["status"], 0) + 1
    return {
        "plan_path": str(plan_path),
        "overall_status": (
            "complete"
            if sum(counts.get(status, 0) for status in ("verified", "superseded")) == len(phases)
            else "not_complete"
        ),
        "phase_count": len(phases),
        "status_counts": counts,
        "validation_error_count": len(validation_errors),
        "main_menu_proven": main_menu_status["main_menu_proven"],
        "main_menu_missing_modes": main_menu_status["missing_modes"],
        "phases": phases,
    }


def plan_completion_report_text(status: dict[str, Any]) -> str:
    lines = [
        "# Stellar AI Director V1 Plan Status",
        "",
        f"Overall status: {status['overall_status']}",
        f"Phase count: {status['phase_count']}",
        f"Validation errors: {status['validation_error_count']}",
        f"Main menu proven: {status['main_menu_proven']}",
        f"Main menu missing modes: {', '.join(status['main_menu_missing_modes']) or 'none'}",
        "",
        "| phase | status | requirement | evidence | open reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for phase in status["phases"]:
        evidence = "; ".join(
            f"{artifact['path']}={'present' if artifact['exists'] else 'missing'}" for artifact in phase["artifacts"]
        )
        if not evidence:
            evidence = "session/external evidence required"
        lines.append(
            f"| {phase['phase']} | {phase['status']} | {phase['requirement']} | {evidence} | {phase['open_reason']} |"
        )
    return "\n".join(lines) + "\n"


def generate_plan_status_artifacts() -> dict[str, Any]:
    status = collect_plan_completion_status()
    write_json(PLAN_STATUS_JSON, status)
    write_text_file(PLAN_STATUS_MD, plan_completion_report_text(status))
    return status


def launcher_descriptor_text(mod_root: Path = MOD_ROOT) -> str:
    path = mod_root.resolve().as_posix()
    return descriptor_text() + f'path="{path}"\n'


def launcher_descriptor_path(launcher_mod_root: Path = PARADOX_MOD_ROOT) -> Path:
    return launcher_mod_root / "StellarAIDirector.mod"


def collect_launcher_installation_state(
    launcher_mod_root: Path = PARADOX_MOD_ROOT,
    mod_root: Path = MOD_ROOT,
    dlc_load_path: Path = DLC_LOAD_PATH,
) -> dict[str, Any]:
    descriptor = launcher_descriptor_path(launcher_mod_root)
    expected_path = mod_root.resolve().as_posix()
    enabled_mod_entry = DIRECTOR_DLC_LOAD_ENTRY
    actual_path = ""
    enabled_mods: list[str] = []
    if dlc_load_path.exists():
        enabled_mods = json.loads(read_text(dlc_load_path)).get("enabled_mods", [])
    if descriptor.exists():
        match = re.search(r'^\s*path\s*=\s*"([^"]+)"', read_text(descriptor), flags=re.MULTILINE)
        if match:
            actual_path = Path(match.group(1)).resolve().as_posix()
    return {
        "descriptor_path": str(descriptor),
        "descriptor_exists": descriptor.exists(),
        "source_mod_path": expected_path,
        "source_descriptor_exists": (mod_root / "descriptor.mod").exists(),
        "descriptor_points_to_source": actual_path == expected_path,
        "descriptor_path_value": actual_path,
        "dlc_load_path": str(dlc_load_path),
        "dlc_load_exists": dlc_load_path.exists(),
        "enabled_mod_entry": enabled_mod_entry,
        "enabled_in_dlc_load": enabled_mod_entry in enabled_mods,
    }


def install_launcher_descriptor(
    launcher_mod_root: Path = PARADOX_MOD_ROOT,
    mod_root: Path = MOD_ROOT,
) -> Path:
    descriptor = launcher_descriptor_path(launcher_mod_root)
    write_text_file(descriptor, launcher_descriptor_text(mod_root))
    return descriptor


def set_director_enabled_in_dlc_load(enabled: bool, dlc_load_path: Path = DLC_LOAD_PATH) -> Path:
    data = {"disabled_dlcs": [], "enabled_mods": []}
    if dlc_load_path.exists():
        data = json.loads(read_text(dlc_load_path))
    enabled_mods = data.setdefault("enabled_mods", [])
    if enabled:
        if DIRECTOR_DLC_LOAD_ENTRY not in enabled_mods:
            enabled_mods.append(DIRECTOR_DLC_LOAD_ENTRY)
    else:
        data["enabled_mods"] = [entry for entry in enabled_mods if entry != DIRECTOR_DLC_LOAD_ENTRY]
    data.setdefault("disabled_dlcs", [])
    dlc_load_path.parent.mkdir(parents=True, exist_ok=True)
    dlc_load_path.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    return dlc_load_path


def enable_director_in_dlc_load(dlc_load_path: Path = DLC_LOAD_PATH) -> Path:
    return set_director_enabled_in_dlc_load(True, dlc_load_path)


def disable_director_in_dlc_load(dlc_load_path: Path = DLC_LOAD_PATH) -> Path:
    return set_director_enabled_in_dlc_load(False, dlc_load_path)


def collect_load_proof_contract(mod_root: Path = MOD_ROOT) -> dict[str, Any]:
    files = {
        "on_action": mod_root / "common" / "on_actions" / "zzz_staid_load_proof_on_actions.txt",
        "event": mod_root / "events" / "zzz_staid_load_proof_events.txt",
        "localisation": mod_root / "localisation" / "english" / "staid_load_proof_l_english.yml",
    }
    errors: list[str] = []
    for label, path in files.items():
        if not path.exists():
            errors.append(f"Load-proof {label} file is missing: {path}")

    on_action = files["on_action"]
    if on_action.exists():
        text = read_text(on_action)
        try:
            parse_file(on_action)
        except PDXParseError as exc:
            errors.append(f"Load-proof on_action parse failed: {exc}")
        if "on_game_start_country" not in text:
            errors.append("Load-proof on_action does not hook on_game_start_country")
        if LOAD_PROOF_EVENT_ID not in text:
            errors.append(f"Load-proof on_action does not reference {LOAD_PROOF_EVENT_ID}")

    event = files["event"]
    if event.exists():
        text = read_text(event)
        try:
            parse_file(event)
        except PDXParseError as exc:
            errors.append(f"Load-proof event parse failed: {exc}")
        required_fragments = (
            "namespace = staid_load_proof",
            "country_event =",
            f"id = {LOAD_PROOF_EVENT_ID}",
            f"title = {LOAD_PROOF_EVENT_ID}.name",
            f"desc = {LOAD_PROOF_EVENT_ID}.desc",
            "picture = GFX_evt_grand_speech",
            "show_sound = event_default",
            "is_triggered_only = yes",
            "fire_only_once = yes",
            "is_ai = no",
            LOAD_PROOF_LOG_MARKER,
            f"name = {LOAD_PROOF_EVENT_ID}.a",
        )
        for fragment in required_fragments:
            if fragment not in text:
                errors.append(f"Load-proof event is missing expected fragment: {fragment}")

    localisation = files["localisation"]
    if localisation.exists():
        raw = localisation.read_bytes()
        text = read_text(localisation)
        if not raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"Load-proof localisation must be UTF-8 BOM encoded: {localisation}")
        for key in (f"{LOAD_PROOF_EVENT_ID}.name", f"{LOAD_PROOF_EVENT_ID}.desc", f"{LOAD_PROOF_EVENT_ID}.a"):
            if key not in text:
                errors.append(f"Load-proof localisation is missing key: {key}")
        if LOAD_PROOF_TITLE not in text:
            errors.append(f"Load-proof localisation title is not {LOAD_PROOF_TITLE!r}")

    return {
        "status": "ok" if not errors else "fail",
        "errors": errors,
        "files": {label: str(path) for label, path in files.items()},
    }


def generate_roi_artifacts() -> list[dict[str, Any]]:
    rows = extract_megastructure_rows()
    write_csv(RESEARCH_ROOT / "stellar-ai-director-roi-matrix-2026-07-04.csv", rows)
    write_csv(RESEARCH_ROOT / "stellar-ai-director-market-values-2026-07-04.csv", market_price_rows())
    generate_roi_quality_audit_artifacts(rows)
    generate_integration_surface_artifacts()
    thresholds = generated_thresholds(rows)
    top_rows = [row for row in rows if row["decision_eligible"] == "yes"][:40]
    lines = [
        "# Stellar AI Director ROI Matrix",
        "",
        "Generated from copied 2026-07-04 source snapshots. Values are alloy-equivalent planning heuristics, not game engine runtime values.",
        "",
        "Market-aware columns use `market_amount` / `market_price` from `common/strategic_resources` and market caps from vanilla `common/defines/00_defines.txt`.",
        "Deficit values use the no-fee max-buy ceiling. Surplus values use the no-fee min-sell floor. Default-fee columns are included separately for stress testing.",
        "Strategic shipyard columns are not income. They estimate fleet-construction throughput for empires with enough alloy/energy surplus to exploit added shipyard capacity.",
        "",
        "Rows marked `decision_eligible = no` are kept for auditability but are excluded from generated priority thresholds.",
        "",
        "## Generated Thresholds",
        "",
        "| threshold | value |",
        "| --- | ---: |",
        *[f"| {key} | {value} |" for key, value in thresholds.items()],
        "",
        "## Top Decision-Eligible Rows",
        "",
        "| priority | object | source | market deficit cost | market payoff/year | market payback | shipyard throughput alloys/year | shipyard payback | quality | notes |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in top_rows:
        lines.append(
            f"| {row['priority_tier']} | `{row['object_name']}` | {row['mod_name']} | "
            f"{row['market_deficit_cost_energy']} | {row['market_deficit_annual_payoff_energy']} | "
            f"{row['market_deficit_payback_years']} | {row['strategic_shipyard_annual_alloy_throughput']} | "
            f"{row['strategic_shipyard_payback_years']} | {row['data_quality']} | "
            f"role {row['director_strategy_role']}; gate {row['director_build_gate']}; "
            f"surplus sink {row['director_surplus_sink_priority']}:{row['director_surplus_sink_role']}; "
            f"shipyards {row['shipyard_capacity']}; build speed {row['build_speed']}; "
            f"source ai weight {row['source_has_ai_weight']}; produces {row['produces']}; unpriced {row['market_unpriced_resources']} |"
        )
    write_text_file(RESEARCH_ROOT / "stellar-ai-director-roi-matrix-2026-07-04.md", "\n".join(lines) + "\n")
    return rows


def generate_mod_files(rows: list[dict[str, Any]] | None = None) -> None:
    rows = rows or extract_megastructure_rows()
    thresholds = generated_thresholds(rows)
    playset = build_active_playset_snapshot()
    write_json(RESEARCH_ROOT / "stellar-ai-director-active-playset-2026-07-04.json", playset)
    write_text_file(MOD_ROOT / "descriptor.mod", descriptor_text())
    write_text_file(MOD_ROOT / "README.md", readme_text(playset))
    write_text_file(
        MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt",
        triggers_text(thresholds),
    )
    write_text_file(MOD_ROOT / "common" / "ai_budget" / "zzz_staid_alloys_budget.txt", ai_budget_text(thresholds))
    write_text_file(MOD_ROOT / "common" / "ai_budget" / "zzz_staid_gigas_resource_budgets.txt", gigas_resource_budget_text())
    write_text_file(MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt", economic_plan_text())
    write_text_file(
        MOD_ROOT / "common" / "on_actions" / "zzz_staid_market_and_fleet_safety_on_actions.txt",
        market_and_fleet_safety_on_actions_text(),
    )
    write_text_file(MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt", market_and_fleet_safety_events_text())
    write_text_file(MOD_ROOT / "common" / "script_values" / "zzz_staid_roi_values.txt", script_values_text(thresholds))
    generate_route_override_artifacts()
    write_text_file(
        RESEARCH_ROOT / "stellar-ai-director-implementation-notes-2026-07-04.md",
        implementation_notes_text(playset, thresholds),
    )
    notes_root = MOD_ROOT / "notes"
    write_text_file(notes_root / "load-order.md", load_order_note_text(playset))
    write_text_file(notes_root / "conflicts.md", conflicts_note_text())
    write_text_file(notes_root / "observer-test-log.md", observer_test_log_text(playset))
    write_text_file(notes_root / "tuning-notes.md", tuning_notes_text(thresholds))
    generate_threat_response_artifacts()
    generate_dependency_audit_artifacts()
    generate_irony_order_proof_artifacts()
    generate_file_audit_artifacts()
    generate_conflict_classification_artifacts()
    generate_reference_audit_artifacts()


def descriptor_text() -> str:
    deps = "\n".join(f'\t"{name}"' for name in [*REQUIRED_MODS.values(), UNIVERSAL_RESOURCE_PATCH_NAME])
    return f'''version="0.1.0"
tags={{
\t"Gameplay"
\t"Balance"
\t"AI"
}}
name="Stellar AI Director"
supported_version="v4.4.*"
dependencies={{
{deps}
}}
'''


def triggers_text(thresholds: dict[str, int]) -> str:
    text = '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Deterministic state gates for late-game investment decisions.

staid_core_deficit_short_runway = {
\tOR = {
\t\thas_deficit = energy
\t\thas_deficit = minerals
\t\thas_deficit = alloys
\t\thas_deficit = trade
\t\tAND = { country_uses_consumer_goods = yes has_deficit = consumer_goods }
\t\tAND = { country_uses_food = yes has_deficit = food }
\t\tAND = {
\t\t\tNOT = { has_monthly_income = { resource = energy value > 0 } }
\t\t\tresource_stockpile_compare = { resource = energy value < 2400 }
\t\t}
\t\tAND = {
\t\t\tNOT = { has_monthly_income = { resource = minerals value > 0 } }
\t\t\tresource_stockpile_compare = { resource = minerals value < 2400 }
\t\t}
\t\tAND = {
\t\t\tNOT = { has_monthly_income = { resource = alloys value > 0 } }
\t\t\tresource_stockpile_compare = { resource = alloys value < 2400 }
\t\t}
\t\tAND = {
\t\t\tNOT = { has_monthly_income = { resource = trade value > 0 } }
\t\t\tresource_stockpile_compare = { resource = trade value < 2400 }
\t\t}
\t}
}

staid_trade_capacity_safe = {
\tNOT = { has_deficit = trade }
\thas_monthly_income = { resource = trade value > 25 }
}

staid_trade_fleet_capacity_safe = {
\tstaid_trade_capacity_safe = yes
\thas_monthly_income = { resource = trade value > 75 }
}

staid_trade_planetary_capacity_safe = {
\tstaid_trade_capacity_safe = yes
\thas_monthly_income = { resource = trade value > 50 }
}

staid_trade_surplus_capacity_safe = {
\tstaid_trade_capacity_safe = yes
\thas_monthly_income = { resource = trade value > 100 }
}

staid_survival_mode = {
\tis_nomadic = no
\tOR = {
\t\tstaid_core_deficit_short_runway = yes
\t\tAND = { recently_lost_war = yes used_naval_capacity_percent < 0.60 }
\t\tAND = { is_at_war = yes highest_threat > 35 used_naval_capacity_percent < 0.75 }
\t}
}

staid_recovery_mode = {
\tis_nomadic = no
\tOR = {
\t\tstaid_survival_mode = yes
\t\tstellarai_basic_econ_recovery_needed = yes
\t\tAND = { recently_lost_war = yes used_naval_capacity_percent < 0.80 }
\t}
}

staid_megastructure_prep_ready = {
\tis_nomadic = no
\tcan_build_megastructures = yes
\tNOT = { staid_recovery_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_trade_planetary_capacity_safe = yes
\tresource_stockpile_compare = { resource = alloys value > 15000 }
\thas_monthly_income = { resource = alloys value > 120 }
\thas_monthly_income = { resource = energy value > 80 }
\thas_monthly_income = { resource = minerals value > 60 }
\tOR = {
\t\tis_at_war = no
\t\tused_naval_capacity_percent > 0.90
\t}
}

staid_megastructure_commit_safe = {
\tis_nomadic = no
\tcan_build_megastructures = yes
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_trade_planetary_capacity_safe = yes
\tOR = {
\t\tis_at_war = no
\t\tused_naval_capacity_percent > 0.85
\t}
}

staid_pause_new_megastructure = {
\tOR = {
\t\tstaid_survival_mode = yes
\t\tAND = { is_at_war = yes used_naval_capacity_percent < 0.85 }
\t\tAND = { highest_threat > 45 used_naval_capacity_percent < 0.90 }
\t}
}

staid_shipyard_payoff_ready = {
\tNOT = { staid_recovery_mode = yes }
\thas_monthly_income = { resource = alloys value > 150 }
\thas_monthly_income = { resource = energy value > 100 }
\tstaid_trade_fleet_capacity_safe = yes
\tresource_stockpile_compare = { resource = alloys value > 10000 }
}

staid_fleet_buildup_economy_safe = {
\tNOT = { staid_recovery_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_trade_fleet_capacity_safe = yes
\thas_monthly_income = { resource = alloys value > 200 }
\thas_monthly_income = { resource = energy value > 150 }
\tresource_stockpile_compare = { resource = alloys value > 15000 }
\tresource_stockpile_compare = { resource = energy value > 8000 }
\tused_naval_capacity_percent < 1.05
}

staid_resource_waste_pressure = {
\tNOT = { staid_core_deficit_short_runway = yes }
\tOR = {
\t\tAND = {
\t\t\thas_monthly_income = { resource = minerals value > 0 }
\t\t\tresource_stockpile_compare = { resource = minerals value > 50000 }
\t\t}
\t\tAND = {
\t\t\tcountry_uses_food = yes
\t\t\thas_monthly_income = { resource = food value > 0 }
\t\t\tresource_stockpile_compare = { resource = food value > 30000 }
\t\t}
\t\tAND = {
\t\t\tcountry_uses_consumer_goods = yes
\t\t\thas_monthly_income = { resource = consumer_goods value > 0 }
\t\t\tresource_stockpile_compare = { resource = consumer_goods value > 30000 }
\t\t}
\t\tAND = {
\t\t\thas_monthly_income = { resource = volatile_motes value > 0 }
\t\t\tresource_stockpile_compare = { resource = volatile_motes value > 800 }
\t\t}
\t\tAND = {
\t\t\thas_monthly_income = { resource = exotic_gases value > 0 }
\t\t\tresource_stockpile_compare = { resource = exotic_gases value > 800 }
\t\t}
\t\tAND = {
\t\t\thas_monthly_income = { resource = rare_crystals value > 0 }
\t\t\tresource_stockpile_compare = { resource = rare_crystals value > 800 }
\t\t}
\t\tAND = {
\t\t\thas_monthly_income = { resource = sr_dark_matter value > 0 }
\t\t\tresource_stockpile_compare = { resource = sr_dark_matter value > 1000 }
\t\t}
\t\tAND = {
\t\t\thas_monthly_income = { resource = sr_zro value > 0 }
\t\t\tresource_stockpile_compare = { resource = sr_zro value > 1000 }
\t\t}
\t\tAND = {
\t\t\thas_monthly_income = { resource = nanites value > 0 }
\t\t\tresource_stockpile_compare = { resource = nanites value > 1000 }
\t\t}
\t\tAND = {
\t\t\thas_technology = tech_ehof_sentient_tier_1
\t\t\thas_monthly_income = { resource = giga_sr_sentient_metal value > 0 }
\t\t\tresource_stockpile_compare = { resource = giga_sr_sentient_metal value > 2500 }
\t\t}
\t}
}

staid_research_under_curve = {
\tNOT = { staid_core_deficit_short_runway = yes }
\tOR = {
\t\tAND = {
\t\t\tyears_passed > 119
\t\t\tOR = {
\t\t\t\thas_monthly_income = { resource = physics_research value < 1000 }
\t\t\t\thas_monthly_income = { resource = society_research value < 1000 }
\t\t\t\thas_monthly_income = { resource = engineering_research value < 1200 }
\t\t\t}
\t\t}
\t\tAND = {
\t\t\tyears_passed > 79
\t\t\tOR = {
\t\t\t\thas_monthly_income = { resource = physics_research value < 750 }
\t\t\t\thas_monthly_income = { resource = society_research value < 750 }
\t\t\t\thas_monthly_income = { resource = engineering_research value < 900 }
\t\t\t}
\t\t}
\t\tAND = {
\t\t\tyears_passed > 44
\t\t\tOR = {
\t\t\t\thas_monthly_income = { resource = physics_research value < 400 }
\t\t\t\thas_monthly_income = { resource = society_research value < 400 }
\t\t\t\thas_monthly_income = { resource = engineering_research value < 550 }
\t\t\t}
\t\t}
\t}
}

staid_surplus_sink_pressure = {
\tNOT = { staid_recovery_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tNOT = { has_deficit = alloys }
\tNOT = { has_deficit = energy }
\tOR = {
\t\tstaid_resource_waste_pressure = yes
\t\tstaid_research_under_curve = yes
\t\tAND = {
\t\t\tstaid_trade_surplus_capacity_safe = yes
\t\t\thas_monthly_income = { resource = alloys value > 300 }
\t\t\thas_monthly_income = { resource = energy value > 300 }
\t\t\tresource_stockpile_compare = { resource = alloys value > 20000 }
\t\t}
\t}
}

staid_research_sink_priority_ready = {
\tstaid_surplus_sink_pressure = yes
}

staid_core_unlock_research_priority_ready = {
\tOR = {
\t\tstaid_surplus_sink_pressure = yes
\t\tstaid_research_under_curve = yes
\t}
\tOR = {
\t\tNOT = { has_technology = tech_mega_engineering }
\t\tNOT = { has_technology = tech_mega_shipyard }
\t\tstaid_research_under_curve = yes
\t}
}

staid_shipyard_expansion_ready = {
\tstaid_fleet_buildup_economy_safe = yes
\thas_technology = tech_mega_shipyard
\tOR = {
\t\tstaid_surplus_sink_pressure = yes
\t\tAND = { is_at_war = yes highest_threat > 35 used_naval_capacity_percent > 0.80 }
\t}
}

staid_fleet_payoff_exploitation_ready = {
\tstaid_shipyard_payoff_ready = yes
\tNOT = { staid_core_deficit_short_runway = yes }
\tused_naval_capacity_percent < 1.05
\tOR = {
\t\tstaid_shipyard_expansion_ready = yes
\t\tAND = { is_at_war = yes highest_threat > 35 }
\t}
}

staid_planetary_capacity_growth_ready = {
\tis_nomadic = no
\tNOT = { staid_recovery_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_trade_planetary_capacity_safe = yes
\thas_monthly_income = { resource = minerals value > 100 }
\thas_monthly_income = { resource = energy value > 100 }
\tresource_stockpile_compare = { resource = minerals value > 5000 }
\tresource_stockpile_compare = { resource = energy value > 5000 }
}

staid_economy_megastructure_build_priority_ready = {
\tstaid_megastructure_commit_safe = yes
\tOR = {
\t\tyears_passed > 79
\t\tstaid_resource_waste_pressure = yes
\t\tstaid_research_under_curve = yes
\t}
}

staid_mega_shipyard_build_priority_ready = {
\tstaid_shipyard_expansion_ready = yes
\thas_technology = tech_mega_shipyard
}

staid_planetcraft_research_priority_ready = {
\tis_nomadic = no
\tNOT = { staid_recovery_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\thas_technology = tech_mega_engineering
\tOR = {
\t\tyears_passed > 79
\t\tstaid_research_under_curve = yes
\t\tstaid_surplus_sink_pressure = yes
\t}
}

staid_planetcraft_build_priority_ready = {
\tstaid_megastructure_commit_safe = yes
\thas_technology = giga_tech_planet_assembly
\thas_monthly_income = { resource = alloys value > 300 }
\tresource_stockpile_compare = { resource = alloys value > 25000 }
}

staid_war_moon_research_priority_ready = {
\tis_nomadic = no
\tNOT = { staid_recovery_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\thas_technology = tech_mega_engineering
\tOR = {
\t\tyears_passed > 79
\t\thas_technology = giga_tech_planet_assembly
\t\tstaid_fleet_buildup_economy_safe = yes
\t}
}

staid_war_moon_build_priority_ready = {
\tstaid_fleet_buildup_economy_safe = yes
\thas_technology = giga_tech_war_moon_2
\thas_monthly_income = { resource = alloys value > 350 }
\tresource_stockpile_compare = { resource = alloys value > 30000 }
}

staid_systemcraft_research_priority_ready = {
\tis_nomadic = no
\tNOT = { staid_recovery_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tOR = {
\t\tyears_passed > 119
\t\thas_technology = giga_tech_war_moon_2
\t\tstaid_surplus_sink_pressure = yes
\t}
}

staid_systemcraft_build_priority_ready = {
\tstaid_megastructure_commit_safe = yes
\thas_ascension_perk = ap_celestial_printing
\thas_technology = giga_tech_war_system_1
\thas_monthly_income = { resource = alloys value > 500 }
\tresource_stockpile_compare = { resource = alloys value > 50000 }
}

staid_gigas_special_resource_unlock_ready = {
\tis_nomadic = no
\tNOT = { staid_recovery_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tOR = {
\t\tyears_passed > 79
\t\tstaid_planetcraft_research_priority_ready = yes
\t\tstaid_systemcraft_research_priority_ready = yes
\t}
}

staid_defensive_starbase_strategy = {
\tis_nomadic = no
\tOR = {
\t\thas_ethic = ethic_pacifist
\t\thas_ethic = ethic_fanatic_pacifist
\t}
}

staid_crisis_starbase_pressure = {
\tis_nomadic = no
\tNOT = { staid_recovery_mode = yes }
\thighest_threat > 50
\thas_monthly_income = { resource = alloys value > 80 }
\thas_monthly_income = { resource = energy value > 60 }
\tresource_stockpile_compare = { resource = alloys value > 5000 }
}

staid_aggressive_fleet_pressure = {
\tOR = {
\t\thas_ethic = ethic_militarist
\t\thas_ethic = ethic_fanatic_militarist
\t}
\tused_naval_capacity_percent < 0.95
}

staid_starbase_defense_economy_safe = {
\tis_nomadic = no
\tNOT = { staid_recovery_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_trade_capacity_safe = yes
\thas_monthly_income = { resource = alloys value > 60 }
\thas_monthly_income = { resource = energy value > 50 }
\tresource_stockpile_compare = { resource = alloys value > 3000 }
\tresource_stockpile_compare = { resource = energy value > 3000 }
}

staid_static_defense_investment_ready = {
\tstaid_starbase_defense_economy_safe = yes
\tOR = {
\t\tAND = {
\t\t\tstaid_defensive_starbase_strategy = yes
\t\t\tNOT = { staid_aggressive_fleet_pressure = yes }
\t\t}
\t\tstaid_crisis_starbase_pressure = yes
\t}
}

staid_unity_sink_priority_ready = {
\tstaid_surplus_sink_pressure = yes
}

staid_homeland_under_attack = {
\tis_at_war = yes
\tOR = {
\t\tany_owned_planet = { is_occupied_flag = yes }
\t\tany_owned_planet = { has_orbital_bombardment = yes }
\t\tAND = { highest_threat > 35 used_naval_capacity_percent < 0.85 }
\t}
}
'''
    return (
        text.replace("resource_stockpile_compare = { resource = alloys value > 15000 }",
                     f"resource_stockpile_compare = {{ resource = alloys value > {thresholds['prep_stockpile_alloys']} }}")
        .replace("has_monthly_income = { resource = alloys value > 120 }",
                 f"has_monthly_income = {{ resource = alloys value > {thresholds['prep_income_alloys']} }}")
        .replace("has_monthly_income = { resource = alloys value > 150 }",
                 f"has_monthly_income = {{ resource = alloys value > {thresholds['shipyard_income_alloys']} }}")
        .replace("resource_stockpile_compare = { resource = alloys value > 10000 }",
                 f"resource_stockpile_compare = {{ resource = alloys value > {thresholds['shipyard_stockpile_alloys']} }}")
    )


def ai_budget_text(thresholds: dict[str, int]) -> str:
    text = '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: intentionally replaces upstream megastructure alloy
# budgeting with high-scale Gigas/NSC3 survival pressure. This is deliberately
# aggressive: an AI that can build megastructures but does not reserve for them
# will lose the modded crisis curve.

alloys_expenditure_megastructures = {
\tresource = alloys
\ttype = expenditure
\tcategory = megastructures

\tpotential = {
\t\tis_country_type = default
\t\tcan_build_megastructures = yes
\t\tNOT = { staid_pause_new_megastructure = yes }
\t}

\tweight = {
\t\tweight = 8

\t\tmodifier = { factor = 0.5 staid_survival_mode = yes }
\t\tmodifier = { factor = 1.5 staid_recovery_mode = yes }
\t\tmodifier = { factor = 5 staid_megastructure_prep_ready = yes }
\t\tmodifier = {
\t\t\tfactor = 8
\t\t\tstaid_megastructure_commit_safe = yes
\t\t\tany_owned_megastructure = { can_be_upgraded = yes }
\t\t}
\t\tmodifier = {
\t\t\tfactor = 5
\t\t\thas_technology = tech_mega_engineering
\t\t}
\t\tmodifier = {
\t\t\tfactor = 3
\t\t\tyears_passed > 79
\t\t}
\t}

\tdesired_min = {
\t\tbase = 25000
\t\tmodifier = { add = 100000 staid_megastructure_prep_ready = yes }
\t\tmodifier = {
\t\t\tadd = 250000
\t\t\tstaid_megastructure_commit_safe = yes
\t\t\tany_owned_megastructure = { can_be_upgraded = yes }
\t\t}
\t\tmodifier = { add = 500000 years_passed > 119 }
\t}

\tdesired_max = {
\t\tbase = 100000
\t\tmodifier = { add = 250000 has_technology = tech_mega_engineering }
\t\tmodifier = { add = 500000 staid_megastructure_prep_ready = yes }
\t\tmodifier = {
\t\t\tadd = 1000000
\t\t\tstaid_megastructure_commit_safe = yes
\t\t\tany_owned_megastructure = { can_be_upgraded = yes }
\t\t}
\t\tmodifier = { add = 1500000 years_passed > 119 }
\t}
}
'''
    return text


def gigas_resource_budget_text() -> str:
    return '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object overrides: intentionally replaces narrow Gigas special-resource
# megastructure budget objects so the Director can pause exotic projects during
# survival/recovery and reserve rare resources for safe commits.

sentient_metal_expenditure_megastructures = {
\tresource = giga_sr_sentient_metal
\ttype = expenditure
\tcategory = megastructures

\tpotential = {
\t\tis_country_type = default
\t\tNOT = { staid_pause_new_megastructure = yes }
\t}

\tweight = {
\t\tweight = 0.35
\t\tmodifier = { factor = 0 staid_survival_mode = yes }
\t\tmodifier = { factor = 0.25 staid_recovery_mode = yes }
\t\tmodifier = { factor = 2 staid_megastructure_commit_safe = yes }
\t}
}

negative_mass_expenditure_megastructures = {
\tresource = giga_sr_negative_mass
\ttype = expenditure
\tcategory = megastructures

\tpotential = {
\t\tis_country_type = default
\t\tNOT = { staid_pause_new_megastructure = yes }
\t}

\tweight = {
\t\tweight = 0.30
\t\tmodifier = { factor = 0 staid_survival_mode = yes }
\t\tmodifier = { factor = 0.20 staid_recovery_mode = yes }
\t\tmodifier = { factor = 2 staid_megastructure_commit_safe = yes }
\t}
}

supertensiles_upkeep_megastructures = {
\tresource = giga_sr_amb_megaconstruction
\ttype = upkeep
\tcategory = megastructures

\tpotential = {
\t\tis_country_type = default
\t\tNOT = { staid_survival_mode = yes }
\t}

\tweight = {
\t\tweight = 1
\t\tmodifier = { factor = 0.25 staid_recovery_mode = yes }
\t\tmodifier = { factor = 1.5 staid_megastructure_commit_safe = yes }
\t}
}
'''


def economic_plan_text() -> str:
    return '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: intentionally replaces `basic_economy_plan` with a
# mod-set-specific high-scale survival plan. This is not a compatibility shim:
# the Director assumes Gigas/NSC3/ESC crisis scaling and forces research,
# alloy, trade, naval-cap, habitat/tall, and megastructure pressure early.

basic_economy_plan = {
\tai_weight = { weight = 5000 }

\tincome = {
\t\tphysics_research = 400
\t\tsociety_research = 400
\t\tengineering_research = 600
\t\talloys = 120
\t\tunity = 120
\t\ttrade = 75
\t}

\tfocus = {
\t\tphysics_research = 150
\t\tsociety_research = 150
\t\tengineering_research = 250
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director early modded research rush"
\t\tpotential = {
\t\t\tyears_passed < 50
\t\t\tNOT = { staid_core_deficit_short_runway = yes }
\t\t}
\t\tincome = {
\t\t\tphysics_research = 350
\t\t\tsociety_research = 350
\t\t\tengineering_research = 550
\t\t\tunity = 100
\t\t}
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director midgame megastructure rush"
\t\tpotential = {
\t\t\tyears_passed > 44
\t\t\tNOT = { staid_core_deficit_short_runway = yes }
\t\t}
\t\tincome = {
\t\t\tphysics_research = 1500
\t\t\tsociety_research = 1500
\t\t\tengineering_research = 2500
\t\t\talloys = 500
\t\t\tenergy = 350
\t\t\tminerals = 350
\t\t\tunity = 300
\t\t\ttrade = 150
\t\t}
\t\tnaval_cap = 600
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director crisis-scale giga rush"
\t\tpotential = {
\t\t\tyears_passed > 79
\t\t\tNOT = { staid_core_deficit_short_runway = yes }
\t\t}
\t\tincome = {
\t\t\tphysics_research = 4500
\t\t\tsociety_research = 4500
\t\t\tengineering_research = 7000
\t\t\talloys = 1500
\t\t\tenergy = 1000
\t\t\tminerals = 1000
\t\t\tunity = 600
\t\t\ttrade = 250
\t\t}
\t\tnaval_cap = 1500
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director planetcraft survival curve"
\t\tpotential = {
\t\t\tyears_passed > 119
\t\t\tNOT = { staid_core_deficit_short_runway = yes }
\t\t}
\t\tincome = {
\t\t\tphysics_research = 10000
\t\t\tsociety_research = 10000
\t\t\tengineering_research = 15000
\t\t\talloys = 3500
\t\t\tenergy = 2500
\t\t\tminerals = 2500
\t\t\tunity = 1200
\t\t\ttrade = 400
\t\t}
\t\tnaval_cap = 3500
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director trade capacity reserve"
\t\tpotential = {
\t\t\tstaid_trade_capacity_safe = yes
\t\t}
\t\tincome = {
\t\t\ttrade = 100
\t\t}
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director trade deficit recovery"
\t\tpotential = {
\t\t\tNOT = { staid_trade_capacity_safe = yes }
\t\t}
\t\tincome = {
\t\t\ttrade = 150
\t\t}
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director mega alloy reserve"
\t\tpotential = {
\t\t\tstaid_megastructure_prep_ready = yes
\t\t}
\t\tincome = {
\t\t\talloys = 15
\t\t\ttrade = 25
\t\t}
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director giga special resource reserve"
\t\tpotential = {
\t\t\tOR = {
\t\t\t\thas_technology = tech_ehof_sentient_tier_1
\t\t\t\thas_technology = tech_nm_utilization_1
\t\t\t\thas_technology = giga_tech_amb_supertensiles
\t\t\t}
\t\t\tNOT = { staid_recovery_mode = yes }
\t\t}
\t\tincome = {
\t\t\tgiga_sr_sentient_metal = 5
\t\t\tgiga_sr_negative_mass = 3
\t\t\tgiga_sr_amb_megaconstruction = 5
\t\t}
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director payoff exploitation alloys"
\t\tpotential = {
\t\t\tstaid_fleet_payoff_exploitation_ready = yes
\t\t}
\t\tincome = {
\t\t\talloys = 20
\t\t\tenergy = 20
\t\t\ttrade = 50
\t\t}
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director modded unlock research reserve"
\t\tpotential = {
\t\t\tOR = {
\t\t\t\tstaid_core_unlock_research_priority_ready = yes
\t\t\t\tyears_passed > 44
\t\t\t}
\t\t}
\t\tincome = {
\t\t\tphysics_research = 1200
\t\t\tsociety_research = 1200
\t\t\tengineering_research = 1800
\t\t\tunity = 250
\t\t}
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director capped stockpile research conversion"
\t\tpotential = {
\t\t\tOR = {
\t\t\t\tstaid_resource_waste_pressure = yes
\t\t\t\tstaid_research_under_curve = yes
\t\t\t}
\t\t}
\t\tincome = {
\t\t\tphysics_research = 1600
\t\t\tsociety_research = 1600
\t\t\tengineering_research = 2200
\t\t\ttrade = 250
\t\t\tunity = 350
\t\t}
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director 2360 physics catchup"
\t\tpotential = {
\t\t\tyears_passed > 119
\t\t\tstaid_research_under_curve = yes
\t\t\thas_monthly_income = { resource = physics_research value < 1200 }
\t\t}
\t\tincome = { physics_research = 1800 }
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director 2360 society catchup"
\t\tpotential = {
\t\t\tyears_passed > 119
\t\t\tstaid_research_under_curve = yes
\t\t\thas_monthly_income = { resource = society_research value < 1200 }
\t\t}
\t\tincome = { society_research = 1800 }
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director 2360 engineering catchup"
\t\tpotential = {
\t\t\tyears_passed > 119
\t\t\tstaid_research_under_curve = yes
\t\t\thas_monthly_income = { resource = engineering_research value < 1400 }
\t\t}
\t\tincome = { engineering_research = 2400 }
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director fleet throughput reserve"
\t\tpotential = {
\t\t\tstaid_shipyard_expansion_ready = yes
\t\t}
\t\tincome = {
\t\t\talloys = 500
\t\t\tenergy = 300
\t\t\ttrade = 150
\t\t}
\t\tnaval_cap = 800
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director threat readiness reserve"
\t\tpotential = {
\t\t\thas_country_flag = staid_tr_defensive_readiness_low
\t\t\tstaid_tr_foreign_affairs_safe = yes
\t\t}
\t\tincome = {
\t\t\talloys = 7
\t\t\tenergy = 6
\t\t\ttrade = 25
\t\t}
\t\tnaval_cap = 40
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director planetary capacity reserve"
\t\tpotential = {
\t\t\tstaid_planetary_capacity_growth_ready = yes
\t\t}
\t\tincome = {
\t\t\tminerals = 500
\t\t\tenergy = 400
\t\t\ttrade = 150
\t\t}
\t\tpops = 400000
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director defensive starbase reserve"
\t\tpotential = {
\t\t\tstaid_static_defense_investment_ready = yes
\t\t}
\t\tincome = {
\t\t\talloys = 18
\t\t\tenergy = 25
\t\t\ttrade = 25
\t\t}
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director crisis starbase reserve"
\t\tpotential = {
\t\t\tstaid_crisis_starbase_pressure = yes
\t\t}
\t\tincome = {
\t\t\talloys = 30
\t\t\tenergy = 40
\t\t\ttrade = 50
\t\t}
\t}
}
'''


def market_cap_breaker_sale_text(resource: str, reserve: int, amount: int, extra_limit: str) -> str:
    extra = f"\n\t\t\t{extra_limit}" if extra_limit else ""
    return f'''\t\tif = {{
\t\t\tlimit = {{{extra}
\t\t\t\tNOT = {{ has_deficit = {resource} }}
\t\t\t\thas_monthly_income = {{ resource = {resource} value > 0 }}
\t\t\t\tresource_stockpile_compare = {{ resource = {resource} value > {reserve} }}
\t\t\t}}
\t\t\tset_variable = {{
\t\t\t\twhich = staid_market_trade_value
\t\t\t\tvalue = value:stellarai_market_sell_value|RESOURCE|{resource}|AMOUNT|{amount}|
\t\t\t}}
\t\t\tif = {{
\t\t\t\tlimit = {{ check_variable = {{ which = staid_market_trade_value value > 0 }} }}
\t\t\t\tadd_resource = {{ {resource} = -{amount} }}
\t\t\t\tadd_resource = {{ trade = 1 mult = staid_market_trade_value }}
\t\t\t}}
\t\t\tclear_variable = staid_market_trade_value
\t\t}}
'''


def market_and_fleet_safety_on_actions_text() -> str:
    return '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Monthly Director safety layer for market cap breaking and stranded fleet recovery.

on_monthly_pulse = {
\tevents = {
\t\tstaid_economy_safety.1
\t}
}
'''


def market_and_fleet_safety_events_text() -> str:
    sales = "\n".join(
        market_cap_breaker_sale_text(resource, reserve, amount, extra_limit)
        for resource, reserve, amount, extra_limit in MARKET_CAP_BREAKER_SALES
    )
    return f'''# Generated by tools/generate_stellar_ai_director_patch.py.
# Uses vanilla `set_mia = mia_return_home` only after a two-pulse stranded-fleet gate.

namespace = staid_economy_safety

event = {{
\tid = staid_economy_safety.1
\thide_window = yes
\tis_triggered_only = yes

\timmediate = {{
\t\tevery_country = {{
\t\t\tlimit = {{
\t\t\t\tis_ai = yes
\t\t\t\tis_nomadic = no
\t\t\t\tOR = {{
\t\t\t\t\tis_regular_empire = yes
\t\t\t\t\tis_gestalt = yes
\t\t\t\t\tis_hive_empire = yes
\t\t\t\t\tis_virtual_empire = yes
\t\t\t\t\tis_galvanic_empire = yes
\t\t\t\t}}
\t\t\t}}
\t\t\tcountry_event = {{ id = staid_economy_safety.2 }}
\t\t\tcountry_event = {{ id = staid_economy_safety.3 }}
\t\t}}
\t}}
}}

country_event = {{
\tid = staid_economy_safety.2
\thide_window = yes
\tis_triggered_only = yes

\timmediate = {{
{sales}
\t}}
}}

country_event = {{
\tid = staid_economy_safety.3
\thide_window = yes
\tis_triggered_only = yes

\timmediate = {{
\t\tif = {{
\t\t\tlimit = {{
\t\t\t\tstaid_homeland_under_attack = yes
\t\t\t}}
\t\t\tevery_owned_fleet = {{
\t\t\t\tlimit = {{
\t\t\t\t\tcan_go_mia = yes
\t\t\t\t\tis_fleet_idle = yes
\t\t\t\t\tis_in_combat = no
\t\t\t\t\tfleet_power > 1000
\t\t\t\t\tsolar_system = {{
\t\t\t\t\t\texists = space_owner
\t\t\t\t\t\tspace_owner = {{ NOT = {{ is_same_value = root }} }}
\t\t\t\t\t}}
\t\t\t\t}}
\t\t\t\tif = {{
\t\t\t\t\tlimit = {{ has_fleet_flag = staid_stranded_fleet_warning }}
\t\t\t\t\tremove_fleet_flag = staid_stranded_fleet_warning
\t\t\t\t\tset_mia = mia_return_home
\t\t\t\t}}
\t\t\t\telse = {{
\t\t\t\t\tset_timed_fleet_flag = {{
\t\t\t\t\t\tflag = staid_stranded_fleet_warning
\t\t\t\t\t\tdays = 70
\t\t\t\t\t}}
\t\t\t\t}}
\t\t\t}}
\t\t}}
\t\telse = {{
\t\t\tevery_owned_fleet = {{
\t\t\t\tlimit = {{ has_fleet_flag = staid_stranded_fleet_warning }}
\t\t\t\tremove_fleet_flag = staid_stranded_fleet_warning
\t\t\t}}
\t\t}}
\t}}
}}
'''


def script_values_text(thresholds: dict[str, int]) -> str:
    return f'''# Generated by tools/generate_stellar_ai_director_patch.py.
# Numeric anchors for documentation, debug events, and future generated gates.

staid_alloy_equivalent_alloys = 1
staid_alloy_equivalent_minerals = 0.35
staid_alloy_equivalent_energy = 0.25
staid_alloy_equivalent_consumer_goods = 0.75
staid_alloy_equivalent_unity = 0.50
staid_min_megastructure_prep_alloys = {thresholds["prep_stockpile_alloys"]}
staid_min_megastructure_prep_income_alloys = {thresholds["prep_income_alloys"]}
staid_shipyard_payoff_stockpile_alloys = {thresholds["shipyard_stockpile_alloys"]}
staid_shipyard_payoff_income_alloys = {thresholds["shipyard_income_alloys"]}
staid_roi_matrix_eligible_rows = {thresholds["eligible_roi_rows"]}
staid_safe_deficit_runway_months = 24
'''


def readme_text(playset: dict[str, Any]) -> str:
    missing = [info["name"] for info in playset["required_mods"].values() if not info["present"]]
    return f'''# Stellar AI Director

Late-loading deterministic AI policy patch for the active Irony playset.

This mod is a deterministic, full-power AI replacement policy for the current
4.4 high-scale playset. It does not try to preserve vanilla or Stellar AI
assumptions after the opening curve; it encodes explicit state gates,
priorities, and emergency exits for Gigastructural Engineering, NSC3, ESC NEXT,
Starbase Extended, and the active supporting mods.

## Required Parents

- Stellar AI
- Gigastructural Engineering & More (4.4)
- NSC3
- Extra Ship Components NEXT
- Starbase Extended 3.0
- !!!Universal Resource Patch [2.4+]

Detected selected collection: `{playset["collection_name"]}`.

Missing required Steam parents during generation: {", ".join(missing) if missing else "none"}.

## Scope

- Adds scripted decision-state triggers for survival, recovery, megastructure
  prep, safe commit, surplus-sink pressure, and shipyard payoff exploitation.
- Overrides Stellar AI's megastructure alloy budget object with explicit
  emergency exits and larger reserves for Gigas/NSC3-scale projects.
- Replaces the base economic plan with a mod-set-specific high-scale survival
  plan that forces research, alloy, trade, naval-cap, tall-scaling, and
  megastructure pressure on a mid-2300s crisis curve.
- Adds economic-plan targets for alloy reserves, Gigas special resources,
  and static-defense/starbase pressure when empires need to climb toward
  Gigas/NSC3/ESC-scale economy and fleet power.
- Adds trade-capacity recovery and reserve subplans so the Director preserves
  Stellaris 4.4 logistics/upkeep headroom instead of treating trade as a
  normal buy/sell commodity.
- Adds a monthly market cap-breaker for AI empires that are wasting large
  positive-income stockpiles, converting marketable overflow into trade
  currency instead of letting storage caps void the income.
- Adds a two-pulse stranded-fleet recovery guard that uses vanilla
  `set_mia = mia_return_home` only for idle, MIA-eligible AI fleets outside
  their owner's space while the homeland is under wartime pressure.
- Adds a fleet-throughput economic subplan so Mega Shipyard unlocks and strong
  surplus can become fleet power without ignoring energy/alloy/trade runway checks.
- Adds a planetary-capacity economic subplan plus direct research lab and
  habitat science district construction weights for safe mineral/energy-backed
  tall growth without broad job automation rewrites or trade logistics collapse.
- Adds mandatory unlock-research pressure so AI empires keep pushing
  engineering/research/unity toward Mega Engineering, Mega Shipyard,
  planetcraft/systemcraft chains, NSC hulls, and ESC component tiers.
- Adds a bounded V1 threat-response layer for observed classified aggression:
  opinion modifiers, timed relation/country flags, and a third-party defensive
  readiness economy subplan capped at alloys 7, energy 6, and naval cap 40.
- Keeps unknown or unclassified war goals inert and does not declare wars,
  join wars, add punitive casus belli, or override diplomatic actions.
- Adds full-object route overrides for Mega Engineering, Mega Shipyard, Gigas
  planetcraft/systemcraft unlocks, NSC3 hull unlocks, ESC high-tier component
  unlocks, AP/tradition pressure, economy megastructures, planetcraft, war moon,
  systemcraft, and ESC starbase reactor support.
- Leaves ESC internal component-template `key = ...` overrides and direct NSC3
  ship-design templates as manual-review blockers until the atlas models those
  loader surfaces safely.

## Load Order

Place Stellar AI Director after all required parents and after parent
compatibility patches that the Director must supersede. In the current selected
collection, the latest required parent is at load position
{max((info["load_position"] or 0) for info in playset["required_mods"].values())}.
The Director should be below Stellar AI so its megastructure alloy reserve
override wins intentionally.

## Load Proof

When a player-controlled country starts, the mod fires a one-time popup titled
`{LOAD_PROOF_TITLE}`. Seeing that popup proves Irony loaded the Director into
the active playset and the game executed the Director event/on_action surface.

## Surplus Sink Ordering

After survival and recovery gates, the Director treats strong alloy/energy
surplus, capped marketable resources, or under-curve research as signals that
the empire needs useful spending outlets. The v1 order is:

1. research sink;
2. fleet-production sink;
3. unity sink.

`source_has_ai_weight` in the ROI matrix only reports whether the parent mod
defined an upstream AI weight. The Director's own policy is expressed in the
separate `director_*` columns.

## Validation

Run:

```powershell
python tools/validate_stellar_ai_director_patch.py
python -m unittest discover -s tools/tests
```
'''


def implementation_notes_text(playset: dict[str, Any], thresholds: dict[str, int]) -> str:
    lines = [
        "# Stellar AI Director Implementation Notes",
        "",
        "Generated 2026-07-04 from copied source snapshots and the selected Irony collection.",
        "",
        "## Decision Surfaces",
        "",
        "| surface | file | risk | reason |",
        "| --- | --- | --- | --- |",
        "| state gates | `common/scripted_triggers/zzz_staid_decision_state_triggers.txt` | low | additive namespaced triggers |",
        "| unlock-research policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive economic-plan subplan extends Stellar AI research pressure into validated modded unlock gates |",
        "| alloy reserves | `common/ai_budget/zzz_staid_alloys_budget.txt` | medium | intentional full-object override of Stellar AI megastructure budget |",
        "| Gigas special-resource reserves | `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` | medium | intentional full-object overrides of Gigas megastructure special-resource budgets |",
        "| economy targets | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | high | intentional full-object replacement of `basic_economy_plan` with high-scale Gigas/NSC3/ESC survival targets |",
        "| fleet-throughput policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | medium | replacement economic-plan subplan maps shipyard ROI into crisis-scale alloy/energy/naval-cap targets after anti-collapse gates |",
        "| route unlock overrides | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | high | full-object copied source overrides add Director AI weights for Mega Engineering, Mega Shipyard, Gigas, NSC3, ESC, and starbase unlock chains |",
        "| AP/tradition route overrides | `common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt`, `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` | medium | full-object copied source overrides add Director AI weights for Gigas, planetcraft, conquest escape, economy, and crowded tall routes |",
        "| megastructure route overrides | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | high | full-object copied source overrides add Director AI weights for economy multipliers, Mega Shipyard, planetcraft, war moon, and systemcraft starts |",
        "| starbase static-defense policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt`, `common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt` | medium | additive economy reserves plus copied ESC starbase reactor AI weight support when crisis pressure is safe |",
        "| planetary-capacity policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive economic-plan subplan raises mineral/energy, pop, and empire-size targets without building/job IDs |",
        "| trade-capacity policy | `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`, `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive triggers and economy targets preserve Stellaris 4.4 trade logistics for ship, colony, market, and imbalance pressure |",
        "| cap-breaker market safety | `common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt`, `events/zzz_staid_market_and_fleet_safety_events.txt` | medium | additive monthly event sells large marketable positive-income overflow using Stellar AI market value script instead of allowing capped resources to void income |",
        "| stranded-fleet recovery | `common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt`, `events/zzz_staid_market_and_fleet_safety_events.txt` | medium | two-pulse guard marks idle MIA-eligible fleets outside owner space under homeland attack, then uses vanilla `set_mia = mia_return_home` if still stranded |",
        "| ROI anchors | `common/script_values/zzz_staid_roi_values.txt` | low | additive namespaced values |",
        "| threat-response values/triggers | `common/script_values/zzz_staid_threat_response_values.txt`, `common/scripted_triggers/zzz_staid_threat_response_triggers.txt` | low | additive `staid_tr_` namespace with unknown-war-goal inertness and foreign-affairs safety gates |",
        "| threat-response opinions/events | `common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`, `common/on_actions/zzz_staid_threat_response_on_actions.txt`, `events/zzz_staid_threat_response_events.txt` | medium | event-dispatched opinion/readiness response gated by attacker leader, awareness, participant exclusion, and forbidden-effect validation |",
        "| integration surface ledger | `research/stellar-ai-director-integration-surfaces-2026-07-04.csv` | low | parsed source-object evidence for P6-P11 minimum interventions |",
        "",
        "## Selected Playset",
        "",
        f"- Collection: {playset['collection_name']}",
        f"- Mod count: {playset['mod_count']}",
        f"- Irony patch mod enabled: {playset['patch_mod_enabled']}",
        "",
        "## Required Parent Detection",
        "",
        "| mod | present | load position |",
        "| --- | --- | ---: |",
    ]
    for info in playset["required_mods"].values():
        lines.append(f"| {info['name']} | {info['present']} | {info['load_position']} |")
    lines.extend(
        [
            "",
            "## Generated ROI Thresholds",
            "",
            "These values are generated from rows where `data_quality = resolved` and `decision_eligible = yes`.",
            "",
            "| threshold | value |",
            "| --- | ---: |",
        ]
    )
    for key, value in thresholds.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Surplus Sink Policy",
            "",
            "Surplus is no longer treated as the only time the AI may climb. In this playset, capped marketable resources and under-curve research are strategic failures even when alloy reserves are not yet high. The replacement economic plan forces research, alloy, trade, naval-cap, and megastructure pressure on time gates, while still using survival/recovery gates to prevent immediate deficit death spirals.",
            "",
            "## Trade-Capacity Policy",
            "",
            "Stellaris 4.4 treats `trade` as a standard advanced resource and the market resource, but local vanilla ship-size files also use `logistics = { trade = ... }` and vanilla economic plans target trade income through intermediate, mature, and endgame stages. The Director therefore models trade as logistics/capacity headroom: it is not converted through market ROI pricing, and fleet, planet, defense, surplus, and megastructure gates require explicit trade income floors before adding more upkeep pressure.",
            "",
            "## Market Cap-Breaker Policy",
            "",
            "Stellar AI's parent monthly market script sells only a small bounded number of surplus batches. The Director adds a late-loading monthly safety event for large positive-income overflow in marketable resources: minerals, food, consumer goods, volatile motes, exotic gases, rare crystals, Zro, dark matter, nanites, and verified market-priced Gigas sentient metal. Alloys, energy, unity, negative mass, and ambiguous non-market Gigas construction resources are intentionally excluded from direct forced selling.",
            "",
            "## Stranded-Fleet Recovery Policy",
            "",
            "The Director does not issue normal fleet orders. Runtime evidence points to fleets stranded after access changes or war-end border changes, so the generated safety layer uses the vanilla-supported `set_mia = mia_return_home` mechanic behind a two-pulse guard. A fleet must be AI-owned, idle, out of combat, `can_go_mia = yes`, outside its owner's space, and still marked on the next monthly pulse while the country has wartime homeland pressure before forced MIA recovery fires.",
            "",
            "## Unlock-Research Policy",
            "",
            "The Director treats modded unlock research as mandatory survival pressure. Core targets include Mega Engineering, Mega Shipyard, Gigas planetcraft/systemcraft chains, NSC3 large hull infrastructure, ESC high-tier components, and the economy techs needed to feed them. Full-object copied source overrides now add direct AI weights for those route unlocks and for selected AP/tradition route pressure.",
            "",
            "## Static-Defense Policy",
            "",
            "Defensive starbase investment is expressed as additive `basic_economy_plan` subplans plus a copied ESC starbase reactor override. The v1 policy requires no recovery mode, no short-runway core deficit, safe alloy/energy income and stockpiles, then either defensive ethics without an aggressive under-cap fleet push or high threat pressure.",
            "",
            "## Planetary-Capacity Policy",
            "",
            "Expanded planet and building capacity is covered through a safe country-level economic-plan subplan plus direct research infrastructure overrides for Stellar AI research labs and the vanilla habitat science district. The policy raises mineral/energy, pop, and empire-size targets only when recovery and short-runway deficit gates are clear, then pushes labs/habitat science with copied source objects and Director-owned coefficients.",
            "",
            "## NSC3/ESC Design Policy",
            "",
            "NSC3 and ESC unlock usage now has direct technology AI-weight overrides plus fleet-throughput economy pressure. ESC internal component-template `key = ...` entries and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.",
            "",
            "## Threat-Response Policy",
            "",
            "The V1 threat-response feature adds observer opinion, timed flags, and a capped third-party defensive-readiness economy subplan for classified observed aggression. `wg_conquest`, `wg_subjugation`, and `wg_humiliation` are the initial allowlist; unknown war goals stay inert until evidence, severity, output expectations, tests, and validator coverage are added. The generated event path must not declare wars, join wars, add casus belli, force `wg_*` dispatch, or override diplomatic actions.",
            "",
            "`source_has_ai_weight` records whether the parent mod file had an upstream AI weight. It does not mean the Director has no policy. Director policy is recorded separately as `director_strategy_role`, `director_weight_basis`, `director_build_gate`, `director_surplus_sink_role`, and `director_surplus_sink_priority` in the ROI matrix.",
            "",
            "## v1 Boundaries",
            "",
            "- Direct technology/AP/tradition object overrides are emitted from copied source objects for the supported high-scale route families.",
            "- Direct Mega Shipyard, economy megastructure, planetcraft, war moon, and systemcraft object weights are emitted from copied source objects and paired with economy/reserve gates.",
            "- Direct starbase support includes copied ESC starbase reactor AI weight plus country-level static-defense economy targets.",
            "- Direct research infrastructure overrides are emitted for copied Stellar AI research labs and the habitat science district; broad job automation and generic planet-building rewrites remain deferred.",
            "- ESC internal component-template `key = ...` overrides and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.",
            "- Exotic Gigas superprojects remain outside the main decision path until the core reserve/commit/payoff loop is observer-tested, but their special-resource budget objects are gated by Director survival/recovery state.",
        ]
    )
    return "\n".join(lines) + "\n"


def load_order_note_text(playset: dict[str, Any]) -> str:
    required = list(playset["required_mods"].values())
    latest_parent = max((info["load_position"] or 0) for info in required)
    lines = [
        "# Stellar AI Director Load Order",
        "",
        f"Selected collection: {playset['collection_name']}",
        f"Required parent maximum load position: {latest_parent}",
        "",
        "## Required Position",
        "",
        "- Load after Stellar AI.",
        "- Load after Gigastructural Engineering & More (4.4).",
        "- Load after NSC3.",
        "- Load after Extra Ship Components NEXT.",
        "- Load after Starbase Extended 3.0.",
        "- Load after !!!Universal Resource Patch [2.4+].",
        "- Load after parent compatibility patches whose AI/economy behavior the Director intentionally coordinates.",
        "- Load before any future local patch that intentionally overrides the Director.",
        "",
        "## Required Parent Evidence",
        "",
        "| mod | present | load position |",
        "| --- | --- | ---: |",
    ]
    for info in required:
        lines.append(f"| {info['name']} | {info['present']} | {info['load_position']} |")
    lines.extend(
        [
            "",
        "## Current Intentional Supersession",
            "",
            "- `common/ai_budget/zzz_staid_alloys_budget.txt` intentionally overrides Stellar AI's `alloys_expenditure_megastructures` budget.",
            "- `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` intentionally overrides Gigas `sentient_metal_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, and `supertensiles_upkeep_megastructures` budgets.",
            "- `common/economic_plans/zzzz_staid_additive_economic_plan.txt` intentionally replaces `basic_economy_plan` with Director high-scale survival economy, mandatory modded unlock research, trade-capacity, fleet-throughput, static-defense, and planetary-capacity targets.",
            "- Additive scripted triggers, script values, and economic-plan subplans use the `staid_` namespace and should not conflict with parent object IDs.",
        ]
    )
    return "\n".join(lines) + "\n"


def conflicts_note_text() -> str:
    return """# Stellar AI Director Conflict Notes

## Intentional Conflicts

- `common/ai_budget/zzz_staid_alloys_budget.txt` intentionally replaces the upstream `alloys_expenditure_megastructures` object so late-game megastructure reserves obey Director survival, recovery, prep, and commit gates.
- `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` intentionally replaces upstream Gigas special-resource megastructure budget objects: `sentient_metal_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, and `supertensiles_upkeep_megastructures`.
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt` intentionally replaces `basic_economy_plan` with Director high-scale survival economy, mandatory modded unlock research, trade-capacity, fleet-throughput, static-defense, and planetary-capacity targets; despite the historical filename, conflict review must treat it as a Director-owned economic-plan surface.
- `common/technology/zzzz_staid_01_unlock_technology_technology.txt` intentionally replaces copied vanilla/Gigas/NSC3/ESC/Starbase Extended technology objects with Director route AI weights.
- `common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt` and `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` intentionally replace copied AP/tradition objects with Director route AI weights.
- `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` intentionally replaces copied Gigas/vanilla-compatible megastructure starts for economy multipliers, Mega Shipyard, planetcraft, war moon, and systemcraft priority.
- `common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt` intentionally replaces copied ESC starbase reactor support with Director crisis-starbase pressure.
- `common/buildings/zzzz_staid_06_research_infrastructure_buildings.txt` intentionally replaces copied Stellar AI research lab, institute, supercomputer, and archaeostudies objects with Director research-throughput construction coefficients while preserving parent rare-resource guards.
- `common/districts/zzzz_staid_06_research_infrastructure_districts.txt` intentionally replaces copied vanilla `district_hab_science` with Director crowded-tall habitat research construction weight.

## Expected Additive Surfaces

- `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`
- `common/script_values/zzz_staid_roi_values.txt`
- `common/scripted_triggers/zzz_staid_threat_response_triggers.txt`
- `common/script_values/zzz_staid_threat_response_values.txt`
- `common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt`
- `events/zzz_staid_market_and_fleet_safety_events.txt`
- `common/opinion_modifiers/zzz_staid_threat_response_opinions.txt`
- `common/on_actions/zzz_staid_threat_response_on_actions.txt`
- `events/zzz_staid_threat_response_events.txt`
- `localisation/english/staid_threat_response_l_english.yml`

## Threat-Response Boundaries

- V1 threat response is diplomacy/readiness pressure only.
- Unknown or unclassified war goals are inert until manually classified and tested.
- Generated threat-response files must not declare wars, join wars, add casus belli, or override diplomatic actions.
- Third-party readiness economy pressure must remain behind `staid_tr_foreign_affairs_safe`.

## NSC3/ESC Design Policy

- NSC3 and ESC unlock technologies now have copied source-object route AI weights.
- Fleet-throughput economy gates provide the current ship-use path without guessing direct ship-design templates.
- ESC internal component-template `key = ...` overrides and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.

## Review Rules

- Any new full-object override must include an ownership note naming the parent surface and reason.
- Optional-mod references must be omitted or guarded unless the generator proves the referenced object exists.
- Irony conflict results should be classified as intentional Director wins, parent wins required, harmless additive duplicates, unexpected gameplay conflicts, or false positives.

## Irony Analyze Only Review

- Reviewed in Irony Conflict Solver Analyze Only for collection `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`.
- Existing collection order was preserved; `Stellar AI Director` is the only added local mod and is last after `!!!Universal Resource Patch [2.4+]`.
- Reviewed `common\\ai_budget` conflicts: `alloys_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, `sentient_metal_expenditure_megastructures`, and `supertensiles_upkeep_megastructures`.
- Each reviewed object resolves to `Stellar AI Director ... (LIOS)` as an intentional Director win.
- No unexplained Director gameplay conflicts were observed in the reviewed Director conflict set.
"""


def observer_test_log_text(playset: dict[str, Any]) -> str:
    if OBSERVER_SMOKE_SAVE_SUMMARY_JSON.exists():
        summary = json.loads(read_text(OBSERVER_SMOKE_SAVE_SUMMARY_JSON))
        setup = f"""- Galaxy size: Tiny Irony-launched smoke save.
- AI count: inferred from save country count ({summary['initialized_country_count']} initialized countries).
- Difficulty: Cadet smoke setup from launch run notes.
- Crisis settings: inherited selected playset defaults for the smoke save.
- Mod order evidence: required parents are recorded in `notes/load-order.md`; save mod list contains {summary['mod_count']} mods."""
        checkpoints = f"""- Early economy stability: short-smoke pass from `{OBSERVER_SMOKE_SAVE_SUMMARY_MD.name}`.
- First mega-engineering unlock: pending.
- First high-ROI megastructure start: pending.
- First economy multiplier completion: pending.
- Shipyard/fleet payoff behavior: pending.
- Deficit spiral check: no early deficit collapse observed in parsed 2202.01.01 save metrics.
- War interruption behavior: pending.
- Starbase defense investment: pending."""
        threat_response = """- Classified aggressive war deterministic contract: covered by generated tests and validator.
- Threat-response generated files emitted after 2026-07-05 implementation: covered by file audit and validator.
- Unknown/modded war goal inertness: covered by classification data, tests, and validator.
- No forced wars, join-war behavior, or punitive CBs: covered by forbidden-effect tests and validator.
- Runtime launch observation: intentionally out of scope for this deterministic implementation goal."""
        results = f"""Short Irony-launched save summary: `{OBSERVER_SMOKE_SAVE_SUMMARY_MD.name}`.

- Save date: {summary['date']}.
- Director listed in save mod list: {summary['required_mods_present'].get('Stellar AI Director')}.
- Short smoke passes: {summary['short_smoke_passes']}.
- Player metrics: `{json.dumps(summary['player_metrics'], sort_keys=True)}`.
- Player monthly income: `{json.dumps(summary['player_monthly_income'], sort_keys=True)}`.
- High-ROI path observed: {summary['high_roi_path_observed']}.

This short-smoke evidence is retained as historical context. P15 runtime/observer validation is superseded for this deterministic implementation goal; generated artifacts, tests, validators, and indexed evidence are the acceptance gate."""
    else:
        setup = """- Galaxy size: not run yet.
- AI count: not run yet.
- Difficulty: not run yet.
- Crisis settings: not run yet.
- Mod order evidence: required parents are recorded in `notes/load-order.md`."""
        checkpoints = """- Early economy stability: pending.
- First mega-engineering unlock: pending.
- First high-ROI megastructure start: pending.
- First economy multiplier completion: pending.
- Shipyard/fleet payoff behavior: pending.
- Deficit spiral check: pending.
- War interruption behavior: pending.
- Starbase defense investment: pending."""
        threat_response = """- Classified aggressive war observed: pending.
- Threat-response generated files loaded after 2026-07-05 implementation: pending.
- Unknown/modded war goal inertness observed at runtime: pending.
- No forced wars, join-war behavior, or punitive CBs observed from threat response: pending.
- No threat-response missing localization or repeated event spam in fresh logs: pending."""
        results = "No observer run has been recorded yet in this file."
    return f"""# Stellar AI Director Observer Test Log

Selected collection: {playset['collection_name']}

## Repeatable Setup

{setup}

## Checkpoints

{checkpoints}

## Threat-Response Checkpoints

{threat_response}

## Results

{results}
"""


def tuning_notes_text(thresholds: dict[str, int]) -> str:
    lines = [
        "# Stellar AI Director Tuning Notes",
        "",
        "Generated thresholds are derived from decision-eligible, resolved ROI rows.",
        "",
        "| knob | current value | intent |",
        "| --- | ---: | --- |",
        f"| prep stockpile alloys | {thresholds['prep_stockpile_alloys']} | minimum reserve before new megastructure prep |",
        f"| prep income alloys | {thresholds['prep_income_alloys']} | minimum monthly alloy income for prep |",
        f"| commit stockpile alloys | {thresholds['commit_stockpile_alloys']} | reserve for continuing safe projects |",
        f"| shipyard stockpile alloys | {thresholds['shipyard_stockpile_alloys']} | reserve before shipyard payoff exploitation |",
        f"| shipyard income alloys | {thresholds['shipyard_income_alloys']} | monthly alloy floor for fleet-production sink |",
        "| fleet buildup stockpile energy | 8000 | energy runway before shipyard/fleet sink can add naval-cap pressure |",
        "| trade capacity income floor | 25 | minimum monthly trade before generic expansion gates are considered safe |",
        "| fleet trade capacity income floor | 75 | minimum monthly trade before fleet-throughput and payoff gates add logistics pressure |",
        "| planetary trade capacity income floor | 50 | minimum monthly trade before planetary-capacity and megastructure-prep gates add logistics pressure |",
        "| surplus trade capacity income floor | 100 | minimum monthly trade before surplus sink pressure can activate |",
        "| fleet buildup naval cap ceiling | 1.05 | stop pushing fleet payoff when naval usage is already above target |",
        "| static-defense stockpile alloys | 3000 | minimum reserve before country-level starbase defense economy target |",
        "| static-defense income alloys | 60 | monthly alloy floor for defensive starbase reserve |",
        "| crisis starbase threat | 50 | threat floor that can activate crisis starbase reserve |",
        "| planetary-capacity stockpile minerals | 5000 | mineral runway before expanded planet/building capacity target activates |",
        "| planetary-capacity stockpile energy | 5000 | energy runway before expanded planet/building capacity target activates |",
        "| planetary-capacity pops target | 400000 | high-scale pop target used by the country-level tall-growth capacity subplan |",
        "| market cap-breaker minerals reserve | 50000 | sell large positive-income mineral overflow before caps void income |",
        "| market cap-breaker food/consumer goods reserve | 30000 | sell large positive-income food/CG overflow while preserving large buffers |",
        "| market cap-breaker strategic reserve | 800-2500 | sell marketable strategic overflow only above high reserves |",
        "| stranded fleet warning duration | 70 days | require a second monthly proof before forcing vanilla MIA return-home |",
        f"| threat response relation flag days | {THREAT_RELATION_FLAG_DAYS} | duration for observer/aggressor and observer/victim threat state |",
        f"| threat response economy ratio cap | {int(THREAT_ECONOMY_RATIO_CAP * 100)} | maximum share of fleet-throughput reserve available to third-party threat readiness |",
        f"| threat readiness alloys cap | {THREAT_ECONOMY_MAX['alloys']} | maximum added alloys target from third-party threat readiness |",
        f"| threat readiness energy cap | {THREAT_ECONOMY_MAX['energy']} | maximum added energy target from third-party threat readiness |",
        f"| threat readiness naval cap | {THREAT_ECONOMY_MAX['naval_cap']} | maximum added naval-cap target from third-party threat readiness |",
        f"| eligible ROI rows | {thresholds['eligible_roi_rows']} | source sample used for threshold generation |",
        "",
        "## Static-Defense Policy",
        "",
        "- Defensive or high-threat empires get additive starbase reserve subplans only after recovery and short-runway deficit gates are clear.",
        "- Aggressive under-cap empires keep fleet expansion priority unless crisis pressure is high.",
        "- The generated ESC starbase reactor override adds direct crisis-starbase AI weight support; other starbase modules/buildings remain manual-review candidates.",
        "",
        "## Trade-Capacity Policy",
        "",
        "- Trade is modeled as Stellaris 4.4 logistics/capacity headroom, not as a normal priced ROI resource.",
        "- The generated `basic_economy_plan` includes trade reserve and trade recovery subplans so the Director's full-object replacement keeps trade logistics visible while pushing beyond vanilla/Stellar AI scale.",
        "- Fleet, planetary, megastructure, static-defense, and surplus gates require trade income floors before adding more ship, colony, or resource-imbalance upkeep pressure.",
        "",
        "## Market Cap-Breaker Policy",
        "",
        "- Capped stockpile waste is treated as an economic emergency, not harmless savings.",
        "- The monthly cap breaker sells only large positive-income overflow for marketable resources with verified market pricing or parent market-value support.",
        "- Alloys, energy, unity, Gigas negative mass, and Gigas megaconstruction are excluded from forced sale because they are strategic reserves or not safely market-priced in source files.",
        "",
        "## Fleet-Throughput Policy",
        "",
        "- Mega Shipyard readiness becomes an economic-plan subplan only when alloy income, energy income, trade income, alloy stockpile, and energy stockpile are all safe.",
        "- Fleet payoff exploitation is blocked while over-naval-cap upkeep spirals are likely (`used_naval_capacity_percent >= 1.05`).",
        "- Research sink remains first when the Mega Shipyard unlock is missing because `staid_shipyard_expansion_ready` requires `tech_mega_shipyard`.",
        "",
        "## Unlock-Research Policy",
        "",
        "- The unlock-research policy is mandatory survival pressure after the opening curve, not a surplus-only luxury; it keeps physics, society, engineering, and unity pressure on until core Mega Engineering, Mega Shipyard, Gigas, NSC3, and ESC unlock paths are reachable.",
        "- Direct technology/AP/tradition route overrides are emitted from copied source objects and trace back to the policy matrix and route override report.",
        "",
        "## Mega/Giga Build Priority Policy",
        "",
        "- ROI-ready megastructure and gigastructure rows are mapped through generated alloy, special-resource, and economy-plan gates.",
        "- Generated full-object route overrides now cover Dyson Sphere, Mega Shipyard, neutronium gigaforge, Nidavellir forge, Matrioshka brain, planetcraft printer, war moon, and systemcraft starts; generated files preserve parent `@variable` parse context and remove absent optional `pc_magnetar` compatibility references.",
        "- Exotic projects outside those route starts remain inventoried until the core loop is observer-tested against the high-scale crisis benchmark.",
        "",
        "## Planetary-Capacity Policy",
        "",
        "- Expanded planet/building capacity is covered through a country-level economic-plan subplan once mineral, energy, and trade logistics runway are safe.",
        "- The generated subplan uses supported `pops` and income targets only; do not emit `empire_size`, which Stellaris 4.4.4 rejects in active economic-plan files.",
        "- Direct research infrastructure overrides now cover copied Stellar AI research labs and the habitat science district; broad job automation rewrites remain a required follow-up when a specific missing parent surface is proven.",
        "",
        "## NSC3/ESC Design Policy",
        "",
        "- NSC3 and ESC unlock technologies now have copied source-object route AI weights and are paired with fleet-throughput economy gates.",
        "- ESC internal component-template `key = ...` overrides and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.",
        "",
        "## Threat-Response Policy",
        "",
        "- V1 reacts only to explicitly classified war goals: `wg_conquest`, `wg_subjugation`, and `wg_humiliation`.",
        "- Unknown or unclassified war goals are inert: no punitive opinion, no shared-threat opinion, no alignment opinion, no readiness flag, no economy pressure, no CB, and no forced war.",
        "- Design axes such as moral outrage and regional fear remain generator-owned; runtime files consume only generated values, triggers, flags, events, and opinion modifiers.",
        "- Third-party defensive-readiness economy pressure is gated by `staid_tr_foreign_affairs_safe`, requires no survival/recovery/deficit/war state, and is capped at 20% of the existing fleet-throughput reserve.",
        "- Directly attacked empires remain owned by vanilla/Stellar AI/Director war and survival behavior, not the third-party threat economy path.",
        "",
        "## Stranded-Fleet Recovery Policy",
        "",
        "- The Director does not attempt normal movement/pathfinding orders from script.",
        "- Idle, out-of-combat, MIA-eligible AI fleets outside their owner's space are marked only while `staid_homeland_under_attack` is true.",
        "- A marked fleet must still satisfy the same stranded gate on a later monthly pulse before `set_mia = mia_return_home` fires.",
        "- The gate is intended for post-war access/pocket failures where a strong fleet is trapped away from a collapsing homeland, not for active offensive fleets.",
        "",
        "## Safe Tuning Rules",
        "",
        "- Do not lower prep or commit reserves below survival/recovery safety gates.",
        "- Keep research sink before fleet sink until core modded unlocks are available.",
        "- Treat unpriced resources and trade logistics as bottlenecks, not fake scalar value.",
        "- Re-run generator, validator, unit tests, and coverage after every tuning change.",
    ]
    return "\n".join(lines) + "\n"


def validate_generated_patch(snapshot_root: Path = SNAPSHOT_ROOT) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_object_atlas_artifacts())
    for row in collect_generated_file_audit_rows(MOD_ROOT):
        if row["status"] != "ok":
            errors.append(f"Generated file audit failed for {row['generated_file']}: {row['status']} ({row['reason']})")
    object_names = collect_object_names(snapshot_root)
    generated_files = list((MOD_ROOT / "common").rglob("*.txt"))
    if not generated_files:
        errors.append(f"No generated PDXScript files found under {MOD_ROOT / 'common'}")
        return errors
    for row in collect_generated_reference_rows(MOD_ROOT, snapshot_root):
        if row["status"] == "missing":
            errors.append(
                f"{MOD_ROOT / row['generated_file']}: missing {row['reference_type']} reference {row['reference_name']}"
            )
    for row in generated_unresolved_at_variable_rows(MOD_ROOT):
        errors.append(
            f"{MOD_ROOT / row['generated_file']}:{row['line']}: unresolved source-local variable {row['variable']}"
        )
    for file_path in generated_files:
        try:
            parsed = parse_file(file_path)
        except PDXParseError as exc:
            errors.append(str(exc))
            continue
        top_keys = [assignment.key for assignment in block_assignments(parsed)]
        if file_path.parts[-2] == "ai_budget":
            for key in top_keys:
                if key not in object_names["ai_budget"]:
                    errors.append(f"Generated ai_budget object does not override a known budget: {key}")
    return errors


def run_all() -> None:
    generate_object_atlas_artifacts()
    rows = generate_roi_artifacts()
    generate_mod_files(rows)
    errors = validate_generated_patch()
    if errors:
        raise SystemExit("Validation failed:\n" + "\n".join(errors))
