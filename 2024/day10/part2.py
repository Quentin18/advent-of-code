def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        topographic_map = [list(map(int, line.strip())) for line in file]

    height, width = len(topographic_map), len(topographic_map[0])
    trail_heads = [
        (i, j)
        for i in range(height)
        for j in range(width)
        if topographic_map[i][j] == 0
    ]

    def count_paths(node: tuple[int, int]) -> int:
        value = topographic_map[node[0]][node[1]]
        if value == 9:
            return 1

        return sum(
            count_paths(neighbor)
            for neighbor in (
                (node[0] - 1, node[1]),
                (node[0], node[1] + 1),
                (node[0] + 1, node[1]),
                (node[0], node[1] - 1),
            )
            if (
                0 <= neighbor[0] < height
                and 0 <= neighbor[1] < width
                and topographic_map[neighbor[0]][neighbor[1]] == value + 1
            )
        )

    print(sum(count_paths(trail_head) for trail_head in trail_heads))


if __name__ == "__main__":
    main()
