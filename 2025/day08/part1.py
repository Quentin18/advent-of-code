import networkx as nx
import numpy as np
from scipy.spatial import distance_matrix

N_CONNECTIONS = 1000
N_CIRCUITS = 3


def main() -> None:
    with open("input.txt", "r", encoding="utf-8") as file:
        positions = [list(map(int, line.strip().split(","))) for line in file]

    dist = distance_matrix(positions, positions)
    mask = np.triu(np.ones(dist.shape, dtype=bool), k=1)
    vals = dist[mask]
    sorted_flat = np.argsort(vals)
    rows, cols = np.where(mask)

    graph = nx.Graph()
    for row, col in zip(
        rows[sorted_flat][:N_CONNECTIONS],
        cols[sorted_flat][:N_CONNECTIONS],
    ):
        graph.add_edge(row, col)

    circuits_lengths = sorted(
        [len(c) for c in nx.connected_components(graph)],
        reverse=True,
    )

    print(np.prod(circuits_lengths[:N_CIRCUITS]))


if __name__ == "__main__":
    main()
