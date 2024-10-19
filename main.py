import sys, pygame
from casilla import *
from Nodo import *
from mapa import *
from pygame.locals import *
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

SELECCION_HEURISTICA = 2
# 1 para h = 0
# 2 para Manhattan, 
# 3 para Euclidiana, 
# 4 para Chebyshev
# 5 para Hamming
# 6 para Octil.

# Configuraciónes

VALORES_EPSILON = [0, 0.25, 0.5, 1, 2, 3, 4, 5]  # Diferentes valores de epsilon para A*ε
RESULTADOS  = []  # Lista para almacenar los resultados de los experimentos

HEURISTICAS = [1, 2, 3, 4, 5, 6]  # h=0, Manhattan, Euclidiana, Chebyshev, Hamming, Octil

NOMBRES_HEURISTICAS = {
    1: 'h = 0',
    2: 'Manhattan',
    3: 'Euclidiana',
    4: 'Chebyshev',
    5: 'Hamming',
    6: 'Octil'
}

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


# ---------------------------------------------------------------------
# Funciones para analisis
# ---------------------------------------------------------------------

def ejecutar_experimentos(mapa, origen, destino, camino):

    for heuristica in HEURISTICAS:
        global SELECCION_HEURISTICA
        SELECCION_HEURISTICA = heuristica

        resultado = a_estrella(mapa, origen, destino, camino)
        if resultado is None:
            print(f"Error: No se encontró un camino válido con la heurística {NOMBRES_HEURISTICAS[heuristica]}.")
        else:
            camino_resultado, coste_total, _, cal = resultado
            RESULTADOS.append({
                'algoritmo': 'A*',
                'heuristica': NOMBRES_HEURISTICAS[heuristica],  # Asignar nombre de la heurística
                'epsilon': None,
                'coste': coste_total,
                'calorias': cal,
                'nodos_explorados': len(LI)  # Capturar la cantidad de nodos explorados
            })

        # Ejecutar A*ε para cada valor de epsilon
        for epsilon in VALORES_EPSILON:
            LI.clear()  # Limpiar nodos explorados antes de cada ejecución
            resultado = a_estrella_epsilon(mapa, origen, destino, epsilon, camino)
            if resultado is None:
                print(f"Error: No se encontró un camino válido con epsilon {epsilon}.")
            else:
                camino_resultado, coste_total, _, cal = resultado
                RESULTADOS.append({
                    'algoritmo': 'A*ε',
                    'heuristica': NOMBRES_HEURISTICAS[heuristica],  # Asignar nombre de la heurística
                    'epsilon': epsilon,
                    'coste': coste_total,
                    'calorias': cal,
                    'nodos_explorados': len(LI)  # Capturar la cantidad de nodos explorados
                })


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

            return camino, coste_total, matriz_exploracion, cal  # Devolver el camino, coste y la matriz de exploración y las calorias

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

    return None

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

            return camino, coste_total, matriz_exploracion, cal  # Devolver el camino, coste y la matriz de exploración
        

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
            calorias_nodo_hijo =  gasto_en_calorias(terreno_hijo) * (1 + epsilon)
            
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

    return None, 0, matriz_exploracion, cal  # Devolver None, 0 y la matriz si no hay solución



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

def pulsaBoton(mapi, posicion):
    res = -1

    # Botón 1
    if posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-65 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-15 and \
        posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res = 1
    # Botón 2
    elif posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+15 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+65 and \
        posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res = 2
    # Botón 3 (Nuevo)
    elif posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+85 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+135 and \
        posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res = 3

    return res

def graficar_resultados(RESULTADOS):
    # Convertir los resultados en un DataFrame de pandas
    df = pd.DataFrame(RESULTADOS)

    # Filtrar los resultados de A*
    df_a_estrella = df[df['algoritmo'] == 'A*']
    
    # Graficar el costo del camino solución para A* según la heurística
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))  # Dos gráficos en una ventana

    # Gráfico 1: Costo del camino vs. Heurística
    ax[0].bar(df_a_estrella['heuristica'], df_a_estrella['coste'], color='skyblue')
    ax[0].set_xlabel('Heurística')
    ax[0].set_ylabel('Costo del Camino')
    ax[0].set_title('Costo del Camino por A* según la Heurística')

    # Filtrar los resultados de A*ε
    df_a_estrella_epsilon = df[df['algoritmo'] == 'A*ε']
    
    # Gráfico 2: Calorías consumidas vs. epsilon
    ax[1].bar(df_a_estrella_epsilon['epsilon'], df_a_estrella_epsilon['calorias'], color='orange', width=0.3)
    ax[1].set_xlabel('Valor de Epsilon')
    ax[1].set_ylabel('Calorías Consumidas')
    ax[1].set_title('Calorías Consumidas por A*ε según el Valor de Epsilon')

    # Mostrar solo los valores de epsilon en el eje x
    ax[1].set_xticks(VALORES_EPSILON)

    plt.tight_layout()  # Para ajustar los gráficos
    plt.show()
