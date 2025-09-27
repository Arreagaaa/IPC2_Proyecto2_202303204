from app.tdas.lista_enlazada import ListaEnlazada
from app.models.invernadero import Invernadero
from app.models.resultado import Resultado


# registro de instrucciones en un momento dado
class RegistroTiempo:
    def __init__(self, tiempo, instrucciones):
        self.tiempo = tiempo
        self.instrucciones = instrucciones


# contenedor de instrucciones para todos los drones
class InstruccionesDron:
    def __init__(self):
        self.instrucciones = ListaEnlazada()

    def agregar_instruccion(self, dron_id, instruccion):
        self.instrucciones.insertar_al_final(
            InstruccionDron(dron_id, instruccion))

    def obtener_instruccion(self, dron_id):
        for instruccion in self.instrucciones:
            if instruccion.dron_id == dron_id:
                return instruccion.instruccion
        return None


# instruccion individual para un dron
class InstruccionDron:
    def __init__(self, dron_id, instruccion):
        self.dron_id = dron_id
        self.instruccion = instruccion


# resultado de un dron al finalizar simulacion
class ResultadoDron:
    def __init__(self, id_dron, agua_utilizada, fertilizante_utilizado):
        self.id = id_dron
        self.agua_utilizada = agua_utilizada
        self.fertilizante_utilizado = fertilizante_utilizado


# resultados completos de la simulacion
class ResultadosSimulacion:
    def __init__(self, tiempo_total, total_agua, total_fertilizante, resultados_drones, plan_ejecutado):
        self.tiempo_total = tiempo_total
        self.total_agua = total_agua
        self.total_fertilizante = total_fertilizante
        self.resultados_drones = resultados_drones
        self.plan_ejecutado = plan_ejecutado


