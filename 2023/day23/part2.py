import sys
from typing import Iterator, NamedTuple

import networkx as nx


class Path(NamedTuple):
    current: tuple[int, int]
    visited: set[tuple[int, int]]
    weight: int

    def is_done(self, end: tuple[int, int]) -> bool:
        return self.current == end


def iterate_neighbors(
    position: tuple[int, int],
    grid: list[str],
) -> Iterator[tuple[int, int]]:
    row, col = position

    n_rows = len(grid)
    n_cols = len(grid[0])

    for r, c in (
        (row - 1, col),
        (row, col + 1),
        (row + 1, col),
        (row, col - 1),
    ):
        if 0 <= r < n_rows and 0 <= c < n_cols and grid[r][c] != "#":
            yield r, c


def find_next_crossroads(
    grid: list[str],
    crossroad: tuple[int, int],
    graph: nx.Graph,
) -> set[tuple[int, int]]:
    next_crossroads = set()

    for current in iterate_neighbors(position=crossroad, grid=grid):
        visited = {crossroad, current}
        while True:
            neighbors = [
                neighbor
                for neighbor in iterate_neighbors(position=current, grid=grid)
                if neighbor not in visited
            ]
            if len(neighbors) != 1:
                break
            current = neighbors[0]
            visited.add(current)

        if not graph.has_edge(crossroad, current):
            graph.add_edge(crossroad, current, weight=len(visited) - 1)
        next_crossroads.add(current)

    return next_crossroads


def construct_graph(grid: list[str], start: tuple[int, int]) -> nx.Graph:
    graph = nx.Graph()
    crossroads = {start}
    visited_cross_roads = set()

    while crossroads:
        crossroad = crossroads.pop()
        visited_cross_roads.add(crossroad)
        crossroads.update(
            crossroad
            for crossroad in find_next_crossroads(
                grid=grid,
                crossroad=crossroad,
                graph=graph,
            )
            if crossroad not in visited_cross_roads
        )

    return graph


def calculate_length(graph: nx.Graph, path: list[tuple[int, int]]) -> int:
    length = 0

    for u, v in zip(path[:-1], path[1:]):
        edge_data = graph.get_edge_data(u, v)
        length += edge_data["weight"]

    return length


def find_max_length(
    graph: nx.Graph,
    start: tuple[int, int],
    end: tuple[int, int],
) -> int:
    return max(
        calculate_length(graph=graph, path=path)
        for path in nx.all_simple_paths(graph, start, end)
    )


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [line.strip() for line in file]

    start = (0, grid[0].index("."))
    end = (len(grid) - 1, grid[-1].index("."))
    print(f"{start=}, {end=}", file=sys.stderr)

    graph = construct_graph(grid=grid, start=start)
    print(graph, file=sys.stderr)

    print(find_max_length(graph=graph, start=start, end=end))


if __name__ == "__main__":
    main()
