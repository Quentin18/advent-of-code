import networkx as nx
import numpy as np
from scipy.spatial import distance_matrix


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        positions = [list(map(int, line.strip().split(","))) for line in file]

    dist = distance_matrix(positions, positions)
    mask = np.triu(np.ones(dist.shape, dtype=bool), k=1)
    vals = dist[mask]
    sorted_flat = np.argsort(vals)
    rows, cols = np.where(mask)

    graph = nx.Graph()
    graph.add_nodes_from(np.arange(len(positions)))

    for row, col in zip(
        rows[sorted_flat],
        cols[sorted_flat],
    ):
        graph.add_edge(row, col)
        if nx.number_connected_components(graph) == 1:
            print(positions[row][0] * positions[col][0])
            return

    raise RuntimeError("answer not found")


if __name__ == "__main__":
    main()
