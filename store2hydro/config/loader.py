from pathlib import Path
import yaml


def load_config(path):
    """
    Load a YAML configuration file.

    Parameters
    ----------
    path : str or Path
        Path to YAML file.

    Returns
    -------
    dict
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r") as f:
        config = yaml.safe_load(f)

    return config
