def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        ranges = []

        for line in file:
            line = line.strip()
            if "-" in line:
                ranges.append(tuple(map(int, line.split("-"))))

    ranges.sort()

    output = 0
    start, end = ranges[0]
    for i in range(1, len(ranges)):
        if end < ranges[i][0]:
            output += end - start + 1
            start, end = ranges[i]
        else:
            end = max(end, ranges[i][1])

    output += end - start + 1

    print(output)


if __name__ == "__main__":
    main()
