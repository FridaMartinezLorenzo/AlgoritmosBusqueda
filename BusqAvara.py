import math

def leer_grafo_con_pesos_desde_archivo(ruta):
    grafo = {}
    with open(ruta, 'r') as archivo:
        for linea in archivo:
            if linea.strip():
                nodo, hijos = linea.strip().split(':', 1)
                nodo = nodo.strip().replace('"', '')
                hijos = hijos.strip().strip('[]').replace(' ', '')
                lista_hijos = []
                if hijos:
                    for hijo_peso in hijos.split(','):
                        hijo, peso = hijo_peso.split(':')
                        lista_hijos.append((hijo.strip(), int(peso.strip())))
                grafo[nodo] = lista_hijos
    return grafo


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


def calcular_heuristica(coordenadas, objetivo):
    heuristica = {}
    x_goal, y_goal = coordenadas[objetivo]
    for nodo, (x, y) in coordenadas.items():
        heuristica[nodo] = math.sqrt((x - x_goal) ** 2 + (y - y_goal) ** 2)
    return heuristica


def busqueda_avara_con_costos(grafo, heuristica, nodo_inicio, nodo_meta):
    nodos = [nodo_inicio]  # lista ordenada por heurística
    padres = {nodo_inicio: None}
    visitados = set()
    costo_total = {nodo_inicio: 0}  # Costo acumulado al nodo inicio (0)

    while nodos:
        print("Lista de nodos:", nodos)
        nodo = nodos.pop(0)  # Expandimos el primero (menor heurística)
        print("Expandimos:", nodo)

        if nodo == nodo_meta:
            # Construir el camino
            camino = []
            actual = nodo_meta
            while actual is not None:
                camino.insert(0, actual)
                actual = padres[actual]
            return camino, costo_total[nodo_meta]

        visitados.add(nodo)

        hijos = []
        for hijo, peso in grafo.get(nodo, []):
            if hijo not in visitados and hijo not in nodos:
                padres[hijo] = nodo
                costo_total[hijo] = costo_total[nodo] + peso  # Actualizamos el costo acumulado
                hijos.append(hijo)

        # Ordenar los hijos por heurística
        hijos.sort(key=lambda x: heuristica[x])
        print("Hijos ordenados por heurística:", hijos)

        # Insertar cada hijo en su posición correspondiente
        for hijo in hijos:
            i = 0
            while i < len(nodos) and heuristica[hijo] >= heuristica[nodos[i]]:
                i += 1
            nodos.insert(i, hijo)

    return None, None  # No se encontró camino


#Main
# Leer grafo con pesos como antes
grafo = leer_grafo_con_pesos_desde_archivo("grafo_pesado.txt")
print("Grafo")
print(grafo)
# Leer coordenadas y calcular heurística
coordenadas = leer_coordenadas_desde_archivo("coordenadas.txt")
heuristica = calcular_heuristica(coordenadas, 'F')
print("La heuristica:\n", heuristica)
# Ejecutar búsqueda voraz
camino = busqueda_avara_con_costos(grafo, heuristica, 'A', 'F')

if camino:
    print("Camino encontrado:", camino)
else:
    print("No se encontró un camino.")

