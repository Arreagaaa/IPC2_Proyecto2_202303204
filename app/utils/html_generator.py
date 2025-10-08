import os
from datetime import datetime
from app.tdas.lista_enlazada import ListaEnlazada
from app.models.resultado import Resultado


class HTMLGenerator:
    def __init__(self):
        pass

    def generar_reporte_invernadero(self, invernadero, resultados_simulacion=None, registro_instrucciones=None):
        # Generar reporte HTML completo para un invernadero
        html = ListaEnlazada()

        # Encabezado HTML
        html.insertar_al_final("<!DOCTYPE html>")
        html.insertar_al_final("<html lang='es'>")
        html.insertar_al_final("<head>")
        html.insertar_al_final("<meta charset='UTF-8'>")
        html.insertar_al_final(
            "<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html.insertar_al_final(
            f"<title>Reporte - {invernadero.nombre}</title>")
        html.insertar_al_final(self._generar_estilos_css())
        html.insertar_al_final("</head>")
        html.insertar_al_final("<body>")

        # Contenido del reporte
        html.insertar_al_final(f"<div class='container'>")
        html.insertar_al_final(
            f"<h1>Reporte de Simulación - {invernadero.nombre}</h1>")
        html.insertar_al_final(
            f"<p class='fecha'>Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>")

        # Información general del invernadero
        html.insertar_al_final("<h2>Información General</h2>")
        html.insertar_al_final("<table class='info-table'>")
        html.insertar_al_final(
            f"<tr><td><strong>Nombre:</strong></td><td>{invernadero.nombre}</td></tr>")
        html.insertar_al_final(
            f"<tr><td><strong>Número de hileras:</strong></td><td>{invernadero.hileras.obtener_tamaño()}</td></tr>")
        html.insertar_al_final(
            f"<tr><td><strong>Drones asignados:</strong></td><td>{invernadero.drones.obtener_tamaño()}</td></tr>")
        html.insertar_al_final(
            f"<tr><td><strong>Plan de riego:</strong></td><td>{invernadero.plan_riego.obtener_plan_original()}</td></tr>")
        html.insertar_al_final("</table>")

        # Tabla de plantas por hilera
        html.insertar_al_final("<h2>Configuración de Plantas</h2>")
        html.insertar_al_final(self._generar_tabla_plantas(invernadero))

        # Asignación de drones
        html.insertar_al_final("<h2>Asignación de Drones</h2>")
        html.insertar_al_final(self._generar_tabla_drones(invernadero))

        # Resultados de simulación
        if resultados_simulacion:
            html.insertar_al_final("<h2>Resultados de Simulación</h2>")
            html.insertar_al_final(
                self._generar_resultados_simulacion(resultados_simulacion))

        # Instrucciones por tiempo
        if registro_instrucciones:
            html.insertar_al_final("<h2>Instrucciones por Tiempo</h2>")
            html.insertar_al_final(
                self._generar_tabla_instrucciones(registro_instrucciones))

        # Estadísticas finales
        if resultados_simulacion:
            html.insertar_al_final("<h2>Estadísticas Finales</h2>")
            html.insertar_al_final(
                self._generar_estadisticas_finales(resultados_simulacion))

        html.insertar_al_final("</div>")
        html.insertar_al_final("</body>")
        html.insertar_al_final("</html>")

        return self._convertir_lista_a_string(html)

    def _generar_estilos_css(self):
        return """
        <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; border-left: 4px solid #3498db; padding-left: 10px; margin-top: 30px; }
        .fecha { text-align: right; color: #7f8c8d; font-style: italic; }
        .info-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        .info-table td { padding: 8px 12px; border: 1px solid #ddd; }
        .info-table td:first-child { background-color: #ecf0f1; font-weight: bold; width: 200px; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { padding: 10px; text-align: center; border: 1px solid #ddd; }
        th { background-color: #3498db; color: white; font-weight: bold; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        tr:hover { background-color: #e8f4f8; }
        .estadisticas { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat-box { background-color: #3498db; color: white; padding: 20px; border-radius: 8px; text-align: center; min-width: 150px; }
        .stat-number { font-size: 2em; font-weight: bold; }
        .stat-label { font-size: 0.9em; margin-top: 5px; }
        </style>
        """

    def _generar_tabla_plantas(self, invernadero):
        tabla = ListaEnlazada()
        tabla.insertar_al_final("<table>")
        tabla.insertar_al_final(
            "<thead><tr><th>Hilera</th><th>Posición</th><th>Tipo de Planta</th><th>Agua (L)</th><th>Fertilizante (g)</th></tr></thead>")
        tabla.insertar_al_final("<tbody>")

        for i in range(invernadero.hileras.obtener_tamaño()):
            hilera = invernadero.hileras.obtener(i)
            for j in range(hilera.plantas.obtener_tamaño()):
                planta = hilera.plantas.obtener(j)
                tabla.insertar_al_final(
                    f"<tr><td>H{hilera.numero}</td><td>P{planta.posicion}</td><td>{planta.nombre}</td><td>{planta.agua_requerida}</td><td>{planta.fertilizante_requerido}</td></tr>"
                )

        tabla.insertar_al_final("</tbody></table>")
        return self._convertir_lista_a_string(tabla)

    def _generar_tabla_drones(self, invernadero):
        tabla = ListaEnlazada()
        tabla.insertar_al_final("<table>")
        tabla.insertar_al_final(
            "<thead><tr><th>Hilera</th><th>Dron</th></tr></thead>")
        tabla.insertar_al_final("<tbody>")

        for i in range(invernadero.drones.obtener_tamaño()):
            dron = invernadero.drones.obtener(i)
            hilera_num = dron.hilera_asignada.numero if dron.hilera_asignada else "Sin asignar"
            tabla.insertar_al_final(
                f"<tr><td>H{hilera_num}</td><td>{dron.nombre}</td></tr>")

        tabla.insertar_al_final("</tbody></table>")
        return self._convertir_lista_a_string(tabla)

    def _generar_resultados_simulacion(self, resultados):
        resultado = ListaEnlazada()
        resultado.insertar_al_final("<div class='estadisticas'>")
        resultado.insertar_al_final(
            f"<div class='stat-box'><div class='stat-number'>{resultados.tiempo_total}</div><div class='stat-label'>Segundos</div></div>")
        resultado.insertar_al_final(
            f"<div class='stat-box'><div class='stat-number'>{resultados.total_agua}</div><div class='stat-label'>Litros de Agua</div></div>")
        resultado.insertar_al_final(
            f"<div class='stat-box'><div class='stat-number'>{resultados.total_fertilizante}</div><div class='stat-label'>Gramos de Fertilizante</div></div>")
        resultado.insertar_al_final("</div>")

        # Tabla de resultados por dron
        resultado.insertar_al_final("<h3>Resultados por Dron</h3>")
        resultado.insertar_al_final("<table>")
        resultado.insertar_al_final(
            "<thead><tr><th>Dron</th><th>Agua Utilizada (L)</th><th>Fertilizante Utilizado (g)</th></tr></thead>")
        resultado.insertar_al_final("<tbody>")

        for i in range(resultados.resultados_drones.obtener_tamaño()):
            resultado_dron = resultados.resultados_drones.obtener(i)
            resultado.insertar_al_final(
                f"<tr><td>{resultado_dron.id}</td><td>{resultado_dron.agua_utilizada}</td><td>{resultado_dron.fertilizante_utilizado}</td></tr>")

        resultado.insertar_al_final("</tbody></table>")
        return self._convertir_lista_a_string(resultado)

    def _generar_tabla_instrucciones(self, registro_instrucciones):
        tabla = ListaEnlazada()
        tabla.insertar_al_final("<table>")

        # Encabezado dinámico basado en drones disponibles
        encabezado = ListaEnlazada()
        encabezado.insertar_al_final("<thead><tr><th>Tiempo</th>")

        # Obtener lista de drones únicos del registro
        drones_unicos = ListaEnlazada()
        for entrada in registro_instrucciones:
            for instruccion in entrada.instrucciones.instrucciones:
                # Verificar si el dron ya está en la lista
                encontrado = False
                for dron_existente in drones_unicos:
                    if dron_existente == instruccion.dron_id:
                        encontrado = True
                        break
                if not encontrado:
                    drones_unicos.insertar_al_final(instruccion.dron_id)

        # Agregar encabezados de drones
        for dron_id in drones_unicos:
            encabezado.insertar_al_final(f"<th>{dron_id}</th>")
        encabezado.insertar_al_final("</tr></thead>")
        tabla.insertar_al_final(self._convertir_lista_a_string(encabezado))

        # Cuerpo de la tabla
        tabla.insertar_al_final("<tbody>")
        for entrada in registro_instrucciones:
            fila = ListaEnlazada()
            fila.insertar_al_final(f"<tr><td>{entrada.tiempo}</td>")

            # Para cada dron, buscar su instrucción en este tiempo
            for dron_id in drones_unicos:
                instruccion_encontrada = "Esperar"
                for instruccion in entrada.instrucciones.instrucciones:
                    if instruccion.dron_id == dron_id:
                        instruccion_encontrada = instruccion.instruccion
                        break
                fila.insertar_al_final(f"<td>{instruccion_encontrada}</td>")

            fila.insertar_al_final("</tr>")
            tabla.insertar_al_final(self._convertir_lista_a_string(fila))

        tabla.insertar_al_final("</tbody></table>")
        return self._convertir_lista_a_string(tabla)

    def _generar_estadisticas_finales(self, resultados):
        estadisticas = ListaEnlazada()
        estadisticas.insertar_al_final(
            "<p><strong>Información del plan de riego y aplicación de fertilizante robotizado:</strong></p>")
        estadisticas.insertar_al_final("<ul>")
        estadisticas.insertar_al_final(
            f"<li><strong>Tiempo para regado óptimo:</strong> {resultados.tiempo_total} segundos</li>")
        estadisticas.insertar_al_final(
            "<li><strong>Agua requerida por dron:</strong><ul>")

        for i in range(resultados.resultados_drones.obtener_tamaño()):
            resultado_dron = resultados.resultados_drones.obtener(i)
            estadisticas.insertar_al_final(
                f"<li>{resultado_dron.id} - {resultado_dron.agua_utilizada} litros</li>")

        estadisticas.insertar_al_final(
            f"<li><strong>TOTAL:</strong> {resultados.total_agua} litros</li>")
        estadisticas.insertar_al_final("</ul></li>")
        estadisticas.insertar_al_final(
            "<li><strong>Fertilizante requerido por dron:</strong><ul>")

        for i in range(resultados.resultados_drones.obtener_tamaño()):
            resultado_dron = resultados.resultados_drones.obtener(i)
            estadisticas.insertar_al_final(
                f"<li>{resultado_dron.id} - {resultado_dron.fertilizante_utilizado} gramos</li>")

        estadisticas.insertar_al_final(
            f"<li><strong>TOTAL:</strong> {resultados.total_fertilizante} gramos</li>")
        estadisticas.insertar_al_final("</ul></li>")
        estadisticas.insertar_al_final("</ul>")

        return self._convertir_lista_a_string(estadisticas)

    def _convertir_lista_a_string(self, lista):
        resultado = ""
        for elemento in lista:
            resultado += str(elemento) + "\n"
        return resultado

    def guardar_reporte(self, contenido_html, ruta_archivo):
        try:
            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_html)
            return Resultado(True, f"Reporte HTML guardado en: {ruta_archivo}")
        except Exception as e:
            return Resultado(False, f"Error guardando reporte HTML: {e}")
