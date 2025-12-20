import networkx as nx


def count_paths(
    graph: nx.DiGraph,
    source: str,
    target: str,
) -> int:
    topo_order = list(nx.topological_sort(graph))
    path_counts = {node: 0 for node in graph.nodes()}
    path_counts[source] = 1

    for node in topo_order:
        if path_counts[node] > 0:
            for neighbor in graph.successors(node):
                path_counts[neighbor] += path_counts[node]

    return path_counts[target]


def main() -> None:
    graph = nx.DiGraph()

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            source, targets = line.strip().split(": ")
            for target in targets.split():
                graph.add_edge(source, target)

    assert nx.is_directed_acyclic_graph(graph)

    print(
        count_paths(graph, "svr", "fft")
        * count_paths(graph, "fft", "dac")
        * count_paths(graph, "dac", "out")
    )


if __name__ == "__main__":
    main()
