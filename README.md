# busqueda_heuristica
 Desarrollo del algoritmo A estrella para encontrar el camino mas corto

Objetivos:
• Comprender el funcionamiento de la búsqueda heurística y en concreto del algoritmo
A y del A*ε.
• Implementar los algoritmos A* y A*ε y saber cómo seleccionar una heurística apropiada
al problema.
• Realizar un análisis cuantitativo respecto al número de nodos explorados con este
algoritmo.

# Distancias y Heurísticas Utilizadas

En este proyecto, utilizamos varias métricas de distancia como heurísticas para resolver problemas de búsqueda en espacios discretos (como una cuadrícula). A continuación se describen las diferentes métricas de distancia empleadas:

## 1. Distancia Manhattan

La **distancia Manhattan** (también conocida como **distancia de la ciudad** o **distancia de bloques**) se refiere al número total de pasos que se requieren para moverse desde un punto a otro en una cuadrícula, únicamente a través de movimientos horizontales y verticales. Imagina una persona caminando por una ciudad con calles que se cruzan en ángulos rectos, donde solo pueden caminar en líneas rectas, no en diagonal.

**Fórmula:**

h(n) = |x_meta - x_nodo| + |y_meta - y_nodo|

Esta métrica es útil para espacios donde el movimiento diagonal no está permitido, como en un plano de calles o una cuadrícula de un videojuego.

## 2. Distancia Euclidiana

La **distancia Euclidiana** es la distancia más corta entre dos puntos en un espacio cartesiano (como el plano XY) y se calcula utilizando el teorema de Pitágoras. Representa la distancia en línea recta entre dos puntos, como si se trazara una cuerda entre ellos.

**Fórmula:**

h(n) = sqrt((x_meta - x_nodo)^2 + (y_meta - y_nodo)^2)

Se utiliza cuando se permite el movimiento en diagonal, como en el espacio real.

## 3. Distancia Chebyshev

La **distancia Chebyshev** mide la cantidad mínima de movimientos necesarios para moverse de un punto a otro en una cuadrícula, permitiendo movimientos diagonales y ortogonales (horizontales y verticales). Es útil cuando los movimientos diagonales cuestan lo mismo que los horizontales o verticales.

**Fórmula:**

h(n) = max(|x_meta - x_nodo|, |y_meta - y_nodo|)

## 4. Distancia Hamming

La **distancia Hamming** mide la cantidad de posiciones en las que dos secuencias de igual longitud difieren entre sí. Es comúnmente usada en áreas como la teoría de la codificación y detección de errores, ya que cuenta el número de diferencias entre dos cadenas o secuencias discretas.

**Fórmula:**

h = número de posiciones donde los elementos son diferentes

No tiene en cuenta la magnitud de la diferencia, solo si las posiciones son iguales o no.

## 5. Distancia Canberra

La **distancia Canberra** es una métrica que compara dos puntos sensibles a pequeñas diferencias entre ellos. Se utiliza en problemas donde pequeñas variaciones son importantes. Es la suma de las fracciones de las diferencias absolutas normalizadas entre dos puntos.

**Fórmula:**

h(n) = sum(|x_meta - x_nodo| / (|x_meta| + |x_nodo|))

Esta métrica resalta pequeñas diferencias, haciéndola útil en problemas donde se necesita destacar variaciones mínimas.






