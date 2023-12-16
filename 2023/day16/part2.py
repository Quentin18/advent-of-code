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


def get_start_beams(grid: list[str]) -> list[Beam]:
    start_beams = []
    last_col = len(grid) - 1
    last_row = len(grid[0]) - 1

    for row in range(len(grid)):
        start_beams.extend(
            [
                Beam(row=row, col=0, direction=Direction.RIGHT),
                Beam(row=row, col=last_col, direction=Direction.LEFT),
            ]
        )

    for col in range(len(grid[0])):
        start_beams.extend(
            [
                Beam(row=0, col=col, direction=Direction.DOWN),
                Beam(row=last_row, col=col, direction=Direction.UP),
            ]
        )

    return start_beams


def count_energized_tiles(grid: list[str], start_beam: Beam) -> int:
    energized_tiles = set()
    visited_positions = set()
    beams = [start_beam]

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

    print(
        max(
            count_energized_tiles(grid=grid, start_beam=start_beam)
            for start_beam in get_start_beams(grid=grid)
        )
    )


if __name__ == "__main__":
    main()
