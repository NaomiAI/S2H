from store2hydro.config.loader import load_config
from store2hydro.networks.planning import build_planning_network


def main():
    config = load_config("configs/planning.yaml")
    network = build_planning_network(config)
    print(network)


if __name__ == "__main__":
    main()
