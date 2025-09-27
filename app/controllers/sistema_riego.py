from app.utils.xml_parser import XMLParser
from app.utils.xml_generator import XMLGenerator
from app.utils.html_generator import HTMLGenerator
from app.utils.graphviz_generator import GraphvizGenerator
from app.models.simulacion import Simulacion
from app.models.resultado import Resultado
from app.tdas.lista_enlazada import ListaEnlazada


# controlador principal del sistema de riego
class SistemaRiego:
    def __init__(self):
        self.xml_parser = XMLParser()
        self.xml_generator = XMLGenerator()
        self.html_generator = HTMLGenerator()
        self.graphviz_generator = GraphvizGenerator()
        self.simulaciones = ListaEnlazada()
        self.invernadero_actual = None

    @property
    def drones(self):
        return self.xml_parser.obtener_drones()

    @property
    def invernaderos(self):
        return self.xml_parser.obtener_invernaderos()

    def cargar_configuracion(self, ruta_archivo):
        print("Cargando configuración desde archivo XML...")

        resultado = self.xml_parser.cargar_archivo(ruta_archivo)

        if not resultado.es_exitoso():
            print(f"Error al cargar archivo: {resultado.obtener_mensaje()}")
            return False

        print("Archivo cargado exitosamente")
        print(self.xml_parser.generar_resumen_carga())

        # Validar configuración
        errores = self.xml_parser.validar_configuracion()
        if errores.obtener_tamaño() > 0:
            print("\nErrores encontrados en la configuración:")
            for i in range(errores.obtener_tamaño()):
                print(f"  - {errores.obtener(i)}")
            return False

        print("\nConfiguración validada correctamente")
        return True

    def seleccionar_invernadero(self, indice=0):
        invernaderos = self.xml_parser.obtener_invernaderos()

        if indice < 0 or indice >= invernaderos.obtener_tamaño():
            print(f"Índice de invernadero inválido: {indice}")
            return False

        self.invernadero_actual = invernaderos.obtener(indice)
        print(f"Invernadero seleccionado: {self.invernadero_actual.nombre}")
        return True

    def ejecutar_simulacion(self):
        if self.invernadero_actual is None:
            print("No hay invernadero seleccionado")
            return False

        print(f"Iniciando simulación para: {self.invernadero_actual.nombre}")
        print(
            f"Plan de riego: {self.invernadero_actual.plan_riego.obtener_plan_original()}")

        simulacion = Simulacion(self.invernadero_actual)
        resultado = simulacion.ejecutar_simulacion()

        if not resultado.es_exitoso():
            print("Error en la simulación:")
            errores = resultado.obtener_data()
            for i in range(errores.obtener_tamaño()):
                print(f"  - {errores.obtener(i)}")
            return False

        # Guardar simulación
        self.simulaciones.insertar_al_final(simulacion)

        print("Simulación completada exitosamente")
        self._mostrar_resultados_simulacion(simulacion)

        return True

    def _mostrar_resultados_simulacion(self, simulacion):
        resultados = simulacion.obtener_resultados()

        print(f"\n=== RESULTADOS DE SIMULACIÓN ===")
        print(f"Tiempo total: {resultados.tiempo_total} segundos")
        print(f"Agua total utilizada: {resultados.total_agua} litros")
        print(
            f"Fertilizante total utilizado: {resultados.total_fertilizante} gramos")

        print(f"\nResultados por dron:")
        for i in range(resultados.resultados_drones.obtener_tamaño()):
            resultado_dron = resultados.resultados_drones.obtener(i)
            print(
                f"  {resultado_dron.id}: {resultado_dron.agua_utilizada}L, {resultado_dron.fertilizante_utilizado}g")

    def generar_archivo_salida(self, ruta_salida):
        if self.simulaciones.obtener_tamaño() == 0:
            print("No hay simulaciones para generar salida")
            return False

        # Usar la última simulación
        ultima_simulacion = self.simulaciones.obtener(
            self.simulaciones.obtener_tamaño() - 1)
        resultados = ultima_simulacion.obtener_resultados()
        registro_instrucciones = ultima_simulacion.obtener_registro_instrucciones()

        resultado = self.xml_generator.generar_archivo_salida(
            self.invernadero_actual,
            resultados,
            registro_instrucciones,
            ruta_salida
        )

        if resultado.es_exitoso():
            print(f"Archivo de salida generado: {ruta_salida}")
        else:
            print(
                f"Error al generar archivo de salida: {resultado.obtener_mensaje()}")

        return resultado.es_exitoso()

    def mostrar_reporte_detallado(self):
        if self.simulaciones.obtener_tamaño() == 0:
            print("No hay simulaciones para mostrar")
            return

        ultima_simulacion = self.simulaciones.obtener(
            self.simulaciones.obtener_tamaño() - 1)
        reporte = ultima_simulacion.generar_reporte_detallado()
        print(reporte)

    def listar_invernaderos(self):
        invernaderos = self.xml_parser.obtener_invernaderos()

        if invernaderos.obtener_tamaño() == 0:
            print("No hay invernaderos cargados")
            return

        print("Invernaderos disponibles:")
        for i in range(invernaderos.obtener_tamaño()):
            invernadero = invernaderos.obtener(i)
            estado = " (SELECCIONADO)" if invernadero == self.invernadero_actual else ""
            print(f"  {i}: {invernadero.nombre}{estado}")

    def obtener_estado_sistema(self):
        estado = ListaEnlazada()

        estado.insertar_al_final("=== ESTADO DEL SISTEMA ===")

        drones = self.xml_parser.obtener_drones()
        invernaderos = self.xml_parser.obtener_invernaderos()

        estado.insertar_al_final(f"Drones cargados: {drones.obtener_tamaño()}")
        estado.insertar_al_final(
            f"Invernaderos cargados: {invernaderos.obtener_tamaño()}")
        estado.insertar_al_final(
            f"Simulaciones ejecutadas: {self.simulaciones.obtener_tamaño()}")

        if self.invernadero_actual:
            estado.insertar_al_final(
                f"Invernadero actual: {self.invernadero_actual.nombre}")
        else:
            estado.insertar_al_final("Invernadero actual: Ninguno")

        # Convertir a string
        resultado = ""
        for i in range(estado.obtener_tamaño()):
            if i > 0:
                resultado += "\n"
            resultado += estado.obtener(i)

        return resultado

    def generar_reporte_html(self, ruta_reporte=None):
        # Generar reporte HTML para el invernadero actual
        if self.invernadero_actual is None:
            print("No hay invernadero seleccionado")
            return False

        if self.simulaciones.obtener_tamaño() == 0:
            print("No hay simulaciones para generar reporte")
            return False

        # Usar la última simulación
        ultima_simulacion = self.simulaciones.obtener(
            self.simulaciones.obtener_tamaño() - 1)
        resultados = ultima_simulacion.obtener_resultados()
        registro_instrucciones = ultima_simulacion.obtener_registro_instrucciones()

        # Generar nombre de archivo si no se proporciona
        if ruta_reporte is None:
            nombre_archivo = self.invernadero_actual.nombre.replace(" ", "_")
            ruta_reporte = f"ReporteInvernadero_{nombre_archivo}.html"

        # Generar contenido HTML
        contenido_html = self.html_generator.generar_reporte_invernadero(
            self.invernadero_actual,
            resultados,
            registro_instrucciones
        )

        # Guardar archivo
        resultado = self.html_generator.guardar_reporte(
            contenido_html, ruta_reporte)

        if resultado.es_exitoso():
            print(f"Reporte HTML generado: {ruta_reporte}")
        else:
            print(
                f"Error al generar reporte HTML: {resultado.obtener_mensaje()}")

        return resultado.es_exitoso()

    def generar_grafos_tdas(self, prefijo_archivo="grafo"):
        # Generar gráficos de las TDAs utilizadas
        if self.invernadero_actual is None:
            print("No hay invernadero seleccionado")
            return False

        resultados = ListaEnlazada()

        # Grafo del plan de riego
        plan_riego = self.invernadero_actual.plan_riego
        resultado1 = self.graphviz_generator.generar_grafo_plan_riego(
            plan_riego, f"{prefijo_archivo}_plan_riego.dot")
        resultados.insertar_al_final(resultado1)

        # Grafo de la cola de riego (si tiene pasos pendientes)
        resultado2 = self.graphviz_generator.generar_grafo_cola_riego(
            plan_riego.secuencia_riego, f"{prefijo_archivo}_cola_riego.dot")
        resultados.insertar_al_final(resultado2)

        # Grafo del estado de los drones
        resultado3 = self.graphviz_generator.generar_grafo_estado_drones(
            self.invernadero_actual.drones, f"{prefijo_archivo}_drones.dot")
        resultados.insertar_al_final(resultado3)

        # Mostrar resultados
        todos_exitosos = True
        for i in range(resultados.obtener_tamaño()):
            resultado = resultados.obtener(i)
            print(resultado.obtener_mensaje())
            if not resultado.es_exitoso():
                todos_exitosos = False

        if todos_exitosos:
            print("Todos los gráficos Graphviz fueron generados exitosamente")
            print("Para visualizar, use: dot -Tpng archivo.dot -o archivo.png")

        return todos_exitosos

    def generar_reporte_completo(self):
        # Generar reporte completo: XML + HTML + Graphviz
        if self.invernadero_actual is None:
            print("No hay invernadero seleccionado")
            return False

        if self.simulaciones.obtener_tamaño() == 0:
            print("No hay simulaciones ejecutadas")
            return False

        print("Generando reporte completo...")

        # Generar archivo XML de salida
        exito_xml = self.generar_archivo_salida("output/salida.xml")

        # Generar reporte HTML
        exito_html = self.generar_reporte_html()

        # Generar gráficos Graphviz
        exito_graphviz = self.generar_grafos_tdas()

        if exito_xml and exito_html and exito_graphviz:
            print("Reporte completo generado exitosamente")
            print("Archivos generados:")
            print("  - output/salida.xml (XML de salida)")
            print(
                f"  - ReporteInvernadero_{self.invernadero_actual.nombre.replace(' ', '_')}.html (Reporte HTML)")
            print("  - grafo_*.dot (Gráficos Graphviz)")
            return True
        else:
            print("Hubo errores al generar algunos componentes del reporte")
            return False

    def limpiar_sistema(self):
        self.xml_parser = XMLParser()
        self.xml_generator = XMLGenerator()
        self.html_generator = HTMLGenerator()
        self.graphviz_generator = GraphvizGenerator()
        self.simulaciones.limpiar()
        self.invernadero_actual = None
        print("Sistema limpiado")
