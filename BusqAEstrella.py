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
        heuristica[nodo] = math.sqrt((x - x_goal)**2 + (y - y_goal)**2)
    return heuristica

def busqueda_a_estrella(grafo, heuristica, nodo_inicio, nodo_meta):
    nodos = [(nodo_inicio, 0)]  # tupla (nodo, costo acumulado)
    padres = {nodo_inicio: None}
    costos = {nodo_inicio: 0}
    visitados = set()

    while nodos:
        # Ordenar la lista por f(n) = g(n) + h(n)
        nodos.sort(key=lambda x: costos[x[0]] + heuristica[x[0]])
        print("Lista de nodos con f(n):", [(n, round(costos[n] + heuristica[n], 2)) for n, _ in nodos])
        nodo, _ = nodos.pop(0)
        print("Expandimos:", nodo)

        if nodo == nodo_meta:
            camino = []
            actual = nodo_meta
            while actual is not None:
                camino.insert(0, actual)
                actual = padres[actual]
            return camino, costos[nodo_meta]

        visitados.add(nodo)

        for hijo, peso in grafo.get(nodo, []):
            nuevo_costo = costos[nodo] + peso
            if hijo not in costos or nuevo_costo < costos[hijo]:
                costos[hijo] = nuevo_costo
                padres[hijo] = nodo
                if hijo not in visitados:
                    nodos.append((hijo, nuevo_costo))

    return None, None

# Main
grafo = leer_grafo_con_pesos_desde_archivo("grafo_pesado.txt")
print("Grafo:\n", grafo)

coordenadas = leer_coordenadas_desde_archivo("coordenadas.txt")
heuristica = calcular_heuristica(coordenadas, 'F')
print("Heurística (distancia euclidiana a F):\n", heuristica)

camino, costo = busqueda_a_estrella(grafo, heuristica, 'A', 'F')

if camino:
    print("Camino encontrado:", camino)
    print(f"Costo total: {costo}")
else:
    print("No se encontró un camino.")
