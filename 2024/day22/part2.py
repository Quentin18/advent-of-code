from collections import deque


def get_next_secret_number(secret_number: int) -> int:
    secret_number = ((secret_number * 64) ^ secret_number) % 16777216
    secret_number = ((secret_number // 32) ^ secret_number) % 16777216
    return ((secret_number * 2048) ^ secret_number) % 16777216


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        secret_numbers = [int(line.strip()) for line in file]

    secret_number_instructions_price = []

    for secret_number in secret_numbers:
        price = secret_number % 10
        changes = deque(maxlen=4)
        instructions_price = {}

        for _ in range(2000):
            next_secret_number = get_next_secret_number(secret_number)
            next_price = next_secret_number % 10
            changes.append(next_price - price)
            instructions = tuple(changes)
            if len(instructions) == 4 and instructions not in instructions_price:
                instructions_price[instructions] = next_price

            secret_number = next_secret_number
            price = next_price

        secret_number_instructions_price.append(instructions_price)

    best_price = -1

    for instructions in set().union(*secret_number_instructions_price):
        price = sum(
            instructions_price.get(instructions, 0)
            for instructions_price in secret_number_instructions_price
        )
        best_price = max(best_price, price)

    print(best_price)


if __name__ == "__main__":
    main()
