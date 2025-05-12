import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from data.lojas import lojas
from src.utils import calcular_distancia

# Comprador e sua localização
comprador = {'nome': 'Comprador -SP - Av Paulista', 'coordenadas': (-23.561684, -46.625378)}  # Localização do comprador na Av. Paulista, SP

# Lista com as lojas e o comprador
pontos = [comprador] + lojas

G = nx.Graph()  # Criando o grafo

# Adiciono todos os nós com base nas coordenadas.
for ponto in pontos:
    G.add_node(ponto['nome'], pos=ponto['coordenadas'])

# Conecta todos os pares de pontos e calcula a distância como peso
for i in range(len(pontos)):
    for j in range(i + 1, len(pontos)):
        ponto1 = pontos[i]
        ponto2 = pontos[j]
        distancia = calcular_distancia(ponto1['coordenadas'], ponto2['coordenadas'])  # Calcula a distância entre os pontos
        G.add_edge(ponto1['nome'], ponto2['nome'], weight=distancia)

# Arestas com base no peso (distância)
for u, v, d in G.edges(data=True):
    print(f"{u} <-> {v} | Distância: {d['weight']:.2f} km")

pos_original = nx.get_node_attributes(G, 'pos')  # Posições geográficas dos nós
pos = nx.spring_layout(G, k=0.8, iterations=200, pos=pos_original, fixed=[comprador['nome']])
labels = nx.get_edge_attributes(G, 'weight')  
fig, ax = plt.subplots(figsize=(16, 12))  # Tamanho do gráfico

# Desenha os nós no gráfico
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue', ax=ax)

# Cores das arestas: verde = perto, roxo = longe
weights = list(labels.values())
norm = plt.Normalize(min(weights), max(weights))  
edge_colors = plt.cm.viridis(norm(weights))

# Desenha as arestas no gráfico
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, edge_cmap=plt.cm.viridis, width=2, alpha=0.7, ax=ax)

# Barra de cores para mostrar a distância entre os pontos
sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.7, pad=0.02)
cbar.set_label('Distância (km)', fontsize=12)

# Labels nos nós
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', ax=ax)

# KM de todas as arestas (distâncias)
labels_todas = {(u, v): f"{d['weight']:.2f} km" for u, v, d in G.edges(data=True)}

# Desenha os labels nas arestas
nx.draw_networkx_edge_labels(
    G, pos, 
    edge_labels=labels_todas, 
    font_color='red', 
    font_size=6,   
    label_pos=0.3, 
    ax=ax, 
    rotate=False
)

# Título do gráfico
ax.set_title("Mapa de Comprador e Lojas - Grafo Completo com Distâncias", fontsize=18, fontweight='bold')
plt.axis('off')  
plt.tight_layout() 
plt.show()
