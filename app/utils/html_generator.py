from app.tdas.lista_enlazada import ListaEnlazada
from app.models.resultado import Resultado


# generador de reportes HTML
class HTMLGenerator:
    def __init__(self):
        pass

    def generar_reporte_invernadero(self, invernadero, resultados_simulacion, registro_instrucciones):
        # Generar HTML completo para un invernadero
        html_content = ListaEnlazada()

        # Encabezado HTML
        html_content.insertar_al_final("<!DOCTYPE html>")
        html_content.insertar_al_final("<html lang='es'>")
        html_content.insertar_al_final("<head>")
        html_content.insertar_al_final("    <meta charset='UTF-8'>")
        html_content.insertar_al_final(
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html_content.insertar_al_final(
            f"    <title>Reporte - {invernadero.nombre}</title>")
        html_content.insertar_al_final("    <style>")
        html_content.insertar_al_final(self._generar_css())
        html_content.insertar_al_final("    </style>")
        html_content.insertar_al_final("</head>")
        html_content.insertar_al_final("<body>")

        # Título principal
        html_content.insertar_al_final("    <div class='container'>")
        html_content.insertar_al_final(
            f"        <h1>Reporte de Simulación - {invernadero.nombre}</h1>")

        # Información general
        html_content.insertar_al_final("        <div class='section'>")
        html_content.insertar_al_final(
            "            <h2>Información General</h2>")
        html_content.insertar_al_final("            <div class='info-grid'>")
        html_content.insertar_al_final(
            f"                <div class='info-item'><strong>Invernadero:</strong> {invernadero.nombre}</div>")
        html_content.insertar_al_final(
            f"                <div class='info-item'><strong>Plan ejecutado:</strong> {resultados_simulacion.plan_ejecutado}</div>")
        html_content.insertar_al_final(
            f"                <div class='info-item'><strong>Tiempo total:</strong> {resultados_simulacion.tiempo_total} segundos</div>")
        html_content.insertar_al_final(
            f"                <div class='info-item'><strong>Agua total:</strong> {resultados_simulacion.total_agua} litros</div>")
        html_content.insertar_al_final(
            f"                <div class='info-item'><strong>Fertilizante total:</strong> {resultados_simulacion.total_fertilizante} gramos</div>")
        html_content.insertar_al_final("            </div>")
        html_content.insertar_al_final("        </div>")

        # Tabla 1: Asignación de drones a hileras
        html_content.insertar_al_final("        <div class='section'>")
        html_content.insertar_al_final(
            "            <h2>Tabla 1 - Asignación de drones a hileras</h2>")
        html_content.insertar_al_final(
            "            <table class='assignment-table'>")
        html_content.insertar_al_final("                <thead>")
        html_content.insertar_al_final("                    <tr>")
        html_content.insertar_al_final(
            "                        <th>Hilera</th>")
        html_content.insertar_al_final("                        <th>Dron</th>")
        html_content.insertar_al_final("                    </tr>")
        html_content.insertar_al_final("                </thead>")
        html_content.insertar_al_final("                <tbody>")

        # Agregar filas de asignación
        for i in range(invernadero.drones.obtener_tamaño()):
            dron = invernadero.drones.obtener(i)
            html_content.insertar_al_final("                    <tr>")
            html_content.insertar_al_final(
                f"                        <td>H{dron.hilera_asignada.numero}</td>")
            html_content.insertar_al_final(
                f"                        <td>{dron.id}</td>")
            html_content.insertar_al_final("                    </tr>")

        html_content.insertar_al_final("                </tbody>")
        html_content.insertar_al_final("            </table>")
        html_content.insertar_al_final("        </div>")

        # Tabla 2: Instrucciones por tiempo
        html_content.insertar_al_final("        <div class='section'>")
        html_content.insertar_al_final(
            "            <h2>Tabla 2 - Instrucciones enviadas a cada dron por unidad de tiempo</h2>")
        html_content.insertar_al_final(
            "            <table class='instructions-table'>")
        html_content.insertar_al_final("                <thead>")
        html_content.insertar_al_final("                    <tr>")
        html_content.insertar_al_final(
            "                        <th>Tiempo</th>")

        # Encabezados de drones
        for i in range(invernadero.drones.obtener_tamaño()):
            dron = invernadero.drones.obtener(i)
            html_content.insertar_al_final(
                f"                        <th>{dron.id}</th>")

        html_content.insertar_al_final("                    </tr>")
        html_content.insertar_al_final("                </thead>")
        html_content.insertar_al_final("                <tbody>")

        # Agregar filas de instrucciones
        for i in range(registro_instrucciones.obtener_tamaño()):
            registro = registro_instrucciones.obtener(i)
            html_content.insertar_al_final("                    <tr>")
            html_content.insertar_al_final(
                f"                        <td>{registro.tiempo} segundo{'s' if registro.tiempo > 1 else ''}</td>")

            # Obtener instrucciones para cada dron en este tiempo
            for j in range(invernadero.drones.obtener_tamaño()):
                dron = invernadero.drones.obtener(j)
                instruccion = registro.instrucciones.obtener_instruccion(
                    dron.id)
                if instruccion:
                    # Colorear según el tipo de acción
                    clase_css = self._obtener_clase_accion(instruccion)
                    html_content.insertar_al_final(
                        f"                        <td class='{clase_css}'>{instruccion}</td>")
                else:
                    html_content.insertar_al_final(
                        "                        <td class='esperar'>-</td>")

            html_content.insertar_al_final("                    </tr>")

        html_content.insertar_al_final("                </tbody>")
        html_content.insertar_al_final("            </table>")
        html_content.insertar_al_final("        </div>")

        # Tabla 3: Estadísticas por dron
        html_content.insertar_al_final("        <div class='section'>")
        html_content.insertar_al_final(
            "            <h2>Estadísticas de uso de agua y fertilizante</h2>")
        html_content.insertar_al_final(
            "            <table class='stats-table'>")
        html_content.insertar_al_final("                <thead>")
        html_content.insertar_al_final("                    <tr>")
        html_content.insertar_al_final("                        <th>Dron</th>")
        html_content.insertar_al_final(
            "                        <th>Agua (litros)</th>")
        html_content.insertar_al_final(
            "                        <th>Fertilizante (gramos)</th>")
        html_content.insertar_al_final("                    </tr>")
        html_content.insertar_al_final("                </thead>")
        html_content.insertar_al_final("                <tbody>")

        # Agregar estadísticas por dron
        for i in range(resultados_simulacion.resultados_drones.obtener_tamaño()):
            resultado_dron = resultados_simulacion.resultados_drones.obtener(i)
            html_content.insertar_al_final("                    <tr>")
            html_content.insertar_al_final(
                f"                        <td><strong>{resultado_dron.id}</strong></td>")
            html_content.insertar_al_final(
                f"                        <td>{resultado_dron.agua_utilizada}</td>")
            html_content.insertar_al_final(
                f"                        <td>{resultado_dron.fertilizante_utilizado}</td>")
            html_content.insertar_al_final("                    </tr>")

        # Fila de totales
        html_content.insertar_al_final(
            "                    <tr class='total-row'>")
        html_content.insertar_al_final(
            "                        <td><strong>TOTAL</strong></td>")
        html_content.insertar_al_final(
            f"                        <td><strong>{resultados_simulacion.total_agua}</strong></td>")
        html_content.insertar_al_final(
            f"                        <td><strong>{resultados_simulacion.total_fertilizante}</strong></td>")
        html_content.insertar_al_final("                    </tr>")

        html_content.insertar_al_final("                </tbody>")
        html_content.insertar_al_final("            </table>")
        html_content.insertar_al_final("        </div>")

        # Cierre del HTML
        html_content.insertar_al_final("    </div>")
        html_content.insertar_al_final("</body>")
        html_content.insertar_al_final("</html>")

        return self._convertir_lista_a_string(html_content)

    def _obtener_clase_accion(self, instruccion):
        # Determinar clase CSS según el tipo de acción
        if "Regar" in instruccion:
            return "regar"
        elif "Adelante" in instruccion:
            return "adelante"
        elif "Atrás" in instruccion or "Regresar" in instruccion:
            return "atras"
        elif "FIN" in instruccion:
            return "fin"
        else:
            return "esperar"

    def _generar_css(self):
        # CSS para el reporte HTML
        css = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        }
        
        h2 {
            color: #34495e;
            margin-bottom: 15px;
            padding-left: 10px;
            border-left: 4px solid #3498db;
        }
        
        .section {
            margin-bottom: 40px;
            padding: 20px;
            background-color: #fafafa;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .info-item {
            padding: 10px;
            background-color: white;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        th {
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: center;
            font-weight: bold;
        }
        
        td {
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }
        
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        tr:hover {
            background-color: #e8f6f3;
        }
        
        .total-row {
            background-color: #2c3e50 !important;
            color: white;
            font-weight: bold;
        }
        
        .total-row:hover {
            background-color: #34495e !important;
        }
        
        /* Colores para diferentes tipos de acciones */
        .regar {
            background-color: #e8f5e8 !important;
            color: #2e7d32;
            font-weight: bold;
        }
        
        .adelante {
            background-color: #e3f2fd !important;
            color: #1565c0;
        }
        
        .atras {
            background-color: #fff3e0 !important;
            color: #ef6c00;
        }
        
        .fin {
            background-color: #f3e5f5 !important;
            color: #7b1fa2;
            font-weight: bold;
        }
        
        .esperar {
            background-color: #fafafa !important;
            color: #757575;
            font-style: italic;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            table {
                font-size: 14px;
            }
            
            th, td {
                padding: 8px;
            }
        }
        """
        return css

    def _convertir_lista_a_string(self, lista_enlazada):
        # Convertir ListaEnlazada a string
        resultado = ""
        for i in range(lista_enlazada.obtener_tamaño()):
            if i > 0:
                resultado += "\n"
            resultado += lista_enlazada.obtener(i)
        return resultado

    def guardar_reporte(self, contenido_html, nombre_archivo):
        # Guardar el contenido HTML en un archivo
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_html)
            return Resultado(True, f"Reporte guardado en: {nombre_archivo}")
        except Exception as e:
            return Resultado(False, f"Error al guardar reporte: {str(e)}")
