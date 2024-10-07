class Nodo:
    def __init__(self, f, g, posicion, padre=None):
        self.f = f  # Costo total estimado (f = g + h)
        self.g = g  # Costo desde el inicio hasta el nodo actual
        self.h = 0
        self.posicion = posicion  # La posición actual como objeto de la clase Casilla
        self.padre = padre  # Referencia al nodo padre
    
    
    def __str__(self):
        return f"Nodo(f: {self.f}, g: {self.g}, h: {self.h}, posicion: (fila: {self.posicion.getFila()}, columna: {self.posicion.getCol()}))"
    
    def getF(self):
        return self.f

    def getG(self):
        return self.g

    def getH(self):
        return self.h
    
    def getPosicion(self):
        return self.posicion
