import sys
from typing import Iterator

from numpy.polynomial.polynomial import Polynomial
from scipy.interpolate import lagrange

STEPS = 26501365  # = 202300 * 131 + 65


def iterate_neighbors(
    position: tuple[int, int],
    grid: list[str],
) -> Iterator[tuple[int, int]]:
    n_rows = len(grid)
    n_cols = len(grid[0])

    for row, col in (
        (position[0] - 1, position[1]),
        (position[0] + 1, position[1]),
        (position[0], position[1] - 1),
        (position[0], position[1] + 1),
    ):
        if grid[row % n_rows][col % n_cols] != "#":
            yield row, col


def main() -> None:
    grid = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for row, line in enumerate(file):
            grid.append(line.strip())
            col = line.find("S")
            if col >= 0:
                start = (row, col)

    n_rows = len(grid)
    n_cols = len(grid[0])
    assert n_rows == n_cols

    step = 0
    positions = {start}
    y = []

    while positions and len(y) < 3:
        step += 1
        next_positions = set()
        for position in positions:
            for neighbor in iterate_neighbors(position=position, grid=grid):
                next_positions.add(neighbor)

        positions = next_positions

        if step % n_rows == STEPS % n_rows:
            print(
                f"step={step}, x={step // n_rows}, y={len(positions)}",
                file=sys.stderr,
            )
            y.append(len(positions))

    x = [0, 1, 2]
    poly = Polynomial(lagrange(x, y).coef[::-1])
    print(int(poly(STEPS // n_rows)))


if __name__ == "__main__":
    main()
