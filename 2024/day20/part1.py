import networkx as nx
from tqdm import tqdm


def add_edges(
    graph: nx.Graph,
    source: tuple[int, int],
    grid: list[str],
) -> None:
    x, y = source
    height, width = len(grid), len(grid[0])
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if 0 <= x + dx < width and 0 <= y + dy < height and grid[y + dy][x + dx] != "#":
            graph.add_edge((x, y), (x + dx, y + dy))


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [line.strip() for line in file]

    walls = []
    start = end = None
    graph = nx.Graph()

    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            node = (x, y)

            if char == "#":
                walls.append(node)
                continue

            if char == "S":
                start = node
            elif char == "E":
                end = node

            add_edges(graph=graph, source=node, grid=grid)

    shortest_path_length = nx.shortest_path_length(graph, start, end)
    cheats = 0

    for x, y in tqdm(walls, desc="Searching for cheats"):
        node = (x, y)
        add_edges(graph=graph, source=node, grid=grid)

        if not graph.has_node(node):
            continue

        saved_time = shortest_path_length - nx.shortest_path_length(graph, start, end)
        if saved_time >= 100:
            cheats += 1

        graph.remove_node(node)

    print(cheats)


if __name__ == "__main__":
    main()
