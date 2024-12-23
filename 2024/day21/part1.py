import itertools
import sys

import networkx as nx

DIR_KEYPAD_NEXT_POS = {
    "^": {"v": "v", ">": "A"},
    "v": {"^": "^", "<": "<", ">": ">"},
    "<": {">": "v"},
    ">": {"<": "v", "^": "A"},
    "A": {"<": "^", "v": ">"},
}
NUM_KEYPAD_NEXT_POS = {
    "0": {"^": "2", ">": "A"},
    "1": {">": "2", "^": "4"},
    "2": {"v": "0", "<": "1", ">": "3", "^": "5"},
    "3": {"<": "2", "^": "6", "v": "A"},
    "4": {"v": "1", ">": "5", "^": "7"},
    "5": {"v": "2", "<": "4", ">": "6", "^": "8"},
    "6": {"v": "3", "<": "5", "^": "9"},
    "7": {"v": "4", ">": "8"},
    "8": {"v": "5", "<": "7", ">": "9"},
    "9": {"v": "6", "<": "8"},
    "A": {"<": "0", "^": "3"},
}


def generate_graph() -> nx.Graph:
    graph = nx.DiGraph()

    for node in itertools.product(
        DIR_KEYPAD_NEXT_POS,
        DIR_KEYPAD_NEXT_POS,
        NUM_KEYPAD_NEXT_POS,
    ):
        graph.add_node(node)

        for human_action in DIR_KEYPAD_NEXT_POS:
            if human_action == "A":
                if node[0] == "A":
                    if node[1] == "A":
                        continue

                    door_robot_pos = NUM_KEYPAD_NEXT_POS[node[2]].get(node[1])
                    if door_robot_pos is not None:
                        graph.add_edge(
                            node,
                            (node[0], node[1], door_robot_pos),
                            action=human_action,
                        )
                else:
                    second_robot_pos = DIR_KEYPAD_NEXT_POS[node[1]].get(node[0])
                    if second_robot_pos is not None:
                        graph.add_edge(
                            node,
                            (node[0], second_robot_pos, node[2]),
                            action=human_action,
                        )
            else:
                first_robot_pos = DIR_KEYPAD_NEXT_POS[node[0]].get(human_action)
                if first_robot_pos is not None:
                    graph.add_edge(
                        node,
                        (first_robot_pos, node[1], node[2]),
                        action=human_action,
                    )

    return graph


def find_shortest_sequence(graph: nx.Graph, code: str) -> str:
    start = ("A", "A", "A")
    sequence = ""
    for char in code:
        shortest_path = nx.shortest_path(graph, start, ("A", "A", char))
        sequence += "".join(
            graph[source][target]["action"]
            for source, target in zip(shortest_path[:-1], shortest_path[1:])
        )
        sequence += "A"
        start = shortest_path[-1]

    return sequence


def get_complexity(code: str, sequence: str) -> int:
    return len(sequence) * int("".join(char for char in code if char.isdigit()))


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        codes = [line.strip() for line in file]

    graph = generate_graph()
    print(graph, file=sys.stderr)

    complexity = 0

    for code in codes:
        sequence = find_shortest_sequence(graph=graph, code=code)
        print(code, sequence, file=sys.stderr)
        complexity += get_complexity(code=code, sequence=sequence)

    print(complexity)


if __name__ == "__main__":
    main()
