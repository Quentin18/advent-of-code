from __future__ import annotations

import sys
from typing import NamedTuple

import numpy as np
import z3


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


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        hailstones = [Hailstone.parse(line=line) for line in file]

    print(f"{hailstones=}", file=sys.stderr)

    solver = z3.Solver()
    x, y, z = z3.Ints("x y z")
    vx, vy, vz = z3.Ints("vx vy vz")

    for i, hailstone in enumerate(hailstones):
        x_i, y_i, z_i = hailstone.position
        vx_i, vy_i, vz_i = hailstone.velocity
        t_i = z3.Int(f"t_{i}")
        solver.add(x + t_i * vx == x_i + t_i * vx_i)
        solver.add(y + t_i * vy == y_i + t_i * vy_i)
        solver.add(z + t_i * vz == z_i + t_i * vz_i)

    print(solver, file=sys.stderr)
    print(solver.check(), file=sys.stderr)

    model = solver.model()
    print(model, file=sys.stderr)

    print(model.eval(x + y + z))


if __name__ == "__main__":
    main()
