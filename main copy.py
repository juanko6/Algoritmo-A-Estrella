import sys, pygame
from casilla import *
from Nodo import *
from mapa import *
from pygame.locals import *
import math

SELECCION_HEURISTICA = 2

# 1 para h = 0
# 2 para Manhattan, 
# 3 para Euclidiana, 
# 4 para Chebyshev
# 5 para Hamming
# 6 para Octil.

EXPERIMENTOS = 10  # Número de repeticiones por experimento
EPSILON_VALORES = [0.1, 0.5, 1, 2]  # Valores de ε para A*ε

MARGEN=5
MARGEN_INFERIOR=60
TAM=30
NEGRO=(0,0,0)
HIERBA=(250, 180, 160)
MURO=(30, 70, 140)
AGUA=(173, 216, 230) 
ROCA=(110, 75, 48)
AMARILLO=(255, 255, 0) 

#Declaracion de listas frontera e interior
LF=[] # estados alcanzados no seleccionados
LI=[] # estados seleccionados y expandidos

# Resultados almacenados
resultados_experimentos = []

# ---------------------------------------------------------------------
# Funciones analisis
# ---------------------------------------------------------------------


def contar_nodos_explorados(matriz_exploracion):
    """Contar el número de nodos explorados en la matriz de exploración."""
    return sum(1 for fila in matriz_exploracion for celda in fila if celda != -1)

def ejecutar_experimento(mapa, origen, destino, algoritmo="A*", epsilon=None):
    """Ejecutar un experimento con A* o A*ε y retornar las métricas de resultado."""
    camino = inic(mapa)
    nodos_explorados = 0
    coste_total = 0
    calorias_consumidas = 0

    if algoritmo == "A*":
        resultado = a_estrella(mapa, origen, destino, camino)
        if resultado is not None:
            camino, coste_total, matriz_exploracion = resultado
            nodos_explorados = contar_nodos_explorados(matriz_exploracion)
    elif algoritmo == "A*ε":
        resultado = a_estrella_epsilon(mapa, origen, destino, epsilon, camino)
        if resultado is not None:
            camino, coste_total, matriz_exploracion = resultado
            nodos_explorados = contar_nodos_explorados(matriz_exploracion)
            calorias_consumidas = cal  # Calorías acumuladas globalmente durante el experimento

    return {
        "algoritmo": algoritmo,
        "heuristica": SELECCION_HEURISTICA,
        "epsilon": epsilon,
        "nodos_explorados": nodos_explorados,
        "coste_total": coste_total,
        "calorias_consumidas": calorias_consumidas
    }

def ejecutar_experimentos_varios(mapa, origen, destino):
    """Ejecutar varios experimentos y almacenar los resultados."""
    global resultados_experimentos
    # Ejecutar A* con cada heurística
    for heuristica in range(2, 7):  # Heurísticas del 2 al 6
        global SELECCION_HEURISTICA
        SELECCION_HEURISTICA = heuristica
        for _ in range(EXPERIMENTOS):
            resultados_experimentos.append(ejecutar_experimento(mapa, origen, destino, "A*"))

    # Ejecutar A*ε con varios valores de epsilon
    for epsilon in EPSILON_VALORES:
        for heuristica in range(2, 7):
            SELECCION_HEURISTICA = heuristica
            for _ in range(EXPERIMENTOS):
                resultados_experimentos.append(ejecutar_experimento(mapa, origen, destino, "A*ε", epsilon))



# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino o como origen
def bueno(mapi, pos):
    res= False
    
    if mapi.getCelda(pos.getFila(),pos.getCol())==0 or mapi.getCelda(pos.getFila(),pos.getCol())==4 or mapi.getCelda(pos.getFila(),pos.getCol())==5:
        res=True
    
    return res
    
# Devuelve si una posición de la ventana corresponde al mapa
def esMapa(mapi, posicion):
    res=False     
    
    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True       
    
    return res
    
