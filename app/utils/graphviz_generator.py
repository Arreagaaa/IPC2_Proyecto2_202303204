from app.tdas.lista_enlazada import ListaEnlazada
from app.models.resultado import Resultado


# generador de graficos con Graphviz
class GraphvizGenerator:
    def __init__(self):
        pass

    def generar_grafo_plan_riego(self, plan_riego, nombre_archivo="grafo_plan_riego.dot"):
        # Generar código Graphviz para visualizar el plan de riego
        dot_content = ListaEnlazada()

        # Encabezado del grafo
        dot_content.insertar_al_final("digraph PlanRiego {")
        dot_content.insertar_al_final("    rankdir=LR;")
        dot_content.insertar_al_final(
            "    node [shape=box, style=filled, fillcolor=lightblue];")
        dot_content.insertar_al_final("    edge [color=darkblue, penwidth=2];")
        dot_content.insertar_al_final("")
        dot_content.insertar_al_final("    # Nodos del plan de riego")

        # Agregar nodos para cada paso del plan
        plan_original = plan_riego.obtener_plan_original()
        if plan_original:
            # Separar los pasos manualmente
            pasos = ListaEnlazada()
            paso_actual = ""

            for caracter in plan_original:
                if caracter == ',':
                    if paso_actual.strip():
                        pasos.insertar_al_final(paso_actual.strip())
                    paso_actual = ""
                else:
                    paso_actual += caracter

            # Agregar el último paso
            if paso_actual.strip():
                pasos.insertar_al_final(paso_actual.strip())

            # Generar nodos
            for i in range(pasos.obtener_tamaño()):
                paso = pasos.obtener(i)
                dot_content.insertar_al_final(f'    "{paso}";')

            dot_content.insertar_al_final("")
            dot_content.insertar_al_final("    # Conexiones entre pasos")

            # Generar conexiones
            for i in range(pasos.obtener_tamaño() - 1):
                paso_actual = pasos.obtener(i)
                paso_siguiente = pasos.obtener(i + 1)
                dot_content.insertar_al_final(
                    f'    "{paso_actual}" -> "{paso_siguiente}";')

        dot_content.insertar_al_final("}")

        # Convertir a string y guardar
        contenido_string = self._convertir_lista_a_string(dot_content)

        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_string)
            return Resultado(True, f"Grafo Graphviz generado: {nombre_archivo}")
        except Exception as e:
            return Resultado(False, f"Error al generar grafo: {str(e)}")

    def generar_grafo_cola_riego(self, cola_riego, nombre_archivo="grafo_cola_riego.dot"):
        # Generar código Graphviz para visualizar el estado de la cola de riego
        dot_content = ListaEnlazada()

        # Encabezado del grafo
        dot_content.insertar_al_final("digraph ColaRiego {")
        dot_content.insertar_al_final("    rankdir=LR;")
        dot_content.insertar_al_final("    node [shape=rect, style=filled];")
        dot_content.insertar_al_final("    edge [color=red, penwidth=2];")
        dot_content.insertar_al_final("")

        # Nodo indicador de frente y final
        dot_content.insertar_al_final(
            '    "FRENTE" [fillcolor=green, shape=diamond];')
        dot_content.insertar_al_final(
            '    "FINAL" [fillcolor=red, shape=diamond];')
        dot_content.insertar_al_final("")

        # Generar nodos para elementos en la cola
        if not cola_riego.esta_vacia():
            elementos_cola = ListaEnlazada()

            # Recorrer la cola para obtener elementos
            actual = cola_riego.frente
            contador = 0
            while actual:
                elemento = f"H{actual.dato.hilera}-P{actual.dato.planta}"
                elementos_cola.insertar_al_final(elemento)
                dot_content.insertar_al_final(
                    f'    "Elemento_{contador}" [label="{elemento}", fillcolor=lightblue];')
                actual = actual.siguiente
                contador += 1

            dot_content.insertar_al_final("")
            dot_content.insertar_al_final("    # Conexiones")

            # Conectar frente al primer elemento
            if elementos_cola.obtener_tamaño() > 0:
                dot_content.insertar_al_final('    "FRENTE" -> "Elemento_0";')

                # Conectar elementos entre sí
                for i in range(elementos_cola.obtener_tamaño() - 1):
                    dot_content.insertar_al_final(
                        f'    "Elemento_{i}" -> "Elemento_{i+1}";')

                # Conectar último elemento al final
                ultimo_indice = elementos_cola.obtener_tamaño() - 1
                dot_content.insertar_al_final(
                    f'    "Elemento_{ultimo_indice}" -> "FINAL";')
        else:
            dot_content.insertar_al_final(
                '    "VACIA" [fillcolor=gray, label="Cola Vacía"];')
            dot_content.insertar_al_final('    "FRENTE" -> "VACIA";')
            dot_content.insertar_al_final('    "VACIA" -> "FINAL";')

        dot_content.insertar_al_final("}")

        # Convertir a string y guardar
        contenido_string = self._convertir_lista_a_string(dot_content)

        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_string)
            return Resultado(True, f"Grafo de cola generado: {nombre_archivo}")
        except Exception as e:
            return Resultado(False, f"Error al generar grafo de cola: {str(e)}")

    def generar_grafo_estado_drones(self, lista_drones, nombre_archivo="grafo_drones.dot"):
        # Generar código Graphviz para visualizar el estado actual de los drones
        dot_content = ListaEnlazada()

        # Encabezado del grafo
        dot_content.insertar_al_final("digraph EstadoDrones {")
        dot_content.insertar_al_final("    rankdir=TB;")
        dot_content.insertar_al_final(
            "    node [shape=ellipse, style=filled];")
        dot_content.insertar_al_final("    edge [color=blue];")
        dot_content.insertar_al_final("")

        # Generar nodos para cada dron
        for i in range(lista_drones.obtener_tamaño()):
            dron = lista_drones.obtener(i)

            # Color según estado del dron
            color = "lightgreen" if dron.finalizado else "lightblue"
            if dron.agua_utilizada > 0:
                color = "lightyellow"

            # Información del dron
            info_dron = f"{dron.id}\\nPosición: {dron.posicion_actual}\\nAgua: {dron.agua_utilizada}L\\nFertilizante: {dron.fertilizante_utilizado}g"

            dot_content.insertar_al_final(
                f'    "{dron.id}" [label="{info_dron}", fillcolor={color}];')

            # Conectar con su hilera asignada si existe
            if dron.hilera_asignada:
                hilera_info = f"Hilera_{dron.hilera_asignada.numero}"
                dot_content.insertar_al_final(
                    f'    "{hilera_info}" [label="Hilera {dron.hilera_asignada.numero}\\nPlantas: {dron.hilera_asignada.obtener_cantidad_plantas()}", shape=rect, fillcolor=lightcoral];')
                dot_content.insertar_al_final(
                    f'    "{dron.id}" -> "{hilera_info}";')

        dot_content.insertar_al_final("}")

        # Convertir a string y guardar
        contenido_string = self._convertir_lista_a_string(dot_content)

        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_string)
            return Resultado(True, f"Grafo de drones generado: {nombre_archivo}")
        except Exception as e:
            return Resultado(False, f"Error al generar grafo de drones: {str(e)}")

    def _convertir_lista_a_string(self, lista_enlazada):
        # Convertir ListaEnlazada a string
        resultado = ""
        for i in range(lista_enlazada.obtener_tamaño()):
            if i > 0:
                resultado += "\n"
            resultado += lista_enlazada.obtener(i)
        return resultado