# simulador del sistema de riego robotico
class Simulacion:
    def __init__(self, invernadero):
        self.invernadero = invernadero
        self.tiempo_actual = 0
        self.tiempo_total = 0
        # registro de instrucciones por tiempo
        self.registro_instrucciones = ListaEnlazada()
        self.paso_actual_plan = None
        self.simulacion_completada = False

    def ejecutar_simulacion(self):
        # validar configuración antes de iniciar
        errores = self.invernadero.validar_configuracion()
        if errores.obtener_tamaño() > 0:
            return Resultado(False, "Errores de validación encontrados", errores)

        # reiniciar estado
        self.invernadero.reiniciar_estado()
        self.tiempo_actual = 0
        self.registro_instrucciones.limpiar()
        self.simulacion_completada = False

        # ejecutar simulación paso a paso
        while self.invernadero.plan_riego.hay_pasos_pendientes():
            self.tiempo_actual += 1
            instrucciones_tiempo = self._ejecutar_paso_simulacion()
            self.registro_instrucciones.insertar_al_final(
                RegistroTiempo(self.tiempo_actual, instrucciones_tiempo)
            )

        # finalizar todos los drones
        self._finalizar_drones()

        self.tiempo_total = self.tiempo_actual
        self.simulacion_completada = True

        # crear lista enlazada vacía para errores en lugar de array nativo
        errores_vacios = ListaEnlazada()
        return Resultado(True, "Simulación completada exitosamente", errores_vacios)

    def _ejecutar_paso_simulacion(self):
        instrucciones = InstruccionesDron()

        # obtener el siguiente paso del plan
        if self.paso_actual_plan is None and self.invernadero.plan_riego.hay_pasos_pendientes():
            self.paso_actual_plan = self.invernadero.plan_riego.obtener_siguiente_paso()

        # generar instrucciones para cada dron
        for dron in self.invernadero.drones:
            if not dron.finalizado:
                instruccion = self._generar_instruccion_dron(dron)
                instrucciones.agregar_instruccion(dron.id, instruccion)

        return instrucciones

    def _generar_instruccion_dron(self, dron):
        if self.paso_actual_plan is None:
            return "Esperar"

        hilera_objetivo = self.paso_actual_plan.hilera
        planta_objetivo = self.paso_actual_plan.planta

        # si este dron no es el asignado a la hilera objetivo, esperar
        if dron.hilera_asignada.numero != hilera_objetivo:
            return "Esperar"

        # si el dron ya está en la posición correcta, regar
        if dron.puede_regar(planta_objetivo):
            dron.regar_planta_actual()
            self.paso_actual_plan = None  # completar este paso
            return "Regar"

        # calcular movimiento necesario
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
        drones_activos = ListaEnlazada()
        for dron in self.invernadero.drones:
            if not dron.finalizado:
                drones_activos.insertar_al_final(dron)

        while drones_activos.obtener_tamaño() > 0:
            self.tiempo_actual += 1
            instrucciones = InstruccionesDron()
            drones_a_remover = ListaEnlazada()

            for dron in drones_activos:
                if dron.posicion_actual > 0:
                    dron.mover_atras()
                    if dron.posicion_actual == 0:
                        dron.finalizar()
                        instrucciones.agregar_instruccion(dron.id, "FIN")
                        drones_a_remover.insertar_al_final(dron)
                    else:
                        nueva_posicion = dron.obtener_estado_posicion()
                        instrucciones.agregar_instruccion(
                            dron.id, f"Regresar ({nueva_posicion})")
                else:
                    dron.finalizar()
                    instrucciones.agregar_instruccion(dron.id, "FIN")
                    drones_a_remover.insertar_al_final(dron)

            # remover drones finalizados
            for dron_a_remover in drones_a_remover:
                for i in range(drones_activos.obtener_tamaño()):
                    if drones_activos.obtener(i).id == dron_a_remover.id:
                        drones_activos.eliminar_en_posicion(i)
                        break

            if instrucciones.instrucciones.obtener_tamaño() > 0:
                self.registro_instrucciones.insertar_al_final(
                    RegistroTiempo(self.tiempo_actual, instrucciones)
                )

    def obtener_resultados(self):
        if not self.simulacion_completada:
            return None

        # calcular totales por dron
        resultados_drones = ListaEnlazada()
        total_agua = 0
        total_fertilizante = 0

        for dron in self.invernadero.drones:
            resultado_dron = ResultadoDron(
                dron.id,
                dron.agua_utilizada,
                dron.fertilizante_utilizado
            )
            resultados_drones.insertar_al_final(resultado_dron)
            total_agua += dron.agua_utilizada
            total_fertilizante += dron.fertilizante_utilizado

        return ResultadosSimulacion(
            self.tiempo_total,
            total_agua,
            total_fertilizante,
            resultados_drones,
            self.invernadero.plan_riego.obtener_plan_original()
        )

    def obtener_registro_instrucciones(self):
        return self.registro_instrucciones

    def generar_reporte_detallado(self):
        if not self.simulacion_completada:
            return "Simulación no completada"

        reporte = ListaEnlazada()
        reporte.insertar_al_final(
            f"=== REPORTE DE SIMULACIÓN - {self.invernadero.nombre} ===\n")

        # información del plan
        reporte.insertar_al_final(
            f"Plan de riego ejecutado: {self.invernadero.plan_riego.obtener_plan_original()}")
        reporte.insertar_al_final(
            f"Tiempo total de ejecución: {self.tiempo_total} segundos\n")

        # Registro de instrucciones
        reporte.insertar_al_final("=== INSTRUCCIONES POR TIEMPO ===")
        for entrada in self.registro_instrucciones:
            tiempo = entrada.tiempo
            instrucciones = entrada.instrucciones
            reporte.insertar_al_final(f"Tiempo {tiempo}:")
            for instruccion in instrucciones.instrucciones:
                reporte.insertar_al_final(
                    f"  {instruccion.dron_id}: {instruccion.instruccion}")

        # Resultados
        resultados = self.obtener_resultados()
        reporte.insertar_al_final(f"\n=== RESULTADOS FINALES ===")
        reporte.insertar_al_final(
            f"Agua total utilizada: {resultados.total_agua} litros")
        reporte.insertar_al_final(
            f"Fertilizante total utilizado: {resultados.total_fertilizante} gramos")

        reporte.insertar_al_final(f"\n=== RESULTADOS POR DRON ===")
        for resultado_dron in resultados.resultados_drones:
            reporte.insertar_al_final(f"{resultado_dron.id}: {resultado_dron.agua_utilizada} litros, "
                                      f"{resultado_dron.fertilizante_utilizado} gramos")

        # Convertir ListaEnlazada a string
        resultado_final = ""
        for i in range(reporte.obtener_tamaño()):
            if i > 0:
                resultado_final += "\n"
            resultado_final += reporte.obtener(i)
        return resultado_final

    def __str__(self):
        estado = "Completada" if self.simulacion_completada else "Pendiente"
        return f"Simulación {estado} - Tiempo: {self.tiempo_actual}s"

    def __repr__(self):
        return f"Simulacion(tiempo={self.tiempo_actual}, completada={self.simulacion_completada})"
