# src/algorithms.py
from typing import Dict, Tuple, List, Optional
import heapq
from collections import deque
from .graph import Graph

def bfs(g: Graph, start: str, goal: str) -> Optional[List[str]]:
    """Unweighted shortest path (by hops)."""
    q = deque([start])
    parent = {start: None}
    while q:
        u = q.popleft()
        if u == goal:
            break
        for v, _ in g.neighbors(u):
            if v not in parent:
                parent[v] = u
                q.append(v)
    if goal not in parent:
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]

def dijkstra(g: Graph, start: str, goal: str) -> Optional[Tuple[float, List[str]]]:
    """Weighted shortest path (non-negative)."""
    dist = {start: 0.0}
    parent = {start: None}
    pq = [(0.0, start)]
    while pq:
        du, u = heapq.heappop(pq)
        if u == goal:
            break
        if du > dist.get(u, float('inf')):
            continue
        for v, w in g.neighbors(u):
            nd = du + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
    if goal not in dist:
        return None
    # rebuild path
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return dist[goal], path[::-1]

def astar(g: Graph, start: str, goal: str) -> Optional[Tuple[float, List[str]]]:
    """A* with Euclidean heuristic from node coordinates."""
    h = lambda u: g.distance_xy(u, goal)
    gscore = {start: 0.0}
    fscore = {start: h(start)}
    parent = {start: None}
    openpq = [(fscore[start], start)]
    closed = set()

    while openpq:
        _, u = heapq.heappop(openpq)
        if u == goal:
            # reconstruct path
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return gscore[goal], path[::-1]
        if u in closed:
            continue
        closed.add(u)
        for v, w in g.neighbors(u):
            tentative = gscore[u] + w
            if tentative < gscore.get(v, float('inf')):
                parent[v] = u
                gscore[v] = tentative
                fscore[v] = tentative + h(v)
                heapq.heappush(openpq, (fscore[v], v))
    return None
