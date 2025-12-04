def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [list(line.strip()) for line in file]

    output = 0
    removed = 1

    while removed > 0:
        removed = 0

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] != "@":
                    continue

                rolls = 0
                for dx, dy in [
                    (-1, 0),
                    (-1, -1),
                    (0, -1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                    (0, 1),
                    (-1, 1),
                ]:
                    if (
                        0 <= x + dx < len(grid[y])
                        and 0 <= y + dy < len(grid)
                        and grid[y + dy][x + dx] == "@"
                    ):
                        rolls += 1

                if rolls < 4:
                    output += 1
                    removed += 1
                    grid[y][x] = "."

    print(output)


if __name__ == "__main__":
    main()
