from __future__ import annotations

from dataclasses import dataclass

import z3


@dataclass
class Machine:
    light_diagram: str
    button_wiring_schematics: list[list[int]]
    joltage_requirements: list[int]

    @staticmethod
    def from_string(s: str) -> Machine:
        light_diagram = ""
        button_wiring_schematics = []
        joltage_requirements = []

        for substr in s.split():
            if substr[0] == "[":
                light_diagram = substr[1:-1]
            elif substr[0] == "(":
                button_wiring_schematics.append(list(map(int, substr[1:-1].split(","))))
            elif substr[0] == "{":
                joltage_requirements = list(map(int, substr[1:-1].split(",")))

        return Machine(
            light_diagram,
            button_wiring_schematics,
            joltage_requirements,
        )


def find_fewest_button_presses(machine: Machine) -> int:
    opt = z3.Optimize()

    buttons = [z3.Int(f"b_{i}") for i in range(len(machine.button_wiring_schematics))]

    for counter, joltage_requirement in enumerate(machine.joltage_requirements):
        opt.add(
            z3.Sum(
                *[
                    b
                    for b, schema in zip(buttons, machine.button_wiring_schematics)
                    if counter in schema
                ]
            )
            == joltage_requirement
        )

    for b in buttons:
        opt.add(b >= 0)

    opt.minimize(z3.Sum(buttons))

    if opt.check() != z3.sat:
        raise RuntimeError("No solution found")

    model = opt.model()

    return sum(model[b].as_long() for b in buttons)


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        machines = list(map(Machine.from_string, file.readlines()))

    print(sum(find_fewest_button_presses(machine) for machine in machines))


if __name__ == "__main__":
    main()
