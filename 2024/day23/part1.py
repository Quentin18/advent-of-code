import networkx as nx


def main() -> None:
    graph = nx.DiGraph()

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            u, v = line.strip().split("-")
            graph.add_edge(u, v)
            graph.add_edge(v, u)

    cycles = 0
    for cycle in nx.simple_cycles(graph, 3):
        if len(cycle) == 3 and any(node.startswith("t") for node in cycle):
            cycles += 1

    print(cycles // 2)


if __name__ == "__main__":
    main()
