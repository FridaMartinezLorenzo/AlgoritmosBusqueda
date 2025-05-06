import matplotlib.pyplot as plt
import networkx as nx


def leer_coordenadas_desde_archivo(ruta):
    coordenadas = {}
    with open(ruta, 'r') as archivo:
        for linea in archivo:
            if linea.strip():
                nodo, coord = linea.strip().split('=')
                nodo = nodo.strip()
                x, y = coord.strip('() \n').split(',')
                coordenadas[nodo] = (float(x), float(y))
    return coordenadas



# Leer coordenadas desde archivo
pos = {}
pos = leer_coordenadas_desde_archivo("coordenadas.txt")
print("Coordenadas:", pos)

# Definir las aristas manualmente (ajústalas según tu grafo)
edges = [
    ('A', 'B'),
    ('A', 'C'),
    ('B', 'D'),
    ('B', 'E'),
    ('C', 'D'),
    ('D', 'E'),
    ('D', 'G'),
    ('E', 'F'),
    ('G', 'F')
]

# Crear y dibujar el grafo
G = nx.Graph()
G.add_nodes_from(pos.keys())
G.add_edges_from(edges)

plt.figure(figsize=(8,6))
nx.draw(G, pos, with_labels=True, node_size=700, node_color='pink', font_size=12, font_weight='bold', edge_color='black')
plt.show()
