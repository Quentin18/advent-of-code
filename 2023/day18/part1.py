from __future__ import annotations

from enum import Enum
from typing import NamedTuple

from shapely import Polygon


class Direction(Enum):
    U = "U"
    D = "D"
    L = "L"
    R = "R"


class Trench(NamedTuple):
    direction: Direction
    meters: int
    color: str

    @staticmethod
    def parse(line: str) -> Trench:
        direction, meters, color = line.split()
        return Trench(
            direction=Direction(direction),
            meters=int(meters),
            color=color[2:-1],
        )


def make_polygon(trenches: list[Trench]) -> Polygon:
    coord = (0.5, 0.5)
    coords = [coord]

    for trench in trenches:
        if trench.direction == Direction.U:
            coord = (coord[0] - trench.meters, coord[1])
        elif trench.direction == Direction.D:
            coord = (coord[0] + trench.meters, coord[1])
        elif trench.direction == Direction.L:
            coord = (coord[0], coord[1] - trench.meters)
        elif trench.direction == Direction.R:
            coord = (coord[0], coord[1] + trench.meters)
        coords.append(coord)

    return Polygon(coords)


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        trenches = [Trench.parse(line=line.strip()) for line in file]

    polygon = make_polygon(trenches=trenches)
    polygon_extended = polygon.buffer(
        0.5,
        cap_style="square",
        join_style="mitre",
    )
    print(int(polygon_extended.area))


if __name__ == "__main__":
    main()
