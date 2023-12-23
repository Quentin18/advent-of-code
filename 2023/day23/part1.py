import sys
from typing import Iterator, NamedTuple


class Path(NamedTuple):
    current: tuple[int, int]
    visited: set[tuple[int, int]]

    def __len__(self) -> int:
        return len(self.visited) - 1

    def is_done(self, end: tuple[int, int]) -> bool:
        return self.current == end


def iterate_neighbors(
    position: tuple[int, int],
    grid: list[str],
) -> Iterator[tuple[int, int]]:
    row, col = position
    char = grid[row][col]

    if char == ".":
        n_rows = len(grid)
        n_cols = len(grid[0])

        for r, c in (
            (row - 1, col),
            (row, col + 1),
            (row + 1, col),
            (row, col - 1),
        ):
            if 0 <= r < n_rows and 0 <= c < n_cols and grid[r][c] != "#":
                yield r, c

    # note: we suppose that there is always a dot after a slope
    elif char == "^":
        yield row - 1, col

    elif char == ">":
        yield row, col + 1

    elif char == "v":
        yield row + 1, col

    elif char == "<":
        yield row, col - 1

    else:
        raise RuntimeError("no neighbors")


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        grid = [line.strip() for line in file]

    start = (0, grid[0].index("."))
    end = (len(grid) - 1, grid[-1].index("."))
    print(f"{start=}, {end=}", file=sys.stderr)

    paths = [Path(current=start, visited={start})]

    while not all(path.is_done(end=end) for path in paths):
        next_paths = []

        for path in paths:
            if path.is_done(end=end):
                next_paths.append(path)
                continue

            for neighbor in iterate_neighbors(position=path.current, grid=grid):
                if neighbor not in path.visited:
                    next_paths.append(
                        Path(current=neighbor, visited={*path.visited, neighbor})
                    )

        paths = next_paths

    lengths = sorted(len(path) for path in paths)[::-1]
    print(lengths, file=sys.stderr)
    print(max(lengths))


if __name__ == "__main__":
    main()
