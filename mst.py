import argparse
import collections
import sys
from typing import List
import heapq

from helpers import AbstractMinimumSpanningTree, parse_txt_as_graph

INF = sys.maxsize

class Prim(AbstractMinimumSpanningTree):
    def __init__(self):
        self.dist = None

    def run(self, adj: List[List[int]]) -> int:
        vertices: List[list] = [[INF, -1, i] for i in range(len(adj))]
        vertices[0][0] = 0

        minHeap = vertices[:]
        while minHeap:
            a = heapq.heappop(minHeap)
            for m, weight in enumerate(adj[a[2]]):
                b = vertices[m]
                if b in minHeap and weight < b[0] and weight != 0:
                    b[1] = a[2]
                    b[0] = weight
            heapq.heapify(minHeap)

        cost = sum(key for key, _, _ in vertices)
        return cost

class Kruskal(AbstractMinimumSpanningTree):
    class DisjointSets:
        def __init__(self, n: int):
            self.parent = [-1 for _ in range(n)]
            self.set_size = n

        def __call__(self):
            return self.parent

        def find(self, id: int) -> int:
            while self.parent[id] >= 0:
                id = self.parent[id]
            return id

        def union(self, s1: int, s2: int):
            self.parent[s1] = s2
            self.set_size = self.set_size - 1

    def __init__(self):
        self.dist = None
        self.sum = 0

    def run(self, adj: List[List[int]]) -> int:
        ds = self.DisjointSets(len(adj))
        edges = []
        [edges.append([weight, m, n]) for m, neighbor in enumerate(adj) for n, weight in enumerate(neighbor) if weight != 0 and n > m]
        edges.sort()

        cost = 0
        for i, j, k in edges:
            u = ds.find(j)
            v = ds.find(k)
            if u != v:
                cost += i
                ds.union(v, u)
        return cost


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mst_type", type=str, default="prim",
                        choices=["prim", "kruskal"], help="Choose MST algorithm.")
    parser.add_argument("--path", type=str, default="graph0.txt", help="Input file path")
    args = parser.parse_args()

    algos_dict = {"prim": Prim(),
                  "kruskal": Kruskal()}

    adj = parse_txt_as_graph(args.path)
    mst_algorithm = algos_dict[args.mst_type]
    total_weight = mst_algorithm.run(adj)
    print(total_weight)
