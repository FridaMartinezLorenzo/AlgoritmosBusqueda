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

def calcular_heuristica(coordenadas, objetivo):
    heuristica = {}
    x_goal, y_goal = coordenadas[objetivo]
    for nodo, (x, y) in coordenadas.items():
        heuristica[nodo] = math.sqrt((x - x_goal)**2 + (y - y_goal)**2)
    return heuristica

def busqueda_a_estrella(grafo, heuristica, nodo_inicio, nodo_meta):
    nodos = [(nodo_inicio, 0)]  # tupla (nodo, costo acumulado g(n))
    padres = {nodo_inicio: None}
    costos = {nodo_inicio: 0}
    visitados = set()

    while nodos:
        # Ordenar por f(n) = g(n) + h(n)
        nodos.sort(key=lambda x: costos[x[0]] + heuristica[x[0]])
        print("Lista de nodos con f(n):", [(n, round(costos[n] + heuristica[n], 2)) for n, _ in nodos])
        nodo, _ = nodos.pop(0)

        if nodo in visitados:
            continue  # Ya fue expandido

        print("Expandimos:", nodo)
        visitados.add(nodo)

        if nodo == nodo_meta:
            camino = []
            actual = nodo
            while actual is not None:
                camino.insert(0, actual)
                actual = padres[actual]
            return camino, costos[nodo], padres

        for hijo, peso in grafo.get(nodo, []):
            nuevo_costo = costos[nodo] + peso
            if (hijo not in costos or nuevo_costo < costos[hijo]) and hijo not in visitados:
                costos[hijo] = nuevo_costo
                padres[hijo] = nodo
                nodos.append((hijo, nuevo_costo))

    return None, None, padres

# Main

from dibujar_grafo import dibujar_grafo, dibujar_arbol

grafo, coordenadas = leer_grafo_y_coordenadas("graph.txt")
heuristica = calcular_heuristica(coordenadas, 'J')  # Cambia el nodo meta si es otro

camino, costo, padres = busqueda_a_estrella(grafo, heuristica, 'A', 'J')

if camino:
    print("Camino encontrado:", camino)
    print("Costo total:", costo)
    dibujar_grafo(grafo, camino, coordenadas)
    dibujar_arbol(padres, nodo_raiz='A', grafo_original=grafo, coordenadas=coordenadas)
else:
    print("No se encontró un camino.")


#grafo = leer_grafo_con_pesos_desde_archivo("grafo_bifurcado.txt")
#print("Grafo:\n", grafo)
#
#coordenadas = leer_coordenadas_desde_archivo("coordenadas_bifurcado.txt")
#heuristica = calcular_heuristica(coordenadas, 'J')  # heurística hacia el nodo meta
#print("Heurística (distancia euclidiana a J):\n", heuristica)
#
#camino, costo = busqueda_a_estrella(grafo, heuristica, 'A', 'J')
#
#if camino:
#    print("Camino encontrado:", camino)
#    print(f"Costo total: {costo}")
#else:
#    print("No se encontró un camino.")
