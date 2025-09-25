from .nodo import Nodo


class Cola:
    # Cola (FIFO - First In, First Out) para procesar elementos en orden
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamaño = 0

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, dato):
        nuevo_nodo = Nodo(dato)

        if self.esta_vacia():
            self.frente = nuevo_nodo
            self.final = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo

        self.tamaño += 1

    def desencolar(self):
        if self.esta_vacia():
            raise IndexError("No se puede desencolar de una cola vacía")

        dato = self.frente.dato
        self.frente = self.frente.siguiente

        if self.frente is None:
            self.final = None

        self.tamaño -= 1
        return dato

    def ver_frente(self):
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.frente.dato

    def obtener_tamaño(self):
        return self.tamaño

    def limpiar(self):
        self.frente = None
        self.final = None
        self.tamaño = 0

    def __str__(self):
        if self.esta_vacia():
            return "Cola vacía"

        elementos = []
        actual = self.frente
        while actual:
            elementos.append(str(actual.dato))
            actual = actual.siguiente

        return "Frente -> [" + " | ".join(elementos) + "] <- Final"

    def __iter__(self):
        actual = self.frente
        while actual:
            yield actual.dato
            actual = actual.siguiente
