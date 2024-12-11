import math


def get_next_stones(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    digits = int(math.log10(stone)) + 1
    if digits % 2 == 0:
        return [int(str(stone)[: digits // 2]), int(str(stone)[digits // 2 :])]

    return [stone * 2024]


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        stones = list(map(int, file.read().strip().split()))

    for _ in range(25):
        next_stones = []

        for stone in stones:
            next_stones.extend(get_next_stones(stone))

        stones = next_stones

    print(len(stones))


if __name__ == "__main__":
    main()
