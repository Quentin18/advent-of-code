from __future__ import annotations

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


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [line.strip() for line in file]

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

    while True:
        next_position = (position[0] + vector[0], position[1] + vector[1])

        if not (0 <= next_position[0] < width and 0 <= next_position[1] < height):
            break

        if grid[next_position[1]][next_position[0]] == "#":
            direction = direction.next_direction()
            vector = direction.vector()
        else:
            position = next_position
            visited.add(position)

    print(len(visited))


if __name__ == "__main__":
    main()
