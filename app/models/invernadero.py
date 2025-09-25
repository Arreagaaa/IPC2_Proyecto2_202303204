from ..tdas import ListaEnlazada
from .hilera import Hilera
from .dron import Dron
from .plan_riego import PlanRiego


class Invernadero:

    def __init__(self, nombre="Invernadero"):
        self.nombre = nombre
        self.hileras = ListaEnlazada()  # Lista de hileras
        self.drones = ListaEnlazada()  # Lista de drones
        self.plan_riego = PlanRiego()  # Plan de riego actual

    def agregar_hilera(self, numero_hilera):
        hilera = Hilera(numero_hilera)
        self.hileras.insertar_al_final(hilera)
        return hilera

    def obtener_hilera(self, numero_hilera):
        for hilera in self.hileras:
            if hilera.numero == numero_hilera:
                return hilera
        raise ValueError(f"Hilera H{numero_hilera} no encontrada")

    def agregar_dron(self, id_dron):
        dron = Dron(id_dron)
        self.drones.insertar_al_final(dron)
        return dron

    def obtener_dron(self, id_dron):
        for dron in self.drones:
            if dron.id == id_dron:
                return dron
        raise ValueError(f"Dron {id_dron} no encontrado")

    def asignar_dron_a_hilera(self, id_dron, numero_hilera):
        dron = self.obtener_dron(id_dron)
        hilera = self.obtener_hilera(numero_hilera)
        hilera.asignar_dron(dron)

    def configurar_plan_riego(self, plan_cadena):
        self.plan_riego.parsear_plan_desde_cadena(plan_cadena)

    def obtener_cantidad_hileras(self):
        return self.hileras.obtener_tamaño()

    def obtener_cantidad_drones(self):
        return self.drones.obtener_tamaño()

    def validar_configuracion(self):
        errores = []

        if self.hileras.obtener_tamaño() == 0:
            errores.append("No hay hileras configuradas")

        if self.drones.obtener_tamaño() == 0:
            errores.append("No hay drones configurados")

        for hilera in self.hileras:
            if hilera.obtener_cantidad_plantas() == 0:
                errores.append(f"Hilera H{hilera.numero} no tiene plantas")

        for hilera in self.hileras:
            if hilera.dron_asignado is None:
                errores.append(
                    f"Hilera H{hilera.numero} no tiene dron asignado")

        if self.plan_riego.obtener_cantidad_pasos() == 0:
            errores.append("No hay plan de riego configurado")

        return errores

    def calcular_totales_agua_fertilizante(self):
        total_agua = 0
        total_fertilizante = 0

        for hilera in self.hileras:
            agua_hilera, fert_hilera = hilera.calcular_totales()
            total_agua += agua_hilera
            total_fertilizante += fert_hilera

        return total_agua, total_fertilizante

    def obtener_resumen_drones(self):
        resumen = []

        for dron in self.drones:
            resumen.append({
                'id': dron.id,
                'agua_utilizada': dron.agua_utilizada,
                'fertilizante_utilizado': dron.fertilizante_utilizado,
                'hilera_asignada': dron.hilera_asignada.numero if dron.hilera_asignada else None
            })

        return resumen

    def reiniciar_estado(self):
        # Reiniciar estado de drones
        for dron in self.drones:
            dron.posicion_actual = 0
            dron.agua_utilizada = 0
            dron.fertilizante_utilizado = 0
            dron.finalizado = False

        # Reiniciar estado de plantas
        for hilera in self.hileras:
            for planta in hilera.plantas:
                planta.regada = False

        # Reiniciar plan de riego
        self.plan_riego.reiniciar_plan()

    def __str__(self):
        return f"{self.nombre} - {self.hileras.obtener_tamaño()} hileras, {self.drones.obtener_tamaño()} drones"

    def __repr__(self):
        return f"Invernadero(nombre='{self.nombre}', hileras={self.hileras.obtener_tamaño()}, drones={self.drones.obtener_tamaño()})"
