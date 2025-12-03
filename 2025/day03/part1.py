def main() -> None:
    output = 0

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            bank = line.strip()
            battery1 = max(bank[:-1])
            battery2 = max(bank[bank.index(battery1) + 1 :])
            output += int(battery1 + battery2)

    print(output)


if __name__ == "__main__":
    main()
