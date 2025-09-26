from app.tdas.lista_enlazada import ListaEnlazada
from app.models.planta import Planta


class Hilera:
    def __init__(self, numero_hilera):
        self.numero = numero_hilera  # Número de la hilera (H1, H2, H3, ...)
        self.plantas = ListaEnlazada()  # Lista de plantas en la hilera
        self.dron_asignado = None  # Dron asignado a esta hilera

    def agregar_planta(self, litros_agua, gramos_fertilizante):
        posicion = self.plantas.obtener_tamaño() + 1
        planta = Planta(posicion, litros_agua, gramos_fertilizante)
        self.plantas.insertar_al_final(planta)
        return planta

    def obtener_planta(self, posicion):
        if posicion < 1 or posicion > self.plantas.obtener_tamaño():
            raise IndexError(
                f"Posición {posicion} fuera de rango en hilera {self.numero}")

        return self.plantas.obtener(posicion - 1)  # Ajustar índice base 0

    def obtener_cantidad_plantas(self):
        return self.plantas.obtener_tamaño()

    def establecer_planta_en_posicion(self, posicion, planta):
        # Establecer la posición de la planta
        planta.posicion = posicion
        # Simplemente agregar al final - las plantas se procesarán en orden
        self.plantas.insertar_al_final(planta)

    def asignar_dron(self, dron):
        self.dron_asignado = dron
        dron.hilera_asignada = self

    def calcular_totales(self):
        total_agua = 0
        total_fertilizante = 0

        for i in range(self.plantas.obtener_tamaño()):
            planta = self.plantas.obtener(i)
            total_agua += planta.litros_agua
            total_fertilizante += planta.gramos_fertilizante

        return total_agua, total_fertilizante

    def __str__(self):
        return f"Hilera H{self.numero} - {self.plantas.obtener_tamaño()} plantas - Dron: {self.dron_asignado.id if self.dron_asignado else 'Sin asignar'}"

    def __repr__(self):
        return f"Hilera(num={self.numero}, plantas={self.plantas.obtener_tamaño()})"
