import sys

import numpy as np

NUMBER_CYCLES = 1000000000


def slide_rocks_north(platform: np.ndarray) -> None:
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


def slide_rocks_west(platform: np.ndarray) -> None:
    slide_rocks_north(platform=platform.T)


def slide_rocks_south(platform: np.ndarray) -> None:
    slide_rocks_north(platform=np.flipud(platform))


def slide_rocks_east(platform: np.ndarray) -> None:
    slide_rocks_north(platform=np.flipud(platform.T))


def platform_to_string(platform: np.ndarray) -> str:
    return "".join("".join(line) for line in platform)


def apply_cycles(platform: np.ndarray) -> np.ndarray:
    platform_str = platform_to_string(platform=platform)
    visited = {platform_str: 0}
    history = [platform.copy()]

    for i in range(1, NUMBER_CYCLES + 1):
        slide_rocks_north(platform=platform)
        slide_rocks_west(platform=platform)
        slide_rocks_south(platform=platform)
        slide_rocks_east(platform=platform)

        platform_str = platform_to_string(platform=platform)
        if platform_str in visited:
            print(f"already visited after {i} iterations", file=sys.stderr)
            start_cycle_index = visited[platform_str]
            cycle_length = i - start_cycle_index
            return history[start_cycle_index + (NUMBER_CYCLES - i) % cycle_length]

        visited[platform_str] = i
        history.append(platform.copy())

    return platform


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
    platform = apply_cycles(platform=platform)
    print(platform, file=sys.stderr)
    load = count_load(platform=platform)
    print(load)


if __name__ == "__main__":
    main()
