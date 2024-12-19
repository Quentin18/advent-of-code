import networkx as nx

HEIGHT = 71  # 7
WIDTH = 71  # 7
BYTES_COUNT = 1024  # 12


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        byte_positions = [tuple(map(int, line.strip().split(","))) for line in file]

    graph = nx.Graph()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            source = (x, y)
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                target = (x + dx, y + dy)
                if 0 <= target[0] < WIDTH and 0 <= target[1] < HEIGHT:
                    graph.add_edge(source, target)

    i = 0

    while nx.has_path(graph, source=(0, 0), target=(WIDTH - 1, HEIGHT - 1)):
        graph.remove_node(byte_positions[i])
        i += 1

    print(",".join(str(j) for j in byte_positions[i - 1]))


if __name__ == "__main__":
    main()