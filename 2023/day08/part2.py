from __future__ import annotations

import math
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


class NodeCycle(NamedTuple):
    cycle_first_start_step: int
    cycle_first_end_step: int
    end_label_steps_in_cycle: list[int]

    @property
    def length(self) -> int:
        return self.cycle_first_end_step - self.cycle_first_start_step

    @staticmethod
    def from_node(
        node: Node,
        instructions: str,
        network: dict[str, Node],
    ) -> NodeCycle:
        current_node = node
        current_instruction_idx = 0
        visited = set()
        cycle = []

        while (current_node.label, current_instruction_idx) not in visited:
            visited.add((current_node.label, current_instruction_idx))
            cycle.append((current_node.label, current_instruction_idx))
            label = current_node.get_next_label(
                instruction=instructions[current_instruction_idx]
            )
            current_node = network[label]
            current_instruction_idx = (current_instruction_idx + 1) % len(instructions)

        start_pos = (current_node.label, current_instruction_idx)
        start_step = cycle.index(start_pos)
        end_step = len(cycle)
        first_cycle = cycle[start_step:end_step]
        end_label_steps_in_cycle = [
            i for i, pos in enumerate(first_cycle) if pos[0].endswith("Z")
        ]
        return NodeCycle(
            cycle_first_start_step=start_step,
            cycle_first_end_step=end_step,
            end_label_steps_in_cycle=end_label_steps_in_cycle,
        )


def main() -> None:
    network = {}

    with open("input.txt", "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i == 0:
                instructions = line.strip()

            elif i >= 2:
                node = Node.parse(line=line)
                network[node.label] = node

    starting_nodes = [node for label, node in network.items() if label.endswith("A")]
    starting_nodes_cycles = [
        NodeCycle.from_node(node=node, instructions=instructions, network=network)
        for node in starting_nodes
    ]
    print(starting_nodes_cycles, file=sys.stderr)

    lengths = [cycle.length for cycle in starting_nodes_cycles]
    print(lengths, file=sys.stderr)

    response = math.lcm(*lengths)
    print(response)


if __name__ == "__main__":
    main()
