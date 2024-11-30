from __future__ import annotations

import sys
from typing import NamedTuple


class Node(NamedTuple):
    label: str
    left: str
    right: str

    @staticmethod
    def parse(line: str) -> Node:
        label, children = line.split(" = ")
        left, right = children[1:9].split(", ")
        return Node(label=label, left=left, right=right)

    def get_next_label(self, instruction: str) -> str:
        return self.left if instruction == "L" else self.right


def main() -> None:
    instructions = None
    network = {}

    with open("input.txt", "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i == 0:
                instructions = line.strip()

            elif i >= 2:
                node = Node.parse(line=line)
                network[node.label] = node

    print(instructions, file=sys.stderr)
    print(network, file=sys.stderr)

    current_node = network["AAA"]
    current_instruction_index = 0
    step = 0

    while current_node.label != "ZZZ":
        print(f"step {step}: {current_node}", file=sys.stderr)
        instruction = instructions[current_instruction_index]
        label = current_node.get_next_label(instruction=instruction)
        current_node = network[label]
        current_instruction_index = (current_instruction_index + 1) % len(instructions)
        step += 1

    print(f"step {step}: {current_node}", file=sys.stderr)
    print(step)


if __name__ == "__main__":
    main()
