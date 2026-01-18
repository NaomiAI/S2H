def add_reservoir(
    network,
    bus,
    name,
    energy_capacity,
    turbine_capacity,
    inflow=None,
):
    """
    Add a hydro reservoir with turbine to the network.

    Parameters
    ----------
    network : pypsa.Network
    bus : str
        Bus where the reservoir is connected.
    name : str
        Reservoir name.
    energy_capacity : float
        Reservoir energy capacity (MWh).
    turbine_capacity : float
        Turbine power capacity (MW).
    inflow : pd.Series, optional
        Natural inflow time series.
    """
    network.add(
        "Store",
        name,
        bus=bus,
        e_nom=energy_capacity,
        e_cyclic=False,
        e_initial=0.5 * energy_capacity,
    )

    network.add(
        "Link",
        f"{name}_turbine",
        bus0=bus,
        bus1=bus,
        p_nom=turbine_capacity,
        efficiency=1.0,
    )
