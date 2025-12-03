DIGITS = 12


def main() -> None:
    output = 0

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            bank = line.strip()
            batteries = ""
            min_index = 0

            for i in range(DIGITS):
                battery = max(bank[min_index : len(bank) - DIGITS + i + 1])
                batteries += battery
                min_index = bank.index(battery, min_index) + 1

            output += int(batteries)

    print(output)


if __name__ == "__main__":
    main()
