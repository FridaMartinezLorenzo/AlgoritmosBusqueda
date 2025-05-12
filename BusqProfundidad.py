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


def busquedaProfundidad(grafo, nodo_inicio, nodo_meta):
    nodos = [nodo_inicio] #Lo vamos a trabajar como una cola
    padres = {nodo_inicio: None}  # Guarda de dónde viene cada nodo

    while nodos:
        print("Nodos: ", nodos);
        nodo = nodos.pop(0)
        print("Nodo: ", nodo)
        if nodo == nodo_meta:
            # Construir camino
            camino = []
            actual = nodo_meta
            while actual is not None:
                camino.insert(0, actual)
                actual = padres[actual]
            return camino, padres  # Retorna el camino y los padres para el grafo
        
        #Expandir
        for hijo in reversed(grafo.get(nodo, [])):
            print("hijo:", hijo)
            if padres[nodo] is not None and hijo == padres[nodo]:
                continue  # Saltar al padre
            else:
                if hijo not in padres:  # Si no fue visitado ni en cola (porque solo entra a padres si ya fue agregado)
                    padres[hijo] = nodo
                    nodos.insert(0,hijo)
       
                
    return None,padres  # No se encontró el nodo meta

#Main
from dibujar_grafo import leer_grafo_desde_archivo, dibujar_grafo, dibujar_arbol

ruta_archivo = 'grafo_rumania.txt'
grafo = leer_grafo_desde_archivo(ruta_archivo)

# Ejecutamos la búsqueda
camino, padres = busquedaProfundidad(grafo, 'Arad', 'Bucharest')

# Dibujar camino encontrado
if camino:
    print("Camino encontrado:", camino)
    dibujar_grafo(grafo, camino)
else:
    print("No se encontró un camino.")
    dibujar_grafo(grafo)

# Mostrar árbol de expansión
dibujar_arbol(padres, nodo_raiz='Arad')

