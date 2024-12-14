import re
from dataclasses import dataclass

import numpy as np

WIDTH = 101  # 11
HEIGHT = 103  # 7
TOTAL_SECONDS = 100


@dataclass
class Robot:
    position: np.ndarray
    velocity: np.ndarray

    def move(self) -> None:
        self.position = (self.position + self.velocity) % [WIDTH, HEIGHT]

    def quadrant(self) -> int | None:
        if self.position[0] < WIDTH // 2 and self.position[1] < HEIGHT // 2:
            return 0

        if self.position[0] > WIDTH // 2 and self.position[1] < HEIGHT // 2:
            return 1

        if self.position[0] < WIDTH // 2 and self.position[1] > HEIGHT // 2:
            return 2

        if self.position[0] > WIDTH // 2 and self.position[1] > HEIGHT // 2:
            return 3

        return None


def main() -> None:
    robots = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            x, y, vx, vy = list(
                map(
                    int,
                    (
                        re.match(
                            r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)",
                            line.strip(),
                        ).groups()
                    ),
                )
            )
            robots.append(
                Robot(
                    position=np.array([x, y]),
                    velocity=np.array([vx, vy]),
                )
            )

    for _ in range(TOTAL_SECONDS):
        for robot in robots:
            robot.move()

    quadrants_count = np.zeros(4, dtype=int)
    for robot in robots:
        quadrant = robot.quadrant()
        if quadrant is not None:
            quadrants_count[quadrant] += 1

    print(np.prod(quadrants_count))


if __name__ == "__main__":
    main()
