from typing import Iterator


def iter_adjacent(
    row: int,
    col: int,
    n_rows: int,
    n_cols: int,
) -> Iterator[tuple[int, int]]:
    for r, c in (
        (row - 1, col),
        (row - 1, col + 1),
        (row, col + 1),
        (row + 1, col + 1),
        (row + 1, col),
        (row + 1, col - 1),
        (row, col - 1),
        (row - 1, col - 1),
    ):
        if 0 <= r < n_rows and 0 <= c < n_cols:
            yield r, c


def is_symbol(char: str) -> bool:
    return not char.isdigit() and char != "."


def is_adjacent_to_symbol(
    engine_schematic: list[str],
    row: int,
    col: int,
    n_rows: int,
    n_cols: int,
) -> bool:
    return any(
        is_symbol(char=engine_schematic[r][c])
        for r, c in iter_adjacent(row=row, col=col, n_rows=n_rows, n_cols=n_cols)
    )


def get_part_numbers_mask(engine_schematic: list[str]) -> list[list[bool]]:
    part_numbers_mask = []

    n_rows = len(engine_schematic)
    n_cols = len(engine_schematic[0])

    number = ""
    is_part_number = False

    for row, line in enumerate(engine_schematic):
        line_mask = []

        for col, char in enumerate(line):
            if char.isdigit():
                number += char
                if not is_part_number:
                    is_part_number = is_adjacent_to_symbol(
                        engine_schematic=engine_schematic,
                        row=row,
                        col=col,
                        n_rows=n_rows,
                        n_cols=n_cols,
                    )

            if number and (not char.isdigit() or col == n_cols - 1):
                if is_part_number:
                    print(number, "is a part number")
                else:
                    print(number, "is not a part number")
                line_mask.extend([is_part_number] * len(number))
                number = ""
                is_part_number = False

            if not char.isdigit():
                line_mask.append(False)

        assert len(line_mask) == n_cols

        part_numbers_mask.append(line_mask)

    return part_numbers_mask


def get_number_from_row_col(
    engine_schematic: list[str],
    row: int,
    col: int,
    n_cols: int,
) -> int:
    number = engine_schematic[row][col]

    # left digits
    for c in range(col - 1, -1, -1):
        char = engine_schematic[row][c]
        if not char.isdigit():
            break
        number = char + number

    # right digits
    for c in range(col + 1, n_cols):
        char = engine_schematic[row][c]
        if not char.isdigit():
            break
        number += char

    return int(number)


# pylint: disable=too-many-positional-arguments
def get_gear_ratio(
    engine_schematic: list[str],
    row: int,
    col: int,
    n_rows: int,
    n_cols: int,
    part_numbers_mask: list[list[bool]],
) -> int:
    if engine_schematic[row][col] != "*":
        return 0

    part_numbers = []

    for r, c in iter_adjacent(row=row, col=col, n_rows=n_rows, n_cols=n_cols):
        if not part_numbers_mask[r][c]:
            continue

        # avoid to take into account the same part number
        if c + 1 < n_cols and c + 1 <= col + 1 and part_numbers_mask[r][c + 1]:
            continue

        part_number = get_number_from_row_col(
            engine_schematic=engine_schematic,
            row=r,
            col=c,
            n_cols=n_cols,
        )

        part_numbers.append(part_number)

    gear_ratio = part_numbers[0] * part_numbers[1] if len(part_numbers) == 2 else 0

    print(f"gear ratio at ({row}, {col}) is {gear_ratio}")

    return gear_ratio


def get_gear_ratios_sum(engine_schematic: list[str]) -> int:
    n_rows = len(engine_schematic)
    n_cols = len(engine_schematic[0])

    part_numbers_mask = get_part_numbers_mask(engine_schematic=engine_schematic)

    gear_ratios_sum = 0

    for row in range(n_rows):
        for col in range(n_cols):
            gear_ratios_sum += get_gear_ratio(
                engine_schematic=engine_schematic,
                row=row,
                col=col,
                n_rows=n_rows,
                n_cols=n_cols,
                part_numbers_mask=part_numbers_mask,
            )

    return gear_ratios_sum


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        engine_schematic = [line.strip() for line in file]

    response = get_gear_ratios_sum(engine_schematic=engine_schematic)
    print(response)


if __name__ == "__main__":
    main()
