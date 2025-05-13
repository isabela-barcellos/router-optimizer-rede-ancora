import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from data.lojas import lojas
from src.utils import calcular_distancia

# Comprador e sua localização
comprador = {'nome': 'Comprador -SP - Av Paulista', 'coordenadas': (-23.561684, -46.625378)}

# Lista com as lojas e o comprador
pontos = [comprador] + lojas

G = nx.Graph()  # Criando o grafo

# Adiciona os nós com posições
for ponto in pontos:
    G.add_node(ponto['nome'], pos=ponto['coordenadas'])

# Conecta os pontos com arestas ponderadas pela distância
for i in range(len(pontos)):
    for j in range(i + 1, len(pontos)):
        ponto1 = pontos[i]
        ponto2 = pontos[j]
        distancia = calcular_distancia(ponto1['coordenadas'], ponto2['coordenadas'])
        G.add_edge(ponto1['nome'], ponto2['nome'], weight=distancia)

# Função para encontrar o menor caminho do comprador até a loja mais próxima
def encontrar_menor_caminho(grafo, comprador_nome, lojas):
    loja_mais_proxima = min(lojas, key=lambda loja: grafo[comprador_nome][loja['nome']]['weight'])
    caminho = nx.shortest_path(grafo, source=comprador_nome, target=loja_mais_proxima['nome'], weight='weight')
    distancia = nx.shortest_path_length(grafo, source=comprador_nome, target=loja_mais_proxima['nome'], weight='weight')
    return caminho, distancia

# Encontra o menor caminho
caminho, distancia = encontrar_menor_caminho(G, comprador['nome'], lojas)

# Exibe o caminho e a distância
print("\nMenor caminho até a loja mais próxima:")
for i in range(len(caminho) - 1):
    print(f"{caminho[i]} -> {caminho[i+1]}")
print(f"Distância total: {distancia:.2f} km")

# -------------------- PLOTAGEM --------------------

pos_original = nx.get_node_attributes(G, 'pos')
pos = nx.spring_layout(G, k=0.8, iterations=200, pos=pos_original, fixed=[comprador['nome']])
labels = nx.get_edge_attributes(G, 'weight')
fig, ax = plt.subplots(figsize=(16, 12))

nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue', ax=ax)

weights = list(labels.values())
norm = plt.Normalize(min(weights), max(weights))
edge_colors = plt.cm.viridis(norm(weights))

nx.draw_networkx_edges(G, pos, edge_color=edge_colors, edge_cmap=plt.cm.viridis, width=2, alpha=0.7, ax=ax)

# Destaca o menor caminho em vermelho
caminho_edges = list(zip(caminho[:-1], caminho[1:]))
nx.draw_networkx_edges(G, pos, edgelist=caminho_edges, edge_color='red', width=3, ax=ax)

# Barra de cores
sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.7, pad=0.02)
cbar.set_label('Distância (km)', fontsize=12)

nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', ax=ax)

# Labels das distâncias
labels_todas = {(u, v): f"{d['weight']:.2f} km" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=labels_todas,
    font_color='red',
    font_size=6,
    label_pos=0.3,
    ax=ax,
    rotate=False
)

ax.set_title("Mapa de Comprador e Lojas - Menor Caminho em Vermelho", fontsize=18, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.show()
