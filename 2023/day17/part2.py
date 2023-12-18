from __future__ import annotations

import sys
from collections import defaultdict
from enum import Enum
from typing import Iterator, NamedTuple

import numpy as np

INF = sys.maxsize


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def opposite(self) -> Direction:
        opposite_direction_map = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposite_direction_map[self]


class Node(NamedTuple):
    row: int
    col: int
    direction: Direction | None = None
    consecutive_blocks: int = 0

    @property
    def pos(self) -> tuple[int, int]:
        return self.row, self.col

    def _get_next_row_col(self, direction: Direction) -> tuple[int, int]:
        direction_delta = {
            Direction.UP: (-1, 0),
            Direction.DOWN: (1, 0),
            Direction.LEFT: (0, -1),
            Direction.RIGHT: (0, 1),
        }
        row_delta, col_delta = direction_delta[direction]
        return self.row + row_delta, self.col + col_delta

    @staticmethod
    def _is_inside(row: int, col: int, n_rows: int, n_cols: int) -> bool:
        return 0 <= row < n_rows and 0 <= col < n_cols

    def iterate_neighbors(self, n_rows: int, n_cols: int) -> Iterator[Node]:
        for direction in Direction:
            if self.direction is not None and direction == self.direction.opposite():
                continue

            if self.direction is not None and (
                (direction != self.direction and self.consecutive_blocks < 4)
                or (direction == self.direction and self.consecutive_blocks >= 10)
            ):
                continue

            row, col = self._get_next_row_col(direction=direction)
            if not self._is_inside(row=row, col=col, n_rows=n_rows, n_cols=n_cols):
                continue

            consecutive_blocks = (
                1 if direction != self.direction else self.consecutive_blocks + 1
            )
            yield Node(
                row=row,
                col=col,
                direction=direction,
                consecutive_blocks=consecutive_blocks,
            )


def dijkstra_shortest_dist(
    start: tuple[int, int],
    goal: tuple[int, int],
    grid: np.ndarray,
) -> int:
    n_rows, n_cols = grid.shape
    start_node = Node(row=start[0], col=start[1])
    open_set = {start_node}
    dist = defaultdict(lambda: INF)
    dist[start_node] = 0

    while open_set:
        current = min(open_set, key=lambda key: dist[key])
        open_set.remove(current)
        for neighbor in current.iterate_neighbors(n_rows=n_rows, n_cols=n_cols):
            if neighbor not in dist:
                open_set.add(neighbor)
                dist[neighbor] = dist[current] + grid[neighbor.row, neighbor.col]

    return min(
        distance
        for node, distance in dist.items()
        if node.pos == goal and node.consecutive_blocks >= 4
    )


def minimum_heat_loss(grid: np.ndarray) -> int:
    return dijkstra_shortest_dist(
        start=(0, 0),
        goal=(grid.shape[0] - 1, grid.shape[1] - 1),
        grid=grid,
    )


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = np.array([[int(i) for i in line.strip()] for line in file], dtype=int)

    print(minimum_heat_loss(grid=grid))


if __name__ == "__main__":
    main()
