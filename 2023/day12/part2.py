from functools import cache

NUMBER_COPIES = 5


def count_arrangements(record: str) -> int:
    conditions, sizes = record.split()
    sizes = [int(i) for i in sizes.split(",")]

    conditions = "?".join([conditions] * NUMBER_COPIES)
    sizes = tuple(sizes * NUMBER_COPIES)

    @cache
    def count_arrangements_recursive(
        condition_index: int,
        size_index: int,
        expected_sharps: int,
    ) -> int:
        if condition_index >= len(conditions) or size_index >= len(sizes):
            return expected_sharps <= 0 and size_index == len(sizes) - 1

        char = conditions[condition_index]
        count = 0

        if char in ".?":
            if expected_sharps <= 0:
                count += count_arrangements_recursive(
                    condition_index=condition_index + 1,
                    size_index=size_index,
                    expected_sharps=-1,
                )

        if char in "#?":
            if expected_sharps == -1:
                count += count_arrangements_recursive(
                    condition_index=condition_index + 1,
                    size_index=size_index + 1,
                    expected_sharps=sizes[size_index + 1] - 1
                    if size_index + 1 < len(sizes)
                    else -1,
                )
            elif expected_sharps >= 1:
                count += count_arrangements_recursive(
                    condition_index=condition_index + 1,
                    size_index=size_index,
                    expected_sharps=expected_sharps - 1,
                )

        return count

    return count_arrangements_recursive(
        condition_index=0,
        size_index=-1,
        expected_sharps=-1,
    )


def main() -> None:
    total_arrangements = 0

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            total_arrangements += count_arrangements(record=line)

    print(total_arrangements)


if __name__ == "__main__":
    main()
