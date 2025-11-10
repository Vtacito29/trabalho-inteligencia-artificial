# main.py - Rota Inteligente: Otimização de Entregas com IA
"""
Como executar:
    python main.py --k 2 --deliveries A B C D E
Descrição:
    - Carrega um grafo de cidade (data/city_nodes.csv, data/city_edges.csv)
    - Agrupa entregas por K-Means (k = número de entregadores)
    - Para cada cluster, calcula a melhor rota (A*) do DEPOT até a sequência de pontos (heurística do vizinho mais próximo + A* entre pares)
Saídas esperadas:
    - Impressão no console com clusters, rotas e custos
    - Figura docs/graph.png com o grafo desenhado
"""
import csv, argparse
from pathlib import Path
from typing import List, Dict, Tuple
from src.graph import Graph
from src.algorithms import astar
from src.clustering import kmeans

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DOCS = BASE / "docs"

def load_graph(nodes_csv: Path, edges_csv: Path) -> Graph:
    g = Graph()
    with open(nodes_csv, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            g.add_node(row["node"], float(row["x"]), float(row["y"]))
    with open(edges_csv, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            g.add_edge(row["u"], row["v"], float(row["weight"]), undirected=False)
    return g

def nearest_neighbor_order(g: Graph, start: str, stops: List[str]) -> List[str]:
    remaining = set(stops)
    order = []
    cur = start
    while remaining:
        nxt = min(remaining, key=lambda s: g.distance_xy(cur, s))
        order.append(nxt)
        remaining.remove(nxt)
        cur = nxt
    return order

def route_cost_and_path(g: Graph, start: str, ordered: List[str]) -> Tuple[float, List[str]]:
    total = 0.0
    full_path = [start]
    cur = start
    for target in ordered:
        res = astar(g, cur, target)
        if res is None:
            raise RuntimeError(f"Sem caminho entre {cur} e {target}")
        cost, path = res
        total += cost
        full_path += path[1:]
        cur = target
    return total, full_path

def main(k: int, deliveries: List[str]):
    g = load_graph(DATA / "city_nodes.csv", DATA / "city_edges.csv")
    depot = "DEPOT"

    pts = {d: g.coords[d] for d in deliveries}
    assignments, centroids = kmeans(pts, k=k, seed=7)

    clusters: Dict[int, List[str]] = {}
    for d, cid in assignments.items():
        clusters.setdefault(cid, []).append(d)

    print(f"Entregadores (k) = {k}")
    for cid in sorted(clusters):
        stops = clusters[cid]
        order = nearest_neighbor_order(g, depot, stops)
        cost, path = route_cost_and_path(g, depot, order)
        print(
            f"""\nCluster {cid}: pontos {stops}\nOrdem sugerida: {order}\nRota completa: {path}\nCusto total estimado: {cost:.3f}"""
        )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=2, help="Número de entregadores (clusters)")
    parser.add_argument("--deliveries", nargs="+", default=["A","B","C","D","E","F"], help="Lista de paradas")
    args = parser.parse_args()
    main(args.k, args.deliveries)
