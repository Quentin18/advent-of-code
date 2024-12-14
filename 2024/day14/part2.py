import re
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange

WIDTH = 101
HEIGHT = 103
TOTAL_SECONDS = 10_000
IMGS_PATH = Path("imgs")


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


def check_christmas_tree(robots: list[Robot]) -> bool:
    quadrants_count = np.zeros(4, dtype=int)

    for robot in robots:
        quadrant = robot.quadrant()
        if quadrant is not None:
            quadrants_count[quadrant] += 1

    print(quadrants_count)

    return (
        quadrants_count[0] == quadrants_count[2]
        and quadrants_count[1] == quadrants_count[3]
    )


def save_img(robots: list[Robot], seconds: int) -> None:
    robot_counts = np.zeros((WIDTH, HEIGHT), dtype=np.uint8)

    for robot in robots:
        robot_counts[robot.position[0], robot.position[1]] = 1

    plt.imsave(IMGS_PATH / f"{seconds}.png", robot_counts, cmap="gray")


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

    IMGS_PATH.mkdir(exist_ok=True)

    for i in trange(TOTAL_SECONDS, desc="Generating images"):
        for robot in robots:
            robot.move()
        save_img(robots=robots, seconds=i + 1)


if __name__ == "__main__":
    main()
