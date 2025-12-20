from dataclasses import dataclass

import numpy as np


@dataclass
class Region:
    width: int
    length: int
    shape_quantities: list[int]


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]

    shapes = [
        np.array(
            [[int(c == "#") for c in line] for line in lines[i * 5 + 1 : i * 5 + 4]]
        )
        for i in range(6)
    ]

    regions = []
    for line in lines[30:]:
        size, quantities = line.split(": ")
        width, length = size.split("x")
        regions.append(
            Region(
                width=int(width),
                length=int(length),
                shape_quantities=list(map(int, quantities.split())),
            )
        )

    output = 0

    for region in regions:
        area = sum(
            quantity * shape.sum()
            for shape, quantity in zip(shapes, region.shape_quantities)
        )

        if area <= region.width * region.length:
            output += 1

    print(output)


if __name__ == "__main__":
    main()
