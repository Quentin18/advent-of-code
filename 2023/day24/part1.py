from __future__ import annotations

import sys
from itertools import combinations
from typing import NamedTuple

import numpy as np
from shapely.geometry import LineString, Point, Polygon

LOW, HIGH = 200_000_000_000_000, 400_000_000_000_000
MAX_TIME = 800_000_000_000_000


class Hailstone(NamedTuple):
    position: np.ndarray
    velocity: np.ndarray

    @staticmethod
    def parse(line: str) -> Hailstone:
        position, velocity = line.strip().split(" @ ")
        return Hailstone(
            position=np.array([int(i) for i in position.split(", ")]),
            velocity=np.array([int(i) for i in velocity.split(", ")]),
        )

    def start_position(self) -> np.ndarray:
        return self.position[:2]

    def end_position(self) -> np.ndarray:
        return (self.position + self.velocity * MAX_TIME)[:2]

    def line_string(self) -> LineString:
        return LineString([self.start_position(), self.end_position()])

    def intersection(self, other: Hailstone) -> LineString | Point:
        return self.line_string().intersection(other.line_string())


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        hailstones = [Hailstone.parse(line=line) for line in file]

    print(f"{hailstones=}", file=sys.stderr)

    test_area = Polygon([(LOW, LOW), (LOW, HIGH), (HIGH, HIGH), (HIGH, LOW)])
    print(f"{test_area=}", file=sys.stderr)

    count_intersections_inside_test_area = 0

    for hailstone_a, hailstone_b in combinations(hailstones, 2):
        intersection = hailstone_a.intersection(hailstone_b)
        print(
            f"A={hailstone_a}, B={hailstone_b}, intersection={intersection}",
            file=sys.stderr,
        )
        if isinstance(intersection, Point) and test_area.contains(intersection):
            count_intersections_inside_test_area += 1

    print(count_intersections_inside_test_area)


if __name__ == "__main__":
    main()
