def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        ranges = []
        ids = []

        for line in file:
            line = line.strip()
            if "-" in line:
                ranges.append(tuple(map(int, line.split("-"))))
            elif line:
                ids.append(int(line))

    output = sum(
        any(
            range_start <= ingredient_id <= range_end
            for range_start, range_end in ranges
        )
        for ingredient_id in ids
    )
    print(output)


if __name__ == "__main__":
    main()
