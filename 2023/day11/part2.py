import itertools

import numpy as np

EXPANSION_MULTIPLIER = 100000


def find_galaxies(universe: np.ndarray) -> np.ndarray:
    return np.argwhere(universe == "#")


def get_empty_masks(universe: np.ndarray) -> list[np.ndarray]:
    # return two masks to know if the row or column is empty or not
    return [
        np.apply_along_axis(
            lambda a: (a == ".").all(),
            axis,
            universe,
        )
        for axis in range(2)
    ]


def distance_along_axis(x1: int, x2: int, empty_mask: np.ndarray) -> int:
    start, end = (x1, x2) if x1 < x2 else (x2, x1)
    return sum(EXPANSION_MULTIPLIER if empty_mask[i] else 1 for i in range(start, end))


def distance(g1: np.ndarray, g2: np.ndarray, empty_masks: list[np.ndarray]) -> int:
    # note: the empty mask should be the columns mask for axis 0 (rows)
    # and the rows mask for axis 1 (columns)
    return sum(
        distance_along_axis(x1=g1[i], x2=g2[i], empty_mask=empty_masks[::-1][i])
        for i in range(2)
    )


def get_sum_length_shortest_path(universe: np.ndarray) -> int:
    galaxies = find_galaxies(universe=universe)
    empty_masks = get_empty_masks(universe=universe)
    return sum(
        distance(g1=g1, g2=g2, empty_masks=empty_masks)
        for g1, g2 in itertools.combinations(galaxies, 2)
    )


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = [list(line.strip()) for line in file]

    universe = np.array(lines)
    response = get_sum_length_shortest_path(universe=universe)
    print(response)


if __name__ == "__main__":
    main()
