from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import networkx as nx


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
    graph = nx.Graph()

    for source in product(".#", repeat=len(machine.light_diagram)):
        for button_wiring in machine.button_wiring_schematics:
            target = list(source)

            for i in button_wiring:
                target[i] = "." if target[i] == "#" else "#"

            graph.add_edge("".join(source), "".join(target))

    return int(
        nx.shortest_path_length(
            graph,
            source="." * len(machine.light_diagram),
            target=machine.light_diagram,
        )
    )


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        machines = list(map(Machine.from_string, file.readlines()))

    print(sum(find_fewest_button_presses(machine) for machine in machines))


if __name__ == "__main__":
    main()
