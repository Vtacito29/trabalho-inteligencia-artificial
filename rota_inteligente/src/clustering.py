# src/clustering.py
from typing import List, Dict, Tuple
import random
from math import sqrt

def kmeans(points: Dict[str, Tuple[float, float]], k: int, max_iter: int = 100, seed: int = 42):
    """Simple K-Means returning (assignments, centroids)."""
    random.seed(seed)
    keys = list(points.keys())
    centroids = [points[k] for k in random.sample(keys, k)]
    for _ in range(max_iter):
        # assignment
        clusters = {i: [] for i in range(k)}
        for key, (x,y) in points.items():
            dists = [sqrt((x-cx)**2 + (y-cy)**2) for (cx,cy) in centroids]
            idx = min(range(k), key=lambda i: dists[i])
            clusters[idx].append(key)
        # recompute
        new_centroids = []
        for i in range(k):
            if clusters[i]:
                xs = [points[p][0] for p in clusters[i]]
                ys = [points[p][1] for p in clusters[i]]
                new_centroids.append((sum(xs)/len(xs), sum(ys)/len(ys)))
            else:
                new_centroids.append(centroids[i])
        if all(abs(new_centroids[i][0]-centroids[i][0])<1e-6 and abs(new_centroids[i][1]-centroids[i][1])<1e-6 for i in range(k)):
            break
        centroids = new_centroids
    assignments = {}
    for i, pts in clusters.items():
        for key in pts:
            assignments[key] = i
    return assignments, centroids
