from typing import Iterator

STEPS = 64


def is_inside(row: int, col: int, n_rows: int, n_cols: int) -> bool:
    return 0 <= row < n_rows and 0 <= col < n_cols


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
        if (
            is_inside(row=row, col=col, n_rows=n_rows, n_cols=n_cols)
            and grid[row][col] != "#"
        ):
            yield row, col


def main() -> None:
    grid = []
    start = None

    with open("input.txt", "r", encoding="utf-8") as file:
        for row, line in enumerate(file):
            grid.append(line.strip())
            col = line.find("S")
            if col >= 0:
                start = (row, col)

    step = 0
    positions = {start}
    while positions and step < STEPS:
        step += 1
        next_positions = set()
        for position in positions:
            for neighbor in iterate_neighbors(position=position, grid=grid):
                next_positions.add(neighbor)

        positions = next_positions

    print(len(positions))


if __name__ == "__main__":
    main()
