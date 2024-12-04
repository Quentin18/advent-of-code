import re
from collections.abc import Iterator

import numpy as np

PATTERN = "XMAS"


def diagonals(array: np.ndarray) -> Iterator[np.ndarray]:
    for i in range(1, array.shape[1]):
        yield np.diag(array, -i)

    yield np.diag(array, 0)

    for i in range(1, array.shape[0]):
        yield np.diag(array, i)


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = np.array([list(line.strip()) for line in file])

    matches = 0

    for g in (grid, grid.T, diagonals(grid), diagonals(np.fliplr(grid))):
        for line in g:
            matches += len(re.findall(PATTERN, "".join(line))) + len(
                re.findall(PATTERN[::-1], "".join(line))
            )

    print(matches)


if __name__ == "__main__":
    main()
