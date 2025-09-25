from .nodo import Nodo


class Pila:
    # Pila (LIFO - Last In, First Out) para almacenar elementos

    def __init__(self):
        self.tope = None
        self.tamaño = 0

    def esta_vacia(self):
        return self.tope is None

    def apilar(self, dato):
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo
        self.tamaño += 1

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("No se puede desapilar de una pila vacía")

        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self.tamaño -= 1
        return dato

    def ver_tope(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.tope.dato

    def obtener_tamaño(self):
        return self.tamaño

    def limpiar(self):
        self.tope = None
        self.tamaño = 0

    def __str__(self):
        if self.esta_vacia():
            return "Pila vacía"

        elementos = []
        actual = self.tope
        while actual:
            elementos.append(str(actual.dato))
            actual = actual.siguiente

        return "Tope -> [" + " | ".join(elementos) + "]"

    def __iter__(self):
        actual = self.tope
        while actual:
            yield actual.dato
            actual = actual.siguiente
