import sys

import numpy as np


def get_north_tile(
    grid: np.ndarray,
    tile: tuple[int, int],
) -> set[tuple[int, int]]:
    if tile[0] - 1 >= 0 and grid[tile[0] - 1][tile[1]] in "|7F":
        return {(tile[0] - 1, tile[1])}

    return set()


def get_south_tile(
    grid: np.ndarray,
    tile: tuple[int, int],
) -> set[tuple[int, int]]:
    if tile[0] + 1 < len(grid) and grid[tile[0] + 1][tile[1]] in "|LJ":
        return {(tile[0] + 1, tile[1])}

    return set()


def get_west_tile(
    grid: np.ndarray,
    tile: tuple[int, int],
) -> set[tuple[int, int]]:
    if tile[1] - 1 >= 0 and grid[tile[0]][tile[1] - 1] in "-LF":
        return {(tile[0], tile[1] - 1)}

    return set()


def get_east_tile(
    grid: np.ndarray,
    tile: tuple[int, int],
) -> set[tuple[int, int]]:
    if tile[1] + 1 < len(grid[0]) and grid[tile[0]][tile[1] + 1] in "-J7":
        return {(tile[0], tile[1] + 1)}

    return set()


def steps_to_farthest(grid: np.ndarray, start: tuple[int, int]) -> int:
    current_tiles = {start}
    visited = {start}
    distance = 0
    distances = np.zeros_like(grid, dtype=int)

    while current_tiles:
        next_tiles = set()

        for tile in current_tiles:
            distances[tile[0]][tile[1]] = distance
            tile_char = grid[tile[0]][tile[1]]

            if tile_char == "|":
                next_tiles.update(
                    get_north_tile(grid=grid, tile=tile)
                    | get_south_tile(grid=grid, tile=tile)
                )
            elif tile_char == "-":
                next_tiles.update(
                    get_east_tile(grid=grid, tile=tile)
                    | get_west_tile(grid=grid, tile=tile)
                )
            elif tile_char == "L":
                next_tiles.update(
                    get_north_tile(grid=grid, tile=tile)
                    | get_east_tile(grid=grid, tile=tile)
                )
            elif tile_char == "J":
                next_tiles.update(
                    get_north_tile(grid=grid, tile=tile)
                    | get_west_tile(grid=grid, tile=tile)
                )
            elif tile_char == "7":
                next_tiles.update(
                    get_south_tile(grid=grid, tile=tile)
                    | get_west_tile(grid=grid, tile=tile)
                )
            elif tile_char == "F":
                next_tiles.update(
                    get_south_tile(grid=grid, tile=tile)
                    | get_east_tile(grid=grid, tile=tile)
                )
            elif tile_char == "S":
                next_tiles.update(
                    get_north_tile(grid=grid, tile=tile)
                    | get_south_tile(grid=grid, tile=tile)
                    | get_east_tile(grid=grid, tile=tile)
                    | get_west_tile(grid=grid, tile=tile)
                )

        # we return -1 in case there is no loop
        if len(current_tiles) == 1 and len(next_tiles - visited) == 1:
            return -1

        current_tiles = next_tiles - visited
        visited |= next_tiles
        distance += 1

    print(distances, file=sys.stderr)

    return distance - 1


def main() -> None:
    grid = []
    start = None

    with open("input.txt", "r", encoding="utf-8") as file:
        for row, line in enumerate(file):
            if "S" in line:
                start = (row, line.index("S"))
                print("start:", start, file=sys.stderr)
            grid.append(list(line.strip()))

    grid = np.array(grid)

    for start_char in "|-LJ7F":
        grid[start[0]][start[1]] = start_char
        response = steps_to_farthest(grid=grid, start=start)
        print(start_char, response, file=sys.stderr)
        if response > 0:
            break

    print(response)


if __name__ == "__main__":
    main()
