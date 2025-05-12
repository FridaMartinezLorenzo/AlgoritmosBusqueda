import matplotlib.pyplot as plt
import networkx as nx

def leer_grafo_desde_archivo(ruta):
    grafo = {}
    with open(ruta, 'r') as archivo:
        for linea in archivo:
            if linea.strip():
                nodo, hijos = linea.strip().split(':')
                nodo = nodo.strip().replace('"', '')
                hijos = hijos.strip().strip('[]').replace(' ', '')
                lista_hijos = hijos.split(',') if hijos else []
                grafo[nodo] = lista_hijos
    return grafo

import matplotlib.pyplot as plt
import networkx as nx

def dibujar_grafo(grafo, camino=None, coordenadas=None):
    G = nx.DiGraph()

    # Construir el grafo desde estructura
    for nodo, hijos in grafo.items():
        for hijo in hijos:
            if isinstance(hijo, tuple):
                G.add_edge(nodo, hijo[0], weight=hijo[1])
            else:
                G.add_edge(nodo, hijo)

    # Usar coordenadas como posiciones si existen
    if coordenadas:
        pos = coordenadas
    else:
        pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(12, 8))

    # Dibujar el grafo base
    nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color='gray',
            node_size=700, font_weight='bold', font_size=10)

    if coordenadas:
        coord_labels = {nodo: f"({int(x)},{int(y)})" for nodo, (x, y) in coordenadas.items()}

        # Crear nueva posición desplazada para las coordenadas (debajo del nodo)
        pos_coordenadas = {nodo: (x, y - 0.2) for nodo, (x, y) in pos.items()}  # Puedes ajustar -0.1

        nx.draw_networkx_labels(G, pos_coordenadas, labels=coord_labels, font_size=8, font_color='black')

    # Resaltar camino si hay
    if camino:
        edges_destacados = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges_destacados, edge_color='red', width=2)
        nx.draw_networkx_nodes(G, pos, nodelist=camino, node_color='orange')

    # Dibujar pesos si existen
    edge_labels = nx.get_edge_attributes(G, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Grafo con camino y datos educativos")
    plt.axis("off")
    plt.tight_layout()
    plt.show()



import matplotlib.pyplot as plt
import networkx as nx
from collections import deque, defaultdict

import matplotlib.pyplot as plt
import networkx as nx
from collections import deque, defaultdict

def dibujar_arbol(padres, nodo_raiz="A", grafo_original=None, coordenadas=None):
    G = nx.DiGraph()
    niveles = {}
    hijos_por_nivel = defaultdict(list)

    # Construir árbol desde diccionario de padres
    for hijo, padre in padres.items():
        if padre is not None:
            peso = None
            if grafo_original and padre in grafo_original:
                for destino in grafo_original[padre]:
                    if isinstance(destino, tuple) and destino[0] == hijo:
                        peso = destino[1]
                        break
            if peso is not None:
                G.add_edge(padre, hijo, weight=peso)
            else:
                G.add_edge(padre, hijo)

    # Si el grafo está vacío
    if not G:
        print("⚠️ Árbol vacío.")
        return

    # Calcular niveles por BFS
    cola = deque([(nodo_raiz, 0)])
    visitados = set()

    while cola:
        nodo, nivel = cola.popleft()
        if nodo in visitados:
            continue
        visitados.add(nodo)
        niveles[nodo] = nivel
        hijos_por_nivel[nivel].append(nodo)
        for hijo in G.successors(nodo):
            cola.append((hijo, nivel + 1))

    # Asignar posiciones (layout jerárquico vertical)
    pos = {}
    for nivel, nodos in hijos_por_nivel.items():
        ancho = len(nodos)
        for i, nodo in enumerate(nodos):
            pos[nodo] = (i - ancho / 2, -nivel)

    plt.figure(figsize=(12, 8))

    # Dibujar árbol base
    nx.draw(G, pos, with_labels=True, node_size=800, node_color='lightblue',
            font_weight='bold', font_size=10, arrows=True)

    # Dibujar pesos si hay
    edge_labels = nx.get_edge_attributes(G, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    # Dibujar coordenadas si se proporcionan
    if coordenadas:
        coord_labels = {nodo: f"({int(x)},{int(y)})" for nodo, (x, y) in coordenadas.items() if nodo in pos}
        pos_coord = {nodo: (x, y - 0.2) for nodo, (x, y) in pos.items()}
        nx.draw_networkx_labels(G, pos_coord, labels=coord_labels, font_size=8, font_color='black')

    plt.title(f"Árbol de expansión desde {nodo_raiz}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
