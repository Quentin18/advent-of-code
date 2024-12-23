import networkx as nx


def main() -> None:
    graph = nx.Graph()

    with open("input.txt", "r", encoding="utf-8") as file:
        for line in file:
            u, v = line.strip().split("-")
            graph.add_edge(u, v)

    max_clique = max(nx.find_cliques(graph), key=len)
    print(",".join(sorted(max_clique)))


if __name__ == "__main__":
    main()
