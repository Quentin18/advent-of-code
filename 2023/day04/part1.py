def parse_numbers(numbers_string: str) -> set[int]:
    return set(int(number) for number in numbers_string.strip().split())


def parse_points(line: str) -> int:
    _, numbers = line.split(":")
    winning_numbers, my_numbers = numbers.split("|")
    winning_numbers = parse_numbers(numbers_string=winning_numbers)
    my_numbers = parse_numbers(numbers_string=my_numbers)
    my_winning_numbers = winning_numbers & my_numbers
    points = 2 ** (len(my_winning_numbers) - 1) if my_winning_numbers else 0
    print("points:", points)
    return points


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        response = sum(parse_points(line=line) for line in file)

    print(response)


if __name__ == "__main__":
    main()