#Devuelve si se ha pulsado algún botón
def pulsaBoton(mapi, posicion):
    res=-1
    
    if posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-65 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-15 and \
        posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=1
    elif posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+15 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+65 and \
        posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=2

    return res

# Construye la matriz para guardar el camino
def inic(mapi):    
    cam=[]
    for i in range(mapi.alto):        
        cam.append([])
        for j in range(mapi.ancho):            
            cam[i].append('.')
    
    return cam

# Imprime la ubicación de origen y destino
def imprimir_origen_destino(origen, destino):
    print(f"Origen: Fila {origen.getFila()}, Columna {origen.getCol()}")
    print(f"Destino: Fila {destino.getFila()}, Columna {destino.getCol()}")

#funcion que hace una matriz con -1 para saber que nodos fueron explorados
def inicializar_matriz_exploracion(mapa):
    filas = len(mapa.mapa)
    columnas = len(mapa.mapa[0])
    matriz_exploracion = [[-1 for _ in range(columnas)] for _ in range(filas)]
    return matriz_exploracion

# Devuelve las posiciones adyacentes (octaconectadas) a una posición dada
def posiciones_adyacentes(posicion, mapi):
    fila = posicion.getFila()
    col = posicion.getCol()

    # Definimos las 8 direcciones: arriba, abajo, izquierda, derecha, y diagonales
    adyacentes = [
        Casilla(fila - 1, col),      # Arriba
        Casilla(fila + 1, col),      # Abajo
        Casilla(fila, col - 1),      # Izquierda
        Casilla(fila, col + 1),      # Derecha
        Casilla(fila - 1, col - 1),  # Diagonal superior izquierda
        Casilla(fila - 1, col + 1),  # Diagonal superior derecha
        Casilla(fila + 1, col - 1),  # Diagonal inferior izquierda
        Casilla(fila + 1, col + 1)   # Diagonal inferior derecha
    ]
    
    # Filtramos las posiciones válidas:
    # - Que estén dentro del rango del mapa
    # - Que sean seleccionables (sin obstáculos)
    posiciones_validas = [
        pos for pos in adyacentes
        if 0 <= pos.getFila() < mapi.getAlto() and  # Dentro de los límites del mapa
        0 <= pos.getCol() < mapi.getAncho() and
        bueno(mapi, pos)  # Es una posición seleccionable (sin obstáculos)
    ]
    
    return posiciones_validas


# Obtener el nodo de la lista frontera con menor f(n) = g(n) + h(n)
def obtener_nodo_con_menor_f_heuristica(lista_frontera, objetivo):
    # Inicializamos el nodo con menor f como None
    nodo_con_menor_f = None
    menor_f = float('inf')  # Inicializamos con un valor infinito para comparar

    # Recorremos cada nodo en la lista frontera
    for nodo in lista_frontera:
        # Calculamos f = g + h (donde h es la heurística entre la posición del nodo y el objetivo)
        f_actual = nodo.g + seleccionar_heuristica(nodo.posicion, objetivo)

        # Si encontramos un nodo con un f menor, lo actualizamos
        if f_actual < menor_f:
            menor_f = f_actual
            nodo_con_menor_f = nodo

    return nodo_con_menor_f  # Retornamos el nodo con el menor valor de f

# Función para calcular la heurística 
def calcular_heuristica_manhattan(posicion, objetivo):
    return abs(posicion.getFila() - objetivo.getFila()) + abs(posicion.getCol() - objetivo.getCol())

# Función para calcular la heurística usando la distancia Euclidiana
def calcular_heuristica_euclidiana(posicion, objetivo):
    return ((posicion.getFila() - objetivo.getFila())**2 + (posicion.getCol() - objetivo.getCol())**2) ** 0.5

# Función para calcular la heurística usando la distancia Chebyshev
def calcular_heuristica_chebyshev(posicion, objetivo):
    return max(abs(posicion.getFila() - objetivo.getFila()), abs(posicion.getCol() - objetivo.getCol()))

