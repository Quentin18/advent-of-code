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

    score = 0

    for trail_head in trail_heads:
        current_nodes = {trail_head}
        trail_head_score = 0

        while current_nodes:
            next_nodes = set()

            for node in current_nodes:
                value = topographic_map[node[0]][node[1]]
                if value == 9:
                    trail_head_score += 1
                    continue

                for neighbor in (
                    (node[0] - 1, node[1]),
                    (node[0], node[1] + 1),
                    (node[0] + 1, node[1]),
                    (node[0], node[1] - 1),
                ):
                    if (
                        0 <= neighbor[0] < height
                        and 0 <= neighbor[1] < width
                        and topographic_map[neighbor[0]][neighbor[1]] == value + 1
                    ):
                        next_nodes.add(neighbor)

            current_nodes = next_nodes

        score += trail_head_score

    print(score)


if __name__ == "__main__":
    main()
