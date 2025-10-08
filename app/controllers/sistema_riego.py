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

    def ejecutar_simulacion(self, nombre_plan=None):
        if self.invernadero_actual is None:
            return False

        simulacion = Simulacion(self.invernadero_actual)
        resultado = simulacion.ejecutar_simulacion()

        if not resultado.es_exitoso():
            return False

        # Guardar simulación
        self.simulaciones.insertar_al_final(simulacion)

        return True

    def _mostrar_resultados_simulacion(self, simulacion):
        # Método para mostrar resultados si es necesario
        # Los resultados se pueden obtener llamando simulacion.obtener_resultados()
        pass

    def generar_archivo_salida(self, ruta_salida):
        if self.simulaciones.obtener_tamaño() == 0:
            return False

        # Usar la última simulación
        ultima_simulacion = self.simulaciones.obtener(
            self.simulaciones.obtener_tamaño() - 1)
        resultados = ultima_simulacion.obtener_resultados()
        registro_instrucciones = ultima_simulacion.obtener_registro_instrucciones()

        # Si no se especifica ruta, generar con estructura organizada
        if ruta_salida == "output/salida.xml" or not ruta_salida:
            nombre_invernadero = self.invernadero_actual.nombre.replace(
                " ", "_")
            carpeta_invernadero = f"output/{nombre_invernadero}"
            ruta_salida = f"{carpeta_invernadero}/salida_{nombre_invernadero}.xml"

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

        # Generar nombre de archivo y estructura de carpetas si no se proporciona
        if ruta_reporte is None:
            nombre_archivo = self.invernadero_actual.nombre.replace(" ", "_")
            carpeta_invernadero = f"output/{nombre_archivo}"
            ruta_reporte = f"{carpeta_invernadero}/ReporteInvernadero_{nombre_archivo}.html"

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

    def generar_grafos_tdas(self, prefijo_archivo="grafo", tiempo_t=None):
        # Generar gráficos de las TDAs utilizadas con conversión PNG y HTML
        # tiempo_t: momento específico para visualizar el estado de las TDAs
        if self.invernadero_actual is None:
            print("No hay invernadero seleccionado")
            return False

        # Crear estructura de carpetas organizada por invernadero
        nombre_invernadero = self.invernadero_actual.nombre.replace(" ", "_")
        carpeta_graficos = f"output/{nombre_invernadero}/graficos"

        # Actualizar prefijo con la nueva ruta
        prefijo_completo = f"{carpeta_graficos}/{prefijo_archivo}"

        resultados = ListaEnlazada()

        # Grafo del plan de riego
        plan_riego = self.invernadero_actual.plan_riego
        resultado1 = self.graphviz_generator.generar_grafo_plan_riego(
            plan_riego, f"{prefijo_completo}_plan_riego.dot")
        resultados.insertar_al_final(resultado1)

        # Grafo de la cola de riego
        resultado2 = self.graphviz_generator.generar_grafo_cola_riego(
            plan_riego.secuencia_riego, f"{prefijo_completo}_cola_riego.dot")
        resultados.insertar_al_final(resultado2)

        # Grafo del estado de los drones
        resultado3 = self.graphviz_generator.generar_grafo_estado_drones(
            self.invernadero_actual.drones, f"{prefijo_completo}_drones.dot")
        resultados.insertar_al_final(resultado3)

        # Generar visualización de TDAs en tiempo_t si se especifica
        if tiempo_t is not None:
            resultado4 = self.graphviz_generator.generar_visualizacion_tdas_tiempo_t(
                self.invernadero_actual, tiempo_t, f"{prefijo_completo}_tiempo_{tiempo_t}")
            resultados.insertar_al_final(resultado4)

        # Convertir DOT a PNG y generar HTML
        archivos_generados = ListaEnlazada()
        todos_exitosos = True

        for i in range(resultados.obtener_tamaño()):
            resultado = resultados.obtener(i)
            print(resultado.obtener_mensaje())

            if resultado.es_exitoso():
                # Obtener nombre del archivo DOT
                archivo_dot = resultado.obtener_mensaje().split(": ")[-1]

                # Convertir a PNG
                archivo_png = archivo_dot.replace(".dot", ".png")
                resultado_png = self.graphviz_generator.convertir_dot_a_png(
                    archivo_dot, archivo_png)

                if resultado_png.es_exitoso():
                    archivos_generados.insertar_al_final(archivo_png)

                    # Generar página HTML de visualización
                    nombre_base = archivo_dot.replace(".dot", "")
                    resultado_html = self.graphviz_generator.generar_pagina_visualizacion_html(
                        archivo_png, f"{nombre_base}.html", nombre_base)

                    if not resultado_html.es_exitoso():
                        todos_exitosos = False
                        print(
                            f"Error generando HTML: {resultado_html.obtener_mensaje()}")
                else:
                    todos_exitosos = False
                    print(
                        f"Error convirtiendo PNG: {resultado_png.obtener_mensaje()}")
            else:
                todos_exitosos = False

        if todos_exitosos:
            print(
                "Todos los gráficos fueron generados exitosamente con conversión PNG y HTML")
        else:
            print("Algunos gráficos tuvieron errores durante la generación")

        return todos_exitosos

    def generar_grafos_tdas_con_simulacion(self, prefijo_archivo="grafo", tiempo_t=None, simulacion=None):
        # Generar gráficos de las TDAs con datos de simulación específica
        # tiempo_t: momento específico para visualizar el estado de las TDAs
        # simulacion: simulación de la cual obtener los datos de estado
        if self.invernadero_actual is None:
            print("No hay invernadero seleccionado")
            return False

        # Crear estructura de carpetas organizada por invernadero
        nombre_invernadero = self.invernadero_actual.nombre.replace(" ", "_")
        carpeta_graficos = f"output/{nombre_invernadero}/graficos"

        # Actualizar prefijo con la nueva ruta
        prefijo_completo = f"{carpeta_graficos}/{prefijo_archivo}"

        resultados = ListaEnlazada()

        # Generar los 3 gráficos separados requeridos
        plan_riego = self.invernadero_actual.plan_riego

        # 1. Grafo del plan de riego en tiempo específico
        resultado1 = self.graphviz_generator.generar_grafo_plan_riego_tiempo_t(
            plan_riego, f"{prefijo_completo}_plan_riego.dot", tiempo_t, simulacion)
        resultados.insertar_al_final(resultado1)

        # 2. Grafo de la cola de riego en tiempo específico
        resultado2 = self.graphviz_generator.generar_grafo_cola_riego_tiempo_t(
            plan_riego.secuencia_riego, f"{prefijo_completo}_cola_riego.dot", tiempo_t, simulacion)
        resultados.insertar_al_final(resultado2)

        # 3. Grafo del estado de los drones en tiempo específico
        resultado3 = self.graphviz_generator.generar_grafo_estado_drones_tiempo_t(
            self.invernadero_actual.drones, f"{prefijo_completo}_drones.dot", tiempo_t, simulacion)
        resultados.insertar_al_final(resultado3)

        # 4. Grafo unificado del estado completo del sistema en tiempo t
        resultado4 = self.graphviz_generator.generar_visualizacion_tdas_tiempo_t_con_simulacion(
            self.invernadero_actual, tiempo_t, f"{prefijo_completo}_tiempo_{tiempo_t}", simulacion)
        resultados.insertar_al_final(resultado4)

        # Convertir DOT a PNG y generar HTML
        archivos_generados = ListaEnlazada()
        todos_exitosos = True

        for i in range(resultados.obtener_tamaño()):
            resultado = resultados.obtener(i)
            print(resultado.obtener_mensaje())

            if resultado.es_exitoso():
                # Obtener nombre del archivo DOT
                archivo_dot = resultado.obtener_mensaje().split(": ")[-1]

                # Convertir a PNG
                archivo_png = archivo_dot.replace(".dot", ".png")
                resultado_png = self.graphviz_generator.convertir_dot_a_png(
                    archivo_dot, archivo_png)

                if resultado_png.es_exitoso():
                    archivos_generados.insertar_al_final(archivo_png)

                    # Generar página HTML de visualización
                    nombre_base = archivo_dot.replace(".dot", "")
                    resultado_html = self.graphviz_generator.generar_pagina_visualizacion_html(
                        archivo_png, f"{nombre_base}.html", nombre_base)

                    if not resultado_html.es_exitoso():
                        todos_exitosos = False
                        print(
                            f"Error generando HTML: {resultado_html.obtener_mensaje()}")
                else:
                    todos_exitosos = False
                    print(
                        f"Error convirtiendo PNG: {resultado_png.obtener_mensaje()}")
            else:
                todos_exitosos = False

        if todos_exitosos:
            print("Visualización de TDAs generada exitosamente con datos de simulación")
        else:
            print("Error generando visualización de TDAs con datos de simulación")

        return todos_exitosos

    def visualizar_tdas_en_tiempo(self, tiempo_t):
        # Visualizar el estado de las TDAs en un momento específico t
        # Requerido por el enunciado para mostrar el estado de estructuras de datos
        if self.invernadero_actual is None:
            print(
                f"No hay invernadero seleccionado para visualizar en tiempo {tiempo_t}")
            return False

        # Verificar que hay simulaciones ejecutadas
        if self.simulaciones.obtener_tamaño() == 0:
            print(
                f"No hay simulaciones ejecutadas para visualizar en tiempo {tiempo_t}")
            print("Ejecute una simulación primero antes de visualizar las TDAs")
            return False

        print(f"Generando visualización de TDAs en tiempo t={tiempo_t}")

        # Obtener la última simulación ejecutada
        ultima_simulacion = self.simulaciones.obtener(
            self.simulaciones.obtener_tamaño() - 1)

        # Generar archivos de visualización con datos de la simulación
        prefijo = f"visualization_t{tiempo_t}"
        exito = self.generar_grafos_tdas_con_simulacion(
            prefijo, tiempo_t, ultima_simulacion)

        if exito:
            nombre_invernadero = self.invernadero_actual.nombre.replace(
                " ", "_")
            print(
                f"Visualización generada exitosamente para tiempo t={tiempo_t}")
            print(
                f"Archivos generados en: output/{nombre_invernadero}/graficos/{prefijo}_*.png")
            print(
                f"Páginas HTML en: output/{nombre_invernadero}/graficos/{prefijo}_*.html")
        else:
            print(f"Error generando visualización para tiempo t={tiempo_t}")

        return exito

    def obtener_archivos_visualizacion_disponibles(self):
        # Obtener lista de archivos de visualización disponibles
        # Para uso en la interfaz Flask
        import os
        archivos = ListaEnlazada()

        try:
            # Buscar en la estructura organizada
            directorio_output = "output"
            if os.path.exists(directorio_output):
                for invernadero_dir in os.listdir(directorio_output):
                    directorio_grafos = os.path.join(
                        directorio_output, invernadero_dir, "graficos")
                    if os.path.exists(directorio_grafos):
                        for archivo in os.listdir(directorio_grafos):
                            if archivo.endswith('.html'):
                                # Incluir la ruta relativa para el invernadero
                                ruta_relativa = f"{invernadero_dir}/{archivo}"
                                archivos.insertar_al_final(ruta_relativa)
        except Exception as e:
            print(f"Error listando archivos de visualización: {e}")

        return archivos

    def generar_reporte_completo(self):
        # Generar reporte completo: XML + HTML + Graphviz
        if self.invernadero_actual is None:
            print("No hay invernadero seleccionado")
            return False

        if self.simulaciones.obtener_tamaño() == 0:
            print("No hay simulaciones ejecutadas")
            return False

        print("Generando reporte completo...")

        # Crear estructura de carpetas organizada por invernadero
        nombre_invernadero = self.invernadero_actual.nombre.replace(" ", "_")

        # Generar archivo XML de salida
        exito_xml = self.generar_archivo_salida(
            f"output/{nombre_invernadero}/salida.xml")

        # Generar reporte HTML
        exito_html = self.generar_reporte_html()

        # Generar gráficos Graphviz
        exito_graphviz = self.generar_grafos_tdas()

        if exito_xml and exito_html and exito_graphviz:
            print("Reporte completo generado exitosamente")
            print("Archivos generados en estructura organizada:")
            print(
                f"  - output/{nombre_invernadero}/salida.xml (XML de salida)")
            print(
                f"  - output/{nombre_invernadero}/ReporteInvernadero_{nombre_invernadero}.html (Reporte HTML)")
            print(
                f"  - output/{nombre_invernadero}/graficos/ (Gráficos Graphviz)")
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
