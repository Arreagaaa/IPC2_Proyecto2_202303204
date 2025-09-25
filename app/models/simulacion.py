from ..tdas import ListaEnlazada
from .invernadero import Invernadero


class Simulacion:
    def __init__(self, invernadero):
        self.invernadero = invernadero
        self.tiempo_actual = 0
        self.tiempo_total = 0
        # Registro de instrucciones por tiempo
        self.registro_instrucciones = ListaEnlazada()
        self.paso_actual_plan = None
        self.simulacion_completada = False

    def ejecutar_simulacion(self):
        # Validar configuración antes de iniciar
        errores = self.invernadero.validar_configuracion()
        if errores:
            return False, errores

        # Reiniciar estado
        self.invernadero.reiniciar_estado()
        self.tiempo_actual = 0
        self.registro_instrucciones.limpiar()
        self.simulacion_completada = False

        # Ejecutar simulación paso a paso
        while self.invernadero.plan_riego.hay_pasos_pendientes():
            self.tiempo_actual += 1
            instrucciones_tiempo = self._ejecutar_paso_simulacion()
            self.registro_instrucciones.insertar_al_final({
                'tiempo': self.tiempo_actual,
                'instrucciones': instrucciones_tiempo
            })

        # Finalizar todos los drones
        self._finalizar_drones()

        self.tiempo_total = self.tiempo_actual
        self.simulacion_completada = True

        return True, []

    def _ejecutar_paso_simulacion(self):
        instrucciones = {}

        # Obtener el siguiente paso del plan
        if self.paso_actual_plan is None and self.invernadero.plan_riego.hay_pasos_pendientes():
            self.paso_actual_plan = self.invernadero.plan_riego.obtener_siguiente_paso()

        # Generar instrucciones para cada dron
        for dron in self.invernadero.drones:
            if not dron.finalizado:
                instruccion = self._generar_instruccion_dron(dron)
                instrucciones[dron.id] = instruccion

        return instrucciones

    def _generar_instruccion_dron(self, dron):
        if self.paso_actual_plan is None:
            return "Esperar"

        hilera_objetivo = self.paso_actual_plan['hilera']
        planta_objetivo = self.paso_actual_plan['planta']

        # Si este dron no es el asignado a la hilera objetivo, esperar
        if dron.hilera_asignada.numero != hilera_objetivo:
            return "Esperar"

        # Si el dron ya está en la posición correcta, regar
        if dron.puede_regar(planta_objetivo):
            dron.regar_planta_actual()
            self.paso_actual_plan = None  # Completar este paso
            return "Regar"

        # Calcular movimiento necesario
        movimientos_necesarios = dron.obtener_posicion_objetivo(
            planta_objetivo)

        if movimientos_necesarios > 0:
            dron.mover_adelante()
            nueva_posicion = dron.obtener_estado_posicion()
            return f"Adelante ({nueva_posicion})"
        elif movimientos_necesarios < 0:
            dron.mover_atras()
            nueva_posicion = dron.obtener_estado_posicion()
            return f"Atrás ({nueva_posicion})"

        return "Esperar"

    def _finalizar_drones(self):
        drones_activos = []
        for dron in self.invernadero.drones:
            if not dron.finalizado:
                drones_activos.append(dron)

        while drones_activos:
            self.tiempo_actual += 1
            instrucciones = {}
            drones_a_remover = []

            for dron in drones_activos:
                if dron.posicion_actual > 0:
                    dron.mover_atras()
                    if dron.posicion_actual == 0:
                        dron.finalizar()
                        instrucciones[dron.id] = "FIN"
                        drones_a_remover.append(dron)
                    else:
                        nueva_posicion = dron.obtener_estado_posicion()
                        instrucciones[dron.id] = f"Regresar ({nueva_posicion})"
                else:
                    dron.finalizar()
                    instrucciones[dron.id] = "FIN"
                    drones_a_remover.append(dron)

            # Remover drones finalizados
            for dron in drones_a_remover:
                drones_activos.remove(dron)

            if instrucciones:
                self.registro_instrucciones.insertar_al_final({
                    'tiempo': self.tiempo_actual,
                    'instrucciones': instrucciones
                })

    def obtener_resultados(self):
        if not self.simulacion_completada:
            return None

        # Calcular totales por dron
        resultados_drones = []
        total_agua = 0
        total_fertilizante = 0

        for dron in self.invernadero.drones:
            resultados_drones.append({
                'id': dron.id,
                'agua_utilizada': dron.agua_utilizada,
                'fertilizante_utilizado': dron.fertilizante_utilizado
            })
            total_agua += dron.agua_utilizada
            total_fertilizante += dron.fertilizante_utilizado

        return {
            'tiempo_total': self.tiempo_total,
            'total_agua': total_agua,
            'total_fertilizante': total_fertilizante,
            'resultados_drones': resultados_drones,
            'plan_ejecutado': self.invernadero.plan_riego.obtener_plan_original()
        }

    def obtener_registro_instrucciones(self):
        registro = []
        for entrada in self.registro_instrucciones:
            registro.append(entrada)
        return registro

    def generar_reporte_detallado(self):
        if not self.simulacion_completada:
            return "Simulación no completada"

        reporte = []
        reporte.append(
            f"=== REPORTE DE SIMULACIÓN - {self.invernadero.nombre} ===\n")

        # Información del plan
        reporte.append(
            f"Plan de riego ejecutado: {self.invernadero.plan_riego.obtener_plan_original()}")
        reporte.append(
            f"Tiempo total de ejecución: {self.tiempo_total} segundos\n")

        # Registro de instrucciones
        reporte.append("=== INSTRUCCIONES POR TIEMPO ===")
        for entrada in self.registro_instrucciones:
            tiempo = entrada['tiempo']
            instrucciones = entrada['instrucciones']
            reporte.append(f"Tiempo {tiempo}:")
            for dron_id, instruccion in instrucciones.items():
                reporte.append(f"  {dron_id}: {instruccion}")

        # Resultados
        resultados = self.obtener_resultados()
        reporte.append(f"\n=== RESULTADOS FINALES ===")
        reporte.append(
            f"Agua total utilizada: {resultados['total_agua']} litros")
        reporte.append(
            f"Fertilizante total utilizado: {resultados['total_fertilizante']} gramos")

        reporte.append(f"\n=== RESULTADOS POR DRON ===")
        for resultado_dron in resultados['resultados_drones']:
            reporte.append(f"{resultado_dron['id']}: {resultado_dron['agua_utilizada']} litros, "
                           f"{resultado_dron['fertilizante_utilizado']} gramos")

        return "\n".join(reporte)

    def __str__(self):
        estado = "Completada" if self.simulacion_completada else "Pendiente"
        return f"Simulación {estado} - Tiempo: {self.tiempo_actual}s"

    def __repr__(self):
        return f"Simulacion(tiempo={self.tiempo_actual}, completada={self.simulacion_completada})"
