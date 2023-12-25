import sys
from math import prod

import networkx as nx


def make_graph(lines: list[str]) -> nx.Graph:
    graph = nx.Graph()
    for line in lines:
        node, neighbors = line.strip().split(": ")
        for neighbor in neighbors.split():
            graph.add_edge(node, neighbor)

    return graph


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        graph = make_graph(lines=file.readlines())

    graph.remove_edge("hrs", "mnf")
    graph.remove_edge("nnl", "kpc")
    graph.remove_edge("sph", "rkh")

    lengths = [len(c) for c in nx.components.connected_components(graph)]
    print(lengths, file=sys.stderr)
    print(prod(lengths))


if __name__ == "__main__":
    main()
