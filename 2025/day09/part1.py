def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        tiles = [list(map(int, line.strip().split(","))) for line in file]

    area = 0

    for i in range(len(tiles) - 1):
        for j in range(i + 1, len(tiles)):
            area = max(
                area,
                abs(tiles[i][0] - tiles[j][0] + 1) * abs(tiles[i][1] - tiles[j][1] + 1),
            )

    print(area)


if __name__ == "__main__":
    main()
