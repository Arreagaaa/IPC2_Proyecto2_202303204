import os
import subprocess
from app.tdas.lista_enlazada import ListaEnlazada

class GraphvizGenerator:
    def __init__(self):
        pass
    
    def generar_grafico_plan_riego(self, plan_riego, tiempo_t=None):
        lineas = ListaEnlazada()
        lineas.insertar_al_final("digraph PlanRiego {")
        lineas.insertar_al_final("    rankdir=LR;")
        lineas.insertar_al_final("    node [shape=box, style=filled, fillcolor=lightblue];")
        lineas.insertar_al_final("    edge [color=blue];")
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
            
            # Generar nodos
            contador = 0
            for paso in pasos:
                color = "lightgreen" if tiempo_t and contador < tiempo_t else "lightblue"
                lineas.insertar_al_final(f'    "Paso{contador}" [label="{paso}", fillcolor={color}];')
                contador += 1
            
            # Generar conexiones
            for i in range(contador - 1):
                lineas.insertar_al_final(f'    "Paso{i}" -> "Paso{i+1}";')
        
        lineas.insertar_al_final("}")
        return self._convertir_lista_a_string(lineas)
    
    def generar_grafico_cola_riego(self, cola_riego, tiempo_t=None):
        lineas = ListaEnlazada()
        lineas.insertar_al_final("digraph ColaRiego {")
        lineas.insertar_al_final("    rankdir=LR;")
        lineas.insertar_al_final("    node [shape=box, style=filled, fillcolor=lightyellow];")
        lineas.insertar_al_final("    edge [color=red];")
        lineas.insertar_al_final("")
        
        if cola_riego.esta_vacia():
            lineas.insertar_al_final('    "Cola_Vacia" [label="Cola Vacia", fillcolor=gray];')
        else:
            # Crear una copia temporal para no modificar la cola original
            elementos_temporales = ListaEnlazada()
            contador = 0
            
            # Extraer elementos temporalmente
            while not cola_riego.esta_vacia():
                elemento = cola_riego.desencolar()
                elementos_temporales.insertar_al_final(elemento)
                lineas.insertar_al_final(f'    "Elem{contador}" [label="{elemento}"];')
                contador += 1
            
            # Reconectar elementos en la cola
            for elemento in elementos_temporales:
                cola_riego.encolar(elemento)
            
            # Generar conexiones
            for i in range(contador - 1):
                lineas.insertar_al_final(f'    "Elem{i}" -> "Elem{i+1}";')
        
        lineas.insertar_al_final("}")
        return self._convertir_lista_a_string(lineas)
    
    def generar_grafico_drones(self, drones, tiempo_t=None):
        lineas = ListaEnlazada()
        lineas.insertar_al_final("digraph Drones {")
        lineas.insertar_al_final("    rankdir=TB;")
        lineas.insertar_al_final("    node [shape=ellipse, style=filled, fillcolor=lightcoral];")
        lineas.insertar_al_final("    edge [color=darkgreen];")
        lineas.insertar_al_final("")
        
        lineas.insertar_al_final('    "Sistema_Drones" [label="Sistema de Drones", shape=box, fillcolor=yellow];')
        
        contador = 0
        for dron in drones:
            estado = "Activo" if tiempo_t and contador < tiempo_t else "Inactivo"
            etiqueta = f"Dron {dron.id}\\nHilera: {getattr(dron, 'hilera_asignada', 'N/A')}\\nEstado: {estado}"
            color = "lightgreen" if estado == "Activo" else "lightcoral"
            lineas.insertar_al_final(f'    "Dron{contador}" [label="{etiqueta}", fillcolor={color}];')
            lineas.insertar_al_final(f'    "Sistema_Drones" -> "Dron{contador}";')
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
        try:
            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_dot)
            return True
        except Exception as e:
            print(f"Error generando archivo DOT: {e}")
            return False
    
    def convertir_dot_a_png(self, ruta_dot, ruta_png):
        try:
            # Intentar usar Graphviz para convertir DOT a PNG
            resultado = subprocess.run([
                'dot', '-Tpng', ruta_dot, '-o', ruta_png
            ], capture_output=True, text=True)
            
            if resultado.returncode == 0:
                return True
            else:
                print(f"Error convirtiendo DOT a PNG: {resultado.stderr}")
                return False
        except FileNotFoundError:
            print("Graphviz no está instalado o no está en el PATH")
            return False
        except Exception as e:
            print(f"Error convirtiendo DOT a PNG: {e}")
            return False
    
    def generar_html_visualizacion(self, rutas_imagenes, ruta_html):
        """Generar página HTML para visualizar los gráficos PNG"""
        html_content = ListaEnlazada()
        
        html_content.insertar_al_final("<!DOCTYPE html>")
        html_content.insertar_al_final("<html lang='es'>")
        html_content.insertar_al_final("<head>")
        html_content.insertar_al_final("    <meta charset='UTF-8'>")
        html_content.insertar_al_final("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html_content.insertar_al_final("    <title>Visualización de TDAs - GuateRiegos 2.0</title>")
        html_content.insertar_al_final("    <style>")
        html_content.insertar_al_final("        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }")
        html_content.insertar_al_final("        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }")
        html_content.insertar_al_final("        .header { background: #2c3e50; color: white; padding: 20px; margin: -20px -20px 20px -20px; text-align: center; }")
        html_content.insertar_al_final("        .grafico { margin: 20px 0; text-align: center; }")
        html_content.insertar_al_final("        .grafico h3 { color: #2c3e50; margin-bottom: 10px; }")
        html_content.insertar_al_final("        .grafico img { max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; }")
        html_content.insertar_al_final("    </style>")
        html_content.insertar_al_final("</head>")
        html_content.insertar_al_final("<body>")
        html_content.insertar_al_final("    <div class='container'>")
        html_content.insertar_al_final("        <div class='header'>")
        html_content.insertar_al_final("            <h1>Visualización de TDAs</h1>")
        html_content.insertar_al_final("            <h2>GuateRiegos 2.0 - Sistema de Riego Robotico</h2>")
        html_content.insertar_al_final("        </div>")
        
        for ruta_imagen in rutas_imagenes:
            nombre_archivo = os.path.basename(ruta_imagen)
            nombre_grafico = nombre_archivo.replace('.png', '').replace('_', ' ').title()
            
            html_content.insertar_al_final("        <div class='grafico'>")
            html_content.insertar_al_final(f"            <h3>{nombre_grafico}</h3>")
            html_content.insertar_al_final(f"            <img src='{ruta_imagen}' alt='{nombre_grafico}'>")
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