# Función para calcular la heurística usando la distancia Hamming
def calcular_heuristica_hamming(posicion, objetivo):
    return (posicion.getFila() != objetivo.getFila()) + (posicion.getCol() != objetivo.getCol())

# Función para calcular la heurística usando la distancia Octile
def calcular_heuristica_octil(posicion, objetivo):
    delta_fila = abs(posicion.getFila() - objetivo.getFila())
    delta_col = abs(posicion.getCol() - objetivo.getCol())
    return max(delta_fila, delta_col) + (math.sqrt(2) - 1) * min(delta_fila, delta_col)

def seleccionar_heuristica(posicion, objetivo):
    if SELECCION_HEURISTICA == 1:
        return 0
    elif SELECCION_HEURISTICA == 2:
        return calcular_heuristica_manhattan(posicion, objetivo)
    elif SELECCION_HEURISTICA == 3:
        return calcular_heuristica_euclidiana(posicion, objetivo)
    elif SELECCION_HEURISTICA == 4:
        return calcular_heuristica_chebyshev(posicion, objetivo)
    elif SELECCION_HEURISTICA == 5:
        return calcular_heuristica_hamming(posicion, objetivo)
    elif SELECCION_HEURISTICA == 6:
        return calcular_heuristica_octil(posicion, objetivo)
    else:
        raise ValueError("Valor de SELECCION_HEURISTICA no válido")

# A* Algorithm
def a_estrella(mapa, inicio, meta, camino):
    
    matriz_exploracion = inicializar_matriz_exploracion(mapa)  # Crear la matriz de exploración

    LF.clear()  # Resetear la lista frontera
    LI.clear()  # Resetear la lista interior
    nodo_inicial = Nodo(f=0, g=0, posicion=inicio)
    LF.append(nodo_inicial)  # Inicializamos la lista frontera con el nodo inicial
    iteracion = 0  # Contador de iteraciones para la matriz


    while LF:
        #nodo_actual = obtener_nodo_con_menor_f(LF)
        nodo_actual = obtener_nodo_con_menor_f_heuristica(LF, meta)

        # Marcar el nodo actual en la matriz de exploración
        matriz_exploracion[nodo_actual.posicion.getFila()][nodo_actual.posicion.getCol()] = iteracion
        iteracion += 1

        # Si hemos llegado a la meta, reconstruir el camino y calcular el coste total
        if nodo_actual.posicion.getFila() == meta.getFila() and nodo_actual.posicion.getCol() == meta.getCol():
            camino, coste_total = reconstruir_camino(nodo_actual, camino, mapa)
            return camino, coste_total, matriz_exploracion  # Devolver el camino, coste y la matriz de exploración

        LF.remove(nodo_actual)
        LI.append(nodo_actual)

        # Expandimos los nodos adyasentes
        for hijo_posicion in posiciones_adyacentes(nodo_actual.posicion, mapa):
            # Se comprueba si esta en Lista Interior
            if any(nodo.posicion.getFila() == hijo_posicion.getFila() and nodo.posicion.getCol() == hijo_posicion.getCol() for nodo in LI):
                continue

            g_nuevo = nodo_actual.g + 1
            # Se comprueba si el nodo vecino ya esta en Lista Frontera
            nodo_hijo = next((nodo for nodo in LF if nodo.posicion.getFila() == hijo_posicion.getFila() and nodo.posicion.getCol() == hijo_posicion.getCol()), None)
            # Si no esta el nodo en Lista Frontera sera None y se agrega
            if nodo_hijo is None:
                nodo_hijo = Nodo(f=g_nuevo, g=g_nuevo, posicion=hijo_posicion, padre=nodo_actual)
                LF.append(nodo_hijo)
                # O se actualiza el nodo si se el costo mejora
            elif g_nuevo < nodo_hijo.g:
                nodo_hijo.g = g_nuevo
                nodo_hijo.f = nodo_hijo.g
                nodo_hijo.padre = nodo_actual

    return None, 0, matriz_exploracion  # Devolver None, 0 y la matriz si no hay solución

