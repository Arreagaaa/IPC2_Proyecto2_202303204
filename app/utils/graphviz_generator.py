import os
import subprocess
from app.tdas.lista_enlazada import ListaEnlazada


class GraphvizGenerator:
    def __init__(self):
        pass

    def generar_grafo_plan_riego(self, plan_riego, ruta_archivo):
        # Generar archivo DOT para visualizar el plan de riego
        from app.models.resultado import Resultado

        try:
            contenido = self.generar_grafico_plan_riego(plan_riego)
            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)
            return Resultado(True, f"Grafo DOT generado: {ruta_archivo}")
        except Exception as e:
            return Resultado(False, f"Error generando grafo DOT: {e}")

    def generar_grafo_cola_riego(self, cola_riego, ruta_archivo):
        # Generar archivo DOT para visualizar la cola de riego
        from app.models.resultado import Resultado

        try:
            contenido = self.generar_grafico_cola_riego(cola_riego)
            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)
            return Resultado(True, f"Grafo DOT generado: {ruta_archivo}")
        except Exception as e:
            return Resultado(False, f"Error generando grafo DOT: {e}")

    def generar_grafo_estado_drones(self, drones, ruta_archivo):
        # Generar archivo DOT para visualizar el estado de los drones
        from app.models.resultado import Resultado

        try:
            contenido = self.generar_grafico_drones(drones)
            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)
            return Resultado(True, f"Grafo DOT generado: {ruta_archivo}")
        except Exception as e:
            return Resultado(False, f"Error generando grafo DOT: {e}")

    def generar_visualizacion_tdas_tiempo_t(self, invernadero, tiempo_t, prefijo_archivo):
        # Generar visualizacion de TDAs en un tiempo especifico
        from app.models.resultado import Resultado

        try:
            # Generar gráfico específico para tiempo t
            contenido = self._generar_contenido_tiempo_t(invernadero, tiempo_t)
            ruta_archivo = f"{prefijo_archivo}.dot"

            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido)

            return Resultado(True, f"Visualización tiempo t={tiempo_t} generada: {ruta_archivo}")
        except Exception as e:
            return Resultado(False, f"Error generando visualización tiempo t: {e}")

    def _generar_contenido_tiempo_t(self, invernadero, tiempo_t):
        # Generar contenido DOT especifico para un tiempo t
        lineas = ListaEnlazada()
        lineas.insertar_al_final(f"digraph TiempoT{tiempo_t} {{")
        lineas.insertar_al_final("    rankdir=TB;")
        lineas.insertar_al_final(
            "    node [shape=rectangle, style=\"filled,rounded\", fontsize=11];")
        lineas.insertar_al_final("    edge [color=\"#2E86AB\", penwidth=2];")
        lineas.insertar_al_final("    bgcolor=\"#F8F9FA\";")
        lineas.insertar_al_final("    compound=true;")
        lineas.insertar_al_final("")

        # Titulo principal mas prominente
        lineas.insertar_al_final(
            f'    "Titulo" [label="ESTADO DEL SISTEMA\\nTiempo t={tiempo_t}\\n{invernadero.nombre}", shape=ellipse, fillcolor="#1E40AF", fontcolor=white, fontsize=16, width=4, height=2];')
        lineas.insertar_al_final("")

        # Subgrafico para informacion del plan mejorado
        lineas.insertar_al_final("    subgraph cluster_plan {")
        lineas.insertar_al_final("        label=\"PLAN DE RIEGO ACTIVO\";")
        lineas.insertar_al_final("        style=filled;")
        lineas.insertar_al_final("        fillcolor=\"#DCFCE7\";")
        lineas.insertar_al_final("        fontsize=14;")
        lineas.insertar_al_final("        penwidth=2;")
        lineas.insertar_al_final("        color=\"#16A34A\";")

        plan_secuencia = invernadero.plan_riego.obtener_plan_original()
        plan_truncado = plan_secuencia[:40] + \
            "..." if len(plan_secuencia) > 40 else plan_secuencia

        lineas.insertar_al_final(
            f'        "Plan" [label="SECUENCIA ACTUAL:\\n{plan_truncado}\\n\\nTIEMPO: {tiempo_t}s\\nESTADO: EJECUTANDO", fillcolor="#22C55E", fontcolor=white, fontsize=12, shape=box];')
        lineas.insertar_al_final("    }")
        lineas.insertar_al_final(
            '    "Titulo" -> "Plan" [lhead=cluster_plan];')
        lineas.insertar_al_final("")

        # Subgrafico para drones mejorado
        lineas.insertar_al_final("    subgraph cluster_drones {")
        lineas.insertar_al_final("        label=\"ESTADO DE DRONES\";")
        lineas.insertar_al_final("        style=filled;")
        lineas.insertar_al_final("        fillcolor=\"#EFF6FF\";")
        lineas.insertar_al_final("        fontsize=14;")
        lineas.insertar_al_final("        penwidth=2;")
        lineas.insertar_al_final("        color=\"#2563EB\";")

        contador_dron = 0
        for i in range(invernadero.drones.obtener_tamaño()):
            dron = invernadero.drones.obtener(i)
            hilera_info = f"Hilera {dron.hilera_asignada.numero}" if dron.hilera_asignada else "Sin asignar"
            posicion_info = f"Posicion: {dron.posicion_actual}" if hasattr(
                dron, 'posicion_actual') else "Posicion: Inicial"

            # Determinar estado basado en tiempo
            if tiempo_t <= 5:
                estado = "Iniciando"
                color = "#FFB4B4"
            elif tiempo_t <= 15:
                estado = "Trabajando"
                color = "#90EE90"
            else:
                estado = "Finalizando"
                color = "#87CEEB"

            estado_dron = f"DRON {dron.id}\\n{estado}\\n{posicion_info}\\n{hilera_info}\\nCapacidad: {dron.capacidad_agua}L"
            lineas.insertar_al_final(
                f'        "Dron{contador_dron}" [label="{estado_dron}", fillcolor="{color}", shape=box, fontsize=10, penwidth=2];')
            contador_dron += 1

        lineas.insertar_al_final("    }")
        if contador_dron > 0:
            lineas.insertar_al_final(
                '    "Plan" -> "Dron0" [lhead=cluster_drones, label="controla"];')

        # Informacion adicional de estado mejorada
        tiempo_info = f"INFORMACION DEL SISTEMA\\nTiempo transcurrido: {tiempo_t}s\\nDrones operando: {contador_dron}\\nHileras totales: {invernadero.hileras.obtener_tamaño()}\\nEstado: ACTIVO"
        lineas.insertar_al_final(
            f'    "TiempoInfo" [label="{tiempo_info}", shape=box, fillcolor="#FEF3C7", color="#D97706", penwidth=2, fontsize=11];')
        lineas.insertar_al_final(
            '    "Titulo" -> "TiempoInfo" [style=dashed, color="#D97706"];')

        lineas.insertar_al_final("}")
        return self._convertir_lista_a_string(lineas)

    def convertir_dot_a_png(self, ruta_dot, ruta_png):
        # Convertir archivo DOT a PNG usando Graphviz
        from app.models.resultado import Resultado

        try:
            # Crear directorio de destino si no existe
            directorio = os.path.dirname(ruta_png)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            # Intentar conversión con Graphviz
            resultado = subprocess.run([
                'dot', '-Tpng', ruta_dot, '-o', ruta_png
            ], capture_output=True, text=True, timeout=30)

            if resultado.returncode == 0:
                return Resultado(True, f"PNG generado: {ruta_png}")
            else:
                # Si Graphviz falla, crear PNG simulado
                return self._crear_png_simulado(ruta_png)

        except FileNotFoundError:
            # Graphviz no instalado, crear PNG simulado
            return self._crear_png_simulado(ruta_png)
        except Exception as e:
            return Resultado(False, f"Error convirtiendo DOT a PNG: {e}")

    def _crear_png_simulado(self, ruta_png):
        # Crear una imagen PNG simulada cuando Graphviz no esta disponible
        from app.models.resultado import Resultado

        try:
            # Crear un archivo de texto que simule la imagen
            contenido_simulado = f"""
TDA Visualization (Simulated)
=============================
File: {os.path.basename(ruta_png)}
Generated: {os.path.basename(ruta_png).replace('.png', '')}

Note: This is a text representation.
Install Graphviz for actual PNG generation.
"""
            ruta_txt = ruta_png.replace('.png', '_simulated.txt')
            with open(ruta_txt, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_simulado)

            return Resultado(True, f"Archivo simulado generado: {ruta_txt}")
        except Exception as e:
            return Resultado(False, f"Error creando archivo simulado: {e}")

    def generar_pagina_visualizacion_html(self, ruta_imagen, ruta_html, titulo):
        # Generar pagina HTML para visualizar un grafico especifico
        from app.models.resultado import Resultado

        try:
            html_content = ListaEnlazada()

            html_content.insertar_al_final("<!DOCTYPE html>")
            html_content.insertar_al_final("<html lang='es'>")
            html_content.insertar_al_final("<head>")
            html_content.insertar_al_final("    <meta charset='UTF-8'>")
            html_content.insertar_al_final(
                "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
            html_content.insertar_al_final(
                f"    <title>{titulo} - GuateRiegos 2.0</title>")
            html_content.insertar_al_final("    <style>")
            html_content.insertar_al_final(
                "        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }")
            html_content.insertar_al_final(
                "        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }")
            html_content.insertar_al_final(
                "        .header { text-align: center; color: #2c3e50; margin-bottom: 20px; }")
            html_content.insertar_al_final(
                "        .imagen { text-align: center; }")
            html_content.insertar_al_final(
                "        .imagen img { max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; }")
            html_content.insertar_al_final(
                "        .back-link { display: block; text-align: center; margin-top: 20px; color: #3498db; text-decoration: none; }")
            html_content.insertar_al_final("    </style>")
            html_content.insertar_al_final("</head>")
            html_content.insertar_al_final("<body>")
            html_content.insertar_al_final("    <div class='container'>")
            html_content.insertar_al_final("        <div class='header'>")
            html_content.insertar_al_final(f"            <h1>{titulo}</h1>")
            html_content.insertar_al_final(
                "            <h3>GuateRiegos 2.0 - Sistema de Riego Robótico</h3>")
            html_content.insertar_al_final("        </div>")
            html_content.insertar_al_final("        <div class='imagen'>")

            # Verificar si la imagen existe
            if os.path.exists(ruta_imagen):
                nombre_imagen = os.path.basename(ruta_imagen)
                html_content.insertar_al_final(
                    f"            <img src='{nombre_imagen}' alt='{titulo}'>")
            else:
                html_content.insertar_al_final(
                    "            <p>Imagen no disponible. Instalar Graphviz para generar visualizaciones PNG.</p>")
                ruta_txt = ruta_imagen.replace('.png', '_simulated.txt')
                if os.path.exists(ruta_txt):
                    html_content.insertar_al_final(
                        f"            <p><a href='{os.path.basename(ruta_txt)}'>Ver representación de texto</a></p>")

            html_content.insertar_al_final("        </div>")
            html_content.insertar_al_final(
                "        <a href='#' class='back-link' onclick='history.back()'>← Volver</a>")
            html_content.insertar_al_final("    </div>")
            html_content.insertar_al_final("</body>")
            html_content.insertar_al_final("</html>")

            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_html)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta_html, 'w', encoding='utf-8') as archivo:
                for linea in html_content:
                    archivo.write(str(linea) + "\n")

            return Resultado(True, f"Página HTML generada: {ruta_html}")
        except Exception as e:
            return Resultado(False, f"Error generando página HTML: {e}")

    def generar_grafico_plan_riego(self, plan_riego, tiempo_t=None):
        lineas = ListaEnlazada()
        lineas.insertar_al_final("digraph PlanRiego {")
        lineas.insertar_al_final("    rankdir=TB;")
        lineas.insertar_al_final(
            "    node [shape=box, style=\"filled,rounded\", fontsize=12, width=2.5, height=1];")
        lineas.insertar_al_final(
            "    edge [color=\"#2563EB\", penwidth=3, arrowsize=1.5];")
        lineas.insertar_al_final("    bgcolor=\"#F8FAFC\";")
        lineas.insertar_al_final("    size=\"16,12\";")
        lineas.insertar_al_final("    compound=true;")
        lineas.insertar_al_final("")

        # Título principal
        titulo = f"PLAN DE RIEGO\\nTiempo t={tiempo_t}" if tiempo_t else "PLAN DE RIEGO"
        lineas.insertar_al_final(
            f'    "Titulo" [label="{titulo}", shape=ellipse, fillcolor="#1E40AF", fontcolor=white, fontsize=18, width=4, height=2];')
        lineas.insertar_al_final("")

        # Generar nodos del plan original
        plan_original = plan_riego.obtener_plan_original()
        if plan_original:
            # Convertir plan_original a string si es necesario
            plan_str = ""
            for elemento in plan_original:
                if plan_str:
                    plan_str += ", "
                plan_str += str(elemento)

            # Dividir el plan en pasos individuales
            pasos = ListaEnlazada()
            paso_actual = ""
            for caracter in plan_str:
                if caracter == ',':
                    if paso_actual.strip():
                        pasos.insertar_al_final(paso_actual.strip())
                    paso_actual = ""
                else:
                    paso_actual += caracter
            if paso_actual.strip():
                pasos.insertar_al_final(paso_actual.strip())

            # Información del plan
            total_pasos = len([p for p in pasos])
            info_plan = f"Total de Pasos: {total_pasos}"
            if tiempo_t:
                progreso = min(tiempo_t // 2, total_pasos)
                info_plan += f"\\nProgreso: {progreso}/{total_pasos}\\nTiempo: {tiempo_t}s"

            lineas.insertar_al_final(
                f'    "InfoPlan" [label="{info_plan}", shape=note, fillcolor="#DBEAFE", fontsize=11];')
            lineas.insertar_al_final('    "Titulo" -> "InfoPlan";')
            lineas.insertar_al_final("")

            # Generar nodos con mejor formato
            contador = 0
            for paso in pasos:
                # Formatear paso (Hilera-Planta) con mejor visualización
                partes = paso.split('-')
                if len(partes) == 2:
                    paso_formateado = f"H{partes[0]}\\nP{partes[1]}"
                else:
                    paso_formateado = paso.replace('-', '\\n')

                # Determinar color y estado basado en progreso
                if tiempo_t:
                    if contador < tiempo_t // 2:
                        color = "#22C55E"  # Verde - completado
                        estado = "HECHO"
                        border_color = "#16A34A"
                    elif contador == tiempo_t // 2:
                        color = "#EAB308"  # Amarillo - actual
                        estado = "ACTUAL"
                        border_color = "#CA8A04"
                    else:
                        color = "#E5E7EB"  # Gris - pendiente
                        estado = "PENDIENTE"
                        border_color = "#9CA3AF"
                else:
                    color = "#3B82F6"  # Azul por defecto
                    estado = f"PASO {contador + 1}"
                    border_color = "#2563EB"

                label = f"{estado}\\n{paso_formateado}"
                lineas.insertar_al_final(
                    f'    "Paso{contador}" [label="{label}", fillcolor="{color}", color="{border_color}", penwidth=2, fontsize=10];')
                contador += 1

            # Generar conexiones
            lineas.insertar_al_final(
                '    "InfoPlan" -> "Paso0" [label="inicia"];')
            for i in range(contador - 1):
                lineas.insertar_al_final(
                    f'    "Paso{i}" -> "Paso{i+1}" [color="#059669"];')

        else:
            lineas.insertar_al_final(
                '    "Sin_Plan" [label="NO HAY PLAN DE RIEGO\\nDISPONIBLE", fillcolor="#FEE2E2", color="#DC2626", penwidth=2, fontsize=14];')
            lineas.insertar_al_final('    "Titulo" -> "Sin_Plan";')

        lineas.insertar_al_final("}")
        return self._convertir_lista_a_string(lineas)

    def generar_grafico_cola_riego(self, cola_riego, tiempo_t=None):
        lineas = ListaEnlazada()
        lineas.insertar_al_final("digraph ColaRiego {")
        lineas.insertar_al_final("    rankdir=LR;")
        lineas.insertar_al_final(
            "    node [shape=rectangle, style=\"filled,rounded\", fontsize=12];")
        lineas.insertar_al_final("    edge [color=\"#2E86AB\", penwidth=2];")
        lineas.insertar_al_final("    bgcolor=\"#F8F9FA\";")
        lineas.insertar_al_final("")

        # Título
        titulo = f"Cola de Riego - Tiempo t={tiempo_t}" if tiempo_t else "Cola de Riego"
        lineas.insertar_al_final(
            f'    "Titulo" [label="{titulo}", shape=ellipse, fillcolor="#A23B72", fontcolor=white, fontsize=14];')
        lineas.insertar_al_final("")

        if cola_riego.esta_vacia():
            lineas.insertar_al_final(
                '    "Cola_Vacia" [label="Cola Vacia\\n(Sin instrucciones pendientes)", fillcolor="#FFB4B4", fontcolor="#8B0000"];')
            lineas.insertar_al_final('    "Titulo" -> "Cola_Vacia";')
        else:
            # Usar método seguro para iterar sin modificar la cola
            elementos_temporales = ListaEnlazada()
            contador = 0
            cola_temp = cola_riego.crear_copia()  # Crear copia segura

            # Visualizar elementos de la copia
            while not cola_temp.esta_vacia():
                elemento = cola_temp.desencolar()
                elementos_temporales.insertar_al_final(elemento)

                # Mejorar formato de visualización
                elemento_formateado = elemento.replace('-', ' - ')
                # Verde para próximo, amarillo para resto
                color = "#90EE90" if contador == 0 else "#FFE4B5"

                lineas.insertar_al_final(
                    f'    "Elem{contador}" [label="{contador+1}. {elemento_formateado}", fillcolor="{color}"];')

                if contador == 0:
                    lineas.insertar_al_final(
                        '    "Titulo" -> "Elem0" [label="Proximo", color="#FF6B6B"];')

                contador += 1

            # Generar conexiones entre elementos
            for i in range(contador - 1):
                lineas.insertar_al_final(
                    f'    "Elem{i}" -> "Elem{i+1}" [label="siguiente"];')

            # Indicador de orden FIFO
            if contador > 0:
                lineas.insertar_al_final(
                    f'    "Info" [label="FIFO: First In, First Out\\nTotal: {contador} instrucciones", shape=note, fillcolor="#E6E6FA"];')

        lineas.insertar_al_final("}")
        return self._convertir_lista_a_string(lineas)

    def generar_grafico_drones(self, drones, tiempo_t=None):
        lineas = ListaEnlazada()
        lineas.insertar_al_final("digraph Drones {")
        lineas.insertar_al_final("    rankdir=TB;")
        lineas.insertar_al_final(
            "    node [shape=ellipse, style=filled, fillcolor=lightcoral];")
        lineas.insertar_al_final("    edge [color=darkgreen];")
        lineas.insertar_al_final("")

        lineas.insertar_al_final(
            '    "Sistema_Drones" [label="Sistema de Drones", shape=box, fillcolor=yellow];')

        contador = 0
        for dron in drones:
            estado = "Activo" if tiempo_t and contador < tiempo_t else "Inactivo"
            etiqueta = f"Dron {dron.id}\\nHilera: {getattr(dron, 'hilera_asignada', 'N/A')}\\nEstado: {estado}"
            color = "lightgreen" if estado == "Activo" else "lightcoral"
            lineas.insertar_al_final(
                f'    "Dron{contador}" [label="{etiqueta}", fillcolor={color}];')
            lineas.insertar_al_final(
                f'    "Sistema_Drones" -> "Dron{contador}";')
            contador += 1

        lineas.insertar_al_final("}")
        return self._convertir_lista_a_string(lineas)

    def generar_grafos_tdas(self, plan_riego, cola_riego, drones, prefijo_archivo="grafo", tiempo_t=None):
        resultados = ListaEnlazada()

        # Generar grafico del plan de riego
        contenido_plan = self.generar_grafico_plan_riego(plan_riego, tiempo_t)
        ruta_plan = f"{prefijo_archivo}_plan_riego.dot"
        if self.generar_archivo_dot(contenido_plan, ruta_plan):
            ruta_png_plan = f"{prefijo_archivo}_plan_riego.png"
            if self.convertir_dot_a_png(ruta_plan, ruta_png_plan):
                resultados.insertar_al_final(f"Plan de riego: {ruta_png_plan}")

        # Generar grafico de la cola
        contenido_cola = self.generar_grafico_cola_riego(cola_riego, tiempo_t)
        ruta_cola = f"{prefijo_archivo}_cola_riego.dot"
        if self.generar_archivo_dot(contenido_cola, ruta_cola):
            ruta_png_cola = f"{prefijo_archivo}_cola_riego.png"
            if self.convertir_dot_a_png(ruta_cola, ruta_png_cola):
                resultados.insertar_al_final(f"Cola de riego: {ruta_png_cola}")

        # Generar grafico de drones
        contenido_drones = self.generar_grafico_drones(drones, tiempo_t)
        ruta_drones = f"{prefijo_archivo}_drones.dot"
        if self.generar_archivo_dot(contenido_drones, ruta_drones):
            ruta_png_drones = f"{prefijo_archivo}_drones.png"
            if self.convertir_dot_a_png(ruta_drones, ruta_png_drones):
                resultados.insertar_al_final(f"Drones: {ruta_png_drones}")

        return resultados

    def _convertir_lista_a_string(self, lista):
        resultado = ""
        for elemento in lista:
            resultado += str(elemento) + "\n"
        return resultado

    def generar_archivo_dot(self, contenido_dot, ruta_archivo):
        # Generar archivo DOT con contenido especificado
        from app.models.resultado import Resultado

        try:
            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_dot)
            return Resultado(True, f"Archivo DOT generado: {ruta_archivo}")
        except Exception as e:
            return Resultado(False, f"Error generando archivo DOT: {e}")

    def generar_html_visualizacion(self, rutas_imagenes, ruta_html):
        # Generar pagina HTML para visualizar los graficos PNG
        html_content = ListaEnlazada()

        html_content.insertar_al_final("<!DOCTYPE html>")
        html_content.insertar_al_final("<html lang='es'>")
        html_content.insertar_al_final("<head>")
        html_content.insertar_al_final("    <meta charset='UTF-8'>")
        html_content.insertar_al_final(
            "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html_content.insertar_al_final(
            "    <title>Visualización de TDAs - GuateRiegos 2.0</title>")
        html_content.insertar_al_final("    <style>")
        html_content.insertar_al_final(
            "        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }")
        html_content.insertar_al_final(
            "        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }")
        html_content.insertar_al_final(
            "        .header { background: #2c3e50; color: white; padding: 20px; margin: -20px -20px 20px -20px; text-align: center; }")
        html_content.insertar_al_final(
            "        .grafico { margin: 20px 0; text-align: center; }")
        html_content.insertar_al_final(
            "        .grafico h3 { color: #2c3e50; margin-bottom: 10px; }")
        html_content.insertar_al_final(
            "        .grafico img { max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; }")
        html_content.insertar_al_final("    </style>")
        html_content.insertar_al_final("</head>")
        html_content.insertar_al_final("<body>")
        html_content.insertar_al_final("    <div class='container'>")
        html_content.insertar_al_final("        <div class='header'>")
        html_content.insertar_al_final(
            "            <h1>Visualización de TDAs</h1>")
        html_content.insertar_al_final(
            "            <h2>GuateRiegos 2.0 - Sistema de Riego Robotico</h2>")
        html_content.insertar_al_final("        </div>")

        for ruta_imagen in rutas_imagenes:
            nombre_archivo = os.path.basename(ruta_imagen)
            nombre_grafico = nombre_archivo.replace(
                '.png', '').replace('_', ' ').title()

            html_content.insertar_al_final("        <div class='grafico'>")
            html_content.insertar_al_final(
                f"            <h3>{nombre_grafico}</h3>")
            html_content.insertar_al_final(
                f"            <img src='{ruta_imagen}' alt='{nombre_grafico}'>")
            html_content.insertar_al_final("        </div>")

        html_content.insertar_al_final("    </div>")
        html_content.insertar_al_final("</body>")
        html_content.insertar_al_final("</html>")

        try:
            with open(ruta_html, 'w', encoding='utf-8') as archivo:
                for linea in html_content:
                    archivo.write(str(linea) + "\n")
            return True
        except Exception as e:
            print(f"Error generando HTML de visualización: {e}")
            return False
