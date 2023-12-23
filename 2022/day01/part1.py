def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        calories = 0
        max_calories = 0

        for line in file:
            line = line.strip()
            if not line:
                max_calories = max(calories, max_calories)
                calories = 0
            else:
                calories += int(line)

    print(max_calories)


if __name__ == "__main__":
    main()
