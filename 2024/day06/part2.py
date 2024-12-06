from __future__ import annotations

import sys
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def next_direction(self) -> Direction:
        match self:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP
            case Direction.RIGHT:
                return Direction.DOWN

    def vector(self) -> tuple[int, int]:
        match self:
            case Direction.UP:
                return 0, -1
            case Direction.DOWN:
                return 0, 1
            case Direction.LEFT:
                return -1, 0
            case Direction.RIGHT:
                return 1, 0


def leave_area(
    grid: list[list[str]],
    position: tuple[int, int],
    direction: Direction,
) -> bool:
    height, width = len(grid), len(grid[0])
    vector = direction.vector()
    visited = {(position, direction)}

    while True:
        next_position = (position[0] + vector[0], position[1] + vector[1])

        if not (0 <= next_position[0] < width and 0 <= next_position[1] < height):
            return True

        if grid[next_position[1]][next_position[0]] == "#":
            direction = direction.next_direction()
            vector = direction.vector()
        elif (next_position, direction) in visited:
            return False
        else:
            position = next_position

        visited.add((position, direction))


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [list(line.strip()) for line in file]

    height = len(grid)
    width = len(grid[0])

    position = None
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "^":
                position = (x, y)

    assert position is not None
    direction = Direction.UP
    vector = direction.vector()
    visited = {position}
    obstructions = set()

    while True:
        next_position = (position[0] + vector[0], position[1] + vector[1])

        if not (0 <= next_position[0] < width and 0 <= next_position[1] < height):
            break

        if grid[next_position[1]][next_position[0]] == "#":
            direction = direction.next_direction()
            vector = direction.vector()
        else:
            if next_position not in obstructions and next_position not in visited:
                grid[next_position[1]][next_position[0]] = "#"

                if not leave_area(grid=grid, position=position, direction=direction):
                    print("obstruction at", next_position, file=sys.stderr)
                    obstructions.add(next_position)

                grid[next_position[1]][next_position[0]] = "."

            position = next_position
            visited.add(position)

    print(len(obstructions))


if __name__ == "__main__":
    main()

# 1478 wrong
