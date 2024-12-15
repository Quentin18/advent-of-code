import sys

import numpy as np


class WareHouse:
    def __init__(self, grid: np.ndarray, robot: np.ndarray) -> None:
        self.grid = grid
        self.robot = robot

    def _transpose(self) -> None:
        self.grid = np.transpose(self.grid)
        self.robot = np.flip(self.robot)

    def _reverse(self) -> None:
        self.grid = np.flipud(self.grid)
        self.robot[0] = len(self.grid) - 1 - self.robot[0]

    def _up(self) -> None:
        start_row, col = self.robot
        end_row = start_row

        while self.grid[end_row - 1, col] == "O":
            end_row -= 1

        if self.grid[end_row - 1, col] == "#":
            return

        self.grid[end_row - 1 : start_row, col] = self.grid[
            end_row : start_row + 1, col
        ]
        self.grid[start_row, col] = "."
        self.robot += [-1, 0]

    def _down(self) -> None:
        self._reverse()
        self._up()
        self._reverse()

    def _left(self) -> None:
        self._transpose()
        self._up()
        self._transpose()

    def _right(self) -> None:
        self._transpose()
        self._reverse()
        self._up()
        self._reverse()
        self._transpose()

    def move(self, char: str) -> None:
        match char:
            case "^":
                return self._up()
            case "v":
                return self._down()
            case "<":
                return self._left()
            case ">":
                return self._right()

    def sum_gps_coordinates(self) -> int:
        rows, cols = np.where(self.grid == "O")
        return (100 * rows + cols).sum()

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.grid)


def main() -> None:
    grid = []
    robot = None
    moves = ""

    with open("input.txt", "r", encoding="utf-8") as file:
        for row, line in enumerate(file):
            if not line.strip():
                break

            grid.append(list(line.strip()))
            col = line.find("@")
            if col != -1:
                robot = np.array([row, col])

        grid = np.array(grid)

        for line in file:
            moves += line.strip()

    warehouse = WareHouse(grid=grid, robot=robot)
    print("Initial state:", file=sys.stderr)
    print(warehouse, file=sys.stderr)

    for char in moves:
        warehouse.move(char)

    print("Final state:", file=sys.stderr)
    print(warehouse, file=sys.stderr)

    print(warehouse.sum_gps_coordinates())


if __name__ == "__main__":
    main()
