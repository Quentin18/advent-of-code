from __future__ import annotations

from collections import Counter

CARD_VALUE = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A",
]
HAND_TYPES = [
    "high_card",
    "one_pair",
    "two_pair",
    "three_of_a_kind",
    "full_house",
    "four_of_a_kind",
    "five_of_a_kind",
]


class Hand:
    def __init__(self, cards: str, bid: int) -> None:
        self.cards = cards
        self.bid = bid

        self.cards_counter = Counter(cards)
        self.most_common_cards = self.cards_counter.most_common()
        self.type = self.get_type()
        self.type_score = HAND_TYPES.index(self.type)

    def get_type(self) -> str:
        if self.is_five_of_a_kind():
            return "five_of_a_kind"

        if self.is_four_of_a_kind():
            return "four_of_a_kind"

        if self.is_full_house():
            return "full_house"

        if self.is_three_of_a_kind():
            return "three_of_a_kind"

        if self.is_two_pairs():
            return "two_pair"

        if self.is_one_pair():
            return "one_pair"

        return "high_card"

    def is_five_of_a_kind(self) -> bool:
        return self.most_common_cards[0][1] == 5

    def is_four_of_a_kind(self) -> bool:
        return self.most_common_cards[0][1] == 4 and self.most_common_cards[1][1] == 1

    def is_full_house(self) -> bool:
        return self.most_common_cards[0][1] == 3 and self.most_common_cards[1][1] == 2

    def is_three_of_a_kind(self) -> bool:
        return (
            self.most_common_cards[0][1] == 3
            and self.most_common_cards[1][1] == 1
            and self.most_common_cards[2][1] == 1
        )

    def is_two_pairs(self) -> bool:
        return (
            self.most_common_cards[0][1] == 2
            and self.most_common_cards[1][1] == 2
            and self.most_common_cards[2][1] == 1
        )

    def is_one_pair(self) -> bool:
        return (
            self.most_common_cards[0][1] == 2
            and self.most_common_cards[1][1] == 1
            and self.most_common_cards[2][1] == 1
            and self.most_common_cards[3][1] == 1
        )

    @staticmethod
    def parse(line: str) -> Hand:
        cards, bid = line.split()
        return Hand(cards=cards, bid=int(bid))

    def __gt__(self, other: Hand) -> bool:
        if self.type_score != other.type_score:
            return self.type_score > other.type_score

        for card, other_card in zip(self.cards, other.cards):
            card_value = CARD_VALUE.index(card)
            other_card_value = CARD_VALUE.index(other_card)

            if card_value != other_card_value:
                return card_value > other_card_value

        return False


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        hands = [Hand.parse(line=line) for line in file]

    hands.sort()
    response = sum((i + 1) * hand.bid for i, hand in enumerate(hands))
    print(response)


if __name__ == "__main__":
    main()
