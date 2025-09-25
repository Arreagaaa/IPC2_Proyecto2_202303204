from ..tdas import Cola


class PlanRiego:
    def __init__(self):
        self.secuencia_riego = Cola()  # Cola con la secuencia de riego
        self.plan_original = []  # Lista para mantener el plan original

    def agregar_paso(self, numero_hilera, numero_planta):
        paso = {
            'hilera': numero_hilera,
            'planta': numero_planta,
            'completado': False
        }
        self.secuencia_riego.encolar(paso)
        self.plan_original.append(f"H{numero_hilera}-P{numero_planta}")

    def obtener_siguiente_paso(self):
        if not self.secuencia_riego.esta_vacia():
            return self.secuencia_riego.desencolar()
        return None

    def hay_pasos_pendientes(self):
        return not self.secuencia_riego.esta_vacia()

    def obtener_plan_original(self):
        return ", ".join(self.plan_original)

    def obtener_cantidad_pasos(self):
        return len(self.plan_original)

    def reiniciar_plan(self):
        self.secuencia_riego.limpiar()
        for paso_str in self.plan_original:
            # Parsear "H1-P2" -> hilera=1, planta=2
            partes = paso_str.split('-')
            hilera = int(partes[0][1:])  # Quitar 'H' y convertir a int
            planta = int(partes[1][1:])  # Quitar 'P' y convertir a int

            paso = {
                'hilera': hilera,
                'planta': planta,
                'completado': False
            }
            self.secuencia_riego.encolar(paso)

    def parsear_plan_desde_cadena(self, plan_cadena):
        self.secuencia_riego.limpiar()
        self.plan_original.clear()

        if not plan_cadena.strip():
            return

        pasos = [paso.strip() for paso in plan_cadena.split(',')]

        for paso_str in pasos:
            if '-' in paso_str:
                try:
                    partes = paso_str.split('-')
                    hilera = int(partes[0][1:])  # Quitar 'H' y convertir a int
                    planta = int(partes[1][1:])  # Quitar 'P' y convertir a int
                    self.agregar_paso(hilera, planta)
                except (ValueError, IndexError):
                    continue  # Ignorar pasos mal formateados

    def __str__(self):
        return f"Plan de riego: {self.obtener_plan_original()} - Pasos pendientes: {self.secuencia_riego.obtener_tamaño()}"

    def __repr__(self):
        return f"PlanRiego(pasos={len(self.plan_original)}, pendientes={self.secuencia_riego.obtener_tamaño()})"
