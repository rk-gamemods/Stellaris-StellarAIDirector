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
import time
import zipfile
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_ROOT = REPO_ROOT / "research" / "mod-source-snapshots" / "2026-07-04"
IRONY_DATA_ROOT = Path(r"C:\Users\Admin\AppData\Roaming\Mario")
STELLARIS_INSTALL_ROOT = Path(r"C:\Steam\steamapps\common\Stellaris")
PLANETARY_DIVERSITY_WORKSHOP_ROOT = Path(r"C:\Steam\steamapps\workshop\content\281990\819148835")
PLANETARY_DIVERSITY_MORE_ARCOLOGIES_WORKSHOP_ROOT = Path(r"C:\Steam\steamapps\workshop\content\281990\1732447147")
STELLARIS_LOG_ROOT = Path(r"C:\Users\Admin\Documents\Paradox Interactive\Stellaris\logs")
STELLARIS_SAVE_ROOT = Path(r"C:\Users\Admin\Documents\Paradox Interactive\Stellaris\save games")
PARADOX_MOD_ROOT = Path(r"C:\Users\Admin\Documents\Paradox Interactive\Stellaris\mod")
DLC_LOAD_PATH = Path(r"C:\Users\Admin\Documents\Paradox Interactive\Stellaris\dlc_load.json")
MOD_ROOT = REPO_ROOT / "mods" / "StellarAIDirector"
RESEARCH_ROOT = REPO_ROOT / "research" / "stellar-ai"
DECISION_STATE_TRIGGER_PATH = (
    MOD_ROOT / "common" / "scripted_triggers" / "zzz_staid_decision_state_triggers.txt"
)
OUTPOST_BUDGET_PATH = MOD_ROOT / "common" / "ai_budget" / "zzz_staid_outpost_budgets.txt"
IDENTITY_DIPLOMATIC_STANCE_PATH = (
    MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt"
)
CORE_AI_ARTIFACT_PATHS = (
    DECISION_STATE_TRIGGER_PATH,
    OUTPOST_BUDGET_PATH,
)
FLEET_ALLOY_BUDGET_PATH = MOD_ROOT / "common" / "ai_budget" / "zzz_staid_alloys_budget.txt"
TECHNOLOGY_ROUTE_OVERRIDE_PATH = (
    MOD_ROOT
    / "common"
    / "technology"
    / "zzzz_staid_01_unlock_technology_technology.txt"
)
IDENTITY_STRATEGY_ROUTE_OVERRIDE_PATHS = (
    MOD_ROOT / "common" / "ascension_perks" / "zzzz_staid_02_perks_traditions_ascension_perks.txt",
    MOD_ROOT / "common" / "tradition_categories" / "zzzz_staid_02_perks_traditions_tradition_categories.txt",
    MOD_ROOT / "common" / "traditions" / "zzzz_staid_02_perks_traditions_traditions.txt",
)
IDENTITY_CLAIM_BUDGET_PATH = (
    MOD_ROOT
    / "common"
    / "ai_budget"
    / "zzzz_staid_08_site_limited_expansion_ai_budget.txt"
)
IDENTITY_STATIC_DEFENSE_PATHS = (
    MOD_ROOT
    / "common"
    / "starbase_buildings"
    / "zzzz_staid_05_starbase_defense_starbase_buildings.txt",
    MOD_ROOT
    / "common"
    / "starbase_modules"
    / "zzzz_staid_05_starbase_defense_starbase_modules.txt",
)
IDENTITY_MEGASTRUCTURE_PATH = (
    MOD_ROOT
    / "common"
    / "megastructures"
    / "zzzz_staid_03_megastructures_megastructures.txt"
)
IDENTITY_SUBJECT_AGREEMENT_ROOT = MOD_ROOT / "common" / "agreement_presets"
IDENTITY_SUBJECT_AGREEMENT_SOURCES = {
    "00_agreement_presets.txt": (
        "zzzz_staid_23_identity_specialist_base_agreement_presets.txt",
        {
            "preset_bulwark": "0958a6f04355d5c32ea68bb97a4ad89816270f8f8a058db0340fcbb49d5d3bfb",
            "preset_scholarium": "1b5eee6266eb96226a03cad74042e92b10165f2658bd78adf0daa3aa81263a0c",
            "preset_prospectorium": "a81b35bd053f09c125848516180787cdae78bd3651cf0ce157e7466cecdaf24b",
        },
    ),
    "02_agreement_presets_ai_bulwark.txt": (
        "zzzz_staid_23_identity_specialist_bulwark_ai.txt",
        {
            "preset_bulwark_nice_01": "1d0b371bb1bd30b2f96abd800f20ee93478ddddb2c7d1515e2505d6c65d5e8d8",
            "preset_bulwark_nice_02": "0c77b708c62d3af775b58ebd37a0998fe596e7ac6256da7747ce3379fb465eb7",
            "preset_bulwark_mean_01": "588839aff76c70955799198d03ecb22ff52317782dca3b895c472f7b94d76415",
            "preset_bulwark_mean_02": "cb6711171c8be8dbb304904e5ea4427ca90c7b2b33e0b5128227c4a4d6881df7",
            "preset_bulwark_mean_03": "11fd354bc74439503f40ea9f6ea0b59afb62e28a284640a64258d20e6fe52514",
        },
    ),
    "03_agreement_presets_ai_scholarium.txt": (
        "zzzz_staid_23_identity_specialist_scholarium_ai.txt",
        {
            "preset_scholarium_nice_01": "3705ad064057624416a7729f3b35aff9ad22617d330a5315e77e277af8596ce2",
            "preset_scholarium_nice_02": "6e2eaa16149ee0e9421d5111476a4480f5aa0ffe8d9921a74a0ee49333f2c386",
            "preset_scholarium_mean_01": "cc2d654cbb0a52568c16e34a9c4381282a73348c40786d0f53d0dc536ff365e8",
            "preset_scholarium_mean_02": "42ba1d99e36527cecfd8d51bc81c3168e4cc2f4242753aa750f6ce868a32e23b",
            "preset_scholarium_mean_03": "3c21728ae6fc286e6bab525a6981d0032bc8c1ed4be1131722b11868e99ba4dc",
        },
    ),
    "04_agreement_presets_ai_prospectorium.txt": (
        "zzzz_staid_23_identity_specialist_prospectorium_ai.txt",
        {
            "preset_prospectorium_nice_01": "da8880302f020094aebdc79a3a4977b718a0c9e41f74927b818ed5c1652121f9",
            "preset_prospectorium_nice_02": "e89785b22c6988a73a92ef66598a83306ba26aa15c7fcbc91b02c10425bb39e5",
            "preset_prospectorium_mean_01": "0267cfe4af58ada713378e9090d95aa48e541b81c417a4405e4fa3725aadbca4",
            "preset_prospectorium_mean_02": "b1aa1b7f04c7f7fe264fb52dd72ee1d0f301b3338d5fe7e6b7bb9d256ff84ea6",
            "preset_prospectorium_mean_03": "d07a8ffafaaeee98443152fa380615dc8c9831aba009217ad1b8d74edbb8d24d",
        },
    ),
}
ARCHETYPE_OVERLAY_ARTIFACT_PATHS = (
    FLEET_ALLOY_BUDGET_PATH,
    TECHNOLOGY_ROUTE_OVERRIDE_PATH,
    *IDENTITY_STRATEGY_ROUTE_OVERRIDE_PATHS,
    IDENTITY_CLAIM_BUDGET_PATH,
    *IDENTITY_STATIC_DEFENSE_PATHS,
    IDENTITY_MEGASTRUCTURE_PATH,
)
FLEET_ARCHETYPE_FACTORS = {
    "extermination": 1.12,
    "conquest": 1.08,
}
FLEET_THREAT_RESPONSE_FACTOR = 1.10
TECHNOLOGY_ARCHETYPE_ROUTE_FACTORS = {
    "research": {
        "research_megastructure_core": 1.15,
        "science_kilo_snowball_core": 1.15,
        "planetary_computer_research_core": 1.15,
    },
    "diplomatic": {
        "research_megastructure_core": 1.05,
        "science_kilo_snowball_core": 1.05,
        "planetary_computer_research_core": 1.05,
    },
    "gestalt_growth": {
        "pop_assembly_snowball_core": 1.08,
        "ring_world_growth_core": 1.08,
    },
    "defensive": {
        "fallen_empire_benchmark_route": 1.08,
    },
    "conquest": {
        "mega_shipyard_core": 1.08,
        "war_moon_route": 1.08,
        "systemcraft_route": 1.08,
        "nsc3_capital_hull_route": 1.08,
        "esc_component_route": 1.08,
    },
    "extermination": {
        "mega_shipyard_core": 1.12,
        "war_moon_route": 1.12,
        "systemcraft_route": 1.12,
        "nsc3_capital_hull_route": 1.12,
        "esc_component_route": 1.12,
    },
}
TECHNOLOGY_ARCHETYPE_EXCLUDED_OBJECTS = {
    # Source draw weight is zero or an event-only factor-zero gate makes the
    # technology inert. ai_weight cannot put these objects into the draw pool.
    "giga_tech_lunar_assembly",
    "giga_tech_war_system_1",
    "tech_ring_world",
    "esc_tech_dreadnought_computer",
}
IDENTITY_STRATEGY_PRIMARY_FACTORS = {
    "research": {
        "ap_technological_ascendancy": 1.15,
        "tradition_discovery": 1.15,
        "tr_discovery_to_boldly_go": 1.15,
        "tr_discovery_databank_uplinks": 1.15,
        "tr_discovery_science_division": 1.15,
        "tr_discovery_polytechnic_education": 1.15,
        "tr_discovery_faith_in_science": 1.15,
    },
    "diplomatic": {
        "tradition_diplomacy": 1.15,
        "tr_diplomacy_the_federation": 1.15,
        "tr_diplomacy_entente_coordination": 1.15,
        "tr_diplomacy_diplomatic_networking": 1.15,
        "tr_diplomacy_direct_diplomacy": 1.15,
        "tr_diplomacy_eminent_diplomats": 1.15,
    },
    "defensive": {"tradition_adaptability": 1.08},
    "conquest": {"ap_lord_of_war": 1.08, "tradition_supremacy": 1.08},
    "extermination": {"ap_lord_of_war": 1.12, "tradition_supremacy": 1.12},
}
IDENTITY_STRATEGY_DEFINING_FACTORS = {
    "staid_identity_megacorp": {"tradition_mercantile": 1.15},
    "staid_identity_inward_perfection": {"tradition_adaptability": 1.12},
    "staid_identity_barbaric_despoiler": {"tradition_supremacy": 1.12},
    "staid_identity_rogue_servitor": {"tradition_diplomacy": 1.08},
    "staid_identity_assimilator": {"tradition_supremacy": 1.10},
}
STRATEGIC_RESOURCE_DEFICIT_RECOVERY_PATH = (
    MOD_ROOT / "common" / "economic_plans" / "zzzz_staid_21_strategic_resource_deficit_recovery.txt"
)
ORDINARY_STRATEGIC_RESOURCE_RECOVERY = (
    ("volatile_motes", "volatile motes"),
    ("exotic_gases", "exotic gases"),
    ("rare_crystals", "rare crystals"),
)
DIRECTOR_DLC_LOAD_ENTRY = "mod/StellarAIDirector.mod"
BASELINE_ERROR_LOG = RESEARCH_ROOT / "baseline-without-director-error-2026-07-04.log"
BASELINE_GAME_LOG = RESEARCH_ROOT / "baseline-without-director-game-2026-07-04.log"
WITH_DIRECTOR_ERROR_LOG = RESEARCH_ROOT / "with-director-error-2026-07-04.log"
WITH_DIRECTOR_GAME_LOG = RESEARCH_ROOT / "with-director-game-2026-07-04.log"
MAIN_MENU_PROOF_PATH = RESEARCH_ROOT / "stellar-ai-director-main-menu-proof-2026-07-04.json"
MAIN_MENU_CONFIRMATION_ENV = "STELLAR_AI_DIRECTOR_MAIN_MENU_CONFIRMED"
LAUNCH_SURFACE_ENV = "STELLAR_AI_DIRECTOR_LAUNCH_SURFACE"
MAIN_MENU_REQUIRED_MODES = ("baseline_without_director", "with_director")
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
GENERATED_VERSION_INVENTORY_MD = RESEARCH_ROOT / "STAID_GENERATED_VERSION_INVENTORY.md"
MOD_STACK_COMPATIBILITY_MD = RESEARCH_ROOT / "STAID_MOD_STACK_COMPATIBILITY.md"
MANUAL_STATIC_VALIDATION_MD = RESEARCH_ROOT / "STAID_MANUAL_STATIC_VALIDATION.md"
STANDALONE_PARITY_INVENTORY_CSV = RESEARCH_ROOT / "stellar-ai-director-standalone-parity-inventory-2026-07-08.csv"
STANDALONE_PARITY_INVENTORY_MD = RESEARCH_ROOT / "stellar-ai-director-standalone-parity-inventory-2026-07-08.md"
STRATEGIC_SUBSYSTEM_AUDIT_CSV = RESEARCH_ROOT / "stellar-ai-director-strategic-subsystem-audit-2026-07-09.csv"
STRATEGIC_SUBSYSTEM_AUDIT_MD = RESEARCH_ROOT / "stellar-ai-director-strategic-subsystem-audit-2026-07-09.md"
RELATIVE_ECONOMIC_STANDARDS_CSV = RESEARCH_ROOT / "stellar-ai-director-relative-economic-standards-2026-07-09.csv"
RELATIVE_ECONOMIC_STANDARDS_MD = RESEARCH_ROOT / "stellar-ai-director-relative-economic-standards-2026-07-09.md"
SFT_EQUIVALENCE_AUDIT_CSV = RESEARCH_ROOT / "stellar-ai-director-sft-equivalence-audit-2026-07-09.csv"
SFT_EQUIVALENCE_AUDIT_MD = RESEARCH_ROOT / "stellar-ai-director-sft-equivalence-audit-2026-07-09.md"
ECONOMIC_VALUATION_DATASET_CSV = RESEARCH_ROOT / "stellar-ai-director-economic-valuation-2026-07-07.csv"
ECONOMIC_VALUATION_DATASET_MD = RESEARCH_ROOT / "stellar-ai-director-economic-valuation-2026-07-07.md"
NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV = (
    RESEARCH_ROOT / "stellar-ai-director-nonconstruction-economic-valuation-2026-07-07.csv"
)
NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_MD = (
    RESEARCH_ROOT / "stellar-ai-director-nonconstruction-economic-valuation-2026-07-07.md"
)
ECONOMIC_VALUATION_EVIDENCE_MD = RESEARCH_ROOT / "stellar-ai-director-economic-valuation-evidence-2026-07-07.md"
BUILD_PLAN_CONSUMER_POLICY_CSV = RESEARCH_ROOT / "stellar-ai-director-build-plan-consumer-policy-2026-07-09.csv"
WAR_PLANNING_444_PROVENANCE_CSV = RESEARCH_ROOT / "stellar-ai-director-war-planning-444-provenance-2026-07-10.csv"
OBJECT_ATLAS_COVERAGE_MD = OBJECT_ATLAS_ROOT / "coverage-report-2026-07-06.md"
ROUTE_REPORT_MD = OBJECT_ATLAS_ROOT / "route-reports-2026-07-06.md"

REQUIRED_MODS = {
    "1121692237": "Gigastructural Engineering & More (4.4)",
    "683230077": "NSC3",
    "2648658105": "Extra Ship Components NEXT",
    "3250900527": "Starbase Extended 3.0",
}

PARITY_REFERENCE_MODS = {
    "3610149307": "Stellar AI",
    "3696204283": "Spacefleet Tactica",
}

# Stellar AI 0.10 (4.4.4) supplied these personality-side aggression values.
# Stellar AI Director remains runtime-standalone: generated overrides copy the
# current vanilla personality bodies and change only this scalar.
STANDALONE_AGGRESSION_PERSONALITY_VALUES = {
    "honorbound_warriors": 4.0,
    "evangelising_zealots": 3.0,
    "erudite_explorers": 1.8,
    "spiritual_seekers": 0.5,
    "ruthless_capitalists": 3.0,
    "hegemonic_imperialists": 2.5,
    "slaving_despots": 2.5,
    "democratic_crusaders": 3.0,
    "harmonious_hierarchy": 1.8,
    "federation_builders": 1.8,
    "fanatic_purifiers": 4.5,
    "hive_mind": 3.0,
    "devouring_swarm": 4.5,
    "migrating_flock": 0.5,
    "machine_intelligence": 3.0,
    "assimilators": 3.0,
    "exterminators": 4.5,
    "servitors": 2.5,
    "fanatic_befrienders": 4.5,
    "became_the_crisis": 4.5,
}

ATLAS_SOURCE_MODS = {
    **REQUIRED_MODS,
    **PARITY_REFERENCE_MODS,
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

DIRECTOR_CAMPAIGN_START_YEAR = 2200
DIRECTOR_ENDGAME_VALUE_HORIZON_YEAR = 2350
LONG_TERM_VALUE_BANDS = (
    (None, 30, 15),
    (30, 60, 45),
    (60, 100, 80),
    (100, 150, 125),
)

ROUTE_LONG_TERM_VALUE_PROFILES = {
    "mega_engineering_core": (900.0, 25000.0, 0.0),
    "mega_shipyard_core": (700.0, 20000.0, 15.0),
    "economy_megastructure_core": (1000.0, 30000.0, 20.0),
    "early_kilo_economy_core": (260.0, 6000.0, 10.0),
    "science_kilo_snowball_core": (320.0, 7000.0, 10.0),
    "research_megastructure_core": (850.0, 25000.0, 15.0),
    "planetary_computer_research_core": (1200.0, 30000.0, 25.0),
    "pop_assembly_snowball_core": (75.0, 1200.0, 8.0),
    "ring_world_growth_core": (900.0, 25000.0, 20.0),
    "storage_cap_core": (0.0, 6000.0, 25.0),
    "gigas_special_resource_core": (400.0, 12000.0, 10.0),
    "research_throughput_infrastructure": (75.0, 900.0, 6.0),
    "planetcraft_route": (2200.0, 60000.0, 60.0),
    "war_moon_route": (1300.0, 45000.0, 45.0),
    "systemcraft_route": (3000.0, 90000.0, 90.0),
    "nsc3_capital_hull_route": (500.0, 12000.0, 25.0),
    "esc_component_route": (450.0, 10000.0, 20.0),
    "crowded_tall_route": (160.0, 3000.0, 8.0),
    "conquest_escape_route": (350.0, 8000.0, 20.0),
    "raiding_pop_acquisition_route": (650.0, 8000.0, 18.0),
    "hostile_space_fauna_clearance_route": (180.0, 2500.0, 5.0),
    "apex_site_preservation_core": (1600.0, 45000.0, 40.0),
    "fallen_empire_benchmark_route": (900.0, 25000.0, 35.0),
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
    "tradition_categories": ("tradition_category", "P6"),
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
    "agreement_presets": "agreement_preset",
    "tradition_categories": "tradition_category",
    "traditions": "tradition",
    "megastructures": "megastructure",
    "buildings": "building",
    "colony_automation_exceptions": "colony_automation_exception",
    "colony_types": "colony_type",
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
    "federation_types": "federation_type",
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
    "early_kilo_economy_core": ("arc_furnace", "asteroid_manufactory", "storm_observatory", "kilostructure"),
    "science_kilo_snowball_core": ("macro_test_site", "atmosphere_shredder", "engineering_test_site", "science_kilo"),
    "research_megastructure_core": ("science_nexus", "think_tank", "research_speed", "research"),
    "planetary_computer_research_core": ("planetary_computer", "pcc_science", "giga_pcc", "computing"),
    "pop_assembly_snowball_core": ("pop_assembly", "robot_assembly", "clone_vats", "spawning_pool", "growth"),
    "ring_world_growth_core": ("ring_world", "segment", "build_surface", "population"),
    "storage_cap_core": ("kugelblitz", "storage", "resource_max", "stockpile"),
    "gigas_special_resource_core": ("sentient_metal", "negative_mass", "megaconstruction", "supertensiles", "dark_matter"),
    "research_throughput_infrastructure": ("research_lab", "research", "institute", "supercomputer", "archaeostudies", "science"),
    "research_diplomacy_core": ("research_federation", "research_agreement", "diplomacy", "technology_sharing"),
    "planetcraft_route": ("planetcraft", "planet_assembly", "planet_behemoth", "celestial_printing"),
    "war_moon_route": ("war_moon", "attack_moon", "lunar"),
    "systemcraft_route": ("systemcraft", "war_system", "planet_behemoth", "celestial_printing"),
    "nsc3_capital_hull_route": ("dreadnought", "carrier", "flagship", "supercapital", "headquarters"),
    "esc_component_route": ("esc_", "dark_matter_power_core", "strikecraft_5", "reactor", "shield"),
    "crowded_tall_route": ("habitat", "orbital", "district", "building", "capacity"),
    "conquest_escape_route": ("claim", "subjugation", "war", "fleet", "naval_cap"),
    "raiding_pop_acquisition_route": ("nihilistic", "raiding", "abduct", "pops", "bombardment"),
    "hostile_space_fauna_clearance_route": ("crystal", "amoeba", "mining_drone", "space_fauna", "leviathan"),
    "apex_site_preservation_core": ("o_star", "matrioshka", "neutronium_gigaforge", "nidavellir", "magnetar"),
    "fallen_empire_benchmark_route": ("fallen", "awakened", "crisis", "systemcraft", "planetcraft"),
}

GENERATED_SURFACE_FOLDERS = {
    "ai_budget": "ai_budget",
    "agreement_presets": "agreement_preset",
    "ascension_perks": "ascension_perk",
    "component_sets": "component_set",
    "component_tags": "component_tag",
    "component_templates": "component_template",
    "country_types": "country_type",
    "bombardment_stances": "bombardment_stance",
    "buildings": "building",
    "colony_automation_exceptions": "colony_automation_exception",
    "colony_types": "colony_type",
    "decisions": "decision",
    "defines": "define",
    "districts": "district",
    "edicts": "edict",
    "economic_plans": "economic_plan",
    "federation_types": "federation_type",
    "game_rules": "game_rule",
    "megastructures": "megastructure",
    "opinion_modifiers": "opinion_modifier",
    "on_actions": "on_action",
    "personalities": "personality",
    "policies": "policy",
    "scripted_effects": "scripted_effect",
    "scripted_modifiers": "scripted_modifier",
    "scripted_triggers": "scripted_trigger",
    "scripted_variables": "scripted_variable",
    "script_values": "scripted_value",
    "ship_behaviors": "ship_behavior",
    "ship_sizes": "ship_size",
    "starbase_buildings": "starbase_building",
    "starbase_modules": "starbase_module",
    "static_modifiers": "static_modifier",
    "technology": "technology",
    "tradition_categories": "tradition_category",
    "traditions": "tradition",
    "zones": "zone",
}
GENERATED_AUXILIARY_COMMON_FOLDERS: set[str] = {"inline_scripts"}

GIGAS_HABITAT_ZONE_SLOT_DISTRICTS = {
    "district_giga_hab_city": ("slot_city_government", "slot_habitat_01", "slot_habitat_02"),
    "district_giga_hab_hive": ("slot_city_government", "slot_habitat_01", "slot_habitat_02"),
    "district_giga_hab_nexus": ("slot_city_government", "slot_habitat_01", "slot_habitat_02"),
    "district_giga_hab_science": ("slot_habitat_research",),
    "district_giga_hab_scavenger": ("slot_habitat_minerals",),
    "district_giga_orbital_farming": ("slot_city_01",),
    "district_giga_orbital_sanctuary": ("slot_city_government", "slot_city_01", "slot_city_02"),
    "district_giga_orbital_preserve": ("slot_city_01",),
    "district_giga_orbital_logistics": ("slot_city_government", "slot_city_01", "slot_city_02"),
}

GIGAS_HABITAT_ZONE_SLOT_SOURCE_FILES = {
    "giga_habitats.txt": (
        "district_giga_hab_city",
        "district_giga_hab_hive",
        "district_giga_hab_nexus",
        "district_giga_hab_science",
        "district_giga_hab_scavenger",
    ),
    "giga_orbital.txt": (
        "district_giga_orbital_farming",
        "district_giga_orbital_sanctuary",
        "district_giga_orbital_preserve",
        "district_giga_orbital_logistics",
    ),
}

PLANETARY_DIVERSITY_OUTPOST_DECISION_SOURCE = "common/decisions/pd_domed_base_decisions.txt"

PLANETARY_DIVERSITY_OUTPOST_DECISION_POLICY = [
    {
        "decision_id": "decision_build_pd_moon_base",
        "role": "moon_network_hub",
        "base_weight": 9000,
        "modifiers": [
            (5, "owner = { staid_planetary_diversity_outpost_investment_ready = yes }"),
            (4, "is_capital = yes"),
            (3, "owner = { staid_planetary_capacity_growth_ready = yes }"),
        ],
    },
    {
        "decision_id": "decision_build_pd_moon_base_moon_colony",
        "role": "moon_colony_network_hub",
        "base_weight": 9000,
        "modifiers": [
            (5, "owner = { staid_planetary_diversity_outpost_investment_ready = yes }"),
            (4, "is_capital = yes"),
            (3, "owner = { staid_planetary_capacity_growth_ready = yes }"),
        ],
    },
    *[
        {
            "decision_id": decision_id,
            "role": "mining_outpost",
            "base_weight": 11000,
            "modifiers": [
                (6, "owner = { staid_planetary_diversity_outpost_investment_ready = yes }"),
                (5, "owner = { has_monthly_income = { resource = minerals value < 250 } }"),
                (3, "owner = { staid_resource_waste_pressure = yes }"),
            ],
        }
        for decision_id in (
            "decision_build_pd_mining_base",
            "decision_build_pd_mining_base_2",
            "decision_build_pd_mining_base_3",
        )
    ],
    *[
        {
            "decision_id": decision_id,
            "role": "food_outpost",
            "base_weight": 10000,
            "modifiers": [
                (0, "owner = { NOT = { country_uses_food = yes } }"),
                (6, "owner = { staid_planetary_diversity_outpost_investment_ready = yes }"),
                (5, "owner = { country_uses_food = yes NOT = { staid_food_runway_safe = yes } }"),
                (3, "owner = { staid_planetary_capacity_growth_ready = yes }"),
            ],
        }
        for decision_id in (
            "decision_build_pd_food_base",
            "decision_build_pd_food_base_2",
            "decision_build_pd_food_base_3",
        )
    ],
    *[
        {
            "decision_id": decision_id,
            "role": "energy_outpost",
            "base_weight": 11000,
            "modifiers": [
                (6, "owner = { staid_planetary_diversity_outpost_investment_ready = yes }"),
                (5, "owner = { has_monthly_income = { resource = energy value < 250 } }"),
                (3, "owner = { staid_planetary_capacity_growth_ready = yes }"),
            ],
        }
        for decision_id in (
            "decision_build_pd_energy_base",
            "decision_build_pd_energy_base_2",
            "decision_build_pd_energy_base_3",
        )
    ],
    *[
        {
            "decision_id": decision_id,
            "role": "capital_research_outpost",
            "base_weight": 15000,
            "modifiers": [
                (8, "owner = { staid_pd_research_outpost_priority_ready = yes }"),
                (7, "is_capital = yes"),
                (5, "owner = { staid_research_under_curve = yes }"),
                (4, "owner = { staid_research_input_runway_safe = yes }"),
                (3, "owner = { staid_planetary_capacity_growth_ready = yes }"),
            ],
        }
        for decision_id in (
            "decision_build_pd_research_base",
            "decision_build_pd_research_base_2",
            "decision_build_pd_research_base_3",
        )
    ],
]

PLANETARY_DIVERSITY_OUTPOST_VALUE_PROFILES = {
    "moon_network_hub": (80.0, 350.0, 0.75),
    "moon_colony_network_hub": (80.0, 350.0, 0.75),
    "mining_outpost": (35.0, 350.0, 0.75),
    "food_outpost": (28.0, 350.0, 0.75),
    "energy_outpost": (25.0, 350.0, 0.75),
    "capital_research_outpost": (90.0, 350.0, 0.75),
}

PD_ECONOMIC_ROLE_KEYWORDS = {
    "research": ("research", "physicist", "biologist", "engineer", "researcher", "calculator", "science"),
    "minerals": ("minerals", "mining", "miner", "mine"),
    "energy": ("energy", "generator", "technician", "grid"),
    "food": ("food", "farming", "farmer", "agriculture"),
    "alloys": ("alloys", "foundry", "metallurgist", "forge"),
    "consumer_goods": ("consumer_goods", "artisan", "factory"),
    "trade": ("trade", "clerk", "merchant"),
    "unity": ("unity", "priest", "bureaucrat", "culture_worker"),
    "growth": ("pop_growth", "pop_assembly", "habitability", "housing", "immigration"),
    "defense": ("stability", "crime", "defense", "army", "orbital_bombardment"),
}

PD_ROLE_VALUE_PROFILES = {
    "research": (90.0, 350.0, 0.75),
    "minerals": (35.0, 350.0, 0.75),
    "energy": (25.0, 350.0, 0.75),
    "food": (28.0, 350.0, 0.75),
    "alloys": (120.0, 500.0, 1.0),
    "consumer_goods": (70.0, 450.0, 1.0),
    "trade": (45.0, 350.0, 0.5),
    "unity": (55.0, 350.0, 0.5),
    "growth": (150.0, 500.0, 1.0),
    "defense": (35.0, 350.0, 0.5),
}

PD_BUILDING_SOURCE_FILES = (
    "pd_buildings_overwrites.txt",
    "pd_gaia_buildings.txt",
    "pd_planetary_infesters_buildings.txt",
    "pd_rare_buildings.txt",
    "pd_uncommon_buildings.txt",
)

RESEARCH_RESOURCES = ("physics_research", "society_research", "engineering_research")
SURPLUS_WASTE_STOCKPILE_THRESHOLDS = {
    "minerals": 25000.0,
    "food": 18000.0,
    "consumer_goods": 18000.0,
    "volatile_motes": 800.0,
    "exotic_gases": 800.0,
    "rare_crystals": 800.0,
    "sr_dark_matter": 1000.0,
    "sr_zro": 1000.0,
    "nanites": 1000.0,
    "giga_sr_sentient_metal": 2500.0,
}

# Cap-based sales require both a finite resource maximum and market tradability.
# Stellaris 4.4.4 nanites have neither (`tradable = no`, no `max`), so they must
# remain outside this list even though they are otherwise modeled economically.
MARKET_CAP_BREAKER_SALES = [
    ("minerals", 50000, 5000, ""),
    ("food", 30000, 5000, "country_uses_food = yes"),
    ("consumer_goods", 30000, 2500, "country_uses_consumer_goods = yes"),
    ("volatile_motes", 800, 200, ""),
    ("exotic_gases", 800, 200, ""),
    ("rare_crystals", 800, 200, ""),
    ("sr_dark_matter", 1000, 100, ""),
    ("sr_zro", 1000, 100, ""),
    ("giga_sr_sentient_metal", 2500, 250, "has_technology = tech_ehof_sentient_tier_1"),
]

ROUTE_OVERRIDE_TARGETS = [
    # Core unlock techs and high-scale research chains.
    {"object_id": "tech_mega_engineering", "object_type": "technology", "mod_id": "vanilla", "route_id": "mega_engineering_core", "weight": 200000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_mega_shipyard", "object_type": "technology", "mod_id": "vanilla", "route_id": "mega_shipyard_core", "weight": 180000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_science_nexus", "object_type": "technology", "mod_id": "vanilla", "route_id": "research_megastructure_core", "weight": 185000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_ring_world", "object_type": "technology", "mod_id": "1121692237", "source_file": "common/technology/zz_giga_tech_overwrites.txt", "route_id": "ring_world_growth_core", "weight": 175000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_orbital_arc_furnace", "object_type": "technology", "mod_id": "vanilla", "route_id": "early_kilo_economy_core", "weight": 165000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_asteroid_manufactory", "object_type": "technology", "mod_id": "1121692237", "route_id": "early_kilo_economy_core", "weight": 160000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_engineering_test_site", "object_type": "technology", "mod_id": "1121692237", "route_id": "science_kilo_snowball_core", "weight": 165000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_macro_scale_weather_manipulation", "object_type": "technology", "mod_id": "1121692237", "route_id": "science_kilo_snowball_core", "weight": 170000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_planetary_computer", "object_type": "technology", "mod_id": "1121692237", "route_id": "planetary_computer_research_core", "weight": 190000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_robotic_workers", "object_type": "technology", "mod_id": "vanilla", "route_id": "pop_assembly_snowball_core", "weight": 145000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_robot_assembly_complex", "object_type": "technology", "mod_id": "vanilla", "route_id": "pop_assembly_snowball_core", "weight": 165000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_mega_assembly", "object_type": "technology", "mod_id": "vanilla", "route_id": "pop_assembly_snowball_core", "weight": 175000, "file_key": "01_unlock_technology"},
    {"object_id": "tech_cloning", "object_type": "technology", "mod_id": "vanilla", "route_id": "pop_assembly_snowball_core", "weight": 150000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_kugelblitz", "object_type": "technology", "mod_id": "1121692237", "route_id": "storage_cap_core", "weight": 160000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_matrioshka_brain_1", "object_type": "technology", "mod_id": "1121692237", "route_id": "apex_site_preservation_core", "weight": 210000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_neutronium_gigaforge", "object_type": "technology", "mod_id": "1121692237", "route_id": "apex_site_preservation_core", "weight": 185000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_nidavellir", "object_type": "technology", "mod_id": "1121692237", "route_id": "apex_site_preservation_core", "weight": 195000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_interstellar_habitat", "object_type": "technology", "mod_id": "1121692237", "route_id": "crowded_tall_route", "weight": 155000, "file_key": "01_unlock_technology"},
    {"object_id": "giga_tech_stellar_ring_habitat", "object_type": "technology", "mod_id": "1121692237", "route_id": "crowded_tall_route", "weight": 150000, "file_key": "01_unlock_technology"},
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
    # AP and native tradition category/node pressure for routes that Stellaris otherwise treats as optional flavor.
    {"object_id": "ap_technological_ascendancy", "object_type": "ascension_perk", "mod_id": "vanilla", "source_file": "common/ascension_perks/00_ascension_perks.txt", "route_id": "research_diplomacy_core", "weight": 150000, "file_key": "02_perks_traditions"},
    {"object_id": "ap_master_builders", "object_type": "ascension_perk", "mod_id": "vanilla", "source_file": "common/ascension_perks/00_ascension_perks.txt", "route_id": "economy_megastructure_core", "weight": 125000, "file_key": "02_perks_traditions"},
    {"object_id": "ap_galactic_wonders", "object_type": "ascension_perk", "mod_id": "vanilla", "source_file": "common/ascension_perks/00_ascension_perks.txt", "route_id": "economy_megastructure_core", "weight": 150000, "file_key": "02_perks_traditions"},
    {"object_id": "ap_gigastructural_constructs", "object_type": "ascension_perk", "mod_id": "1121692237", "route_id": "economy_megastructure_core", "weight": 120000, "file_key": "02_perks_traditions"},
    {"object_id": "ap_celestial_printing", "object_type": "ascension_perk", "mod_id": "1121692237", "route_id": "planetcraft_route", "weight": 180000, "file_key": "02_perks_traditions"},
    {"object_id": "ap_lord_of_war", "object_type": "ascension_perk", "mod_id": "vanilla", "route_id": "conquest_escape_route", "weight": 80000, "file_key": "02_perks_traditions"},
    {"object_id": "tradition_discovery", "object_type": "tradition_category", "mod_id": "vanilla", "source_file": "common/tradition_categories/00_discovery.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tradition_diplomacy", "object_type": "tradition_category", "mod_id": "vanilla", "source_file": "common/tradition_categories/00_diplomacy.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tradition_supremacy", "object_type": "tradition_category", "mod_id": "vanilla", "source_file": "common/tradition_categories/00_supremacy.txt", "route_id": "conquest_escape_route", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tradition_prosperity", "object_type": "tradition_category", "mod_id": "vanilla", "source_file": "common/tradition_categories/00_prosperity.txt", "route_id": "economy_megastructure_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tradition_adaptability", "object_type": "tradition_category", "mod_id": "vanilla", "source_file": "common/tradition_categories/00_adaptability.txt", "route_id": "crowded_tall_route", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tradition_mercantile", "object_type": "tradition_category", "mod_id": "vanilla", "source_file": "common/tradition_categories/00_commerce.txt", "route_id": "crowded_tall_route", "weight": 4, "file_key": "02_perks_traditions"},
    # Selectable nodes retain the research/diplomacy route after a tree is adopted.
    # Adoption and finish rewards are automatic engine effects and must never be targeted.
    {"object_id": "tr_discovery_to_boldly_go", "object_type": "tradition", "mod_id": "vanilla", "source_file": "common/traditions/00_discovery.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tr_discovery_databank_uplinks", "object_type": "tradition", "mod_id": "vanilla", "source_file": "common/traditions/00_discovery.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tr_discovery_science_division", "object_type": "tradition", "mod_id": "vanilla", "source_file": "common/traditions/00_discovery.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tr_discovery_polytechnic_education", "object_type": "tradition", "mod_id": "vanilla", "source_file": "common/traditions/00_discovery.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tr_discovery_faith_in_science", "object_type": "tradition", "mod_id": "vanilla", "source_file": "common/traditions/00_discovery.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tr_diplomacy_the_federation", "object_type": "tradition", "mod_id": "vanilla", "source_file": "common/traditions/00_diplomacy.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tr_diplomacy_entente_coordination", "object_type": "tradition", "mod_id": "vanilla", "source_file": "common/traditions/00_diplomacy.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tr_diplomacy_diplomatic_networking", "object_type": "tradition", "mod_id": "vanilla", "source_file": "common/traditions/00_diplomacy.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tr_diplomacy_direct_diplomacy", "object_type": "tradition", "mod_id": "vanilla", "source_file": "common/traditions/00_diplomacy.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "tr_diplomacy_eminent_diplomats", "object_type": "tradition", "mod_id": "vanilla", "source_file": "common/traditions/00_diplomacy.txt", "route_id": "research_diplomacy_core", "weight": 4, "file_key": "02_perks_traditions"},
    {"object_id": "influence_expenditure_claims", "object_type": "ai_budget", "mod_id": "vanilla", "route_id": "conquest_escape_route", "weight": 145000, "file_key": "08_site_limited_expansion"},
    {"object_id": "influence_expenditure_claims_militarist", "object_type": "ai_budget", "mod_id": "vanilla", "route_id": "conquest_escape_route", "weight": 165000, "file_key": "08_site_limited_expansion"},
    {"object_id": "influence_expenditure_claims_fanatic_militarist", "object_type": "ai_budget", "mod_id": "vanilla", "route_id": "conquest_escape_route", "weight": 185000, "file_key": "08_site_limited_expansion"},
    # Direct research-throughput infrastructure for the observed low-tech/high-stockpile failure mode.
    {"object_id": "building_research_lab_1", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 220000, "coefficient": "14", "additional_weight": "2000", "file_key": "06_research_infrastructure"},
    {"object_id": "building_research_lab_2", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 250000, "coefficient": "16", "additional_weight": "2600", "file_key": "06_research_infrastructure"},
    {"object_id": "building_research_lab_3", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 280000, "coefficient": "18", "additional_weight": "3200", "file_key": "06_research_infrastructure"},
    {"object_id": "building_institute", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 240000, "coefficient": "14", "additional_weight": "2200", "file_key": "06_research_infrastructure"},
    {"object_id": "building_supercomputer", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 240000, "coefficient": "14", "additional_weight": "2200", "file_key": "06_research_infrastructure"},
    {"object_id": "building_archaeostudies_faculty", "object_type": "building", "mod_id": "3610149307", "source_file": "common/buildings/~stellarai_research_buildings.txt", "route_id": "research_throughput_infrastructure", "weight": 190000, "coefficient": "10", "additional_weight": "1600", "file_key": "06_research_infrastructure"},
    {"object_id": "district_hab_science", "object_type": "district", "mod_id": "vanilla", "source_file": "common/districts/03_habitat_districts.txt", "route_id": "research_throughput_infrastructure", "weight": 210000, "coefficient": "12", "additional_weight": "1800", "file_key": "06_research_infrastructure"},
    # Compounding-growth infrastructure: population and science capacity pay off over the full game clock.
    {"object_id": "building_robot_assembly_plant", "object_type": "building", "mod_id": "vanilla", "source_file": "common/buildings/01_pop_assembly_buildings.txt", "route_id": "pop_assembly_snowball_core", "weight": 155000, "coefficient": "8", "additional_weight": "900", "file_key": "07_pop_assembly"},
    {"object_id": "building_robot_assembly_complex", "object_type": "building", "mod_id": "vanilla", "source_file": "common/buildings/01_pop_assembly_buildings.txt", "route_id": "pop_assembly_snowball_core", "weight": 175000, "coefficient": "10", "additional_weight": "1200", "file_key": "07_pop_assembly"},
    {"object_id": "building_machine_assembly_plant", "object_type": "building", "mod_id": "vanilla", "source_file": "common/buildings/01_pop_assembly_buildings.txt", "route_id": "pop_assembly_snowball_core", "weight": 155000, "coefficient": "8", "additional_weight": "900", "file_key": "07_pop_assembly"},
    {"object_id": "building_machine_assembly_complex", "object_type": "building", "mod_id": "vanilla", "source_file": "common/buildings/01_pop_assembly_buildings.txt", "route_id": "pop_assembly_snowball_core", "weight": 175000, "coefficient": "10", "additional_weight": "1200", "file_key": "07_pop_assembly"},
    {"object_id": "building_clone_vats", "object_type": "building", "mod_id": "vanilla", "source_file": "common/buildings/01_pop_assembly_buildings.txt", "route_id": "pop_assembly_snowball_core", "weight": 170000, "coefficient": "10", "additional_weight": "1200", "file_key": "07_pop_assembly"},
    {"object_id": "building_spawning_pool", "object_type": "building", "mod_id": "vanilla", "source_file": "common/buildings/01_pop_assembly_buildings.txt", "route_id": "pop_assembly_snowball_core", "weight": 160000, "coefficient": "9", "additional_weight": "1000", "file_key": "07_pop_assembly"},
    {"object_id": "building_offspring_nest", "object_type": "building", "mod_id": "vanilla", "source_file": "common/buildings/01_pop_assembly_buildings.txt", "route_id": "pop_assembly_snowball_core", "weight": 150000, "coefficient": "7", "additional_weight": "800", "file_key": "07_pop_assembly"},
    {"object_id": "district_giga_pcc_science", "object_type": "district", "mod_id": "1121692237", "source_file": "common/districts/giga_planetary_computer.txt", "route_id": "planetary_computer_research_core", "weight": 190000, "coefficient": "12", "additional_weight": "1800", "file_key": "06_research_infrastructure"},
    # Concrete build-priority objects for economy multipliers, Mega Shipyard, planetcraft, war moons, and systemcraft.
    {"object_id": "dyson_sphere_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_dyson_sphere.txt", "route_id": "economy_megastructure_core", "weight": 130000, "file_key": "03_megastructures"},
    {"object_id": "orbital_arc_furnace_1", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_orbital_arc_furnace.txt", "route_id": "early_kilo_economy_core", "weight": 130000, "file_key": "03_megastructures"},
    {"object_id": "asteroid_manufactory_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_asteroid_manufactory.txt", "route_id": "early_kilo_economy_core", "weight": 125000, "file_key": "03_megastructures"},
    {"object_id": "macro_test_site_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_macroengineering_test_site.txt", "route_id": "science_kilo_snowball_core", "weight": 145000, "file_key": "03_megastructures"},
    {"object_id": "macro_test_site_1", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_macroengineering_test_site.txt", "route_id": "science_kilo_snowball_core", "weight": 160000, "file_key": "03_megastructures"},
    {"object_id": "macro_test_site_2", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_macroengineering_test_site.txt", "route_id": "science_kilo_snowball_core", "weight": 175000, "file_key": "03_megastructures"},
    {"object_id": "macro_test_site_3", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_macroengineering_test_site.txt", "route_id": "science_kilo_snowball_core", "weight": 190000, "file_key": "03_megastructures"},
    {"object_id": "atmosphere_shredder_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_atmospheric_storm_observatory.txt", "route_id": "science_kilo_snowball_core", "weight": 150000, "file_key": "03_megastructures"},
    {"object_id": "atmosphere_shredder_1", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_atmospheric_storm_observatory.txt", "route_id": "science_kilo_snowball_core", "weight": 165000, "file_key": "03_megastructures"},
    {"object_id": "atmosphere_shredder_2", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_atmospheric_storm_observatory.txt", "route_id": "science_kilo_snowball_core", "weight": 180000, "file_key": "03_megastructures"},
    {"object_id": "atmosphere_shredder_3", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_atmospheric_storm_observatory.txt", "route_id": "science_kilo_snowball_core", "weight": 195000, "file_key": "03_megastructures"},
    {"object_id": "think_tank_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_science_nexus.txt", "route_id": "research_megastructure_core", "weight": 155000, "file_key": "03_megastructures"},
    {"object_id": "think_tank_1", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_science_nexus.txt", "route_id": "research_megastructure_core", "weight": 170000, "file_key": "03_megastructures"},
    {"object_id": "think_tank_2", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_science_nexus.txt", "route_id": "research_megastructure_core", "weight": 185000, "file_key": "03_megastructures"},
    {"object_id": "think_tank_3", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_science_nexus.txt", "route_id": "research_megastructure_core", "weight": 200000, "file_key": "03_megastructures"},
    {"object_id": "ring_world_1", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_ring_world.txt", "route_id": "ring_world_growth_core", "weight": 145000, "file_key": "03_megastructures"},
    {"object_id": "ring_world_2_intermediate", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_ring_world.txt", "route_id": "ring_world_growth_core", "weight": 160000, "file_key": "03_megastructures"},
    {"object_id": "ring_world_3_intermediate", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_ring_world.txt", "route_id": "ring_world_growth_core", "weight": 175000, "file_key": "03_megastructures"},
    {"object_id": "kugelblitz_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_kugelblitz.txt", "route_id": "storage_cap_core", "weight": 125000, "file_key": "03_megastructures"},
    {"object_id": "kugelblitz_1", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_kugelblitz.txt", "route_id": "storage_cap_core", "weight": 150000, "file_key": "03_megastructures"},
    {"object_id": "kugelblitz_2", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_kugelblitz.txt", "route_id": "storage_cap_core", "weight": 170000, "file_key": "03_megastructures"},
    {"object_id": "kugelblitz_3", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_c_kugelblitz.txt", "route_id": "storage_cap_core", "weight": 190000, "file_key": "03_megastructures"},
    {"object_id": "habitat_central_complex", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_b_habitats.txt", "route_id": "crowded_tall_route", "weight": 5, "file_key": "03_megastructures"},
    {"object_id": "interstellar_habitat_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_interstellar_habitat.txt", "route_id": "crowded_tall_route", "weight": 145000, "file_key": "03_megastructures"},
    {"object_id": "stellar_ring_habitat_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_stellar_ring_habitat.txt", "route_id": "crowded_tall_route", "weight": 145000, "file_key": "03_megastructures"},
    {"object_id": "planetary_computer_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_planetary_computer.txt", "route_id": "planetary_computer_research_core", "weight": 175000, "file_key": "03_megastructures"},
    {"object_id": "planetary_computer_1", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_planetary_computer.txt", "route_id": "planetary_computer_research_core", "weight": 190000, "file_key": "03_megastructures"},
    {"object_id": "mega_shipyard_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_mega_shipyard.txt", "route_id": "mega_shipyard_core", "weight": 150000, "file_key": "03_megastructures"},
    {"object_id": "matrioshka_brain_0_g_star", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_i_matrioshka_brain_revised.txt", "route_id": "economy_megastructure_core", "weight": 145000, "file_key": "03_megastructures"},
    {"object_id": "matrioshka_brain_0_o_star", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_i_matrioshka_brain_revised.txt", "route_id": "apex_site_preservation_core", "weight": 230000, "file_key": "03_megastructures"},
    {"object_id": "dyson_sphere_0_o_star", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_dyson_sphere_o_star.txt", "route_id": "apex_site_preservation_core", "weight": 45000, "file_key": "03_megastructures"},
    {"object_id": "neutronium_gigaforge_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_neutronium_gigaforge.txt", "route_id": "apex_site_preservation_core", "weight": 210000, "file_key": "03_megastructures"},
    {"object_id": "nidavellir_forge_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_i_nidavellir_forge.txt", "route_id": "apex_site_preservation_core", "weight": 220000, "file_key": "03_megastructures"},
    {"object_id": "planetcraft_printer_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_i_behemoth_assembly_plant.txt", "route_id": "planetcraft_route", "weight": 180000, "file_key": "03_megastructures"},
    {"object_id": "war_moon_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_e_attack_moon.txt", "route_id": "war_moon_route", "weight": 165000, "file_key": "03_megastructures"},
    {"object_id": "war_system_0", "object_type": "megastructure", "mod_id": "1121692237", "source_file": "common/megastructures/zz_i_stellar_systemcraft.txt", "route_id": "systemcraft_route", "weight": 200000, "file_key": "03_megastructures"},
    # Parent design surfaces that need direct pressure when AI weights are partial or wrong-goal.
    # NSC3 hull and ESC component-template usage is covered through unlock tech, fleet economy,
    # and starbase support here because the current atlas does not model ESC internal `key =`
    # component-template entries as top-level load-order objects.
    {"object_id": "esc_starbase_reactor", "object_type": "starbase_building", "mod_id": "2648658105", "route_id": "fallen_empire_benchmark_route", "weight": 75000, "file_key": "05_starbase_defense"},
    {"object_id": "adv_starbase_defenses", "object_type": "starbase_building", "mod_id": "683230077", "source_file": "common/starbase_buildings/nsc_starbase_buildings.txt", "route_id": "fallen_empire_benchmark_route", "weight": 110000, "file_key": "05_starbase_defense"},
    {"object_id": "reinforced_defenses", "object_type": "starbase_building", "mod_id": "3250900527", "source_file": "common/starbase_buildings/sbx_3_0_buildings.txt", "route_id": "fallen_empire_benchmark_route", "weight": 105000, "file_key": "05_starbase_defense"},
    {"object_id": "strategic_defenses", "object_type": "starbase_building", "mod_id": "3250900527", "source_file": "common/starbase_buildings/sbx_3_0_buildings.txt", "route_id": "fallen_empire_benchmark_route", "weight": 120000, "file_key": "05_starbase_defense"},
    {"object_id": "gun_battery", "object_type": "starbase_module", "mod_id": "3250900527", "source_file": "common/starbase_modules/sbx_3_0_starbase_modules.txt", "route_id": "fallen_empire_benchmark_route", "weight": 90000, "file_key": "05_starbase_defense"},
    {"object_id": "missile_battery", "object_type": "starbase_module", "mod_id": "3250900527", "source_file": "common/starbase_modules/sbx_3_0_starbase_modules.txt", "route_id": "fallen_empire_benchmark_route", "weight": 90000, "file_key": "05_starbase_defense"},
    {"object_id": "hangar_bay", "object_type": "starbase_module", "mod_id": "3250900527", "source_file": "common/starbase_modules/sbx_3_0_starbase_modules.txt", "route_id": "fallen_empire_benchmark_route", "weight": 95000, "file_key": "05_starbase_defense"},
    {"object_id": "large_battery", "object_type": "starbase_module", "mod_id": "3250900527", "source_file": "common/starbase_modules/sbx_3_0_starbase_modules.txt", "route_id": "fallen_empire_benchmark_route", "weight": 105000, "file_key": "05_starbase_defense"},
    {"object_id": "armor_module", "object_type": "starbase_module", "mod_id": "3250900527", "source_file": "common/starbase_modules/sbx_3_0_starbase_modules.txt", "route_id": "fallen_empire_benchmark_route", "weight": 80000, "file_key": "05_starbase_defense"},
    {"object_id": "orbital_ring_gun_battery", "object_type": "starbase_module", "mod_id": "3250900527", "source_file": "common/starbase_modules/sbx_3_0_orbital_ring_modules.txt", "route_id": "fallen_empire_benchmark_route", "weight": 80000, "file_key": "05_starbase_defense"},
    {"object_id": "orbital_ring_missile_battery", "object_type": "starbase_module", "mod_id": "3250900527", "source_file": "common/starbase_modules/sbx_3_0_orbital_ring_modules.txt", "route_id": "fallen_empire_benchmark_route", "weight": 80000, "file_key": "05_starbase_defense"},
    {"object_id": "orbital_ring_hangar_bay", "object_type": "starbase_module", "mod_id": "3250900527", "source_file": "common/starbase_modules/sbx_3_0_orbital_ring_modules.txt", "route_id": "fallen_empire_benchmark_route", "weight": 85000, "file_key": "05_starbase_defense"},
    {"object_id": "orbital_ring_large_gun_battery", "object_type": "starbase_module", "mod_id": "3250900527", "source_file": "common/starbase_modules/sbx_3_0_orbital_ring_modules.txt", "route_id": "fallen_empire_benchmark_route", "weight": 90000, "file_key": "05_starbase_defense"},
    {"object_id": "orbital_ring_armor_module", "object_type": "starbase_module", "mod_id": "3250900527", "source_file": "common/starbase_modules/sbx_3_0_orbital_ring_modules.txt", "route_id": "fallen_empire_benchmark_route", "weight": 75000, "file_key": "05_starbase_defense"},
    # Verified diplomacy lever: federation type ai_weight is safe to copy and patch.
    # Diplomatic actions, personalities, and federation law rewrites remain gated high-risk work.
    {"object_id": "research_federation", "object_type": "federation_type", "mod_id": "vanilla", "source_file": "common/federation_types/00_federation_types.txt", "route_id": "research_diplomacy_core", "weight": 0, "file_key": "15_research_diplomacy"},
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
    # Save-compatibility IDs only. The stateful threat-response producer is
    # retired, and existing serialized modifiers must resolve without changing
    # diplomacy while old timed references age out of copied saves.
    "anti_aggressor_low": 0,
    "anti_aggressor_medium": 0,
    "anti_aggressor_high": 0,
    "anti_aggressor_severe": 0,
    "shared_threat_low": 0,
    "shared_threat_medium": 0,
    "shared_threat_high": 0,
    "alignment_low": 0,
    "alignment_medium": 0,
    "alignment_high": 0,
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
    "P14": "Deferred until non-runtime gates are complete: launch proof must be checked separately from static validation.",
    "P15": "Deferred until non-runtime gates are complete: observer runtime validation remains the final efficacy proof gate.",
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
    items: list[PDXAssignment | PDXAtom | PDXBlock] = field(default_factory=list)


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
                elif tokens[index] == "{":
                    block.items.append(parse_value())
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
        text = read_text(path)
        return parse_pdx(normalize_macro_expressions(text, collect_variables(text)))
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
        lambda match: str(
            variables.get(match.group(0), variables.get(f"@{match.group(0)}", match.group(0)))
        ),
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
        "parity_reference_mods": {
            mod_id: {
                "name": name,
                "present": mod_id in present_ids,
                "load_position": mod_ids.index(mod_id) + 1 if mod_id in present_ids else None,
            }
            for mod_id, name in PARITY_REFERENCE_MODS.items()
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
    roots = [Path(row["snapshot_path"]) for row in manifest.values() if Path(row["snapshot_path"]).exists()]
    for root in (PLANETARY_DIVERSITY_WORKSHOP_ROOT, PLANETARY_DIVERSITY_MORE_ARCOLOGIES_WORKSHOP_ROOT):
        if root.exists() and root not in roots:
            roots.append(root)
    return roots


WRAPPED_OBJECT_ID_CHILD_KEYS = {
    "component_set": "key",
    "component_template": "key",
    "ship_behavior": "name",
}


def assignment_object_id(object_type: str, assignment: PDXAssignment) -> str | None:
    child_key = WRAPPED_OBJECT_ID_CHILD_KEYS.get(object_type)
    if child_key is None:
        return assignment.key
    if not isinstance(assignment.value, PDXBlock):
        return None
    for child in block_assignments(assignment.value, child_key):
        value = atom_value(child.value)
        if value:
            return value
    return None


def collect_object_names(
    snapshot_root: Path = SNAPSHOT_ROOT,
    inventory_roots: Iterable[Path] | None = None,
) -> dict[str, set[str]]:
    # on_actions and defines have merge semantics that are not represented by
    # this object-level collision inventory. All remaining generated surfaces
    # use named full-object definitions and must be checked against parents.
    folder_map = {
        folder: object_type
        for folder, object_type in GENERATED_SURFACE_FOLDERS.items()
        if folder not in {"defines", "on_actions", "scripted_variables"}
    }
    folder_map.update(
        {
            "strategic_resources": "resource",
            "resources": "resource",
            "planet_classes": "planet_class",
            "pop_jobs": "pop_job",
        }
    )
    buckets = {object_type: set() for object_type in folder_map.values()}
    roots = list(inventory_roots) if inventory_roots is not None else object_inventory_roots(snapshot_root)
    for root in roots:
        common = root / "common"
        if not common.exists():
            continue
        for folder, bucket in folder_map.items():
            folder_path = common / folder
            if not folder_path.exists():
                continue
            for file_path in iter_text_files(folder_path):
                if file_path.name.startswith(DATASET_JOB_PRESSURE_FILE_PREFIX):
                    continue
                try:
                    parsed = parse_file(file_path)
                except PDXParseError:
                    continue
                for assignment in block_assignments(parsed):
                    object_id = assignment_object_id(bucket, assignment)
                    if object_id and not object_id.startswith("@"):
                        buckets[bucket].add(object_id)
    vanilla = VANILLA_COMMON_ROOT
    if vanilla.exists():
        for folder, bucket in folder_map.items():
            folder_path = vanilla / folder
            if not folder_path.exists():
                continue
            for file_path in iter_text_files(folder_path):
                if file_path.name.startswith(DATASET_JOB_PRESSURE_FILE_PREFIX):
                    continue
                try:
                    parsed = parse_file(file_path)
                except PDXParseError:
                    continue
                for assignment in block_assignments(parsed):
                    object_id = assignment_object_id(bucket, assignment)
                    if object_id and not object_id.startswith("@"):
                        buckets[bucket].add(object_id)
    return buckets


ECONOMIC_VALUATION_FOLDERS = {
    "buildings": "building",
    "zones": "zone",
    "districts": "district",
}
ECONOMIC_VALUATION_SOURCE_FOLDERS = {
    "ascension_perk": "ascension_perks",
    "building": "buildings",
    "colony_type": "colony_types",
    "decision": "decisions",
    "deposit": "deposits",
    "district": "districts",
    "edict": "edicts",
    "policy": "policies",
    "pop_job": "pop_jobs",
    "resource": "strategic_resources",
    "starbase_building": "starbase_buildings",
    "starbase_module": "starbase_modules",
    "technology": "technology",
    "tradition": "traditions",
    "zone": "zones",
}
DATASET_JOB_PRESSURE_FILE_PREFIX = "zzzz_staid_13_dataset_job_pressure_"

ECONOMIC_VALUATION_RESOURCE_KEYS = set(RESOURCE_VALUES) | {
    "food",
    "trade",
    "influence",
    "amenities",
    "stability",
    "crime",
    "naval_cap",
    "mod_country_naval_cap_add",
    "pop_growth_speed",
}
GENERIC_JOB_MONTHLY_VALUE = 6.0
JOB_WORKFORCE_UNITS = 100.0
GENERIC_BUILDING_SLOT_VALUE = 12.0
GENERIC_MODIFIER_KEY_VALUE = 3.0


def _json_dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _normalized_number(value: float) -> int | float:
    rounded = round(float(value), 6)
    return int(rounded) if rounded.is_integer() else rounded


def _source_numeric_facts(value: PDXValue, variables: dict[str, float]) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []

    def walk(current: PDXValue, path: tuple[str, ...]) -> None:
        if isinstance(current, PDXAtom):
            token = current.value.strip('"')
            if token in variables:
                facts.append(
                    {
                        "path": ".".join(path),
                        "source": "variable",
                        "token": token,
                        "value": _normalized_number(variables[token]),
                    }
                )
                return
            try:
                number = float(token)
            except ValueError:
                return
            facts.append(
                {
                    "path": ".".join(path),
                    "source": "literal",
                    "token": token,
                    "value": _normalized_number(number),
                }
            )
            return
        for item in current.items:
            if isinstance(item, PDXAssignment):
                walk(item.value, (*path, item.key.strip('"')))
            elif isinstance(item, PDXAtom):
                walk(item, (*path, "$atom"))
            elif isinstance(item, PDXBlock):
                walk(item, (*path, "$block"))

    walk(value, ())
    return facts


def _source_numeric_fact_columns(value: PDXValue, variables: dict[str, float]) -> dict[str, str]:
    facts_json = _json_dump(_source_numeric_facts(value, variables))
    return {
        "source_numeric_facts_json": facts_json,
        "source_numeric_facts_hash": hashlib.sha256(facts_json.encode("utf-8")).hexdigest(),
    }


def _pdx_to_plain(value: PDXValue) -> Any:
    if isinstance(value, PDXAtom):
        return value.value.strip('"')
    rows: list[Any] = []
    for item in value.items:
        if isinstance(item, PDXAssignment):
            rows.append({item.key: _pdx_to_plain(item.value)})
        elif isinstance(item, PDXAtom):
            rows.append(item.value.strip('"'))
        elif isinstance(item, PDXBlock):
            rows.append(_pdx_to_plain(item))
    return rows


def _numeric_atom(value: PDXValue, variables: dict[str, float]) -> tuple[float, str | None]:
    atom = atom_value(value)
    if atom is None:
        return (0.0, None)
    if atom in variables:
        return (variables[atom], None)
    macro_value = eval_macro_expression(atom, variables)
    if macro_value is not None:
        return (macro_value, None)
    try:
        return (float(atom), None)
    except ValueError:
        if atom.startswith("@["):
            return (0.0, atom)
        return (0.0, atom if atom.startswith("@") else None)


def _object_variables(winner: dict[str, Any], global_variables: dict[str, float]) -> dict[str, float]:
    variables = dict(global_variables)
    source_file = winner.get("source_file")
    if source_file:
        variables.update(collect_variables(read_text(Path(source_file))))
    return variables


SPECIAL_SCOPED_UNRESOLVED_VARIABLE_EXCLUSIONS = {
    ("district", "district_giga_birch_physma_administration"): {
        "@[": "birch_world_special_colony_missing_sector_job_expression_modeled_zero_effect",
    },
}


SPECIAL_COLONY_CLASSES = {"alderson_disk", "birch_world", "frameworld"}


def _scope_prefix(item: str) -> str:
    return item.split(":", 1)[1] if ":" in item else item


def _row_item_token(row: dict[str, Any]) -> str:
    object_type = str(row.get("object_type", ""))
    object_id = str(row.get("object_id", ""))
    if object_type == "district":
        return f"district:{object_id}"
    return object_id


def build_plan_consumer_policy_excludes_dataset_object(
    row: dict[str, Any],
    policy_row: dict[str, Any] | None,
) -> bool:
    colony_class = str(row.get("colony_class", ""))
    if colony_class in SPECIAL_COLONY_CLASSES:
        if not policy_row:
            return True
        object_id = str(policy_row.get("object_id", ""))
        selected_objects = {
            _scope_prefix(item.strip())
            for item in str(policy_row.get("selected_objects", "")).split("|")
            if item.strip()
        }
        if object_id.endswith(f":{colony_class}") and _scope_prefix(_row_item_token(row)) in selected_objects:
            return False
        return True
    return False


def _collect_resource_amounts(value: PDXValue, variables: dict[str, float]) -> tuple[dict[str, float], set[str]]:
    amounts: dict[str, float] = {}
    unresolved: set[str] = set()
    for assignment in iter_assignments(value):
        key = assignment.key.strip('"')
        if key not in ECONOMIC_VALUATION_RESOURCE_KEYS:
            continue
        amount, unresolved_variable = _numeric_atom(assignment.value, variables)
        if unresolved_variable:
            unresolved.add(unresolved_variable)
        amounts[key] = amounts.get(key, 0.0) + amount
    return amounts, unresolved


def _resource_value(amounts: dict[str, float]) -> float:
    return sum(amount * RESOURCE_VALUES.get(resource, 0.25) for resource, amount in amounts.items())


JOB_ADD_EXCLUDED_CONTEXTS = {
    "country_modifier",
    "triggered_country_modifier",
    "owner_modifier",
    "triggered_owner_modifier",
    "system_modifier",
    "triggered_system_modifier",
    "starbase_modifier",
    "triggered_starbase_modifier",
    "ship_modifier",
    "triggered_ship_modifier",
    "fleet_modifier",
    "triggered_fleet_modifier",
}


def _iter_assignments_with_path(value: PDXValue, path: tuple[str, ...] = ()) -> Iterable[tuple[PDXAssignment, tuple[str, ...]]]:
    if isinstance(value, PDXBlock):
        for item in value.items:
            if isinstance(item, PDXAssignment):
                key = item.key.strip('"')
                item_path = (*path, key)
                yield item, item_path
                yield from _iter_assignments_with_path(item.value, item_path)


def _collect_job_adds(
    value: PDXValue,
    variables: dict[str, float],
    ignored_job_add_keys: set[str] | None = None,
) -> tuple[dict[str, float], set[str]]:
    jobs: dict[str, float] = {}
    unresolved: set[str] = set()
    ignored_keys = ignored_job_add_keys or set()
    for assignment, path in _iter_assignments_with_path(value):
        key = assignment.key.strip('"')
        if not re.fullmatch(r"job_[A-Za-z0-9_]+_add", key):
            continue
        if key in ignored_keys:
            continue
        if any(context in JOB_ADD_EXCLUDED_CONTEXTS for context in path[:-1]):
            continue
        amount, unresolved_variable = _numeric_atom(assignment.value, variables)
        if unresolved_variable:
            unresolved.add(unresolved_variable)
        jobs[key.removesuffix("_add")] = jobs.get(key.removesuffix("_add"), 0.0) + amount
    return jobs, unresolved


def _assignment_plain(value: PDXBlock, keys: set[str]) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for assignment in block_assignments(value):
        if assignment.key in keys:
            rows[assignment.key] = _pdx_to_plain(assignment.value)
    return rows


def _top_level_ai_state(value: PDXBlock, variables: dict[str, float]) -> tuple[dict[str, Any], set[str]]:
    ai_keys = {
        "ai_weight",
        "ai_weight_coefficient",
        "additional_ai_weight",
        "ai_priority",
        "ai_resource_production",
        "ai_estimate_without_unemployment",
    }
    state = _assignment_plain(value, ai_keys)
    unresolved: set[str] = set()
    for key in ("ai_weight_coefficient", "ai_priority"):
        for assignment in block_assignments(value, key):
            amount, unresolved_variable = _numeric_atom(assignment.value, variables)
            state[f"{key}_numeric"] = amount
            if unresolved_variable:
                unresolved.add(unresolved_variable)
    return state, unresolved


def _collect_modifier_keys(value: PDXValue) -> list[str]:
    keys: set[str] = set()
    for assignment in iter_assignments(value):
        key = assignment.key.strip('"')
        if key.startswith("planet_") or key.startswith("pop_") or key.startswith("job_") or key.startswith("mod_"):
            keys.add(key)
    return sorted(keys)


def _collect_upgrade_ids(value: PDXBlock) -> list[str]:
    upgrades: set[str] = set()
    for key in ("upgrades", "upgrades_to", "upgrade"):
        for assignment in block_assignments(value, key):
            if isinstance(assignment.value, PDXBlock):
                upgrades.update(atom for atom in block_atoms(assignment.value) if not atom.startswith("@"))
            else:
                atom = atom_value(assignment.value)
                if atom and not atom.startswith("@"):
                    upgrades.add(atom)
    return sorted(upgrades)


def _count_nested_assignment_blocks(value: PDXValue, key: str) -> int:
    return sum(1 for assignment in iter_assignments(value) if assignment.key == key and isinstance(assignment.value, PDXBlock))


def _serialized_value_tokens(value: PDXValue) -> set[str]:
    serialized = _json_dump(_pdx_to_plain(value))
    return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", serialized))


def _economic_structural_reference_columns(value: PDXBlock, modifier_keys: list[str]) -> dict[str, Any]:
    tokens = _serialized_value_tokens(value)
    referenced_unlocks = sorted(
        token
        for token in tokens
        if token.endswith("_unlocked") or token.startswith("unlock_") or token.startswith("allow_")
    )
    referenced_technologies = sorted(token for token in tokens if token.startswith("tech_") or token.startswith("giga_tech_"))
    referenced_deposits = sorted(token for token in tokens if token.startswith("d_"))
    job_or_modifier_tokens = sorted(
        token
        for token in tokens | set(modifier_keys)
        if token.startswith("job_") or token.startswith("planet_") or token.startswith("pop_") or token.startswith("mod_")
    )
    return {
        "top_level_keys": "|".join(sorted({assignment.key for assignment in block_assignments(value)})),
        "nested_resources_blocks": _count_nested_assignment_blocks(value, "resources"),
        "nested_ai_weight_blocks": _count_nested_assignment_blocks(value, "ai_weight"),
        "nested_modifier_blocks": _count_nested_assignment_blocks(value, "modifier"),
        "referenced_unlocks_or_flags": "|".join(referenced_unlocks),
        "referenced_technologies": "|".join(referenced_technologies),
        "referenced_deposits": "|".join(referenced_deposits),
        "referenced_jobs_or_modifiers": "|".join(job_or_modifier_tokens),
    }


def _valuation_stack_roots(playset: dict[str, Any]) -> list[dict[str, Any]]:
    roots = [
        {
            "load_position": 0,
            "steam_id": "vanilla",
            "name": "Stellaris vanilla",
            "root": STELLARIS_INSTALL_ROOT,
        }
    ]
    for mod in playset.get("mods", []):
        path = Path(str(mod.get("path", "")))
        if path.exists():
            roots.append(
                {
                    "load_position": int(mod.get("position", 0) or 0),
                    "steam_id": safe_mod_id(mod.get("steam_id")),
                    "name": str(mod.get("name", "")),
                    "root": path,
                }
            )
    return roots


def _collect_economic_definitions(playset: dict[str, Any]) -> list[dict[str, Any]]:
    definitions: list[dict[str, Any]] = []
    for root_info in _valuation_stack_roots(playset):
        root = Path(root_info["root"])
        common = root / "common"
        if not common.exists():
            continue
        for folder, object_type in ECONOMIC_VALUATION_FOLDERS.items():
            folder_path = common / folder
            if not folder_path.exists():
                continue
            for file_path in iter_text_files(folder_path):
                if file_path.name.startswith(DATASET_JOB_PRESSURE_FILE_PREFIX):
                    continue
                try:
                    parsed = parse_file(file_path)
                except PDXParseError as exc:
                    definitions.append(
                        {
                            **root_info,
                            "object_type": object_type,
                            "object_id": "",
                            "source_file": str(file_path),
                            "relative_file": str(file_path.relative_to(root)),
                            "parse_error": str(exc),
                            "value": None,
                        }
                    )
                    continue
                for assignment in block_assignments(parsed):
                    if assignment.key.startswith("@") or not isinstance(assignment.value, PDXBlock):
                        continue
                    definitions.append(
                        {
                            **root_info,
                            "object_type": object_type,
                            "object_id": assignment.key,
                            "source_file": str(file_path),
                            "relative_file": str(file_path.relative_to(root)),
                            "parse_error": "",
                            "value": assignment.value,
                        }
                    )
    return definitions


def _collect_nonconstruction_resource_definitions(playset: dict[str, Any]) -> list[dict[str, Any]]:
    definitions: list[dict[str, Any]] = []
    for root_info in _valuation_stack_roots(playset):
        root = Path(root_info["root"])
        folder_path = root / "common" / "strategic_resources"
        if not folder_path.exists():
            continue
        for file_path in iter_text_files(folder_path):
            try:
                parsed = parse_file(file_path)
            except PDXParseError:
                continue
            for assignment in block_assignments(parsed):
                if assignment.key.startswith("@") or not isinstance(assignment.value, PDXBlock):
                    continue
                definitions.append(
                    {
                        **root_info,
                        "object_type": "resource",
                        "object_id": assignment.key,
                        "source_file": str(file_path),
                        "relative_file": str(file_path.relative_to(root)),
                        "parse_error": "",
                        "value": assignment.value,
                    }
                )
    return definitions


def _winning_economic_definitions(definitions: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    winners: dict[tuple[str, str], dict[str, Any]] = {}
    for definition in definitions:
        object_id = definition.get("object_id")
        value = definition.get("value")
        if not object_id or value is None:
            continue
        key = (str(definition["object_type"]), str(object_id))
        current = winners.get(key)
        if current is None or int(definition["load_position"]) >= int(current["load_position"]):
            winners[key] = definition
    return winners


def _economic_source_summary(definitions: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    summaries: dict[tuple[str, str], dict[str, Any]] = {}
    for definition in definitions:
        object_id = definition.get("object_id")
        if not object_id:
            continue
        key = (str(definition["object_type"]), str(object_id))
        summary = summaries.setdefault(key, {"source_count": 0, "source_mods": [], "source_files": []})
        summary["source_count"] += 1
        summary["source_mods"].append(str(definition.get("name", "")))
        summary["source_files"].append(str(definition.get("relative_file", "")))
    return summaries


def _economic_object_row(
    key: tuple[str, str],
    winner: dict[str, Any],
    source_summary: dict[str, Any],
    variables: dict[str, float],
) -> dict[str, Any]:
    variables = _object_variables(winner, variables)
    value = winner["value"]
    assert isinstance(value, PDXBlock)
    flags: set[str] = set()
    cost: dict[str, float] = {}
    upkeep: dict[str, float] = {}
    output: dict[str, float] = {}
    unresolved: set[str] = set()
    for resources in block_assignments(value, "resources"):
        if not isinstance(resources.value, PDXBlock):
            continue
        for assignment in block_assignments(resources.value):
            if assignment.key == "cost":
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                cost.update({resource: cost.get(resource, 0.0) + amount for resource, amount in amounts.items()})
                unresolved.update(missing)
            elif assignment.key == "upkeep":
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                upkeep.update({resource: upkeep.get(resource, 0.0) + amount for resource, amount in amounts.items()})
                unresolved.update(missing)
            elif assignment.key in {"produces", "produced_resources"}:
                amounts, missing = _collect_resource_amounts(assignment.value, variables)
                output.update({resource: output.get(resource, 0.0) + amount for resource, amount in amounts.items()})
                unresolved.update(missing)
    for ai_production in block_assignments(value, "ai_resource_production"):
        amounts, missing = _collect_resource_amounts(ai_production.value, variables)
        output.update({resource: output.get(resource, 0.0) + amount for resource, amount in amounts.items()})
        unresolved.update(missing)
    jobs, missing_jobs = _collect_job_adds(value, variables)
    unresolved.update(missing_jobs)
    ai_state, missing_ai = _top_level_ai_state(value, variables)
    unresolved.update(missing_ai)
    scoped_exclusions = SPECIAL_SCOPED_UNRESOLVED_VARIABLE_EXCLUSIONS.get(key, {})
    unresolved = {item for item in unresolved if item not in scoped_exclusions}
    modifier_keys = _collect_modifier_keys(value)
    top_level = _assignment_plain(
        value,
        {
            "potential",
            "allow",
            "possible",
            "prerequisites",
            "show_tech_unlock_if",
            "planet_modifier",
            "triggered_planet_modifier",
            "triggered_district_planet_modifier",
            "country_modifier",
            "resources",
            "building_sets",
            "zone_sets",
            "district_set",
            "category",
        },
    )
    if jobs:
        flags.add("has_jobs")
    if output:
        flags.add("has_ai_or_direct_output")
    if cost:
        flags.add("has_build_cost")
    if upkeep:
        flags.add("has_upkeep")
    if any(assignment.key == "inline_script" for assignment in iter_assignments(value)):
        flags.add("uses_inline_script")
    if unresolved:
        flags.add("unresolved_variables")
    if "ai_weight" not in ai_state:
        flags.add("ai_weight_absent")
    elif re.search(r"weight[^A-Za-z0-9_]*0", _json_dump(ai_state.get("ai_weight", ""))):
        flags.add("ai_weight_zero_or_gated_zero")
    if int(source_summary["source_count"]) > 1:
        flags.add("overridden_in_stack")
    raw_job_workforce_total = sum(max(0.0, amount) for amount in jobs.values())
    jobs_total = raw_job_workforce_total / JOB_WORKFORCE_UNITS
    output_value = _resource_value(output)
    job_value = jobs_total * GENERIC_JOB_MONTHLY_VALUE
    modifier_value = len([key for key in modifier_keys if "produces" in key or "output" in key or "add" in key]) * GENERIC_MODIFIER_KEY_VALUE
    if "zone_building_slots_add" in modifier_keys:
        modifier_value += GENERIC_BUILDING_SLOT_VALUE
    cost_value = _resource_value(cost)
    upkeep_value = _resource_value(upkeep)
    gross_monthly_value = output_value + job_value + modifier_value
    net_monthly_value = gross_monthly_value - upkeep_value
    structural_columns = _economic_structural_reference_columns(value, modifier_keys)
    row = {
        "object_type": key[0],
        "object_id": key[1],
        "winning_load_position": winner["load_position"],
        "winning_mod_id": winner["steam_id"],
        "winning_mod_name": winner["name"],
        "winning_file": winner["relative_file"],
        "definition_count": source_summary["source_count"],
        "source_mods": "|".join(dict.fromkeys(source_summary["source_mods"])),
        "source_files": "|".join(dict.fromkeys(source_summary["source_files"])),
        "category": atom_value(block_assignments(value, "category")[0].value) if block_assignments(value, "category") else "",
        "build_cost_json": _json_dump(cost),
        "build_cost_value_estimate": round(cost_value, 3),
        "upkeep_json": _json_dump(upkeep),
        "monthly_upkeep_value_estimate": round(upkeep_value, 3),
        "jobs_created_json": _json_dump(jobs),
        "jobs_created_total_estimate": round(jobs_total, 3),
        "direct_monthly_output_json": _json_dump(output),
        "direct_monthly_output_value_estimate": round(output_value, 3),
        "modifier_keys": "|".join(modifier_keys),
        "modifier_monthly_value_estimate": round(modifier_value, 3),
        "gross_monthly_value_estimate": round(gross_monthly_value, 3),
        "net_monthly_value_estimate": round(net_monthly_value, 3),
        "roi_2200_to_2350_estimate": round(net_monthly_value * 150 * 12 - cost_value, 3),
        "roi_2250_to_2350_estimate": round(net_monthly_value * 100 * 12 - cost_value, 3),
        "roi_2300_to_2350_estimate": round(net_monthly_value * 50 * 12 - cost_value, 3),
        "roi_2325_to_2350_estimate": round(net_monthly_value * 25 * 12 - cost_value, 3),
        "upgrades_json": _json_dump(_collect_upgrade_ids(value)),
        "ai_state_json": _json_dump(ai_state),
        "prerequisites_json": _json_dump(
            {key: top_level[key] for key in ("potential", "allow", "possible", "prerequisites", "show_tech_unlock_if") if key in top_level}
        ),
        "modifiers_json": _json_dump(
            {key: top_level[key] for key in ("planet_modifier", "triggered_planet_modifier", "triggered_district_planet_modifier", "country_modifier") if key in top_level}
        ),
        "building_zone_district_sets_json": _json_dump(
            {key: top_level[key] for key in ("building_sets", "zone_sets", "district_set") if key in top_level}
        ),
        "data_quality_flags": "|".join(sorted(flags)),
        "unresolved_variables": "|".join(sorted(unresolved)),
        **_source_numeric_fact_columns(value, variables),
        **structural_columns,
    }
    return row


def _nonconstruction_resource_row(
    object_key: tuple[str, str],
    winner: dict[str, Any],
    source_summary: dict[str, Any],
    variables: dict[str, float],
) -> dict[str, Any]:
    value = winner["value"]
    assert isinstance(value, PDXBlock)
    modifier_keys = _collect_modifier_keys(value)
    ai_state, _ = _top_level_ai_state(value, {})
    top_level = _assignment_plain(value, {"potential", "modifier"})
    flags = {"cost_absent_or_indirect", "direct_output_absent_or_indirect", "strategic_classification_needed"}
    if not ai_state:
        flags.add("ai_weight_absent")
    if int(source_summary["source_count"]) > 1:
        flags.add("overridden_in_stack")
    return normalize_economic_valuation_rows(
        [
            {
                "object_type": object_key[0],
                "object_id": object_key[1],
                "winning_load_position": winner["load_position"],
                "winning_mod_id": winner["steam_id"],
                "winning_mod_name": winner["name"],
                "winning_file": winner["relative_file"],
                "definition_count": source_summary["source_count"],
                "source_mods": "|".join(dict.fromkeys(source_summary["source_mods"])),
                "source_files": "|".join(dict.fromkeys(source_summary["source_files"])),
                "category": "resource",
                "build_cost_json": "{}",
                "build_cost_value_estimate": 0,
                "upkeep_json": "{}",
                "monthly_upkeep_value_estimate": 0,
                "jobs_created_json": "{}",
                "jobs_created_total_estimate": 0,
                "direct_monthly_output_json": "{}",
                "direct_monthly_output_value_estimate": 0,
                "modifier_keys": "|".join(modifier_keys),
                "modifier_monthly_value_estimate": 0,
                "gross_monthly_value_estimate": 0,
                "net_monthly_value_estimate": 0,
                "roi_2200_to_2350_estimate": 0,
                "roi_2250_to_2350_estimate": 0,
                "roi_2300_to_2350_estimate": 0,
                "roi_2325_to_2350_estimate": 0,
                "upgrades_json": "[]",
                "ai_state_json": _json_dump(ai_state),
                "prerequisites_json": _json_dump({field: top_level[field] for field in ("potential",) if field in top_level}),
                "modifiers_json": _json_dump({field: top_level[field] for field in ("modifier",) if field in top_level}),
                "building_zone_district_sets_json": "{}",
                "data_quality_flags": "|".join(sorted(flags)),
                "unresolved_variables": "none",
                **_source_numeric_fact_columns(value, variables),
                **_economic_structural_reference_columns(value, modifier_keys),
            }
        ]
    )[0]


def build_nonconstruction_resource_rows(playset: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    playset = build_active_playset_snapshot() if playset is None else playset
    roots = [Path(item["root"]) for item in _valuation_stack_roots(playset)]
    variables = collect_global_variables(roots)
    definitions = _collect_nonconstruction_resource_definitions(playset)
    winners = _winning_economic_definitions(definitions)
    summaries = _economic_source_summary(definitions)
    return [
        _nonconstruction_resource_row(object_key, winner, summaries[object_key], variables)
        for object_key, winner in sorted(winners.items(), key=lambda item: (item[0][0], item[0][1]))
    ]


def build_economic_valuation_rows(playset: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    playset = build_active_playset_snapshot() if playset is None else playset
    roots = [Path(item["root"]) for item in _valuation_stack_roots(playset)]
    variables = collect_global_variables(roots)
    definitions = _collect_economic_definitions(playset)
    winners = _winning_economic_definitions(definitions)
    summaries = _economic_source_summary(definitions)
    rows = [
        _economic_object_row(key, winner, summaries[key], variables)
        for key, winner in sorted(winners.items(), key=lambda item: (item[0][0], item[0][1]))
    ]
    parse_errors = [definition for definition in definitions if definition.get("parse_error")]
    for parse_error in parse_errors:
        rows.append(
            {
                "object_type": "parse_error",
                "object_id": "",
                "winning_load_position": parse_error["load_position"],
                "winning_mod_id": parse_error["steam_id"],
                "winning_mod_name": parse_error["name"],
                "winning_file": parse_error["relative_file"],
                "definition_count": 0,
                "source_mods": parse_error["name"],
                "source_files": parse_error["relative_file"],
                "category": "",
                "build_cost_json": "{}",
                "build_cost_value_estimate": 0,
                "upkeep_json": "{}",
                "monthly_upkeep_value_estimate": 0,
                "jobs_created_json": "{}",
                "jobs_created_total_estimate": 0,
                "direct_monthly_output_json": "{}",
                "direct_monthly_output_value_estimate": 0,
                "modifier_keys": "",
                "modifier_monthly_value_estimate": 0,
                "gross_monthly_value_estimate": 0,
                "net_monthly_value_estimate": 0,
                "roi_2200_to_2350_estimate": 0,
                "roi_2250_to_2350_estimate": 0,
                "roi_2300_to_2350_estimate": 0,
                "roi_2325_to_2350_estimate": 0,
                "upgrades_json": "[]",
                "ai_state_json": "{}",
                "prerequisites_json": "{}",
                "modifiers_json": "{}",
                "building_zone_district_sets_json": "{}",
                "data_quality_flags": "parse_error",
                "unresolved_variables": str(parse_error["parse_error"]),
            }
        )
    return rows


def _economic_valuation_default(column: str) -> Any:
    if column in ECONOMIC_VALUATION_NUMERIC_COLUMNS:
        return 0
    if column in {"upgrades_json", "source_numeric_facts_json"}:
        return "[]"
    if column in ECONOMIC_VALUATION_JSON_COLUMNS:
        return "{}"
    return "none"


def normalize_economic_valuation_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        normalized_row: dict[str, Any] = {}
        for column in ECONOMIC_VALUATION_CANONICAL_COLUMNS:
            value = row.get(column, _economic_valuation_default(column))
            if value is None or value == "":
                value = _economic_valuation_default(column)
            normalized_row[column] = value
        normalized.append(normalized_row)
    return normalized


ECONOMIC_VALUATION_SOURCE_FACT_COLUMNS = (
    "winning_load_position",
    "winning_mod_id",
    "winning_mod_name",
    "winning_file",
    "definition_count",
    "source_mods",
    "source_files",
    "source_numeric_facts_json",
    "source_numeric_facts_hash",
)


def fresh_economic_valuation_source_facts(
    rows: list[dict[str, Any]],
    playset: dict[str, Any] | None = None,
) -> dict[tuple[str, str], dict[str, Any]]:
    playset = build_active_playset_snapshot() if playset is None else playset
    roots = [Path(item["root"]) for item in _valuation_stack_roots(playset)]
    variables = collect_global_variables(roots)
    wanted: dict[str, set[str]] = {}
    for row in rows:
        object_type = str(row.get("object_type", ""))
        object_id = str(row.get("object_id", ""))
        if object_type in ECONOMIC_VALUATION_SOURCE_FOLDERS and object_id:
            wanted.setdefault(object_type, set()).add(object_id)
    definitions: list[dict[str, Any]] = []
    for root_info in _valuation_stack_roots(playset):
        root = Path(root_info["root"])
        common = root / "common"
        if not common.exists():
            continue
        for object_type, folder in ECONOMIC_VALUATION_SOURCE_FOLDERS.items():
            wanted_ids = wanted.get(object_type)
            if not wanted_ids:
                continue
            folder_path = common / folder
            if not folder_path.exists():
                continue
            for file_path in iter_text_files(folder_path):
                if file_path.name.startswith(DATASET_JOB_PRESSURE_FILE_PREFIX):
                    continue
                try:
                    parsed = parse_file(file_path)
                except PDXParseError:
                    continue
                for assignment in block_assignments(parsed):
                    if assignment.key not in wanted_ids or not isinstance(assignment.value, PDXBlock):
                        continue
                    definitions.append(
                        {
                            **root_info,
                            "object_type": object_type,
                            "object_id": assignment.key,
                            "source_file": str(file_path),
                            "relative_file": str(file_path.relative_to(root)),
                            "parse_error": "",
                            "value": assignment.value,
                        }
                    )
    winners = _winning_economic_definitions(definitions)
    summaries = _economic_source_summary(definitions)
    facts: dict[tuple[str, str], dict[str, Any]] = {}
    for object_key, winner in winners.items():
        value = winner["value"]
        assert isinstance(value, PDXBlock)
        object_variables = _object_variables(winner, variables)
        summary = summaries[object_key]
        fact_row = {
            "object_type": object_key[0],
            "object_id": object_key[1],
            "winning_load_position": winner["load_position"],
            "winning_mod_id": winner["steam_id"],
            "winning_mod_name": winner["name"],
            "winning_file": winner["relative_file"],
            "definition_count": summary["source_count"],
            "source_mods": "|".join(dict.fromkeys(summary["source_mods"])),
            "source_files": "|".join(dict.fromkeys(summary["source_files"])),
            **_source_numeric_fact_columns(value, object_variables),
        }
        normalized_fact_row = normalize_economic_valuation_rows([fact_row])[0]
        facts[object_key] = {
            column: normalized_fact_row[column] for column in ECONOMIC_VALUATION_SOURCE_FACT_COLUMNS
        }
    return facts


def enrich_economic_valuation_rows_with_source_facts(
    rows: list[dict[str, Any]],
    playset: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    facts = fresh_economic_valuation_source_facts(rows, playset)
    enriched: list[dict[str, Any]] = []
    for row in rows:
        updated = dict(row)
        row_facts = facts.get((str(row.get("object_type", "")), str(row.get("object_id", ""))))
        if row_facts:
            updated.update(row_facts)
        enriched.append(updated)
    return normalize_economic_valuation_rows(enriched)


def economic_valuation_dataset_summary(rows: list[dict[str, Any]], playset: dict[str, Any]) -> str:
    by_type: dict[str, int] = {}
    flagged: dict[str, int] = {}
    top_roi = sorted(
        [row for row in rows if row["object_type"] != "parse_error"],
        key=lambda row: float(row["roi_2250_to_2350_estimate"]),
        reverse=True,
    )[:25]
    for row in rows:
        by_type[row["object_type"]] = by_type.get(row["object_type"], 0) + 1
        for flag in str(row["data_quality_flags"]).split("|"):
            if flag:
                flagged[flag] = flagged.get(flag, 0) + 1
    type_lines = "\n".join(f"- {key}: {value}" for key, value in sorted(by_type.items()))
    flag_lines = "\n".join(f"- {key}: {value}" for key, value in sorted(flagged.items()))
    top_lines = "\n".join(
        f"- {row['object_type']} `{row['object_id']}` from {row['winning_mod_name']}: "
        f"ROI@2250={row['roi_2250_to_2350_estimate']}, jobs={row['jobs_created_total_estimate']}, "
        f"flags={row['data_quality_flags'] or 'none'}"
        for row in top_roi
    )
    return f"""# Stellar AI Director Economic Valuation Dataset

Generated: {datetime.now(timezone.utc).isoformat()}

This dataset is the required evidence gate before generating new late-game unemployment or construction-pressure weights. It mines the active Irony stack plus vanilla for planet `buildings`, `zones`, and `districts`, records the top-level load winner, and computes rough long-horizon ROI against the 2350 target end date.

Important limitations:

- ROI is a rough planning number, not a game simulation.
- Explicit `ai_resource_production` and direct production are valued directly.
- Stellaris 4.x job modifiers use workforce units, normalized here as `{JOB_WORKFORCE_UNITS:g}` workforce per full job equivalent before valuation.
- Job-only objects use `{GENERIC_JOB_MONTHLY_VALUE}` value per normalized job per month because final job output depends on empire, species, designation, buildings, and modifiers.
- Modifier-only objects use a conservative key-count proxy and are flagged for review.
- Inline scripts and unresolved variables are flagged so later weight generation can prefer high-confidence rows or require manual review.

Active collection: {playset.get('collection_name', '')}
Active mod count: {playset.get('mod_count', 0)}

## Row Counts

{type_lines}

## Data Quality Flags

{flag_lines}

## Highest Rough ROI At 2250 Horizon

{top_lines}
"""


def build_economic_valuation_dataset(
    playset: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Build the current valuation rows without updating checked artifacts."""

    if playset is None:
        playset = build_active_playset_snapshot()
    return enrich_economic_valuation_rows_with_source_facts(
        build_economic_valuation_rows(playset),
        playset,
    )


def generate_economic_valuation_dataset() -> list[dict[str, Any]]:
    playset = build_active_playset_snapshot()
    rows = build_economic_valuation_dataset(playset)
    write_csv(ECONOMIC_VALUATION_DATASET_CSV, rows)
    write_text_file_preserving_generated_timestamp(
        ECONOMIC_VALUATION_DATASET_MD, economic_valuation_dataset_summary(rows, playset)
    )
    return rows


def normalize_economic_valuation_dataset_file(path: Path) -> None:
    rows, _ = _read_economic_valuation_csv_rows(path)
    if rows:
        write_csv(path, enrich_economic_valuation_rows_with_source_facts(rows))


def normalize_nonconstruction_economic_valuation_dataset_file(path: Path) -> None:
    rows, _ = _read_economic_valuation_csv_rows(path)
    if not rows:
        return
    rows = [row for row in rows if row.get("object_type") != "resource"]
    rows.extend(build_nonconstruction_resource_rows())
    facts = fresh_economic_valuation_source_facts(rows)
    current_rows = [
        row
        for row in rows
        if row.get("object_type") not in ECONOMIC_VALUATION_SOURCE_FOLDERS
        or (str(row.get("object_type", "")), str(row.get("object_id", ""))) in facts
    ]
    enriched: list[dict[str, Any]] = []
    for row in current_rows:
        updated = dict(row)
        updated.update(facts.get((str(row.get("object_type", "")), str(row.get("object_id", ""))), {}))
        enriched.append(updated)
    write_csv(path, normalize_economic_valuation_rows(enriched))


def normalize_economic_valuation_dataset_pair() -> None:
    normalize_economic_valuation_dataset_file(ECONOMIC_VALUATION_DATASET_CSV)
    normalize_nonconstruction_economic_valuation_dataset_file(NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV)


def economic_valuation_dataset_passes(repo_root: Path = REPO_ROOT) -> bool:
    csv_path = repo_root / ECONOMIC_VALUATION_DATASET_CSV.relative_to(REPO_ROOT)
    if not csv_path.exists():
        return False
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    required_columns = {
        "object_type",
        "object_id",
        "winning_mod_name",
        "winning_file",
        "build_cost_json",
        "upkeep_json",
        "jobs_created_json",
        "direct_monthly_output_json",
        "modifier_keys",
        "ai_state_json",
        "prerequisites_json",
        "data_quality_flags",
        "roi_2250_to_2350_estimate",
    }
    fieldnames = set(reader.fieldnames or [])
    if not rows or not required_columns.issubset(fieldnames):
        return False
    if fieldnames != set(ECONOMIC_VALUATION_CANONICAL_COLUMNS):
        return False
    if any(any(row.get(column, "") == "" for column in ECONOMIC_VALUATION_CANONICAL_COLUMNS) for row in rows):
        return False
    object_types = {row["object_type"] for row in rows}
    if object_types - CONSTRUCTION_ECONOMIC_OBJECT_TYPES:
        return False
    if not CONSTRUCTION_ECONOMIC_OBJECT_TYPES.issubset(object_types):
        return False
    if not any(row["winning_mod_id"] == "1121692237" and row["object_type"] in {"building", "district"} for row in rows):
        return False
    if not any(row["winning_mod_id"] == "2648658105" and row["object_type"] == "building" for row in rows):
        return False
    if not any(float(row["jobs_created_total_estimate"] or 0) > 0 for row in rows):
        return False
    if not any(float(row["roi_2250_to_2350_estimate"] or 0) > 0 for row in rows):
        return False
    return True


CONSTRUCTION_ECONOMIC_OBJECT_TYPES = {"building", "zone", "district"}
NONCONSTRUCTION_ECONOMIC_OBJECT_TYPES = {
    "ascension_perk",
    "colony_type",
    "decision",
    "deposit",
    "edict",
    "policy",
    "pop_job",
    "resource",
    "starbase_building",
    "starbase_module",
    "technology",
    "tradition",
}
EXCLUDED_NONCONSTRUCTION_OBJECT_TYPES = CONSTRUCTION_ECONOMIC_OBJECT_TYPES | {"megastructure"}
SHARED_ECONOMIC_VALUATION_COLUMNS = {
    "object_type",
    "object_id",
    "winning_mod_name",
    "winning_file",
    "build_cost_json",
    "upkeep_json",
    "direct_monthly_output_json",
    "modifier_keys",
    "ai_state_json",
    "data_quality_flags",
    "roi_2250_to_2350_estimate",
}
ECONOMIC_VALUATION_EXTRA_COLUMNS = (
    "source_numeric_facts_json",
    "source_numeric_facts_hash",
    "top_level_keys",
    "nested_resources_blocks",
    "nested_ai_weight_blocks",
    "nested_modifier_blocks",
    "referenced_unlocks_or_flags",
    "referenced_technologies",
    "referenced_deposits",
    "referenced_jobs_or_modifiers",
)
ECONOMIC_VALUATION_CANONICAL_COLUMNS = (
    "object_type",
    "object_id",
    "winning_load_position",
    "winning_mod_id",
    "winning_mod_name",
    "winning_file",
    "definition_count",
    "source_mods",
    "source_files",
    "category",
    "build_cost_json",
    "build_cost_value_estimate",
    "upkeep_json",
    "monthly_upkeep_value_estimate",
    "jobs_created_json",
    "jobs_created_total_estimate",
    "direct_monthly_output_json",
    "direct_monthly_output_value_estimate",
    "modifier_keys",
    "modifier_monthly_value_estimate",
    "gross_monthly_value_estimate",
    "net_monthly_value_estimate",
    "roi_2200_to_2350_estimate",
    "roi_2250_to_2350_estimate",
    "roi_2300_to_2350_estimate",
    "roi_2325_to_2350_estimate",
    "upgrades_json",
    "ai_state_json",
    "prerequisites_json",
    "modifiers_json",
    "building_zone_district_sets_json",
    "data_quality_flags",
    "unresolved_variables",
    *ECONOMIC_VALUATION_EXTRA_COLUMNS,
)
ECONOMIC_VALUATION_JSON_COLUMNS = {
    "build_cost_json",
    "upkeep_json",
    "jobs_created_json",
    "direct_monthly_output_json",
    "source_numeric_facts_json",
    "ai_state_json",
    "prerequisites_json",
    "modifiers_json",
    "building_zone_district_sets_json",
}
ECONOMIC_VALUATION_NUMERIC_COLUMNS = {
    "winning_load_position",
    "definition_count",
    "build_cost_value_estimate",
    "monthly_upkeep_value_estimate",
    "jobs_created_total_estimate",
    "direct_monthly_output_value_estimate",
    "modifier_monthly_value_estimate",
    "gross_monthly_value_estimate",
    "net_monthly_value_estimate",
    "roi_2200_to_2350_estimate",
    "roi_2250_to_2350_estimate",
    "roi_2300_to_2350_estimate",
    "roi_2325_to_2350_estimate",
    "nested_resources_blocks",
    "nested_ai_weight_blocks",
    "nested_modifier_blocks",
}


def _read_economic_valuation_csv_rows(path: Path) -> tuple[list[dict[str, str]], set[str]]:
    if not path.exists():
        return ([], set())
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return (list(reader), set(reader.fieldnames or []))


def nonconstruction_economic_valuation_dataset_passes(repo_root: Path = REPO_ROOT) -> bool:
    csv_path = repo_root / NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.relative_to(REPO_ROOT)
    rows, fieldnames = _read_economic_valuation_csv_rows(csv_path)
    if not rows or not SHARED_ECONOMIC_VALUATION_COLUMNS.issubset(fieldnames):
        return False
    if fieldnames != set(ECONOMIC_VALUATION_CANONICAL_COLUMNS):
        return False
    if any(any(row.get(column, "") == "" for column in ECONOMIC_VALUATION_CANONICAL_COLUMNS) for row in rows):
        return False
    object_types = {row["object_type"] for row in rows}
    if object_types & EXCLUDED_NONCONSTRUCTION_OBJECT_TYPES:
        return False
    if not object_types.issubset(NONCONSTRUCTION_ECONOMIC_OBJECT_TYPES):
        return False
    required_present = {
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
    }
    if not required_present.issubset(object_types):
        return False
    if not any(float(row["roi_2250_to_2350_estimate"] or 0) > 0 for row in rows):
        return False
    return True


def economic_valuation_evidence_passes(repo_root: Path = REPO_ROOT) -> bool:
    return economic_valuation_dataset_passes(repo_root) and nonconstruction_economic_valuation_dataset_passes(repo_root)


def economic_valuation_evidence_summary(repo_root: Path = REPO_ROOT) -> str:
    construction_rows, _ = _read_economic_valuation_csv_rows(
        repo_root / ECONOMIC_VALUATION_DATASET_CSV.relative_to(REPO_ROOT)
    )
    nonconstruction_rows, _ = _read_economic_valuation_csv_rows(
        repo_root / NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.relative_to(REPO_ROOT)
    )

    def counts(rows: list[dict[str, str]]) -> dict[str, int]:
        result: dict[str, int] = {}
        for row in rows:
            object_type = row.get("object_type", "")
            result[object_type] = result.get(object_type, 0) + 1
        return result

    construction_counts = counts(construction_rows)
    nonconstruction_counts = counts(nonconstruction_rows)
    combined_counts = counts([*construction_rows, *nonconstruction_rows])
    missing_nonconstruction_types = sorted(NONCONSTRUCTION_ECONOMIC_OBJECT_TYPES - set(nonconstruction_counts))
    construction_lines = "\n".join(f"- {key}: {value}" for key, value in sorted(construction_counts.items()))
    nonconstruction_lines = "\n".join(f"- {key}: {value}" for key, value in sorted(nonconstruction_counts.items()))
    combined_lines = "\n".join(f"- {key}: {value}" for key, value in sorted(combined_counts.items()))
    missing_line = ", ".join(missing_nonconstruction_types) if missing_nonconstruction_types else "none"
    return f"""# Stellar AI Director Economic Valuation Evidence

Generated: {datetime.now(timezone.utc).isoformat()}

This is the merged evidence index for economic AI decisions. The construction dataset owns planet-local construction surfaces. The companion nonconstruction dataset owns the rest of the economy-facing AI surfaces and intentionally does not duplicate buildings, zones, districts, or megastructures.

Validation contract:

- Construction dataset: `{ECONOMIC_VALUATION_DATASET_CSV.relative_to(REPO_ROOT).as_posix()}`
- Nonconstruction dataset: `{NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.relative_to(REPO_ROOT).as_posix()}`
- Both datasets must expose the shared source, cost/upkeep/output, AI-state, data-quality, and 2350-horizon ROI columns.
- The nonconstruction dataset must not include `building`, `zone`, `district`, or `megastructure` rows.
- Future economic weight generation should query both datasets together, then choose eligible objects by `object_type`, ROI horizon, affordability, AI-state gap, and data-quality flags.

## Construction Dataset Counts

{construction_lines}

## Nonconstruction Dataset Counts

{nonconstruction_lines}

Configured nonconstruction object types not present in the current file: {missing_line}

## Combined Counts

{combined_lines}
"""


def write_economic_valuation_evidence_summary() -> None:
    write_text_file_preserving_generated_timestamp(ECONOMIC_VALUATION_EVIDENCE_MD, economic_valuation_evidence_summary())


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
    for mod_id, expected_name in ATLAS_SOURCE_MODS.items():
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
    for mod_id, expected_name in ATLAS_SOURCE_MODS.items():
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


def atlas_object_has_ai_signal(value: PDXValue, object_type: str) -> bool:
    """Classify actual AI choice support without mistaking nested swap weights for it."""
    if not isinstance(value, PDXBlock):
        return False
    if object_type == "tradition":
        return any(assignment.key == "ai_weight" for assignment in block_assignments(value))
    return block_has_any_assignment(value, ATLAS_AI_SIGNAL_KEYS)


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
    has_ai_signal = atlas_object_has_ai_signal(value, object_type)
    support_status = parent_ai_support_status("yes" if has_ai_signal else "no", strategic_role)
    route_ids = object_route_ids(object_id, object_type)
    director_action = director_action_for_object(object_type, strategic_role, support_status)
    return {
        "object_id": object_id,
        "object_type": object_type,
        "mod_id": root["mod_id"],
        "mod_name": root["mod_name"],
        "source_file": source_file,
        "load_winner": load_winner,
        "source_has_ai_weight": "yes" if has_ai_signal else "no",
        "ai_weight_summary": "ai_signal_present" if has_ai_signal else "",
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


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = fieldnames or (list(rows[0].keys()) if rows else [])
    temp_path = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    with temp_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    for attempt in range(5):
        try:
            temp_path.replace(path)
            return
        except PermissionError:
            if attempt == 4:
                raise
            time.sleep(0.25 * (attempt + 1))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = normalize_text_file_content(text)
    path.write_text(normalized, encoding="utf-8", newline="\n")


def normalize_text_file_content(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()).rstrip("\n") + "\n"


GENERATED_TIMESTAMP_RE = re.compile(r"(?m)^Generated: .+$")


def write_text_file_preserving_generated_timestamp(path: Path, text: str) -> None:
    normalized = normalize_text_file_content(text)
    if path.exists():
        existing = normalize_text_file_content(path.read_text(encoding="utf-8"))
        existing_without_stamp = GENERATED_TIMESTAMP_RE.sub("Generated: <preserved>", existing, count=1)
        next_without_stamp = GENERATED_TIMESTAMP_RE.sub("Generated: <preserved>", normalized, count=1)
        match = GENERATED_TIMESTAMP_RE.search(existing)
        if match and existing_without_stamp == next_without_stamp:
            normalized = GENERATED_TIMESTAMP_RE.sub(match.group(0), normalized, count=1)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(normalized, encoding="utf-8", newline="\n")


def mod_source_root_for_id(mod_id: str, snapshot_root: Path = SNAPSHOT_ROOT) -> Path:
    if mod_id == "vanilla":
        return STELLARIS_INSTALL_ROOT
    manifest = read_snapshot_manifest(snapshot_root)
    row = manifest.get(mod_id)
    if row:
        return Path(row["snapshot_path"])
    workshop_root = Path(r"C:\Steam\steamapps\workshop\content\281990") / mod_id
    if workshop_root.exists():
        return workshop_root
    raise ValueError(f"No source snapshot or live Workshop folder found for mod id {mod_id}")


def write_stellarai_inline_script_dependencies() -> None:
    source_root = mod_source_root_for_id("3610149307")
    source_dir = source_root / "common" / "inline_scripts" / "stellarai"
    target_dir = MOD_ROOT / "common" / "inline_scripts" / "stellarai"
    for script_name in STELLARAI_INLINE_SCRIPT_DEPENDENCIES:
        source_path = source_dir / f"{script_name}.txt"
        if not source_path.exists():
            raise FileNotFoundError(f"Missing Stellar AI inline script dependency: {source_path}")
        write_text_file(target_dir / source_path.name, read_text(source_path))


SFT_EQUIVALENCE_TEXT_FILES = (
    "common/component_sets/00_SFT_weapon_set.txt",
    "common/component_tags/SFT_component_tags.txt",
    "common/component_templates/000_SFT_00_biogenesis_utilities_roles.txt",
    "common/component_templates/000_SFT_00_biogenesis_weapons_autocannon.txt",
    "common/component_templates/000_SFT_00_biogenesis_weapons_weaver.txt",
    "common/component_templates/000_SFT_00_utilities_roles.txt",
    "common/component_templates/000_SFT_00_utilities_roles_space_fauna.txt",
    "common/component_templates/000_SFT_00_weapons_extra_large_kinetic.txt",
    "common/component_templates/000_SFT_00_weapons_missiles.txt",
    "common/component_templates/000_SFT_00_weapons_projectile.txt",
    "common/component_templates/000_SFT_COMP.txt",
    "common/component_templates/zzz_SFT_GE_ehof_computer_max.txt",
    "common/scripted_modifiers/00_SFT_scripted_modifiers.txt",
    "common/scripted_triggers/zz_SFTt_ACTIVATED.txt",
    "common/scripted_triggers/zz_SFTt_FLEET_NONCOMBAT_REPAIR.txt",
    "common/scripted_triggers/zz_SFTt_SHIP_COMBAT_RANGE.txt",
    "common/scripted_triggers/zz_SFTt_SHIP_DESIGN.txt",
    "common/scripted_triggers/zz_SFTt_SHIP_DESIGN_AIP.txt",
    "common/scripted_triggers/zz_SFTt_SHIP_DESIGN_PrE.txt",
    "common/scripted_triggers/zz_SFTt_SHIP_HAS_COMPO.txt",
    "common/scripted_triggers/zz_SFTt_SHIP_MARINE.txt",
    "common/scripted_triggers/zz_SFTt_SHIP_SIZE.txt",
    "common/scripted_triggers/zz_SFTt_SHIP_USE_ROLES.txt",
    "common/ship_behaviors/000_SFT_behaviors.txt",
    "common/ship_behaviors/000_SFT_behaviors_others.txt",
    "common/ship_behaviors/000_SFT_strike_craft.txt",
    "common/static_modifiers/00_SFTm_ship_speed.txt",
    "common/static_modifiers/00_SFTm_special_component.txt",
    "events/SFT_event_ship_design.txt",
)

SFT_EQUIVALENCE_DIRS = (
    "common/inline_scripts/esc_computers",
    "common/inline_scripts/ship_components",
    "common/inline_scripts/ship_design",
    "common/scripted_variables",
)

SFT_ADDON_EQUIVALENCE_TEXT = """# Generated by tools/generate_stellar_ai_director_patch.py.
# Spacefleet Tactica add-on equivalence for the active playset:
# - SFT ADD-ON : Disable New Ship Sections
# - SFT ADD-ON : Combat Computer Restriction Removal

SFTt_ADDON_NEW_SECTION_USE = { always = no }
SFTt_ADDON_COMBAT_DECEL_USE = { always = yes }
SFTt_ADDON_FF_SP_ACTIVATED = { always = no }
SFTt_ADDON_COMBAT_COM_REST_REMOVED = { always = yes }
"""

SFT_DESIGN_REFRESH_ON_ACTION_TEXT = """# Generated by tools/generate_stellar_ai_director_patch.py.
# SFT+add-ons equivalence: sections are disabled, so only the decade auto-design refresh path remains.

on_decade_pulse = {
\tevents = {
\t\tSFT_event_ship_design.400
\t}
}
"""


def iter_sft_equivalence_sources(source_root: Path) -> Iterable[tuple[Path, Path]]:
    for relative in SFT_EQUIVALENCE_TEXT_FILES:
        path = Path(relative)
        yield source_root / path, MOD_ROOT / path
    for relative_dir in SFT_EQUIVALENCE_DIRS:
        source_dir = source_root / relative_dir
        if not source_dir.exists():
            raise FileNotFoundError(f"Missing SFT source directory: {source_dir}")
        for source_path in sorted(source_dir.glob("*.txt")):
            yield source_path, MOD_ROOT / relative_dir / source_path.name


def write_sft_equivalence_files() -> list[dict[str, str]]:
    source_root = mod_source_root_for_id("3696204283")
    rows: list[dict[str, str]] = []
    for source_path, target_path in iter_sft_equivalence_sources(source_root):
        if not source_path.exists():
            raise FileNotFoundError(f"Missing SFT equivalence source: {source_path}")
        ownership_header = (
            "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
            "# Full-object override ownership: copied from the pinned Spacefleet Tactica equivalence source.\n\n"
        )
        write_text_file(target_path, ownership_header + read_text(source_path))
        rows.append(
            {
                "source": source_path.relative_to(source_root).as_posix(),
                "target": target_path.relative_to(MOD_ROOT).as_posix(),
                "status": "copied",
                "reason": "SFT ship build/combat-computer equivalence surface; section templates intentionally excluded",
            }
        )
    addon_target = MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_sft_addon_equivalence.txt"
    on_action_target = MOD_ROOT / "common" / "on_actions" / "zzzz_staid_sft_design_refresh_on_actions.txt"
    write_text_file(addon_target, SFT_ADDON_EQUIVALENCE_TEXT)
    write_text_file(on_action_target, SFT_DESIGN_REFRESH_ON_ACTION_TEXT)
    rows.extend(
        [
            {
                "source": "SFT add-ons 3703611846 + 3726506420",
                "target": addon_target.relative_to(MOD_ROOT).as_posix(),
                "status": "generated",
                "reason": "matches active add-ons: disable SFT sections and remove combat-computer restrictions",
            },
            {
                "source": "SFT on_decade_pulse ship-design refresh path",
                "target": on_action_target.relative_to(MOD_ROOT).as_posix(),
                "status": "generated",
                "reason": "retains SFT design refresh without copying section unlock or auto-research hooks",
            },
        ]
    )
    write_csv(SFT_EQUIVALENCE_AUDIT_CSV, rows)
    write_text_file(SFT_EQUIVALENCE_AUDIT_MD, sft_equivalence_audit_text(rows))
    return rows


def sft_equivalence_audit_text(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Stellar AI Director Spacefleet Tactica Equivalence Audit",
        "",
        "Generated 2026-07-09. Runtime testing was out of scope; this file records static SFT+add-on logic mirrored into the Director.",
        "",
        "Included: SFT combat-computer/component-role templates, component sets/tags, role and ship-design triggers, ship behaviors, inline scripts required by copied templates, and the decade ship-design refresh event path.",
        "",
        "Active add-on semantics: `SFT ADD-ON : Disable New Ship Sections` is represented by `SFTt_ADDON_NEW_SECTION_USE = no`; `SFT ADD-ON : Combat Computer Restriction Removal` is represented by `SFTt_ADDON_COMBAT_COM_REST_REMOVED = yes`.",
        "",
        "Excluded: SFT section templates, SFT section/AI auto-research hooks, and the full SFT on_action bundle. The active add-on `SFT ADD-ON : Disable New Ship Sections` makes those section surfaces logically inactive.",
        "",
        "| source | target | status | reason |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| `{row['source']}` | `{row['target']}` | {row['status']} | {row['reason']} |")
    return "\n".join(lines) + "\n"


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


def append_child_block_clause(
    block_text: str,
    child_key: str,
    clause_text: str,
    *,
    parent_depth: int = 1,
) -> str:
    """Append a clause inside a named child block without replacing source logic."""
    lines = block_text.rstrip().splitlines()
    child_pattern = re.compile(rf"^[ \t]*{re.escape(child_key)}[ \t]*=")
    depth = 0
    child_start = -1
    for index, line in enumerate(lines):
        if depth == parent_depth and child_pattern.match(line):
            child_start = index
            break
        depth += _brace_delta(line)
    if child_start < 0:
        raise ValueError(f"Could not find child block {child_key} at depth {parent_depth}")

    child_depth = depth + _brace_delta(lines[child_start])
    if child_depth <= parent_depth:
        raise ValueError(f"Child block {child_key} must span multiple lines")
    for index in range(child_start + 1, len(lines)):
        next_depth = child_depth + _brace_delta(lines[index])
        if child_depth == parent_depth + 1 and next_depth == parent_depth:
            lines[index:index] = clause_text.rstrip().splitlines()
            return "\n".join(lines) + "\n"
        child_depth = next_depth
    raise ValueError(f"Could not find closing brace for child block {child_key}")


def remove_top_level_child_block(block_text: str, child_key: str) -> str:
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
    return "\n".join(output) + "\n"


def merge_duplicate_top_level_child_blocks(block_text: str, child_key: str) -> str:
    lines = block_text.rstrip().splitlines()
    output: list[str] = []
    blocks: list[list[str]] = []
    depth = 0
    index = 0
    child_pattern = re.compile(rf"^[ \t]*{re.escape(child_key)}[ \t]*=")
    while index < len(lines):
        line = lines[index]
        if depth == 1 and child_pattern.match(line):
            block_lines = [line]
            depth += _brace_delta(line)
            index += 1
            while index < len(lines) and depth > 1:
                block_lines.append(lines[index])
                depth += _brace_delta(lines[index])
                index += 1
            blocks.append(block_lines)
            continue
        output.append(line)
        depth += _brace_delta(line)
        index += 1
    if len(blocks) <= 1:
        return block_text

    merged = [f"\t{child_key} = {{"]
    for block_lines in blocks:
        merged.extend(block_lines[1:-1])
    merged.append("\t}")
    closing_index = len(output) - 1
    while closing_index >= 0 and not re.match(r"^[ \t]*}\s*$", output[closing_index]):
        closing_index -= 1
    if closing_index < 0:
        raise ValueError("Generated block has no final closing brace")
    output[closing_index:closing_index] = ["", *merged]
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


def insert_top_level_child_modifier(
    block_text: str,
    child_key: str,
    modifier_text: str,
) -> str:
    """Insert a modifier immediately before a top-level child block closes."""
    if modifier_text in block_text:
        return block_text
    lines = block_text.rstrip().splitlines()
    output: list[str] = []
    depth = 0
    index = 0
    child_pattern = re.compile(
        rf"^[ \t]*{re.escape(child_key)}[ \t]*=",
        re.IGNORECASE,
    )
    inserted = False
    while index < len(lines):
        line = lines[index]
        if depth == 1 and child_pattern.match(line):
            output.append(line)
            depth += _brace_delta(line)
            index += 1
            child_lines: list[str] = []
            while index < len(lines) and depth > 1:
                current = lines[index]
                next_depth = depth + _brace_delta(current)
                if next_depth == 1 and current.strip() == "}":
                    child_lines.extend(modifier_text.rstrip().splitlines())
                    inserted = True
                child_lines.append(current)
                depth = next_depth
                index += 1
            output.extend(child_lines)
            continue
        output.append(line)
        depth += _brace_delta(line)
        index += 1
    if not inserted:
        raise ValueError(f"Generated block has no top-level {child_key} block")
    return "\n".join(output) + "\n"


def insert_top_level_ai_weight_modifier(block_text: str, modifier_line: str) -> str:
    """Compatibility wrapper for existing policy-generation callers."""
    try:
        return insert_top_level_child_modifier(block_text, "ai_weight", modifier_line)
    except ValueError:
        # Some source objects genuinely have no AI weight. Preserve the historic
        # fallback rather than silently dropping the requested policy signal.
        lines = block_text.rstrip().splitlines()
        closing_index = len(lines) - 1
        while closing_index >= 0 and not re.match(r"^[ \t]*}\s*$", lines[closing_index]):
            closing_index -= 1
        if closing_index < 0:
            raise ValueError("Generated block has no final closing brace for ai_weight insertion")
        lines[closing_index:closing_index] = [
            "\tai_weight = {",
            "\t\tfactor = 1",
            modifier_line,
            "\t}",
        ]
        return "\n".join(lines) + "\n"



def insert_top_level_ai_weight_modifiers(block_text: str, modifier_lines: list[str]) -> str:
    for modifier_line in modifier_lines:
        block_text = insert_top_level_ai_weight_modifier(block_text, modifier_line)
    return block_text


def research_federation_weight_block(block_text: str) -> str:
    modifiers = [
        "\t\t# staid_research_diplomacy_core = verified Research Cooperative preference",
        "\t\tmodifier = { add = 250 desc = staid_research_diplomacy_core from = { staid_research_diplomacy_priority_ready = yes } }",
        "\t\tmodifier = { add = 175 desc = staid_science_snowball from = { staid_science_nexus_research_priority_ready = yes } }",
        "\t\tmodifier = { add = 125 desc = staid_research_runway from = { staid_research_input_runway_safe = yes } }",
        "\t\tmodifier = { add = 90 desc = staid_materialist_research from = { OR = { has_ethic = ethic_materialist has_ethic = ethic_fanatic_materialist has_authority = auth_machine_intelligence } } }",
        "\t\tmodifier = { add = 70 desc = staid_discovery_federation from = { has_active_tradition = tr_discovery_federations_finish } }",
        "\t\tmodifier = { add = -80 desc = staid_conquest_route_prefers_other_federation from = { staid_aggressive_fleet_pressure = yes NOT = { staid_research_diplomacy_priority_ready = yes } } }",
        "\t\tmodifier = { add = -60 desc = staid_spiritualist_research_federation_drift from = { OR = { has_ethic = ethic_spiritualist has_ethic = ethic_fanatic_spiritualist } NOT = { staid_research_diplomacy_priority_ready = yes } } }",
    ]
    return insert_top_level_ai_weight_modifiers(block_text, modifiers)


def find_verified_source_object_block(common_folder: str, object_id: str, mod_id: str = "vanilla") -> str:
    source_root = mod_source_root_for_id(mod_id)
    folder_root = source_root / "common" / common_folder
    if not folder_root.exists():
        raise ValueError(f"Missing source folder for {mod_id}:{common_folder}")
    object_pattern = re.compile(rf"(?m)^[ \t]*{re.escape(object_id)}[ \t]*=[ \t]*\{{")
    for path in iter_text_files(folder_root):
        text = read_text(path)
        if not object_pattern.search(text):
            continue
        block = extract_top_level_object_text(text, object_id)
        parse_pdx(block)
        return block
    raise ValueError(f"Could not find verified source object {object_id} in {mod_id}:{common_folder}")


def insert_policy_option_ai_weight_modifier(block_text: str, option_name: str, modifier_line: str) -> str:
    # Deduplicate within the target option, not across the whole policy object.
    # Several options intentionally receive the same boxed-in/war-posture rule.
    lines = block_text.rstrip().splitlines()
    output: list[str] = []
    depth = 0
    index = 0
    option_pattern = re.compile(r"^[ \t]*option[ \t]*=[ \t]*\{")
    name_pattern = re.compile(rf'^[ \t]*name[ \t]*=[ \t]*"?{re.escape(option_name)}"?[ \t]*(?:#.*)?$')
    inserted = False
    while index < len(lines):
        line = lines[index]
        if depth == 1 and option_pattern.match(line):
            option_lines = [line]
            option_depth = depth + _brace_delta(line)
            index += 1
            while index < len(lines) and option_depth > 1:
                current = lines[index]
                option_lines.append(current)
                option_depth += _brace_delta(current)
                index += 1
            option_text = "\n".join(option_lines) + "\n"
            if any(name_pattern.match(option_line) for option_line in option_lines):
                option_text = insert_top_level_ai_weight_modifier(option_text, modifier_line)
                inserted = True
            output.extend(option_text.rstrip().splitlines())
            depth = 1
            continue
        output.append(line)
        depth += _brace_delta(line)
        index += 1
    if not inserted:
        raise ValueError(f"Could not find policy option {option_name}")
    return "\n".join(output) + "\n"


def replace_policy_option_ai_weight(block_text: str, option_name: str, ai_weight_text: str) -> str:
    lines = block_text.rstrip().splitlines()
    output: list[str] = []
    depth = 0
    index = 0
    option_pattern = re.compile(r"^[ \t]*option[ \t]*=[ \t]*\{")
    name_pattern = re.compile(rf'^[ \t]*name[ \t]*=[ \t]*"?{re.escape(option_name)}"?[ \t]*(?:#.*)?$')
    replaced = False
    while index < len(lines):
        line = lines[index]
        if depth == 1 and option_pattern.match(line):
            option_lines = [line]
            option_depth = depth + _brace_delta(line)
            index += 1
            while index < len(lines) and option_depth > 1:
                current = lines[index]
                option_lines.append(current)
                option_depth += _brace_delta(current)
                index += 1
            option_text = "\n".join(option_lines) + "\n"
            if any(name_pattern.match(option_line) for option_line in option_lines):
                option_text = replace_top_level_child_block(option_text, "ai_weight", ai_weight_text)
                replaced = True
            output.extend(option_text.rstrip().splitlines())
            depth = 1
            continue
        output.append(line)
        depth += _brace_delta(line)
        index += 1
    if not replaced:
        raise ValueError(f"Could not find policy option {option_name}")
    return "\n".join(output) + "\n"


def director_infrastructure_weight_block(block: str, target: dict[str, Any]) -> str:
    coefficient = str(target.get("coefficient", "4"))
    additional_weight = str(target.get("additional_weight", "400"))
    block = replace_or_insert_top_level_scalar(block, "ai_weight_coefficient", f"\tai_weight_coefficient = {coefficient}")
    block = replace_or_insert_top_level_scalar(
        block,
        "additional_ai_weight",
        f"\tadditional_ai_weight = {additional_weight}",
    )
    route_gate = route_gate_for_target(target)
    block = insert_top_level_ai_weight_modifier(
        block,
        f"\t\tmodifier = {{ factor = 0 owner = {{ NOT = {{ {route_gate} = yes }} }} }}",
    )
    route_id = str(target.get("route_id", ""))
    if route_id == "research_throughput_infrastructure":
        for modifier in (
            "\t\tmodifier = { factor = 8 has_designation = col_research }",
            "\t\tmodifier = { factor = 6 has_designation = col_habitat_research }",
            "\t\tmodifier = { factor = 6 has_designation = col_ring_research }",
            "\t\tmodifier = { factor = 6 has_designation = col_ecu_research }",
            "\t\tmodifier = { factor = 5 has_designation = col_nomad_research }",
            "\t\tmodifier = { factor = 14 owner = { staid_research_under_curve = yes } }",
            "\t\tmodifier = { factor = 10 owner = { years_passed > 79 staid_research_under_curve = yes } }",
            "\t\tmodifier = { factor = 8 owner = { staid_opening_route_research_priority = yes } }",
            "\t\tmodifier = { factor = 8 owner = { staid_surplus_sink_pressure = yes } }",
            "\t\tmodifier = { factor = 6 owner = { staid_high_scale_snowball_pressure = yes } }",
            "\t\tmodifier = { factor = 4 owner = { years_passed > 44 } }",
            "\t\tmodifier = { factor = 3 free_building_slots > 0 }",
        ):
            block = insert_top_level_ai_weight_modifier(block, modifier)
    if target.get("object_id") == "district_hab_science":
        for modifier in (
            "\t\tmodifier = { factor = 8 has_designation = col_habitat_research }",
            "\t\tmodifier = { factor = 8 owner = { staid_research_under_curve = yes } }",
            "\t\tmodifier = { factor = 6 owner = { staid_planetary_capacity_growth_ready = yes } }",
            "\t\tmodifier = { factor = 5 owner = { years_passed > 79 staid_research_under_curve = yes } }",
        ):
            block = insert_top_level_ai_weight_modifier(block, modifier)
    elif route_id == "pop_assembly_snowball_core":
        object_id = str(target.get("object_id", ""))
        pop_assembly_modifiers = {
            "building_robot_assembly_plant": (
                "\t\tmodifier = { factor = 6 owner = { OR = { has_origin = origin_mechanists has_country_flag = synthetic_empire } } }",
                "\t\tmodifier = { factor = 4 owner = { is_materialist = yes } }",
            ),
            "building_robot_assembly_complex": (
                "\t\tmodifier = { factor = 6 owner = { OR = { has_origin = origin_mechanists has_country_flag = synthetic_empire } } }",
                "\t\tmodifier = { factor = 4 owner = { is_materialist = yes } }",
            ),
            "building_machine_assembly_plant": (
                "\t\tmodifier = { factor = 7 owner = { OR = { is_machine_empire = yes is_individual_machine = yes } } }",
            ),
            "building_machine_assembly_complex": (
                "\t\tmodifier = { factor = 7 owner = { OR = { is_machine_empire = yes is_individual_machine = yes } } }",
            ),
            "building_clone_vats": (
                "\t\tmodifier = { factor = 5 owner = { OR = { has_technology = tech_cloning has_cloning_tradition = yes } } }",
                "\t\tmodifier = { factor = 3 owner = { has_ascension_perk = ap_engineered_evolution } }",
            ),
            "building_spawning_pool": (
                "\t\tmodifier = { factor = 6 owner = { is_hive_empire = yes } }",
                "\t\tmodifier = { factor = 0 owner = { has_origin = origin_progenitor_hive } }",
            ),
            "building_offspring_nest": (
                "\t\tmodifier = { factor = 8 owner = { has_origin = origin_progenitor_hive } }",
            ),
        }
        for modifier in pop_assembly_modifiers.get(object_id, ()):
            block = insert_top_level_ai_weight_modifier(block, modifier)
    return block


DATASET_JOB_PRESSURE_OBJECT_LIMIT = 1200
DATASET_JOB_PRESSURE_REPAIR_FAMILY_LIMIT = 35
DATASET_JOB_PRESSURE_UNSAFE_TEXT_MARKERS = (
    "has_unemployed_pop_of_category",
    "district_giga_frameworld_fortress_bunker",
    "district_generator_uncapped",
)
DATASET_JOB_PRESSURE_FORBIDDEN_OBJECT_IDS = {
    "building_pd_rogue_council",
}
BUILD_PLAN_CONSUMABLE_STATUSES = {"yes", "conditional"}

AI_RESOURCE_PRODUCTION_FAMILY_DEFAULTS = {
    "consumer_goods_repair": ("consumer_goods",),
    "food_repair": ("food",),
    "alloy_scaling": ("alloys",),
    "research_scaling": ("physics_research", "society_research", "engineering_research"),
    "energy_scaling": ("energy",),
    "mineral_scaling": ("minerals",),
    "strategic_resource_scaling": (
        "volatile_motes",
        "exotic_gases",
        "rare_crystals",
        "sr_dark_matter",
        "sr_zro",
        "nanites",
    ),
    "general_job_pressure": ("energy", "minerals"),
}

AI_RESOURCE_PRODUCTION_RESOURCE_HINTS = (
    "energy",
    "minerals",
    "food",
    "alloys",
    "consumer_goods",
    "unity",
    "physics_research",
    "society_research",
    "engineering_research",
    "trade",
    "volatile_motes",
    "exotic_gases",
    "rare_crystals",
    "sr_dark_matter",
    "sr_zro",
    "nanites",
    "giga_sr_sentient_metal",
    "giga_sr_negative_mass",
    "giga_sr_amb_megaconstruction",
    "giga_sr_supertensiles",
)


def dataset_job_pressure_family(row: dict[str, Any]) -> str:
    text = " ".join(
        str(row.get(key, "")).lower()
        for key in (
            "object_id",
            "jobs_created_json",
            "direct_monthly_output_json",
            "modifier_keys",
            "category",
        )
    )
    if str(row.get("category", "")).lower() == "army" or any(
        token in text for token in ("naval", "soldier", "fortress", "stronghold", "military", "command_limit")
    ):
        return "military_capacity"
    if any(token in text for token in ("consumer_goods", "artisan", "factory", "industrial", "goods")):
        return "consumer_goods_repair"
    if any(token in text for token in ("food", "farmer", "agri")):
        return "food_repair"
    if any(token in text for token in ("alloys", "foundry", "forge", "metallurg")):
        return "alloy_scaling"
    if any(token in text for token in ("physics_research", "society_research", "engineering_research", "research", "scientist")):
        return "research_scaling"
    if any(token in text for token in ("energy", "technician", "generator")):
        return "energy_scaling"
    if any(token in text for token in ("minerals", "miner", "mining")):
        return "mineral_scaling"
    if any(token in text for token in ("volatile_motes", "exotic_gases", "rare_crystals", "sr_dark_matter", "sr_zro", "nanites")):
        return "strategic_resource_scaling"
    return "general_job_pressure"


def dataset_job_pressure_runtime_safety_issues(
    row: dict[str, Any],
    block: str,
    known_jobs: set[str],
) -> list[str]:
    text = "\n".join(
        str(row.get(key, ""))
        for key in (
            "ai_state_json",
            "prerequisites_json",
            "modifiers_json",
            "modifier_keys",
        )
    )
    text = f"{text}\n{block}"
    issues: list[str] = []
    for marker in DATASET_JOB_PRESSURE_UNSAFE_TEXT_MARKERS:
        if marker in text:
            issues.append(marker)
    if re.search(r"\$[A-Za-z0-9_]+\$", text):
        issues.append("unresolved_dollar_placeholder")
    if "TODO_CD" in text:
        issues.append("unresolved_todo_placeholder")
    if row.get("object_type") == "district" and re.search(r"\btrade_value_add\b", text):
        issues.append("district_trade_value_add")
    if re.search(r"\bbuilding_[a-z0-9_]+_max\b", text):
        issues.append("building_max_modifier")
    if row.get("object_id") in DATASET_JOB_PRESSURE_FORBIDDEN_OBJECT_IDS:
        issues.append("forbidden_object")
    valid_job_modifiers = {f"job_{job}_add" for job in known_jobs} | {f"{job}_add" for job in known_jobs}
    missing_jobs = sorted(
        {
            match.removesuffix("_add")
            for match in re.findall(r"\bjob_[A-Za-z0-9_]+_add\b", text)
            if match not in valid_job_modifiers
        }
    )
    if missing_jobs:
        issues.extend(f"missing_job:{job}" for job in missing_jobs[:8])
    return issues


def build_plan_consumer_policy_rows() -> list[dict[str, Any]]:
    return _read_csv_rows(BUILD_PLAN_CONSUMER_POLICY_CSV)


def build_plan_consumer_policy_buildings(rows: list[dict[str, Any]] | None = None) -> dict[str, dict[str, Any]]:
    policy_rows = rows if rows is not None else build_plan_consumer_policy_rows()
    return {
        str(row["object_id"]): row
        for row in policy_rows
        if row.get("row_family") == "building"
    }


def build_plan_consumer_policy_selected_object_rows(
    rows: list[dict[str, Any]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    policy_rows = rows if rows is not None else build_plan_consumer_policy_rows()
    selected: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in policy_rows:
        if row.get("row_family") != "role_target" or row.get("can_consume_now") != "yes":
            continue
        for item in str(row.get("selected_objects", "")).split("|"):
            item = item.strip()
            if item:
                selected[item].append(row)
    return selected


def build_plan_consumer_policy_selected_objects(rows: list[dict[str, Any]] | None = None) -> set[str]:
    return set(build_plan_consumer_policy_selected_object_rows(rows))


def build_plan_consumer_policy_allows_dataset_object(
    row: dict[str, Any],
    building_policy: dict[str, dict[str, Any]],
    selected_objects: set[str],
    selected_object_policy_rows: dict[str, list[dict[str, Any]]] | None = None,
) -> bool:
    object_type = str(row.get("object_type", ""))
    object_id = str(row.get("object_id", ""))
    if object_type == "building":
        policy = building_policy.get(object_id)
        return bool(
            policy
            and policy.get("can_consume_now") in BUILD_PLAN_CONSUMABLE_STATUSES
            and not build_plan_consumer_policy_excludes_dataset_object(row, policy)
        )
    if object_type == "district":
        token = f"{object_type}:{object_id}"
        if token not in selected_objects:
            return False
        if str(row.get("colony_class", "")) in SPECIAL_COLONY_CLASSES:
            if not selected_object_policy_rows:
                return False
            return any(
                not build_plan_consumer_policy_excludes_dataset_object(row, policy_row)
                for policy_row in selected_object_policy_rows.get(token, [])
            )
        return True
    return False


def dataset_job_pressure_weight_block(block: str, row: dict[str, Any]) -> str:
    family = str(row.get("pressure_family") or dataset_job_pressure_family(row))
    if family == "military_capacity":
        raise ValueError("Military-capacity objects must use hard eligibility gates, not dataset construction scoring")
    # With economic plans active, building ai_weight blocks are not consumed.
    # Preserve parent coefficient/additional values and only supply the
    # economic-plan resource mapping this generated surface actually owns.
    block = replace_top_level_child_block(block, "ai_resource_production", dataset_ai_resource_production_block(row))
    return (
        f"# staid_dataset_job_pressure = family:{family} jobs:{row['jobs_created_total_estimate']} "
        f"roi2250:{row['roi_2250_to_2350_estimate']} flags:{row['data_quality_flags']}\n"
        + block
    )


def _json_object_amounts(value: str) -> dict[str, float]:
    if not value or value == "{}":
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    if not isinstance(parsed, dict):
        return {}
    amounts: dict[str, float] = {}
    for key, amount in parsed.items():
        try:
            numeric = float(amount)
        except (TypeError, ValueError):
            continue
        if numeric > 0:
            amounts[str(key)] = amounts.get(str(key), 0.0) + numeric
    return amounts


def dataset_ai_resource_production_amounts(row: dict[str, Any]) -> dict[str, int]:
    amounts = _json_object_amounts(str(row.get("direct_monthly_output_json", "")))
    modifier_text = str(row.get("modifier_keys", ""))
    for resource in AI_RESOURCE_PRODUCTION_RESOURCE_HINTS:
        if re.search(rf"(?:^|\|)[^|]*_{re.escape(resource)}_produces_(?:add|mult)(?:\||$)", modifier_text):
            amounts[resource] = max(amounts.get(resource, 0.0), 1.0)
    family = str(row.get("pressure_family") or dataset_job_pressure_family(row))
    job_units = max(1.0, float(row.get("jobs_created_total_estimate") or 0))
    if not amounts:
        for resource in AI_RESOURCE_PRODUCTION_FAMILY_DEFAULTS.get(family, ("energy", "minerals")):
            amounts[resource] = max(amounts.get(resource, 0.0), job_units)
    elif float(row.get("jobs_created_total_estimate") or 0) > 0:
        for resource in AI_RESOURCE_PRODUCTION_FAMILY_DEFAULTS.get(family, ()):
            amounts.setdefault(resource, job_units)
    normalized: dict[str, int] = {}
    for resource, amount in amounts.items():
        if resource not in AI_RESOURCE_PRODUCTION_RESOURCE_HINTS:
            continue
        normalized[resource] = max(1, min(5000, int(round(amount))))
    if not normalized:
        normalized["energy"] = max(1, min(5000, int(round(job_units))))
    return dict(sorted(normalized.items()))


def dataset_ai_resource_production_block(row: dict[str, Any]) -> str:
    amounts = dataset_ai_resource_production_amounts(row)
    lines = ["\tai_resource_production = {"]
    for resource, amount in amounts.items():
        lines.append(f"\t\t{resource} = {amount}")
    lines.append("\t}")
    return "\n".join(lines)


def dataset_job_pressure_override_rows(limit: int = DATASET_JOB_PRESSURE_OBJECT_LIMIT) -> list[dict[str, Any]]:
    rows = _read_csv_rows(ECONOMIC_VALUATION_DATASET_CSV)
    policy_rows = build_plan_consumer_policy_rows()
    building_policy = build_plan_consumer_policy_buildings(policy_rows)
    selected_object_policy_rows = build_plan_consumer_policy_selected_object_rows(policy_rows)
    selected_objects = set(selected_object_policy_rows)
    known_jobs = collect_object_names(SNAPSHOT_ROOT).get("pop_job", set())
    candidates: list[dict[str, Any]] = []
    for row in rows:
        if row.get("object_type") not in {"building", "district"}:
            continue
        if not build_plan_consumer_policy_allows_dataset_object(
            row,
            building_policy,
            selected_objects,
            selected_object_policy_rows,
        ):
            continue
        if row.get("winning_mod_name") == "Stellar AI Director":
            continue
        if float(row.get("jobs_created_total_estimate") or 0) <= 0:
            continue
        if float(row.get("roi_2250_to_2350_estimate") or 0) <= 0:
            continue
        mod_id = row.get("winning_mod_id", "")
        if mod_id in {"", "none"}:
            continue
        try:
            source_root = mod_source_root_for_id(mod_id)
        except ValueError:
            continue
        source_path = source_root / row["winning_file"]
        if not source_path.exists():
            continue
        source_text = read_text(source_path)
        try:
            source_block = extract_top_level_object_text(source_text, row["object_id"])
        except ValueError:
            continue
        safety_issues = dataset_job_pressure_runtime_safety_issues(row, source_block, known_jobs)
        if safety_issues:
            continue
        folder = {
            "building": "buildings",
            "district": "districts",
        }[row["object_type"]]
        generated_file = MOD_ROOT / "common" / folder / f"zzzz_staid_13_dataset_job_pressure_{folder}.txt"
        family = dataset_job_pressure_family(row)
        if family == "military_capacity":
            continue
        policy = building_policy.get(row["object_id"], {})
        candidates.append(
            {
                **row,
                "pressure_family": family,
                "build_plan_consumer_status": policy.get("can_consume_now", "role_target"),
                "build_plan_modeling_status": policy.get("consumer_modeling_status", "role_target_scorable"),
                "source_path": str(source_path),
                "generated_folder": folder,
                "generated_file": generated_file.as_posix(),
            }
        )
    def stable_legacy_ordering_value(item: dict[str, Any]) -> float:
        raw_workforce = sum(_json_object_amounts(str(item.get("jobs_created_json", ""))).values())
        normalized_jobs = float(item.get("jobs_created_total_estimate") or 0)
        legacy_job_value = max(0.0, raw_workforce - normalized_jobs) * GENERIC_JOB_MONTHLY_VALUE * 100 * 12
        return float(item["roi_2250_to_2350_estimate"]) + legacy_job_value

    candidates.sort(
        key=lambda item: (
            stable_legacy_ordering_value(item),
            sum(_json_object_amounts(str(item.get("jobs_created_json", ""))).values()),
            item["object_id"],
        ),
        reverse=True,
    )
    selected: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    def add_rows(rows_to_add: Iterable[dict[str, Any]], row_limit: int | None = None) -> None:
        added = 0
        for candidate in rows_to_add:
            key = (candidate["object_type"], candidate["object_id"])
            if key in seen:
                continue
            selected.append(candidate)
            seen.add(key)
            added += 1
            if row_limit is not None and added >= row_limit:
                break

    repair_families = (
        "consumer_goods_repair",
        "alloy_scaling",
        "research_scaling",
        "strategic_resource_scaling",
        "energy_scaling",
        "mineral_scaling",
    )
    for family in repair_families:
        add_rows(
            [candidate for candidate in candidates if candidate["pressure_family"] == family],
            DATASET_JOB_PRESSURE_REPAIR_FAMILY_LIMIT,
        )
    add_rows(candidates, limit)
    return selected[:limit]


def dataset_job_pressure_override_artifacts() -> list[dict[str, Any]]:
    rows = dataset_job_pressure_override_rows()
    grouped: dict[Path, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(Path(row["generated_file"]), []).append(row)
    stale_zone_file = MOD_ROOT / "common" / "zones" / "zzzz_staid_13_dataset_job_pressure_zones.txt"
    if stale_zone_file not in grouped and stale_zone_file.exists():
        stale_zone_file.unlink()
    for file_path, file_rows in grouped.items():
        folder = file_rows[0]["generated_folder"]
        body = [
            "# Generated by tools/generate_stellar_ai_director_patch.py.",
            "# Full-object overrides copied from active-stack construction winners.",
            "# Dataset-driven economic-plan mapping: preserve source construction scoring and expose verified output through ai_resource_production.",
            "# Source potential/allow/possible blocks own prerequisites and legality; military-capacity objects are excluded and require hard eligibility gates.",
            f"# Source dataset: {ECONOMIC_VALUATION_DATASET_CSV.relative_to(REPO_ROOT).as_posix()}",
            f"# Build-plan consumer policy: {BUILD_PLAN_CONSUMER_POLICY_CSV.relative_to(REPO_ROOT).as_posix()}",
            "",
        ]
        variables = route_override_file_variables(file_rows)
        if variables:
            body.append("# Source-local variables required by copied construction objects.")
            body.extend(variables)
            body.append("")
        for row in file_rows:
            source_text = read_text(Path(row["source_path"]))
            block = extract_top_level_object_text(source_text, row["object_id"])
            block = dataset_job_pressure_weight_block(block, row)
            block = "\n".join(line.rstrip() for line in block.splitlines()) + "\n"
            body.append(
                f"# object = {row['object_type']}:{row['object_id']}; "
                f"source = {row['winning_mod_name']}::{row['winning_file']}; "
                f"consumer_policy = {row['build_plan_consumer_status']}:{row['build_plan_modeling_status']}"
            )
            body.append(block.rstrip())
            body.append("")
        text = "\n".join(body).rstrip() + "\n"
        parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
        write_text_file(file_path, text)
    write_csv(RESEARCH_ROOT / "stellar-ai-director-dataset-job-pressure-overrides-2026-07-07.csv", rows)
    return rows


ROUTE_RESEARCH_GATES = {
    "mega_engineering_core": "staid_core_unlock_research_priority_ready",
    "mega_shipyard_core": "staid_core_unlock_research_priority_ready",
    "economy_megastructure_core": "staid_core_unlock_research_priority_ready",
    "early_kilo_economy_core": "staid_early_kilo_economy_research_priority_ready",
    "science_kilo_snowball_core": "staid_science_kilo_research_priority_ready",
    "research_megastructure_core": "staid_science_nexus_research_priority_ready",
    "planetary_computer_research_core": "staid_planetary_computer_research_priority_ready",
    "pop_assembly_snowball_core": "staid_pop_assembly_snowball_ready",
    "ring_world_growth_core": "staid_ring_world_research_priority_ready",
    "storage_cap_core": "staid_storage_cap_research_priority_ready",
    "gigas_special_resource_core": "staid_gigas_special_resource_unlock_ready",
    "planetcraft_route": "staid_planetcraft_research_priority_ready",
    "war_moon_route": "staid_war_moon_research_priority_ready",
    "systemcraft_route": "staid_systemcraft_research_priority_ready",
    "nsc3_capital_hull_route": "staid_nsc3_capital_hull_unlock_ready",
    "esc_component_route": "staid_esc_component_unlock_ready",
    "crowded_tall_route": "staid_planetary_capacity_growth_ready",
    "conquest_escape_route": "staid_aggressive_fleet_pressure",
    "raiding_pop_acquisition_route": "staid_raiding_pop_acquisition_priority",
    "apex_site_preservation_core": "staid_apex_site_preservation_ready",
    "fallen_empire_benchmark_route": "staid_static_defense_investment_ready",
    "research_throughput_infrastructure": "staid_research_construction_priority_ready",
    "research_diplomacy_core": "staid_research_diplomacy_priority_ready",
}

ROUTE_BUILD_GATES = {
    "mega_engineering_core": "staid_core_unlock_research_priority_ready",
    "mega_shipyard_core": "staid_mega_shipyard_build_priority_ready",
    "economy_megastructure_core": "staid_economy_megastructure_build_priority_ready",
    "early_kilo_economy_core": "staid_early_kilo_economy_build_priority_ready",
    "science_kilo_snowball_core": "staid_science_kilo_build_priority_ready",
    "research_megastructure_core": "staid_science_nexus_build_priority_ready",
    "planetary_computer_research_core": "staid_planetary_computer_build_priority_ready",
    "pop_assembly_snowball_core": "staid_pop_assembly_snowball_ready",
    "ring_world_growth_core": "staid_ring_world_build_priority_ready",
    "storage_cap_core": "staid_storage_cap_build_priority_ready",
    "gigas_special_resource_core": "staid_megastructure_commit_safe",
    "planetcraft_route": "staid_planetcraft_build_priority_ready",
    "war_moon_route": "staid_war_moon_build_priority_ready",
    "systemcraft_route": "staid_systemcraft_build_priority_ready",
    "nsc3_capital_hull_route": "staid_modded_fleet_conversion_ready",
    "esc_component_route": "staid_modded_fleet_conversion_ready",
    "crowded_tall_route": "staid_planetary_capacity_growth_ready",
    "conquest_escape_route": "staid_aggressive_fleet_pressure",
    "raiding_pop_acquisition_route": "staid_raiding_pop_acquisition_priority",
    "apex_site_preservation_core": "staid_apex_site_preservation_ready",
    "fallen_empire_benchmark_route": "staid_static_defense_investment_ready",
    "research_throughput_infrastructure": "staid_research_construction_priority_ready",
    "research_diplomacy_core": "staid_research_diplomacy_priority_ready",
}

STELLARAI_INLINE_SCRIPT_DEPENDENCIES = (
    "invalid_planet_type_guard",
    "minerals_recovery_building_weight",
    "rare_resource_guard_modifiers",
)

ROUTE_TIMING_FACTORS = {
    "mega_shipyard_core": (3, 5, 8),
    "economy_megastructure_core": (3, 5, 8),
    "early_kilo_economy_core": (4, 6, 8),
    "science_kilo_snowball_core": (5, 8, 11),
    "research_megastructure_core": (4, 7, 10),
    "planetary_computer_research_core": (4, 8, 12),
    "pop_assembly_snowball_core": (6, 9, 12),
    "ring_world_growth_core": (3, 6, 9),
    "storage_cap_core": (4, 7, 10),
    "gigas_special_resource_core": (3, 5, 8),
    "planetcraft_route": (3, 6, 10),
    "war_moon_route": (3, 6, 10),
    "systemcraft_route": (4, 8, 12),
    "conquest_escape_route": (4, 7, 11),
    "raiding_pop_acquisition_route": (6, 10, 14),
    "apex_site_preservation_core": (2, 5, 9),
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
    "early_kilo_economy_core": [
        "\tmodifier = { factor = 3 has_technology = tech_orbital_arc_furnace }",
        "\tmodifier = { factor = 3 has_technology = giga_tech_asteroid_manufactory }",
        "\tmodifier = { factor = 6 staid_resource_waste_pressure = yes }",
        "\tmodifier = { factor = 8 staid_high_scale_snowball_pressure = yes }",
    ],
    "science_kilo_snowball_core": [
        "\tmodifier = { factor = 4 has_technology = giga_tech_engineering_test_site }",
        "\tmodifier = { factor = 4 has_technology = giga_tech_macro_scale_weather_manipulation }",
        "\tmodifier = { factor = 3 staid_research_under_curve = yes }",
    ],
    "research_megastructure_core": [
        "\tmodifier = { factor = 4 has_technology = tech_science_nexus }",
        "\tmodifier = { factor = 3 staid_research_under_curve = yes }",
    ],
    "planetary_computer_research_core": [
        "\tmodifier = { factor = 5 has_technology = giga_tech_planetary_computer }",
        "\tmodifier = { factor = 4 staid_research_under_curve = yes }",
        "\tmodifier = { factor = 2 staid_planetary_capacity_growth_ready = yes }",
    ],
    "pop_assembly_snowball_core": [
        "\tmodifier = { factor = 5 staid_planetary_capacity_growth_ready = yes }",
        "\tmodifier = { factor = 3 staid_research_under_curve = yes }",
        "\tmodifier = { factor = 2 years_passed < 80 }",
    ],
    "ring_world_growth_core": [
        "\tmodifier = { factor = 4 has_technology = tech_ring_world }",
        "\tmodifier = { factor = 2 staid_planetary_capacity_growth_ready = yes }",
    ],
    "storage_cap_core": [
        "\tmodifier = { factor = 4 has_technology = giga_tech_kugelblitz }",
        "\tmodifier = { factor = 10 staid_resource_waste_pressure = yes }",
        "\tmodifier = { factor = 14 staid_high_scale_snowball_pressure = yes }",
    ],
    "conquest_escape_route": [
        "\tmodifier = { factor = 10 staid_site_limited_expansion_ready = yes }",
        "\tmodifier = { factor = 5 staid_fleet_buildup_economy_safe = yes }",
        "\tmodifier = { factor = 8 staid_militarist_conquest_strategy = yes }",
        "\tmodifier = { factor = 6 has_ethic = ethic_militarist }",
        "\tmodifier = { factor = 12 has_ethic = ethic_fanatic_militarist }",
    ],
    "raiding_pop_acquisition_route": [
        "\tmodifier = { factor = 14 staid_raiding_pop_growth_strategy = yes }",
        "\tmodifier = { factor = 8 staid_opening_military_to_pops = yes }",
        "\tmodifier = { factor = 5 has_ethic = ethic_militarist }",
        "\tmodifier = { factor = 10 has_ethic = ethic_fanatic_militarist }",
    ],
    "apex_site_preservation_core": [
        "\tmodifier = { factor = 8 has_technology = giga_tech_matrioshka_brain_1 }",
        "\tmodifier = { factor = 4 has_technology = giga_tech_neutronium_gigaforge }",
        "\tmodifier = { factor = 0.15 NOT = { staid_apex_site_preservation_ready = yes } }",
    ],
    "nsc3_capital_hull_route": [
        "\tmodifier = { factor = 3 has_technology = tech_Carrier_1 }",
        "\tmodifier = { factor = 4 has_technology = tech_Dreadnought_1 }",
        "\tmodifier = { factor = 6 has_technology = tech_Flagship_1 }",
        "\tmodifier = { factor = 0.5 NOT = { staid_nsc3_capital_hull_unlock_ready = yes } }",
    ],
    "esc_component_route": [
        "\tmodifier = { factor = 3 has_technology = esc_tech_dark_matter_power_core_2 }",
        "\tmodifier = { factor = 3 has_technology = esc_tech_strikecraft_5 }",
        "\tmodifier = { factor = 4 has_technology = esc_tech_dreadnought_computer }",
        "\tmodifier = { factor = 0.25 NOT = { staid_advanced_component_resource_support_ready = yes } }",
    ],
}


def route_modifier_line(factor: int | float | str, condition: str, *, country_scope: str | None = None) -> str:
    if country_scope:
        return f"\tmodifier = {{ factor = {factor} {country_scope} = {{ {condition} }} }}"
    return f"\tmodifier = {{ factor = {factor} {condition} }}"


def long_term_net_value(
    monthly_value: float,
    upfront_cost_value: float,
    monthly_upkeep_value: float,
    years_passed: int | float,
) -> float:
    current_year = DIRECTOR_CAMPAIGN_START_YEAR + years_passed
    remaining_months = max(0.0, (DIRECTOR_ENDGAME_VALUE_HORIZON_YEAR - current_year) * 12.0)
    return max(0.0, monthly_value - monthly_upkeep_value) * remaining_months - upfront_cost_value


def long_term_roi_ratio(
    monthly_value: float,
    upfront_cost_value: float,
    monthly_upkeep_value: float,
    years_passed: int | float,
) -> float:
    denominator = max(1.0, upfront_cost_value)
    return long_term_net_value(monthly_value, upfront_cost_value, monthly_upkeep_value, years_passed) / denominator


def long_term_year_band_condition(lower: int | None, upper: int) -> str:
    if lower is None:
        return f"years_passed < {upper}"
    return f"AND = {{ years_passed > {lower - 1} years_passed < {upper} }}"


def long_term_value_factor_pairs(
    monthly_value: float,
    upfront_cost_value: float,
    monthly_upkeep_value: float,
    *,
    divisor: float = 25.0,
    maximum: int = 30,
) -> list[tuple[int, str]]:
    pairs: list[tuple[int, str]] = []
    for lower, upper, representative_year in LONG_TERM_VALUE_BANDS:
        roi = long_term_roi_ratio(monthly_value, upfront_cost_value, monthly_upkeep_value, representative_year)
        factor = max(1, min(maximum, int(round(max(0.0, roi) / divisor))))
        if factor > 1:
            pairs.append((factor, long_term_year_band_condition(lower, upper)))
    return pairs


def route_lifetime_value_modifiers(target: dict[str, Any]) -> list[str]:
    profile = ROUTE_LONG_TERM_VALUE_PROFILES.get(str(target["route_id"]))
    if not profile:
        return []
    country_scope = route_country_scope_for_target(target)
    monthly_value, upfront_cost_value, monthly_upkeep_value = profile
    return [
        route_modifier_line(factor, condition, country_scope=country_scope)
        for factor, condition in long_term_value_factor_pairs(
            monthly_value,
            upfront_cost_value,
            monthly_upkeep_value,
            divisor=18.0,
            maximum=35,
        )
    ]


def route_country_scope_for_target(target: dict[str, Any]) -> str | None:
    if target["object_type"] == "megastructure":
        return "from"
    if target["object_type"] in {"starbase_building", "starbase_module"}:
        return "owner"
    return None


def scope_route_modifier_for_target(target: dict[str, Any], modifier_line: str) -> str:
    country_scope = route_country_scope_for_target(target)
    if not country_scope:
        return modifier_line
    stripped = modifier_line.strip()
    prefix = "modifier = { factor = "
    suffix = " }"
    if not stripped.startswith(prefix) or not stripped.endswith(suffix):
        return modifier_line
    body = stripped[len(prefix) : -len(suffix)].strip()
    factor, separator, condition = body.partition(" ")
    if not separator or not condition:
        return modifier_line
    return route_modifier_line(factor, condition, country_scope=country_scope)


def route_gate_for_target(target: dict[str, Any]) -> str:
    if target["object_type"] == "megastructure" and target["object_id"] == "kugelblitz_0":
        return "staid_kugelblitz_new_start_budget_ready"
    route_id = str(target["route_id"])
    if target["object_type"] in {"technology", "ascension_perk", "tradition", "tradition_category"}:
        return ROUTE_RESEARCH_GATES.get(route_id, "staid_surplus_sink_pressure")
    return ROUTE_BUILD_GATES.get(route_id, "staid_surplus_sink_pressure")


def kugelblitz_start_budget_modifiers(target: dict[str, Any]) -> list[str]:
    if target["object_type"] != "megastructure" or target["object_id"] != "kugelblitz_0":
        return []
    country_scope = route_country_scope_for_target(target)
    return [
        "\t# kugelblitz_start_budget = empty_silos_are_capped_storage_not_income",
        route_modifier_line(0, "has_country_flag = is_currently_building_kugelblitz", country_scope=country_scope),
        route_modifier_line(0, "staid_unfinished_kugelblitz_exists = yes", country_scope=country_scope),
        route_modifier_line(0, "check_variable = { which = giga_current_kugel value >= 10 }", country_scope=country_scope),
        route_modifier_line(0.03, "has_country_flag = has_recently_built_kugelblitz", country_scope=country_scope),
        route_modifier_line(0.02, "check_variable = { which = giga_current_kugel value >= 9 }", country_scope=country_scope),
        route_modifier_line(0.04, "check_variable = { which = giga_current_kugel value >= 8 }", country_scope=country_scope),
        route_modifier_line(0.08, "check_variable = { which = giga_current_kugel value >= 7 }", country_scope=country_scope),
        route_modifier_line(0.15, "check_variable = { which = giga_current_kugel value >= 6 }", country_scope=country_scope),
        route_modifier_line(0.25, "check_variable = { which = giga_current_kugel value >= 5 }", country_scope=country_scope),
        route_modifier_line(0.40, "check_variable = { which = giga_current_kugel value >= 4 }", country_scope=country_scope),
        route_modifier_line(0.60, "check_variable = { which = giga_current_kugel value >= 3 }", country_scope=country_scope),
    ]


def route_extra_modifiers_for_target(target: dict[str, Any]) -> list[str]:
    if target["object_type"] == "megastructure" and target["object_id"] == "kugelblitz_0":
        return []
    modifiers = ROUTE_EXTRA_MODIFIERS.get(str(target["route_id"]), [])
    if target["object_type"] == "megastructure":
        return [
            line
            for line in modifiers
            if "staid_high_scale_snowball_pressure" not in line
        ]
    return modifiers


def technology_archetype_weight_modifiers(
    target: dict[str, Any],
    archetype_route_factors: Mapping[str, Mapping[str, float]] | None = None,
) -> list[str]:
    """Return bounded identity tie-breakers for reviewed technology routes."""

    if target["object_type"] != "technology":
        return []
    if target["object_id"] in TECHNOLOGY_ARCHETYPE_EXCLUDED_OBJECTS:
        return []
    factors = (
        TECHNOLOGY_ARCHETYPE_ROUTE_FACTORS
        if archetype_route_factors is None
        else archetype_route_factors
    )
    route_id = str(target["route_id"])
    route_gate = route_gate_for_target(target)
    lines: list[str] = []
    for archetype, route_factors in factors.items():
        factor = route_factors.get(route_id)
        if factor is None:
            continue
        if not 1.0 < factor <= 1.15:
            raise ValueError(
                f"Technology archetype factor must be in (1.0, 1.15]: "
                f"{archetype}/{route_id}={factor}"
            )
        condition = " ".join(
            (
                f"staid_archetype_hard_{archetype} = yes",
                "staid_archetype_identity_conflict = no",
                "staid_archetype_eligible_country = yes",
                f"{route_gate} = yes",
                "staid_survival_mode = no",
                "staid_recovery_mode = no",
                "staid_catastrophic_collapse_mode = no",
                "staid_core_deficit_short_runway = no",
                "is_at_war = no",
                "NOT = { recently_lost_war = yes }",
            )
        )
        lines.append(route_modifier_line(factor, condition))
    return lines


def identity_strategy_weight_modifiers(target: dict[str, Any]) -> list[str]:
    """Return bounded resolved-primary, secondary, and defining strategy vectors."""

    if target["object_type"] not in {
        "ascension_perk",
        "tradition_category",
        "tradition",
    }:
        return []
    object_id = str(target["object_id"])
    route_gate = route_gate_for_target(target)
    common = (
        "staid_archetype_identity_conflict = no "
        "staid_archetype_eligible_country = yes "
        f"{route_gate} = yes "
        "staid_survival_mode = no "
        "staid_recovery_mode = no "
        "staid_catastrophic_collapse_mode = no "
        "staid_core_deficit_short_runway = no"
    )
    factors_and_conditions: list[tuple[float, str]] = []
    for archetype, object_factors in IDENTITY_STRATEGY_PRIMARY_FACTORS.items():
        factor = object_factors.get(object_id)
        if factor is None:
            continue
        factors_and_conditions.append(
            (factor, f"staid_archetype_{archetype} = yes {common}")
        )
        factors_and_conditions.append(
            (
                1.05,
                f"staid_archetype_lead_secondary_{archetype} = yes {common}",
            )
        )
    for identity_trigger, object_factors in IDENTITY_STRATEGY_DEFINING_FACTORS.items():
        factor = object_factors.get(object_id)
        if factor is not None:
            factors_and_conditions.append((factor, f"{identity_trigger} = yes {common}"))
    if any(not 1.0 < factor <= 1.15 for factor, _condition in factors_and_conditions):
        raise ValueError(f"Identity strategy factor escaped (1.0, 1.15]: {object_id}")
    return [
        route_modifier_line(factor, condition)
        for factor, condition in factors_and_conditions
    ]


def identity_static_defense_weight_modifiers(target: dict[str, Any]) -> list[str]:
    """Return bounded country-scoped preferences on safe static-defense objects."""

    if target["object_type"] not in {"starbase_building", "starbase_module"}:
        return []
    common = (
        "staid_archetype_identity_conflict = no "
        "staid_archetype_eligible_country = yes "
        "staid_static_defense_investment_ready = yes "
        "staid_survival_mode = no "
        "staid_recovery_mode = no "
        "staid_catastrophic_collapse_mode = no "
        "staid_core_deficit_short_runway = no"
    )
    factors_and_conditions = (
        (1.15, f"staid_archetype_defensive = yes {common}"),
        (1.05, f"staid_archetype_lead_secondary_defensive = yes {common}"),
        (1.10, f"staid_identity_inward_perfection = yes {common}"),
    )
    return [
        route_modifier_line(factor, condition, country_scope="owner")
        for factor, condition in factors_and_conditions
    ]


def identity_megastructure_weight_modifiers(target: dict[str, Any]) -> list[str]:
    """Return bounded country-scoped identity sequencing for owned mega routes."""

    if target["object_type"] != "megastructure":
        return []
    start_object_ids = {
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
    if (
        target.get("megastructure_stage_kind") != "start"
        or str(target["object_id"]) not in start_object_ids
    ):
        return []
    route_id = str(target["route_id"])
    route_gate = route_gate_for_target(target)
    primary_routes = {
        "research": {
            "science_kilo_snowball_core",
            "research_megastructure_core",
            "planetary_computer_research_core",
        },
        "gestalt_growth": {"ring_world_growth_core", "crowded_tall_route"},
        "conquest": {
            "mega_shipyard_core",
            "planetcraft_route",
            "war_moon_route",
            "systemcraft_route",
        },
        "extermination": {
            "mega_shipyard_core",
            "planetcraft_route",
            "war_moon_route",
            "systemcraft_route",
        },
    }
    primary_factors = {
        "research": 1.15,
        "gestalt_growth": 1.12,
        "conquest": 1.10,
        "extermination": 1.15,
    }
    common = (
        "staid_archetype_identity_conflict = no "
        "staid_archetype_eligible_country = yes "
        f"{route_gate} = yes "
        "staid_basic_economy_runway_safe = yes "
        "staid_survival_mode = no "
        "staid_recovery_mode = no "
        "staid_catastrophic_collapse_mode = no "
        "staid_core_deficit_short_runway = no"
    )
    factors_and_conditions: list[tuple[float, str]] = []
    for archetype, routes in primary_routes.items():
        if route_id not in routes:
            continue
        factors_and_conditions.append(
            (
                primary_factors[archetype],
                f"staid_archetype_{archetype} = yes {common}",
            )
        )
        factors_and_conditions.append(
            (
                1.05,
                f"staid_archetype_lead_secondary_{archetype} = yes {common}",
            )
        )
    defining_routes = {
        "staid_identity_megacorp": {
            "economy_megastructure_core",
            "early_kilo_economy_core",
        },
        "staid_identity_inward_perfection": {"crowded_tall_route"},
        "staid_identity_barbaric_despoiler": {
            "mega_shipyard_core",
            "planetcraft_route",
            "war_moon_route",
            "systemcraft_route",
        },
    }
    for identity_trigger, routes in defining_routes.items():
        if route_id in routes:
            factors_and_conditions.append(
                (1.10, f"{identity_trigger} = yes {common}")
            )
    return [
        route_modifier_line(factor, condition, country_scope="from")
        for factor, condition in factors_and_conditions
    ]


def route_weight_modifiers(
    target: dict[str, Any], *, archetype_overlay: bool = True
) -> list[str]:
    route_id = str(target["route_id"])
    route_gate = route_gate_for_target(target)
    mid_factor, late_factor, crisis_factor = ROUTE_TIMING_FACTORS.get(route_id, (2, 3, 5))
    country_scope = route_country_scope_for_target(target)
    survival_factor = 1.5 if target["object_type"] in {"starbase_building", "starbase_module"} else 0
    lines = [
        route_modifier_line(survival_factor, "staid_survival_mode = yes", country_scope=country_scope),
        route_modifier_line(0.35, "staid_recovery_mode = yes", country_scope=country_scope),
        route_modifier_line(0, f"NOT = {{ {route_gate} = yes }}", country_scope=country_scope),
        route_modifier_line(4, f"{route_gate} = yes", country_scope=country_scope),
        route_modifier_line(mid_factor, "years_passed > 44", country_scope=country_scope),
        route_modifier_line(late_factor, "years_passed > 79", country_scope=country_scope),
        route_modifier_line(crisis_factor, "years_passed > 119", country_scope=country_scope),
    ]
    lines.extend(route_lifetime_value_modifiers(target))
    lines.extend(kugelblitz_start_budget_modifiers(target))
    if target.get("megastructure_stage_kind") == "upgrade":
        lines.extend(
            [
                "\t# megastructure_continuation_priority = finish_existing_before_new_start",
                route_modifier_line(35, "staid_megastructure_continuation_priority_ready = yes", country_scope=country_scope),
                route_modifier_line(8, "staid_resource_waste_pressure = yes", country_scope=country_scope),
            ]
        )
    lines.extend(scope_route_modifier_for_target(target, line) for line in route_extra_modifiers_for_target(target))
    if archetype_overlay:
        lines.extend(technology_archetype_weight_modifiers(target))
        lines.extend(identity_strategy_weight_modifiers(target))
        lines.extend(identity_static_defense_weight_modifiers(target))
        lines.extend(identity_megastructure_weight_modifiers(target))
    return lines


GIGAS_HABITAT_UNCOLONIZED_VETO = """        modifier = {
            # AI shouldn't build habitats if they have any uncolonised habitats.
            factor = 0
            owner = {
                any_planet_within_border = {
                    is_planet_class = pc_habitat
                    is_colony = no
                }
            }
        }"""


def gigas_habitat_ai_weight_block(
    block: str,
    target: dict[str, Any],
    *,
    archetype_overlay: bool = True,
) -> str:
    """Preserve current Gigas site scoring while replacing its global deadlock gate."""
    if (
        target.get("mod_id") != "1121692237"
        or target.get("object_type") != "megastructure"
        or target.get("object_id") != "habitat_central_complex"
    ):
        raise ValueError("Gigas habitat AI transformer received the wrong target")
    if block.count(GIGAS_HABITAT_UNCOLONIZED_VETO) != 1:
        raise ValueError("Active Gigas uncolonized-habitat veto drifted; re-audit before generation")

    backlog_penalty = """        modifier = {
            # A real colonization backlog should delay another habitat, but it
            # must not turn one stale or uncolonizable habitat into a global veto.
            factor = 0.1
            from = { ai_colonize_plans > 0 }
        }"""
    route_boost = """        modifier = {
            # Bounded crowded-tall pressure; parent site quality remains decisive.
            factor = 2
            from = { staid_planetary_capacity_growth_ready = yes }
        }"""
    block = block.replace(GIGAS_HABITAT_UNCOLONIZED_VETO, backlog_penalty)
    block = insert_top_level_ai_weight_modifier(block, route_boost)
    if archetype_overlay:
        block = insert_top_level_ai_weight_modifiers(
            block,
            [
                line.replace("\t", "        ", 1)
                for line in identity_megastructure_weight_modifiers(target)
            ],
        )
    return block


def director_ai_weight_block(
    target: dict[str, Any], *, archetype_overlay: bool = True
) -> str:
    if (
        target.get("mod_id") == "1121692237"
        and target.get("object_type") == "megastructure"
        and target.get("object_id") == "habitat_central_complex"
    ):
        raise ValueError("habitat_central_complex requires the parent-aware Gigas transformer")
    lines = [
        "\tai_weight = {",
        f"\t\tfactor = {target['weight']}",
        "",
        f"\t\t# policy_route = {target['route_id']}",
        f"\t\t# source_object = {target['object_type']}:{target['object_id']}",
    ]
    lines.extend(
        line.replace("\t", "\t\t", 1)
        for line in route_weight_modifiers(
            target, archetype_overlay=archetype_overlay
        )
    )
    lines.append("\t}")
    return "\n".join(lines) + "\n"


def native_tradition_route_weight_block(
    block: str,
    target: dict[str, Any],
    *,
    archetype_overlay: bool = True,
) -> str:
    """Boost a native tradition category or selectable node without replacing its policy."""
    route_gate = route_gate_for_target(target)
    modifiers = [
        f"\t\t# policy_route = {target['route_id']}; preserve vanilla category and node selection",
        f"\t\tmodifier = {{ factor = {target['weight']} {route_gate} = yes }}",
    ]
    if archetype_overlay:
        modifiers.extend(
            line.replace("\t", "\t\t", 1)
            for line in identity_strategy_weight_modifiers(target)
        )
    return insert_top_level_ai_weight_modifiers(block, modifiers)


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


def identity_subject_agreement_family(object_id: str) -> str:
    for family in ("bulwark", "scholarium", "prospectorium"):
        if object_id == f"preset_{family}" or object_id.startswith(
            f"preset_{family}_"
        ):
            return family
    raise ValueError(f"Unsupported identity specialist preset: {object_id}")


def identity_subject_agreement_modifiers(
    object_id: str,
    weight_key: str,
) -> list[str]:
    """Return bounded evaluator-side identity preferences for one preset weight."""

    family = identity_subject_agreement_family(object_id)
    archetype = {
        "bulwark": "defensive",
        "scholarium": "research",
        "prospectorium": "gestalt_growth",
    }[family]
    if weight_key not in {"overlord_weight", "subject_weight"}:
        raise ValueError(f"Unsupported specialist preset weight: {weight_key}")
    if weight_key == "subject_weight" and "_mean_" in object_id:
        return []
    common = (
        "staid_archetype_identity_conflict = no "
        "staid_archetype_eligible_country = yes "
        "staid_basic_economy_runway_safe = yes "
        "staid_survival_mode = no "
        "staid_recovery_mode = no "
        "staid_catastrophic_collapse_mode = no "
        "staid_core_deficit_short_runway = no"
    )
    return [
        f"\t\tmodifier = {{ factor = 1.15 staid_archetype_{archetype} = yes {common} }}",
        f"\t\tmodifier = {{ factor = 1.05 staid_archetype_lead_secondary_{archetype} = yes {common} }}",
    ]


def identity_subject_agreement_object_text(
    source_text: str,
    object_id: str,
    expected_sha256: str,
) -> str:
    block = extract_top_level_object_text(source_text, object_id)
    actual_sha256 = hashlib.sha256(
        normalize_text_file_content(block).encode("utf-8")
    ).hexdigest()
    if actual_sha256 != expected_sha256:
        raise ValueError(
            f"Active specialist preset drifted: {object_id} "
            f"expected={expected_sha256} actual={actual_sha256}"
        )
    for weight_key in ("overlord_weight", "subject_weight"):
        modifiers = identity_subject_agreement_modifiers(object_id, weight_key)
        if modifiers:
            block = append_child_block_clause(
                block,
                weight_key,
                "\n".join(modifiers),
            )
    return block


def render_identity_subject_agreement_artifacts() -> dict[Path, str]:
    """Render four fail-closed agreement-preset files without writing them."""

    source_root = STELLARIS_INSTALL_ROOT / "common" / "agreement_presets"
    artifacts: dict[Path, str] = {}
    for source_file, (output_file, object_hashes) in (
        IDENTITY_SUBJECT_AGREEMENT_SOURCES.items()
    ):
        source_path = source_root / source_file
        source_text = read_text(source_path)
        output_path = IDENTITY_SUBJECT_AGREEMENT_ROOT / output_file
        rows = [
            {
                "source_path": str(source_path),
                "object_id": object_id,
                "generated_file": str(output_path),
            }
            for object_id in object_hashes
        ]
        variables = route_override_file_variables(rows)
        lines = [
            "# Generated by tools/generate_stellar_ai_subject_agreements.py.",
            f"# Full-object, hash-locked copies from common/agreement_presets/{source_file}.",
            "# Only evaluator-side overlord_weight/subject_weight identity preferences are added.",
            "# Terms, potential, acceptance, Nomad exclusions, and negative subject weights remain parent-owned.",
            "",
        ]
        if variables:
            lines.extend(variables)
            lines.append("")
        for object_id, expected_sha256 in object_hashes.items():
            lines.append(f"# source_object_sha256 = {expected_sha256}")
            lines.append(
                identity_subject_agreement_object_text(
                    source_text,
                    object_id,
                    expected_sha256,
                ).rstrip()
            )
            lines.append("")
        rendered = "\n".join(lines).rstrip() + "\n"
        parse_pdx(rendered)
        artifacts[output_path] = rendered
    if len(artifacts) != 4 or sum(
        len(object_hashes)
        for _source_file, (_output_file, object_hashes) in IDENTITY_SUBJECT_AGREEMENT_SOURCES.items()
    ) != 18:
        raise ValueError("Identity specialist agreement manifest must remain 4 files / 18 objects")
    return artifacts


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
    global_defined = set(common_scripted_variable_definitions(common))
    global_defined.update(common_scripted_variable_definitions(STELLARIS_INSTALL_ROOT / "common"))
    # The generated game-rule override preserves Forgotten Empires' references
    # to its globally loaded scripted variables instead of redefining them.
    for mod_id in (*ATLAS_SOURCE_MODS, "3728581560"):
        try:
            global_defined.update(common_scripted_variable_definitions(mod_source_root_for_id(mod_id) / "common"))
        except ValueError:
            continue
    for file_path in iter_text_files(common):
        relative = file_path.relative_to(mod_root)
        is_inline_script = len(relative.parts) >= 2 and relative.parts[:2] == ("common", "inline_scripts")
        defined: set[str] = set(global_defined)
        uses: list[tuple[int, str]] = []
        for line_number, raw_line in enumerate(read_text(file_path).splitlines(), start=1):
            code = raw_line.split("#", 1)[0]
            definition = AT_VARIABLE_DEFINITION_RE.match(code.rstrip())
            if definition:
                defined.add(definition.group("name"))
                code = definition.group("value")
            for match in AT_VARIABLE_RE.finditer(code):
                if is_inline_script and match.end() < len(code) and code[match.end()] == "$":
                    continue
                uses.append((line_number, match.group(0)))
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


def validate_staid_scripted_trigger_cycles(mod_root: Path = MOD_ROOT) -> list[str]:
    trigger_root = mod_root / "common" / "scripted_triggers"
    if not trigger_root.exists():
        return []
    definitions: dict[str, PDXValue] = {}
    owners: dict[str, list[str]] = {}
    errors: list[str] = []
    for trigger_path in iter_text_files(trigger_root):
        relative = trigger_path.relative_to(mod_root).as_posix()
        root = parse_pdx(read_text(trigger_path))
        for assignment in block_assignments(root):
            if not assignment.key.startswith("staid_"):
                continue
            owners.setdefault(assignment.key, []).append(relative)
            definitions.setdefault(assignment.key, assignment.value)
    for name, paths in sorted(owners.items()):
        if len(paths) > 1:
            errors.append(
                f"Duplicate staid scripted trigger {name}: " + ", ".join(paths)
            )

    graph = {
        name: {
            assignment.key
            for assignment in iter_assignments(value)
            if assignment.key in definitions
        }
        for name, value in definitions.items()
    }
    visiting: list[str] = []
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            cycle = visiting[visiting.index(node) :] + [node]
            provenance = ", ".join(
                f"{name}={owners[name][0]}" for name in dict.fromkeys(cycle)
            )
            errors.append(
                "Cyclic staid scripted trigger references: "
                + " -> ".join(cycle)
                + f" ({provenance})"
            )
            return
        if node in visited:
            return
        visiting.append(node)
        for child in sorted(graph[node]):
            visit(child)
        visiting.pop()
        visited.add(node)

    for node in sorted(graph):
        visit(node)

    return errors


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
        row["generated_file"] = route_override_generated_file_path(row).as_posix()
        resolved.append(row)
    return resolved


def route_override_generated_file_path(
    row: dict[str, Any],
    mod_root: Path = MOD_ROOT,
) -> Path:
    """Resolve a route artifact from portable row fields, never a captured absolute path."""

    generated_folder = str(row.get("generated_folder", ""))
    file_key = str(row.get("file_key", ""))
    safe_component = re.compile(r"^[A-Za-z0-9_]+$")
    if not safe_component.fullmatch(generated_folder):
        raise ValueError(f"Invalid route generated_folder: {generated_folder!r}")
    if not safe_component.fullmatch(file_key):
        raise ValueError(f"Invalid route file_key: {file_key!r}")
    return (
        mod_root
        / "common"
        / generated_folder
        / f"zzzz_staid_{file_key}_{generated_folder}.txt"
    )


def route_override_evidence_rows(
    rows: list[dict[str, Any]],
    mod_root: Path = MOD_ROOT,
) -> list[dict[str, Any]]:
    """Project operational route rows into a worktree-independent evidence schema."""

    evidence_rows: list[dict[str, Any]] = []
    for row in rows:
        evidence_row = dict(row)
        evidence_row["generated_file"] = route_override_generated_file_path(
            row,
            mod_root,
        ).relative_to(mod_root).as_posix()
        evidence_rows.append(evidence_row)
    return evidence_rows


def route_override_file_header(folder: str) -> str:
    return (
        "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
        "# Full-object override: copied parent/vanilla objects with Director-owned AI weighting.\n"
        "# Required source-local @variables are copied into this file to preserve parent parse context.\n"
        "# Trace each object through research/stellar-ai/object-atlas/policy-matrix-2026-07-06.csv.\n\n"
        f"# Generated surface: common/{folder}\n\n"
    )


def repair_gigas_habitat_spawn_effect_params(block: str, target: dict[str, Any]) -> str:
    if target["object_id"] != "habitat_central_complex" or "HABITAT_OWNER" in block:
        return block
    return block.replace(
        "spawn_habitat_effect = {\n                DISTANCE =",
        "spawn_habitat_effect = {\n                HABITAT_OWNER = root\n"
        "                TARGET_PLANET = event_target:target_planet\n"
        "                DISTANCE =",
    )


def strip_unsupported_district_keys(block: str) -> str:
    return "\n".join(
        line
        for line in block.splitlines()
        if not re.match(r"^\s*is_capped_by_modifier\s*=", line)
    )


def inject_zone_slots(block: str, slots: tuple[str, ...]) -> str:
    if re.search(r"(?m)^\s*zone_slots\s*=", block):
        return block
    lines = block.splitlines()
    if not lines:
        return block
    slot_lines = ["\tzone_slots = {", *(f"\t\t{slot}" for slot in slots), "\t}"]
    return "\n".join([lines[0], *slot_lines, *lines[1:]])


def gigas_habitat_zone_slot_compat_districts_text() -> str:
    source_root = SNAPSHOT_ROOT / "1121692237-gigastructural-engineering-more-44" / "common" / "districts"
    compat_rows = [
        {
            "source_path": str(source_root / source_file),
            "object_id": object_id,
            "generated_file": (MOD_ROOT / "common" / "districts" / "zzzz_staid_09_gigas_habitat_zone_slot_compat_districts.txt").as_posix(),
        }
        for source_file, object_ids in GIGAS_HABITAT_ZONE_SLOT_SOURCE_FILES.items()
        for object_id in object_ids
    ]
    lines = [
        "# Generated by tools/generate_stellar_ai_director_patch.py.",
        "# Full-object compatibility override for Gigas habitat/orbital districts exposed by Director's crowded-tall route.",
        "# Stellaris 4.4 district objects require zone_slots; the parent Gigas 4.4 files omit them for these districts.",
        "",
    ]
    variables = route_override_file_variables(compat_rows)
    if variables:
        lines.append("# Source-local variables required by copied parent district objects.")
        lines.extend(variables)
        lines.append("")
    for source_file, object_ids in GIGAS_HABITAT_ZONE_SLOT_SOURCE_FILES.items():
        source_path = source_root / source_file
        source_text = read_text(source_path)
        lines.append(f"# Source: common/districts/{source_file}")
        for object_id in object_ids:
            block = extract_top_level_object_text(source_text, object_id)
            block = strip_unsupported_district_keys(block)
            # District object gates execute from colony scope in 4.4. The
            # parent Gigas source uses bare planet flags, so copied full-object
            # overrides must restore the explicit planet scope switch.
            block = re.sub(
                r"\bhas_planet_flag\s*=\s*([A-Za-z0-9_.:+-]+)",
                r"planet = { has_planet_flag = \1 }",
                block,
            )
            block = inject_zone_slots(block, GIGAS_HABITAT_ZONE_SLOT_DISTRICTS[object_id])
            lines.append(block.rstrip())
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def identity_claim_budget_modifiers(target: dict[str, Any]) -> list[str]:
    """Return bounded claim-affordability preferences for conquest identities."""

    if str(target["object_id"]) not in {
        "influence_expenditure_claims",
        "influence_expenditure_claims_militarist",
        "influence_expenditure_claims_fanatic_militarist",
    }:
        return []
    common = (
        "staid_archetype_identity_conflict = no "
        "staid_archetype_eligible_country = yes "
        "has_potential_claims = yes "
        "staid_basic_economy_runway_safe = yes "
        "is_at_war = no "
        "staid_survival_mode = no "
        "staid_recovery_mode = no "
        "staid_catastrophic_collapse_mode = no "
        "staid_core_deficit_short_runway = no"
    )
    return [
        route_modifier_line(1.15, f"staid_archetype_conquest = yes {common}"),
        route_modifier_line(
            1.05,
            f"staid_archetype_lead_secondary_conquest = yes {common}",
        ),
        route_modifier_line(
            1.10,
            f"staid_identity_barbaric_despoiler = yes {common}",
        ),
    ]


def director_ai_budget_weight_block(
    block: str,
    target: dict[str, Any],
    *,
    archetype_overlay: bool = True,
) -> str:
    base_weights = {
        "influence_expenditure_claims": "0.20",
        "influence_expenditure_claims_militarist": "0.10",
        "influence_expenditure_claims_fanatic_militarist": "0.15",
    }
    object_id = str(target["object_id"])
    if object_id not in base_weights:
        return block
    identity_lines = "\n".join(
        (
            line.replace("\t", "\t\t", 1)
            for line in identity_claim_budget_modifiers(target)
        )
        if archetype_overlay
        else ()
    )
    identity_suffix = f"\n{identity_lines}" if identity_lines else ""
    weight = f"""\
\tweight = {{
\t\tweight = {base_weights[object_id]}
\t\tmodifier = {{ factor = 3 staid_influence_claim_pressure = yes }}
\t\tmodifier = {{ factor = 12 staid_boxed_in_claim_urgency = yes }}
\t\tmodifier = {{ factor = 2 has_resource = {{ type = influence amount > 900 }} }}{identity_suffix}
\t}}"""
    return replace_top_level_child_block(block, "weight", weight)


def route_override_object_text(
    target: dict[str, Any],
    object_names: dict[str, set[str]] | None = None,
    *,
    archetype_overlay: bool = True,
) -> str:
    source_text = read_text(Path(target["source_path"]))
    block = extract_top_level_object_text(source_text, target["object_id"])
    if target["object_type"] == "megastructure":
        target = {
            **target,
            "megastructure_stage_kind": "upgrade" if re.search(r"(?m)^\s*upgrade_from\s*=", block) else "start",
        }
    if target["object_type"] == "megastructure" and object_names is not None:
        block = strip_optional_absent_planet_classes(block, object_names)
        block = repair_gigas_habitat_spawn_effect_params(block, target)
    if target["object_type"] in {"building", "district"}:
        block = director_infrastructure_weight_block(block, target)
    elif target["object_type"] == "ai_budget":
        block = director_ai_budget_weight_block(
            block,
            target,
            archetype_overlay=archetype_overlay,
        )
    elif (
        target["object_type"] == "megastructure"
        and target["object_id"] == "habitat_central_complex"
    ):
        block = gigas_habitat_ai_weight_block(
            block,
            target,
            archetype_overlay=archetype_overlay,
        )
    elif target["object_type"] in {"tradition_category", "tradition"}:
        block = native_tradition_route_weight_block(
            block,
            target,
            archetype_overlay=archetype_overlay,
        )
    elif target["object_type"] == "federation_type" and target["object_id"] == "research_federation":
        block = research_federation_weight_block(block)
    else:
        if target["object_type"] == "starbase_module":
            block = merge_duplicate_top_level_child_blocks(block, "potential")
        block = replace_top_level_child_block(
            block,
            "ai_weight",
            director_ai_weight_block(
                target, archetype_overlay=archetype_overlay
            ),
        )
    block = "\n".join(line.rstrip() for line in block.splitlines()) + "\n"
    return (
        f"# policy_route = {target['route_id']}; source = {target['source_file']}; "
        f"parent_ai = {target['parent_ai_support']}; source_ai_weight = {target['source_has_ai_weight']}\n"
        + block
    )


def route_override_file_text(
    file_rows: list[dict[str, Any]],
    object_names: dict[str, set[str]] | None = None,
    *,
    archetype_overlay: bool = True,
) -> str:
    """Render one generated route-override file without writing it."""

    if not file_rows:
        raise ValueError("Route override file renderer requires at least one row")
    folders = {str(row["generated_folder"]) for row in file_rows}
    generated_files = {str(row["generated_file"]) for row in file_rows}
    if len(folders) != 1 or len(generated_files) != 1:
        raise ValueError(
            "Route override file rows must share one folder and generated file"
        )
    body = [route_override_file_header(str(file_rows[0]["generated_folder"]))]
    variables = route_override_file_variables(file_rows)
    if variables:
        body.append("# Source-local variables required by copied parent objects.")
        body.extend(variables)
        body.append("")
    for row in file_rows:
        body.append(
            route_override_object_text(
                row,
                object_names,
                archetype_overlay=archetype_overlay,
            )
        )
        body.append("")
    text = normalize_text_file_content("\n".join(body))
    parse_pdx(text)
    return text


def gigas_habitat_compat_scripted_effects_text() -> str:
    source_root = SNAPSHOT_ROOT / "1121692237-gigastructural-engineering-more-44" / "common" / "scripted_effects"
    source_objects = [
        (source_root / "giga_habitat_effects.txt", "science_kilo_update_orbital_effect"),
        (source_root / "giga_dismantle_effects.txt", "giga_dismantle_science_kilo_effect"),
    ]
    blocks = [
        "# Generated by tools/generate_stellar_ai_director_patch.py.",
        "# Full-object scripted-effect compatibility override for Gigas 4.4 habitat orbitals.",
        "# The copied Gigas effects probe removed *_orbital_resource ship-size keys.",
        "# No active 4.4 source defines a replacement orbital ship_size key, so fail that probe closed.",
        "",
    ]
    for source_path, object_id in source_objects:
        block = extract_top_level_object_text(read_text(source_path), object_id)
        block = block.replace(
            "is_ship_size = major_orbital_resource",
            "always = no # removed stale major_orbital_resource ship-size probe",
        )
        block = block.replace(
            "is_ship_size = minor_orbital_resource",
            "always = no # removed stale minor_orbital_resource ship-size probe",
        )
        blocks.append(block.rstrip())
        blocks.append("")
    return "\n".join(blocks).rstrip() + "\n"


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
        generated_file = (
            route_override_generated_file_path(row)
            .relative_to(MOD_ROOT)
            .as_posix()
        )
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
    rows = [
        row
        for row in route_override_target_rows()
        if row["object_type"] not in {"building", "district"}
    ]
    for stale_path in (
        MOD_ROOT / "common" / "buildings" / "zzzz_staid_06_research_infrastructure_buildings.txt",
        MOD_ROOT / "common" / "districts" / "zzzz_staid_06_research_infrastructure_districts.txt",
        MOD_ROOT / "common" / "buildings" / "zzzz_staid_07_pop_assembly_buildings.txt",
    ):
        stale_path.unlink(missing_ok=True)
    object_names = collect_object_names()
    grouped: dict[Path, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(route_override_generated_file_path(row), []).append(row)
    for file_path, file_rows in grouped.items():
        write_text_file(
            file_path,
            route_override_file_text(file_rows, object_names),
        )
    write_csv(
        RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.csv",
        route_override_evidence_rows(rows),
    )
    write_text_file(
        RESEARCH_ROOT / "stellar-ai-director-route-overrides-2026-07-06.md",
        route_override_report_text(rows),
    )
    return rows


def planetary_diversity_outpost_value_profile(policy: dict[str, Any]) -> tuple[float, float, float]:
    return PLANETARY_DIVERSITY_OUTPOST_VALUE_PROFILES[str(policy["role"])]


def planetary_diversity_outpost_base_weight(policy: dict[str, Any]) -> int:
    monthly_value, upfront_cost_value, monthly_upkeep_value = planetary_diversity_outpost_value_profile(policy)
    roi = long_term_roi_ratio(monthly_value, upfront_cost_value, monthly_upkeep_value, 0)
    formula_weight = int(max(1000.0, min(400000.0, round(1000.0 * max(1.0, roi)))))
    return max(int(policy["base_weight"]), formula_weight)


def planetary_diversity_outpost_ai_weight_block(policy: dict[str, Any]) -> str:
    monthly_value, upfront_cost_value, monthly_upkeep_value = planetary_diversity_outpost_value_profile(policy)
    lines = [
        "\tai_weight = {",
        f"\t\tfactor = {planetary_diversity_outpost_base_weight(policy)}",
        "",
        f"\t\t# policy_route = planetary_diversity_{policy['role']}",
        "\t\t# Availability owns prerequisites: copied parent potential/allow already gate tech, sites, and resources.",
        "\t\t# Lifetime value formula: (monthly value - upkeep) * months remaining before 2350 - upfront mineral cost value.",
        "\t\tmodifier = { factor = 0 owner = { staid_survival_mode = yes } }",
        "\t\tmodifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }",
        "\t\tmodifier = { factor = 0.35 owner = { staid_recovery_mode = yes } }",
    ]
    for factor, condition in long_term_value_factor_pairs(
        monthly_value,
        upfront_cost_value,
        monthly_upkeep_value,
        divisor=25.0,
        maximum=35,
    ):
        lines.append(f"\t\tmodifier = {{ factor = {factor} {condition} }}")
    for factor, condition in policy["modifiers"]:
        lines.append(f"\t\tmodifier = {{ factor = {factor} {condition} }}")
    lines.append("\t}")
    return "\n".join(lines) + "\n"


def planetary_diversity_outpost_decisions_text() -> str:
    source_path = PLANETARY_DIVERSITY_WORKSHOP_ROOT / PLANETARY_DIVERSITY_OUTPOST_DECISION_SOURCE
    if not source_path.exists():
        raise ValueError(f"Missing Planetary Diversity outpost decision source: {source_path}")
    source_text = read_text(source_path)
    lines = [
        "# Generated by tools/generate_stellar_ai_director_patch.py.",
        "# Full-object override: copied Planetary Diversity outpost decisions with Director-owned AI weighting.",
        "# The copied parent potential/allow blocks decide whether a button exists; Director does not duplicate PD tech/site prerequisite checks.",
        "",
        f"# Source: {PLANETARY_DIVERSITY_OUTPOST_DECISION_SOURCE}",
        "",
    ]
    for policy in PLANETARY_DIVERSITY_OUTPOST_DECISION_POLICY:
        block = extract_top_level_object_text(source_text, policy["decision_id"])
        block = replace_top_level_child_block(block, "ai_weight", planetary_diversity_outpost_ai_weight_block(policy))
        block = "\n".join(line.rstrip() for line in block.splitlines()) + "\n"
        lines.append(f"# planetary_diversity_role = {policy['role']}")
        lines.append(block.rstrip())
        lines.append("")
    text = "\n".join(lines).rstrip() + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def classify_pd_economic_roles(text: str) -> list[str]:
    lowered = text.lower()
    roles = [
        role
        for role, keywords in PD_ECONOMIC_ROLE_KEYWORDS.items()
        if any(keyword in lowered for keyword in keywords)
    ]
    return roles or ["general"]


def pd_top_level_rows(folder: str, source_files: Iterable[str] | None = None) -> list[dict[str, Any]]:
    folder_root = PLANETARY_DIVERSITY_WORKSHOP_ROOT / "common" / folder
    rows: list[dict[str, Any]] = []
    files = [folder_root / name for name in source_files] if source_files else sorted(folder_root.glob("*.txt"))
    for source_path in files:
        if not source_path.exists():
            continue
        parsed = parse_file(source_path)
        source_text = read_text(source_path)
        for assignment in block_assignments(parsed):
            if assignment.key.startswith("@"):
                continue
            try:
                block = extract_top_level_object_text(source_text, assignment.key)
            except ValueError:
                block = f"{assignment.key} = {{}}\n"
            rows.append(
                {
                    "folder": folder,
                    "source_file": source_path.name,
                    "object_id": assignment.key,
                    "roles": classify_pd_economic_roles(block),
                    "has_planet_modifier_block": "planet_modifier" in block,
                }
            )
    return rows


def planetary_diversity_modifier_profile_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in pd_top_level_rows("static_modifiers"):
        row["trigger_kind"] = "has_modifier"
        rows.append(row)
    for row in pd_top_level_rows("deposits"):
        row["trigger_kind"] = "has_deposit"
        rows.append(row)
    for row in pd_top_level_rows("buildings", PD_BUILDING_SOURCE_FILES):
        row["trigger_kind"] = "has_building"
        rows.append(row)
    return rows


def planetary_diversity_role_triggers_text() -> str:
    rows = planetary_diversity_modifier_profile_rows()
    role_rows: dict[str, list[dict[str, Any]]] = {role: [] for role in PD_ROLE_VALUE_PROFILES}
    for row in rows:
        if row["trigger_kind"] not in {"has_modifier", "has_deposit"}:
            continue
        for role in row["roles"]:
            if role in role_rows:
                role_rows[role].append(row)
    lines = [
        "# Generated by tools/generate_stellar_ai_director_patch.py.",
        "# Planet-scope Planetary Diversity value classifiers.",
        "# These triggers let the Director route planet roles/buildings from actual PD modifiers and deposits.",
        "",
    ]
    for role, role_items in role_rows.items():
        lines.append(f"staid_pd_planet_{role}_value = {{")
        if role_items:
            lines.append("\tOR = {")
            for row in sorted(role_items, key=lambda item: (item["trigger_kind"], item["object_id"])):
                lines.append(f"\t\t{row['trigger_kind']} = {row['object_id']}")
            lines.append("\t}")
        else:
            lines.append("\talways = no")
        lines.append("}")
        lines.append("")
    text = "\n".join(lines)
    parse_pdx(text)
    return text


def pd_building_primary_role(block: str) -> str:
    roles = classify_pd_economic_roles(block)
    for preferred in ("research", "alloys", "minerals", "energy", "food", "consumer_goods", "growth", "trade", "unity", "defense"):
        if preferred in roles:
            return preferred
    return roles[0]


def pd_building_ai_weighted_block(block: str, object_id: str) -> str:
    role = pd_building_primary_role(block)
    monthly_value, upfront_cost_value, monthly_upkeep_value = PD_ROLE_VALUE_PROFILES.get(role, (35.0, 350.0, 0.75))
    roi = long_term_roi_ratio(monthly_value, upfront_cost_value, monthly_upkeep_value, 0)
    coefficient = max(4, min(16, int(round(max(1.0, roi) / 20.0))))
    additional = max(400, min(4000, int(round(max(1.0, roi) * 20.0))))
    block = replace_or_insert_top_level_scalar(block, "ai_weight_coefficient", f"\tai_weight_coefficient = {coefficient}")
    block = replace_or_insert_top_level_scalar(block, "additional_ai_weight", f"\tadditional_ai_weight = {additional}")
    modifiers = [
        "\t\tmodifier = { factor = 0 owner = { staid_survival_mode = yes } }",
        "\t\tmodifier = { factor = 0 owner = { staid_core_deficit_short_runway = yes } }",
        f"\t\tmodifier = {{ factor = 8 staid_pd_planet_{role}_value = yes }}",
    ]
    for factor, condition in long_term_value_factor_pairs(
        monthly_value,
        upfront_cost_value,
        monthly_upkeep_value,
        divisor=25.0,
        maximum=30,
    ):
        modifiers.append(f"\t\tmodifier = {{ factor = {factor} {condition} }}")
    if role == "research":
        modifiers.append("\t\tmodifier = { factor = 5 owner = { staid_research_under_curve = yes } }")
    elif role == "alloys":
        modifiers.append("\t\tmodifier = { factor = 5 owner = { staid_militarist_conquest_strategy = yes } }")
    elif role == "growth":
        modifiers.append("\t\tmodifier = { factor = 5 owner = { staid_planetary_capacity_growth_ready = yes } }")
    for modifier in modifiers:
        block = insert_top_level_ai_weight_modifier(block, modifier)
    return "# pd_economic_role = " + role + "\n" + block


def planetary_diversity_buildings_text() -> str:
    source_root = PLANETARY_DIVERSITY_WORKSHOP_ROOT / "common" / "buildings"
    variable_rows: list[dict[str, Any]] = []
    for source_file in PD_BUILDING_SOURCE_FILES:
        source_path = source_root / source_file
        if not source_path.exists():
            continue
        parsed = parse_file(source_path)
        for assignment in block_assignments(parsed):
            if assignment.key.startswith("@"):
                continue
            variable_rows.append(
                {
                    "source_path": str(source_path),
                    "object_id": assignment.key,
                    "generated_file": (MOD_ROOT / "common" / "buildings" / "zzzz_staid_12_planetary_diversity_buildings.txt").as_posix(),
                }
            )
    lines = [
        "# Generated by tools/generate_stellar_ai_director_patch.py.",
        "# Full-object override: copied Planetary Diversity buildings with Director-owned economic ROI weights.",
        "# Availability owns PD prerequisites; weights classify the planet modifier/deposit role and the 2350 horizon payoff.",
        "",
    ]
    variables = route_override_file_variables(variable_rows)
    if variables:
        lines.append("# Source-local variables required by copied Planetary Diversity building objects.")
        lines.extend(variables)
        lines.append("")
    for source_file in PD_BUILDING_SOURCE_FILES:
        source_path = source_root / source_file
        if not source_path.exists():
            continue
        source_text = read_text(source_path)
        parsed = parse_file(source_path)
        lines.append(f"# Source: common/buildings/{source_file}")
        for assignment in block_assignments(parsed):
            if assignment.key.startswith("@"):
                continue
            block = extract_top_level_object_text(source_text, assignment.key)
            block = pd_building_ai_weighted_block(block, assignment.key)
            block = "\n".join(line.rstrip() for line in block.splitlines()) + "\n"
            lines.append(block.rstrip())
            lines.append("")
    text = "\n".join(lines).rstrip() + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def planetary_diversity_naval_capacity_buildings_text() -> str:
    source_path = (
        mod_source_root_for_id("1732447147")
        / "common"
        / "buildings"
        / "pd_arc_buildings.txt"
    )
    source_text = read_text(source_path)
    base = extract_top_level_object_text(source_text, "building_navel_base")
    command = extract_top_level_object_text(source_text, "building_navel_command")
    ai_build_gate = """\t\tOR = {
\t\t\thas_carrier_flag = ignore_ai_building_limitations
\t\t\towner = { is_ai = no }
\t\t\tAND = {
\t\t\t\towner = { staid_naval_capacity_expansion_ready = yes }
\t\t\t\tNOT = { has_research_designation = yes }
\t\t\t}
\t\t}"""
    base = replace_top_level_child_block(
        base,
        "potential",
        """\tpotential = {
\t\texists = owner
\t\tNOR = {
\t\t\thas_modifier = slave_colony
\t\t\thas_modifier = resort_colony
\t\t\thas_modifier = penal_colony
\t\t}
"""
        + ai_build_gate
        + """
\t}""",
    )
    command = replace_top_level_child_block(
        command,
        "allow",
        """\tallow = {
\t\thas_upgraded_capital = yes
"""
        + ai_build_gate
        + """
\t}""",
    )
    destroy_trigger = """\tdestroy_trigger = {
\t\texists = owner
\t\thas_research_designation = yes
\t\towner = { is_ai = yes }
\t}"""
    base = replace_top_level_child_block(base, "destroy_trigger", destroy_trigger)
    command = replace_top_level_child_block(command, "destroy_trigger", destroy_trigger)
    text = """# Generated by tools/generate_stellar_ai_director_patch.py.
# Narrow full-object override of Planetary Diversity - More Arcologies naval administration buildings.
# Vanilla 4.4 construction uses potential/allow as hard AI eligibility filters; building ai_weight is inactive
# while economic plans are enabled. Human placement is preserved. AI construction requires a real naval-capacity
# emergency, is forbidden on research-designated colonies, and existing AI research-world copies are destroyed.

""" + base.rstrip() + "\n\n" + command.rstrip() + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def fortress_colony_types_text() -> str:
    source_path = VANILLA_COMMON_ROOT / "colony_types" / "00_colony_types.txt"
    source_text = read_text(source_path)
    blocks = []
    for object_id in ("col_fortress", "col_habitat_fortress"):
        block = extract_top_level_object_text(source_text, object_id)
        placement_gate = "\t\t\t\tstaid_fortress_planet_strategically_placed = yes"
        if object_id == "col_habitat_fortress":
            placement_gate = """\t\t\t\tOR = {
\t\t\t\t\tstaid_fortress_planet_strategically_placed = yes
\t\t\t\t\thas_building = building_order_keep
\t\t\t\t\thas_building = building_order_castle
\t\t\t\t}"""
        ai_gate = """\t\tOR = {
\t\t\towner = { is_ai = no }
\t\t\tAND = {
\t\t\t\towner = { staid_fortress_designation_ready = yes }
""" + placement_gate + """
\t\t\t}
\t\t}"""
        blocks.append(append_child_block_clause(block, "potential", ai_gate).rstrip())
    text = """# Generated by tools/generate_stellar_ai_director_patch.py.
# Narrow current-vanilla full-object overrides for AI fortress designations.
# Human designation access is preserved. AI fortress worlds require a solvent economy,
# enough colonies to spare one, meaningful naval-capacity use, and a real defensive need.

@stickiness = 10

""" + "\n\n".join(blocks) + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def research_plan_colony_types_text() -> str:
    source_path = VANILLA_COMMON_ROOT / "colony_types" / "00_colony_types.txt"
    source_text = read_text(source_path)
    city = extract_top_level_object_text(source_text, "col_city")
    research = extract_top_level_object_text(source_text, "col_research")
    research = append_child_block_clause(
        research,
        "weight_modifier",
        """\t\t# Native, bounded research specialization: prefer suitable worlds while
\t\t# preserving a soft one-third ceiling and allowing bad roles to unwind.
\t\tmodifier = {
\t\t\tadd = 15
\t\t\tstaid_research_role_candidate = yes
\t\t}
\t\tmodifier = {
\t\t\tfactor = 0.2
\t\t\tOR = {
\t\t\t\tstaid_research_role_reachable = no
\t\t\t\tstaid_research_role_high_conversion_cost = yes
\t\t\t\tAND = {
\t\t\t\t\towner = { staid_research_designation_under_soft_cap = no }
\t\t\t\t\tNOT = { has_designation = col_research }
\t\t\t\t}
\t\t\t}
\t\t}""",
    )
    text = """# Generated by tools/generate_stellar_ai_director_patch.py.
# Narrow current-vanilla full-object overrides for the colony build-out plan.
# Humans retain vanilla designation access. AI roles use native designation
# weights; no event, carrier flag, or forced designation manufactures the role.

@stickiness = 10
@stickiness_low = 5
@zone_rural = 10

""" + city.rstrip() + "\n\n" + research.rstrip() + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def research_world_zone_priority_text() -> str:
    """Make a research designation select zones that unlock research buildings."""
    source_path = VANILLA_COMMON_ROOT / "zones" / "00_zones.txt"
    source_text = read_text(source_path)
    blocks: list[str] = []
    for zone_id in (
        "zone_research",
        "zone_research_physics",
        "zone_research_society",
        "zone_research_engineering",
    ):
        block = extract_top_level_object_text(source_text, zone_id).rstrip()
        closing = block.rfind("\n}")
        if closing < 0:
            raise ValueError(f"Could not find closing brace for {zone_id}")
        priority = """

\t# Bounded follow-through for a selected Tech-World; this is candidate
\t# pressure, not an event-backed directive or guaranteed conversion.
\tadditional_ai_weight = {
\t\tmodifier = {
\t\t\tadd = 5
\t\t\thas_designation = col_research
\t\t\towner = { is_ai = yes }
\t\t}
\t}
""".rstrip()
        blocks.append(block[:closing] + priority + block[closing:] + "\n")
    text = """# Generated by tools/generate_stellar_ai_director_patch.py.
# Narrow Pegasus 4.4.4 full-object overrides for ordinary urban research zones.
# Vanilla building_research_lab_1 requires has_any_research_zone for AI empires;
# this gives a natively selected Tech-World a reachable producer path.

""" + "\n".join(blocks)
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def fortress_army_buildings_text() -> str:
    source_path = VANILLA_COMMON_ROOT / "buildings" / "09_army_buildings.txt"
    source_text = read_text(source_path)
    stronghold = extract_top_level_object_text(source_text, "building_stronghold")
    fortress = extract_top_level_object_text(source_text, "building_fortress")
    stronghold = replace_top_level_child_block(
        stronghold,
        "allow",
        """\tallow = {
\t\texists = owner
\t\tOR = {
\t\t\thas_carrier_flag = ignore_ai_building_limitations
\t\t\towner = { is_ai = no }
\t\t\tAND = {
\t\t\t\tOR = {
\t\t\t\t\thas_modifier = giga_rogue_ai_computer
\t\t\t\t\tAND = {
\t\t\t\t\t\towner = { staid_fortress_designation_ready = yes }
\t\t\t\t\t\tstaid_fortress_planet_strategically_placed = yes
\t\t\t\t\t}
\t\t\t\t}
\t\t\t\tOR = {
\t\t\t\t\thas_any_fortress_zone = yes
\t\t\t\t\tAND = {
\t\t\t\t\t\tnum_buildings = { type = building_stronghold value < 2 }
\t\t\t\t\t\tnum_buildings = { type = building_fortress value < 2 }
\t\t\t\t\t}
\t\t\t\t}
\t\t\t}
\t\t}
\t}""",
    )
    fortress = replace_top_level_child_block(
        fortress,
        "allow",
        """\tallow = {
\t\thas_upgraded_capital = yes
\t\tOR = {
\t\t\towner = { is_ai = no }
\t\t\thas_modifier = giga_rogue_ai_computer
\t\t\tAND = {
\t\t\t\towner = { staid_fortress_designation_ready = yes }
\t\t\t\tstaid_fortress_planet_strategically_placed = yes
\t\t\t}
\t\t}
\t}""",
    )
    text = """# Generated by tools/generate_stellar_ai_director_patch.py.
# Narrow current-vanilla full-object overrides for stronghold construction and upgrades.
# Human and explicit carrier bypasses are preserved. AI military buildings require the
# same strategic/economic readiness gate as fortress designation and fortress zones,
# except for Gigas's rogue-AI planetary computer automation emergency.

""" + stronghold.rstrip() + "\n\n" + fortress.rstrip() + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def gigas_rogue_ai_automation_exception_text() -> str:
    source_path = (
        SNAPSHOT_ROOT
        / "1121692237-gigastructural-engineering-more-44"
        / "common"
        / "colony_automation_exceptions"
        / "giga_rogue_ai.txt"
    )
    handler = extract_top_level_object_text(read_text(source_path), "giga_rogue_ai_planet")
    text = """# Generated by tools/generate_stellar_ai_director_patch.py.
# Exact Gigas 4.4 rogue-AI planetary computer automation handler full-object override.
# Director loads after Gigas, so it preserves the parent handler while the matching
# stronghold override explicitly permits this emergency to construct its defenses.

""" + handler.rstrip() + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def fortress_zone_inline_script_text() -> str:
    source_path = VANILLA_COMMON_ROOT / "inline_scripts" / "zones" / "shared_fortress_zone.txt"
    source_text = read_text(source_path)
    ai_gate = """\tOR = {
\t\towner = { is_ai = no }
\t\tAND = {
\t\t\towner = { staid_fortress_designation_ready = yes }
\t\t\tstaid_fortress_planet_strategically_placed = yes
\t\t}
\t}"""
    text = append_child_block_clause(source_text, "potential", ai_gate, parent_depth=0)
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def write_planetary_diversity_profile_artifacts() -> None:
    rows = planetary_diversity_modifier_profile_rows()
    flat_rows = [
        {
            **{key: value for key, value in row.items() if key != "roles"},
            "roles": ",".join(row["roles"]),
        }
        for row in rows
    ]
    write_csv(RESEARCH_ROOT / "stellar-ai-director-planetary-diversity-profile-2026-07-07.csv", flat_rows)
    role_counts: dict[str, int] = {}
    for row in rows:
        for role in row["roles"]:
            role_counts[role] = role_counts.get(role, 0) + 1
    lines = [
        "# Stellar AI Director Planetary Diversity Profile",
        "",
        "Generated from the active Planetary Diversity workshop source.",
        "",
        "| role | object count |",
        "| --- | ---: |",
    ]
    for role, count in sorted(role_counts.items()):
        lines.append(f"| {role} | {count} |")
    lines.extend(
        [
            "",
            "## Follow-Up Task: Hostile Space Fauna Clearance",
            "",
            "- Inventory crystalline entities, amoebas, mining drones, void clouds, leviathans, and modded equivalents by expected fleet power and rewards.",
            "- Add early fleet reserve pressure for cheap 1k-2k fleet-power clearance targets so AI empires can open blocked hyperlanes, claim guarded systems, and unlock event research instead of idling fleets.",
            "- Keep high-risk leviathan-style targets separate from cheap early blockers; do not make the AI suicide fleets into oversized guardians.",
        ]
    )
    write_text_file(RESEARCH_ROOT / "stellar-ai-director-planetary-diversity-profile-2026-07-07.md", "\n".join(lines) + "\n")


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
        f"staid_tr_is_{row['classification']}_war_goal = {{\n"
        f"\tfrom = {{ using_war_goal = {{ type = {row['war_goal']} owner = root }} }}\n"
        f"}}\n"
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
\t\tif = {{
\t\t\tlimit = {{ staid_tr_is_subjugation_war_goal = yes }}
\t\t\tset_timed_country_flag = {{ flag = staid_tr_war_goal_subjugation days = {THREAT_COUNTRY_FLAG_DAYS} }}
\t\t}}
\t\telse_if = {{
\t\t\tlimit = {{ staid_tr_is_conquest_war_goal = yes }}
\t\t\tset_timed_country_flag = {{ flag = staid_tr_war_goal_conquest days = {THREAT_COUNTRY_FLAG_DAYS} }}
\t\t}}
\t\telse_if = {{
\t\t\tlimit = {{ staid_tr_is_humiliation_war_goal = yes }}
\t\t\tset_timed_country_flag = {{ flag = staid_tr_war_goal_humiliation days = {THREAT_COUNTRY_FLAG_DAYS} }}
\t\t}}
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
\t\t\tlimit = {{ from = {{ has_country_flag = staid_tr_war_goal_subjugation }} }}
\t\t\tadd_opinion_modifier = {{ who = from modifier = staid_tr_anti_aggressor_high }}
\t\t\tset_timed_relation_flag = {{ who = from flag = staid_tr_anti_aggressor_high days = {THREAT_RELATION_FLAG_DAYS} }}
\t\t}}
\t\telse_if = {{
\t\t\tlimit = {{ from = {{ has_country_flag = staid_tr_war_goal_conquest }} }}
\t\t\tadd_opinion_modifier = {{ who = from modifier = staid_tr_anti_aggressor_medium }}
\t\t\tset_timed_relation_flag = {{ who = from flag = staid_tr_anti_aggressor_medium days = {THREAT_RELATION_FLAG_DAYS} }}
\t\t}}
\t\telse_if = {{
\t\t\tlimit = {{ from = {{ has_country_flag = staid_tr_war_goal_humiliation }} }}
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
    return """# Stellar AI Director Threat Response Retirement

## H09a Decision

- Retire the production `on_war_beginning` event chain, galaxy-wide observer
  loop, timed flags, relation writes, and threat-readiness economic subplan.
- Preserve the ten legacy opinion IDs and localization as zero-effect
  compatibility definitions so serialized references in copied saves resolve.
- Do not add a migration event. Existing flags are inert because no production
  trigger, plan, event, or on-action consumes them.

## Save Classification

Cleanup-required, copied-save-only. Static checks prove the absence of new
writes and live consumers. A copied-save runtime check is still required to
prove the retained zero-effect definitions load cleanly while old timed
references expire.

## Follow-up Boundary

Any later threat or arms-race behavior must be a separate native-only,
stateless, bounded slice. It must not restore these event, state, or absolute
income/stockpile mechanisms.
"""


def generate_threat_response_artifacts() -> None:
    for retired_path in threat_response_retired_paths(MOD_ROOT).values():
        retired_path.unlink(missing_ok=True)
    write_text_file(
        MOD_ROOT / "common" / "opinion_modifiers" / "zzz_staid_threat_response_opinions.txt",
        threat_response_opinions_text(),
    )
    write_text_file(
        MOD_ROOT / "localisation" / "english" / "staid_threat_response_l_english.yml",
        threat_response_localisation_text(),
    )
    write_text_file(threat_feasibility_note_path(RESEARCH_ROOT), threat_response_feasibility_note_text())
    write_csv(threat_classification_csv_path(RESEARCH_ROOT), threat_response_classification_rows())


def threat_response_generated_paths(mod_root: Path = MOD_ROOT) -> dict[str, Path]:
    return {
        "opinions": mod_root / "common" / "opinion_modifiers" / "zzz_staid_threat_response_opinions.txt",
        "localisation": mod_root / "localisation" / "english" / "staid_threat_response_l_english.yml",
    }


def threat_response_retired_paths(mod_root: Path = MOD_ROOT) -> dict[str, Path]:
    return {
        "values": mod_root / "common" / "script_values" / "zzz_staid_threat_response_values.txt",
        "triggers": mod_root / "common" / "scripted_triggers" / "zzz_staid_threat_response_triggers.txt",
        "on_actions": mod_root / "common" / "on_actions" / "zzz_staid_threat_response_on_actions.txt",
        "events": mod_root / "events" / "zzz_staid_threat_response_events.txt",
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

    for label, path in threat_response_retired_paths(mod_root).items():
        if path.exists():
            errors.append(f"Retired threat-response {label} file must be absent: {path}")

    opinions = read_text(paths["opinions"]) if paths["opinions"].exists() else ""
    for key in THREAT_OPINION_VALUES:
        block_match = re.search(rf"staid_tr_{re.escape(key)}\s*=\s*\{{(.*?)\}}", opinions, re.DOTALL)
        if block_match is None:
            errors.append(f"Threat-response compatibility opinion is missing: staid_tr_{key}")
        elif not re.search(r"\bopinion\s*=\s*0\b", block_match.group(1)):
            errors.append(f"Threat-response compatibility opinion must be inert: staid_tr_{key}")

    economy_path = mod_root / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
    if economy_path.exists():
        economy = read_text(economy_path)
        for forbidden in (
            "Stellar AI Director threat readiness reserve",
            "has_country_flag = staid_tr_defensive_readiness_low",
            "staid_tr_foreign_affairs_safe = yes",
        ):
            if forbidden in economy:
                errors.append(f"Retired threat-response economy fragment remains live: {forbidden}")

    strategy_path = mod_root / "common" / "scripted_triggers" / "zzzz_staid_20_strategy_kernel_triggers.txt"
    if strategy_path.exists() and "staid_tr_" in read_text(strategy_path):
        errors.append("Strategy kernel still consumes retired staid_tr_ state")

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
        "p15_completion_note": "Short Irony-launched save evidence is retained as historical context only; strategic v2 still requires a final constrained observer run for long-run efficacy proof.",
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
    playset = build_active_playset_snapshot()
    mod_root_resolved = mod_root.resolve()
    parent_roots = [
        Path(row["root"])
        for row in _valuation_stack_roots(playset)
        if Path(row["root"]).resolve() != mod_root_resolved
    ]
    object_names = collect_object_names(snapshot_root, inventory_roots=parent_roots)
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
                object_id = assignment_object_id(object_type, assignment)
                if not object_id or object_id.startswith("@"):
                    continue
                parent_has_object = object_id in object_names.get(object_type, set())
                lower_text = text.lower()
                if parent_has_object and "full-object" in lower_text and "override" in lower_text:
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
                        "object_name": object_id,
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
        if file_path.relative_to(common).parts[0] == "inline_scripts":
            continue
        try:
            parsed = parse_file(file_path)
        except PDXParseError:
            continue
        for assignment in iter_assignments(parsed):
            value = atom_value(assignment.value)
            if value and re.fullmatch(r"\$[A-Za-z0-9_.:-]+\$", value):
                # Legal parameter of a scripted value/effect, not an object ID.
                continue
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


STALE_STELLAR_AI_REQUIREMENT_PATTERNS = (
    re.compile(r"\brequires?\s+Stellar AI\b", re.IGNORECASE),
    re.compile(
        r"\bStellar AI\s+(?:is|remains|must be|should be|needs to be)\s+"
        r"(?:a\s+)?(?:required|required parent|required dependency|launch dependency|dependency)",
        re.IGNORECASE,
    ),
    re.compile(r"\brequired\s+(?:launch\s+)?dependency\s*:\s*Stellar AI\b", re.IGNORECASE),
)
SAFE_STELLAR_AI_CONTEXT_RE = re.compile(
    r"\b(no longer|not|omits?|without|private parity|reference only|not a launch dependency|not a required parent)\b",
    re.IGNORECASE,
)
CURRENT_STANDALONE_DOCS = (
    Path("README.md"),
    Path("notes/load-order.md"),
)
FORBIDDEN_GENERATED_SURFACES = (
    Path("common/country_types"),
    Path("common/diplomatic_actions"),
    Path("common/personalities"),
    Path("common/ship_designs"),
    Path("common/component_templates"),
    Path("common/section_templates"),
    Path("common/ship_sizes"),
)
RESEARCHED_GENERATED_SURFACE_ALLOWLIST = {
    Path("common/component_templates"),
    Path("common/country_types"),
    Path("common/personalities"),
    Path("common/ship_sizes"),
}


def line_implies_stellar_ai_required(line: str) -> bool:
    if "Stellar AI" not in line:
        return False
    if SAFE_STELLAR_AI_CONTEXT_RE.search(line):
        return False
    return any(pattern.search(line) for pattern in STALE_STELLAR_AI_REQUIREMENT_PATTERNS)


def stale_stellar_ai_dependency_errors(
    mod_root: Path = MOD_ROOT,
    research_root: Path = RESEARCH_ROOT,
) -> list[str]:
    errors: list[str] = []
    descriptor_path = mod_root / "descriptor.mod"
    if descriptor_path.exists() and "Stellar AI" in descriptor_dependencies(read_text(descriptor_path)):
        errors.append(f"{descriptor_path}: descriptor must not require Stellar AI as a launch dependency")

    doc_paths = [mod_root / relative for relative in CURRENT_STANDALONE_DOCS]
    doc_paths.append(research_root / "README.md")
    for path in doc_paths:
        if not path.exists():
            continue
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            if line_implies_stellar_ai_required(line):
                errors.append(f"{path}:{line_number}: current docs must not imply Stellar AI is required")
    return errors


def forbidden_generated_surface_errors(
    mod_root: Path = MOD_ROOT,
    allowed_surfaces: set[Path] | None = None,
) -> list[str]:
    allowed = allowed_surfaces if allowed_surfaces is not None else RESEARCHED_GENERATED_SURFACE_ALLOWLIST
    errors: list[str] = []
    for relative in FORBIDDEN_GENERATED_SURFACES:
        if relative in allowed:
            continue
        path = mod_root / relative
        if path.exists():
            errors.append(f"{path}: forbidden generated surface exists without a researched task flag")
    return errors


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


def unresolved_template_placeholder_count(text: str, *, allow_scripted_effect_parameters: bool = False) -> int:
    patterns = [
        r"__PLACEHOLDER_[A-Za-z0-9_]+__",
        r"\bTODO\b",
        r"\bPLACEHOLDER\b",
    ]
    if not allow_scripted_effect_parameters:
        patterns.append(r"\$[A-Za-z0-9_.:-]+\$")
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
        placeholder_count = unresolved_template_placeholder_count(
            text,
            allow_scripted_effect_parameters=folder
            in {"inline_scripts", "script_values", "scripted_effects", "scripted_modifiers"},
        )
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
        elif top_level_object_count == 0 and folder != "component_tags":
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
        "staid_static_defense_threat_window",
        "staid_static_defense_investment_ready",
        "staid_core_deficit_short_runway = yes",
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
    decisions_path = repo_root / "mods/StellarAIDirector/common/decisions/zzzz_staid_12_planetary_diversity_outpost_decisions.txt"
    naval_gate_path = repo_root / "mods/StellarAIDirector/common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt"
    required_economy_terms = {
        "Stellar AI Director planetary capacity reserve",
        "Stellar AI Director Planetary Diversity outpost reserve",
        "Stellar AI Director safe research baseline",
        "staid_planetary_capacity_growth_ready = yes",
        "staid_planetary_diversity_outpost_investment_ready = yes",
        "staid_research_construction_priority_ready = yes",
        "pops = 400000",
        "minerals = 500",
    }
    required_trigger_terms = {
        "staid_planetary_capacity_growth_ready",
        "staid_core_deficit_short_runway = yes",
        "resource_stockpile_compare = { resource = minerals value > 5000 }",
        "has_monthly_income = { resource = minerals value > 100 }",
        "staid_pd_research_outpost_priority_ready",
        "resource_stockpile_compare = { resource = minerals value > 1200 }",
    }
    required_note_terms = {
        "planetary-capacity policy",
        "safe research economic-plan demand",
        "hard naval-capacity eligibility",
        "planetary diversity outpost decisions",
    }
    if not (
        economy_path.exists()
        and triggers_path.exists()
        and tuning_path.exists()
        and decisions_path.exists()
        and naval_gate_path.exists()
    ):
        return False
    try:
        parse_file(economy_path)
        parse_file(triggers_path)
        parse_file(decisions_path)
        parse_file(naval_gate_path)
    except PDXParseError:
        return False
    economy = read_text(economy_path)
    triggers = read_text(triggers_path)
    tuning = (
        read_text(tuning_path)
        + "\n"
        + read_text(decisions_path)
        + "\n"
        + read_text(naval_gate_path)
    ).lower()
    return (
        all(term in economy for term in required_economy_terms)
        and all(term in triggers for term in required_trigger_terms)
        and all(term in tuning for term in required_note_terms)
        and "decision_build_pd_research_base" in tuning
        and "availability owns prerequisites" in tuning
        and "building_navel_base" in tuning
        and "not = { has_research_designation = yes }" in tuning
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
    categories_path = repo_root / "mods/StellarAIDirector/common/tradition_categories/zzzz_staid_02_perks_traditions_tradition_categories.txt"
    traditions_path = repo_root / "mods/StellarAIDirector/common/traditions/zzzz_staid_02_perks_traditions_traditions.txt"
    reference_audit_path = repo_root / "research/stellar-ai/stellar-ai-director-generated-reference-audit-2026-07-04.csv"
    required_paths = [economy_path, triggers_path, tuning_path, reference_audit_path, technology_path, ascension_path, categories_path, traditions_path]
    if not all(path.exists() for path in required_paths):
        return False
    try:
        for path in (economy_path, triggers_path, technology_path, ascension_path, categories_path, traditions_path):
            parse_file(path)
    except PDXParseError:
        return False
    with reference_audit_path.open(encoding="utf-8", newline="") as handle:
        if any(row.get("status") == "missing" for row in csv.DictReader(handle)):
            return False
    economy = read_text(economy_path)
    triggers = read_text(triggers_path)
    tuning = (
        read_text(tuning_path)
        + "\n"
        + read_text(technology_path)
        + "\n"
        + read_text(ascension_path)
        + "\n"
        + read_text(categories_path)
        + "\n"
        + read_text(traditions_path)
    ).lower()
    return (
        "Stellar AI Director modded unlock research reserve" in economy
        and "staid_core_unlock_research_priority_ready = yes" in economy
        and "staid_core_unlock_research_priority_ready" in triggers
        and "has_technology = tech_mega_engineering" in triggers
        and "has_technology = tech_mega_shipyard" in triggers
        and "unlock-research policy" in tuning
        and "direct technology/ap/tradition category/node route overrides are emitted" in tuning
        and "tech_mega_engineering" in tuning
        and "ap_celestial_printing" in tuning
        and "tradition_supremacy" in tuning
        and "tr_discovery_science_division" in tuning
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
        "common/opinion_modifiers/zzz_staid_threat_response_opinions.txt",
        "common/script_values/zzz_staid_roi_values.txt",
        "common/scripted_triggers/zzz_staid_decision_state_triggers.txt",
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
        and "direct technology/ap/tradition category/node route overrides are emitted" in tuning
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


def opening_strategy_triggers_text() -> str:
    return '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Computed opening classifier for the first 75-year strategy kernel.

staid_opening_direct_research = {
\tstaid_is_opening_phase = yes
\tstaid_can_afford_research_push = yes
\tOR = {
\t\thas_ethic = ethic_materialist
\t\thas_ethic = ethic_fanatic_materialist
\t\thas_authority = auth_machine_intelligence
\t\thas_civic = civic_technocracy
\t}
}

staid_opening_unity_to_research = {
\tstaid_is_opening_phase = yes
\tstaid_has_safe_basic_stockpiles = yes
\tOR = {
\t\thas_ethic = ethic_spiritualist
\t\thas_ethic = ethic_fanatic_spiritualist
\t\thas_civic = civic_exalted_priesthood
\t\thas_civic = civic_death_cult
\t}
}

staid_opening_military_to_pops = {
\tstaid_is_opening_phase = yes
\tstaid_has_safe_basic_stockpiles = yes
\tNOT = { has_deficit = alloys }
\tOR = {
\t\thas_ethic = ethic_militarist
\t\thas_ethic = ethic_fanatic_militarist
\t\thas_ethic = ethic_authoritarian
\t\thas_ethic = ethic_fanatic_authoritarian
\t}
}

staid_opening_hostile_fauna_clearance = {
\tstaid_is_opening_phase = yes
\tstaid_has_safe_basic_stockpiles = yes
\tNOT = { has_deficit = alloys }
\tOR = {
\t\thas_ethic = ethic_militarist
\t\thas_ethic = ethic_fanatic_militarist
\t\thas_ethic = ethic_xenophobe
\t\thas_ethic = ethic_fanatic_xenophobe
\t\thas_authority = auth_machine_intelligence
\t}
}

staid_opening_defensive_tall_research = {
\tstaid_is_opening_phase = yes
\tstaid_can_afford_research_push = yes
\tOR = {
\t\thas_ethic = ethic_pacifist
\t\thas_ethic = ethic_fanatic_pacifist
\t\thas_ethic = ethic_xenophobe
\t\thas_ethic = ethic_fanatic_xenophobe
\t}
}

staid_opening_trade_to_research = {
\tstaid_is_opening_phase = yes
\tstaid_has_safe_basic_stockpiles = yes
\tOR = {
\t\thas_ethic = ethic_xenophile
\t\thas_ethic = ethic_fanatic_xenophile
\t\thas_civic = civic_merchant_guilds
\t\thas_civic = civic_corporate_dominion
\t}
}

staid_opening_hive_growth_research = {
\tstaid_is_opening_phase = yes
\tstaid_has_safe_basic_stockpiles = yes
\thas_authority = auth_hive_mind
}

staid_opening_machine_growth_research = {
\tstaid_is_opening_phase = yes
\tstaid_has_safe_basic_stockpiles = yes
\thas_authority = auth_machine_intelligence
}

staid_opening_nomad_arkship_research = {
\tstaid_is_opening_phase = yes
\tis_nomadic = yes
\tstaid_has_safe_basic_stockpiles = yes
}

staid_opening_any_research_route = {
\tOR = {
\t\tstaid_opening_direct_research = yes
\t\tstaid_opening_unity_to_research = yes
\t\tstaid_opening_defensive_tall_research = yes
\t\tstaid_opening_trade_to_research = yes
\t\tstaid_opening_hive_growth_research = yes
\t\tstaid_opening_machine_growth_research = yes
\t\tstaid_opening_nomad_arkship_research = yes
\t}
}
'''


def strategy_kernel_triggers_text() -> str:
    return '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Computed strategic state shared by economy, policy, edict, technology, fleet,
# and native war-planning weights. No trigger in this file mutates game state.

staid_is_opening_phase = {
	years_passed < 75
}

# Stellar AI 0.10 used a roughly forty-year peaceful expansion opening, but
# explicitly exited that posture when war or physical containment demanded it.
# Director keeps its longer economic opening while using this narrower trigger
# only for diplomacy and war-support spending.
staid_is_diplomatic_opening_phase = {
	years_passed < 40
	is_at_war = no
	NOT = { staid_boxed_in_war_pressure = yes }
}

staid_is_midgame_scaling_phase = {
	years_passed > 44
	years_passed < 120
}

staid_is_crisis_scaling_phase = {
	years_passed > 119
}

staid_has_safe_basic_stockpiles = {
	NOT = { has_deficit = energy }
	NOT = { has_deficit = minerals }
	NOT = { has_deficit = food }
	NOT = { has_deficit = consumer_goods }
	resource_stockpile_percent = { resource = energy value > 0.10 }
	resource_stockpile_percent = { resource = minerals value > 0.10 }
}

staid_can_afford_research_push = {
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_has_safe_basic_stockpiles = yes
		staid_high_scale_snowball_pressure = yes
		staid_construction_spenddown_pressure = yes
	}
	OR = {
		staid_research_input_runway_safe = yes
		staid_high_scale_snowball_pressure = yes
		staid_construction_spenddown_pressure = yes
	}
}

staid_security_threatened = {
	staid_crisis_starbase_pressure = yes
}

staid_security_existential = {
	OR = {
		staid_crisis_starbase_pressure = yes
		AND = {
			staid_security_threatened = yes
			NOT = { staid_shipyard_payoff_ready = yes }
		}
	}
}

# Topology-backed boxed-in state. The vanilla `has_bordering_system` scripted
# trigger checks owned border systems for an intel-visible, unowned, peacefully
# claimable hyperlane neighbor. Do not use `has_ai_expansion_plan`: TEST_2231
# proved that internal planning state can remain active after every peaceful
# territorial exit is gone. Native targets, CBs, war goals, and declarations
# remain engine-owned.
staid_boxed_in_war_pressure = {
	is_nomadic = no
	is_at_war = no
	has_country_flag = has_encountered_other_empire
	has_bordering_system = no
	NOT = { has_ethic = ethic_pacifist }
	NOT = { has_ethic = ethic_fanatic_pacifist }
	OR = {
		has_ai_personality_behaviour = propagator
		has_ai_personality_behaviour = conqueror
		has_ai_personality_behaviour = subjugator
		has_ai_personality_behaviour = opportunist
		num_owned_planets < 8
	}
}

staid_native_war_posture_active = {
	NOT = { is_pacifist = yes }
	OR = {
		staid_boxed_in_war_pressure = yes
		staid_militarist_conquest_strategy = yes
		staid_raiding_pop_growth_strategy = yes
		has_ai_personality_behaviour = conqueror
		has_ai_personality_behaviour = subjugator
		has_ai_personality_behaviour = purger
		has_ai_personality_behaviour = opportunist
	}
}

# Shared mineral/alloy competition signal. This reserves logistics capacity but
# never creates armies, fleets, claims, casus belli, targets, or wars.
staid_war_logistics_pressure = {
	OR = {
		is_at_war = yes
		recently_lost_war = yes
		staid_boxed_in_war_pressure = yes
		staid_militarist_conquest_strategy = yes
		staid_raiding_pop_growth_strategy = yes
		staid_security_threatened = yes
	}
}

# Pegasus 4.4.5 fixed an executable defect where high naval capacity could
# suppress declarations. 4.4.4 cannot receive that code fix, so the native
# workaround is to stop peacetime ship expansion before fleets sit permanently
# at full capacity. Wartime, crisis, and defensive-emergency spending bypass it.
staid_peacetime_high_naval_capacity_guard = {
	is_at_war = no
	used_naval_capacity_percent >= 0.80
	NOT = { recently_lost_war = yes }
	NOT = { staid_security_existential = yes }
	NOT = { has_ascension_perk = ap_become_the_crisis }
}

staid_megastructure_prereq_release = {
	staid_megastructure_prep_ready = yes
	staid_can_afford_research_push = yes
}

staid_megastructure_alloy_release = {
	staid_megastructure_commit_safe = yes
	NOT = { staid_security_existential = yes }
}

staid_fleet_defensive_minimum_mode = {
	OR = {
		staid_security_threatened = yes
		staid_shipyard_expansion_ready = yes
	}
}

staid_fleet_strategic_aggression_mode = {
	OR = {
		staid_fleet_payoff_exploitation_ready = yes
		AND = {
			used_naval_capacity_percent < 1.40
			has_monthly_income = { resource = alloys value > 80 }
		}
		staid_hostile_fauna_clearance_strategy = yes
	}
	NOT = { staid_security_existential = yes }
}

staid_fleet_survival_emergency_mode = {
	staid_security_existential = yes
}

staid_opening_route_research_priority = {
	OR = {
		staid_opening_any_research_route = yes
		staid_research_under_curve = yes
	}
}
'''


def fleet_doctrine_triggers_text() -> str:
    return '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Fleet doctrine classifiers for tech and spend weights. These do not force ship designs.

staid_fleet_energy_shield_doctrine = {
\tstaid_fleet_defensive_minimum_mode = yes
\tOR = {
\t\thas_ethic = ethic_materialist
\t\thas_ethic = ethic_fanatic_materialist
\t\thas_technology = tech_lasers_2
\t\thas_technology = tech_shields_2
\t}
}

staid_fleet_kinetic_armor_doctrine = {
\tstaid_fleet_defensive_minimum_mode = yes
\tOR = {
\t\thas_ethic = ethic_militarist
\t\thas_ethic = ethic_fanatic_militarist
\t\thas_technology = tech_mass_drivers_2
\t\thas_technology = tech_ship_armor_2
\t}
}

staid_fleet_missile_evasion_doctrine = {
\tstaid_fleet_strategic_aggression_mode = yes
\tOR = {
\t\thas_technology = tech_missiles_2
\t\thas_technology = tech_afterburners_1
\t\thas_technology = tech_thrusters_2
\t}
}

staid_fleet_carrier_strikecraft_doctrine = {
\tOR = {
\t\tstaid_fleet_strategic_aggression_mode = yes
\t\tstaid_is_midgame_scaling_phase = yes
\t}
\tOR = {
\t\thas_technology = tech_space_whale_weapon_1
\t\thas_technology = tech_strike_craft_1
\t\thas_technology = tech_starbase_3
\t}
}

staid_fleet_balanced_filler_doctrine = {
\tNOT = { staid_fleet_energy_shield_doctrine = yes }
\tNOT = { staid_fleet_kinetic_armor_doctrine = yes }
\tNOT = { staid_fleet_missile_evasion_doctrine = yes }
\tNOT = { staid_fleet_carrier_strikecraft_doctrine = yes }
}
'''


def archetype_triggers_text() -> str:
    try:
        from tools.stellar_ai_archetype_triggers import render_archetype_triggers
    except ModuleNotFoundError:
        from stellar_ai_archetype_triggers import render_archetype_triggers

    rendered = render_archetype_triggers(
        VANILLA_COMMON_ROOT / "personalities" / "00_personalities.txt"
    )
    parse_pdx(rendered)
    return rendered


def opening_growth_policies_text(*, identity_overlay: bool = True) -> str:
    diplomatic_block = find_verified_source_object_block("policies", "diplomatic_stance")
    bombardment_block = find_verified_source_object_block("policies", "orbital_bombardment")
    surrender_block = find_verified_source_object_block("policies", "orbital_bombardment_accept_surrender")

    cooperative_opening = """\t\t\tmodifier = {
\t\t\t\tfactor = 2
\t\t\t\tstaid_is_diplomatic_opening_phase = yes
\t\t\t\tstaid_opening_any_research_route = yes
\t\t\t\tNOT = { staid_security_existential = yes }
\t\t\t\tNOT = { staid_native_war_posture_active = yes }
\t\t\t\tnum_rivals = 0
\t\t\t}"""
    cooperative_exit = "\t\t\tmodifier = { factor = 0 staid_native_war_posture_active = yes }"
    cooperative_identity = (
        "\t\t\tmodifier = { factor = 1.40 staid_archetype_diplomatic = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes }"
    )
    cooperative_secondary_diplomatic = (
        "\t\t\tmodifier = { factor = 1.15 staid_archetype_lead_secondary_diplomatic = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes }"
    )
    cooperative_research = (
        "\t\t\tmodifier = { factor = 1.15 staid_archetype_research = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes }"
    )
    cooperative_secondary_research = (
        "\t\t\tmodifier = { factor = 1.10 staid_archetype_lead_secondary_research = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes }"
    )
    cooperative_subject = "\t\t\tmodifier = { factor = 1.15 staid_role_subject = yes }"
    belligerent_native = "\t\t\tmodifier = { factor = 2 staid_native_war_posture_active = yes }"
    belligerent_boxed = "\t\t\tmodifier = { factor = 8 staid_boxed_in_war_pressure = yes }"
    mercantile_opening = "\t\t\tmodifier = { factor = 5 staid_opening_trade_to_research = yes staid_is_diplomatic_opening_phase = yes }"
    mercantile_exit = "\t\t\tmodifier = { factor = 0.25 staid_native_war_posture_active = yes }"
    mercantile_identity = (
        "\t\t\tmodifier = { factor = 1.40 staid_identity_megacorp = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes }"
    )
    isolationist_identity = (
        "\t\t\tmodifier = { factor = 1.40 staid_archetype_defensive = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes "
        "has_federation = no staid_role_subject = no is_at_war = no "
        "staid_native_war_posture_active = no }"
    )
    isolationist_secondary = (
        "\t\t\tmodifier = { factor = 1.15 staid_archetype_lead_secondary_defensive = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes "
        "has_federation = no staid_role_subject = no is_at_war = no "
        "staid_native_war_posture_active = no }"
    )
    expansionist_opening = "\t\t\tmodifier = { factor = 4 staid_opening_military_to_pops = yes staid_is_diplomatic_opening_phase = yes staid_has_safe_basic_stockpiles = yes }"
    expansionist_exit = "\t\t\tmodifier = { factor = 0.25 staid_native_war_posture_active = yes }"
    expansionist_boxed = "\t\t\tmodifier = { factor = 0.10 staid_boxed_in_war_pressure = yes }"
    supremacist_native = "\t\t\tmodifier = { factor = 6 staid_native_war_posture_active = yes }"
    supremacist_boxed = "\t\t\tmodifier = { factor = 8 staid_boxed_in_war_pressure = yes }"

    for option in ("diplo_stance_belligerent", "diplo_stance_belligerent_nomad"):
        try:
            diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, option, belligerent_native)
            diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, option, belligerent_boxed)
        except ValueError:
            if option.endswith("_nomad"):
                continue
            raise
    for option in ("diplo_stance_cooperative", "diplo_stance_cooperative_nomad"):
        diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, option, cooperative_opening)
        diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, option, cooperative_exit)
    if identity_overlay:
        for modifier in (
            cooperative_identity,
            cooperative_secondary_diplomatic,
            cooperative_research,
            cooperative_secondary_research,
            cooperative_subject,
        ):
            diplomatic_block = insert_policy_option_ai_weight_modifier(
                diplomatic_block, "diplo_stance_cooperative", modifier
            )
    diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, "diplo_stance_mercantile", mercantile_opening)
    diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, "diplo_stance_mercantile", mercantile_exit)
    if identity_overlay:
        diplomatic_block = insert_policy_option_ai_weight_modifier(
            diplomatic_block, "diplo_stance_mercantile", mercantile_identity
        )
        for modifier in (isolationist_identity, isolationist_secondary):
            diplomatic_block = insert_policy_option_ai_weight_modifier(
                diplomatic_block, "diplo_stance_isolationist", modifier
            )
    diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, "diplo_stance_expansionist", expansionist_opening)
    diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, "diplo_stance_expansionist", expansionist_exit)
    diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, "diplo_stance_expansionist", expansionist_boxed)
    for option in ("diplo_stance_supremacist", "diplo_stance_supremacist_nomad"):
        diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, option, supremacist_native)
        diplomatic_block = insert_policy_option_ai_weight_modifier(diplomatic_block, option, supremacist_boxed)

    conquest_bombardment = "\t\t\tmodifier = { factor = 18 staid_militarist_conquest_strategy = yes }"
    opening_bombardment = "\t\t\tmodifier = { factor = 8 staid_opening_military_to_pops = yes staid_has_safe_basic_stockpiles = yes }"
    bombardment_block = insert_policy_option_ai_weight_modifier(
        bombardment_block, "orbital_bombardment_indiscriminate", conquest_bombardment
    )
    bombardment_block = insert_policy_option_ai_weight_modifier(
        bombardment_block, "orbital_bombardment_indiscriminate", opening_bombardment
    )
    forbidden_ai_weight = """\t\tai_weight = {
\t\t\tbase = 1
\t\t\tmodifier = { factor = 80 staid_raiding_pop_growth_strategy = yes }
\t\t\tmodifier = { factor = 20 staid_militarist_conquest_strategy = yes }
\t\t\tmodifier = { factor = 8 staid_opening_military_to_pops = yes staid_has_safe_basic_stockpiles = yes }
\t\t\tmodifier = {
\t\t\t\tfactor = 0.01
\t\t\t\tNOT = { staid_raiding_pop_growth_strategy = yes }
\t\t\t\tNOT = { staid_militarist_conquest_strategy = yes }
\t\t\t\tNOT = { staid_opening_military_to_pops = yes }
\t\t\t}
\t\t}"""
    surrender_block = replace_policy_option_ai_weight(
        surrender_block, "orbital_bombardment_surrender_forbidden", forbidden_ai_weight
    )

    text = "\n".join(block.rstrip() for block in (diplomatic_block, bombardment_block, surrender_block)) + "\n"
    parse_pdx(text)
    return (
        "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
        "# Pegasus 4.4.4 full-object policy overrides. Native option legality and all non-AI fields are preserved.\n"
        "# The peaceful opening exits at war pressure; boxed-in empires strongly prefer Belligerent/Supremacist posture.\n\n"
        + text
    )


def render_identity_diplomatic_stance_artifacts() -> dict[Path, str]:
    """Render the single existing policy artifact owned by the identity stance slice."""

    artifacts = {IDENTITY_DIPLOMATIC_STANCE_PATH: opening_growth_policies_text()}
    if tuple(artifacts) != (IDENTITY_DIPLOMATIC_STANCE_PATH,):
        raise ValueError("Identity diplomatic stance renderer violated its fixed output allowlist")
    for text in artifacts.values():
        parse_pdx(text)
    return artifacts


def militarist_bombardment_stances_text() -> str:
    block = find_verified_source_object_block("bombardment_stances", "raiding")
    ai_weight = """\tai_weight = {
\t\tweight = 80
\t\tmodifier = {
\t\t\tfactor = 0
\t\t\texists = from
\t\t\tfrom = {
\t\t\t\tOR = {
\t\t\t\t\tpop_amount < 200
\t\t\t\t\towner = { NOT = { is_hostile = root.owner } }
\t\t\t\t}
\t\t\t}
\t\t}
\t\tmodifier = { factor = 60 owner = { staid_raiding_pop_growth_strategy = yes } }
\t\tmodifier = { factor = 25 owner = { staid_militarist_conquest_strategy = yes } }
\t\tmodifier = { factor = 8 owner = { staid_opening_military_to_pops = yes } }
\t\tmodifier = {
\t\t\tfactor = 0.25
\t\t\texists = from
\t\t\tfrom = { owner = { has_claim = root.solar_system } }
\t\t}
\t}"""
    block = replace_top_level_child_block(block, "ai_weight", ai_weight)
    parse_pdx(block)
    return (
        "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
        "# Full-object override: vanilla raiding bombardment stance with Director-owned abduct-pop AI weighting.\n\n"
        + block
    )


def opening_growth_edicts_text() -> str:
    targets = {
        "research_subsidies": "\t\tmodifier = { factor = 12 staid_opening_route_research_priority = yes staid_can_afford_research_push = yes }",
        "encourage_free_thought": "\t\tmodifier = { factor = 8 staid_opening_route_research_priority = yes staid_can_afford_research_push = yes }",
        "map_the_stars": "\t\tmodifier = { factor = 5 staid_is_opening_phase = yes staid_has_safe_basic_stockpiles = yes }",
        "capacity_subsidies": "\t\tmodifier = { factor = 6 staid_is_opening_phase = yes NOT = { has_deficit = energy } }",
        "mining_subsidies": "\t\tmodifier = { factor = 6 staid_is_opening_phase = yes NOT = { has_deficit = minerals } }",
        "farming_subsidies": "\t\tmodifier = { factor = 4 staid_is_opening_phase = yes NOT = { has_deficit = food } }",
        "fortify_the_border": "\t\tmodifier = { factor = 6 staid_security_threatened = yes }",
    }
    blocks = [
        "# Generated by tools/generate_stellar_ai_director_patch.py.",
        "# Verified full-object edict overrides from installed vanilla edicts.",
        "# Required source-local @variables are copied into this file to preserve vanilla parse context.",
        "@Edict1Cost = 10",
        "@Edict2Cost = 20",
        "@Edict3Cost = 30",
        "@EdictPerpetual = -1",
        "@EdictHighPrio = 100",
        "@EdictMedPrio = 10",
        "",
    ]
    for object_id, modifier in targets.items():
        block = find_verified_source_object_block("edicts", object_id)
        block = insert_top_level_ai_weight_modifier(block, modifier)
        parse_pdx(block)
        blocks.append(block.rstrip())
        blocks.append("")
    return "\n".join(blocks).rstrip() + "\n"


def standalone_parity_inventory_rows() -> list[dict[str, str]]:
    return [
        {
            "surface": "descriptor_dependencies",
            "classification": "reimplement",
            "baseline_status": "implemented",
            "director_evidence": "mods/StellarAIDirector/descriptor.mod",
            "stellar_ai_reference": "Stellar AI is private parity evidence only; descriptor dependency intentionally omitted.",
            "parity_note": "Director can launch without declaring Stellar AI once static validation passes.",
        },
        {
            "surface": "common/ai_budget",
            "classification": "absorb_reimplement",
            "baseline_status": "implemented",
            "director_evidence": "common/ai_budget/zzz_staid_alloys_budget.txt; common/ai_budget/zzz_staid_gigas_resource_budgets.txt; common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt",
            "stellar_ai_reference": "Stellar AI budget behavior used as private reference for alloy/construction reserve policy.",
            "parity_note": "The active parent owns generic megastructure alloy reserves; Director budgets cover bounded Gigas resources, fleet conversion, and construction pressure without a Stellar AI runtime dependency.",
        },
        {
            "surface": "common/economic_plans",
            "classification": "absorb_reimplement",
            "baseline_status": "implemented",
            "director_evidence": "common/economic_plans/zzzz_staid_additive_economic_plan.txt",
            "stellar_ai_reference": "Stellar AI basic economy plan used as private parity source for high-scale AI economy spine.",
            "parity_note": "Director replaces basic_economy_plan with survival, research, construction, trade, fleet-throughput, static-defense, and high-scale reserve subplans.",
        },
        {
            "surface": "buildings/districts/jobs/zones",
            "classification": "targeted_reimplement",
            "baseline_status": "implemented_for_baseline",
            "director_evidence": "common/buildings/zzzz_staid_13_dataset_job_pressure_buildings.txt; common/districts/zzzz_staid_13_dataset_job_pressure_districts.txt; generated dataset job-pressure audit",
            "stellar_ai_reference": "Parent AI support and active-stack valuation datasets preserve source provenance.",
            "parity_note": "Baseline covers safe building, district, and zone construction pressure through ai_resource_production; broad job automation remains deferred.",
        },
        {
            "surface": "colony_types_designations_planet_roles",
            "classification": "targeted_reimplement",
            "baseline_status": "implemented_for_baseline",
            "director_evidence": "common/decisions/zzzz_staid_12_planetary_diversity_outpost_decisions.txt; common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt; common/economic_plans/zzzz_staid_additive_economic_plan.txt",
            "stellar_ai_reference": "Stellar AI/active-stack planet automation was used as parity context, but no broad colony_type rewrite is emitted.",
            "parity_note": "Director supports high-value planetary diversity/outpost and capacity pressure while deferring broad colony-type/personality-style rewrites.",
        },
        {
            "surface": "personalities_diplomacy_war",
            "classification": "absorb_reimplement_native",
            "baseline_status": "implemented_static_needs_runtime",
            "director_evidence": "common/personalities/zzzzz_staid_16_standalone_war_pressure.txt; common/policies/zzzz_staid_10_opening_growth_policies.txt; common/country_types/zzzzz_staid_18_native_war_readiness.txt; common/ai_budget/zzzz_staid_14_army_recruitment_budget.txt; common/scripted_triggers/zzzz_staid_20_strategy_kernel_triggers.txt",
            "stellar_ai_reference": "Stellar AI 0.10 personality values and temporary peaceful-opening pattern are absorbed without a runtime dependency.",
            "parity_note": "Director now owns complete 4.4.4 personality copies, native posture transitions, boxed-in claim/logistics pressure, and pre-planner readiness repair while declarations, CBs, war goals, target choice, and fleets remain engine-owned.",
        },
        {
            "surface": "policies_edicts_defines",
            "classification": "reimplement",
            "baseline_status": "implemented",
            "director_evidence": "common/policies/zzzz_staid_10_opening_growth_policies.txt; common/edicts/zzzz_staid_10_opening_growth_edicts.txt; common/defines/zzzz_staid_14_high_scale_ai_defines.txt",
            "stellar_ai_reference": "Stellar AI opening/growth pressure informed parity goals; Director emits standalone policy/edict/define AI weights.",
            "parity_note": "Baseline covers growth, research conversion, diplomacy stance pressure, construction scoring, and high-scale AI refresh/target tuning.",
        },
        {
            "surface": "research_economy_fleet_conversion",
            "classification": "reimplement",
            "baseline_status": "implemented",
            "director_evidence": "common/technology/zzzz_staid_01_unlock_technology_technology.txt; common/tradition_categories/zzzz_staid_02_perks_traditions_tradition_categories.txt; common/traditions/zzzz_staid_02_perks_traditions_traditions.txt; common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt; fleet-throughput economic subplans",
            "stellar_ai_reference": "Stellar AI research/economy spine used as parity reference for mandatory unlock and fleet payoff routing.",
            "parity_note": "Director pushes Mega Engineering, Mega Shipyard, Gigas, NSC3, ESC, AP/tradition, and fleet-throughput routes directly.",
        },
        {
            "surface": "generated_conflict_winners",
            "classification": "validate_preserve_or_intentional_override",
            "baseline_status": "implemented",
            "director_evidence": "stellar-ai-director-generated-conflicts-2026-07-04.csv; stellar-ai-director-generated-reference-audit-2026-07-04.csv",
            "stellar_ai_reference": "Stellar AI copied/reimplemented objects retain source provenance in generated audits.",
            "parity_note": "Static validation must show generated references resolve and intentional winners are documented before standalone readiness is claimed.",
        },
        {
            "surface": "spacefleet_tactica_ship_build_logic",
            "classification": "absorb_reimplement",
            "baseline_status": "implemented",
            "director_evidence": "common/component_templates/000_SFT_00_utilities_roles.txt; common/scripted_triggers/zzzz_staid_sft_addon_equivalence.txt; common/on_actions/zzzz_staid_sft_design_refresh_on_actions.txt; research/stellar-ai/stellar-ai-director-sft-equivalence-audit-2026-07-09.md",
            "stellar_ai_reference": "Spacefleet Tactica 3696204283 plus active add-ons 3703611846 and 3726506420 are copied as the ship-build parity source for the Director.",
            "parity_note": "Director preserves SFT component/combat-computer AI weights and the surviving auto-design refresh path while explicitly disabling SFT new sections and enabling combat-computer restriction removal to match the active add-ons.",
        },
        {
            "surface": "advanced_ship_design_nsc3_esc_gigas_runtime",
            "classification": "defer",
            "baseline_status": "non_baseline_gap",
            "director_evidence": "mods/StellarAIDirector/notes/tuning-notes.md; research/stellar-ai/stellar-ai-director-open-roadmap-2026-07-07.md; research/stellar-ai/stellar-ai-director-sft-equivalence-audit-2026-07-09.md",
            "stellar_ai_reference": "Stellar AI does not settle active-stack section-template, ship-size, Gigas runtime, or observer-proof questions.",
            "parity_note": "SFT component/combat-computer logic is absorbed separately; direct section-template emission, ship-size edits, broad ship-design overrides, advanced Gigas optimization, diplomatic actions, and observer proof remain gated. Native personality war behavior is now implemented in the dedicated 4.4.4 layer.",
        },
    ]


def standalone_parity_inventory_text(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Stellar AI Director Standalone Parity Inventory",
        "",
        "Generated 2026-07-08. Stellar AI is a private local parity reference, not a launch dependency. This inventory records the fastest Pareto baseline: which high-value Stellar AI-style AI surfaces are absorbed, reimplemented, deferred, or intentionally not copied before the descriptor drops the hard dependency.",
        "",
        "| surface | classification | baseline status | Director evidence | parity note |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['surface']} | {row['classification']} | {row['baseline_status']} | `{row['director_evidence']}` | {row['parity_note']} |"
        )
    lines.extend(
        [
            "",
            "Redistribution note: current Stellar AI source is used for private local development provenance only. Any copied third-party content needs explicit permission or a later replacement/rewrite pass before redistribution.",
        ]
    )
    return "\n".join(lines) + "\n"


def generate_standalone_parity_inventory_artifacts() -> list[dict[str, str]]:
    rows = standalone_parity_inventory_rows()
    write_csv(STANDALONE_PARITY_INVENTORY_CSV, rows)
    write_text_file(STANDALONE_PARITY_INVENTORY_MD, standalone_parity_inventory_text(rows))
    return rows


def strategic_subsystem_audit_rows() -> list[dict[str, str]]:
    version_contract = "4.4.5_forward|4.4.4_required_runtime"
    rows = [
        ("data_pipeline", "data", "Current active-stack winners and normalized economic facts feed generated strategy.", "research:stellar-ai-director-economic-valuation-2026-07-07.csv; research:stellar-ai-director-build-plan-consumer-policy-2026-07-09.csv", "active playset; current winning PDXScript objects; benefit policy matrix", "Director generator", "director_internal", "all", "winner provenance; blocker accounting; consumer proof status", "data_foundation", "Canonical dataset handles and stale-source keys still need continuous validation.", "Audit winner selection, normalization, filters, and generated-source feedback on every regeneration."),
        ("resource_survival", "economy", "Repair energy, mineral, consumer-goods, food, and alloy deficits through earned income before discretionary growth.", "mod:common/scripted_triggers/zzz_staid_decision_state_triggers.txt; mod:common/economic_plans/zzzz_staid_additive_economic_plan.txt; research:stellar-ai-director-relative-economic-standards-2026-07-09.csv", "vanilla deficit/monthly-income/fleet-power triggers; relative standards dataset", "37 mutually exclusive colony/fleet repair subplans plus shared income-and-stockpile runway gates", "source_proven", "regular|machine|hive|individual_machine", "resource-use gates; colony-scale headroom; fleet replacement burden; food reserve exception; market purchases cannot satisfy income gates", "corrected_static", "Runtime recovery speed and band calibration remain unproven for the current playtest.", "Measure deficit duration, research throttling, rebuild time, and recovery across archetypes and empire sizes."),
        ("research_capacity", "economy", "Preserve consumer-goods runway and build research capacity only when support resources are safe.", "mod:common/economic_plans/zzzz_staid_additive_economic_plan.txt; mod:common/buildings/zzzz_staid_13_dataset_job_pressure_buildings.txt", "research-capacity datasets; vanilla research-zone potential gates", "economic plan plus building ai_resource_production", "source_proven", "regular|machine|hive|individual_machine", "staid_research_construction_priority_ready; source potential/allow", "corrected_static", "The exact engine score composition among coefficient, additive weight, and ai_resource_production still needs runtime proof.", "Reconstruct candidate scoring and inspect research-world build choices in playtest saves."),
        ("colony_construction", "economy", "Bias eligible buildings and districts by modeled output without inventing inactive building ai_weight control.", "mod:common/buildings/zzzz_staid_13_dataset_job_pressure_buildings.txt; mod:common/districts/zzzz_staid_13_dataset_job_pressure_districts.txt", "economic valuation; consumer policy; source hard gates", "building/district ai_resource_production", "source_proven", "all_supported_planet_owners", "potential/allow preserved; military-capacity excluded", "implemented_static_needs_runtime", "Player Planetary Automation files are not proven AI-empire construction consumers.", "Trace actual candidate selection and keep automation policy separate unless a call site is proven."),
        ("colony_designation", "economy", "Align construction pressure with research, forge, factory, mining, energy, food, unity, trade, and special-world roles.", "research:stellar-ai-director-colony-role-targets-2026-07-09.csv; mod:common/colony_types/zzzzz_staid_15_fortress_economic_hard_gates.txt; mod:common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt", "active colony types; role target dataset; vanilla bottleneck trigger", "designation potential plus hard zone/building eligibility", "source_proven", "regular|machine|hive|special_worlds", "fortress economy/colony-count/threat/topology readiness; research-world naval exclusion", "corrected_static", "Fortress waste and non-bottleneck placement are hard-gated, but the remaining broad designation choice and special-world role selection are not yet reconstructed.", "Audit every remaining colony type winner, selection weight, and role-specific eligible candidate set."),
        ("budget_management", "economy", "Reserve alloys, minerals, and strategic resources for viable construction and fleet pipelines.", "mod:common/ai_budget/zzz_staid_alloys_budget.txt; mod:common/ai_budget/zzz_staid_gigas_resource_budgets.txt; mod:common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt", "vanilla and mod expenditure categories", "ai_budget desired_min/desired_max/expenditure", "source_proven", "all", "deficit gates; positive-alloy fleet gate; defensive emergency bypass; prerequisite readiness", "corrected_static", "The base ship and upgrade budgets now stop during unaffordable peacetime deficits; overlap with mod-specific expenditure categories still needs runtime audit.", "Test simultaneous fleet, planet, and megastructure demand across positive, deficit, and wartime emergency states."),
        ("influence_market", "economy", "Spend capped influence on claims/expansion and limit Director market activity to cap-prevention overflow sales.", "mod:events/zzz_staid_market_and_fleet_safety_events.txt; mod:common/script_values/zzz_staid_roi_values.txt; mod:common/scripted_triggers/zzz_staid_decision_state_triggers.txt", "influence pressure; vanilla market_resource_price; resource_stockpile_percent; Gigas Kugelblitz storage stages", "claim ai_weight plus Director-owned 90%-of-cap overflow sale and storage-cap investment gate; no Director market-buy path", "source_proven", "regular|gestalt|subject", "claim viability; no deficit; positive earned income; fixed reserve; 90% actual storage cap", "corrected_static", "Vanilla AI emergency buying and diplomatic trade composition remain engine-side; Director production gates require earned income as well as stockpile.", "Inventory enclave, subject/federation, irregular-event, liability-reduction, and diplomatic trade channels; observe whether emergency buying persists after repair income becomes available."),
        ("territorial_expansion", "grand_strategy", "Recognize boxed-in empires and convert spatial constraint into expansion or conquest pressure.", "mod:common/scripted_triggers/zzzz_staid_20_strategy_kernel_triggers.txt; mod:common/scripted_triggers/zzz_staid_decision_state_triggers.txt; mod:common/ai_budget/zzzz_staid_08_site_limited_expansion_ai_budget.txt; mod:common/policies/zzzz_staid_10_opening_growth_policies.txt", "border access; colony sites; claims; relative power", "native boxed-in declaration multiplier plus claim, stance, personality, and logistics weights", "source_proven", "regular|gestalt|pacifist|genocidal", "available sites; claim legality; pacifist exclusion; influence reserve", "implemented_static_needs_runtime", "The executable owns the exact blocking-country target and closed-border reachability calculation; script exposes no verified target-specific override.", "Use the single fresh 20–30-year observer acceptance run to verify a strong boxed-in empire attacks its blocking neighbor."),
        ("war_selection", "grand_strategy", "Choose legal, profitable, weak targets and escalate when peaceful expansion is exhausted.", "mod:common/scripted_triggers/zzz_staid_decision_state_triggers.txt; mod:common/personalities/zzzzz_staid_16_standalone_war_pressure.txt; mod:common/defines/zzzz_staid_14_high_scale_ai_defines.txt", "relative power; claims; war goals; borders; threat", "claim budget, personality weights, and native declaration planner", "mixed", "regular|genocidal|raider|pacifist", "war legality; fleet/economic readiness; target value", "gap_identified", "The claim/CB prerequisite receives boxed-in urgency, but Director still does not directly rank targets or declare ordinary expansion wars.", "Audit personalities, diplomatic actions, casus belli, war goals, and the hardcoded declaration chain before any forced-war implementation."),
        ("diplomacy_personality", "grand_strategy", "Adapt aggression, cooperation, rivalry, and pact behavior to ethics, power, and strategic need.", "mod:common/personalities/zzzzz_staid_16_standalone_war_pressure.txt; mod:common/policies/zzzz_staid_10_opening_growth_policies.txt", "Pegasus 4.4.4 personalities; Stellar AI 0.10 personality values; vanilla policy weights", "full personality objects plus diplomatic-stance policy", "source_proven", "all", "ethics; genocidal legality; subject status", "implemented_static_needs_runtime", "Direct diplomatic-action acceptance overrides remain intentionally untouched; rivalry and target selection remain native.", "Check only final load-order winners, then use the single observer acceptance run for behavioral proof."),
        ("fleet_doctrine", "military", "Scale fleet spending to threat and payoff without bankrupting research or civilian production.", "mod:common/scripted_triggers/zzzz_staid_11_fleet_doctrine_triggers.txt; mod:common/scripted_triggers/zzz_staid_decision_state_triggers.txt; mod:common/economic_plans/zzzz_staid_additive_economic_plan.txt; mod:common/ai_budget/zzz_staid_alloys_budget.txt", "relative power; naval capacity; alloy income/runway; war state", "economic plan and alloy ship expenditure budget", "source_proven", "regular|machine|hive|genocidal", "positive alloy income; core deficit; defensive emergency; approved military routes", "corrected_static", "Runtime fleet-manager reinforcement behavior and fleet splitting remain outside current proof.", "Audit fleet templates, reinforcement, merging, and military construction against economic runway."),
        ("hostile_targets", "military", "Treat bosses and lethal fauna separately from ordinary enemy empires and remember failed attacks.", "mod:common/defines/zzzz_staid_14_high_scale_ai_defines.txt; mod:events/zzzz_staid_boss_defeat_escalation_events.txt", "vanilla boss flags; active-stack outlier fleet flags; battle-loss on_action", "boss military-power defines plus defeat escalation", "source_proven", "all_ai_empires", "BOSS/ULTRA_BOSS thresholds; exact survivor flag escalation", "corrected_static", "Only confirmed outlier flags receive adaptive post-loss escalation; the full active-stack boss inventory is not yet classified.", "Classify every is_boss/is_ultra_boss entity and verify AI pathing after a failed attack."),
        ("ship_design", "military", "Preserve viable component/combat-computer choices across SFT, NSC3, ESC, and Gigas.", "mod:common/component_templates/000_SFT_00_utilities_roles.txt; mod:common/on_actions/zzzz_staid_sft_design_refresh_on_actions.txt", "Spacefleet Tactica parity sources; active component graph", "component ai_weight and auto-design refresh", "mixed", "all_ship_builders", "component legality; add-on equivalence", "partial_audit", "Section templates, ship-size edits, and advanced modded hull designs remain unverified.", "Run ship graph validation and audit generated designs per unlocked hull tier."),
        ("technology_routes", "progression", "Research economic prerequisites, fleet payoff, megastructure, and modded unlock routes in viable order.", "mod:common/technology/zzzz_staid_01_unlock_technology_technology.txt", "route override dataset; prerequisites; unlock flags", "technology ai_weight", "source_proven", "regular|machine|hive|special_origins", "route prerequisites; resource readiness; feature flags", "implemented_static_needs_runtime", "Competing routes and archetype-inapplicable technologies need a full negative-path audit.", "Validate every route prerequisite graph and empire applicability gate."),
        ("ascension_strategy", "progression", "Choose traditions, ascension perks, and ascension paths that fit the empire and current strategic bottleneck.", "mod:common/tradition_categories/zzzz_staid_02_perks_traditions_tradition_categories.txt; mod:common/traditions/zzzz_staid_02_perks_traditions_traditions.txt; mod:common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt", "route overrides; perk/tradition prerequisites", "tradition category/node and ascension-perk ai_weight", "source_proven", "regular|machine|hive|psionic|cybernetic|synthetic|biological", "prerequisites and source potential", "partial_audit", "Current overrides push selected routes but do not yet express a mutually coherent empire-specific ascension plan.", "Audit all path exclusions, prerequisites, synergies, and extreme-empire preferences."),
        ("megastructure_strategy", "progression", "Sequence high-return megastructures only when prerequisites, economy, and sites are ready.", "mod:common/megastructures/zzzz_staid_03_megastructures_megastructures.txt; mod:common/economic_plans/zzzz_staid_additive_economic_plan.txt", "ROI datasets; site limits; route graph", "megastructure ai_weight plus economic plans/budgets", "mixed", "all_eligible", "prerequisites; site availability; resource runway", "implemented_static_needs_runtime", "Concurrent projects, repair/upgrade decisions, and unique mod chains need adversarial sequencing tests.", "Audit each chain from technology through site, budget, build, and upgrade completion."),
        ("crisis_response", "military", "Convert economy and fleet production for real crises without permanently starving development.", "mod:common/scripted_triggers/zzzz_staid_20_strategy_kernel_triggers.txt; mod:common/ai_budget/zzz_staid_alloys_budget.txt; mod:common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt", "crisis country types; relative power; native crisis predicates", "native crisis budget multipliers plus Director starbase weights", "mixed", "all_non_crisis_ai", "native crisis identity; economic readiness; collapse protection", "partial_audit", "Vanilla and modded crises, fallen empires, and pseudo-crisis bosses are not yet exhaustively separated.", "Inventory crisis actors and verify response activation, target legality, and recovery after threat removal."),
        ("starbase_defense", "military", "Build shipyards and static defense where strategically useful without crowding civilian research worlds.", "mod:common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt; mod:common/starbase_modules/zzzz_staid_05_starbase_defense_starbase_modules.txt", "route dataset; chokepoints; threat state", "starbase building/module ai_weight and economic plans", "source_proven", "all_starbase_owners", "deficit safety; threat readiness; source potential", "implemented_static_needs_runtime", "Chokepoint value, defensive platform affordability, and modded starbase slot competition need validation.", "Audit module/building selection at border, shipyard, trade, and interior starbases."),
        ("invasion_bombardment", "military", "Use bombardment and armies appropriate to conquest objectives and empire ethics.", "mod:common/bombardment_stances/zzzz_staid_12_militarist_raiding_bombardment.txt; mod:common/ai_budget/zzzz_staid_14_army_recruitment_budget.txt; mod:common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt", "bombardment stances; native army and transport AI; mineral budget competition", "bombardment stance ai_weight plus uncapped native army mineral reserve", "mixed", "militarist|raider|genocidal|pacifist", "ethics; civic; legal stance; economy", "implemented_static_needs_runtime", "Transport escort, invasion thresholds, army-type choice, and planet target choice remain executable-owned.", "Use the single observer acceptance run to confirm useful but non-excessive offensive armies."),
        ("machine_hive_gestalt", "archetype", "Use correct upkeep/resources, jobs, growth, unity, and ascension routes for gestalts and individual machines.", "mod:common/economic_plans/zzzz_staid_additive_economic_plan.txt", "country_uses_* triggers; machine/hive route gates", "economic plans and route weights", "mixed", "machine|individual_machine|hive", "consumer-goods and food use gates; owner type", "partial_audit", "Individual machines, rogue servitors, assimilators, exterminators, and hive variants need separate strategy matrices.", "Build an archetype capability matrix and add negative tests for inapplicable resources and routes."),
        ("genocidal_extremes", "archetype", "Favor rapid conquest and war economy for purifiers, exterminators, swarms, and other no-diplomacy empires.", "mod:common/economic_plans/zzzz_staid_additive_economic_plan.txt", "civics; personality; war legality", "war-support economic subplans", "mixed", "fanatic_purifier|determined_exterminator|devouring_swarm", "economy runway; target power; total-war legality", "gap_identified", "No dedicated direct target/declaration logic or civic-specific strategic plan is yet proven.", "Audit civic triggers, total-war goals, fleet timing, and post-conquest stabilization."),
        ("pacifist_isolationist", "archetype", "Pursue habitats, diplomacy, vassalization, and internal scaling when offensive war is illegal or undesirable.", "mod:common/economic_plans/zzzz_staid_additive_economic_plan.txt", "ethics; war philosophy; expansion sites", "economic plans only", "mixed", "pacifist|inward_perfection", "war legality; habitat prerequisites; diplomacy access", "gap_identified", "Alternative boxed-in growth paths are not yet coherently ranked against claims and war pressure.", "Define legal expansion ladders for pacifist and isolationist states."),
        ("megacorp_trade", "archetype", "Prioritize trade, branch offices, commercial pacts, and compact growth without sacrificing research support.", "mod:common/economic_plans/zzzz_staid_additive_economic_plan.txt", "trade income; authority; branch-office and diplomacy surfaces", "economic plans", "mixed", "megacorp|trade_focused", "market access; trade capacity; diplomacy legality", "partial_audit", "Branch-office target selection, commercial pacts, criminal syndicates, and trade-policy transitions are not fully modeled.", "Audit trade and branch-office consumers plus megacorp-specific influence spending."),
        ("nomad_arkship", "archetype", "Avoid planet-only assumptions and support Arkship, Wayline, and nomadic economic surfaces.", "research:stellar-ai-director-nomad-arkship-compatibility-audit-2026-07-09.md", "4.4 Arkship/Wayline sources", "source objects preserved; limited Director routing", "mixed", "nomad|arkship", "country type; colony ownership; special resources", "partial_audit", "Several colony, construction, budget, and war assumptions still require nomad-specific negative paths.", "Trace every planet-scoped trigger and construction lane for nomad applicability."),
        ("subjects_overlords", "archetype", "Respect subject restrictions and value loyalty, specialization, contracts, integration, and defensive obligations.", "none", "subject contracts; diplomatic actions; overlord holdings", "none Director-owned", "absent", "subject|overlord", "contract legality; loyalty; independence status", "gap_identified", "Subject and overlord strategic decisions have not yet received a dedicated Director pass.", "Inventory subject/federation consumers and define empire-role-specific priorities."),
        ("special_origins", "archetype", "Avoid breaking origin-specific economies, planets, ships, event gates, and victory paths.", "research:stellar-ai-director-build-plan-consumer-policy-2026-07-09.csv", "origin/civic/event gates in winning objects", "source potential/allow preserved", "mixed", "frameworld|birch|ring|clone|knights|other_special", "source gates; event flags; origin ownership", "partial_audit", "Preserving source gates prevents illegal candidates but does not prove strategically correct origin-specific planning.", "Create a capability matrix for every active-stack origin that changes the economic or military substrate."),
        ("compatibility_winners", "integration", "Ensure Director overrides the intended object and preserves required parent-mod behavior.", "research:stellar-ai-director-generated-conflicts-2026-07-04.csv; research:stellar-ai-director-generated-reference-audit-2026-07-04.csv", "Irony load order; active playset; generated file audit", "Stellaris object loader", "source_proven", "all", "winner checks; reference resolution; forbidden surfaces", "implemented_static_needs_runtime", "Static winner proof cannot establish runtime semantics for every modded object.", "Re-run conflict/reference audits after each generator change and add targeted smoke checks for high-risk surfaces."),
        ("runtime_telemetry", "validation", "Observe whether strategic pressures activate and produce the intended economic, construction, diplomatic, and military outcomes.", "research:STAID_MANUAL_STATIC_VALIDATION.md", "logs; saves; observer checkpoints; user playtest reports", "none at runtime unless observer tooling is explicitly enabled", "unproven", "all", "commands_at_date disabled outside approved runs", "gap_identified", "Current changes are statically validated; the ongoing user playtest is the primary runtime evidence for this build.", "Define save/log checkpoints for deficits, build choices, war declarations, boss attacks, and archetype behavior."),
    ]
    columns = (
        "subsystem_id", "scope", "intended_behavior", "director_artifacts", "upstream_inputs",
        "engine_consumer", "consumer_authority", "empire_archetypes", "safety_gates", "audit_status",
        "known_gap", "next_action",
    )
    return [dict(zip(columns, row)) | {"version_contract": version_contract} for row in rows]


def strategic_subsystem_audit_text(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Stellar AI Director Strategic Subsystem Audit",
        "",
        "Generated 2026-07-09. This is the canonical boundary map for the continuing audit. `implemented` is not inferred from the existence of data: each row records the actual consumer, proof level, remaining gap, and next action.",
        "",
        "Version contract: develop toward Stellaris 4.4.5 while retaining error-free runtime compatibility with the pinned 4.4.4 playset.",
        "",
        "| subsystem | scope | consumer authority | audit status | known gap | next action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['subsystem_id']} | {row['scope']} | {row['consumer_authority']} | {row['audit_status']} | {row['known_gap']} | {row['next_action']} |"
        )
    return "\n".join(lines) + "\n"


def generate_strategic_subsystem_audit_artifacts() -> list[dict[str, str]]:
    rows = strategic_subsystem_audit_rows()
    write_csv(STRATEGIC_SUBSYSTEM_AUDIT_CSV, rows)
    write_text_file(STRATEGIC_SUBSYSTEM_AUDIT_MD, strategic_subsystem_audit_text(rows))
    return rows


def generated_version_inventory_text(playset: dict[str, Any]) -> str:
    required_lines = [
        f"- {mod_id}: {row['name']} present={row['present']} load_position={row['load_position']}"
        for mod_id, row in sorted(playset.get("required_mods", {}).items())
    ]
    optional_lines = [
        f"- {label}: {present}"
        for label, present in sorted(playset.get("optional_integrations", {}).items())
    ]
    return f"""# Stellar AI Director Generated Version Inventory

Generated by `tools/generate_stellar_ai_director_patch.py`.

- Primary development target: Stellaris PC 4.4.5.
- Required compatibility/runtime baseline: installed Pegasus v4.4.4 (5505); generated gameplay surfaces must remain error-free and functional on this pinned playset until its incompatible mods update.
- Launcher metadata remains `v4.4.*` for the stable 4.4 line.
- Static validation scope: no Stellaris launch, observer game, benchmark scenario, screenshot, or save checkpoint is required by this generated pass.
- Launcher descriptor support line: `supported_version="v4.4.*"`.
- Active Irony collection: `{playset.get('collection_name', '')}`.
- Active mod count: {playset.get('mod_count', 0)}.
- Patch mod enabled in Irony collection: {playset.get('patch_mod_enabled')}.

## Required Mod Presence

{chr(10).join(required_lines) if required_lines else "- No required mod inventory rows were found."}

## Optional Integration Signals

{chr(10).join(optional_lines) if optional_lines else "- No optional integration rows were found."}

## Generated July 7 Surfaces

- `common/scripted_triggers/zzzz_staid_10_opening_strategy_triggers.txt`
- `common/scripted_triggers/zzzz_staid_20_strategy_kernel_triggers.txt`
- `common/scripted_triggers/zzzz_staid_11_fleet_doctrine_triggers.txt`
- `common/policies/zzzz_staid_10_opening_growth_policies.txt`
- `common/edicts/zzzz_staid_10_opening_growth_edicts.txt`

Policy and edict artifacts are generated from locally extracted, parse-verified installed objects. Missing IDs or missing policy options fail generation.
"""


def mod_stack_compatibility_text(playset: dict[str, Any]) -> str:
    mod_rows = playset.get("mods", [])
    top_mods = [
        f"- {row.get('position')}: {row.get('name')} ({row.get('steam_id') or row.get('path')})"
        for row in mod_rows[:40]
    ]
    return f"""# Stellar AI Director Mod Stack Compatibility

Generated by `tools/generate_stellar_ai_director_patch.py`.

## Compatibility Contract

- Primary target: Stellaris 4.4.5; required live compatibility baseline: pinned Pegasus v4.4.4 (5505), with `v4.4.*` descriptor compatibility retained for the stable 4.4 line.
- Strategy style: computed scripted triggers and AI weights first; persistent flags or event forcing are reserved for verified cooldowns and runtime memory only.
- Policy scope: this pass modifies `diplomatic_stance` AI weights only, because that object extracts and parses cleanly from the installed vanilla policy file.
- Edict scope: this pass modifies installed vanilla edict AI weights for research, exploration, energy, mineral, food, and border-defense pressure.
- High-risk deferred surfaces: diplomatic actions, personalities, federation laws, species rights, forced ship designs, and direct Gigas megastructure object rewrites require separate full-object review.

## Active Stack Snapshot

Collection: `{playset.get('collection_name', '')}`

{chr(10).join(top_mods) if top_mods else "- No active mod rows were found."}
"""


def manual_static_validation_text() -> str:
    return """# Stellar AI Director Static Validation Notes

Generated by `tools/generate_stellar_ai_director_patch.py`.

This implementation pass is intentionally static-only. It provides no Stellaris launch, observer-run, benchmark, screenshot, or save-checkpoint proof.

Required local checks for this pass:

- Python compile of generator, entrypoint, and validator.
- Generator run.
- Static validator run.
- Unit test discovery under `tools/tests`.
- Generated PDXScript parse/load-safety audit.
- Generated reference audit.
- `git diff --check`.
- Live launcher descriptor and `dlc_load.json` inclusion check before claiming live-launch readiness.

Manual runtime questions left out of scope:

- Whether the computed route classifier reaches the intended empirical 2270-2280 and 2350 research breakpoints in a full game.
- Whether research-pact and Research Federation behavior emerges strongly enough from diplomatic stance weights alone.
- Whether NSC3/ESC doctrine technology weights need direct component or ship-size overrides after runtime observation.
"""


def standalone_aggression_personalities_text() -> str:
    vanilla_path = VANILLA_COMMON_ROOT / "personalities" / "00_personalities.txt"
    reference_root = mod_source_root_for_id("3610149307")
    reference_path = reference_root / "common" / "personalities" / "00_personalities.txt"
    variable_path = reference_root / "common" / "scripted_variables" / "stellarai_scripted_variables.txt"
    vanilla_text = read_text(vanilla_path)
    reference_text = read_text(reference_path)
    reference_variables = collect_variables(read_text(variable_path))
    blocks: list[str] = []
    for object_id, aggression in STANDALONE_AGGRESSION_PERSONALITY_VALUES.items():
        reference_block = extract_top_level_object_text(reference_text, object_id)
        reference_values: dict[str, float] = {}
        for field in ("aggressiveness", "bravery", "military_spending"):
            match = re.search(rf"(?m)^\s*{field}\s*=\s*([^\s#]+)", reference_block)
            if match is None:
                raise ValueError(f"Stellar AI reference personality {object_id} has no {field} scalar")
            reference_value = parse_numeric(match.group(1), reference_variables)
            if not isinstance(reference_value, (int, float)):
                raise ValueError(
                    f"Stellar AI personality evidence for {object_id}.{field} is not numeric: {reference_value}"
                )
            reference_values[field] = float(reference_value)
        if not math.isclose(reference_values["aggressiveness"], aggression, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError(
                f"Stellar AI aggression evidence drift for {object_id}: "
                f"expected {aggression}, got {reference_values['aggressiveness']}"
            )
        vanilla_block = extract_top_level_object_text(vanilla_text, object_id)
        generated_block = vanilla_block
        for field, value in reference_values.items():
            generated_block = replace_or_insert_top_level_scalar(
                generated_block,
                field,
                f"\t{field} = {value:g}",
            )
        blocks.append(generated_block.rstrip())
    text = """# Generated by tools/generate_stellar_ai_director_patch.py.
# Pegasus 4.4.4 full-object personality overrides restoring the native war
# behavior signals lost when Stellar AI stopped being a runtime dependency.
# Provenance: 4.4.4 common/personalities/00_personalities.txt plus Stellar AI
# 0.10 common/personalities/00_personalities.txt and scripted variables.
# Aggressiveness, bravery, and military spending follow that working reference;
# behavior flags, diplomacy fields, design preferences, and selection rules stay vanilla.
# War declarations still use the engine planner, legal casus belli, and war goals.

""" + "\n\n".join(blocks) + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def native_war_readiness_country_type_text() -> str:
    """Remove Pegasus country-type gates that deadlock before target selection."""
    vanilla_path = VANILLA_COMMON_ROOT / "country_types" / "00_country_types.txt"
    vanilla_default = extract_top_level_object_text(read_text(vanilla_path), "default")
    # Pegasus 4.4.4 defaults regular empires to 50% desired navy and six
    # assault armies before the native planner may consider any war. Omitting
    # min_navy_for_wars uses the documented 4.4.4 default of zero and remains
    # compatible with 4.4.5, where Paradox removed that parameter entirely.
    generated_default = re.sub(
        r"(?m)^\s*min_navy_for_wars\s*=.*(?:\n|$)",
        "",
        vanilla_default,
    )
    generated_default, replacements = re.subn(
        r"(?m)^(\s*)min_assault_armies_for_wars\s*=.*$",
        r"\1min_assault_armies_for_wars = 0",
        generated_default,
        count=1,
    )
    if replacements != 1:
        raise ValueError("Vanilla default country type has no min_assault_armies_for_wars gate")
    text = """# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object current-vanilla override of the regular `default` country type.
# Provenance: Pegasus 4.4.4 common/country_types/00_country_types.txt.
# The stock 0.5 navy and six-assault-army declaration gates produced a hard
# deadlock in the active stack: no ordinary AI passed both after 32 years.
# This removes only those pre-planner gates; native targets, CBs, war goals,
# strength evaluation, preparation, declaration, and fleet execution remain.

""" + generated_default.rstrip() + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def high_scale_ai_defines_text() -> str:
    return """# Generated by tools/generate_stellar_ai_director_patch.py.
# Director economic/construction defines remain high-scale. War-planning defines
# are restored to the native Pegasus 4.4.4 envelope used by working Stellar AI
# 0.10, except for a bounded boxed-in multiplier. This avoids global overwar while
# retaining strong local breakout pressure.

NAI = {
	AI_FREE_JOBS_DISTRICT_BUILD_CAP = 2000
	AI_FREE_JOBS_BUILDING_BUILD_CAP = 5000
	AI_DEFICIT_SCORE_MULT = 500
	AI_FOCUS_SCORE_MULT = 12
	AI_RESOURCE_PRODUCTION_SCORE_MULT = 8
	AI_AMENITIES_SCORE_MULT = 8
	AI_HOUSING_SCORE_MULT = 8
	AI_CRIME_REDUCTION_SCORE_MULT = 4
	AI_ADMIN_CAP_SCORE_MULT = 6
	AI_POPS_SCORE_MULT = 0.25
	# Vanilla value. Avoids inflating capacity into the 4.4.4 high-cap planner bug.
	AI_NAVAL_CAP_SCORE_MULT = 15
	AI_UPGRADE_SCORE_MULT = 10
	AI_RESOURCE_TARGET_EXPIRATION_MONTHS = 6
	AI_RESOURCE_TARGET_VALID_THRESHOLD = 0.90
	AI_DISTRICT_MAX_OPPORTUNITY_COST_FACTOR = 0.05
	AI_DISTRICT_OPPORTUNITY_COST_FALLOFF = 0.25
	AI_BUILDING_MAX_OPPORTUNITY_COST_FACTOR = 0.05
	AI_BUILDING_OPPORTUNITY_COST_FALLOFF = 0.25
	AI_BUILDING_MIN_HYPOTHETICAL_WEIGHT = 5
	AI_DISTRICT_MIN_HYPOTHETICAL_WEIGHT = 5
	BUILDING_BUILD_THRESHOLD = 0.1
	BUILDING_EXISTS_DIV_SCORE = 0.2
	UNDERDEVELOPED_PLANET_LIMIT = 999
	AI_UNBUILT_DISTRICT_BOOST_POP_THRESHOLD = 250
	# Save-backed 2230 regression: rich planets with 7-22 unemployed pops and
	# ample district headroom still produced no queue. Strengthen only the
	# engine's existing unemployment/underdevelopment candidate signal.
	AI_UNBUILT_DISTRICT_BOOST_MULTIPLIER = 20.0
	AI_STORAGE_BUILDING_CAPPED_RESOURCE_BOOST = 1000

	# Early strategic reconnaissance: vanilla already requests five science ships
	# for the first 30 years. Spread their auto-explore targets aggressively,
	# avoid redundant home-space coverage, and permit routes through accessible
	# foreign systems so at least two explorers can push in opposite directions.
	AUTO_EXPLORE_ATTRACTION_SCORE = 1000
	AUTO_EXPLORE_COLLABORATION_PENALTY = 2000
	AUTO_EXPLORE_SYSTEM_OWNED = 100

	# Working Stellar AI did not replace these global declaration defines; its
	# reliable wars came from complete personalities and supported economies.
	AI_WAR_PREPARATION_MIN_MONTHS = 12
	AI_WAR_PREPARATION_MAX_MONTHS = 30
	AI_AGGRESSIVENESS_BASE = 25
	AI_AGGRESSIVENESS_PROPAGATOR_BOXED_IN_MULT = 12
	AI_AGGRESSIVENESS_BOXED_IN_MULT = 8
	AI_AGGRESSIVENESS_NO_COLONY_TARGET_MULT = 2
	ENEMY_FLEET_POWER_MULT = 1.2
	AI_HOSTILE_FLEET_DISTANCE = 3
	BOSS_MILITARY_POWER = 100000
	ULTRA_BOSS_MILITARY_POWER = 500000
	WAR_DECLARATION_MAX_DISTANCE = 300
	WAR_DECLARATION_MALUS_DISTANCE = 25
	WAR_DECLARATION_MALUS = 0.05
	WAR_DECLARATION_MINIMUM_SCORE = 0.5
	OFFENSE_VS_DEFENSE_STRATEGY_ALLOTMENT = 1.0
}
"""


def minerals_planet_construction_budget_text() -> str:
    def object_text(name: str, base_weight: float, stockpile_gate: str) -> str:
        return f"""
{name} = {{
	resource = minerals
	type = expenditure
	category = planets

	potential = {{
		is_country_type = default
{stockpile_gate}
	}}

	weight = {{
		weight = {base_weight}
		# Preserve jobs and deficit recovery, but yield budget share while the
		# empire needs armies or other war logistics.
		modifier = {{ factor = 0.65 staid_war_logistics_pressure = yes }}
		modifier = {{ add = 0.20 staid_planetary_capacity_growth_ready = yes }}
		modifier = {{ add = 0.20 staid_core_deficit_short_runway = yes }}
		modifier = {{ add = 0.50 staid_construction_spenddown_pressure = yes }}
		modifier = {{ add = 0.25 staid_resource_waste_pressure = yes }}
		modifier = {{ add = 0.30 staid_high_scale_snowball_pressure = yes }}
		modifier = {{ add = 0.75 staid_unemployment_construction_pressure = yes }}
		modifier = {{ add = 0.50 any_owned_planet = {{ free_building_slots > 0 num_unemployed > 0 }} }}
		modifier = {{ add = 0.20 resource_stockpile_compare = {{ resource = minerals value > 10000 }} }}
		modifier = {{ add = 0.30 resource_stockpile_compare = {{ resource = minerals value > 25000 }} }}
	}}
}}
"""

    return (
        "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
        "# Full-object Pegasus 4.4.4 planet-budget overrides. Vanilla low/medium/high base weights are preserved.\n"
        "# War logistics temporarily receive room without disabling unemployment, deficit, or stockpile spending.\n"
        + object_text(
            "minerals_expenditure_planets_low",
            1.0,
            "\t\tresource_stockpile_compare = { resource = minerals value < 1000 }",
        )
        + object_text(
            "minerals_expenditure_planets_med",
            0.8,
            "\t\tresource_stockpile_compare = { resource = minerals value >= 1000 }\n\t\tresource_stockpile_compare = { resource = minerals value < 2000 }",
        )
        + object_text(
            "minerals_expenditure_planets_high",
            0.6,
            "\t\tresource_stockpile_compare = { resource = minerals value >= 2000 }",
        )
    )


def army_recruitment_budget_text() -> str:
    return """# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object replacement of the two Pegasus 4.4.4 mineral army budget entries.
# Provenance: common/ai_budget/00_minerals_budget.txt.
# A small native mineral reserve makes the first useful offensive armies possible
# without making armies a declaration prerequisite or imposing a recruitment cap.

minerals_expenditure_armies = {
	resource = minerals
	type = expenditure
	category = armies

	potential = {
		is_nomadic = no
	}

	weight = {
		weight = 0.20
		modifier = { factor = 3 staid_war_logistics_pressure = yes }
		modifier = { factor = 1.5 highest_threat > 20 }
		modifier = { factor = 0.25 staid_catastrophic_collapse_mode = yes }
	}

	# Reserve minerals, not units. The engine remains free to recruit fewer or
	# more armies according to legal army types, invasion demand, and economy.
	desired_min = {
		base = 200
		modifier = { add = 300 staid_boxed_in_war_pressure = yes }
		modifier = {
			add = 300
			OR = {
				staid_militarist_conquest_strategy = yes
				staid_raiding_pop_growth_strategy = yes
			}
		}
		modifier = {
			add = 300
			staid_basic_economy_runway_safe = yes
			staid_core_deficit_short_runway = no
			staid_catastrophic_collapse_mode = no
			OR = {
				staid_identity_machine_exterminator = yes
				staid_identity_devouring_swarm = yes
				staid_identity_assimilator = yes
			}
		}
		modifier = {
			add = 500
			OR = {
				is_at_war = yes
				staid_security_existential = yes
			}
		}
	}
}

minerals_expenditure_armies_threatened = {
	resource = minerals
	type = expenditure
	category = armies

	potential = {
		is_nomadic = no
		highest_threat > 20
	}

	weight = {
		weight = 0.10
		modifier = { factor = 2 staid_security_existential = yes }
		modifier = { factor = 0.25 staid_catastrophic_collapse_mode = yes }
	}
}
"""


def wartime_colony_alloy_budget_text() -> str:
    """Preserve native colony funding while a pre-midgame AI is at war."""
    return """# Vanilla Pegasus 4.4.4 blocks this budget while at war before midgame.
# Keep every native colonization-plan and affordability gate, removing only
# that wartime exclusion so long wars cannot freeze otherwise valid expansion.
alloys_expenditure_colonies_expand = {
	resource = alloys
	type = expenditure
	category = colonies

	potential = {
		is_nomadic = no
		ai_colonize_plans > 0
		OR = {
			AND = {
				is_lithoid_empire = no
				is_infernal_empire = no
				has_monthly_income = {
					resource = food
					value > 0
				}
				OR = {
					AND = {
						country_uses_bio_ships = no
						has_resource = { type = food amount > 400 }
					}
					AND = {
						country_uses_bio_ships = yes
						has_resource = { type = food amount > 600 }
					}
				}
			}
			AND = {
				is_lithoid_empire = yes
				has_resource = { type = minerals amount > 400 }
				has_monthly_income = {
					resource = minerals
					value > 0
				}
			}
			AND = {
				is_robot_empire = yes
				has_resource = { type = energy amount > 400 }
				has_monthly_income = {
					resource = energy
					value > 0
				}
			}
		}
	}

	weight = { weight = 0.5 }

	desired_min = {
		base = 0
		modifier = {
			add = @colony_cost_base
			is_guided_sapience_empire = no
			is_virtual_empire = no
		}
		modifier = {
			add = @colony_cost_low
			is_guided_sapience_empire = no
			is_virtual_empire = yes
		}
		modifier = {
			add = @colony_cost_mid
			is_guided_sapience_empire = yes
			is_virtual_empire = no
		}
		modifier = {
			add = @colony_cost_base
			is_guided_sapience_empire = yes
			is_virtual_empire = yes
		}
		modifier = { mult = 0.5 has_origin = origin_tree_of_life }
		modifier = { mult = 0.5 country_uses_bio_ships = yes }
	}

	desired_max = {
		base = 0
		modifier = {
			add = @colony_cost_base_max
			is_guided_sapience_empire = no
			is_virtual_empire = no
		}
		modifier = {
			add = @colony_cost_low_max
			is_guided_sapience_empire = no
			is_virtual_empire = yes
		}
		modifier = {
			add = @colony_cost_mid_max
			is_guided_sapience_empire = yes
			is_virtual_empire = no
		}
		modifier = {
			add = @colony_cost_base_max
			is_guided_sapience_empire = yes
			is_virtual_empire = yes
		}
		modifier = { mult = 0.5 has_origin = origin_tree_of_life }
		modifier = { mult = 0.5 country_uses_bio_ships = yes }
	}
}
"""


def generate_mod_files(rows: list[dict[str, Any]] | None = None) -> None:
    rows = rows or extract_megastructure_rows()
    thresholds = generated_thresholds(rows)
    core_ai_artifacts = render_core_ai_artifacts(rows)
    playset = build_active_playset_snapshot()
    write_json(RESEARCH_ROOT / "stellar-ai-director-active-playset-2026-07-04.json", playset)
    # Remove superseded construction-weight outputs before rebuilding the
    # active-stack valuation index. Otherwise a single generator run can index
    # files that it deletes later and leave the dataset internally stale.
    for stale_path in (
        MOD_ROOT / "common" / "buildings" / "zzzz_staid_06_research_infrastructure_buildings.txt",
        MOD_ROOT / "common" / "districts" / "zzzz_staid_06_research_infrastructure_districts.txt",
        MOD_ROOT / "common" / "buildings" / "zzzz_staid_07_pop_assembly_buildings.txt",
        MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_12_planetary_diversity_value_triggers.txt",
        MOD_ROOT / "common" / "buildings" / "zzzz_staid_12_planetary_diversity_buildings.txt",
        MOD_ROOT / "common" / "on_actions" / "zzzz_staid_army_reserve_on_actions.txt",
        MOD_ROOT / "events" / "zzzz_staid_army_reserve_events.txt",
        MOD_ROOT / "common" / "component_templates" / "zzzzz_staid_science_cloaking_ai_safety.txt",
    ):
        stale_path.unlink(missing_ok=True)
    generate_economic_valuation_dataset()
    normalize_economic_valuation_dataset_pair()
    write_economic_valuation_evidence_summary()
    write_text_file(MOD_ROOT / "descriptor.mod", descriptor_text())
    write_text_file(MOD_ROOT / "README.md", readme_text(playset))
    write_text_file(
        DECISION_STATE_TRIGGER_PATH,
        core_ai_artifacts[DECISION_STATE_TRIGGER_PATH],
    )
    write_text_file(
        MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_10_opening_strategy_triggers.txt",
        opening_strategy_triggers_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_20_strategy_kernel_triggers.txt",
        strategy_kernel_triggers_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_11_fleet_doctrine_triggers.txt",
        fleet_doctrine_triggers_text(),
    )
    write_text_file(
        MOD_ROOT
        / "common"
        / "scripted_triggers"
        / "zzzz_staid_21_nation_archetype_triggers.txt",
        archetype_triggers_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "policies" / "zzzz_staid_10_opening_growth_policies.txt",
        opening_growth_policies_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "edicts" / "zzzz_staid_10_opening_growth_edicts.txt",
        opening_growth_edicts_text(),
    )
    write_text_file(MOD_ROOT / "common" / "ai_budget" / "zzz_staid_alloys_budget.txt", ai_budget_text(thresholds))
    write_text_file(
        OUTPOST_BUDGET_PATH,
        core_ai_artifacts[OUTPOST_BUDGET_PATH],
    )
    write_text_file(MOD_ROOT / "common" / "ai_budget" / "zzz_staid_gigas_resource_budgets.txt", gigas_resource_budget_text())
    write_text_file(MOD_ROOT / "common" / "defines" / "zzzz_staid_14_high_scale_ai_defines.txt", high_scale_ai_defines_text())
    write_text_file(
        MOD_ROOT / "common" / "personalities" / "zzzzz_staid_16_standalone_war_pressure.txt",
        standalone_aggression_personalities_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "country_types" / "zzzzz_staid_18_native_war_readiness.txt",
        native_war_readiness_country_type_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "ship_sizes" / "zzzzz_staid_17_mem_surveyor_outpost_compat.txt",
        mem_surveyor_outpost_ship_size_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "game_rules" / "zzzzz_staid_science_route_system_restriction.txt",
        science_route_system_restriction_game_rule_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_14_minerals_planet_construction_budget.txt",
        minerals_planet_construction_budget_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_14_army_recruitment_budget.txt",
        army_recruitment_budget_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "ai_budget" / "zzzz_staid_15_opening_leader_recruitment_budget.txt",
        opening_leader_recruitment_budget_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "ai_budget" / "zzzzz_staid_19_wartime_colony_alloy_budget.txt",
        wartime_colony_alloy_budget_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "buildings" / "zzzzz_staid_17_medical_center_churn_fix.txt",
        medical_center_churn_fix_text(),
    )
    write_war_planning_444_provenance()
    generate_strategic_resource_recovery_artifacts()
    write_text_file(
        MOD_ROOT / "common" / "scripted_effects" / "zzz_staid_gigas_habitat_compat_effects.txt",
        gigas_habitat_compat_scripted_effects_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "districts" / "zzzz_staid_09_gigas_habitat_zone_slot_compat_districts.txt",
        gigas_habitat_zone_slot_compat_districts_text(),
    )
    for stale_path in (
        MOD_ROOT / "common" / "scripted_triggers" / "zzzz_staid_12_planetary_diversity_value_triggers.txt",
        MOD_ROOT / "common" / "buildings" / "zzzz_staid_12_planetary_diversity_buildings.txt",
    ):
        stale_path.unlink(missing_ok=True)
    write_text_file(
        MOD_ROOT / "common" / "decisions" / "zzzz_staid_12_planetary_diversity_outpost_decisions.txt",
        planetary_diversity_outpost_decisions_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "bombardment_stances" / "zzzz_staid_12_militarist_raiding_bombardment.txt",
        militarist_bombardment_stances_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "on_actions" / "zzz_staid_market_and_fleet_safety_on_actions.txt",
        market_and_fleet_safety_on_actions_text(),
    )
    write_text_file(MOD_ROOT / "events" / "zzz_staid_market_and_fleet_safety_events.txt", market_and_fleet_safety_events_text())
    write_text_file(
        MOD_ROOT / "common" / "on_actions" / "zzzz_staid_boss_defeat_escalation_on_actions.txt",
        boss_defeat_escalation_on_actions_text(),
    )
    write_text_file(
        MOD_ROOT / "events" / "zzzz_staid_boss_defeat_escalation_events.txt",
        boss_defeat_escalation_events_text(),
    )
    write_text_file(MOD_ROOT / "common" / "script_values" / "zzz_staid_roi_values.txt", script_values_text(thresholds))
    write_stellarai_inline_script_dependencies()
    write_sft_equivalence_files()
    write_planetary_diversity_profile_artifacts()
    generate_route_override_artifacts()
    dataset_job_pressure_override_artifacts()
    write_text_file(
        MOD_ROOT / "common" / "buildings" / "zzzzz_staid_14_pd_naval_capacity_hard_gates.txt",
        planetary_diversity_naval_capacity_buildings_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "colony_types" / "zzzzz_staid_15_fortress_economic_hard_gates.txt",
        fortress_colony_types_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "colony_types" / "zzzzz_staid_16_research_buildout_plan.txt",
        research_plan_colony_types_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "zones" / "zzzzz_staid_20_research_world_zone_priority.txt",
        research_world_zone_priority_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "buildings" / "zzzzz_staid_15_fortress_economic_hard_gates.txt",
        fortress_army_buildings_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "colony_automation_exceptions" / "zzzzz_staid_01_gigas_rogue_ai.txt",
        gigas_rogue_ai_automation_exception_text(),
    )
    write_text_file(
        MOD_ROOT / "common" / "inline_scripts" / "zones" / "shared_fortress_zone.txt",
        fortress_zone_inline_script_text(),
    )
    write_text_file(
        RESEARCH_ROOT / "stellar-ai-director-implementation-notes-2026-07-04.md",
        implementation_notes_text(playset, thresholds),
    )
    write_text_file(GENERATED_VERSION_INVENTORY_MD, generated_version_inventory_text(playset))
    write_text_file(MOD_STACK_COMPATIBILITY_MD, mod_stack_compatibility_text(playset))
    write_text_file(MANUAL_STATIC_VALIDATION_MD, manual_static_validation_text())
    generate_standalone_parity_inventory_artifacts()
    generate_relative_economic_standard_artifacts()
    generate_strategic_subsystem_audit_artifacts()
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


def war_planning_444_provenance_rows() -> list[dict[str, str]]:
    """Return one provenance row for every war-package full-object override.

    Custom scripted triggers are intentionally absent: they are new Director
    objects, not copied vanilla objects. The NAI define group is included as a
    separate override surface even though Stellaris defines are not object
    blocks in the same sense as personalities, policies, budgets, or country
    types.
    """
    rows: list[dict[str, str]] = []
    for object_id in STANDALONE_AGGRESSION_PERSONALITY_VALUES:
        rows.append(
            {
                "generated_path": "mods/StellarAIDirector/common/personalities/zzzzz_staid_16_standalone_war_pressure.txt",
                "object_type": "personality",
                "object_id": object_id,
                "pegasus_444_vanilla_source": "common/personalities/00_personalities.txt",
                "working_reference_source": "Workshop 3610149307 v0.10/common/personalities/00_personalities.txt; common/scripted_variables/stellarai_scripted_variables.txt",
                "replacement_policy": "vanilla 4.4.4 full object; replace aggressiveness, bravery, military_spending with verified working-reference values",
                "compatibility_note": "regenerate from pinned 4.4.4 source; conflicts with any later personality overhaul",
            }
        )

    override_rows = (
        (
            "mods/StellarAIDirector/common/country_types/zzzzz_staid_18_native_war_readiness.txt",
            "country_type",
            "default",
            "common/country_types/00_country_types.txt",
            "Stellaris 4.4.4 default country type; 4.4.5 removal of min_navy_for_wars is later-fix evidence",
            "vanilla 4.4.4 full object; omit min_navy_for_wars and set min_assault_armies_for_wars to zero",
            "fresh-game native planner fix; regenerate after any version change",
        ),
        (
            "mods/StellarAIDirector/common/policies/zzzz_staid_10_opening_growth_policies.txt",
            "policy",
            "diplomatic_stance",
            "common/policies/00_policies.txt",
            "Stellaris 4.4.4 policy object; Stellar AI 0.10 phase-transition pattern",
            "vanilla 4.4.4 full object; add temporary opening exit and boxed-in/native-war-posture weights",
            "conflicts with any later diplomatic-stance overhaul; no forced policy changes",
        ),
        (
            "mods/StellarAIDirector/common/policies/zzzz_staid_10_opening_growth_policies.txt",
            "policy",
            "orbital_bombardment",
            "common/policies/00_policies.txt",
            "Stellaris 4.4.4 policy object",
            "vanilla 4.4.4 full object; preserve Director bombardment weighting already owned by this file",
            "included because the replacement policy file must remain a complete current-version object set",
        ),
        (
            "mods/StellarAIDirector/common/policies/zzzz_staid_10_opening_growth_policies.txt",
            "policy",
            "orbital_bombardment_accept_surrender",
            "common/policies/00_policies.txt",
            "Stellaris 4.4.4 policy object",
            "vanilla 4.4.4 full object; preserve Director surrender weighting already owned by this file",
            "included because the replacement policy file must remain a complete current-version object set",
        ),
        (
            "mods/StellarAIDirector/common/ai_budget/zzzz_staid_14_army_recruitment_budget.txt",
            "ai_budget",
            "minerals_expenditure_armies",
            "common/ai_budget/00_minerals_budget.txt",
            "Stellaris 4.4.4 mineral budget; Stellar AI 0.10 native-budget pattern",
            "vanilla 4.4.4 full object; increase weight and add uncapped native desired_min reserves",
            "does not create armies and has no desired_max recruitment cap",
        ),
        (
            "mods/StellarAIDirector/common/ai_budget/zzzz_staid_14_army_recruitment_budget.txt",
            "ai_budget",
            "minerals_expenditure_armies_threatened",
            "common/ai_budget/00_minerals_budget.txt",
            "Stellaris 4.4.4 mineral budget",
            "vanilla 4.4.4 full object; preserve threat lane with bounded Director modifiers",
            "native recruitment only; no scripted units",
        ),
        (
            "mods/StellarAIDirector/common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt",
            "ai_budget",
            "minerals_expenditure_planets_low",
            "common/ai_budget/00_minerals_budget.txt",
            "Stellaris 4.4.4 mineral budget",
            "vanilla 4.4.4 full object plus Director economic pressure; yield part of share during war logistics",
            "prevents construction from starving native army recruitment",
        ),
        (
            "mods/StellarAIDirector/common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt",
            "ai_budget",
            "minerals_expenditure_planets_med",
            "common/ai_budget/00_minerals_budget.txt",
            "Stellaris 4.4.4 mineral budget",
            "vanilla 4.4.4 full object plus Director economic pressure; yield part of share during war logistics",
            "prevents construction from starving native army recruitment",
        ),
        (
            "mods/StellarAIDirector/common/ai_budget/zzzz_staid_14_minerals_planet_construction_budget.txt",
            "ai_budget",
            "minerals_expenditure_planets_high",
            "common/ai_budget/00_minerals_budget.txt",
            "Stellaris 4.4.4 mineral budget",
            "vanilla 4.4.4 full object plus Director economic pressure; yield part of share during war logistics",
            "prevents construction from starving native army recruitment",
        ),
        (
            "mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt",
            "ai_budget",
            "alloys_expenditure_ships",
            "common/ai_budget/00_alloys_budget.txt",
            "Stellaris 4.4.4 ship budget; 4.4.5 high-naval-cap declaration fix is later-fix evidence",
            "vanilla 4.4.4 full object with an always-open category and bounded peacetime >=80% naval-cap dampening",
            "native executable workaround reduces budget share without permanently blocking weak-fleet recovery",
        ),
        (
            "mods/StellarAIDirector/common/ai_budget/zzz_staid_alloys_budget.txt",
            "ai_budget",
            "alloys_expenditure_ship_upgrades",
            "common/ai_budget/00_alloys_budget.txt",
            "Stellaris 4.4.4 ship-upgrade budget",
            "vanilla 4.4.4 full object with native peace and can-upgrade eligibility",
            "no broad runway veto; weight 0.2 and actual upgrade availability bound spending",
        ),
        (
            "mods/StellarAIDirector/common/defines/zzzz_staid_14_high_scale_ai_defines.txt",
            "define_group",
            "NAI",
            "common/defines/00_defines.txt",
            "Stellaris 4.4.4 NAI values; 4.4.5 high-naval-cap declaration fix is later-fix evidence",
            "restore near-vanilla 4.4.4 declaration/preparation/fleet-confidence envelope while preserving Director construction and boss values",
            "define groups overwrite globally; load Director after parent AI mods and do not stack another war-defines mod",
        ),
    )
    for generated_path, object_type, object_id, vanilla_source, reference_source, policy, note in override_rows:
        rows.append(
            {
                "generated_path": generated_path,
                "object_type": object_type,
                "object_id": object_id,
                "pegasus_444_vanilla_source": vanilla_source,
                "working_reference_source": reference_source,
                "replacement_policy": policy,
                "compatibility_note": note,
            }
        )
    return rows


def write_war_planning_444_provenance() -> None:
    write_csv(
        WAR_PLANNING_444_PROVENANCE_CSV,
        war_planning_444_provenance_rows(),
        [
            "generated_path",
            "object_type",
            "object_id",
            "pegasus_444_vanilla_source",
            "working_reference_source",
            "replacement_policy",
            "compatibility_note",
        ],
    )


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


RELATIVE_SCALE_BANDS = (
    (None, 6),
    (6, 15),
    (15, 30),
    (30, 50),
    (50, None),
)

RELATIVE_COLONY_RESOURCE_TARGETS = {
    "energy": {
        "income": (25, 75, 150, 300, 600),
        "stockpile": (1500, 3000, 6000, 10000, 15000),
    },
    "minerals": {
        "income": (25, 75, 150, 300, 600),
        "stockpile": (1500, 3000, 6000, 10000, 15000),
    },
    "alloys": {
        "income": (75, 150, 300, 600, 1200),
        "stockpile": (1500, 3000, 6000, 10000, 15000),
    },
    "consumer_goods": {
        "income": (10, 25, 60, 120, 250),
        "stockpile": (1000, 2000, 4000, 8000, 12000),
    },
    "food": {
        # Food is principally an upkeep buffer: require positive balance, but
        # scale reserves rather than demanding a large net monthly surplus.
        "stockpile": (750, 1500, 3000, 6000, 12000),
    },
}

RELATIVE_ALLOY_FLEET_TARGETS = {
    "income": (
        (None, 10000, 75),
        (10000, 50000, 150),
        (50000, 200000, 300),
        (200000, 500000, 600),
        (500000, 1000000, 1200),
        (1000000, None, 2000),
    ),
    "stockpile": (
        (None, 10000, 1500),
        (10000, 50000, 3000),
        (50000, 200000, 6000),
        (200000, 500000, 10000),
        (500000, 1000000, 15000),
        (1000000, None, 20000),
    ),
}

RELATIVE_BIOSHIP_FOOD_FLEET_TARGETS = {
    "income": (
        (None, 10000, 25),
        (10000, 50000, 75),
        (50000, 200000, 150),
        (200000, 500000, 300),
        (500000, 1000000, 600),
        (1000000, None, 1000),
    ),
    "stockpile": RELATIVE_ALLOY_FLEET_TARGETS["stockpile"],
}

TWO_MONTH_DEFICIT_BANDS = (
    (1000, 2000),
    (500, 1000),
    (250, 500),
    (100, 200),
    (50, 100),
    (25, 50),
    (0, 25),
)


def _scaled_resource_gate_text(
    trigger_id: str,
    metric: str,
    bands: Iterable[tuple[int | None, int | None, int]],
    resource: str,
    measure: str,
) -> str:
    lines = [f"{trigger_id} = {{", "\tOR = {"]
    for lower, upper, target in bands:
        lines.append("\t\tAND = {")
        if lower is not None:
            lines.append(f"\t\t\t{metric} >= {lower}")
        if upper is not None:
            lines.append(f"\t\t\t{metric} < {upper}")
        if measure == "income":
            lines.append(f"\t\t\thas_monthly_income = {{ resource = {resource} value > {target} }}")
        else:
            lines.append(f"\t\t\tresource_stockpile_compare = {{ resource = {resource} value > {target} }}")
        lines.append("\t\t}")
    lines.extend(["\t}", "}"])
    return "\n".join(lines)


def _two_month_runway_trigger_text(resource: str) -> str:
    lines = [f"staid_{resource}_two_month_runway_unsafe = {{", "\tOR = {", f"\t\thas_deficit = {resource}"]
    for deficit, stockpile in TWO_MONTH_DEFICIT_BANDS:
        operator = "<" if deficit == 0 else "<="
        income = 0 if deficit == 0 else -deficit
        lines.extend(
            [
                "\t\tAND = {",
                f"\t\t\thas_monthly_income = {{ resource = {resource} value {operator} {income} }}",
                f"\t\t\tresource_stockpile_compare = {{ resource = {resource} value < {stockpile} }}",
                "\t\t}",
            ]
        )
    lines.extend(["\t}", "}"])
    return "\n".join(lines)


def relative_economic_runway_triggers_text() -> str:
    blocks = [
        "# Country-scope relative economic standards. Colony bands scale civilian",
        "# construction/upkeep capacity; fleet-power bands separately scale alloy",
        "# replacement income and reserves. Both alloy standards must pass.",
    ]
    for resource, targets in RELATIVE_COLONY_RESOURCE_TARGETS.items():
        for measure, values in targets.items():
            bands = [
                (lower, upper, int(values[index]))
                for index, (lower, upper) in enumerate(RELATIVE_SCALE_BANDS)
            ]
            blocks.append(
                _scaled_resource_gate_text(
                    f"staid_scaled_{resource}_{measure}_safe",
                    "num_owned_planets",
                    bands,
                    resource,
                    measure,
                )
            )
    for measure, bands in RELATIVE_ALLOY_FLEET_TARGETS.items():
        blocks.append(
            _scaled_resource_gate_text(
                f"staid_scaled_alloy_fleet_{measure}_safe",
                "fleet_power",
                bands,
                "alloys",
                measure,
            )
        )
    for measure, bands in RELATIVE_BIOSHIP_FOOD_FLEET_TARGETS.items():
        blocks.append(
            _scaled_resource_gate_text(
                f"staid_scaled_bioship_food_fleet_{measure}_safe",
                "fleet_power",
                bands,
                "food",
                measure,
            )
        )
    for resource in ("energy", "minerals", "alloys", "trade", "consumer_goods", "food"):
        blocks.append(_two_month_runway_trigger_text(resource))
    text = "\n\n".join(blocks) + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def relative_economic_standard_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for resource, targets in RELATIVE_COLONY_RESOURCE_TARGETS.items():
        for measure, values in targets.items():
            for index, (lower, upper) in enumerate(RELATIVE_SCALE_BANDS):
                rows.append(
                    {
                        "basis": "owned_colonies",
                        "resource": resource,
                        "measure": measure,
                        "lower_inclusive": "" if lower is None else lower,
                        "upper_exclusive": "" if upper is None else upper,
                        "target": values[index],
                        "consumer_trigger": f"staid_scaled_{resource}_{measure}_safe",
                        "rationale": (
                            "maintenance balance plus scaled reserve"
                            if resource == "food"
                            else "civilian economy scale and construction/upkeep headroom"
                        ),
                    }
                )
    for measure, bands in RELATIVE_ALLOY_FLEET_TARGETS.items():
        for lower, upper, target in bands:
            rows.append(
                {
                    "basis": "current_fleet_power",
                    "resource": "alloys",
                    "measure": measure,
                    "lower_inclusive": "" if lower is None else lower,
                    "upper_exclusive": "" if upper is None else upper,
                    "target": target,
                    "consumer_trigger": f"staid_scaled_alloy_fleet_{measure}_safe",
                    "rationale": (
                        "fleet replacement throughput"
                        if measure == "income"
                        else "capped military operating float; surplus remains investable"
                    ),
                }
            )
    for measure, bands in RELATIVE_BIOSHIP_FOOD_FLEET_TARGETS.items():
        for lower, upper, target in bands:
            rows.append(
                {
                    "basis": "bio_ship_fleet_power",
                    "resource": "food",
                    "measure": measure,
                    "lower_inclusive": "" if lower is None else lower,
                    "upper_exclusive": "" if upper is None else upper,
                    "target": target,
                    "consumer_trigger": f"staid_scaled_bioship_food_fleet_{measure}_safe",
                    "rationale": (
                        "biological-ship replacement throughput"
                        if measure == "income"
                        else "capped biological-fleet operating float; surplus remains investable"
                    ),
                }
            )
    return rows


def relative_economic_standards_text(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Stellar AI Director Relative Economic Standards",
        "",
        "Generated 2026-07-09 for the 4.4.5-forward / 4.4.4-compatible Director build.",
        "",
        "These are country-scope, piecewise relative standards. Colony bands scale civilian-resource headroom. Alloy safety must pass both the colony band and the current-fleet-power income band, so a large empire or fleet cannot qualify on an early-game flat floor. Stockpile targets are capped operating floats, not full replacement-cost warehouses. Ordinary food economies require positive monthly balance and a colony-scaled reserve; biological-ship empires additionally scale food income and operating reserves with fleet power.",
        "",
        "| basis | resource | measure | lower inclusive | upper exclusive | target | consumer trigger | rationale |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['basis']} | {row['resource']} | {row['measure']} | {row['lower_inclusive']} | "
            f"{row['upper_exclusive']} | {row['target']} | `{row['consumer_trigger']}` | {row['rationale']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The thresholds are net monthly income after upkeep, not gross production.",
            "- Current fleet power deliberately lowers the military replacement-income band after catastrophic losses, while the colony band still requires a large empire to retain strong baseline throughput.",
            "- Biological-ship empires use the colony alloy band for non-ship infrastructure but replace the alloy fleet burden with a food fleet burden.",
            "- The largest alloy/biological-food military float is 20,000. Surplus above the operating float remains available to megastructures, fleet construction, and other high-return sinks; no normal state attempts to pre-fund an entire fleet replacement.",
            "- A much larger reserve should only be introduced later behind explicit strategic evidence such as imminent total-war exposure or a known catastrophic battle, not as a default scale rule.",
            "- These are safety gates for discretionary expansion, research scaling, fleet growth, and fortress investment; deficit-repair plans remain active below them.",
            "- The economic plan generates 37 mutually exclusive colony/fleet repair bands. Each unsafe gate requires both earned monthly income and an operating float, so a market purchase can delay depletion but cannot make the economy count as repaired.",
            "- Hard-shortage detection approximates two months of runway with deficit-magnitude bands because Stellaris exposes income and stockpile comparisons but not stockpile/income division.",
            "- Core repair subplans request domestic resource income directly and contain no trade-income target. Director-owned market code has no buy path; its only market action is a positive-income, no-deficit overflow sale above the fixed reserve and 90% of the mods-included storage cap.",
            "- Near-cap pressure also opens the source-proven Kugelblitz storage route when megastructure commitment is otherwise safe; storage expansion buys investment time but does not replace income repair.",
            "- Runtime observation is still required to tune band boundaries against the active mod stack.",
        ]
    )
    return "\n".join(lines) + "\n"


def generate_relative_economic_standard_artifacts() -> list[dict[str, Any]]:
    rows = relative_economic_standard_rows()
    write_csv(RELATIVE_ECONOMIC_STANDARDS_CSV, rows)
    write_text_file(RELATIVE_ECONOMIC_STANDARDS_MD, relative_economic_standards_text(rows))
    return rows


def research_colony_plan_triggers_text() -> str:
    soft_cap_branches = []
    for cap in range(1, 21):
        minimum_colonies = cap * 3
        maximum_clause = f"\n\t\tnum_owned_colonies < {minimum_colonies + 3}" if cap < 20 else ""
        soft_cap_branches.append(
            f'''\tAND = {{
\t\tnum_owned_colonies >= {minimum_colonies}{maximum_clause}
\t\tcount_owned_colony = {{
\t\t\tlimit = {{ has_designation = col_research }}
\t\t\tcount < {cap}
\t\t}}
\t}}'''
        )
    soft_cap = "\n".join(soft_cap_branches)
    return '''# Native colony-scope research role quality and country-scope soft ceiling.
# This intentionally counts realized designations, never persistent event flags.
staid_good_research_candidate = {
\tOR = {
\t\tcheck_modifier_value = { modifier = planet_researchers_produces_mult value > 0.09 }
\t\tcheck_modifier_value = { modifier = planet_researchers_physics_research_produces_mult value > 0.09 }
\t\tcheck_modifier_value = { modifier = planet_researchers_society_research_produces_mult value > 0.09 }
\t\tcheck_modifier_value = { modifier = planet_researchers_engineering_research_produces_mult value > 0.09 }
\t\thas_any_research_zone = yes
\t\thas_building = building_research_lab_1
\t\thas_building = building_research_lab_2
\t\thas_building = building_research_lab_3
\t}
}

staid_research_role_high_conversion_cost = {
\tOR = {
\t\tAND = {
\t\t\thas_any_generator_zone = yes
\t\t\tnum_districts = { type = district_generator value > 3 }
\t\t}
\t\tAND = {
\t\t\thas_any_mining_zone = yes
\t\t\tnum_districts = { type = district_mining value > 3 }
\t\t}
\t\tAND = {
\t\t\thas_any_agriculture_zone = yes
\t\t\tnum_districts = { type = district_farming value > 3 }
\t\t}
\t\tAND = {
\t\t\thas_any_industrial_zone = yes
\t\t\tOR = {
\t\t\t\tnum_districts = { type = district_city value > 3 }
\t\t\t\tnum_districts = { type = district_hive value > 3 }
\t\t\t\tnum_districts = { type = district_nexus value > 3 }
\t\t\t}
\t\t}
\t\tAND = {
\t\t\thas_any_trade_zone = yes
\t\t\tOR = {
\t\t\t\tnum_districts = { type = district_city value > 3 }
\t\t\t\tnum_districts = { type = district_hive value > 3 }
\t\t\t\tnum_districts = { type = district_nexus value > 3 }
\t\t\t}
\t\t}
\t}
}

staid_research_role_reachable = {
\tis_colony = yes
\tis_capital = no
\tis_special_colony_type = no
\texists = owner
\towner = {
\t\tis_ai = yes
\t\tis_nomadic = no
\t}
\tNOT = { is_planet_class = pc_nanotech }
\tNOR = {
\t\tuses_district_set = city_world
\t\tuses_district_set = ring_world
\t\tuses_district_set = habitat
\t\tuses_district_set = cosmogenesis_world
\t}
\tOR = {
\t\tstaid_good_research_candidate = yes
\t\tAND = {
\t\t\tstaid_research_role_high_conversion_cost = no
\t\t\tnum_districts = { type = district_city value > 0 }
\t\t\thas_any_generator_zone = no
\t\t\thas_any_mining_zone = no
\t\t\thas_any_agriculture_zone = no
\t\t\thas_any_industrial_zone = no
\t\t\thas_any_trade_zone = no
\t\t\thas_any_unity_zone = no
\t\t\thas_any_fortress_zone = no
\t\t\tnum_zones = { type = zone_urban value < 1 }
\t\t}
\t}
}

staid_research_designation_under_soft_cap = {
\tOR = {
$SOFT_CAP$
\t}
}

staid_research_role_candidate = {
\tstaid_research_role_reachable = yes
\towner = {
\t\tNOT = { staid_catastrophic_collapse_mode = yes }
\t\tstaid_energy_two_month_runway_unsafe = no
\t\tOR = {
\t\t\tcountry_uses_consumer_goods = no
\t\t\tstaid_consumer_goods_two_month_runway_unsafe = no
\t\t}
\t\tstaid_research_designation_under_soft_cap = yes
\t}
}
'''.replace("$SOFT_CAP$", soft_cap)


def science_route_system_restriction_game_rule_text() -> str:
    """Restrict inaccessible contacted systems before native AI route selection."""
    source_path = mod_source_root_for_id("3728581560") / "common" / "game_rules" / "scfe_game_rules.txt"
    source_object = extract_top_level_object_text(read_text(source_path), "ai_should_restrict_system")
    expected_source_sha256 = "2f0c0512ef0ec300f6ad53c643683a234fb09a695bd66a0cc938f3ed327c586a"
    source_sha256 = hashlib.sha256(source_object.encode("utf-8")).hexdigest()
    if source_sha256 != expected_source_sha256:
        raise ValueError(
            f"Forgotten Empires ai_should_restrict_system changed: expected {expected_source_sha256}, got {source_sha256}"
        )
    object_marker = "ai_should_restrict_system = {\n    OR = {\n"
    if source_object.count(object_marker) != 1:
        raise ValueError(f"Expected one ai_should_restrict_system OR marker in {source_path}")
    access_branch = '''        AND = {
            root = {
                is_country_type = default
            }
            exists = owner
            owner = {
                NOT = { is_same_value = root }
                has_communications = root
                NOT = { is_at_war_with = root }
            }
            NOT = { has_access_fleet = root }
        }
'''
    patched_object = source_object.replace(object_marker, object_marker + access_branch, 1)
    parse_pdx(patched_object)
    return (
        "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
        "# Full-object override copied from the active Forgotten Empires 3728581560 winner.\n"
        "# Only Director delta: default AI empires avoid contacted foreign systems they cannot enter while at peace.\n"
        "# Current access is evaluated by the native game rule; this stores no retry state and does not disable cloaking.\n\n"
        + patched_object
    )


def triggers_text(thresholds: dict[str, int]) -> str:
    text = '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Deterministic state gates for late-game investment decisions.

''' + relative_economic_runway_triggers_text() + research_colony_plan_triggers_text() + '''
staid_core_deficit_short_runway = {
\tOR = {
\t\tstaid_energy_two_month_runway_unsafe = yes
\t\tstaid_minerals_two_month_runway_unsafe = yes
\t\tstaid_alloys_two_month_runway_unsafe = yes
\t\tstaid_trade_two_month_runway_unsafe = yes
\t\tAND = {
\t\t\tcountry_uses_consumer_goods = yes
\t\t\tstaid_consumer_goods_two_month_runway_unsafe = yes
\t\t}
\t\tAND = {
\t\t\tcountry_uses_food = yes
\t\t\tstaid_food_two_month_runway_unsafe = yes
\t\t}
\t}
}

staid_consumer_goods_runway_safe = {
\tOR = {
\t\tNOT = { country_uses_consumer_goods = yes }
\t\tAND = {
\t\t\tNOT = { has_deficit = consumer_goods }
\t\t\tstaid_scaled_consumer_goods_income_safe = yes
\t\t\tstaid_scaled_consumer_goods_stockpile_safe = yes
\t\t}
\t}
}

staid_energy_runway_safe = {
\tNOT = { has_deficit = energy }
\tstaid_scaled_energy_income_safe = yes
\tstaid_scaled_energy_stockpile_safe = yes
}

staid_mineral_runway_safe = {
\tNOT = { has_deficit = minerals }
\tstaid_scaled_minerals_income_safe = yes
\tstaid_scaled_minerals_stockpile_safe = yes
}

staid_alloy_colony_runway_safe = {
\tNOT = { has_deficit = alloys }
\tstaid_scaled_alloys_income_safe = yes
\tstaid_scaled_alloys_stockpile_safe = yes
}

staid_alloy_runway_safe = {
\tstaid_alloy_colony_runway_safe = yes
\tOR = {
\t\tcountry_uses_bio_ships = yes
\t\tAND = {
\t\t\tstaid_scaled_alloy_fleet_income_safe = yes
\t\t\tstaid_scaled_alloy_fleet_stockpile_safe = yes
\t\t}
\t}
}

staid_food_colony_runway_safe = {
\tNOT = { has_deficit = food }
\thas_monthly_income = { resource = food value > 0 }
\tstaid_scaled_food_stockpile_safe = yes
}

staid_food_runway_safe = {
\tOR = {
\t\tNOT = { country_uses_food = yes }
\t\tAND = {
\t\t\tstaid_food_colony_runway_safe = yes
\t\t\tOR = {
\t\t\t\tNOT = { country_uses_bio_ships = yes }
\t\t\t\tAND = {
\t\t\t\t\tstaid_scaled_bioship_food_fleet_income_safe = yes
\t\t\t\t\tstaid_scaled_bioship_food_fleet_stockpile_safe = yes
\t\t\t\t}
\t\t\t}
\t\t}
\t}
}

staid_research_input_runway_safe = {
\tstaid_consumer_goods_runway_safe = yes
\tstaid_energy_runway_safe = yes
}

staid_research_minimum_input_runway_safe = {
\tstaid_consumer_goods_runway_safe = yes
\tNOT = { has_deficit = energy }
\thas_monthly_income = { resource = energy value > 25 }
}

staid_research_diplomacy_priority_ready = {
\tNOT = { staid_survival_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tOR = {
\t\tstaid_science_nexus_research_priority_ready = yes
\t\tstaid_research_input_runway_safe = yes
\t\thas_ethic = ethic_materialist
\t\thas_ethic = ethic_fanatic_materialist
\t\thas_authority = auth_machine_intelligence
\t\thas_active_tradition = tr_discovery_federations_finish
\t}
}

staid_basic_economy_runway_safe = {
\tstaid_research_input_runway_safe = yes
\tstaid_food_runway_safe = yes
\tstaid_mineral_runway_safe = yes
\tstaid_alloy_runway_safe = yes
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

staid_high_scale_snowball_pressure = {
\tis_nomadic = no
\tOR = {
\t\tresource_stockpile_compare = { resource = minerals value > 25000 }
\t\tresource_stockpile_compare = { resource = energy value > 50000 }
\t\tresource_stockpile_compare = { resource = alloys value > 15000 }
\t\tAND = {
\t\t\tyears_passed > 79
\t\t\thas_monthly_income = { resource = minerals value > 500 }
\t\t\thas_monthly_income = { resource = energy value > 500 }
\t\t\thas_monthly_income = { resource = alloys value > 500 }
\t\t}
\t\tAND = {
\t\t\tyears_passed > 119
\t\t\tresource_stockpile_compare = { resource = minerals value > 12000 }
\t\t\tresource_stockpile_compare = { resource = energy value > 12000 }
\t\t}
\t}
}

staid_catastrophic_collapse_mode = {
\tis_nomadic = no
\tOR = {
\t\tAND = { has_deficit = energy resource_stockpile_compare = { resource = energy value < 600 } }
\t\tAND = { has_deficit = minerals resource_stockpile_compare = { resource = minerals value < 600 } }
\t\tAND = { has_deficit = alloys resource_stockpile_compare = { resource = alloys value < 600 } }
\t\tAND = { country_uses_consumer_goods = yes has_deficit = consumer_goods resource_stockpile_compare = { resource = consumer_goods value < 400 } }
\t\tAND = { country_uses_food = yes has_deficit = food resource_stockpile_compare = { resource = food value < 400 } }
\t\tAND = { is_at_war = yes highest_threat > 50 used_naval_capacity_percent < 0.45 }
\t\tAND = { recently_lost_war = yes used_naval_capacity_percent < 0.35 }
\t}
}

staid_survival_mode = {
\tis_nomadic = no
\tOR = {
\t\tstaid_catastrophic_collapse_mode = yes
\t\tAND = { recently_lost_war = yes used_naval_capacity_percent < 0.45 }
\t\tAND = { is_at_war = yes highest_threat > 60 used_naval_capacity_percent < 0.55 }
\t}
}

staid_recovery_mode = {
\tis_nomadic = no
\tOR = {
\t\tstaid_catastrophic_collapse_mode = yes
\t\tAND = { recently_lost_war = yes used_naval_capacity_percent < 0.50 }
\t}
}

staid_megastructure_prep_ready = {
\tis_nomadic = no
\tcan_build_megastructures = yes
\tNOT = { staid_recovery_mode = yes }
\tstaid_basic_economy_runway_safe = yes
\tstaid_trade_planetary_capacity_safe = yes
\tresource_stockpile_compare = { resource = alloys value > 8000 }
\thas_monthly_income = { resource = alloys value > 80 }
\thas_monthly_income = { resource = energy value > 40 }
\thas_monthly_income = { resource = minerals value > 40 }
\tOR = {
\t\tis_at_war = no
\t\tused_naval_capacity_percent > 0.70
\t}
}

staid_megastructure_commit_safe = {
\tis_nomadic = no
\tcan_build_megastructures = yes
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_basic_economy_runway_safe = yes
\tstaid_trade_planetary_capacity_safe = yes
\tOR = {
\t\tis_at_war = no
\t\tused_naval_capacity_percent > 0.65
\t}
}

staid_megastructure_continuation_priority_ready = {
\tstaid_megastructure_commit_safe = yes
\tNOT = { staid_survival_mode = yes }
\tOR = {
\t\tstaid_surplus_sink_pressure = yes
\t\tstaid_resource_waste_pressure = yes
\t}
}

staid_pause_new_megastructure = {
\tOR = {
\t\tstaid_survival_mode = yes
\t\tAND = { is_at_war = yes used_naval_capacity_percent < 0.55 }
\t\tAND = { highest_threat > 75 used_naval_capacity_percent < 0.65 }
\t}
}

staid_shipyard_payoff_ready = {
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tOR = {
\t\thas_monthly_income = { resource = alloys value > 80 }
\t\tresource_stockpile_compare = { resource = alloys value > 5000 }
\t\tstaid_high_scale_snowball_pressure = yes
\t}
\tOR = {
\t\thas_monthly_income = { resource = energy value > 80 }
\t\tresource_stockpile_compare = { resource = energy value > 5000 }
\t\tstaid_high_scale_snowball_pressure = yes
\t}
\tOR = {
\t\tresource_stockpile_compare = { resource = alloys value > 10000 }
\t\tAND = {
\t\t\tused_naval_capacity_percent < 1.60
\t\t\thas_monthly_income = { resource = alloys value > 80 }
\t\t}
\t\tAND = {
\t\t\tused_naval_capacity_percent < 1.40
\t\t\thas_monthly_income = { resource = alloys value > 80 }
\t\t}
\t}
}

staid_fleet_buildup_economy_safe = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_basic_economy_runway_safe = yes
\thas_monthly_income = { resource = alloys value > 0 }
\tused_naval_capacity_percent < 1.40
}

# Native affordability/resource-share support for a rich wartime empire whose
# existing templates are satisfied far below naval capacity. This only funds
# the lane; NSC3 ai_ship_data remains responsible for demand and composition.
staid_wartime_fleet_surge_ready = {
\tis_ai = yes
\tis_country_type = default
\tis_nomadic = no
\tis_at_war = yes
\tcountry_uses_bio_ships = no
\tuses_standard_ship_sizes = yes
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_energy_two_month_runway_unsafe = no
\tstaid_alloys_two_month_runway_unsafe = no
\tused_naval_capacity_percent < 0.90
\tOR = {
\t\thas_technology = tech_battleships
\t\thas_technology = tech_Battlecruiser_1
\t\thas_technology = tech_Carrier_1
\t\thas_technology = tech_Dreadnought_1
\t}
\tresource_stockpile_compare = { resource = alloys value > 5000 }
}

staid_emergency_fleet_spending_required = {
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tOR = {
\t\trecently_lost_war = yes
\t\tAND = {
\t\t\tis_at_war = yes
\t\t\tOR = {
\t\t\t\thighest_threat > 35
\t\t\t\tused_naval_capacity_percent < 0.85
\t\t\t}
\t\t}
\t\tAND = {
\t\t\thighest_threat > 60
\t\t\tused_naval_capacity_percent < 0.85
\t\t}
\t}
}

staid_fortress_designation_ready = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_basic_economy_runway_safe = yes
\tNOT = { has_deficit = alloys }
\thas_monthly_income = { resource = alloys value > 0 }
\tnum_owned_planets >= 6
\tused_naval_capacity_percent > 0.70
\tOR = {
\t\tis_at_war = yes
\t\trecently_lost_war = yes
\t\thighest_threat > 50
\t\tAND = {
\t\t\tnum_owned_planets >= 10
\t\t\thighest_threat > 25
\t\t}
\t}
}

# Planet scope. Stellaris computes bottlenecks from the current hyperlane graph;
# vanilla planet-scope decisions use the same planet -> solar_system scope change.
staid_fortress_planet_strategically_placed = {
\texists = owner
\tsolar_system = { is_bottleneck_system = yes }
}

staid_resource_waste_pressure = {
\tOR = {
\t\tAND = {
\t\t\thas_monthly_income = { resource = minerals value > 0 }
\t\t\tresource_stockpile_compare = { resource = minerals value > 25000 }
\t\t}
\t\tAND = {
\t\t\tcountry_uses_food = yes
\t\t\thas_monthly_income = { resource = food value > 0 }
\t\t\tresource_stockpile_compare = { resource = food value > 18000 }
\t\t}
\t\tAND = {
\t\t\tcountry_uses_consumer_goods = yes
\t\t\thas_monthly_income = { resource = consumer_goods value > 0 }
\t\t\tresource_stockpile_compare = { resource = consumer_goods value > 18000 }
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

staid_unemployment_construction_pressure = {
\tis_nomadic = no
\tany_owned_planet = { num_unemployed > 0 }
}

staid_construction_spenddown_pressure = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tOR = {
\t\tstaid_high_scale_snowball_pressure = yes
\t\tstaid_resource_waste_pressure = yes
\t\tstaid_unemployment_construction_pressure = yes
\t\tany_owned_planet = { free_building_slots > 0 num_unemployed > 0 }
\t\tresource_stockpile_compare = { resource = minerals value > 10000 }
\t}
}

staid_research_under_curve = {
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tOR = {
\t\tstaid_research_input_runway_safe = yes
\t\tstaid_research_minimum_input_runway_safe = yes
\t\tstaid_high_scale_snowball_pressure = yes
\t}
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

staid_research_construction_priority_ready = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tstaid_research_minimum_input_runway_safe = yes
\tOR = {
\t\tstaid_research_input_runway_safe = yes
\t\tstaid_high_scale_snowball_pressure = yes
\t\tstaid_research_under_curve = yes
\t}
}

staid_surplus_sink_pressure = {
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_research_minimum_input_runway_safe = yes
\tNOT = { has_deficit = alloys }
\tNOT = { has_deficit = energy }
\tOR = {
\t\tstaid_resource_waste_pressure = yes
\t\tstaid_high_scale_snowball_pressure = yes
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

staid_early_kilo_economy_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		years_passed > 29
		staid_resource_waste_pressure = yes
		staid_research_under_curve = yes
	}
}

staid_early_kilo_economy_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	OR = {
		has_technology = tech_orbital_arc_furnace
		has_technology = giga_tech_asteroid_manufactory
	}
	OR = {
		staid_resource_waste_pressure = yes
		AND = {
			has_monthly_income = { resource = alloys value > 120 }
			resource_stockpile_compare = { resource = alloys value > 5000 }
		}
	}
}

staid_science_kilo_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_research_under_curve = yes
		AND = {
			years_passed > 24
			staid_early_kilo_economy_research_priority_ready = yes
		}
	}
}

staid_science_kilo_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	OR = {
		has_technology = giga_tech_engineering_test_site
		has_technology = giga_tech_macro_scale_weather_manipulation
	}
	OR = {
		staid_research_under_curve = yes
		AND = {
			has_monthly_income = { resource = alloys value > 90 }
			resource_stockpile_compare = { resource = alloys value > 3000 }
		}
	}
}

staid_pop_assembly_snowball_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_basic_economy_runway_safe = yes
		staid_high_scale_snowball_pressure = yes
		staid_construction_spenddown_pressure = yes
	}
	OR = {
		years_passed > 4
		staid_planetary_capacity_growth_ready = yes
		staid_research_under_curve = yes
	}
}

staid_planetary_computer_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_research_under_curve = yes
		AND = {
			years_passed > 69
			staid_core_unlock_research_priority_ready = yes
		}
	}
}

staid_planetary_computer_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	has_technology = giga_tech_planetary_computer
	OR = {
		staid_research_under_curve = yes
		staid_planetary_capacity_growth_ready = yes
		resource_stockpile_compare = { resource = alloys value > 12000 }
	}
}

staid_science_nexus_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_research_under_curve = yes
		AND = {
			years_passed > 44
			staid_core_unlock_research_priority_ready = yes
		}
	}
}

staid_science_nexus_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	has_technology = tech_science_nexus
	OR = {
		staid_research_under_curve = yes
		resource_stockpile_compare = { resource = alloys value > 15000 }
	}
}

staid_ring_world_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_planetary_capacity_growth_ready = yes
		AND = {
			years_passed > 79
			staid_core_unlock_research_priority_ready = yes
		}
	}
}

staid_ring_world_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	has_technology = tech_ring_world
	OR = {
		staid_planetary_capacity_growth_ready = yes
		resource_stockpile_compare = { resource = alloys value > 20000 }
	}
}

staid_storage_cap_research_priority_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_resource_waste_pressure = yes
		AND = {
			years_passed > 44
			staid_surplus_sink_pressure = yes
		}
	}
}

staid_storage_cap_build_priority_ready = {
	staid_megastructure_commit_safe = yes
	has_technology = giga_tech_kugelblitz
	OR = {
		country_near_tangible_resource_cap = yes
		staid_resource_waste_pressure = yes
		staid_high_scale_snowball_pressure = yes
		resource_stockpile_compare = { resource = energy value > 25000 }
	}
}

staid_unfinished_kugelblitz_exists = {
	any_owned_megastructure = {
		OR = {
			is_megastructure_type = kugelblitz_0
			is_megastructure_type = kugelblitz_1
			is_megastructure_type = kugelblitz_2
			is_megastructure_type = kugelblitz_restored
		}
	}
}

staid_kugelblitz_new_start_budget_ready = {
	staid_storage_cap_build_priority_ready = yes
	NOT = { has_country_flag = is_currently_building_kugelblitz }
	NOT = { staid_unfinished_kugelblitz_exists = yes }
	NOT = { check_variable = { which = giga_current_kugel value >= 10 } }
	OR = {
		check_variable = { which = giga_current_kugel value < 4 }
		AND = {
			staid_resource_waste_pressure = yes
			check_variable = { which = giga_current_kugel value < 6 }
		}
		AND = {
			staid_high_scale_snowball_pressure = yes
			check_variable = { which = giga_current_kugel value < 8 }
		}
	}
}

staid_phase_mega_engineering_rush = {
	NOT = { has_technology = tech_mega_engineering }
	staid_core_unlock_research_priority_ready = yes
}

staid_phase_early_kilo_economy = {
	OR = {
		NOT = { has_technology = tech_orbital_arc_furnace }
		NOT = { has_technology = giga_tech_asteroid_manufactory }
	}
	staid_early_kilo_economy_research_priority_ready = yes
}

staid_phase_science_kilo_snowball = {
	OR = {
		NOT = { has_technology = giga_tech_engineering_test_site }
		NOT = { has_technology = giga_tech_macro_scale_weather_manipulation }
	}
	staid_science_kilo_research_priority_ready = yes
}

staid_phase_pop_assembly_snowball = {
	staid_pop_assembly_snowball_ready = yes
	OR = {
		NOT = { has_technology = tech_robotic_workers }
		NOT = { has_technology = tech_cloning }
		NOT = { has_technology = tech_robot_assembly_complex }
	}
}

staid_phase_science_nexus_rush = {
	NOT = { has_technology = tech_science_nexus }
	staid_science_nexus_research_priority_ready = yes
}

staid_phase_planetary_computer_research = {
	NOT = { has_technology = giga_tech_planetary_computer }
	staid_planetary_computer_research_priority_ready = yes
}

staid_phase_ring_world_growth = {
	NOT = { has_technology = tech_ring_world }
	staid_ring_world_research_priority_ready = yes
}

staid_phase_storage_cap_expansion = {
	NOT = { has_technology = giga_tech_kugelblitz }
	staid_storage_cap_research_priority_ready = yes
}

staid_phase_boxed_tall_habitat_escape = {
	staid_planetary_capacity_growth_ready = yes
	OR = {
		NOT = { has_technology = tech_habitat_1 }
		NOT = { has_technology = giga_tech_interstellar_habitat }
		NOT = { has_technology = giga_tech_stellar_ring_habitat }
	}
}

staid_phase_galactic_wonders_entry = {
	has_technology = tech_mega_engineering
	NOT = { has_ascension_perk = ap_galactic_wonders }
	OR = {
		staid_unity_sink_priority_ready = yes
		staid_surplus_sink_pressure = yes
		years_passed > 79
	}
}

staid_phase_gigastructural_constructs_rush = {
	has_ascension_perk = ap_galactic_wonders
	NOT = { has_ascension_perk = ap_gigastructural_constructs }
	OR = {
		staid_core_unlock_research_priority_ready = yes
		staid_unity_sink_priority_ready = yes
		years_passed > 79
	}
}

staid_phase_planetcraft_rush = {
	has_ascension_perk = ap_gigastructural_constructs
	NOT = { has_technology = giga_tech_planet_assembly }
	staid_planetcraft_research_priority_ready = yes
}

staid_phase_systemcraft_escalation = {
	has_ascension_perk = ap_celestial_printing
	NOT = { has_technology = giga_tech_war_system_1 }
	staid_systemcraft_research_priority_ready = yes
}

staid_phase_fleet_conversion_repeatables = {
	OR = {
		has_technology = tech_Carrier_1
		has_technology = tech_Dreadnought_1
		has_technology = tech_Flagship_1
		has_technology = giga_tech_war_moon_2
		has_technology = giga_tech_war_system_1
		has_technology = esc_tech_dark_matter_power_core_2
	}
}

staid_shipyard_expansion_ready = {
\thas_technology = tech_mega_shipyard
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tused_naval_capacity_percent < 1.85
\tOR = {
\t\thas_monthly_income = { resource = alloys value > 80 }
\t\tresource_stockpile_compare = { resource = alloys value > 5000 }
\t\tstaid_high_scale_snowball_pressure = yes
\t}
\tOR = {
\t\tstaid_surplus_sink_pressure = yes
\t\tAND = { is_at_war = yes highest_threat > 35 used_naval_capacity_percent > 0.80 }
\t}
}

staid_fleet_payoff_exploitation_ready = {
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_fleet_buildup_economy_safe = yes
\tOR = {
\t\tAND = { is_at_war = yes highest_threat > 35 }
\t\tAND = { staid_aggressive_fleet_pressure = yes resource_stockpile_compare = { resource = alloys value > 12000 } resource_stockpile_compare = { resource = energy value > 5000 } }
\t}
}

staid_advanced_component_resource_support_ready = {
	NOT = { staid_catastrophic_collapse_mode = yes }
	NOT = { staid_core_deficit_short_runway = yes }
	OR = {
		staid_basic_economy_runway_safe = yes
		staid_high_scale_snowball_pressure = yes
	}
	staid_trade_fleet_capacity_safe = yes
	OR = {
		has_monthly_income = { resource = volatile_motes value > 5 }
		has_monthly_income = { resource = exotic_gases value > 5 }
		has_monthly_income = { resource = rare_crystals value > 5 }
		has_monthly_income = { resource = sr_dark_matter value > 1 }
		has_monthly_income = { resource = sr_zro value > 1 }
		has_monthly_income = { resource = nanites value > 1 }
		has_monthly_income = { resource = giga_sr_sentient_metal value > 1 }
		has_monthly_income = { resource = giga_sr_negative_mass value > 1 }
		has_monthly_income = { resource = giga_sr_amb_megaconstruction value > 1 }
		staid_resource_waste_pressure = yes
	}
}

staid_nsc3_capital_hull_unlock_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	OR = {
		staid_phase_fleet_conversion_repeatables = yes
		AND = {
			years_passed > 79
			OR = {
				resource_stockpile_compare = { resource = alloys value > 5000 }
				has_monthly_income = { resource = alloys value > 80 }
			}
		}
	}
}

staid_esc_component_unlock_ready = {
	is_nomadic = no
	NOT = { staid_catastrophic_collapse_mode = yes }
	staid_advanced_component_resource_support_ready = yes
	OR = {
		staid_phase_fleet_conversion_repeatables = yes
		AND = {
			years_passed > 79
			OR = {
				resource_stockpile_compare = { resource = alloys value > 5000 }
				has_monthly_income = { resource = engineering_research value > 600 }
			}
		}
	}
}

staid_modded_fleet_conversion_ready = {
	NOT = { staid_catastrophic_collapse_mode = yes }
	staid_advanced_component_resource_support_ready = yes
	OR = {
		has_technology = tech_Carrier_1
		has_technology = tech_Dreadnought_1
		has_technology = tech_Flagship_1
		has_technology = giga_tech_war_moon_2
		has_technology = giga_tech_war_system_1
		has_technology = esc_tech_dark_matter_power_core_2
	}
}

staid_planetary_capacity_growth_ready = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tOR = {
\t\tstaid_basic_economy_runway_safe = yes
\t\tstaid_high_scale_snowball_pressure = yes
\t}
\tOR = {
\t\thas_monthly_income = { resource = minerals value > 40 }
\t\tresource_stockpile_compare = { resource = minerals value > 2500 }
\t\tstaid_high_scale_snowball_pressure = yes
\t}
\tOR = {
\t\thas_monthly_income = { resource = energy value > 40 }
\t\tresource_stockpile_compare = { resource = energy value > 2500 }
\t\tstaid_high_scale_snowball_pressure = yes
\t}
}

staid_planetary_diversity_outpost_investment_ready = {
\tis_nomadic = no
\tNOT = { staid_survival_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tNOT = { has_deficit = minerals }
\tNOT = { has_deficit = energy }
\thas_monthly_income = { resource = minerals value > 20 }
\thas_monthly_income = { resource = energy value > 20 }
\tresource_stockpile_compare = { resource = minerals value > 1200 }
\tresource_stockpile_compare = { resource = energy value > 1000 }
}

staid_pd_research_outpost_priority_ready = {
\tstaid_planetary_diversity_outpost_investment_ready = yes
\tOR = {
\t\tstaid_research_under_curve = yes
\t\tstaid_research_input_runway_safe = yes
\t}
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
\tNOT = { staid_catastrophic_collapse_mode = yes }
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
\tNOT = { staid_catastrophic_collapse_mode = yes }
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
\tNOT = { staid_catastrophic_collapse_mode = yes }
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
\tNOT = { staid_catastrophic_collapse_mode = yes }
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
\t\thas_ethic = ethic_militarist
\t\thas_ethic = ethic_fanatic_militarist
\t\thas_ethic = ethic_xenophobe
\t\thas_ethic = ethic_fanatic_xenophobe
\t\thas_valid_civic = civic_barbaric_despoilers
\t}
}

staid_crisis_starbase_pressure = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\thighest_threat > 50
\thas_monthly_income = { resource = alloys value > 80 }
\thas_monthly_income = { resource = energy value > 60 }
\tresource_stockpile_compare = { resource = alloys value > 5000 }
}

staid_aggressive_fleet_pressure = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_basic_economy_runway_safe = yes
\tOR = {
\t\thas_ethic = ethic_militarist
\t\thas_ethic = ethic_fanatic_militarist
\t\thas_ethic = ethic_xenophobe
\t\thas_ethic = ethic_fanatic_xenophobe
\t\thas_valid_civic = civic_barbaric_despoilers
\t\tAND = { is_at_war = yes highest_threat > 35 }
\t}
\tused_naval_capacity_percent < 1.40
}

staid_militarist_conquest_strategy = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_basic_economy_runway_safe = yes
\tOR = {
\t\thas_ethic = ethic_militarist
\t\thas_ethic = ethic_fanatic_militarist
\t\thas_valid_civic = civic_barbaric_despoilers
\t\thas_ethic = ethic_xenophobe
\t\thas_ethic = ethic_fanatic_xenophobe
\t}
\tused_naval_capacity_percent < 1.40
}

staid_influence_claim_pressure = {
\tis_nomadic = no
\tis_at_war = no
\tNOT = { has_ethic = ethic_pacifist }
\tNOT = { has_ethic = ethic_fanatic_pacifist }
\thas_potential_claims = yes
\thas_resource = { type = influence amount > 500 }
\tNOT = { has_ai_expansion_plan = yes }
\thas_bordering_system = no
\tNOT = { staid_boxed_in_war_pressure = yes }
}

staid_boxed_in_claim_urgency = {
\tis_nomadic = no
\tis_at_war = no
\tNOT = { has_ethic = ethic_pacifist }
\tNOT = { has_ethic = ethic_fanatic_pacifist }
\thas_potential_claims = yes
\tstaid_boxed_in_war_pressure = yes
\thas_resource = { type = influence amount > 250 }
}

staid_naval_capacity_expansion_ready = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tstaid_basic_economy_runway_safe = yes
\tused_naval_capacity_percent > 0.90
\tOR = {
\t\tAND = { is_at_war = yes highest_threat > 35 }
\t\trecently_lost_war = yes
\t\thighest_threat > 60
\t}
}

staid_raiding_pop_growth_strategy = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tOR = {
\t\thas_ascension_perk = ap_nihilistic_acquisition
\t\thas_valid_civic = civic_barbaric_despoilers
\t\thas_origin = origin_slavers
\t\thas_origin = origin_khan_successor
\t}
\tused_naval_capacity_percent < 2.00
}

staid_raiding_pop_acquisition_priority = {
\tOR = {
\t\tstaid_raiding_pop_growth_strategy = yes
\t\tAND = {
\t\t\tstaid_opening_military_to_pops = yes
\t\t\tyears_passed < 75
\t\t}
\t}
}

staid_hostile_fauna_safe_clearance_window = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tNOT = { staid_security_existential = yes }
\tstaid_has_safe_basic_stockpiles = yes
\tstaid_fleet_buildup_economy_safe = yes
\tused_naval_capacity_percent < 1.20
\tOR = {
\t\tstaid_opening_hostile_fauna_clearance = yes
\t\tAND = {
\t\t\tyears_passed < 60
\t\t\thas_monthly_income = { resource = alloys value > 60 }
\t\t}
\t}
}

staid_hostile_fauna_clearance_strategy = {
\tstaid_hostile_fauna_safe_clearance_window = yes
}

staid_site_limited_expansion_ready = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tstaid_fleet_buildup_economy_safe = yes
\tOR = {
\t\tstaid_planetary_capacity_growth_ready = yes
\t\tstaid_resource_waste_pressure = yes
\t\tstaid_research_under_curve = yes
\t\tyears_passed > 79
\t}
}

staid_apex_site_preservation_ready = {
\tis_nomadic = no
\tstaid_megastructure_commit_safe = yes
\tOR = {
\t\thas_technology = giga_tech_matrioshka_brain_1
\t\thas_technology = giga_tech_neutronium_gigaforge
\t\thas_technology = giga_tech_nidavellir
\t\tyears_passed > 119
\t}
}

staid_starbase_defense_economy_safe = {
\tis_nomadic = no
\tNOT = { staid_catastrophic_collapse_mode = yes }
\tNOT = { staid_core_deficit_short_runway = yes }
\tOR = {
\t\tNOT = { staid_recovery_mode = yes }
\t\tstaid_security_existential = yes
\t\tstaid_crisis_starbase_pressure = yes
\t\tstaid_homeland_under_attack = yes
\t}
\tOR = {
\t\thas_monthly_income = { resource = alloys value > 35 }
\t\tresource_stockpile_compare = { resource = alloys value > 1200 }
\t\tstaid_high_scale_snowball_pressure = yes
\t}
\tOR = {
\t\thas_monthly_income = { resource = energy value > 35 }
\t\tresource_stockpile_compare = { resource = energy value > 1200 }
\t\tstaid_high_scale_snowball_pressure = yes
\t}
}

staid_static_defense_threat_window = {
\tOR = {
\t\tstaid_crisis_starbase_pressure = yes
\t\tstaid_security_existential = yes
\t\tstaid_homeland_under_attack = yes
\t\tstaid_defensive_starbase_strategy = yes
\t\tAND = {
\t\t\tOR = {
\t\t\t\tstaid_aggressive_fleet_pressure = yes
\t\t\t\tstaid_militarist_conquest_strategy = yes
\t\t\t}
\t\t\tOR = {
\t\t\t\thighest_threat > 25
\t\t\t\tyears_passed > 80
\t\t\t\tstaid_high_scale_snowball_pressure = yes
\t\t\t}
\t\t}
\t}
}

staid_static_defense_investment_ready = {
\tstaid_starbase_defense_economy_safe = yes
\tstaid_static_defense_threat_window = yes
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


OUTPOST_BUDGET_VANILLA_HASHES = {
    "alloys_expenditure_starbases_expand": "bda8dc9d856924f7aade4041b86f9876116255ab53b00c59079f231a4cb7130d",
    "food_expenditure_starbases_expand": "c6f4b69a3e13485d701a177427b523fa0fe76ad0c5cfaef30177539c214a16ca",
}


def active_outpost_budget_parent_overrides() -> list[str]:
    object_ids = tuple(OUTPOST_BUDGET_VANILLA_HASHES)
    patterns = {
        object_id: re.compile(
            rf"(?m)^[ \t]*{re.escape(object_id)}[ \t]*=[ \t]*\{{"
        )
        for object_id in object_ids
    }
    sources: list[str] = []
    for mod in build_active_playset_snapshot()["mods"]:
        if str(mod.get("name", "")).casefold() == "stellar ai director":
            continue
        raw_path = str(mod.get("path", "")).strip()
        if not raw_path:
            continue
        root = Path(raw_path)
        budget_root = root / "common" / "ai_budget"
        if not budget_root.exists():
            continue
        for path in iter_text_files(budget_root):
            text = read_text(path)
            for object_id, pattern in patterns.items():
                if pattern.search(text):
                    sources.append(
                        f"{object_id}:{mod.get('name', '')}:{path}"
                    )
    return sorted(sources)


def outpost_identity_weight_modifiers_text() -> str:
    """Return the shared alloy/food H08 territorial identity modifiers."""

    return (
        "\n\t\t# Bounded H08 territorial identity preferences; native expansion-plan,\n"
        "\t\t# influence, threat, legality, and resource-type gates remain decisive.\n"
        "\t\tmodifier = { factor = 1.25 staid_archetype_gestalt_growth = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes }\n"
        "\t\tmodifier = { factor = 1.15 staid_archetype_defensive = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes }\n"
        "\t\tmodifier = { factor = 1.15 staid_archetype_conquest = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes }\n"
        "\t\tmodifier = { factor = 1.10 staid_archetype_extermination = yes "
        "staid_archetype_identity_conflict = no staid_archetype_eligible_country = yes }\n"
        "\t\tmodifier = {\n"
        "\t\t\tfactor = 1.05\n"
        "\t\t\tstaid_archetype_identity_conflict = no\n"
        "\t\t\tstaid_archetype_eligible_country = yes\n"
        "\t\t\tOR = {\n"
        "\t\t\t\tstaid_archetype_lead_secondary_gestalt_growth = yes\n"
        "\t\t\t\tstaid_archetype_lead_secondary_defensive = yes\n"
        "\t\t\t\tstaid_archetype_lead_secondary_conquest = yes\n"
        "\t\t\t\tstaid_archetype_lead_secondary_extermination = yes\n"
        "\t\t\t}\n"
        "\t\t}\n"
    )


def outpost_budget_text() -> str:
    """Keep native outpost funding eligible beside colonization work."""

    alloy_source = read_text(VANILLA_COMMON_ROOT / "ai_budget" / "00_alloys_budget.txt")
    food_source = read_text(VANILLA_COMMON_ROOT / "ai_budget" / "00_food_budget.txt")
    alloy_outposts = extract_top_level_object_text(
        alloy_source, "alloys_expenditure_starbases_expand"
    )
    food_outposts = extract_top_level_object_text(
        food_source, "food_expenditure_starbases_expand"
    )
    source_blocks = {
        "alloys_expenditure_starbases_expand": alloy_outposts,
        "food_expenditure_starbases_expand": food_outposts,
    }
    for object_id, source_block in source_blocks.items():
        actual_hash = hashlib.sha256(source_block.encode("utf-8")).hexdigest()
        expected_hash = OUTPOST_BUDGET_VANILLA_HASHES[object_id]
        if actual_hash != expected_hash:
            raise ValueError(
                f"Vanilla {object_id} source drifted: {actual_hash} != {expected_hash}"
            )
    active_overrides = active_outpost_budget_parent_overrides()
    if active_overrides:
        raise ValueError(
            "Active playset overrides native outpost budgets; reconstruct the winner: "
            + "; ".join(active_overrides)
        )

    alloy_potential = extract_assignment_block(alloy_outposts, "potential")
    alloy_not = "\t\tNOT = {\n"
    alloy_colonization_veto = "\t\t\tai_colonize_plans > 0\n"
    if alloy_potential.count(alloy_not) != 1 or alloy_potential.count(
        alloy_colonization_veto
    ) != 1:
        raise ValueError(
            "Vanilla alloy outpost potential changed; review before generation"
        )
    alloy_potential = alloy_potential.replace(alloy_not, "\t\tNOR = {\n", 1)
    alloy_potential = alloy_potential.replace(alloy_colonization_veto, "", 1)
    alloy_outposts = replace_top_level_child_block(
        alloy_outposts, "potential", "\tpotential = " + alloy_potential
    )
    food_potential = extract_assignment_block(food_outposts, "potential")
    food_colonization_veto = "\t\t\t\tai_colonize_plans > 0\n"
    if food_potential.count(food_colonization_veto) != 1:
        raise ValueError(
            "Vanilla biological outpost potential changed; review before generation"
        )
    food_potential = food_potential.replace(food_colonization_veto, "", 1)
    food_outposts = replace_top_level_child_block(
        food_outposts, "potential", "\tpotential = " + food_potential
    )
    threat_cutoff = "\t\thighest_threat < 50\n"
    threat_weight_modifier = (
        "\n\t\tmodifier = {\n"
        "\t\t\tfactor = 0.5\n"
        "\t\t\thighest_threat >= 50\n"
        "\t\t}\n"
    )
    identity_weight_modifiers = outpost_identity_weight_modifiers_text()
    softened_outposts = {}
    for object_id, outposts in (
        ("alloys_expenditure_starbases_expand", alloy_outposts),
        ("food_expenditure_starbases_expand", food_outposts),
    ):
        potential = extract_assignment_block(outposts, "potential")
        if potential.count(threat_cutoff) != 1:
            raise ValueError(
                f"{object_id} threat cutoff changed; review before generation"
            )
        potential = potential.replace(threat_cutoff, "", 1)
        outposts = replace_top_level_child_block(
            outposts, "potential", "\tpotential = " + potential
        )
        weight = extract_assignment_block(outposts, "weight")
        if weight.count("\n\t}") != 1:
            raise ValueError(f"{object_id} weight shape changed; review before generation")
        weight = weight.replace(
            "\n\t}",
            threat_weight_modifier + identity_weight_modifiers + "\t}",
            1,
        )
        old_weight_assignment = "\tweight = " + extract_assignment_block(
            outposts, "weight"
        )
        if outposts.count(old_weight_assignment) != 1:
            raise ValueError(f"{object_id} weight assignment is not unique")
        softened_outposts[object_id] = outposts.replace(
            old_weight_assignment, "\tweight = " + weight, 1
        )
    alloy_outposts = softened_outposts["alloys_expenditure_starbases_expand"]
    food_outposts = softened_outposts["food_expenditure_starbases_expand"]
    text = """# Generated by tools/generate_stellar_ai_director_patch.py.
# Pegasus 4.4.4 save-backed outpost availability overrides. Native expansion
# targets, system scores, pathing, influence, biological-ship rules,
# wilderness terraforming exclusion, weights, and desired minima remain.
# A colonization-plan count no longer disables or dampens outpost allocation;
# that count can remain stale after a colony is established. Native colony
# allocation remains separately prioritized. The alloy source's ambiguous
# multi-statement NOT is normalized to the explicit NOR used by the biological
# analogue. Threat now halves the native budget weight instead of making safe
# hole-filling and frontier outposts categorically unavailable.

""" + alloy_outposts.rstrip() + "\n\n" + food_outposts.rstrip() + "\n"
    parse_pdx(
        "\n".join(
            line for line in text.splitlines() if not line.lstrip().startswith("#")
        )
        + "\n"
    )
    return text


def nomad_waystation_budget_text() -> str:
    """Keep native Nomad Waystation funding eligible under bounded threat."""

    specs = (
        (
            "00_influence_budget.txt",
            "influence_expenditure_megastructures_waystations",
            "132b1d9e8bae761973902031616edbb9c7074eea7ba6d0397dbec81b391cbee9",
        ),
        (
            "00_alloys_budget.txt",
            "alloys_expenditure_megastructures_waystations",
            "bc9e54e907687db617a9a3322b0dfd7778a73e3676780e53e0ec35b3523c7e5c",
        ),
        (
            "00_food_budget.txt",
            "food_expenditure_megastructures_waystations",
            "fa72a243f83fc9b727396ca39102e5a23bf6437df0fdfc4a8e4209baaa32aa63",
        ),
    )
    rendered = []
    for file_name, object_id, expected_hash in specs:
        block = extract_top_level_object_text(
            read_text(VANILLA_COMMON_ROOT / "ai_budget" / file_name), object_id
        )
        actual_hash = hashlib.sha256(block.encode("utf-8")).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(
                f"Vanilla {object_id} source drifted: {actual_hash} != {expected_hash}"
            )
        potential = extract_assignment_block(block, "potential")
        threat_cutoff = "\t\thighest_threat < 50\n"
        if potential.count(threat_cutoff) != 1:
            raise ValueError(f"{object_id} threat cutoff changed")
        block = replace_top_level_child_block(
            block,
            "potential",
            "\tpotential = " + potential.replace(threat_cutoff, "", 1),
        )
        weight = extract_assignment_block(block, "weight")
        threat_modifier = (
            "\n\t\tmodifier = {\n"
            "\t\t\tfactor = 0.5\n"
            "\t\t\thighest_threat >= 50\n"
            "\t\t}\n"
        )
        if weight.count("\n\t}") != 1:
            raise ValueError(f"{object_id} weight shape changed")
        adjusted_weight = weight.replace("\n\t}", threat_modifier + "\t}", 1)
        old_assignment = "\tweight = " + weight
        if block.count(old_assignment) != 1:
            raise ValueError(f"{object_id} weight assignment is not unique")
        rendered.append(
            block.replace(old_assignment, "\tweight = " + adjusted_weight, 1)
        )
    text = (
        "# Generated by tools/generate_stellar_ai_nomad_waystation_budgets.py.\n"
        "# Pegasus 4.4.4 full-object Nomad Waystation budget overrides.\n"
        "# Threat halves funding weight instead of disabling Waystations; native\n"
        "# technology, resource-model, cost, and starbase-capacity controls remain.\n\n"
        + "\n\n".join(block.rstrip() for block in rendered)
        + "\n"
    )
    parse_pdx(text)
    return text


def render_core_ai_artifacts(
    rows: list[dict[str, Any]] | None = None,
) -> dict[Path, str]:
    """Render and parse the fixed core AI artifacts without writing files."""

    source_rows = extract_megastructure_rows() if rows is None else rows
    thresholds = generated_thresholds(source_rows)
    artifacts = {
        DECISION_STATE_TRIGGER_PATH: normalize_text_file_content(
            triggers_text(thresholds)
        ),
        OUTPOST_BUDGET_PATH: normalize_text_file_content(outpost_budget_text()),
    }
    if tuple(artifacts) != CORE_AI_ARTIFACT_PATHS:
        raise ValueError("Core AI artifact renderer violated its fixed output allowlist")
    for text in artifacts.values():
        parse_pdx(text)
    return artifacts


def fleet_archetype_budget_modifier(archetype: str, factor: float) -> str:
    """Render one ordinary-peacetime fleet identity tie-breaker."""

    if archetype not in FLEET_ARCHETYPE_FACTORS:
        raise ValueError(f"Unsupported fleet archetype: {archetype}")
    if not 1.0 < factor <= 1.15:
        raise ValueError(
            f"Fleet archetype factor must be in (1.0, 1.15]: "
            f"{archetype}={factor}"
        )
    return f"""\t\t# Bounded H08c identity bias for ordinary peacetime underfill only.
\t\tmodifier = {{
\t\t\tfactor = {factor}
\t\t\tstaid_archetype_hard_{archetype} = yes
\t\t\tstaid_archetype_identity_conflict = no
\t\t\tstaid_archetype_eligible_country = yes
\t\t\tused_naval_capacity_percent < 0.80
\t\t\tis_at_war = no
\t\t\tNOT = {{ recently_lost_war = yes }}
\t\t\tstaid_catastrophic_collapse_mode = no
\t\t\tstaid_core_deficit_short_runway = no
\t\t\tNOR = {{
\t\t\t\tany_neighbor_country = {{
\t\t\t\t\thas_ascension_perk = ap_become_the_crisis
\t\t\t\t}}
\t\t\t\tany_country = {{
\t\t\t\t\tis_crisis_faction = yes
\t\t\t\t}}
\t\t\t}}
\t\t}}"""


def fleet_threat_response_budget_modifier() -> str:
    """Render one bounded, stateless peacetime threat-response nudge."""

    return f"""\t\t# Bounded H09b arms-race nudge for threatened peacetime underfill.
\t\tmodifier = {{
\t\t\tfactor = {FLEET_THREAT_RESPONSE_FACTOR:.2f}
\t\t\thighest_threat > 50
\t\t\tused_naval_capacity_percent < 0.80
\t\t\tis_at_war = no
\t\t\tNOT = {{ recently_lost_war = yes }}
\t\t\tstaid_catastrophic_collapse_mode = no
\t\t\tstaid_core_deficit_short_runway = no
\t\t\tNOR = {{
\t\t\t\tany_neighbor_country = {{
\t\t\t\t\thas_ascension_perk = ap_become_the_crisis
\t\t\t\t}}
\t\t\t\tany_country = {{
\t\t\t\t\tis_crisis_faction = yes
\t\t\t\t}}
\t\t\t}}
\t\t}}"""


def fleet_alloy_budget_text(
    *,
    archetype_overlay: bool = True,
    archetype_factors: Mapping[str, float] | None = None,
) -> str:
    source_path = VANILLA_COMMON_ROOT / "ai_budget" / "00_alloys_budget.txt"
    source_text = read_text(source_path)
    ships = extract_top_level_object_text(source_text, "alloys_expenditure_ships")
    upgrades = extract_top_level_object_text(source_text, "alloys_expenditure_ship_upgrades")
    ships = replace_top_level_child_block(
        ships,
        "potential",
        """\tpotential = {
\t\t# This category also funds civilian science ships. Keep the native lane
\t\t# available; affordability and competing budget shares govern execution.
\t\talways = yes
\t}""",
    )
    ships = insert_top_level_child_modifier(
        ships,
        "weight",
        """\t\t# Pegasus 4.4.4 high-capacity declaration workaround. Reduce, but do
\t\t# not eliminate, the ship lane so weak absolute fleets can still recover.
\t\tmodifier = {
\t\t\tfactor = 0.25
\t\t\tstaid_peacetime_high_naval_capacity_guard = yes
\t\t}""",
        )
    ships = insert_top_level_child_modifier(
        ships,
        "weight",
        """\t\t# Bounded wartime surge for satisfied templates far below naval cap.
\t\t# The vanilla 3x war factor remains; this only adds affordable lane share.
\t\tmodifier = {
\t\t\tfactor = 1.5
\t\t\tstaid_wartime_fleet_surge_ready = yes
\t\t}""",
    )
    ships = insert_top_level_child_modifier(
        ships,
        "desired_min",
        """\t\t# Reserve enough partitioned alloys for at least one current capital-hull
\t\t# decision. This cannot create a fleet template or bypass construction.
\t\tmodifier = {
\t\t\tadd = 5000
\t\t\tstaid_wartime_fleet_surge_ready = yes
\t\t}""",
    )
    if archetype_overlay:
        ships = insert_top_level_child_modifier(
            ships,
            "weight",
            fleet_threat_response_budget_modifier(),
        )
        factors = (
            FLEET_ARCHETYPE_FACTORS
            if archetype_factors is None
            else archetype_factors
        )
        for archetype, factor in factors.items():
            ships = insert_top_level_child_modifier(
                ships,
                "weight",
                fleet_archetype_budget_modifier(archetype, factor),
            )
    upgrades = replace_top_level_child_block(
        upgrades,
        "potential",
        """\tpotential = {
\t\tis_at_war = no
\t\tany_owned_fleet = {
\t\t\tcontroller = { is_same_value = root }
\t\t\tcan_be_upgraded = yes
\t\t}
\t}""",
    )
    overlay_note = (
        """
# Threat response and identity tie-breakers apply only during ordinary
# peacetime underfill and never during war, recent-loss, crisis, collapse, or
# short-runway states."""
        if archetype_overlay
        else ""
    )
    text = f"""# Pegasus 4.4.4 full-object overrides for alloy-funded ship construction and upgrades.
# The vanilla weights and war/crisis multipliers remain. At 80% used naval
# capacity, peacetime construction receives a bounded share reduction instead
# of becoming ineligible. This retains a cautious 4.4.4 workaround while weak
# absolute fleets and civilian science-ship demand can still recover.{overlay_note}

""" + ships.rstrip() + "\n\n" + upgrades.rstrip() + "\n"
    parse_pdx("\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#")) + "\n")
    return text


def ai_budget_text(
    thresholds: dict[str, int], *, archetype_overlay: bool = True
) -> str:
    text = '''# Generated by tools/generate_stellar_ai_director_patch.py.
# The generic alloys_expenditure_megastructures object deliberately remains
# upstream/parent-owned. Director route weights may rank legal projects, but a
# global reserve must not crowd out outposts, ships, or other alloy lanes.
'''
    return text.rstrip() + "\n\n" + fleet_alloy_budget_text(
        archetype_overlay=archetype_overlay
    )


def render_archetype_consumer_artifacts(
    *, archetype_overlay: bool = True
) -> dict[Path, str]:
    """Render the two fixed H08c consumer artifacts without writing files."""

    rows = route_override_target_rows()
    technology_rows = [
        row for row in rows if row["object_type"] == "technology"
    ]
    expected_count = sum(
        target["object_type"] == "technology"
        for target in ROUTE_OVERRIDE_TARGETS
    )
    if len(technology_rows) != expected_count:
        raise ValueError(
            "Technology route row count drifted: "
            f"expected={expected_count}, actual={len(technology_rows)}"
        )
    generated_paths = {
        Path(str(row["generated_file"])).resolve()
        for row in technology_rows
    }
    if generated_paths != {TECHNOLOGY_ROUTE_OVERRIDE_PATH.resolve()}:
        raise ValueError(
            "Technology route rows violated the fixed H08c destination: "
            f"{sorted(str(path) for path in generated_paths)}"
        )
    strategy_rows = [
        row
        for row in rows
        if row["object_type"]
        in {"ascension_perk", "tradition_category", "tradition"}
    ]
    strategy_rows_by_path: dict[Path, list[dict[str, Any]]] = defaultdict(list)
    for row in strategy_rows:
        strategy_rows_by_path[Path(str(row["generated_file"])).resolve()].append(row)
    if set(strategy_rows_by_path) != {
        path.resolve() for path in IDENTITY_STRATEGY_ROUTE_OVERRIDE_PATHS
    }:
        raise ValueError("Identity strategy rows violated the fixed output allowlist")
    claim_rows = [row for row in rows if row["object_type"] == "ai_budget"]
    if {Path(str(row["generated_file"])).resolve() for row in claim_rows} != {
        IDENTITY_CLAIM_BUDGET_PATH.resolve()
    }:
        raise ValueError("Identity claim rows violated the fixed output allowlist")
    defense_rows = [
        row
        for row in rows
        if row["object_type"] in {"starbase_building", "starbase_module"}
    ]
    defense_rows_by_path: dict[Path, list[dict[str, Any]]] = defaultdict(list)
    for row in defense_rows:
        defense_rows_by_path[Path(str(row["generated_file"])).resolve()].append(row)
    if set(defense_rows_by_path) != {
        path.resolve() for path in IDENTITY_STATIC_DEFENSE_PATHS
    }:
        raise ValueError("Identity static-defense rows violated the fixed output allowlist")
    megastructure_rows = [
        row for row in rows if row["object_type"] == "megastructure"
    ]
    if {Path(str(row["generated_file"])).resolve() for row in megastructure_rows} != {
        IDENTITY_MEGASTRUCTURE_PATH.resolve()
    }:
        raise ValueError("Identity megastructure rows violated the fixed output allowlist")
    artifacts = {
        FLEET_ALLOY_BUDGET_PATH: normalize_text_file_content(
            ai_budget_text({}, archetype_overlay=archetype_overlay)
        ),
        TECHNOLOGY_ROUTE_OVERRIDE_PATH: route_override_file_text(
            technology_rows,
            archetype_overlay=archetype_overlay,
        ),
    }
    for path in IDENTITY_STRATEGY_ROUTE_OVERRIDE_PATHS:
        artifacts[path] = route_override_file_text(
            strategy_rows_by_path[path.resolve()],
            archetype_overlay=archetype_overlay,
        )
    artifacts[IDENTITY_CLAIM_BUDGET_PATH] = route_override_file_text(
        claim_rows,
        archetype_overlay=archetype_overlay,
    )
    for path in IDENTITY_STATIC_DEFENSE_PATHS:
        artifacts[path] = route_override_file_text(
            defense_rows_by_path[path.resolve()],
            archetype_overlay=archetype_overlay,
        )
    artifacts[IDENTITY_MEGASTRUCTURE_PATH] = route_override_file_text(
        megastructure_rows,
        collect_object_names(),
        archetype_overlay=archetype_overlay,
    )
    if tuple(artifacts) != ARCHETYPE_OVERLAY_ARTIFACT_PATHS:
        raise ValueError(
            "Archetype consumer renderer violated its fixed output allowlist"
        )
    for text in artifacts.values():
        parse_pdx(text)
    return artifacts


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


def opening_leader_recruitment_budget_text() -> str:
    return '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Provenance: common/ai_budget/00_unity_budget.txt.
# Science ships are useless without scientists. Keep the opening leader budget
# competitive while the native leader-assignment planner fills empty locations.

unity_expenditure_leaders = {
	resource = unity
	type = expenditure
	category = leaders

	potential = {
		always = yes
	}

	weight = {
		weight = 0.4
		modifier = {
			factor = 5
			years_passed < 20
		}
	}

	desired_max = {
		base = 1000
	}
}
'''


def medical_center_churn_fix_text() -> str:
    source_path = VANILLA_COMMON_ROOT / "buildings" / "07_amenity_buildings.txt"
    source_text = read_text(source_path)
    block = extract_top_level_object_text(source_text, "building_medical_2")
    block = replace_top_level_child_block(
        block,
        "destroy_trigger",
        '''\tdestroy_trigger = {
\t\texists = owner
\t\t# Vanilla lets Gene Clinics upgrade into this building, then destroys the
\t\t# result on stable ordinary AI worlds. Preserve a completed upgrade so the
\t\t# AI cannot pay to rebuild the same medical chain indefinitely.
\t\towner = { is_regular_empire = no }
\t}''',
    )
    definitions = source_file_variable_definitions(source_text)
    used = sorted(used_at_variables_in_text(block))
    local_definitions = "\n".join(definitions[name] for name in used if name in definitions)
    return (
        "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
        "# Full-object vanilla 4.4.4 override fixing the Medical Center upgrade/destroy loop.\n"
        f"# Source: {source_path.as_posix()}\n\n"
        + (local_definitions + "\n\n" if local_definitions else "")
        + block.rstrip()
        + "\n"
    )


def _repair_band_window_lines(
    metric: str,
    lower: int | None,
    upper: int | None,
    indent: str = "\t\t\t",
) -> list[str]:
    lines: list[str] = []
    if lower is not None:
        lines.append(f"{indent}{metric} >= {lower}")
    if upper is not None:
        lines.append(f"{indent}{metric} < {upper}")
    return lines


def _relative_repair_subplan_text(
    *,
    name: str,
    gate_lines: Iterable[str],
    metric: str,
    lower: int | None,
    upper: int | None,
    resource: str,
    income_target: int,
) -> str:
    band_label = f"{lower or 0}-{upper - 1}" if upper is not None else f"{lower}+"
    lines = [
        "\tsubplan = {",
        "\t\tscaling = yes",
        f'\t\tset_name = "Stellar AI Director {name} {band_label}"',
        "\t\tpotential = {",
    ]
    lines.extend(f"\t\t\t{line}" for line in gate_lines)
    lines.extend(_repair_band_window_lines(metric, lower, upper))
    lines.extend(
        [
            "\t\t}",
            "\t\tincome = {",
            f"\t\t\t{resource} = {income_target}",
            "\t\t}",
            "\t}",
        ]
    )
    return "\n".join(lines)


def relative_economic_repair_subplans_text() -> str:
    """Generate income-led repair pressure that market purchases cannot satisfy."""
    blocks = [
        "\t# Relative repair plans require both earned monthly income and an operating",
        "\t# float. Buying stockpile on the market cannot clear an unsafe income gate.",
    ]
    colony_specs = (
        ("energy income repair", "staid_energy_runway_safe", "energy", RELATIVE_COLONY_RESOURCE_TARGETS["energy"]["income"]),
        (
            "mineral income repair",
            "staid_mineral_runway_safe",
            "minerals",
            RELATIVE_COLONY_RESOURCE_TARGETS["minerals"]["income"],
        ),
        (
            "consumer goods income repair",
            "staid_consumer_goods_runway_safe",
            "consumer_goods",
            RELATIVE_COLONY_RESOURCE_TARGETS["consumer_goods"]["income"],
        ),
        (
            "colony alloy income repair",
            "staid_alloy_colony_runway_safe",
            "alloys",
            RELATIVE_COLONY_RESOURCE_TARGETS["alloys"]["income"],
        ),
        (
            "food operating-float repair",
            "staid_food_colony_runway_safe",
            "food",
            (25, 50, 100, 200, 400),
        ),
    )
    for name, gate, resource, targets in colony_specs:
        for index, (lower, upper) in enumerate(RELATIVE_SCALE_BANDS):
            gate_lines = [f"NOT = {{ {gate} = yes }}"]
            if resource == "consumer_goods":
                gate_lines.insert(0, "country_uses_consumer_goods = yes")
            elif resource == "food":
                gate_lines.insert(0, "country_uses_food = yes")
            blocks.append(
                _relative_repair_subplan_text(
                    name=name,
                    gate_lines=gate_lines,
                    metric="num_owned_planets",
                    lower=lower,
                    upper=upper,
                    resource=resource,
                    income_target=int(targets[index]),
                )
            )

    for lower, upper, target in RELATIVE_ALLOY_FLEET_TARGETS["income"]:
        blocks.append(
            _relative_repair_subplan_text(
                name="fleet replacement alloy repair",
                gate_lines=(
                    "country_uses_bio_ships = no",
                    "OR = {",
                    "\tNOT = { staid_scaled_alloy_fleet_income_safe = yes }",
                    "\tNOT = { staid_scaled_alloy_fleet_stockpile_safe = yes }",
                    "}",
                ),
                metric="fleet_power",
                lower=lower,
                upper=upper,
                resource="alloys",
                income_target=target,
            )
        )

    for lower, upper, target in RELATIVE_BIOSHIP_FOOD_FLEET_TARGETS["income"]:
        blocks.append(
            _relative_repair_subplan_text(
                name="bio-ship replacement food repair",
                gate_lines=(
                    "country_uses_food = yes",
                    "country_uses_bio_ships = yes",
                    "OR = {",
                    "\tNOT = { staid_scaled_bioship_food_fleet_income_safe = yes }",
                    "\tNOT = { staid_scaled_bioship_food_fleet_stockpile_safe = yes }",
                    "}",
                ),
                metric="fleet_power",
                lower=lower,
                upper=upper,
                resource="food",
                income_target=target,
            )
        )
    return "\n\n".join(blocks)


_ARCHETYPE_ECONOMIC_TARGETS = {
    "extermination": {
        "alloys": 900,
        "energy": 600,
        "minerals": 400,
        "physics_research": 600,
        "society_research": 600,
        "engineering_research": 900,
    },
    "gestalt_growth": {
        "minerals": 600,
        "energy": 500,
        "alloys": 250,
        "physics_research": 600,
        "society_research": 600,
        "engineering_research": 900,
    },
    "defensive": {
        "alloys": 500,
        "energy": 400,
        "minerals": 350,
        "physics_research": 600,
        "society_research": 600,
        "engineering_research": 900,
    },
    "research": {
        "physics_research": 1500,
        "society_research": 1500,
        "engineering_research": 2500,
        "energy": 350,
    },
    "diplomatic": {
        "trade": 300,
        "physics_research": 600,
        "society_research": 600,
        "engineering_research": 900,
        "energy": 250,
    },
}

_ARCHETYPE_SECONDARY_ECONOMIC_TARGETS = {
    "extermination": {
        "alloys": 450,
        "energy": 300,
        "minerals": 250,
        "physics_research": 500,
        "society_research": 500,
        "engineering_research": 750,
    },
    "conquest": {"alloys": 350, "energy": 250, "minerals": 180},
    "gestalt_growth": {"minerals": 350, "energy": 300, "alloys": 180},
    "defensive": {"alloys": 300, "energy": 250, "minerals": 220},
    "research": {
        "physics_research": 800,
        "society_research": 800,
        "engineering_research": 1200,
        "energy": 220,
    },
    "diplomatic": {
        "trade": 200,
        "energy": 180,
        "physics_research": 500,
        "society_research": 500,
        "engineering_research": 750,
    },
}

_DEFINING_IDENTITY_ECONOMIC_TARGETS = {
    "machine exterminator": (
        "staid_identity_machine_exterminator",
        {
            "alloys": 900,
            "energy": 600,
            "minerals": 400,
            "unity": 150,
            "physics_research": 600,
            "society_research": 600,
            "engineering_research": 900,
        },
        (),
    ),
    "rogue servitor": (
        "staid_identity_rogue_servitor",
        {
            "food": 120,
            "consumer_goods": 220,
            "energy": 500,
            "minerals": 350,
            "alloys": 300,
            "unity": 250,
            "physics_research": 600,
            "society_research": 600,
            "engineering_research": 900,
        },
        ("country_uses_food = yes", "country_uses_consumer_goods = yes"),
    ),
    "assimilator": (
        "staid_identity_assimilator",
        {
            "energy": 550,
            "minerals": 450,
            "alloys": 550,
            "unity": 150,
            "physics_research": 600,
            "society_research": 600,
            "engineering_research": 900,
        },
        (),
    ),
    "devouring swarm": (
        "staid_identity_devouring_swarm",
        {
            "alloys": 800,
            "energy": 500,
            "minerals": 400,
            "unity": 150,
            "physics_research": 500,
            "society_research": 500,
            "engineering_research": 750,
        },
        (),
    ),
    "inward perfection": (
        "staid_identity_inward_perfection",
        {
            "energy": 400,
            "minerals": 450,
            "alloys": 350,
            "consumer_goods": 220,
            "unity": 250,
            "physics_research": 800,
            "society_research": 800,
            "engineering_research": 1200,
        },
        ("country_uses_consumer_goods = yes",),
    ),
    "megacorp": (
        "staid_identity_megacorp",
        {
            "trade": 400,
            "energy": 350,
            "consumer_goods": 250,
            "minerals": 300,
            "unity": 200,
            "physics_research": 600,
            "society_research": 600,
            "engineering_research": 900,
        },
        ("country_uses_consumer_goods = yes",),
    ),
}


def archetype_economic_subplans_text() -> str:
    """Render bounded identity preferences below relative recovery plans."""

    research_resources = {
        "physics_research",
        "society_research",
        "engineering_research",
    }
    blocks: list[str] = []
    for role, plan_targets in (
        ("primary", _ARCHETYPE_ECONOMIC_TARGETS),
        ("lead secondary", _ARCHETYPE_SECONDARY_ECONOMIC_TARGETS),
    ):
        trigger_prefix = (
            "staid_archetype_"
            if role == "primary"
            else "staid_archetype_lead_secondary_"
        )
        for archetype, targets in plan_targets.items():
            gates = [
                "staid_basic_economy_runway_safe = yes",
                "NOT = { staid_core_deficit_short_runway = yes }",
                "NOT = { staid_catastrophic_collapse_mode = yes }",
                "NOR = {",
                "\tstaid_identity_machine_exterminator = yes",
                "\tstaid_identity_rogue_servitor = yes",
                "\tstaid_identity_assimilator = yes",
                "\tstaid_identity_devouring_swarm = yes",
                "\tstaid_identity_inward_perfection = yes",
                "\tstaid_identity_barbaric_despoiler = yes",
                "\tstaid_identity_megacorp = yes",
                "}",
                f"{trigger_prefix}{archetype} = yes",
            ]
            if research_resources & targets.keys():
                gates.append("staid_research_construction_priority_ready = yes")
            target_lines = [
                f"\t\t\t{resource} = {value}"
                for resource, value in targets.items()
            ]
            blocks.append(
                "\n".join(
                    (
                        "\tsubplan = {",
                        "\t\toptional = yes",
                        f'\t\tset_name = "Stellar AI Director {role} {archetype} economy"',
                        "\t\tpotential = {",
                        *(f"\t\t\t{gate}" for gate in gates),
                        "\t\t}",
                        "\t\tincome = {",
                        *target_lines,
                        "\t\t}",
                        "\t}",
                    )
                )
            )
    for label, (trigger, targets, resource_gates) in (
        _DEFINING_IDENTITY_ECONOMIC_TARGETS.items()
    ):
        gates = [
            "staid_basic_economy_runway_safe = yes",
            "NOT = { staid_core_deficit_short_runway = yes }",
            "NOT = { staid_catastrophic_collapse_mode = yes }",
            f"{trigger} = yes",
            *resource_gates,
            "staid_research_construction_priority_ready = yes",
        ]
        blocks.append(
            "\n".join(
                (
                    "\tsubplan = {",
                    "\t\toptional = yes",
                    f'\t\tset_name = "Stellar AI Director defining {label} economy"',
                    "\t\tpotential = {",
                    *(f"\t\t\t{gate}" for gate in gates),
                    "\t\t}",
                    "\t\tincome = {",
                    *(f"\t\t\t{resource} = {value}" for resource, value in targets.items()),
                    "\t\t}",
                    "\t}",
                )
            )
        )
    blocks.append(
        """\tsubplan = {
\t\toptional = yes
\t\tset_name = "Stellar AI Director defining nomadic economy"
\t\tpotential = {
\t\t\tstaid_identity_nomadic = yes
\t\t\tNOT = { staid_catastrophic_collapse_mode = yes }
\t\t\tstaid_research_input_runway_safe = yes
\t\t}
\t\tincome = {
\t\t\talloys = 400
\t\t\tfood = 150
\t\t\tenergy = 350
\t\t\tminerals = 250
\t\t\tunity = 250
\t\t\tphysics_research = 500
\t\t\tsociety_research = 500
\t\t\tengineering_research = 750
\t\t}
\t}"""
    )
    return "\n\n".join(blocks)


def economic_plan_text() -> str:
    return '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Full-object override: intentionally replaces `basic_economy_plan` with a
# mod-set-specific high-scale survival plan. This is not a compatibility shim:
# the Director assumes Gigas/NSC3/ESC crisis scaling and forces research,
# alloy, trade, naval-cap, habitat/tall, and megastructure pressure early.

basic_economy_plan = {
\tai_weight = { weight = 5000 }

\tincome = {
\t\talloys = 120
\t\tconsumer_goods = 150
\t\tfood = 10
\t\tenergy = 150
\t\tminerals = 150
\t\tunity = 120
\t\ttrade = 75
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director safe research baseline"
\t\tpotential = {
\t\t\tstaid_research_construction_priority_ready = yes
\t\t}
\t\tincome = {
\t\t\tphysics_research = 400
\t\t\tsociety_research = 400
\t\t\tengineering_research = 600
\t\t}
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director opening direct research route"
\t\tpotential = {
\t\t\tstaid_research_construction_priority_ready = yes
\t\t\tstaid_opening_direct_research = yes
\t\t}
\t\tincome = {
\t\t\tphysics_research = 450
\t\t\tsociety_research = 450
\t\t\tengineering_research = 650
\t\t\tconsumer_goods = 180
\t\t\tenergy = 180
\t\t}
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director opening trade to research route"
\t\tpotential = {
\t\t\tstaid_research_construction_priority_ready = yes
\t\t\tstaid_opening_trade_to_research = yes
\t\t}
\t\tincome = {
\t\t\ttrade = 300
\t\t\tconsumer_goods = 180
\t\t\tphysics_research = 300
\t\t\tsociety_research = 300
\t\t\tengineering_research = 450
\t\t}
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director opening growth to research route"
\t\tpotential = {
\t\t\tstaid_research_construction_priority_ready = yes
\t\t\tOR = {
\t\t\t\tstaid_opening_hive_growth_research = yes
\t\t\t\tstaid_opening_machine_growth_research = yes
\t\t\t\tstaid_opening_military_to_pops = yes
\t\t\t\tstaid_opening_nomad_arkship_research = yes
\t\t\t}
\t\t}
\t\tincome = {
\t\t\talloys = 180
\t\t\tminerals = 260
\t\t\tenergy = 220
\t\t\tphysics_research = 250
\t\t\tsociety_research = 250
\t\t\tengineering_research = 400
\t\t}
\t}

__STAID_RELATIVE_ECONOMIC_REPAIR_SUBPLANS__

__STAID_ARCHETYPE_ECONOMIC_SUBPLANS__

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director construction spenddown reserve"
\t\tpotential = {
\t\t\tstaid_construction_spenddown_pressure = yes
\t\t\tstaid_basic_economy_runway_safe = yes
\t\t}
\t\tincome = {
\t\t\tminerals = 30000
\t\t\tenergy = 18000
\t\t\tconsumer_goods = 6000
\t\t\talloys = 8000
\t\t\tfood = 2000
\t\t\tunity = 5000
\t\t\ttrade = 3000
\t\t}
\t\tpops = 1000000
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director unemployed pop construction catch-up"
\t\tpotential = {
\t\t\tstaid_unemployment_construction_pressure = yes
\t\t}
\t\tincome = {
\t\t\tminerals = 12000
\t\t\tenergy = 8000
\t\t\tconsumer_goods = 2500
\t\t\talloys = 3000
\t\t\tfood = 1200
\t\t\tunity = 2000
\t\t\ttrade = 1200
\t\t}
\t\tpops = 1000000
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director open slot construction catch-up"
\t\tpotential = {
\t\t\tany_owned_planet = {
\t\t\t\tfree_building_slots > 0
\t\t\t\tnum_unemployed > 0
\t\t\t}
\t\t}
\t\tincome = {
\t\t\tminerals = 16000
\t\t\tenergy = 10000
\t\t\tconsumer_goods = 3000
\t\t\talloys = 4000
\t\t\tunity = 2500
\t\t\ttrade = 1500
\t\t}
\t\tpops = 1000000
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director rich empire spend-down construction"
\t\tpotential = {
\t\t\tresource_stockpile_compare = { resource = minerals value > 10000 }
\t\t\tany_owned_planet = {
\t\t\t\tOR = {
\t\t\t\t\tnum_unemployed > 0
\t\t\t\t\tfree_building_slots > 0
\t\t\t\t}
\t\t\t}
\t\t}
\t\tincome = {
\t\t\tminerals = 25000
\t\t\tenergy = 16000
\t\t\tconsumer_goods = 5000
\t\t\talloys = 7000
\t\t\tunity = 4000
\t\t\ttrade = 2500
\t\t}
\t\tpops = 1000000
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director habitat and terraforming expansion reserve"
\t\tpotential = {
\t\t\tOR = {
\t\t\t\tstaid_planetary_capacity_growth_ready = yes
\t\t\t\tstaid_high_scale_snowball_pressure = yes
\t\t\t}
\t\t}
\t\tincome = {
\t\t\tminerals = 5000
\t\t\tenergy = 5000
\t\t\tconsumer_goods = 1200
\t\t\tfood = 800
\t\t\tunity = 1000
\t\t\ttrade = 800
\t\t}
\t\tpops = 1000000
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
\t\t\tNOT = { staid_catastrophic_collapse_mode = yes }
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
\t\toptional = yes
\t\tset_name = "Stellar AI Director militarist conquest fleet reserve"
\t\tpotential = {
\t\t\tstaid_archetype_conquest = yes
\t\t\tstaid_basic_economy_runway_safe = yes
\t\t\tNOT = { staid_core_deficit_short_runway = yes }
\t\t\tNOT = { staid_catastrophic_collapse_mode = yes }
\t\t\tstaid_research_construction_priority_ready = yes
\t\t}
\t\tincome = {
\t\t\talloys = 600
\t\t\tenergy = 350
\t\t\tminerals = 250
\t\t\tunity = 100
\t\t\ttrade = 80
\t\t\tphysics_research = 200
\t\t\tsociety_research = 200
\t\t\tengineering_research = 310
\t\t}
\t}

\tsubplan = {
\t\toptional = yes
\t\tset_name = "Stellar AI Director raiding pop acquisition reserve"
\t\tpotential = {
\t\t\tstaid_identity_barbaric_despoiler = yes
\t\t\tstaid_archetype_conquest = yes
\t\t\tstaid_basic_economy_runway_safe = yes
\t\t\tNOT = { staid_core_deficit_short_runway = yes }
\t\t\tNOT = { staid_catastrophic_collapse_mode = yes }
\t\t\tstaid_research_construction_priority_ready = yes
\t\t}
\t\tincome = {
\t\t\talloys = 650
\t\t\tenergy = 450
\t\t\tminerals = 300
\t\t\tunity = 150
\t\t\tphysics_research = 400
\t\t\tsociety_research = 400
\t\t\tengineering_research = 600
\t\t}
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director hostile fauna clearance reserve"
\t\tpotential = {
\t\t\tstaid_hostile_fauna_clearance_strategy = yes
\t\t}
\t\tincome = {
\t\t\talloys = 220
\t\t\tenergy = 160
\t\t\tminerals = 90
\t\t}
\t\tnaval_cap = 250
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director modded unlock research reserve"
\t\tpotential = {
\t\t\tstaid_research_input_runway_safe = yes
\t\t\tstaid_core_unlock_research_priority_ready = yes
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
\t\tset_name = "Stellar AI Director ESC component resource readiness"
\t\tpotential = {
\t\t\tstaid_research_input_runway_safe = yes
\t\t\tNOT = { staid_catastrophic_collapse_mode = yes }
\t\t\tNOT = { staid_advanced_component_resource_support_ready = yes }
\t\t\tOR = {
\t\t\t\thas_technology = tech_dark_matter_power_core
\t\t\t\thas_technology = esc_tech_dark_matter_power_core_2
\t\t\t\tstaid_phase_fleet_conversion_repeatables = yes
\t\t\t}
\t\t}
\t\tincome = {
\t\t\tsr_dark_matter = 3
\t\t\tsr_zro = 3
\t\t\tnanites = 3
\t\t\tengineering_research = 600
\t\t\tenergy = 500
\t\t\tminerals = 400
\t\t\ttrade = 150
\t\t}
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director capped stockpile research conversion"
\t\tpotential = {
\t\t\tstaid_research_input_runway_safe = yes
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
\t\t\tstaid_research_input_runway_safe = yes
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
\t\t\tstaid_research_input_runway_safe = yes
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
\t\t\tstaid_research_input_runway_safe = yes
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
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director NSC3 hull readiness reserve"
\t\tpotential = {
\t\t\tstaid_research_input_runway_safe = yes
\t\t\tNOT = { staid_catastrophic_collapse_mode = yes }
\t\t\tOR = {
\t\t\t\tstaid_nsc3_capital_hull_unlock_ready = yes
\t\t\t\thas_technology = tech_battleships
\t\t\t\thas_technology = tech_Carrier_1
\t\t\t\thas_technology = tech_Dreadnought_1
\t\t\t}
\t\t}
\t\tincome = {
\t\t\talloys = 900
\t\t\tenergy = 650
\t\t\tminerals = 450
\t\t\tengineering_research = 900
\t\t\tphysics_research = 450
\t\t\ttrade = 250
\t\t}
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
\t\t\tconsumer_goods = 250
\t\t\tfood = 150
\t\t\ttrade = 150
\t\t}
\t\tpops = 400000
\t}

\tsubplan = {
\t\toptional = yes
\t\tscaling = yes
\t\tset_name = "Stellar AI Director Planetary Diversity outpost reserve"
\t\tpotential = {
\t\t\tstaid_planetary_diversity_outpost_investment_ready = yes
\t\t\tstaid_research_construction_priority_ready = yes
\t\t}
\t\tincome = {
\t\t\tminerals = 800
\t\t\tenergy = 500
\t\t\tconsumer_goods = 250
\t\t\tphysics_research = 400
\t\t\tsociety_research = 400
\t\t\tengineering_research = 600
\t\t\ttrade = 150
\t\t}
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director defensive starbase reserve"
\t\tpotential = {
\t\t\tstaid_static_defense_investment_ready = yes
\t\t}
\t\tincome = {
\t\t\talloys = 2200
\t\t\tenergy = 1400
\t\t\tminerals = 1200
\t\t\ttrade = 500
\t\t}
\t}

\tsubplan = {
\t\tscaling = yes
\t\tset_name = "Stellar AI Director crisis starbase reserve"
\t\tpotential = {
\t\t\tstaid_starbase_defense_economy_safe = yes
\t\t\tstaid_crisis_starbase_pressure = yes
\t\t}
\t\tincome = {
\t\t\talloys = 3500
\t\t\tenergy = 2200
\t\t\tminerals = 1800
\t\t\ttrade = 800
\t\t}
\t}
}
'''.replace(
        "__STAID_RELATIVE_ECONOMIC_REPAIR_SUBPLANS__",
        relative_economic_repair_subplans_text(),
    ).replace(
        "__STAID_ARCHETYPE_ECONOMIC_SUBPLANS__",
        archetype_economic_subplans_text(),
    )


def _economic_subplan_block(plan_text: str, set_name: str) -> str:
    marker = f'set_name = "{set_name}"'
    if plan_text.count(marker) != 1:
        return ""
    marker_index = plan_text.index(marker)
    block_start = plan_text.rfind("\n\tsubplan = {", 0, marker_index)
    if block_start < 0:
        return ""
    block_start += 1
    block_end = plan_text.find("\n\tsubplan = {", marker_index)
    if block_end < 0:
        block_end = plan_text.find("\n}", marker_index)
    if block_end < 0:
        return ""
    return plan_text[block_start:block_end].rstrip()


def _strategic_resource_deficit_recovery_subplan_text(resource: str, label: str) -> str:
    return f'''\tsubplan = {{
\t\toptional = yes
\t\tset_name = "Stellar AI Director actual-deficit recovery - {label}"
\t\tpotential = {{ has_deficit = {resource} }}
\t\tincome = {{ {resource} = 1 }}
\t}}'''


def _unchecked_strategic_resource_deficit_recovery_plan_text() -> str:
    subplans = [
        _strategic_resource_deficit_recovery_subplan_text(resource, label)
        for resource, label in ORDINARY_STRATEGIC_RESOURCE_RECOVERY
    ]
    return (
        "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
        "# Additive, bounded actual-deficit recovery; parent producer legality remains authoritative.\n\n"
        "basic_economy_plan = {\n"
        + "\n\n".join(subplans)
        + "\n}\n"
    )


def strategic_resource_recovery_contract_errors(primary_plan_text: str, recovery_plan_text: str) -> list[str]:
    errors: list[str] = []
    residual_name = "Stellar AI Director ESC component resource readiness"
    residual_block = _economic_subplan_block(primary_plan_text, residual_name)
    if not residual_block:
        errors.append(f"Missing unique residual ESC subplan: {residual_name}")
    else:
        if "\t\toptional = yes" not in residual_block:
            errors.append("Residual ESC readiness subplan must remain optional")
        if re.search(r"(?m)^\s*scaling\s*=", residual_block):
            errors.append("Residual ESC readiness subplan must remain non-scaling")
        for resource, _label in ORDINARY_STRATEGIC_RESOURCE_RECOVERY:
            if re.search(rf"(?m)^\s*{re.escape(resource)}\s*=", residual_block):
                errors.append(f"Residual ESC readiness subplan must not target ordinary resource {resource}")
        for resource, value in (
            ("sr_dark_matter", "3"),
            ("sr_zro", "3"),
            ("nanites", "3"),
            ("engineering_research", "600"),
            ("energy", "500"),
            ("minerals", "400"),
            ("trade", "150"),
        ):
            if not re.search(rf"(?m)^\s*{re.escape(resource)}\s*=\s*{value}\s*$", residual_block):
                errors.append(f"Residual ESC readiness subplan lost retained target {resource} = {value}")
        expected_targets = {
            "sr_dark_matter": "3",
            "sr_zro": "3",
            "nanites": "3",
            "engineering_research": "600",
            "energy": "500",
            "minerals": "400",
            "trade": "150",
        }
        income_block = extract_assignment_block(residual_block, "income")
        actual_targets: dict[str, str] = {}
        malformed_lines: list[str] = []
        for line in income_block[1:-1].splitlines() if income_block else ():
            stripped = line.split("#", 1)[0].strip()
            if not stripped:
                continue
            match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_]*)\s*=\s*([^\s{}]+)", stripped)
            if match is None or match.group(1) in actual_targets:
                malformed_lines.append(stripped)
                continue
            actual_targets[match.group(1)] = match.group(2)
        if malformed_lines or actual_targets != expected_targets:
            errors.append(
                "Residual ESC readiness income target set must remain exact; "
                f"expected={expected_targets!r} actual={actual_targets!r} "
                f"malformed={malformed_lines!r}"
            )

    try:
        parse_pdx(recovery_plan_text)
    except PDXParseError as exc:
        errors.append(f"Strategic-resource recovery plan does not parse: {exc}")
    if recovery_plan_text.count("basic_economy_plan = {") != 1:
        errors.append("Strategic-resource recovery file must define basic_economy_plan exactly once")
    if recovery_plan_text.count("\n\tsubplan = {") != len(ORDINARY_STRATEGIC_RESOURCE_RECOVERY):
        errors.append("Strategic-resource recovery file must contain exactly three subplans")
    if recovery_plan_text.count("\t\toptional = yes") != len(ORDINARY_STRATEGIC_RESOURCE_RECOVERY):
        errors.append("Strategic-resource recovery requires exactly three optional subplans")
    if re.search(r"(?m)^\s*scaling\s*=", recovery_plan_text):
        errors.append("Strategic-resource recovery subplans must remain non-scaling")

    forbidden_recovery_terms = (
        "has_technology",
        "has_monthly_income",
        "resource_stockpile_compare",
        "years_passed",
        "market",
        "staid_phase_",
    )
    for term in forbidden_recovery_terms:
        if term in recovery_plan_text:
            errors.append(f"Strategic-resource recovery must not add gate or market term: {term}")

    for resource, label in ORDINARY_STRATEGIC_RESOURCE_RECOVERY:
        set_name = f"Stellar AI Director actual-deficit recovery - {label}"
        block = _economic_subplan_block(recovery_plan_text, set_name)
        expected = _strategic_resource_deficit_recovery_subplan_text(resource, label)
        if not block:
            errors.append(f"Missing unique actual-deficit recovery subplan: {set_name}")
        elif block != expected:
            errors.append(f"Actual-deficit recovery subplan drifted from exact +1 has_deficit-only contract: {set_name}")
    return errors


def strategic_resource_deficit_recovery_plan_text(primary_plan_text: str | None = None) -> str:
    primary_plan_text = primary_plan_text if primary_plan_text is not None else economic_plan_text()
    recovery_plan_text = _unchecked_strategic_resource_deficit_recovery_plan_text()
    errors = strategic_resource_recovery_contract_errors(primary_plan_text, recovery_plan_text)
    if errors:
        raise ValueError("Strategic-resource recovery generation refused:\n" + "\n".join(errors))
    return recovery_plan_text


def strategic_resource_recovery_artifact_errors(mod_root: Path = MOD_ROOT) -> list[str]:
    primary_path = mod_root / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
    recovery_path = mod_root / STRATEGIC_RESOURCE_DEFICIT_RECOVERY_PATH.relative_to(MOD_ROOT)
    errors: list[str] = []
    if not primary_path.exists():
        errors.append(f"Missing primary economic plan: {primary_path}")
    if not recovery_path.exists():
        errors.append(f"Missing bounded strategic-resource recovery plan: {recovery_path}")
    if primary_path.exists() and recovery_path.exists():
        errors.extend(
            strategic_resource_recovery_contract_errors(
                read_text(primary_path),
                read_text(recovery_path),
            )
        )
    strategic_resource_root = mod_root / "common" / "strategic_resources"
    overrides = sorted(strategic_resource_root.rglob("*.txt")) if strategic_resource_root.exists() else []
    for override in overrides:
        errors.append(f"Ordinary strategic-resource object override is forbidden: {override}")
    return errors


def generate_strategic_resource_recovery_artifacts(mod_root: Path = MOD_ROOT) -> tuple[Path, Path]:
    primary_path = mod_root / "common" / "economic_plans" / "zzzz_staid_additive_economic_plan.txt"
    recovery_path = mod_root / STRATEGIC_RESOURCE_DEFICIT_RECOVERY_PATH.relative_to(MOD_ROOT)
    primary_plan_text = economic_plan_text()
    recovery_plan_text = strategic_resource_deficit_recovery_plan_text(primary_plan_text)
    write_text_file(primary_path, primary_plan_text)
    write_text_file(recovery_path, recovery_plan_text)
    return primary_path, recovery_path


def market_cap_breaker_sale_text(resource: str, reserve: int, amount: int, extra_limit: str) -> str:
    extra = f"\n\t\t\t{extra_limit}" if extra_limit else ""
    return f'''\t\tif = {{
\t\t\tlimit = {{{extra}
\t\t\t\tNOT = {{ has_deficit = {resource} }}
\t\t\t\thas_monthly_income = {{ resource = {resource} value > 0 }}
\t\t\t\tresource_stockpile_compare = {{ resource = {resource} value > {reserve} }}
\t\t\t\tresource_stockpile_percent = {{ resource = {resource} value >= 0.9 }}
\t\t\t}}
\t\t\tset_variable = {{
\t\t\t\twhich = staid_market_trade_value
\t\t\t\tvalue = value:staid_market_sell_value|RESOURCE|{resource}|AMOUNT|{amount}|
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
# Monthly Director safety layer for market cap breaking and colony-plan upkeep.

on_monthly_pulse = {
\tevents = {
\t\tstaid_economy_safety.1
\t}
}

'''


def mem_surveyor_outpost_ship_size_text() -> str:
    """Copy the active outpost winner and block one unresolved MEM event system for AI only."""
    active_starbase_extended = (
        Path(r"C:\Steam\steamapps\workshop\content\281990\3250900527")
        / "common"
        / "ship_sizes"
        / "sbx_3_0_starbases.txt"
    )
    snapshot_starbase_extended = (
        mod_source_root_for_id("3250900527") / "common" / "ship_sizes" / "nsc_starbases.txt"
    )
    vanilla = VANILLA_COMMON_ROOT / "ship_sizes" / "00_ship_sizes.txt"
    source_path = next(
        path
        for path in (active_starbase_extended, snapshot_starbase_extended, vanilla)
        if path.exists()
    )
    source_text = read_text(source_path)
    block = extract_top_level_object_text(source_text, "starbase_outpost")
    block = replace_top_level_child_block(
        block,
        "possible_construction",
        '''\tpossible_construction = {
\t\t# Keep the MEM Surveyor home system unclaimed only while its ruins anomaly
\t\t# is unresolved. Event mem_surveyor.300 adds this permanent planet modifier
\t\t# and then asks for a research station, so construction must reopen here.
\t\tOR = {
\t\t\tfrom = { is_ai = no }
\t\t\tsolar_system = { NOT = { has_star_flag = mem_surveyor_home_system } }
\t\t\tsolar_system = {
\t\t\t\tany_system_planet = {
\t\t\t\t\thas_carrier_flag = mem_surveyor_alkree_homeworld
\t\t\t\t\thas_modifier = mem_surveyor_alkree_homeworld
\t\t\t\t}
\t\t\t}
\t\t}
\t}''',
    )
    definitions = source_file_variable_definitions(source_text)
    used = sorted(used_at_variables_in_text(block))
    local_definitions = "\n".join(definitions[name] for name in used if name in definitions)
    return (
        "# Generated by tools/generate_stellar_ai_director_patch.py.\n"
        "# Active-winner compatibility copy; player construction remains unchanged.\n"
        f"# Source: {source_path.as_posix()}\n\n"
        + (local_definitions + "\n\n" if local_definitions else "")
        + block.rstrip()
        + "\n"
    )


def boss_defeat_escalation_on_actions_text() -> str:
    return '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Defeat-driven boss escalation. This hook is event-only and never changes
# normal-empire war scoring or runs on a periodic pulse.

on_space_battle_lost = {
	events = {
		staid_boss_safety.1
	}
}
'''


def boss_defeat_escalation_events_text() -> str:
    return '''# Generated by tools/generate_stellar_ai_director_patch.py.
# Active-stack compatibility: Gigas Rogue Eeloo and Ancient Systems Forgos
# are unusually strong fleets already marked as bosses by their parent mods.
# When either defeats an AI fleet, persistently promote that exact surviving
# fleet to the engine's ultra-boss readiness tier before another attempt.

namespace = staid_boss_safety

country_event = {
	id = staid_boss_safety.1
	hide_window = yes
	is_triggered_only = yes

	trigger = {
		is_ai = yes
		exists = fromfromfrom
		fromfromfrom = {
			OR = {
				has_fleet_flag = eeloofleet
				has_fleet_flag = legendary_guardian_fleet
			}
			NOT = { has_fleet_flag = staid_escalated_ultra_boss }
		}
	}

	immediate = {
		fromfromfrom = {
			# set_fleet_settings resets omitted settings. Both parent fleets use
			# spawn_debris = no, so preserve it while replacing boss with ultra-boss.
			set_fleet_settings = {
				spawn_debris = no
				is_ultra_boss = yes
			}
			set_fleet_flag = staid_escalated_ultra_boss
		}
	}
}
'''


def market_and_fleet_safety_events_text() -> str:
    sales = "\n".join(
        market_cap_breaker_sale_text(resource, reserve, amount, extra_limit)
        for resource, reserve, amount, extra_limit in MARKET_CAP_BREAKER_SALES
    )
    return f'''# Generated by tools/generate_stellar_ai_director_patch.py.
# Monthly market safety only; colony roles remain native AI decisions.
# Fleet movement and MIA recovery remain entirely native engine responsibilities.

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

# Director-owned market valuation. Do not depend on identifiers from the
# separately authored Stellar AI mod.
staid_market_sell_value = {{
\tcomplex_trigger_modifier = {{
\t\ttrigger = market_resource_price
\t\tparameters = {{
\t\t\tresource = $RESOURCE$
\t\t\tamount = $AMOUNT$
\t\t\ttrade_type = market_sell
\t\t}}
\t\tmode = add
\t}}
}}
'''


def readme_text(playset: dict[str, Any]) -> str:
    missing = [info["name"] for info in playset["required_mods"].values() if not info["present"]]
    parity_reference = playset.get("parity_reference_mods", {}).get("3610149307", {})
    return f'''# Stellar AI Director

Late-loading deterministic AI policy patch for the active Irony playset.

This mod is a deterministic standalone AI replacement baseline for the current
4.4 high-scale playset. It no longer declares or requires Stellar AI at launch.
Stellar AI remains a private parity reference for local development provenance:
the Director absorbs or reimplements the high-value AI budget, economic-plan,
research/economy/fleet conversion, construction-pressure, and war-support
surfaces needed for a viable single-AI baseline before deeper enhancements.

## Required Parents

- Gigastructural Engineering & More (4.4)
- NSC3
- Extra Ship Components NEXT
- Starbase Extended 3.0
- !!!Universal Resource Patch [2.4+]

Detected selected collection: `{playset["collection_name"]}`.

Missing required Steam parents during generation: {", ".join(missing) if missing else "none"}.

## Stellar AI Parity Reference

- Stellar AI source was used as private local parity evidence, not as a launch
  dependency.
- Reference present during generation: {parity_reference.get("present", False)}.
- Reference load position during generation: {parity_reference.get("load_position")}.
- Absorbed/reimplemented baseline surfaces: `common/ai_budget`,
  `common/economic_plans`, construction-pressure defines and budgets,
  research/economy/fleet conversion, market/runway safety, claim/war-support
  reserves, and high-scale modded progression hooks.
- Remaining standalone limits: direct diplomatic-action overrides, direct
  NSC3/ESC ship-design handling, executable-only target/reachability details,
  and runtime observer proof.

## Scope

- Adds scripted decision-state triggers for survival, recovery, megastructure
  prep, safe commit, surplus-sink pressure, and shipyard payoff exploitation.
- Overrides the regular `default` country type to remove Pegasus 4.4.4's
  pre-planner readiness deadlock: the 50% desired-navy requirement is omitted
  and the six-assault-army requirement is set to zero. Every other field is
  copied from the current vanilla object, and native target selection, casus
  belli, war goals, relative-strength checks, preparation, declarations, and
  fleet execution remain engine-owned. Regenerate and revalidate this
  full-object override after changing Stellaris versions.
- Copies the 20 ordinary/crisis personality objects from Pegasus 4.4.4 and
  substitutes only the working Stellar AI 0.10 `aggressiveness`, `bravery`, and
  `military_spending` values. Native behavior flags, diplomacy fields, design
  preferences, and selection rules remain intact.
- Gives diplomacy a bounded sub-40-year peaceful opening that exits immediately
  for war pressure or physical containment. Boxed-in empires strongly prefer
  Belligerent or Supremacist posture and retain claim pressure after five colonies.
- Replaces the native mineral army budgets with a modest uncapped reserve. The
  engine still chooses legal army types and counts; armies are not a declaration
  prerequisite and no unit is created by script.
- Applies a bounded Pegasus 4.4.4 high-naval-capacity workaround: the peacetime
  ship-budget share is reduced to 25% at 80% used capacity, but the category
  remains eligible so weak absolute fleets can still recover.
- Leaves the generic megastructure alloy budget upstream/parent-owned while
  retaining targeted Director route weights and Gigas special-resource support.
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
- Removes the legacy two-pulse stranded-fleet event. Its intended post-war
  rescue gate also matched idle fleets in active enemy territory and could
  recall an offensive fleet during homeland pressure; movement and MIA recovery
  now remain native engine responsibilities.
- Adds a fleet-throughput economic subplan so Mega Shipyard unlocks and strong
  surplus can become fleet power without ignoring energy/alloy/trade runway checks.
- Adds planetary-capacity and safe research economic-plan demand while leaving
  vanilla designation/zone eligibility to select legal research infrastructure.
- Adds hard AI eligibility for More Arcologies `building_navel_base` and
  `building_navel_command`: naval expansion must be strategically ready and
  research-designated worlds are excluded. Inactive building `ai_weight`
  modifiers are not used as plan enforcement.
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
  unlocks, AP/tradition category/node pressure, economy megastructures, planetcraft, war moon,
  systemcraft, and ESC starbase reactor support.
- Adds threat/economy-gated starbase defense pressure for copied safe parent
  starbase modules and buildings while keeping Starbase Extended Waystation
  section and ship/component surfaces outside Director ownership.
- Records 4.4.4 Nomad/Arkship compatibility as a targeted opening-research
  lane plus normal-empire-only high-scale pressure; the Director does not own
  Nomad colony types, Arkship ship sizes, Arkship component templates,
  Waystation sections, Waylines, Contracts, or Operational Reserve objects.
- Leaves ESC internal component-template `key = ...` overrides and direct NSC3
  ship-design templates as manual-review blockers until the atlas models those
  loader surfaces safely.

## Load Order

Place Stellar AI Director after all required content parents and after parent
compatibility patches that the Director must supersede. Stellar AI is not a
required parent and should not be needed for the standalone baseline. In the
current selected collection, the latest required parent is at load position
{max((info["load_position"] or 0) for info in playset["required_mods"].values())}.
The Director may still be compared against Stellar AI for private parity review,
but the descriptor intentionally omits a Stellar AI dependency.

## Runtime Proof

The normal mod must not fire startup proof popups or auto-confirm third-party
setup menus. Live-launch proof is checked through the launcher descriptor,
`dlc_load.json`, static validation, and explicit user-approved smoke testing
outside normal gameplay flow.

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
python tools/generate_stellar_ai_director_patch.py
python tools/validate_staid_444_war_solution.py
python tools/validate_stellar_ai_director_patch.py
python -m unittest discover -s tools/tests
```

Static validation proves generated file safety, known-reference coverage, and
deterministic policy contracts.
War-planning runtime proof remains one final fresh-game observer gate: run the
normal 4.4.4 playset for roughly 20–30 years with every regular empire under AI
control, then confirm multiple ordinary wars, a boxed-in breakout attempt, useful
but non-excessive offensive armies, and a functioning economy. Longer economic
and research benchmarking remains a separate Director quality goal.
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
        "| unlock-research policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive economic-plan subplan reimplements parity-reference research pressure into validated modded unlock gates |",
        "| alloy budgets | `common/ai_budget/zzz_staid_alloys_budget.txt` | medium | Director owns ship-conversion gates while the active parent retains the generic megastructure budget |",
        "| Gigas special-resource reserves | `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` | medium | intentional full-object overrides of Gigas megastructure special-resource budgets |",
        "| economy targets | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | high | intentional full-object replacement of `basic_economy_plan` with high-scale Gigas/NSC3/ESC survival targets |",
        "| fleet-throughput policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | medium | replacement economic-plan subplan maps shipyard ROI into crisis-scale alloy/energy/naval-cap targets after anti-collapse gates |",
        "| route unlock overrides | `common/technology/zzzz_staid_01_unlock_technology_technology.txt` | high | full-object copied source overrides add Director AI weights for Mega Engineering, Mega Shipyard, Gigas, NSC3, ESC, and starbase unlock chains |",
        "| AP/tradition category/node route overrides | `common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt`, `common/tradition_categories/zzzz_staid_02_perks_traditions_tradition_categories.txt`, `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` | medium | full-object copied source overrides preserve parent selection logic and add bounded Director route pressure to perks, categories, and selectable nodes |",
        "| megastructure route overrides | `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` | high | full-object copied source overrides add Director AI weights for economy multipliers, Mega Shipyard, planetcraft, war moon, and systemcraft starts; the Gigas habitat start uniquely preserves parent scoring and replaces only the global empty-habitat veto with a bounded colonization-plan penalty |",
        "| starbase static-defense policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt`, `common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt` | medium | additive economy reserves plus copied ESC starbase reactor AI weight support when crisis pressure is safe |",
        "| planetary-capacity policy | `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive economic-plan subplan raises mineral/energy, pop, and empire-size targets without building/job IDs |",
        "| trade-capacity policy | `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`, `common/economic_plans/zzzz_staid_additive_economic_plan.txt` | low | additive triggers and economy targets preserve Stellaris 4.4 trade logistics for ship, colony, market, and imbalance pressure |",
        "| cap-breaker market safety | `common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt`, `events/zzz_staid_market_and_fleet_safety_events.txt` | medium | additive monthly event sells large marketable positive-income overflow using Stellar AI market value script instead of allowing capped resources to void income |",
        "| native fleet-control restoration | `common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt`, `events/zzz_staid_market_and_fleet_safety_events.txt` | medium | the former two-pulse scripted MIA exception is removed; native mission assignment, access, and MIA behavior own active-war and post-war fleet movement |",
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
            "## Standalone Stellar AI Parity Reference",
            "",
            "Stellar AI is no longer a required launch dependency. Its current local source remains private parity evidence for this standalone baseline; copied or reimplemented surfaces must keep provenance notes and should not be prepared for redistribution without a later permission or rewrite pass.",
            "",
            "| reference mod | present | load position | role |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for info in playset.get("parity_reference_mods", {}).values():
        lines.append(
            f"| {info['name']} | {info['present']} | {info['load_position']} | private parity/reference source, not descriptor dependency |"
        )
    lines.extend(
        [
            "",
            "Baseline absorbed/reimplemented surfaces: AI budgets, `basic_economy_plan`, construction pressure, research/economy/fleet conversion, market/runway safety, claim/war support reserves, and high-scale modded progression hooks.",
            "",
            "Deferred non-baseline surfaces: diplomatic-action overrides, direct ship-design/component/section handling for NSC3/ESC, executable target-specific reachability internals, and runtime observer proof. Complete 4.4.4 personality objects and native war-support budgets are now implemented.",
        ]
    )
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
            "The Stellar AI parity-reference monthly market script sells only a small bounded number of surplus batches. The Director adds a late-loading monthly safety event for large positive-income overflow in resources with both a finite stockpile maximum and verified market tradability: minerals, food, consumer goods, volatile motes, exotic gases, rare crystals, Zro, dark matter, and Gigas sentient metal. Nanites, alloys, energy, unity, negative mass, and ambiguous non-market Gigas construction resources are intentionally excluded from direct forced selling.",
            "",
            "## Stranded-Fleet Recovery Policy",
            "",
            "The Director does not issue fleet orders. The former two-pulse `set_mia = mia_return_home` exception was intended for post-war access pockets, but its foreign-space test also matched active enemy territory and could recall an offensive fleet during homeland pressure. The exception is removed; native pathfinding, access, and MIA handling own recovery.",
            "",
            "## Unlock-Research Policy",
            "",
            "The Director treats modded unlock research as mandatory survival pressure. Core targets include Mega Engineering, Mega Shipyard, Gigas planetcraft/systemcraft chains, NSC3 large hull infrastructure, ESC high-tier components, and the economy techs needed to feed them. Full-object copied source overrides now add direct AI weights for those route unlocks and bounded pressure on selected AP/tradition categories and selectable nodes.",
            "",
            "## Static-Defense Policy",
            "",
            "Defensive starbase investment is expressed as additive `basic_economy_plan` subplans plus a copied ESC starbase reactor override. The v1 policy requires no recovery mode, no short-runway core deficit, safe alloy/energy income and stockpiles, then either defensive ethics without an aggressive under-cap fleet push or high threat pressure.",
            "",
            "## Planetary-Capacity Policy",
            "",
            "Expanded planet and building capacity is covered through safe country-level economic-plan demand. Research demand is enabled only behind consumer-goods, energy, and deficit runway gates; vanilla research-zone eligibility remains the hard construction boundary. More Arcologies naval buildings use explicit AI eligibility that excludes research-designated worlds.",
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
            "- Direct technology/AP/tradition category/node object overrides are emitted from copied source objects for the supported high-scale route families; automatic adoption/finish rewards remain untouched.",
            "- Direct Mega Shipyard, economy megastructure, planetcraft, war moon, and systemcraft object weights are emitted from copied source objects and paired with economy/reserve gates.",
            "- Direct starbase support includes copied ESC starbase reactor AI weight plus country-level static-defense economy targets.",
            "- Research infrastructure uses safe economic-plan demand plus vanilla research-zone eligibility; inactive building `ai_weight` is not treated as the primary construction planner.",
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
        f"Required compatibility-mod maximum load position: {latest_parent}",
        "",
        "## Required Position",
        "",
        "- Load after Gigastructural Engineering & More (4.4).",
        "- Load after NSC3.",
        "- Load after Extra Ship Components NEXT.",
        "- Load after Starbase Extended 3.0.",
        "- Load after Planetary Diversity and Planetary Diversity - More Arcologies when those collection surfaces are active.",
        "- Load after !!!Universal Resource Patch [2.4+].",
        "- Load after compatibility patches whose AI/economy behavior the Director intentionally coordinates.",
        "- Stellar AI is not a required parent for the standalone baseline; keep it only as private parity/reference evidence when comparing behavior during development.",
        "- Load before any future local patch that intentionally overrides the Director.",
        "",
        "## Required Compatibility Evidence",
        "",
        "| mod | present | load position |",
        "| --- | --- | ---: |",
    ]
    for info in required:
        lines.append(f"| {info['name']} | {info['present']} | {info['load_position']} |")
    lines.extend(
        [
            "",
            "## Stellar AI Standalone Parity",
            "",
            "The Director descriptor intentionally omits Stellar AI. Current Stellar AI source is a private local parity reference only; its high-value AI budget, economic-plan, construction-pressure, research/economy/fleet conversion, and war-support surfaces are absorbed or reimplemented by Director-owned generated files.",
            "",
            "| reference mod | present | load position | role |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for info in playset.get("parity_reference_mods", {}).values():
        lines.append(
            f"| {info['name']} | {info['present']} | {info['load_position']} | private parity/reference source, not descriptor dependency |"
        )
    lines.extend(
        [
            "",
            "## Current Intentional Supersession",
            "",
            "- `common/ai_budget/zzz_staid_alloys_budget.txt` owns only ship and upgrade gates; the generic `alloys_expenditure_megastructures` budget remains upstream/parent-owned so it cannot crowd out outposts or fleets.",
            "- `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` intentionally overrides Gigas `sentient_metal_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, and `supertensiles_upkeep_megastructures` budgets.",
            "- `common/economic_plans/zzzz_staid_additive_economic_plan.txt` intentionally replaces `basic_economy_plan` with Director high-scale survival economy, mandatory modded unlock research, trade-capacity, fleet-throughput, static-defense, and planetary-capacity targets.",
            "- `common/buildings/zzzz_staid_13_dataset_job_pressure_buildings.txt` maps selected nonmilitary parent buildings to `ai_resource_production`; military-capacity objects are excluded from this generated pressure path.",
            "- `common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt` narrowly overrides More Arcologies naval administration buildings with AI strategic-readiness and research-world exclusion gates.",
            "- Additive scripted triggers, script values, and economic-plan subplans use the `staid_` namespace and should not conflict with parent object IDs.",
        ]
    )
    return "\n".join(lines) + "\n"


def conflicts_note_text() -> str:
    return """# Stellar AI Director Conflict Notes

## Intentional Conflicts

- `common/ai_budget/zzz_staid_alloys_budget.txt` does not replace upstream `alloys_expenditure_megastructures`; the active parent retains generic reserve ownership while Director object weights rank specific legal projects.
- `common/ai_budget/zzz_staid_gigas_resource_budgets.txt` intentionally replaces upstream Gigas special-resource megastructure budget objects: `sentient_metal_expenditure_megastructures`, `negative_mass_expenditure_megastructures`, and `supertensiles_upkeep_megastructures`.
- `common/economic_plans/zzzz_staid_additive_economic_plan.txt` intentionally replaces `basic_economy_plan` with Director high-scale survival economy, mandatory modded unlock research, trade-capacity, fleet-throughput, static-defense, and planetary-capacity targets; despite the historical filename, conflict review must treat it as a Director-owned economic-plan surface.
- `common/technology/zzzz_staid_01_unlock_technology_technology.txt` intentionally replaces copied vanilla/Gigas/NSC3/ESC/Starbase Extended technology objects with Director route AI weights.
- `common/ascension_perks/zzzz_staid_02_perks_traditions_ascension_perks.txt`, `common/tradition_categories/zzzz_staid_02_perks_traditions_tradition_categories.txt`, and `common/traditions/zzzz_staid_02_perks_traditions_traditions.txt` intentionally replace copied AP/category/selectable-node objects with bounded Director route AI weights; automatic adoption/finish rewards are not overridden.
- `common/megastructures/zzzz_staid_03_megastructures_megastructures.txt` intentionally replaces copied Gigas/vanilla-compatible megastructure starts for economy multipliers, Mega Shipyard, planetcraft, war moon, and systemcraft priority.
- `common/starbase_buildings/zzzz_staid_05_starbase_defense_starbase_buildings.txt` intentionally replaces copied ESC starbase reactor support with Director crisis-starbase pressure.
- `common/buildings/zzzzz_staid_14_pd_naval_capacity_hard_gates.txt` narrowly replaces More Arcologies `building_navel_base` and `building_navel_command` so AI naval-capacity construction requires strategic readiness and cannot consume research-world slots.

## Expected Additive Surfaces

- `common/economic_plans/zzzz_staid_21_strategic_resource_deficit_recovery.txt` (three unique optional, non-scaling, actual-deficit-only +1 subplans; no strategic-resource object override)
- `common/scripted_triggers/zzz_staid_decision_state_triggers.txt`
- `common/script_values/zzz_staid_roi_values.txt`
- `common/scripted_triggers/zzz_staid_threat_response_triggers.txt`
- `common/script_values/zzz_staid_threat_response_values.txt`
- `common/on_actions/zzz_staid_market_and_fleet_safety_on_actions.txt`
- `events/zzz_staid_market_and_fleet_safety_events.txt`
- `common/on_actions/zzzz_staid_boss_defeat_escalation_on_actions.txt`
- `events/zzzz_staid_boss_defeat_escalation_events.txt`
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
- The residual ESC readiness subplan is optional and non-scaling and does not target volatile motes, exotic gases, or rare crystals; those resources use separate actual-deficit-only +1 subplans.
- Vanilla and parent mods retain producer eligibility and ordinary strategic-resource object ownership.
- ESC internal component-template `key = ...` overrides and direct NSC3 ship-design templates remain manual-review blockers until the atlas models those loader surfaces safely.

## Strategic V2 Compatibility Reviews

- Starbase Extended review: Director-owned starbase defense pressure is limited to copied safe module/building surfaces and generated economy gates. Parent-owned Waystation sections, ship sizes, component templates, and related starbase/ship loader surfaces remain out of scope because the active conflict matrix shows high-risk parent conflicts there.
- Planetary Diversity / More Arcologies review: `building_navel_base` and `building_navel_command` use narrow hard AI eligibility, not dataset weight pressure. `building_pd_rogue_council`, More Arcologies zones, and broad colony/designation rewrites remain blocked until their AI, UI, and load-order semantics are proven.
- Nomad/Arkship review: Director has one additive targeted opening route for Arkship research and otherwise keeps high-scale pressure normal-empire-only. It does not override Nomad colony types, Arkship ship sizes, Arkship component templates, Waystation sections, Waylines, Contracts, or Operational Reserve objects.

## Review Rules

- Any new full-object override must include an ownership note naming the parent surface and reason.
- Optional-mod references must be omitted or guarded unless the generator proves the referenced object exists.
- Irony conflict results should be classified as intentional Director wins, parent wins required, harmless additive duplicates, unexpected gameplay conflicts, or false positives.

## Irony Analyze Only Review

- Reviewed in Irony Conflict Solver Analyze Only for collection `4.4 Stellaris Mod Collection w/Load Order: NSC3, Planetary Diversity`.
- Existing collection order was preserved; `Stellar AI Director` is the only added local mod and is last after `!!!Universal Resource Patch [2.4+]`.
- Reviewed `common\\ai_budget` conflicts: `negative_mass_expenditure_megastructures`, `sentient_metal_expenditure_megastructures`, and `supertensiles_upkeep_megastructures`.
- Each reviewed object resolves to `Stellar AI Director ... (LIOS)` as an intentional Director win.
- No unexplained Director gameplay conflicts were observed in the reviewed Director conflict set.
- Fresh Irony UI review has not yet been repeated for the strategic v2 starbase and Planetary Diversity surfaces; current classifications are based on generated audits and indexed active conflict-matrix evidence.
"""


def observer_test_log_text(playset: dict[str, Any]) -> str:
    if OBSERVER_SMOKE_SAVE_SUMMARY_JSON.exists():
        summary = json.loads(read_text(OBSERVER_SMOKE_SAVE_SUMMARY_JSON))
        setup = f"""- Galaxy size: Tiny Irony-launched smoke save.
- AI count: inferred from save country count ({summary['initialized_country_count']} initialized countries).
- Difficulty: Cadet smoke setup from launch run notes.
- Crisis settings: inherited selected playset defaults for the smoke save.
- Mod order evidence: required parents are recorded in `notes/load-order.md`; save mod list contains {summary['mod_count']} mods."""
        historical_checkpoints = f"""- Early economy stability: short-smoke pass from `{OBSERVER_SMOKE_SAVE_SUMMARY_MD.name}`.
- Deficit spiral check: no early deficit collapse observed in parsed 2202.01.01 save metrics."""
        strategic_v2_checkpoints = """- First Mega Engineering unlock: not yet proven in the current strategic v2 branch.
- First high-ROI megastructure start: not yet proven in the current strategic v2 branch.
- First economy multiplier completion: not yet proven in the current strategic v2 branch.
- Shipyard/fleet payoff behavior: not yet proven in the current strategic v2 branch.
- War interruption behavior: not yet proven in the current strategic v2 branch.
- Starbase defense investment: not yet proven in the current strategic v2 branch.
- At least one AI empire reaching 3,000+ total monthly research before 2350: not yet proven in the current strategic v2 branch."""
        threat_response = """- Classified aggressive war deterministic contract: covered by generated tests and validator.
- Threat-response generated files emitted after 2026-07-05 implementation: covered by file audit and validator.
- Unknown/modded war goal inertness: covered by classification data, tests, and validator.
- No forced wars, join-war behavior, or punitive CBs: covered by forbidden-effect tests and validator.
- Runtime launch observation: required only after non-runtime gates are complete and runtime evidence is the final remaining blocker."""
        results = f"""Short Irony-launched save summary: `{OBSERVER_SMOKE_SAVE_SUMMARY_MD.name}`.

- Save date: {summary['date']}.
- Director listed in save mod list: {summary['required_mods_present'].get('Stellar AI Director')}.
- Short smoke passes: {summary['short_smoke_passes']}.
- Player metrics: `{json.dumps(summary['player_metrics'], sort_keys=True)}`.
- Player monthly income: `{json.dumps(summary['player_monthly_income'], sort_keys=True)}`.
- High-ROI path observed: {summary['high_roi_path_observed']}.

This short-smoke evidence is retained as historical context only. Generated
artifacts, tests, validators, and indexed evidence are the non-runtime gates for
the strategic v2 packet; they do not replace the final constrained observer run
required to prove long-run AI efficacy and the 3,000+ total-research-per-month
before 2350 target."""
    else:
        setup = """- Galaxy size: not run yet.
- AI count: not run yet.
- Difficulty: not run yet.
- Crisis settings: not run yet.
- Mod order evidence: required parents are recorded in `notes/load-order.md`."""
        historical_checkpoints = """- Early economy stability: pending.
- Deficit spiral check: pending."""
        strategic_v2_checkpoints = """- First Mega Engineering unlock: not yet proven in the current strategic v2 branch.
- First high-ROI megastructure start: not yet proven in the current strategic v2 branch.
- First economy multiplier completion: not yet proven in the current strategic v2 branch.
- Shipyard/fleet payoff behavior: not yet proven in the current strategic v2 branch.
- War interruption behavior: not yet proven in the current strategic v2 branch.
- Starbase defense investment: not yet proven in the current strategic v2 branch.
- At least one AI empire reaching 3,000+ total monthly research before 2350: not yet proven in the current strategic v2 branch."""
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

## Historical Smoke Checkpoints

{historical_checkpoints}

## Strategic V2 Observer Checkpoints

{strategic_v2_checkpoints}

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
        "| 4.4.4 peacetime new-ship guard | 0.80 used naval capacity | avoid entering the executable high-capacity war-declaration defect; war/emergency bypasses |",
        "| native army reserve | 200 minerals base; +300 boxed; +300 conquest/raiding; +500 war/existential | fund useful assault-army recruitment without forcing units or capping demand |",
        "| war preparation window | 12–30 months | restore working native preparation rather than one-month declaration churn |",
        "| strategic value horizon year | 2350 | long-lived economic, military, and modifier payoffs are weighted by remaining months before this goal date |",
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
        "- Generated starbase pressure is guarded by `staid_static_defense_threat_window` and `staid_starbase_defense_economy_safe`.",
        "- Copied safe Starbase Extended/ESC starbase module and building objects can receive Director defense pressure; Waystation sections, ship sizes, component templates, and other loader-sensitive defense surfaces remain outside Director ownership.",
        "",
        "## Trade-Capacity Policy",
        "",
        "- Trade is modeled as Stellaris 4.4 logistics/capacity headroom, not as a normal priced ROI resource.",
        "- The generated `basic_economy_plan` includes trade reserve and trade recovery subplans so the Director's full-object replacement keeps trade logistics visible while pushing beyond vanilla/Stellar AI scale.",
        "- Fleet, planetary, megastructure, static-defense, and surplus gates require trade income floors before adding more ship, colony, or resource-imbalance upkeep pressure.",
        "- Advanced component and modded fleet conversion routes require core support runway, fleet-level trade capacity, and strategic-resource income before their strategic-resource pressure can fire.",
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
        "- Militarist conquest, raiding-pop acquisition, and early hostile-fauna clearance now have separate fleet reserve lanes; military empires are not forced to wait for peaceful surplus-only fleet spending.",
        "- War declaration globals use 12–30 months preparation, base aggression 25, enemy-fleet multiplier 1.2, a 300-hop outer consideration ceiling, a distance preference beginning after 25 hops, minimum score 0.5, and offense/defense allotment 1.0. The preference threshold is not a home-system growth cutoff. Boxed-in multipliers remain bounded above vanilla at 8/12.",
        "- Normal peacetime new-ship budget share falls to 25% at 80% used naval capacity but remains eligible. This bounded native-data workaround reduces exposure to the 4.4.4 executable high-cap declaration defect without permanently freezing weak absolute fleets.",
        "- Native army budgets reserve 200 minerals at baseline, with bounded additions for boxed-in, conquest/raiding, war, and existential-defense states. No desired_max caps recruitment and no army is created by script.",
        "- Empires that already possess a raiding perk, civic, or origin prioritize raiding bombardment and a no-surrender bombardment posture; generic conquerors are not pushed toward `ap_nihilistic_acquisition`.",
        "- Hostile space fauna continues to use the engine's separate boss readiness lane at 100000/500000 military power. Ordinary empire confidence uses the native `ENEMY_FLEET_POWER_MULT = 1.2`; boss readiness is not made easier by the war-planner repair.",
        "",
        "## Unlock-Research Policy",
        "",
        "- The unlock-research policy is mandatory survival pressure after the opening curve, not a surplus-only luxury; it keeps physics, society, engineering, and unity pressure on until core Mega Engineering, Mega Shipyard, Gigas, NSC3, and ESC unlock paths are reachable.",
        "- Direct technology/AP/tradition category/node route overrides are emitted from copied source objects and trace back to the policy matrix and route override report.",
        "",
        "## Mega/Giga Build Priority Policy",
        "",
        "- ROI-ready megastructure and gigastructure rows are mapped through generated alloy, special-resource, and economy-plan gates.",
        "- Generated full-object route overrides now cover Dyson Sphere, Mega Shipyard, neutronium gigaforge, Nidavellir forge, Matrioshka brain, planetcraft printer, war moon, and systemcraft starts; generated files preserve parent `@variable` parse context and remove absent optional `pc_magnetar` compatibility references.",
        "- The Gigas habitat start preserves parent base/site scoring, the 30-year queued-build cooldown, the starport veto, and the AI habitat cap. An active native colonization plan applies a nonzero `0.1` backlog penalty instead of any empty habitat hard-zeroing all future starts; crowded-tall readiness adds only a bounded factor `2`.",
        "- Exotic projects outside those route starts remain inventoried until the core loop is observer-tested against the high-scale crisis benchmark.",
        "",
        "## Planetary-Capacity Policy",
        "",
        "- Expanded planet/building capacity is covered through a country-level economic-plan subplan once mineral, energy, and trade logistics runway are safe.",
        "- The generated subplan uses supported `pops` and income targets only; do not emit `empire_size`, which the current Stellaris 4.4.4 economic-plan surface rejects.",
        "- Safe research economic-plan demand is gated by `staid_research_construction_priority_ready`; vanilla research-zone eligibility remains the hard building boundary. The Director no longer emits research or pop-assembly building `ai_weight` files as if they were an authoritative planner.",
        "- Planetary Diversity outpost decisions are copied into generated decision overrides with Director-owned weights for moon, mining, food, energy, and research outposts; the research family strongly favors the capital because the opening strategy treats the capital as the first research hub.",
        "- Planetary Diversity decision availability owns tech, site, and button prerequisites. Director weights do not duplicate those checks; if the button is available and the mineral/energy runway is safe, the AI is pushed to use the matching outpost.",
        "- Permanent and long-lived scaling investments use a 2350 horizon: the same outpost, building, tech, megastructure, or buff is worth far more in 2220 than in 2320 because every remaining year multiplies its payoff.",
        "- Unity-to-research pressure targets source-backed Discovery, Diplomacy, Technological Ascendancy, Master Builders, Galactic Wonders, and Gigastructural Constructs paths instead of hoarding unity generically.",
        "- Research diplomacy pressure stays on the safe lane: copied Research Cooperative federation weighting and Discovery/Diplomacy/AP support remain, while the cooperative stance is restricted to the temporary diplomatic opening and exits for native war pressure. Direct research-agreement actions remain gated.",
        "- Planetary Diversity outpost decisions retain source-owned availability and Director decision weights; obsolete generated PD building-weight and role-trigger files are removed.",
        "- More Arcologies support is intentionally narrow: `building_navel_base` and `building_navel_command` use hard AI strategic-readiness and research-world exclusion gates, while `building_pd_rogue_council`, More Arcologies zones, and broad colony/designation rewrites remain blocked.",
        "- Arkship carrier planets are excluded from copied Planetary Diversity outpost decisions, and later high-scale planetary pressure remains normal-empire-only where the Nomad/Arkship audit found no safe shared surface.",
        "",
        "## Nomad/Arkship Compatibility Policy",
        "",
        "- Nomadic empires get only the targeted opening research route `staid_opening_nomad_arkship_research` until a dedicated Nomad strategy is proven.",
        "- Most megastructure, colony, starbase, war, fleet, fauna, and planetary-capacity pressure is guarded for normal empires with `is_nomadic = no`.",
        "- The Director does not override Nomad colony types, Arkship ship sizes, Arkship component templates, Waystation sections, Waylines, Contracts, or Operational Reserve objects; those remain owned by vanilla and parent mods.",
        "",
        "## NSC3/ESC Design Policy",
        "",
        "- NSC3 and ESC unlock technologies now have copied source-object route AI weights and are paired with fleet-throughput economy gates.",
        "- Ordinary volatile-mote, exotic-gas, and rare-crystal recovery is isolated in three optional, non-scaling `has_deficit`-only subplans with a target of `+1`; small stores or small positive income alone do not activate them.",
        "- The broader ESC readiness subplan no longer targets those three ordinary resources and is optional and non-scaling; it retains only its existing advanced-resource and support-economy targets.",
        "- Producer legality remains owned by vanilla and parent mods. The Director emits no ordinary `strategic_resources` object overrides, scripted purchases, free resources, technology gates, or market gates for this recovery lane.",
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
        "- The Director does not issue movement, stance, MIA, or pathfinding orders from script.",
        "- The removed two-pulse handler was intended for post-war access pockets, but its foreign-space predicate also selected current enemy territory.",
        "- Native pathfinding, border access, and MIA behavior now own both active-war travel and post-war recovery.",
        "",
        "## Safe Tuning Rules",
        "",
        "- Do not lower prep or commit reserves below survival/recovery safety gates.",
        "- Keep research sink before fleet sink until core modded unlocks are available.",
        "- Treat unpriced resources and trade logistics as bottlenecks, not fake scalar value.",
        "- Re-run generator, validator, unit tests, and coverage after every tuning change.",
    ]
    return "\n".join(lines) + "\n"


COLONY_TYPE_PLANET_ONLY_FLAG_OPERATIONS = frozenset(
    {
        "has_planet_flag",
        "set_planet_flag",
        "remove_planet_flag",
    }
)


def generated_colony_root_scope_errors(mod_root: Path = MOD_ROOT) -> list[str]:
    errors: list[str] = []
    colony_root_surfaces = tuple(
        path
        for path in (
            mod_root / "common" / "colony_types",
            mod_root / "common" / "districts",
        )
        if path.exists()
    )
    if not colony_root_surfaces:
        return errors

    scope_switches = {
        "planet": "planet",
        "owner": "country",
        "owner_or_space_owner": "country",
        "space_owner": "country",
        "solar_system": "galactic_object",
        "fleet": "fleet",
        "ship": "ship",
        "leader": "leader",
        "pop": "pop",
    }

    def walk(block: PDXBlock, scope: str, file_path: Path, object_id: str, trail: tuple[str, ...]) -> None:
        for assignment in block_assignments(block):
            key = assignment.key
            next_trail = (*trail, key)
            if key in COLONY_TYPE_PLANET_ONLY_FLAG_OPERATIONS and scope != "planet":
                relative = file_path.relative_to(mod_root).as_posix()
                errors.append(
                    f"{relative}: object {object_id} uses planet-only {key} from {scope} scope at "
                    f"{'/'.join(next_trail)}; wrap it in planet = {{ ... }}"
                )
            if isinstance(assignment.value, PDXBlock):
                normalized_key = key[:-1] if key.endswith("?") else key
                child_scope = scope_switches.get(normalized_key, scope)
                walk(assignment.value, child_scope, file_path, object_id, next_trail)

    for surface_root in colony_root_surfaces:
        for file_path in sorted(surface_root.rglob("*.txt")):
            try:
                parsed = parse_file(file_path)
            except PDXParseError as exc:
                errors.append(str(exc))
                continue
            for assignment in block_assignments(parsed):
                if assignment.key.startswith("@") or not isinstance(assignment.value, PDXBlock):
                    continue
                walk(assignment.value, "colony", file_path, assignment.key, ())
    return errors


def validate_generated_patch(snapshot_root: Path = SNAPSHOT_ROOT) -> list[str]:
    errors: list[str] = []
    errors.extend(stale_stellar_ai_dependency_errors(MOD_ROOT, RESEARCH_ROOT))
    errors.extend(forbidden_generated_surface_errors(MOD_ROOT))
    errors.extend(strategic_resource_recovery_artifact_errors(MOD_ROOT))
    errors.extend(validate_object_atlas_artifacts())
    if not economic_valuation_evidence_passes():
        errors.append(
            "Economic valuation evidence gate failed: regenerate/validate "
            f"{ECONOMIC_VALUATION_DATASET_CSV.relative_to(REPO_ROOT)} and "
            f"{NONCONSTRUCTION_ECONOMIC_VALUATION_DATASET_CSV.relative_to(REPO_ROOT)} before emitting economic AI weights."
        )
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
    errors.extend(validate_staid_scripted_trigger_cycles(MOD_ROOT))
    errors.extend(generated_colony_root_scope_errors(MOD_ROOT))
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
