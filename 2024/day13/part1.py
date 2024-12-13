import re
from typing import NamedTuple

import numpy as np


class Machine(NamedTuple):
    button_a: tuple[float, float]
    button_b: tuple[float, float]
    prize: tuple[float, float]


def main() -> None:
    machines = []

    with open("input.txt", "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i % 4 == 0:
                x, y = re.match(r"Button A: X\+(\d+), Y\+(\d+)", line.strip()).groups()
                button_a = (int(x), int(y))
            elif i % 4 == 1:
                x, y = re.match(r"Button B: X\+(\d+), Y\+(\d+)", line.strip()).groups()
                button_b = (int(x), int(y))
            elif i % 4 == 2:
                x, y = re.match(r"Prize: X=(\d+), Y=(\d+)", line.strip()).groups()
                prize = (int(x), int(y))
            else:
                machines.append(
                    Machine(button_a=button_a, button_b=button_b, prize=prize)
                )

        machines.append(Machine(button_a=button_a, button_b=button_b, prize=prize))

    tokens = 0

    for machine in machines:
        a = np.array(
            [
                [machine.button_a[0], machine.button_b[0]],
                [machine.button_a[1], machine.button_b[1]],
            ]
        )
        b = np.array([machine.prize[0], machine.prize[1]])
        det = a[0, 0] * a[1, 1] - a[1, 0] * a[0, 1]
        x = np.array([[a[1, 1], -a[0, 1]], [-a[1, 0], a[0, 0]]]) @ b

        if not (x % det == 0).all():
            continue

        tokens += ((x // det) * [3, 1]).sum()

    print(tokens)


if __name__ == "__main__":
    main()
