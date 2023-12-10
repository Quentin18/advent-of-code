import sys

import numpy as np
from tqdm import trange


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


def get_loop_mask(grid: np.ndarray, start: tuple[int, int]) -> np.ndarray | None:
    current_tiles = {start}
    visited = {start}
    mask = np.zeros_like(grid, dtype=int)

    while current_tiles:
        next_tiles = set()

        for tile in current_tiles:
            mask[tile[0]][tile[1]] = 1
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

        # we return None in case there is no loop
        if len(current_tiles) == 1 and len(next_tiles - visited) == 1:
            return None

        current_tiles = next_tiles - visited
        visited |= next_tiles

    return mask if len(visited) > 1 else None


def get_vertical_expanded_grid(
    grid: np.ndarray,
    loop_mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    expanded_grid = []

    for row in range(loop_mask.shape[0]):
        expanded_line = []
        for col in range(loop_mask.shape[1] - 1):
            left_char = grid[row][col] if loop_mask[row][col] else "."
            right_char = grid[row][col + 1] if loop_mask[row][col + 1] else "."
            middle_char = "-" if left_char in "-LF" and right_char in "-J7" else "."
            expanded_line.extend([left_char, middle_char])
            if col == loop_mask.shape[1] - 2:
                expanded_line.append(right_char)

        expanded_grid.append(expanded_line)

    expanded_grid = np.array(expanded_grid)
    expanded_mask = expanded_grid != "."

    return expanded_grid, expanded_mask


def get_horizontal_expanded_grid(
    grid: np.ndarray,
    loop_mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    expanded_grid = []

    for col in range(loop_mask.shape[1]):
        expanded_column = []
        for row in range(loop_mask.shape[0] - 1):
            up_char = grid[row][col] if loop_mask[row][col] else "."
            down_char = grid[row + 1][col] if loop_mask[row + 1][col] else "."
            middle_char = "|" if up_char in "|7F" and down_char in "|LJ" else "."
            expanded_column.extend([up_char, middle_char])
            if row == loop_mask.shape[0] - 2:
                expanded_column.append(down_char)

        expanded_grid.append(np.array(expanded_column))

    expanded_grid = np.column_stack(expanded_grid)
    expanded_mask = expanded_grid != "."

    return expanded_grid, expanded_mask


def is_on_border(tile: tuple[int, int], shape: tuple[int, int]) -> bool:
    return (
        tile[0] == 0
        or tile[0] == shape[0] - 1
        or tile[1] == 0
        or tile[1] == shape[1] - 1
    )


def is_inside(tile: tuple[int, int], shape: tuple[int, int]) -> bool:
    return tile[0] >= 0 and tile[0] < shape[0] and tile[1] >= 0 and tile[1] < shape[1]


def is_enclosed(tile: tuple[int, int], loop_mask: np.ndarray) -> bool:
    # case tile on loop
    if loop_mask[tile[0]][tile[1]]:
        return False

    visited = set()
    current_tiles = {tile}

    while current_tiles:
        next_tiles = set()

        for t in current_tiles:
            if is_on_border(tile=t, shape=loop_mask.shape):
                return False

            visited.add(t)
            row, col = t
            for r, c in (
                (row - 1, col),
                (row, col + 1),
                (row + 1, col),
                (row, col - 1),
            ):
                if (
                    is_inside(tile=(r, c), shape=loop_mask.shape)
                    and not loop_mask[r][c]
                ):
                    next_tiles.add((r, c))

        current_tiles = next_tiles - visited

    return True


def get_enclosed_mask(grid: np.ndarray, loop_mask: np.ndarray) -> np.ndarray:
    enclosed_mask = np.zeros_like(grid, dtype=int)

    # takes 10 min - can be optimized
    for row in trange(grid.shape[0]):
        for col in range(grid.shape[1]):
            enclosed_mask[row][col] = is_enclosed(tile=(row, col), loop_mask=loop_mask)

    return enclosed_mask


def count_enclosed_tiles(grid: np.ndarray, loop_mask: np.ndarray) -> int:
    expanded_grid, expanded_loop_mask = get_vertical_expanded_grid(
        grid=grid,
        loop_mask=loop_mask,
    )
    expanded_grid, expanded_loop_mask = get_horizontal_expanded_grid(
        grid=expanded_grid,
        loop_mask=expanded_loop_mask,
    )
    # print("expanded grid:", file=sys.stderr)
    # print("\n".join("".join(line) for line in expanded_grid), file=sys.stderr)

    expanded_enclosed_mask = get_enclosed_mask(
        grid=expanded_grid,
        loop_mask=expanded_loop_mask,
    )
    # print("expanded enclosed mask:", file=sys.stderr)
    # print(
    #     "\n".join("".join(line.astype(str)) for line in expanded_enclosed_mask),
    #     file=sys.stderr,
    # )

    enclosed_mask = expanded_enclosed_mask[::2, ::2]
    # print("enclosed mask:", file=sys.stderr)
    # print(
    #     "\n".join("".join(line.astype(str)) for line in enclosed_mask),
    #     file=sys.stderr,
    # )

    return enclosed_mask.sum()


def main() -> None:
    grid = []
    start = None

    with open("input.txt", "r", encoding="utf-8") as file:
        for row, line in enumerate(file):
            if "S" in line:
                start = (row, line.index("S"))
                # print("start:", start, file=sys.stderr)
            grid.append(list(line.strip()))

    grid = np.array(grid)

    for start_char in "|-LJ7F":
        grid[start[0]][start[1]] = start_char
        mask = get_loop_mask(grid=grid, start=start)
        if mask is not None:
            break

    # print("start_char:", start_char, file=sys.stderr)
    # print("mask:", file=sys.stderr)
    # print(mask, file=sys.stderr)

    response = count_enclosed_tiles(grid=grid, loop_mask=mask)
    print(response)


if __name__ == "__main__":
    main()
