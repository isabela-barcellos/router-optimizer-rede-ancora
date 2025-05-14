import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from data.lojas import lojas
from geopy.distance import geodesic
from itertools import permutations
from data.entregas import enderecos 

#Exercício 1
# Comprador e sua localização
comprador = {'nome': 'Comprador -SP - Av Paulista', 'coordenadas': (-23.561684, -46.625378)}
pontos = [comprador] + lojas

# Criar grafo e conectar pontos com distância geográfica
G = nx.Graph()
for ponto in pontos:
    G.add_node(ponto['nome'], pos=ponto['coordenadas'])

for i in range(len(pontos)):
    for j in range(i + 1, len(pontos)):
        distancia = round(geodesic(pontos[i]['coordenadas'], pontos[j]['coordenadas']).km, 2)
        G.add_edge(pontos[i]['nome'], pontos[j]['nome'], weight=distancia)

# Encontrar a loja mais próxima
loja_mais_proxima = min(lojas, key=lambda loja: G[comprador['nome']][loja['nome']]['weight'])
caminho = nx.shortest_path(G, source=comprador['nome'], target=loja_mais_proxima['nome'], weight='weight')
distancia = nx.shortest_path_length(G, source=comprador['nome'], target=loja_mais_proxima['nome'], weight='weight')

# Exibir resultado
print("\nMenor caminho até a loja mais próxima:")
print(" -> ".join(caminho))
print(f"Distância total: {distancia:.2f} km\n")

# Visualização com distâncias nas arestas
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800)
nx.draw_networkx_edges(G, pos, edgelist=list(zip(caminho[:-1], caminho[1:])), edge_color='red', width=2)

# Adiciona rótulos de distância nas arestas
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.2f} km" for k, v in labels.items()}, font_size=8)

plt.show()

#Exercício 2  
# Criar grafo e conectar pontos com distância geográfica
G = nx.Graph()
for nome1, coord1 in enderecos.items():
    for nome2, coord2 in enderecos.items():
        if nome1 != nome2:
            distancia = round(geodesic(coord1, coord2).km, 2)
            G.add_edge(nome1, nome2, weight=distancia)

# Encontrar a melhor rota de entrega
entregas = [e for e in enderecos if e != 'Origem']
melhor_rota = None
menor_distancia = float('inf')

for perm in permutations(entregas):
    rota = ['Origem'] + list(perm)
    distancia_total = sum(nx.dijkstra_path_length(G, rota[i], rota[i+1], weight='weight') for i in range(len(rota) - 1))

    if distancia_total < menor_distancia:
        menor_distancia = distancia_total
        melhor_rota = rota

# Exibir resultado
print("\nMelhor caminho para realizar a entrega:")
print(" -> ".join(melhor_rota))
print(f"Distância total: {menor_distancia:.2f} km\n")

# Visualização com distâncias nas arestas
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800)
nx.draw_networkx_edges(G, pos, edgelist=list(zip(melhor_rota[:-1], melhor_rota[1:])), edge_color='red', width=2)

# Adiciona rótulos de distância nas arestas
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.2f} km" for k, v in labels.items()}, font_size=8)

plt.show()