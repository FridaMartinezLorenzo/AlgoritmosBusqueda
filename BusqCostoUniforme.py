import math

def leer_grafo_y_coordenadas(ruta):
    grafo = {}
    coordenadas = {}

    with open(ruta, 'r') as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            izq, der = linea.strip().split(':', 1)
            nombre, coord_str = izq.split('=')
            nodo = nombre.strip()
            x, y = coord_str.strip('() ').split(',')
            coordenadas[nodo] = (float(x), float(y))

            der = der.strip().strip('[]').replace(' ', '')
            lista_hijos = []
            if der:
                for hijo_peso in der.split(','):
                    hijo, peso = hijo_peso.split(':')
                    lista_hijos.append((hijo.strip(), int(peso.strip())))
            grafo[nodo] = lista_hijos

    return grafo, coordenadas

def busqueda_costo_uniforme(grafo, nodo_inicio, nodo_meta):
    nodos = [(nodo_inicio, 0)]  # (nodo, costo acumulado)
    padres = {nodo_inicio: None}
    costos = {nodo_inicio: 0}
    visitados = set()

    while nodos:
        # Ordenar por costo acumulado
        nodos.sort(key=lambda x: x[1])
        print("Lista de nodos con costo acumulado:", [(n, c) for n, c in nodos])
        nodo, costo_actual = nodos.pop(0)

        if nodo in visitados:
            continue  # Ya lo exploramos completamente

        print("Expandimos:", nodo)
        visitados.add(nodo)

        if nodo == nodo_meta:
            camino = []
            actual = nodo
            while actual is not None:
                camino.insert(0, actual)
                actual = padres[actual]
            return camino, costos[nodo]

        for hijo, peso in grafo.get(nodo, []):
            nuevo_costo = costo_actual + peso
            if hijo not in costos or nuevo_costo < costos[hijo]:
                costos[hijo] = nuevo_costo
                padres[hijo] = nodo
                if hijo not in visitados:
                    nodos.append((hijo, nuevo_costo))

    return None, None

# Main

from dibujar_grafo import dibujar_grafo, dibujar_arbol

def reconstruir_padres(camino):
    if not camino:
        return {}
    return {camino[i]: camino[i-1] for i in range(1, len(camino))} | {camino[0]: None}

#grafo = leer_grafo_con_pesos_desde_archivo("grafo_bifurcado.txt")
#print("Grafo:\n", grafo)

#coordenadas = leer_coordenadas_desde_archivo("coordenadas_bifurcado.txt")
#camino, costo = busqueda_costo_uniforme(grafo, 'A', 'J')

grafo, coordenadas = leer_grafo_y_coordenadas('graph.txt')

camino, costo = busqueda_costo_uniforme(grafo, 'A', 'E')

if camino:
    padres = reconstruir_padres(camino)
    dibujar_grafo(grafo, camino, coordenadas)
    dibujar_arbol(padres, nodo_raiz='A', grafo_original=grafo, coordenadas=coordenadas)
else:
    print("No se encontró un camino.")

print("Grafo:", grafo)

print('A' in grafo, 'F' in grafo)
