import networkx as nx
from tqdm import tqdm


def distance(source: tuple[int, int], target: tuple[int, int]) -> int:
    return abs(source[0] - target[0]) + abs(source[1] - target[1])


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

    start = end = None
    graph = nx.Graph()

    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            node = (x, y)

            if char == "#":
                continue

            if char == "S":
                start = node
            elif char == "E":
                end = node

            graph.add_node(node)
            add_edges(graph=graph, source=node, grid=grid)

    dist_from_start = nx.single_source_shortest_path_length(graph, start)
    dist_from_end = nx.single_source_shortest_path_length(graph, end)
    cheats = 0

    for cheat_start in tqdm(dist_from_start, desc="Searching for cheats"):
        for cheat_end in dist_from_end:
            if cheat_start == cheat_end:
                continue

            cheat_length = distance(cheat_start, cheat_end)
            if cheat_length > 20:
                continue

            saved_time = dist_from_start[end] - (
                dist_from_start[cheat_start] + cheat_length + dist_from_end[cheat_end]
            )

            if saved_time >= 100:
                cheats += 1

    print(cheats)


if __name__ == "__main__":
    main()
