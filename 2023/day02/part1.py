COLOR_MAX_NUMBER = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_game(line: str) -> int:
    id_string, subsets_string = line.split(":")
    id_ = int(id_string.replace("Game ", ""))

    for subset in subsets_string.split(";"):
        for number_color in subset.split(","):
            number, color = number_color.strip().split()
            if int(number) > COLOR_MAX_NUMBER[color]:
                print(f"Game {id_} is impossible")
                return 0

    print(f"Game {id_} is possible")
    return id_


def main() -> None:
    possible_ids_sum = 0
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            possible_ids_sum += parse_game(line)
    print(possible_ids_sum)


if __name__ == "__main__":
    main()
