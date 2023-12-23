def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        calories = 0
        calories_list = []

        for line in file:
            line = line.strip()
            if not line:
                calories_list.append(calories)
                calories = 0
            else:
                calories += int(line)

    print(sum(sorted(calories_list, reverse=True)[:3]))


if __name__ == "__main__":
    main()
