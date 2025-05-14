# Router Optimizer

## Visão Geral
O **Router Optimizer** foi desenvolvido como parte da entrega da **Sprint 4** na challenge, em parceria com a empresa **Rede Âncora**, uma das maiores distribuidoras do Brasil e pioneira no modelo exclusivo de franquia no segmento de autopeças.

Este projeto foca na implementação de **Programação Dinâmica** e **Grafos**, resolvendo desafios de otimização de rotas e cálculos de menor caminho.

## Objetivos do Projeto
1. **Aplicação de Grafos**  
   Implementar uma função que, com base em um conjunto de lojas cadastradas e o endereço do comprador, utiliza **Grafos** para representar cada loja e calcular a menor distância entre elas. A distância (em km) será o peso dos vértices do grafo.  
   - Utilização de APIs para obter latitude e longitude e calcular a distância entre pontos.

2. **Algoritmo de Dijkstra**  
   Desenvolver uma função para otimizar a rota de entregas de um caminhão da **Rede Âncora**, encontrando o menor caminho para atender **N endereços** em um único dia.

## Tecnologias Utilizadas
- `networkx` – manipulação de grafos
- `pandas` – tratamento de dados
- `matplotlib` – visualização dos resultados
- `geopy` – cálculo de distâncias geográficas

## Como Executar o Projeto
1. Instale as dependências:  
   pip install -r requirements.txt
   python main.py

## Integrantes do grupo
- Beatriz Dantas Sampaio - 554044
- Giovanna Franco Gaudino Rodrigues - 553701
- Isabela Barcellos Freire - 553746
