from .nodo import Nodo
from .lista_enlazada import ListaEnlazada


# estructura de datos cola FIFO
class Cola:
    # cola FIFO para procesar elementos en orden
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

        elementos = ListaEnlazada()
        actual = self.frente
        while actual:
            elementos.insertar_al_final(str(actual.dato))
            actual = actual.siguiente

        # Convertir lista enlazada a string
        cadena_elementos = ""
        for i in range(elementos.obtener_tamaño()):
            if i > 0:
                cadena_elementos += " | "
            cadena_elementos += elementos.obtener(i)

        return "Frente -> [" + cadena_elementos + "] <- Final"

    def crear_copia(self):
        # Crear una copia independiente de la cola para visualización
        nueva_cola = Cola()
        actual = self.frente
        while actual:
            nueva_cola.encolar(actual.dato)
            actual = actual.siguiente
        return nueva_cola

    def __iter__(self):
        actual = self.frente
        while actual:
            yield actual.dato
            actual = actual.siguiente