# A*ε Algorithm
def a_estrella_epsilon(mapa, inicio, meta, epsilon, camino):
    global cal
    matriz_exploracion = inicializar_matriz_exploracion(mapa)  # Crear la matriz de exploración

    LF.clear()  # Resetear la lista frontera
    LI.clear()  # Resetear la lista interior
    nodo_inicial = Nodo(f=0, g=0, posicion=inicio)
    LF.append(nodo_inicial)  # Inicializamos la lista frontera con el nodo inicial
    iteracion = 0  # Contador de iteraciones para la matriz
    cal = 0




    while LF:

        nodo_con_menor_calorias = None
        menor_calorias = float('inf')

        # Obtener el valor mínimo de f en la lista frontera
        f_minimo = min(nodo.f for nodo in LF)

        # Crear la lista focal con la condición f(n) <= (1 + epsilon) * f_minimo
        LFocal = [nodo for nodo in LF if nodo.f <= (1 + epsilon) * f_minimo]

        # Seleccionar el nodo con el menor valor de gasto en calorías
        for nodo in LFocal:
            calorias_nodo = heuristica_focal_calorias(nodo, mapa)
            if calorias_nodo < menor_calorias:
                menor_calorias = calorias_nodo
                nodo_con_menor_calorias = nodo

        nodo_actual = nodo_con_menor_calorias

        # Marcar el nodo actual en la matriz de exploración
        matriz_exploracion[nodo_actual.posicion.getFila()][nodo_actual.posicion.getCol()] = iteracion
        iteracion += 1

        # Si hemos llegado a la meta, reconstruir el camino y calcular el coste total
        if nodo_actual.posicion.getFila() == meta.getFila() and nodo_actual.posicion.getCol() == meta.getCol():
            camino, coste_total = reconstruir_camino(nodo_actual, camino, mapa)
            return camino, coste_total, matriz_exploracion  # Devolver el camino, coste y la matriz de exploración
        

        LF.remove(nodo_actual)
        LI.append(nodo_actual)

        # Expandimos los nodos adyacentes
        for hijo_posicion in posiciones_adyacentes(nodo_actual.posicion, mapa):
            # Se comprueba si esta en Lista Interior
            if any(nodo.posicion.getFila() == hijo_posicion.getFila() and nodo.posicion.getCol() == hijo_posicion.getCol() for nodo in LI):
                continue

            # Obtener el tipo de terreno del hijo
            terreno_hijo = mapa.getCelda(hijo_posicion.getFila(), hijo_posicion.getCol())
            
            # Calcular el nuevo g basado en el gasto en calorías del terreno
            calorias_nodo_hijo =  gasto_en_calorias(terreno_hijo)
            
            g_nuevo = nodo_actual.g + calorias_nodo_hijo
            cal += calorias_nodo_hijo
            

            # Se comprueba si el nodo vecino ya está en Lista Frontera
            nodo_hijo = next((nodo for nodo in LF if nodo.posicion.getFila() == hijo_posicion.getFila() and nodo.posicion.getCol() == hijo_posicion.getCol()), None)
            # Si no está el nodo en Lista Frontera será None y se agrega
            if nodo_hijo is None:
                nodo_hijo = Nodo(f=g_nuevo, g=g_nuevo, posicion=hijo_posicion, padre=nodo_actual)
                LF.append(nodo_hijo)
            # O se actualiza el nodo si el costo mejora
            elif g_nuevo < nodo_hijo.g:
                nodo_hijo.g = g_nuevo
                nodo_hijo.f = nodo_hijo.g
                nodo_hijo.padre = nodo_actual

    return None, 0, matriz_exploracion  # Devolver None, 0 y la matriz si no hay solución



