from enum import Enum


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


MIROR_DIRECTION = {
    "/": {
        Direction.UP: Direction.RIGHT,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.DOWN,
        Direction.RIGHT: Direction.UP,
    },
    "\\": {
        Direction.UP: Direction.LEFT,
        Direction.DOWN: Direction.RIGHT,
        Direction.LEFT: Direction.UP,
        Direction.RIGHT: Direction.DOWN,
    },
}


class Beam:
    def __init__(
        self,
        row: int,
        col: int,
        direction: Direction,
    ) -> None:
        self.row = row
        self.col = col
        self.direction = direction

    def move(self, direction: Direction) -> None:
        self.direction = direction
        if direction == Direction.UP:
            self.row -= 1
        elif direction == Direction.DOWN:
            self.row += 1
        elif direction == Direction.LEFT:
            self.col -= 1
        elif direction == Direction.RIGHT:
            self.col += 1

    def is_inside(self, grid: list[str]) -> bool:
        return 0 <= self.row < len(grid) and 0 <= self.col < len(grid[0])


def count_energized_tiles(grid: list[str]) -> int:
    energized_tiles = set()
    visited_positions = set()
    beams = [Beam(row=0, col=0, direction=Direction.RIGHT)]

    while beams:
        next_beams = []

        for beam in beams:
            char = grid[beam.row][beam.col]
            energized_tiles.add((beam.row, beam.col))
            visited_positions.add((beam.row, beam.col, beam.direction))

            if char in "/\\":
                direction = MIROR_DIRECTION[char][beam.direction]
                beam.move(direction=direction)
                next_beams.append(beam)

            elif char == "|" and beam.direction in (Direction.LEFT, Direction.RIGHT):
                next_beams.extend(
                    [
                        Beam(row=beam.row - 1, col=beam.col, direction=Direction.UP),
                        Beam(row=beam.row + 1, col=beam.col, direction=Direction.DOWN),
                    ]
                )

            elif char == "-" and beam.direction in (Direction.UP, Direction.DOWN):
                next_beams.extend(
                    [
                        Beam(row=beam.row, col=beam.col - 1, direction=Direction.LEFT),
                        Beam(row=beam.row, col=beam.col + 1, direction=Direction.RIGHT),
                    ]
                )

            else:
                beam.move(direction=beam.direction)
                next_beams.append(beam)

        beams = [
            beam
            for beam in next_beams
            if beam.is_inside(grid=grid)
            and (beam.row, beam.col, beam.direction) not in visited_positions
        ]

    return len(energized_tiles)


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [line.strip() for line in file]

    print(count_energized_tiles(grid=grid))


if __name__ == "__main__":
    main()
