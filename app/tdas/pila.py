from .nodo import Nodo


# estructura de datos pila LIFO
class Pila:
    # pila LIFO para almacenar elementos

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

        # Construir cadena sin usar listas nativas
        resultado = "Tope -> ["
        actual = self.tope
        es_primero = True

        while actual:
            if not es_primero:
                resultado += " | "
            resultado += str(actual.dato)
            actual = actual.siguiente
            es_primero = False

        resultado += "]"
        return resultado

    def __iter__(self):
        actual = self.tope
        while actual:
            yield actual.dato
            actual = actual.siguiente
