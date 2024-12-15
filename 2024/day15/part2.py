import sys

import numpy as np


class WareHouse:
    def __init__(self, grid: np.ndarray, robot: np.ndarray) -> None:
        self.grid = grid
        self.robot = robot

    def _flip_ud(self) -> None:
        self.grid = np.flipud(self.grid)
        self.robot[0] = self.grid.shape[0] - 1 - self.robot[0]

    def _flip_lr(self) -> None:
        self.grid = np.fliplr(self.grid)
        self.robot[1] = self.grid.shape[1] - 1 - self.robot[1]

    def _up(self) -> None:
        start_row, col = self.robot
        end_row = start_row
        cols_to_move_per_row = {end_row: {col}}
        stop = False

        while True:
            cols_to_move = set()

            for col in cols_to_move_per_row[end_row]:
                if self.grid[end_row - 1, col] == "#":
                    stop = True
                    break

                if self.grid[end_row - 1, col] == "[":
                    cols_to_move.update({col, col + 1})
                elif self.grid[end_row - 1, col] == "]":
                    cols_to_move.update({col, col - 1})

            if stop or not cols_to_move:
                break

            end_row -= 1
            cols_to_move_per_row[end_row] = cols_to_move

        if any(
            self.grid[end_row - 1, col] == "#" for col in cols_to_move_per_row[end_row]
        ):
            return

        for row in range(end_row, start_row + 1):
            for col in cols_to_move_per_row[row]:
                self.grid[row - 1, col] = self.grid[row, col]
                self.grid[row, col] = "."

        self.robot += [-1, 0]

    def _down(self) -> None:
        self._flip_ud()
        self._up()
        self._flip_ud()

    def _left(self) -> None:
        row, start_col = self.robot
        end_col = start_col

        while self.grid[row, end_col - 1] in "[]":
            end_col -= 1

        if self.grid[row, end_col - 1] == "#":
            return

        self.grid[row, end_col - 1 : start_col] = self.grid[
            row, end_col : start_col + 1
        ]
        self.grid[row, start_col] = "."
        self.robot += [0, -1]

    def _right(self) -> None:
        self._flip_lr()
        self._left()
        self._flip_lr()

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
        rows, cols = np.where(self.grid == "[")
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

            line = (
                line.strip()
                .replace("#", "##")
                .replace("O", "[]")
                .replace(".", "..")
                .replace("@", "@.")
            )

            grid.append(list(line))
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
