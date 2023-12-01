DIGITS = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def main() -> None:
    values = []
    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            digit_start_index_map = {}
            digit_end_index_map = {}

            for digit in DIGITS:
                start_index = line.find(digit)
                if start_index >= 0:
                    digit_start_index_map[digit] = start_index

                end_index = line.rfind(digit)
                if end_index >= 0:
                    digit_end_index_map[digit] = end_index

            first_digit = min(digit_start_index_map, key=digit_start_index_map.get)
            last_digit = max(digit_end_index_map, key=digit_end_index_map.get)
            values.append(int(DIGITS[first_digit] + DIGITS[last_digit]))

    response = sum(values)
    print(response)


if __name__ == "__main__":
    main()
