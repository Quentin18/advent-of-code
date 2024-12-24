import sys

DIR_KEYPAD_ROBOTS = 25
DIR_KEYPAD = {
    " ": (0, 0),
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}
NUM_KEYPAD = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    " ": (0, 3),
    "0": (1, 3),
    "A": (2, 3),
}


def key_path_cost(
    cache: dict[tuple[int, str, str], int],
    robot: int,
    key_start: str,
    key_end: str,
) -> int:
    return 1 if robot == 0 else cache[(robot, key_start, key_end)]


def key_sequence_cost(
    cache: dict[tuple[int, str, str], int],
    robot: int,
    key_sequence: str,
) -> int:
    key_start = "A"
    cost = 0
    for key_end in key_sequence:
        cost += key_path_cost(
            cache=cache,
            robot=robot,
            key_start=key_start,
            key_end=key_end,
        )
        key_start = key_end
    return cost


def cache_robot(
    cache: dict[tuple[int, str, str], int],
    robot: int,
    keypad: dict[str, tuple[int, int]],
) -> None:
    for key_start, (x_start, y_start) in keypad.items():
        for key_end, (x_end, y_end) in keypad.items():
            horizontal_dist = abs(x_end - x_start)
            vertical_dist = abs(y_end - y_start)

            horizontal_keys = (">" if x_end > x_start else "<") * horizontal_dist
            vertical_keys = ("^" if y_end < y_start else "v") * vertical_dist

            horizontal_key_seq = f"{horizontal_keys}{vertical_keys}A"
            vertical_key_seq = f"{vertical_keys}{horizontal_keys}A"

            min_horizontal = (
                key_sequence_cost(
                    cache=cache,
                    robot=robot - 1,
                    key_sequence=horizontal_key_seq,
                )
                if (x_end, y_start) != keypad[" "]
                else sys.maxsize
            )
            min_vertical = (
                key_sequence_cost(
                    cache=cache,
                    robot=robot - 1,
                    key_sequence=vertical_key_seq,
                )
                if (x_start, y_end) != keypad[" "]
                else sys.maxsize
            )

            cache[(robot, key_start, key_end)] = min(min_horizontal, min_vertical)


def cache_robots() -> dict[tuple[int, str, str], int]:
    cache = {}

    for robot in range(DIR_KEYPAD_ROBOTS):
        cache_robot(cache=cache, robot=robot + 1, keypad=DIR_KEYPAD)

    cache_robot(cache=cache, robot=DIR_KEYPAD_ROBOTS + 1, keypad=NUM_KEYPAD)

    return cache


def get_complexity(code: str, sequence_length: int) -> int:
    return sequence_length * int("".join(char for char in code if char.isdigit()))


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        codes = [line.strip() for line in file]

    cache = cache_robots()

    complexity = 0

    for code in codes:
        sequence_length = key_sequence_cost(
            cache=cache,
            robot=DIR_KEYPAD_ROBOTS + 1,
            key_sequence=code,
        )
        print(code, sequence_length, file=sys.stderr)
        complexity += get_complexity(code=code, sequence_length=sequence_length)

    print(complexity)


if __name__ == "__main__":
    main()
