def add_pumping_placeholder(network, zone, total_capacity):
    """
    Placeholder for zonal pumping retrofit capacity.

    In the planning model, pumping is zonal and aggregated.

    Parameters
    ----------
    network : pypsa.Network
    zone : str
        Planning zone.
    total_capacity : float
        Pumping capacity (MW).
    """
    network.add(
        "Link",
        f"{zone}_pump",
        bus0=zone,
        bus1=zone,
        p_nom=total_capacity,
        efficiency=0.9,
    )
