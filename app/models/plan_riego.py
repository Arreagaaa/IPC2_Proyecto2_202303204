from app.tdas.cola import Cola
from app.tdas.lista_enlazada import ListaEnlazada


# paso individual del plan de riego
class PasoRiego:
    def __init__(self, hilera, planta, completado=False):
        self.hilera = hilera
        self.planta = planta
        self.completado = completado


# plan de riego con secuencia de pasos
class PlanRiego:
    def __init__(self):
        self.secuencia_riego = Cola()  # Cola con la secuencia de riego
        self.plan_original = ListaEnlazada()  # Lista para mantener el plan original

    def agregar_paso(self, numero_hilera, numero_planta):
        paso = PasoRiego(numero_hilera, numero_planta, False)
        self.secuencia_riego.encolar(paso)
        self.plan_original.insertar_al_final(
            f"H{numero_hilera}-P{numero_planta}")

    def obtener_siguiente_paso(self):
        if not self.secuencia_riego.esta_vacia():
            return self.secuencia_riego.desencolar()
        return None

    def hay_pasos_pendientes(self):
        return not self.secuencia_riego.esta_vacia()

    def obtener_plan_original(self):
        if self.plan_original.obtener_tamaño() == 0:
            return ""
        resultado = ""
        for i in range(self.plan_original.obtener_tamaño()):
            if i > 0:
                resultado += ", "
            resultado += self.plan_original.obtener(i)
        return resultado

    def obtener_cantidad_pasos(self):
        return self.plan_original.obtener_tamaño()

    def reiniciar_plan(self):
        self.secuencia_riego.limpiar()
        for i in range(self.plan_original.obtener_tamaño()):
            paso_str = self.plan_original.obtener(i)
            # Parsear "H1-P2" -> hilera=1, planta=2 manualmente
            posicion_guion = -1
            for j, caracter in enumerate(paso_str):
                if caracter == '-':
                    posicion_guion = j
                    break

            if posicion_guion > 0:
                parte_hilera = paso_str[:posicion_guion]
                parte_planta = paso_str[posicion_guion + 1:]

                hilera = int(parte_hilera[1:])  # Quitar 'H' y convertir a int
                planta = int(parte_planta[1:])  # Quitar 'P' y convertir a int

                paso = PasoRiego(hilera, planta, False)
                self.secuencia_riego.encolar(paso)

    def parsear_plan_desde_cadena(self, plan_cadena):
        self.secuencia_riego.limpiar()
        self.plan_original.limpiar()

        if not plan_cadena.strip():
            return

        # Procesar la cadena manualmente sin usar split()
        paso_actual = ""
        for caracter in plan_cadena:
            if caracter == ',':
                if paso_actual.strip():
                    self._procesar_paso_individual(paso_actual.strip())
                paso_actual = ""
            else:
                paso_actual += caracter

        # Procesar el último paso si existe
        if paso_actual.strip():
            self._procesar_paso_individual(paso_actual.strip())

    def _procesar_paso_individual(self, paso_str):
        if '-' in paso_str:
            try:
                # Buscar la posición del guión manualmente
                posicion_guion = -1
                for i, caracter in enumerate(paso_str):
                    if caracter == '-':
                        posicion_guion = i
                        break

                if posicion_guion > 0:
                    parte_hilera = paso_str[:posicion_guion]
                    parte_planta = paso_str[posicion_guion + 1:]

                    # Quitar 'H' y convertir a int
                    hilera = int(parte_hilera[1:])
                    # Quitar 'P' y convertir a int
                    planta = int(parte_planta[1:])
                    self.agregar_paso(hilera, planta)
            except (ValueError, IndexError):
                pass  # Ignorar pasos mal formateados

    def __str__(self):
        return f"Plan de riego: {self.obtener_plan_original()} - Pasos pendientes: {self.secuencia_riego.obtener_tamaño()}"

    def __repr__(self):
        return f"PlanRiego(pasos={self.plan_original.obtener_tamaño()}, pendientes={self.secuencia_riego.obtener_tamaño()})"
