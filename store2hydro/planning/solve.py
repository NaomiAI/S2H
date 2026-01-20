from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import pypsa


@dataclass
class PlanningOutputs:
    zonal_investments: pd.DataFrame


def _ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def select_zone_buses(n: pypsa.Network, cfg: dict) -> list[str]:
    """
    Decide which buses count as 'zones' for zonal pumping retrofits.
    By default: use cfg["zones"] if given, otherwise all buses in the network.
    """
    zones = cfg.get("zones")
    if zones:
        missing = [z for z in zones if z not in n.buses.index]
        if missing:
            raise ValueError(
                "Some configured zones are not buses in the planning network: "
                + ", ".join(missing)
            )
        return list(zones)
    return list(n.buses.index)


def add_pumping_retrofit_storageunits(n: pypsa.Network, cfg: dict) -> list[str]:
    """
    Add one extendable StorageUnit per zone bus to represent retrofit pumping capacity.
    This is intentionally 'zonal' and technology-agnostic.

    Investment variable: p_nom (MW)
    Energy capacity: max_hours * p_nom (MWh)
    """
    tech = cfg["pumping_retrofit"]
    zones = select_zone_buses(n, cfg)

    names = []
    for z in zones:
        name = f"pump_retrofit__{z}"
        if name in n.storage_units.index:
            continue

        n.add(
            "StorageUnit",
            name,
            bus=z,
            p_nom_extendable=True,
            p_nom_min=float(tech.get("p_nom_min_mw", 0.0)),
            p_nom_max=float(tech.get("p_nom_max_mw", float("inf"))),
            max_hours=float(tech.get("max_hours", 6.0)),
            efficiency_store=float(tech.get("efficiency_store", 0.9)),
            efficiency_dispatch=float(tech.get("efficiency_dispatch", 0.9)),
            marginal_cost=float(tech.get("marginal_cost", 0.0)),
            capital_cost=float(tech.get("capital_cost_eur_per_mw_year", 0.0)),
            cyclic_state_of_charge=bool(tech.get("cyclic_soc", False)),
        )
        names.append(name)

    return names


def apply_overlays(n: pypsa.Network, cfg: dict) -> None:
    """
    Hook for optional system-wide constraints or parameter overrides.
    Keep it minimal now; extend later as needed.
    """
    # Example: enforce a global CO2 cap if the network has carriers/emissions
    # (only applies if you already model emissions in your network)
    co2_cap = cfg.get("constraints", {}).get("co2_cap", None)
    if co2_cap is not None:
        n.add("GlobalConstraint", "CO2Limit", type="primary_energy", carrier_attribute="co2_emissions", sense="<=", constant=float(co2_cap))


def solve_planning(n: pypsa.Network, cfg: dict) -> None:
    solver_name = cfg.get("solver", {}).get("name", "highs")
    solver_opts = cfg.get("solver", {}).get("options", {}) or {}

    # PyPSA optimization call
    n.optimize(solver_name=solver_name, solver_options=solver_opts)


def extract_zonal_investments(n: pypsa.Network, retrofit_names: list[str]) -> pd.DataFrame:
    """
    Returns a tidy table: zone, p_nom_opt_mw, e_nom_opt_mwh (derived from max_hours).
    """
    rows = []
    for name in retrofit_names:
        su = n.storage_units.loc[name]
        zone = su["bus"]
        p_opt = float(su.get("p_nom_opt", su.get("p_nom", 0.0)))
        max_hours = float(su.get("max_hours", 0.0))
        e_opt = p_opt * max_hours
        rows.append(
            {
                "zone": zone,
                "asset": name,
                "p_nom_opt_mw": p_opt,
                "max_hours": max_hours,
                "e_nom_opt_mwh": e_opt,
            }
        )
    return pd.DataFrame(rows).sort_values(["zone", "asset"]).reset_index(drop=True)


def run_step1_planning(n: pypsa.Network, cfg: dict, out_dir: str | Path) -> PlanningOutputs:
    out_dir = _ensure_dir(out_dir)

    apply_overlays(n, cfg)
    retrofit_names = add_pumping_retrofit_storageunits(n, cfg)
    solve_planning(n, cfg)

    inv = extract_zonal_investments(n, retrofit_names)
    inv.to_csv(out_dir / "zonal_investments.csv", index=False)

    return PlanningOutputs(zonal_investments=inv)
