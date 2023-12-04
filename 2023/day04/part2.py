from collections import defaultdict


def parse_numbers(numbers_string: str) -> set[int]:
    return set(int(number) for number in numbers_string.strip().split())


def update_cards_count_map(
    line: str,
    cards_count_map: dict[int, int],
) -> None:
    card, numbers = line.split(":")

    card_number = int(card.replace("Card ", ""))
    cards_count_map[card_number] += 1

    winning_numbers, my_numbers = numbers.split("|")
    winning_numbers = parse_numbers(numbers_string=winning_numbers)
    my_numbers = parse_numbers(numbers_string=my_numbers)
    my_winning_numbers = winning_numbers & my_numbers

    for number in range(card_number + 1, card_number + 1 + len(my_winning_numbers)):
        cards_count_map[number] += cards_count_map[card_number]


def main() -> None:
    cards_count_map = defaultdict(lambda: 0)

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            update_cards_count_map(
                line=line,
                cards_count_map=cards_count_map,
            )

    response = sum(cards_count_map.values())
    print(response)


if __name__ == "__main__":
    main()
