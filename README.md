Antes de ejecutar defina que heuristica quiere probar en la *linea 10*
Que valor de epsilon va dar para las pruebas individuales en la *linea 18*

si desea tener mas valores para epsilon agreguelos a la lista en la *linea 24*

para el analisis debe de tener instalado pygame, panda y matplotlib

pip install matplotlib
pip install pandas 
pip install pygame

1. Introducción
En esta práctica, se implementaron y analizaron los algoritmos de búsqueda A* y A*ε, aplicados a la resolución de problemas de camino en un mapa con diferentes tipos de terreno. El objetivo es encontrar la ruta más eficiente entre un punto de origen y un destino, minimizando el coste total de movimiento, que en este caso se simula mediante un gasto en calorías según el tipo de terreno. Los terrenos incluyen hierba, agua y roca, cada uno con un coste de desplazamiento diferente.
Para mejorar la eficiencia del algoritmo y experimentar con distintos enfoques, se han implementado varias heurísticas:

Manhattan: Calcula la distancia total en términos de pasos horizontales y verticales, útil para mapas con movimientos en cuadrículas sin diagonales.
h(n)=∣xactual-xmeta∣+∣yactual-ymeta∣

Euclidiana: Calcula la distancia en línea recta, considerando tanto desplazamientos horizontales/verticales como diagonales, adecuada cuando los movimientos son continuos.
h(n)=√(xactual-xmeta)2+(yactual-ymeta)2

Chebyshev: Similar a la distancia Manhattan, pero también considera movimientos diagonales al mismo coste que los horizontales y verticales.
h(n)=max(∣xactual-xmeta∣,∣yactual-ymeta∣)

Hamming: Simplemente cuenta la cantidad de diferencias en fila y columna entre el punto actual y el destino, sin considerar distancias reales.
h(n)=1(xactual ≠ xmeta)+1(yactual  ≠ ymeta)

Octil: Combina movimientos en línea recta y diagonales, con un coste adicional para los desplazamientos diagonales, lo que lo hace más adecuado en terrenos donde ambos tipos de movimiento son posibles.
h(n)=max(Δx,Δy)+(√2-1)⋅min(Δx,Δy)
donde:
Δx=∣xactual-xmeta∣,      Δy=∣yactual-ymeta
Esta diversidad de heurísticas permite analizar cómo influyen en la cantidad de nodos explorados, el coste total y el camino solución, en el algoritmo A*.

Conclusiones
Tanto A* como A*ε son algoritmos efectivos para la búsqueda de caminos, y su elección depende del objetivo específico de la aplicación. A* puede que sea más adecuado cuando se necesita un camino corto y rápido, mientras que A*ε es preferible cuando se busca optimizar el consumo de recursos energéticos en terrenos diversos.

Este trabajo resalta la importancia de adaptar los algoritmos de búsqueda a las necesidades particulares de cada escenario, optimizando la búsqueda no solo en términos de distancia, sino también considerando factores adicionales como el consumo energético, lo cual puede ser crucial en aplicaciones avanzadas de inteligencia artificial y robótica.




