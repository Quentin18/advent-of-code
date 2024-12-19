from functools import cache


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        available_patterns = set(next(file).strip().split(", "))
        next(file)
        designs = [line.strip() for line in file]

    @cache
    def get_number_of_arrangements(design: str) -> int:
        arrangements = 0

        for pattern in available_patterns:
            if design == pattern:
                arrangements += 1

            if design.startswith(pattern):
                arrangements += get_number_of_arrangements(design[len(pattern) :])

        return arrangements

    print(sum(get_number_of_arrangements(design) for design in designs))


if __name__ == "__main__":
    main()
