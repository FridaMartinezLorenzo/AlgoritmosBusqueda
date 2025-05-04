import math
import heapq  # para la cola de prioridad

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



def busqueda_avara(grafo, heuristica, nodo_inicio, nodo_meta):
    frontera = []  # Cola de prioridad
    heapq.heappush(frontera, (heuristica[nodo_inicio], nodo_inicio))
    
    padres = {nodo_inicio: None}
    visitados = set()

    while frontera:
        _, nodo_actual = heapq.heappop(frontera)
        
        print(f"Visitando: {nodo_actual}")
        
        if nodo_actual == nodo_meta:
            # Reconstruir el camino
            camino = []
            while nodo_actual is not None:
                camino.insert(0, nodo_actual)
                nodo_actual = padres[nodo_actual]
            return camino

        visitados.add(nodo_actual)

        for vecino, peso in grafo.get(nodo_actual, []):
            if vecino not in visitados and vecino not in [n for _, n in frontera]:
                padres[vecino] = nodo_actual
                heapq.heappush(frontera, (heuristica[vecino], vecino))

    return None  # no se encontró camino



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
camino = busqueda_avara(grafo, heuristica, 'A', 'F')

if camino:
    print("Camino encontrado:", camino)
else:
    print("No se encontró un camino.")

