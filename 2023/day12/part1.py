def is_valid(conditions: str, sizes: list[int]) -> bool:
    groups = conditions.split(".")
    group_sizes = [len(group) for group in groups if group]
    return group_sizes == sizes


def count_arrangements(record: str) -> int:
    conditions, sizes = record.split()
    sizes = [int(i) for i in sizes.split(",")]

    def count_arrangements_recursive(cond: str) -> int:
        index = cond.find("?")
        if index == -1:
            return int(is_valid(conditions=cond, sizes=sizes))

        return sum(count_arrangements_recursive(cond.replace("?", c, 1)) for c in ".#")

    return count_arrangements_recursive(cond=conditions)


def main() -> None:
    total_arrangements = 0

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            total_arrangements += count_arrangements(record=line)

    print(total_arrangements)


if __name__ == "__main__":
    main()
