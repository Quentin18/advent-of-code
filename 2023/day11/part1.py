import numpy as np
from scipy.spatial.distance import pdist


def expand_universe(universe: np.ndarray) -> np.ndarray:
    # vertical
    expanded_universe_vertical = []
    for row in range(universe.shape[0]):
        line = universe[row, :]
        expanded_universe_vertical.append(line)
        if (line == ".").all():
            expanded_universe_vertical.append(line)

    expanded_universe = np.array(expanded_universe_vertical)

    # horizontal
    expanded_universe_horizontal = []
    for col in range(expanded_universe.shape[1]):
        line = expanded_universe[:, col]
        expanded_universe_horizontal.append(line)
        if (line == ".").all():
            expanded_universe_horizontal.append(line)

    expanded_universe = np.column_stack(expanded_universe_horizontal)

    return expanded_universe


def find_galaxies(universe: np.ndarray) -> np.ndarray:
    return np.argwhere(universe == "#")


def get_sum_length_shortest_path(universe: np.ndarray) -> int:
    galaxies = find_galaxies(universe=universe)
    return int(pdist(galaxies, metric="cityblock").sum())


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = [list(line.strip()) for line in file]

    universe = np.array(lines)
    expanded_universe = expand_universe(universe=universe)
    response = get_sum_length_shortest_path(universe=expanded_universe)
    print(response)


if __name__ == "__main__":
    main()
