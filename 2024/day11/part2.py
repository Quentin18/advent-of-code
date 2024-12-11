import math
from functools import cache


def get_next_stones(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    digits = int(math.log10(stone)) + 1
    if digits % 2 == 0:
        return [int(str(stone)[: digits // 2]), int(str(stone)[digits // 2 :])]

    return [stone * 2024]


@cache
def count_stones(stone: int, n: int) -> int:
    if n == 0:
        return 1
    return sum(count_stones(s, n - 1) for s in get_next_stones(stone))


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        stones = list(map(int, file.read().strip().split()))

    print(sum(count_stones(stone, 75) for stone in stones))


if __name__ == "__main__":
    main()
