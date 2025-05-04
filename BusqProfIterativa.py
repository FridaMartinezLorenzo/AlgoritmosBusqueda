def leer_grafo_desde_archivo(ruta):
    grafo = {}
    with open(ruta, 'r') as archivo:
        for linea in archivo:
            if linea.strip():  # Evita líneas vacías
                nodo, hijos = linea.strip().split(':')
                nodo = nodo.strip().replace('"', '')
                hijos = hijos.strip().strip('[]').replace(' ', '')
                lista_hijos = hijos.split(',') if hijos else []
                grafo[nodo] = lista_hijos
    return grafo

def busquedaProfundidadLimitada(grafo, nodo_inicio, nodo_meta, profundidad_maxima):
    nodos = [(nodo_inicio, 0)]  # pila: (nodo, profundidad)
    padres = {nodo_inicio: None}

    while nodos:
        print("Nodos: ", nodos)
        nodo, profundidad = nodos.pop()
        print(f"Nodo: {nodo}, Profundidad: {profundidad}")

        if nodo == nodo_meta:
            # Construir camino
            camino = []
            actual = nodo_meta
            while actual is not None:
                camino.insert(0, actual)
                actual = padres[actual]
            return camino

        if profundidad < profundidad_maxima:
            for hijo in reversed(grafo.get(nodo, [])):
                print("hijo:", hijo)
                if padres[nodo] is not None and hijo == padres[nodo]:
                    continue  # Saltar al padre
                if hijo not in padres:
                    padres[hijo] = nodo
                    nodos.append((hijo, profundidad + 1))

    return None  # No se encontró el nodo meta

def busquedaProfundizacionIterativa(grafo, nodo_inicio, nodo_meta, profundidad_maxima_max):
    for limite in range(profundidad_maxima_max + 1):
        print(f"\n👉 Buscando con límite de profundidad: {limite}")
        camino = busquedaProfundidadLimitada(grafo, nodo_inicio, nodo_meta, limite)
        if camino is not None:
            return camino
    return None  # No se encontró el nodo meta en ninguna profundidad

# MAIN
ruta_archivo = 'grafo.txt'
grafo = leer_grafo_desde_archivo(ruta_archivo)
print("Grafo:", grafo)

camino = busquedaProfundizacionIterativa(grafo, 'A', 'F', 5)
if camino:
    print("Camino encontrado:", camino)
else:
    print("No se encontró un camino.")