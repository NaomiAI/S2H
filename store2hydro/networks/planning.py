import pypsa
import pandas as pd


def build_planning_network(config):
    """
    Build the 37-node planning network.

    This function only constructs the network structure.
    Solving is handled elsewhere.

    Parameters
    ----------
    config : dict
        Planning model configuration.

    Returns
    -------
    pypsa.Network
    """
    n = pypsa.Network()

    # --- Time index ---
    snapshots = pd.date_range(
        start=config["time"]["start"],
        end=config["time"]["end"],
        freq=config["time"]["resolution"],
        inclusive="left",
    )
    n.set_snapshots(snapshots)

    # --- Buses (zones) ---
    for zone in config["zones"]:
        n.add("Bus", zone)

    return n
