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
            if '=' in linea:
                nodo, coord = linea.strip().split('=')
                nodo = nodo.strip()
                x, y = coord.strip('()').split(',')
                coordenadas[nodo] = (float(x), float(y))
    return coordenadas

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
grafo = leer_grafo_con_pesos_desde_archivo("grafo_bifurcado.txt")
print("Grafo:\n", grafo)

coordenadas = leer_coordenadas_desde_archivo("coordenadas_bifurcado.txt")
camino, costo = busqueda_costo_uniforme(grafo, 'A', 'J')

if camino:
    print("Camino encontrado:", camino)
    print(f"Costo total del camino: {costo}")
else:
    print("No se encontró un camino.")
