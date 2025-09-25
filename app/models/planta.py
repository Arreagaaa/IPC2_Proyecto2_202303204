class Planta:
    def __init__(self, posicion, litros_agua, gramos_fertilizante):
        self.posicion = posicion  # Posición en la hilera (1, 2, 3, ...)
        self.litros_agua = litros_agua  # Cantidad de agua requerida
        # Cantidad de fertilizante requerida
        self.gramos_fertilizante = gramos_fertilizante
        self.regada = False  # Estado de riego

    def regar(self):
        self.regada = True

    def __str__(self):
        estado = "Regada" if self.regada else "Sin regar"
        return f"Planta P{self.posicion} - {self.litros_agua}L, {self.gramos_fertilizante}g - {estado}"

    def __repr__(self):
        return f"Planta(pos={self.posicion}, agua={self.litros_agua}L, fert={self.gramos_fertilizante}g)"
