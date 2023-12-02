def parse_game(line: str) -> int:
    id_string, subsets_string = line.split(":")
    id_ = int(id_string.replace("Game ", ""))

    color_max_number = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }

    for subset in subsets_string.split(";"):
        for number_color in subset.split(","):
            number, color = number_color.strip().split()
            if int(number) > color_max_number[color]:
                color_max_number[color] = int(number)

    power = color_max_number["red"] * color_max_number["green"] * color_max_number["blue"]
    print(f"Game {id_} has power {power}")
    return power


def main() -> None:
    power_sum = 0
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            power_sum += parse_game(line)
    print(power_sum)


if __name__ == "__main__":
    main()
