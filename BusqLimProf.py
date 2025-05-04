def leer_grafo_desde_archivo(ruta):
    grafo = {}
    with open(ruta, 'r') as archivo:
        for linea in archivo:
            if linea.strip():  # Evita líneas vacías
                # Elimina comillas y espacios
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
            for hijo in reversed(grafo.get(nodo, [])):  # 👉 usamos reversed aquí
                print("hijo:", hijo)
                if padres[nodo] is not None and hijo == padres[nodo]:
                    continue  # Saltar al padre
                if hijo not in padres:
                    padres[hijo] = nodo
                    nodos.append((hijo, profundidad + 1))  # directo a la pila

    return None  # No se encontró el nodo meta

#Main
ruta_archivo = 'grafo.txt' 
grafo = leer_grafo_desde_archivo(ruta_archivo)
print("grafo", grafo);
print("grafo A", grafo.get("A",[]))
camino = busquedaProfundidadLimitada(grafo, 'A', 'F',3)
if camino:
    print("Camino encontrado:", camino)
else:
    print("No se encontró un camino.")