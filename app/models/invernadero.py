from app.tdas.lista_enlazada import ListaEnlazada
from app.models.hilera import Hilera
from app.models.dron import Dron
from app.models.plan_riego import PlanRiego


# resumen de estadisticas de un dron
class ResumenDron:
    def __init__(self, id_dron, agua_utilizada, fertilizante_utilizado, hilera_asignada):
        self.id = id_dron
        self.agua_utilizada = agua_utilizada
        self.fertilizante_utilizado = fertilizante_utilizado
        self.hilera_asignada = hilera_asignada


# invernadero con hileras, drones y plan de riego
class Invernadero:

    def __init__(self, nombre="Invernadero"):
        self.nombre = nombre
        self.hileras = ListaEnlazada()  # Lista de hileras
        self.drones = ListaEnlazada()  # Lista de drones
        self.plan_riego = PlanRiego()  # Plan de riego actual

    @property
    def numero_hileras(self):
        return self.hileras.obtener_tamaño()

    @property
    def plantas_por_hilera(self):
        if self.hileras.obtener_tamaño() == 0:
            return 0
        total_plantas = 0
        for i in range(self.hileras.obtener_tamaño()):
            hilera = self.hileras.obtener(i)
            total_plantas += hilera.obtener_cantidad_plantas()
        return total_plantas // self.hileras.obtener_tamaño() if self.hileras.obtener_tamaño() > 0 else 0

    def agregar_hilera(self, numero_hilera):
        hilera = Hilera(numero_hilera)
        self.hileras.insertar_al_final(hilera)
        return hilera

    def obtener_hilera(self, numero_hilera):
        for i in range(self.hileras.obtener_tamaño()):
            hilera = self.hileras.obtener(i)
            if hilera.numero == numero_hilera:
                return hilera
        return None  # Retornar None en lugar de lanzar excepción

    def agregar_dron(self, dron):
        if isinstance(dron, str):
            # Si es un string, crear nuevo dron
            nuevo_dron = Dron(dron)
            self.drones.insertar_al_final(nuevo_dron)
            return nuevo_dron
        else:
            # Si es un objeto Dron, agregarlo directamente
            self.drones.insertar_al_final(dron)
            return dron

    def obtener_dron(self, id_dron):
        for i in range(self.drones.obtener_tamaño()):
            dron = self.drones.obtener(i)
            if dron.id == id_dron:
                return dron
        return None  # Retornar None en lugar de lanzar excepción

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
        errores = ListaEnlazada()

        if self.hileras.obtener_tamaño() == 0:
            errores.insertar_al_final("No hay hileras configuradas")

        if self.drones.obtener_tamaño() == 0:
            errores.insertar_al_final("No hay drones configurados")

        for i in range(self.hileras.obtener_tamaño()):
            hilera = self.hileras.obtener(i)
            if hilera.obtener_cantidad_plantas() == 0:
                errores.insertar_al_final(
                    f"Hilera H{hilera.numero} no tiene plantas")

        for i in range(self.hileras.obtener_tamaño()):
            hilera = self.hileras.obtener(i)
            if hilera.dron_asignado is None:
                errores.insertar_al_final(
                    f"Hilera H{hilera.numero} no tiene dron asignado")

        if self.plan_riego.obtener_cantidad_pasos() == 0:
            errores.insertar_al_final("No hay plan de riego configurado")

        return errores

    def calcular_totales_agua_fertilizante(self):
        total_agua = 0
        total_fertilizante = 0

        for i in range(self.hileras.obtener_tamaño()):
            hilera = self.hileras.obtener(i)
            agua_hilera, fert_hilera = hilera.calcular_totales()
            total_agua += agua_hilera
            total_fertilizante += fert_hilera

        return total_agua, total_fertilizante

    def obtener_resumen_drones(self):
        resumen = ListaEnlazada()

        for i in range(self.drones.obtener_tamaño()):
            dron = self.drones.obtener(i)
            # Crear objeto simple para el resumen en lugar de diccionario
            resumen_dron = ResumenDron(
                dron.id,
                dron.agua_utilizada,
                dron.fertilizante_utilizado,
                dron.hilera_asignada.numero if dron.hilera_asignada else None
            )
            resumen.insertar_al_final(resumen_dron)

        return resumen

    def reiniciar_estado(self):
        # Reiniciar estado de drones
        for i in range(self.drones.obtener_tamaño()):
            dron = self.drones.obtener(i)
            dron.posicion_actual = 0
            dron.agua_utilizada = 0
            dron.fertilizante_utilizado = 0
            dron.finalizado = False

        # Reiniciar estado de plantas
        for i in range(self.hileras.obtener_tamaño()):
            hilera = self.hileras.obtener(i)
            for j in range(hilera.plantas.obtener_tamaño()):
                planta = hilera.plantas.obtener(j)
                planta.regada = False

        # Reiniciar plan de riego
        self.plan_riego.reiniciar_plan()

    def __str__(self):
        return f"{self.nombre} - {self.hileras.obtener_tamaño()} hileras, {self.drones.obtener_tamaño()} drones"

    def __repr__(self):
        return f"Invernadero(nombre='{self.nombre}', hileras={self.hileras.obtener_tamaño()}, drones={self.drones.obtener_tamaño()})"
