def get_next_secret_number(secret_number: int) -> int:
    secret_number = ((secret_number * 64) ^ secret_number) % 16777216
    secret_number = ((secret_number // 32) ^ secret_number) % 16777216
    return ((secret_number * 2048) ^ secret_number) % 16777216


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        secret_numbers = [int(line.strip()) for line in file]

    for _ in range(2000):
        for i, secret_number in enumerate(secret_numbers):
            secret_numbers[i] = get_next_secret_number(secret_number)

    print(sum(secret_numbers))


if __name__ == "__main__":
    main()
