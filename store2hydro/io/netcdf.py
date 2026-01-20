from pathlib import Path
import pypsa


def load_network(nc_path: str | Path) -> pypsa.Network:
    nc_path = Path(nc_path)
    if not nc_path.exists():
        raise FileNotFoundError(f"Network .nc not found: {nc_path}")
    return pypsa.Network(nc_path)


def save_network(n: pypsa.Network, nc_path: str | Path) -> None:
    nc_path = Path(nc_path)
    nc_path.parent.mkdir(parents=True, exist_ok=True)
    n.export_to_netcdf(nc_path)
