class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        
    def __str__(self):
        return str(self.dato)


class NodoDoble:    
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None
        
    def __str__(self):
        return str(self.dato)