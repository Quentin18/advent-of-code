from __future__ import annotations

import sys
from dataclasses import dataclass

import numpy as np


@dataclass
class Position:
    x: int
    y: int
    z: int


@dataclass
class Brick:
    name: int
    position_1: Position
    position_2: Position

    @staticmethod
    def parse(name: int, line: str) -> Brick:
        return Brick(
            name,
            *[
                Position(*[int(i) for i in xyz.split(",")])
                for xyz in line.strip().split("~")
            ],
        )

    @property
    def x_min(self) -> int:
        return min(self.position_1.x, self.position_2.x)

    @property
    def x_max(self) -> int:
        return max(self.position_1.x, self.position_2.x)

    @property
    def y_min(self) -> int:
        return min(self.position_1.y, self.position_2.y)

    @property
    def y_max(self) -> int:
        return max(self.position_1.y, self.position_2.y)

    @property
    def z_min(self) -> int:
        return min(self.position_1.z, self.position_2.z)

    @property
    def z_max(self) -> int:
        return max(self.position_1.z, self.position_2.z)


def make_grid(bricks: list[Brick]) -> np.ndarray:
    x_max = y_max = z_max = 0
    for brick in bricks:
        x_max = max(x_max, brick.x_max)
        y_max = max(y_max, brick.y_max)
        z_max = max(z_max, brick.z_max)

    print(f"{x_max=}, {y_max=}, {z_max=}", file=sys.stderr)

    grid = np.zeros((x_max + 1, y_max + 1, z_max + 1), dtype=int)

    for brick in bricks:
        for x in range(brick.position_1.x, brick.position_2.x + 1):
            for y in range(brick.position_1.y, brick.position_2.y + 1):
                for z in range(brick.position_1.z, brick.position_2.z + 1):
                    grid[x, y, z] = brick.name

    return grid


def fall_downward(bricks: list[Brick], grid: np.ndarray) -> None:
    for brick in bricks:
        z_delta = 0
        z_min = brick.z_min
        z_max = brick.z_max

        while (
            z_min + z_delta > 1
            and (
                grid[
                    brick.x_min : brick.x_max + 1,
                    brick.y_min : brick.y_max + 1,
                    z_min + z_delta - 1,
                ]
                == 0
            ).all()
        ):
            z_delta -= 1

        grid[
            brick.x_min : brick.x_max + 1,
            brick.y_min : brick.y_max + 1,
            z_min : z_max + 1,
        ] = 0

        grid[
            brick.x_min : brick.x_max + 1,
            brick.y_min : brick.y_max + 1,
            z_min + z_delta : z_max + z_delta + 1,
        ] = brick.name

        brick.position_1.z += z_delta
        brick.position_2.z += z_delta
        print(f"brick {brick.name}: {z_delta}", file=sys.stderr)


def get_support_map(bricks: list[Brick], grid: np.ndarray) -> dict[int, set[int]]:
    support_map = {}

    for brick in bricks:
        support_brick = set(
            grid[
                brick.x_min : brick.x_max + 1,
                brick.y_min : brick.y_max + 1,
                brick.z_max + 1,
            ].ravel()
        )
        if 0 in support_brick:
            support_brick.remove(0)
        support_map[brick.name] = support_brick

    return support_map


def get_supported_bricks_without_bricks(
    support_map: dict[int, set[int]],
    fallen_bricks: set[int],
) -> set[int]:
    supported_bricks_without_bricks = set()
    for brick, supported_brick in support_map.items():
        if brick not in fallen_bricks:
            supported_bricks_without_bricks |= supported_brick

    return supported_bricks_without_bricks - fallen_bricks


def count_fallen_bricks(support_map: dict[int, set[int]]) -> int:
    count = 0

    for brick in support_map:
        all_fallen_bricks = set()
        current_fallen_bricks = {brick}

        while current_fallen_bricks:
            supported_bricks_by_current_fallen_bricks = (
                set().union(*[support_map[b] for b in current_fallen_bricks])
                - all_fallen_bricks
            )
            supported_bricks_without_fallen_bricks = (
                get_supported_bricks_without_bricks(
                    support_map=support_map,
                    fallen_bricks=all_fallen_bricks | current_fallen_bricks,
                )
            )
            current_fallen_bricks = (
                supported_bricks_by_current_fallen_bricks
                - supported_bricks_without_fallen_bricks
            )
            all_fallen_bricks |= current_fallen_bricks

        count += len(all_fallen_bricks)
        print(
            (
                f"disintegrating brick {brick} would cause all {len(all_fallen_bricks)} "
                "other bricks to fall"
            ),
            file=sys.stderr,
        )

    return count


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        bricks = [
            Brick.parse(name=name + 1, line=line) for name, line in enumerate(file)
        ]

    bricks.sort(key=lambda b: (b.z_min, b.y_min, b.x_min))

    grid = make_grid(bricks=bricks)

    fall_downward(bricks=bricks, grid=grid)

    support_map = get_support_map(bricks=bricks, grid=grid)
    print(f"{support_map=}", file=sys.stderr)

    print(count_fallen_bricks(support_map=support_map))


if __name__ == "__main__":
    main()
