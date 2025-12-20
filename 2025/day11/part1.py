import networkx as nx


def main() -> None:
    graph = nx.DiGraph()

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            source, targets = line.strip().split(": ")
            for target in targets.split():
                graph.add_edge(source, target)

    print(len(list(nx.all_simple_paths(graph, "you", "out"))))


if __name__ == "__main__":
    main()