def gasto_en_calorias(terreno):
    if terreno == 0:  # Hierba
        return 2
    elif terreno == 4:  # Agua
        return 4
    elif terreno == 5:  # Roca
        return 6
    elif terreno == 1:  # Celda de bloque (inaccesible)
        return float('inf')  # Inaccesible
    else:
        return 1  # Terreno genérico o desconocido (sin penalización especial)

def heuristica_focal_calorias(nodo, mapa):
    # El gasto en calorías se basa en el tipo de terreno donde está el nodo actual
    terreno_actual = mapa.getCelda(nodo.posicion.getFila(), nodo.posicion.getCol())
    return gasto_en_calorias(terreno_actual)




# Función para reconstruir el camino desde la meta hasta el inicio y actualizar la matriz de camino
def reconstruir_camino(nodo, camino, mapa):
    global cal
    cal = 0
    coste_total = 0  # Inicializamos el coste total
    nodo_anterior = None  # Mantendremos una referencia al nodo anterior

    while nodo:
        fila = nodo.posicion.getFila()
        col = nodo.posicion.getCol()
        camino[fila][col] = 'C'  # Marcamos las posiciones del camino con 'C'

        # Si tenemos un nodo anterior, calculamos el coste del movimiento
        if nodo_anterior is not None:
            coste_total += calcular_coste(nodo, nodo_anterior)
            terreno_actual = mapa.getCelda(nodo.posicion.getFila(), nodo.posicion.getCol())
            cal += gasto_en_calorias(terreno_actual)  # Acumulamos calorías solo en el camino


        nodo_anterior = nodo  # Actualizamos el nodo anterior
        nodo = nodo.padre
    
    return camino, coste_total  # Devolvemos el camino y el coste total

# Función para calcular el coste de moverse de un nodo a otro
def calcular_coste(nodo_actual, nodo_hijo):
    fila_actual, col_actual = nodo_actual.posicion.getFila(), nodo_actual.posicion.getCol()
    fila_hijo, col_hijo = nodo_hijo.posicion.getFila(), nodo_hijo.posicion.getCol()

    # Si el movimiento es diagonal (cambia tanto la fila como la columna)
    if abs(fila_actual - fila_hijo) == 1 and abs(col_actual - col_hijo) == 1:
        return 1.5  # Movimiento diagonal
    else:
        return 1  # Movimiento horizontal o vertical

def imprimir_matriz_camino(camino):
    for fila in camino:
        print(' '.join(fila))  # Imprimir cada fila unida por espacios

def imprimir_matriz_exploracion(matriz_exploracion):
    for fila in matriz_exploracion:
        print(' '.join(str(x).rjust(3, ' ') if x != -1 else '.'.rjust(3, ' ') for x in fila))  # Mostrar '.' para no explorados



# función principal
def main():
    pygame.init()
    global cal
    reloj = pygame.time.Clock()

    if len(sys.argv) == 1:  # Si no se indica un mapa, coge mapa.txt por defecto
        file = 'mapa6.txt'
    else:
        file = sys.argv[-1]

    mapi = Mapa(file)
    camino = inic(mapi)
    origen = Casilla(0, 0)
    destino = Casilla(mapi.getAlto() - 1, mapi.getAncho() - 1)  # Se fija el destino

    # Ejecutar los experimentos
    ejecutar_experimentos_varios(mapi, origen, destino)

    # Mostrar los resultados en pantalla
    for resultado in resultados_experimentos:
        print(f"Algoritmo: {resultado['algoritmo']}, Heurística: {resultado['heuristica']}, "
              f"Epsilon: {resultado['epsilon']}, Nodos explorados: {resultado['nodos_explorados']}, "
              f"Coste total: {resultado['coste_total']}, Calorías consumidas: {resultado['calorias_consumidas']}")
    
    pygame.quit()

#---------------------------------------------------------------------
if __name__=="__main__":
    main()

