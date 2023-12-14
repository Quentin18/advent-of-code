import sys

import numpy as np


def slide_rocks(platform: np.ndarray) -> None:
    for col in range(platform.shape[1]):
        for row in range(platform.shape[0]):
            if platform[row, col] != "O":
                continue

            next_row = row
            while next_row > 0 and platform[next_row - 1, col] == ".":
                next_row -= 1

            if row != next_row:
                platform[next_row, col] = "O"
                platform[row, col] = "."


def count_load(platform: np.ndarray) -> int:
    return sum(
        (platform.shape[0] - row) * (platform[row, :] == "O").sum()
        for row in range(platform.shape[0])
    )


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        platform = [list(line.strip()) for line in file]

    platform = np.array(platform)
    print(platform, file=sys.stderr)
    slide_rocks(platform=platform)
    print(platform, file=sys.stderr)
    load = count_load(platform=platform)
    print(load)


if __name__ == "__main__":
    main()
