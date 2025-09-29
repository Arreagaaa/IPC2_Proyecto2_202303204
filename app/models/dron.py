# dron autonomo para riego de plantas
class Dron:
    def __init__(self, id_dron):
        self.id = id_dron  # Identificador del dron (DR01, DR02, etc.)
        self.posicion_actual = 0  # Posición actual del dron (0 = inicio)
        self.hilera_asignada = None  # Hilera a la que está asignado
        self.agua_utilizada = 0  # Litros de agua utilizados
        self.fertilizante_utilizado = 0  # Gramos de fertilizante utilizados
        self.finalizado = False  # Estado de finalización
        # Capacidad máxima de agua en litros (valor por defecto)
        self.capacidad_agua = 50

    def asignar_hilera(self, hilera):
        self.hilera_asignada = hilera

    @property
    def nombre(self):
        return getattr(self, '_nombre', self.id)

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    def mover_adelante(self):
        if self.hilera_asignada and self.posicion_actual < self.hilera_asignada.obtener_cantidad_plantas():
            self.posicion_actual += 1
            return True
        return False

    def mover_atras(self):
        if self.posicion_actual > 0:
            self.posicion_actual -= 1
            return True
        return False

    def regar_planta_actual(self):
        if self.hilera_asignada and self.posicion_actual > 0:
            try:
                planta = self.hilera_asignada.obtener_planta(
                    self.posicion_actual)
                if not planta.regada:
                    planta.regar()
                    self.agua_utilizada += planta.litros_agua
                    self.fertilizante_utilizado += planta.gramos_fertilizante
                    return True
            except IndexError:
                pass
        return False

    def obtener_posicion_objetivo(self, numero_planta):
        return numero_planta - self.posicion_actual

    def puede_regar(self, numero_planta):
        return self.posicion_actual == numero_planta

    def regresar_inicio(self):
        movimientos_necesarios = self.posicion_actual
        self.posicion_actual = 0
        return movimientos_necesarios

    def finalizar(self):
        self.finalizado = True

    def obtener_estado_posicion(self):
        if self.posicion_actual == 0:
            return "Inicio"
        elif self.hilera_asignada:
            return f"H{self.hilera_asignada.numero}P{self.posicion_actual}"
        else:
            return f"Posición {self.posicion_actual}"

    def __str__(self):
        estado = "Finalizado" if self.finalizado else "Activo"
        return f"Dron {self.id} - {self.obtener_estado_posicion()} - {estado} - Agua: {self.agua_utilizada}L, Fertilizante: {self.fertilizante_utilizado}g"

    def __repr__(self):
        return f"Dron(id={self.id}, pos={self.posicion_actual})"
