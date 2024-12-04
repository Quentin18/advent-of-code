import numpy as np


def check_xmas(array: np.ndarray) -> bool:
    assert array.shape == (3, 3), array.shape
    return "".join(array.diagonal()) in ("MAS", "SAM") and "".join(
        np.fliplr(array).diagonal()
    ) in ("MAS", "SAM")


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = np.array([list(line.strip()) for line in file])

    matches = 0

    for i in range(grid.shape[0] - 2):
        for j in range(grid.shape[1] - 2):
            matches += check_xmas(grid[i : i + 3, j : j + 3])

    print(matches)


if __name__ == "__main__":
    main()
