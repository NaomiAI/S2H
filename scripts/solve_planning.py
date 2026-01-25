from pathlib import Path

from store2hydro.config.loader import load_config
from store2hydro.io.netcdf import load_network, save_network
from store2hydro.planning.solve import run_step1_planning, apply_time_subset


def main():
    cfg = load_config("configs/planning.yaml")

    planning_nc = Path(cfg["inputs"]["planning_network_nc"])
    out_dir = Path(cfg.get("outputs", {}).get("planning_dir", "results/planning"))

    n = load_network(planning_nc)

    # Optional testing hook: reduce snapshots via config
    n = apply_time_subset(n, cfg)
    print(f"Running planning model with {len(n.snapshots)} snapshots")

    outputs = run_step1_planning(n, cfg, out_dir=out_dir)

    # optional: save solved network
    solved_nc = cfg.get("outputs", {}).get("planning_solved_nc")
    if solved_nc:
        save_network(n, solved_nc)

    print("Wrote:", out_dir / "zonal_investments.csv")
    print(outputs.zonal_investments.head())


if __name__ == "__main__":
    main()