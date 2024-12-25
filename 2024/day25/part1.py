import numpy as np


def schematic_to_heights(schematic: list[str]) -> np.ndarray:
    heights = [0] * len(schematic[0])

    for line in schematic[1:-1]:
        for i, char in enumerate(line):
            if char == "#":
                heights[i] += 1

    return np.array(heights, dtype=int)


def save_schematic(
    schematic: list[str],
    locks: list[np.ndarray],
    keys: list[np.ndarray],
) -> None:
    if schematic[0] == "#" * len(schematic[0]):
        locks.append(schematic_to_heights(schematic))
    elif schematic[-1] == "#" * len(schematic[-1]):
        keys.append(schematic_to_heights(schematic))
    else:
        raise RuntimeError("invalid schematic")


def main() -> None:
    height = None
    locks = []
    keys = []

    with open("input.txt", "r", encoding="utf-8") as file:
        schematic = []

        for line in file:
            line = line.strip()
            if line:
                schematic.append(line)
            else:
                height = len(schematic)
                save_schematic(schematic=schematic, locks=locks, keys=keys)
                schematic = []

        save_schematic(schematic=schematic, locks=locks, keys=keys)

    print(sum(((lock + key) <= height - 2).all() for lock in locks for key in keys))


if __name__ == "__main__":
    main()
