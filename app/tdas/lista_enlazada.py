from .nodo import Nodo


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.tamaño = 0

    def esta_vacia(self):
        return self.cabeza is None

    def insertar_al_inicio(self, dato):
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        self.tamaño += 1

    def insertar_al_final(self, dato):
        nuevo_nodo = Nodo(dato)

        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

        self.tamaño += 1

    def insertar_en_posicion(self, posicion, dato):
        if posicion < 0 or posicion > self.tamaño:
            raise IndexError("Posición fuera de rango")

        if posicion == 0:
            self.insertar_al_inicio(dato)
            return

        nuevo_nodo = Nodo(dato)
        actual = self.cabeza

        for _ in range(posicion - 1):
            actual = actual.siguiente

        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo
        self.tamaño += 1

    def eliminar(self, dato):
        if self.esta_vacia():
            return False

        if self.cabeza.dato == dato:
            self.cabeza = self.cabeza.siguiente
            self.tamaño -= 1
            return True

        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self.tamaño -= 1
                return True
            actual = actual.siguiente

        return False

    def eliminar_en_posicion(self, posicion):
        if posicion < 0 or posicion >= self.tamaño:
            raise IndexError("Posición fuera de rango")

        if posicion == 0:
            dato = self.cabeza.dato
            self.cabeza = self.cabeza.siguiente
            self.tamaño -= 1
            return dato

        actual = self.cabeza
        for _ in range(posicion - 1):
            actual = actual.siguiente

        dato = actual.siguiente.dato
        actual.siguiente = actual.siguiente.siguiente
        self.tamaño -= 1
        return dato

    def buscar(self, dato):
        actual = self.cabeza
        posicion = 0

        while actual:
            if actual.dato == dato:
                return posicion
            actual = actual.siguiente
            posicion += 1

        return -1

    def obtener(self, posicion):
        if posicion < 0 or posicion >= self.tamaño:
            raise IndexError("Posición fuera de rango")

        actual = self.cabeza
        for _ in range(posicion):
            actual = actual.siguiente

        return actual.dato

    def obtener_tamaño(self):
        return self.tamaño

    def limpiar(self):
        self.cabeza = None
        self.tamaño = 0

    def __str__(self):
        if self.esta_vacia():
            return "[]"

        # Construir cadena sin usar listas nativas
        resultado = "["
        actual = self.cabeza
        es_primero = True

        while actual:
            if not es_primero:
                resultado += " -> "
            resultado += str(actual.dato)
            actual = actual.siguiente
            es_primero = False

        resultado += "]"
        return resultado

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente
