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
        0 <= r < n_rows and 0 <= c < n_cols and is_symbol(char=engine_schematic[r][c])
        for r, c in (
            (row - 1, col),
            (row - 1, col + 1),
            (row, col + 1),
            (row + 1, col + 1),
            (row + 1, col),
            (row + 1, col - 1),
            (row, col - 1),
            (row - 1, col - 1),
        )
    )


def get_part_numbers_sum(engine_schematic: list[str]) -> int:
    n_rows = len(engine_schematic)
    n_cols = len(engine_schematic[0])

    part_numbers_sum = 0
    number = ""
    is_part_number = False

    for row, line in enumerate(engine_schematic):
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
                    part_numbers_sum += int(number)
                else:
                    print(number, "is not a part number")
                number = ""
                is_part_number = False

    return part_numbers_sum


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        engine_schematic = [line.strip() for line in file]

    response = get_part_numbers_sum(engine_schematic=engine_schematic)
    print(response)


if __name__ == "__main__":
    main()
