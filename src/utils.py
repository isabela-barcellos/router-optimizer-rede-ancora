#Função que calcula a distância, resultando no peso. 
from geopy.distance import geodesic 

def calcular_distancia(coord1, coord2):
    #calcula a distância entre as duas cordenadas. 
    return round(geodesic(coord1, coord2).km, 2)
