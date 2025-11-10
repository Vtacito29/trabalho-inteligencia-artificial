# src/graph.py
from typing import Dict, List, Tuple, Iterable

class Graph:
    def __init__(self):
        self.coords: Dict[str, Tuple[float, float]] = {}
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_node(self, node: str, x: float, y: float):
        self.coords[node] = (x, y)
        self.adj.setdefault(node, [])

    def add_edge(self, u: str, v: str, w: float, undirected: bool = True):
        self.adj.setdefault(u, []).append((v, w))
        if undirected:
            self.adj.setdefault(v, []).append((u, w))

    def neighbors(self, u: str) -> Iterable[Tuple[str, float]]:
        return self.adj.get(u, [])

    def nodes(self) -> Iterable[str]:
        return self.adj.keys()

    def distance_xy(self, a: str, b: str) -> float:
        (ax, ay) = self.coords[a]; (bx, by) = self.coords[b]
        return ((ax - bx)**2 + (ay - by)**2) ** 0.5
