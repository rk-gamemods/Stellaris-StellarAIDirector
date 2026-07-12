#!/usr/bin/env python3
"""Model recurring fleet pressure separately from ship construction costs.

The Stellaris AI budget can observe country income and deficits, but it cannot
inspect the upkeep vector of the next auto-design or the ships already queued.
This module therefore owns two distinct contracts:

* source inventory: identify construction, upkeep, and logistics resources in
  the active ship stack; and
* policy scenarios: test whether a proposed completion tranche preserves
  positive net income for every recurring resource it consumes.

The production mod remains native-AI-only. This tool never changes game state.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = (
    REPO_ROOT
    / "research"
    / "stellar-ai"
    / "stellar-ai-director-fleet-economy-model-2026-07-12.json"
)

ACTIVE_SHIP_STACK_ROOTS = {
    "nsc3": Path(r"C:\Steam\steamapps\workshop\content\281990\683230077"),
    "esc_next": Path(r"C:\Steam\steamapps\workshop\content\281990\2648658105"),
    "gigastructures": Path(r"C:\Steam\steamapps\workshop\content\281990\1121692237"),
    "spacefleet_tactica": Path(r"C:\Steam\steamapps\workshop\content\281990\3696204283"),
}

# Every ordinary military fleet in the active stack consumes these resources.
# Food is strict only for biological fleets. The optional resources are
# component/special-hull sensitive. Native expense checks let unused resources
# remain at zero, while any resource with current expense must have positive net.
CORE_POSITIVE_RESOURCES = ("energy", "alloys", "trade")
BIO_POSITIVE_RESOURCES = ("food",)
OPTIONAL_NONNEGATIVE_RESOURCES = (
    "minerals",
    "giga_sr_sentient_metal",
    "influence",
)
STANDARD_OPTIONAL_NONNEGATIVE_RESOURCES = (
    "food",
    *OPTIONAL_NONNEGATIVE_RESOURCES,
)


def render_recurring_income_triggers() -> str:
    """Render the strongest native gate possible without design/queue access."""

    def income_lines(resources: Iterable[str], operator: str) -> list[str]:
        return [
            f"\thas_monthly_income = {{ resource = {resource} value {operator} 0 }}"
            for resource in resources
        ]

    def expense_aware_lines(resources: Iterable[str]) -> list[str]:
        lines: list[str] = []
        for resource in resources:
            lines.extend(
                [
                    "\tOR = {",
                    "\t\tresource_expenses_compare = {",
                    f"\t\t\tresource = {resource}",
                    "\t\t\tvalue = 0",
                    "\t\t}",
                    f"\t\thas_monthly_income = {{ resource = {resource} value > 0 }}",
                    "\t}",
                ]
            )
        return lines

    standard = [
        "staid_standard_fleet_recurring_income_safe = {",
        "\tcountry_uses_bio_ships = no",
        *income_lines(CORE_POSITIVE_RESOURCES, ">"),
        *expense_aware_lines(STANDARD_OPTIONAL_NONNEGATIVE_RESOURCES),
        "}",
    ]
    biological = [
        "staid_bioship_fleet_recurring_income_safe = {",
        "\tcountry_uses_bio_ships = yes",
        *income_lines(CORE_POSITIVE_RESOURCES, ">"),
        *income_lines(BIO_POSITIVE_RESOURCES, ">"),
        *expense_aware_lines(OPTIONAL_NONNEGATIVE_RESOURCES),
        "}",
    ]
    combined = [
        "staid_wartime_fleet_recurring_income_safe = {",
        "\tOR = {",
        "\t\tstaid_standard_fleet_recurring_income_safe = yes",
        "\t\tstaid_bioship_fleet_recurring_income_safe = yes",
        "\t}",
        "}",
    ]
    return "\n".join(
        [
            "# Active-stack recurring fleet pressure. Construction-only resources",
            "# remain governed by native affordability; wartime stockpiles are not gates.",
            "\n".join(standard),
            "\n".join(biological),
            "\n".join(combined),
        ]
    ) + "\n"


@dataclass(frozen=True)
class FleetEconomyState:
    at_war: bool
    naval_capacity_fraction: float
    monthly_net: Mapping[str, float]
    monthly_expenses: Mapping[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class FleetPressureDecision:
    allowed: bool
    blocking_resources: tuple[str, ...]
    projected_net: Mapping[str, float]


def recurring_resources(*, biological: bool) -> tuple[str, ...]:
    resources = list(CORE_POSITIVE_RESOURCES)
    if biological:
        resources.extend(BIO_POSITIVE_RESOURCES)
        resources.extend(OPTIONAL_NONNEGATIVE_RESOURCES)
    else:
        resources.extend(STANDARD_OPTIONAL_NONNEGATIVE_RESOURCES)
    return tuple(resources)


def policy_recurring_resource_union() -> set[str]:
    return set(recurring_resources(biological=False)) | set(
        recurring_resources(biological=True)
    )


def evaluate_completion_tranche(
    state: FleetEconomyState,
    tranche_upkeep: Mapping[str, float],
    *,
    biological: bool,
    naval_capacity_limit: float = 0.90,
) -> FleetPressureDecision:
    """Return whether the next modeled tranche leaves recurring net positive.

    Optional component resources with no current expense or modeled tranche
    upkeep may remain at zero. Any consumed resource must remain strictly positive.
    Stockpiles are intentionally absent from this contract.
    """

    projected = {
        resource: float(state.monthly_net.get(resource, 0.0))
        - float(tranche_upkeep.get(resource, 0.0))
        for resource in recurring_resources(biological=biological)
    }
    blockers: list[str] = []
    if not state.at_war:
        blockers.append("not_at_war")
    if state.naval_capacity_fraction >= naval_capacity_limit:
        blockers.append("naval_capacity")
    strict = set(CORE_POSITIVE_RESOURCES)
    if biological:
        strict.update(BIO_POSITIVE_RESOURCES)
    for resource, net in projected.items():
        consumes_resource = float(tranche_upkeep.get(resource, 0.0)) > 0.0
        has_current_expense = float(state.monthly_expenses.get(resource, 0.0)) > 0.0
        if resource in strict or consumes_resource or has_current_expense:
            if net <= 0.0:
                blockers.append(resource)
    return FleetPressureDecision(
        allowed=not blockers,
        blocking_resources=tuple(blockers),
        projected_net=projected,
    )


def _director_module() -> Any:
    try:
        from tools import stellar_ai_director_lib as director
    except ModuleNotFoundError:
        import stellar_ai_director_lib as director
    return director


def _resource_keys(value: object) -> set[str]:
    director = _director_module()

    if not isinstance(value, director.PDXBlock):
        return set()
    return {
        item.key
        for item in value.items
        if isinstance(item, director.PDXAssignment)
        and item.key not in {"trigger", "mult", "multiplier", "category"}
    }


def _walk_assignments(value: object) -> Iterable[object]:
    director = _director_module()

    if not isinstance(value, director.PDXBlock):
        return
    for item in value.items:
        if isinstance(item, director.PDXAssignment):
            yield item
            yield from _walk_assignments(item.value)
        elif isinstance(item, director.PDXBlock):
            yield from _walk_assignments(item)


def scan_ship_economy_roots(
    roots: Mapping[str, Path],
) -> dict[str, dict[str, object]]:
    """Inventory mobile-ship/component resource pressure from PDXScript roots."""

    director = _director_module()

    report: dict[str, dict[str, object]] = {}
    for label, root in roots.items():
        construction: set[str] = set()
        upkeep: set[str] = set()
        logistics: set[str] = set()
        files_scanned = 0
        source_digest = hashlib.sha256()
        for relative in ("common/ship_sizes", "common/component_templates"):
            folder = root / relative
            if not folder.exists():
                continue
            for path in sorted(folder.rglob("*.txt")):
                raw = path.read_bytes()
                text = raw.decode("utf-8-sig", errors="replace")
                if not text.strip():
                    continue
                source_digest.update(path.relative_to(root).as_posix().encode("utf-8"))
                source_digest.update(b"\0")
                source_digest.update(raw)
                parsed = director.parse_pdx(text)
                files_scanned += 1
                for assignment in _walk_assignments(parsed):
                    if assignment.key != "resources" or not isinstance(
                        assignment.value, director.PDXBlock
                    ):
                        continue
                    categories = {
                        director.atom_value(item.value)
                        for item in director.block_assignments(
                            assignment.value, "category"
                        )
                    }
                    if not categories.intersection({"ships", "ship_components"}):
                        continue
                    for child in director.block_assignments(assignment.value):
                        if child.key == "cost":
                            construction.update(_resource_keys(child.value))
                        elif child.key == "upkeep":
                            upkeep.update(_resource_keys(child.value))
                        elif child.key == "logistics":
                            logistics.update(_resource_keys(child.value))
        report[label] = {
            "construction": sorted(construction),
            "upkeep": sorted(upkeep),
            "logistics": sorted(logistics),
            "files_scanned": files_scanned,
            "source_root": str(root),
            "source_sha256": source_digest.hexdigest(),
        }
    return report


def modeled_scenarios() -> list[dict[str, object]]:
    scenarios = [
        (
            "standard_positive_zero_stockpile",
            False,
            {"energy": 200, "alloys": 100, "trade": 100, "minerals": 0},
            {"energy": 20, "alloys": 10, "trade": 10},
            True,
            0.50,
        ),
        (
            "bio_food_pressure",
            True,
            {"energy": 200, "alloys": 100, "trade": 100, "food": 40},
            {"food": 50, "alloys": 10, "trade": 10},
            True,
            0.50,
        ),
        (
            "esc_mineral_component_pressure",
            False,
            {"energy": 200, "alloys": 100, "trade": 100, "minerals": 5},
            {"minerals": 6},
            True,
            0.50,
        ),
        (
            "gigas_sentient_component_pressure",
            False,
            {
                "energy": 200,
                "alloys": 100,
                "trade": 100,
                "giga_sr_sentient_metal": 0,
            },
            {"giga_sr_sentient_metal": 1},
            True,
            0.50,
        ),
        (
            "gigas_exceptional_hull_pressure",
            False,
            {"energy": 2000, "alloys": 2000, "trade": 300, "influence": 1},
            {"alloys": 1500, "trade": 250, "influence": 0.5},
            True,
            0.50,
        ),
        (
            "sft_food_pressure_on_standard_hull",
            False,
            {"energy": 200, "alloys": 100, "trade": 100, "food": 0},
            {"food": 1},
            True,
            0.50,
        ),
        (
            "construction_only_zro_does_not_gate_sustainability",
            False,
            {"energy": 200, "alloys": 100, "trade": 100, "sr_zro": -5},
            {},
            True,
            0.50,
        ),
        (
            "peace_does_not_surge",
            False,
            {"energy": 200, "alloys": 100, "trade": 100},
            {},
            False,
            0.50,
        ),
        (
            "naval_capacity_boundary_does_not_surge",
            False,
            {"energy": 200, "alloys": 100, "trade": 100},
            {},
            True,
            0.90,
        ),
        (
            "war_shock_optional_resource_negative",
            False,
            {"energy": 200, "alloys": 100, "trade": 100, "minerals": -1},
            {},
            True,
            0.50,
        ),
    ]
    rendered: list[dict[str, object]] = []
    for name, biological, monthly_net, tranche, at_war, naval_capacity in scenarios:
        monthly_expenses = (
            {"minerals": 1}
            if name == "war_shock_optional_resource_negative"
            else {}
        )
        decision = evaluate_completion_tranche(
            FleetEconomyState(
                at_war,
                naval_capacity,
                monthly_net,
                monthly_expenses,
            ),
            tranche,
            biological=biological,
        )
        rendered.append(
            {
                "name": name,
                "biological": biological,
                "monthly_net": monthly_net,
                "monthly_expenses": monthly_expenses,
                "tranche_upkeep": tranche,
                "decision": asdict(decision),
            }
        )
    return rendered


def build_report() -> dict[str, object]:
    return {
        "model": "Stellar AI Director fleet recurring-pressure model",
        "policy": {
            "core_positive": list(CORE_POSITIVE_RESOURCES),
            "bio_positive": list(BIO_POSITIVE_RESOURCES),
            "optional_nonnegative": list(OPTIONAL_NONNEGATIVE_RESOURCES),
            "standard_optional_nonnegative": list(
                STANDARD_OPTIONAL_NONNEGATIVE_RESOURCES
            ),
            "stockpile_gate": False,
            "optional_resource_rule": "zero total expense OR positive net income",
            "native_observability_limit": (
                "Country triggers cannot inspect the next auto-design upkeep vector "
                "or committed queue completion tranche."
            ),
        },
        "active_stack_inventory": scan_ship_economy_roots(ACTIVE_SHIP_STACK_ROOTS),
        "scenarios": modeled_scenarios(),
    }


def main() -> int:
    report = build_report()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(REPORT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
