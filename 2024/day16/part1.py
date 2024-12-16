import networkx as nx

DIRECTIONS = "NESW"
DELTA = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        maze = [line.strip() for line in file]

    graph = nx.Graph()

    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if char == "#":
                continue

            for i, direction in enumerate(DIRECTIONS):
                # forward
                dy, dx = DELTA[direction]
                if maze[row + dy][col + dx] != "#":
                    graph.add_edge(
                        (row, col, direction),
                        (row + dy, col + dx, direction),
                        weight=1,
                    )

                # rotate clockwise
                graph.add_edge(
                    (row, col, direction),
                    (row, col, DIRECTIONS[(i + 1) % len(DIRECTIONS)]),
                    weight=1000,
                )

                # rotate counterclockwise
                graph.add_edge(
                    (row, col, direction),
                    (row, col, DIRECTIONS[i - 1]),
                    weight=1000,
                )

    shortest_path = nx.shortest_path(
        graph,
        source=(len(maze) - 2, 1, "E"),
        target=(1, len(maze[0]) - 2, "N"),
        weight="weight",
    )
    print(nx.path_weight(graph, path=shortest_path, weight="weight"))


if __name__ == "__main__":
    main()
