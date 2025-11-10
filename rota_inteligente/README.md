# Rota Inteligente — Otimização de Entregas com IA

> Projeto acadêmico: **Artificial Intelligence Fundamentals** — solução aplicada à empresa fictícia **Sabor Express**.
> Cidade modelada como **grafo**; uso de **A*** para menor caminho e **K-Means** para agrupar entregas por zona.

## 🎯 Objetivo
Encontrar **rotas eficientes** e **organizar entregas por proximidade** em horários de pico, reduzindo tempo e custo operacional.

## 🧩 Abordagem
- **Grafo**: nós = bairros/pontos de entrega; arestas = ruas com peso (distância/tempo).
- **Menor caminho**: A* com heurística **euclidiana** (coordenadas dos nós).
- **Clustering**: **K-Means** (implementação própria) para criar zonas por entregador.
- **Heurística de turnê**: ordem inicial por **vizinho mais próximo** e ligação entre paradas com A*.

## 📂 Estrutura
```
rota_inteligente/
├── main.py
├── src/
│   ├── graph.py          # estrutura do grafo (coords + adjacência)
│   ├── algorithms.py     # BFS, Dijkstra e A*
│   └── clustering.py     # K-Means simples (sem dependências externas)
├── data/
│   ├── city_nodes.csv    # nós com coordenadas
│   └── city_edges.csv    # arestas com pesos
└── docs/
    └── graph.png         # diagrama do grafo (gerado)
```

## ▶️ Execução
Requer apenas Python 3.10+.
```
cd rota_inteligente
python main.py --k 2 --deliveries A B C D E
```
Exemplo de saída (pode variar conforme dados):
```
Entregadores (k) = 2

Cluster 0: pontos ['A', 'C', 'G', 'H']
Ordem sugerida: ['A', 'C', 'G', 'H']
Rota completa: ['DEPOT', 'A', 'C', 'G', 'H']
Custo total estimado: 9.842

Cluster 1: pontos ['B', 'D', 'E']
Ordem sugerida: ['B', 'D', 'E']
Rota completa: ['DEPOT', 'B', 'D', 'E']
Custo total estimado: 7.114
```

## 📈 Métricas e análise
- **Custo total**: soma dos pesos no caminho (proxy de tempo/combustível).
- **Balanceamento por cluster**: número de paradas por entregador (ajuste `k`).
- **Limitações**:
  - Ordem de visitas usa **vizinho mais próximo** (heurística simples para TSP).
  - Pesos estáticos; sem tráfego em tempo real.
- **Melhorias futuras**:
  - Inserir **janelas de tempo** por entrega (Time Windows).
  - Heurísticas TSP (2-opt/3-opt) e **meta-heurísticas**.
  - Integração com APIs de trânsito para pesos dinâmicos.

## 🧠 Algoritmos
- **A***: busca informada com heurística admissível (distância euclidiana).
- **Dijkstra**: baseline para caminhos mínimos.
- **BFS**: referência para grafo não ponderado.
- **K-Means**: atribuição iterativa ao centroide mais próximo.

## 🖼️ Diagrama do Grafo
Arquivo: `docs/graph.png` (gerado automaticamente com Matplotlib).

## 📜 Licença
Uso acadêmico.
