# planta con requerimientos de agua y fertilizante
class Planta:
    def __init__(self, nombre, posicion):
        self.nombre = nombre  # Nombre de la planta (tipo)
        self.posicion = posicion  # Posición en la hilera (1, 2, 3, ...)
        self.agua_requerida = 0  # Cantidad de agua requerida (será asignada después)
        self.fertilizante_requerido = 0  # Cantidad de fertilizante requerida
        self.regada = False  # Estado de riego
    
    @property
    def litros_agua(self):
        return self.agua_requerida
    
    @property
    def gramos_fertilizante(self):
        return self.fertilizante_requerido

    def regar(self):
        self.regada = True

    def __str__(self):
        estado = "Regada" if self.regada else "Sin regar"
        return f"Planta P{self.posicion} - {self.litros_agua}L, {self.gramos_fertilizante}g - {estado}"

    def __repr__(self):
        return f"Planta(pos={self.posicion}, agua={self.litros_agua}L, fert={self.gramos_fertilizante}g)"