# función principal
def main():

    pygame.init()
    global cal
    
    reloj=pygame.time.Clock()
    
    if len(sys.argv)==1: #si no se indica un mapa coge mapa.txt por defecto
        file='mapa.txt'
    else:
        file=sys.argv[-1]

    mapi=Mapa(file)     
    camino=inic(mapi)   
    
    anchoVentana=mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1 Juan Carlos Gutierrez")
    
    boton1=pygame.image.load("boton1.png").convert()
    boton1=pygame.transform.scale(boton1,[50, 30])
    
    boton2=pygame.image.load("boton2.png").convert()
    boton2=pygame.transform.scale(boton2,[50, 30])

    boton3=pygame.image.load("boton3.png").convert()
    boton3=pygame.transform.scale(boton3,[50, 30])
    
    personaje=pygame.image.load("rabbit.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])
    
    objetivo=pygame.image.load("carrot.png").convert()
    objetivo=pygame.transform.scale(objetivo,[TAM, TAM])
    
    coste=-1
    cal=0
    running= True    
    origen=Casilla(-1,-1)
    destino=Casilla(-1,-1)

    while running:        
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                running=False 
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()  

                if pulsaBoton(mapi, pos)==1 or pulsaBoton(mapi, pos)==2:
                    imprimir_origen_destino(origen, destino)  
                    
                    if origen.getFila()==-1 or destino.getFila()==-1:
                        
                        print('Error: No hay origen o destino')
                    else:
                        camino = inic(mapi)
                        coste = -1
                        if pulsaBoton(mapi, pos)==1:
                            resultado=a_estrella(mapi, origen, destino, camino)
                            ###########################                                                 
                            #coste, cal=llamar a A estrella 
                            
                            if resultado is not None:
                                camino, coste, matriz_exploracion, cal = resultado
                                if camino and len(camino) > 0:
                                    print("Matriz Camino Solucion:")
                                    imprimir_matriz_camino(camino)
                                    print("\n")
                                    print("\n")
                                    print("\n")
                                    print("Matriz de exploración:")
                                    imprimir_matriz_exploracion(matriz_exploracion)
                                else:
                                    print("No se encontró un camino.")
                            else:
                                print('Error: No existe un camino válido entre origen y destino')

                        elif pulsaBoton(mapi, pos)==2:
                            ###########################                                                   
                            #coste, cal=llamar a A estrella subepsilon
                            epsilon = 0.5
                            resultado=a_estrella_epsilon(mapi, origen, destino, epsilon, camino)                    
                            if resultado is not None:
                                camino, coste, matriz_exploracion, cal = resultado
                                if camino and len(camino) > 0:
                                    print("Matriz Camino Solucion:")
                                    imprimir_matriz_camino(camino)
                                    print("\n")
                                    print("\n")
                                    print("\n")
                                    print("Matriz de exploración:")
                                    imprimir_matriz_exploracion(matriz_exploracion)
                                else:
                                    print("No se encontró un camino.")
                            else:
                                print('Error: No existe un camino válido entre origen y destino')
                                
                # Botón 3: Ejecutar análisis
                elif pulsaBoton(mapi, pos) == 3:
                    # Verificar si el origen y el destino están definidos
                    if origen.getFila() == -1 or destino.getFila() == -1:
                        print("Error: No hay origen o destino. Por favor, seleccione un origen y destino antes de ejecutar el análisis.")
                    else:
                        # Inicializar posiciones de origen y destino para las pruebas
                        camino = inic(mapi)  # Reinicializar la matriz 'camino' antes de la ejecución de los experimentos

                        try:
                            resultado = a_estrella(mapi, origen, destino, camino)
                            if resultado is None:
                                print("No se encontró un camino válido con A* para el origen y destino seleccionados.")
                            else:
                                ejecutar_experimentos(mapi, origen, destino, camino)
                                print("Análisis ejecutado. Resultados:")
                                graficar_resultados(RESULTADOS)
                        except ValueError as e:
                            print(f"Error: {str(e)}")

                elif esMapa(mapi,pos):                    
                    if event.button==1: #botón izquierdo                        
                        colOrigen=pos[0]//(TAM+MARGEN)
                        filOrigen=pos[1]//(TAM+MARGEN)
                        casO=Casilla(filOrigen, colOrigen)                        
                        if bueno(mapi, casO):
                            origen=casO
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')
                            
                    elif event.button==3: #botón derecho
                        colDestino=pos[0]//(TAM+MARGEN)
                        filDestino=pos[1]//(TAM+MARGEN)
                        casD=Casilla(filDestino, colDestino)                        
                        if bueno(mapi, casD):
                            destino=casD
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')         
        
        #código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):
                if camino is not None and camino[fil][col] == 'C':
                    pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==0:
                    pygame.draw.rect(screen, HIERBA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==4:
                    pygame.draw.rect(screen, AGUA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==5:
                    pygame.draw.rect(screen, ROCA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                                    
                elif mapi.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, MURO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])        
        #pinta destino
        screen.blit(objetivo, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN])       
        #pinta botón
        screen.blit(boton1, [anchoVentana//2-65, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        screen.blit(boton2, [anchoVentana//2+15, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        screen.blit(boton3, [anchoVentana//2+85, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste y energía
        if coste!=-1:            
            fuente= pygame.font.Font(None, 25)
            textoCoste = fuente.render(f"Coste: {coste}", True, AMARILLO)         
            screen.blit(textoCoste, [anchoVentana-90, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])
            textoEnergía=fuente.render(f"Cal: "+str(cal), True, AMARILLO)
            screen.blit(textoEnergía, [5, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])
            
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)

        
        
    pygame.quit()
    
#---------------------------------------------------------------------
if __name__=="__main__":
    main()

