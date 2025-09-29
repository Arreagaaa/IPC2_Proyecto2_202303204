import xml.etree.ElementTree as ET
from xml.dom import minidom


class XMLGenerator:
    def __init__(self):
        pass

    def generar_archivo_salida(self, invernadero, resultados, registro_instrucciones, ruta_salida):
        try:
            from app.models.resultado import Resultado
            import os

            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_salida)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            root = ET.Element("salida")

            if invernadero is None:
                return Resultado(False, "No hay invernadero para generar salida")

            # Información del invernadero
            invernadero_elem = ET.SubElement(root, "invernadero")
            invernadero_elem.set("nombre", invernadero.nombre)

            hileras_elem = ET.SubElement(invernadero_elem, "numeroHileras")
            hileras_elem.text = str(invernadero.hileras.obtener_tamaño())

            plantas_hilera_elem = ET.SubElement(
                invernadero_elem, "plantasXhilera")
            if invernadero.hileras.obtener_tamaño() > 0:
                primera_hilera = invernadero.hileras.obtener(0)
                plantas_hilera_elem.text = str(
                    primera_hilera.plantas.obtener_tamaño())
            else:
                plantas_hilera_elem.text = "0"

            # Plan de riego ejecutado
            plan_elem = ET.SubElement(root, "planRiego")
            plan_elem.text = invernadero.plan_riego.obtener_plan_original()

            # Resultados de simulación
            if resultados:
                tiempo_elem = ET.SubElement(root, "tiempoTotal")
                tiempo_elem.text = str(resultados.tiempo_total)

                agua_elem = ET.SubElement(root, "aguaTotal")
                agua_elem.text = str(resultados.total_agua)

                fertilizante_elem = ET.SubElement(root, "fertilizanteTotal")
                fertilizante_elem.text = str(resultados.total_fertilizante)

                # Resultados por dron
                drones_elem = ET.SubElement(root, "resultadosDrones")
                for i in range(resultados.resultados_drones.obtener_tamaño()):
                    resultado_dron = resultados.resultados_drones.obtener(i)
                    dron_elem = ET.SubElement(drones_elem, "dron")
                    dron_elem.set("id", str(resultado_dron.id))

                    agua_dron = ET.SubElement(dron_elem, "aguaUtilizada")
                    agua_dron.text = str(resultado_dron.agua_utilizada)

                    fertilizante_dron = ET.SubElement(
                        dron_elem, "fertilizanteUtilizado")
                    fertilizante_dron.text = str(
                        resultado_dron.fertilizante_utilizado)

            # Registro de instrucciones (opcional)
            if registro_instrucciones:
                instrucciones_elem = ET.SubElement(
                    root, "registroInstrucciones")
                for entrada in registro_instrucciones:
                    tiempo_entry = ET.SubElement(instrucciones_elem, "tiempo")
                    tiempo_entry.set("segundo", str(entrada.tiempo))

                    for instruccion in entrada.instrucciones.instrucciones:
                        dron_instruccion = ET.SubElement(tiempo_entry, "dron")
                        dron_instruccion.set("id", str(instruccion.dron_id))
                        dron_instruccion.text = instruccion.instruccion

            # Generar XML con formato
            rough_string = ET.tostring(root, 'utf-8')
            reparsed = minidom.parseString(rough_string)

            with open(ruta_salida, 'w', encoding='utf-8') as archivo:
                archivo.write(reparsed.toprettyxml(indent="  "))

            return Resultado(True, f"Archivo XML generado: {ruta_salida}")

        except Exception as e:
            return Resultado(False, f"Error generando archivo XML: {e}")

    def validar_estructura_xml(self, ruta_archivo):
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()

            # Usar ListaEnlazada en lugar de lista nativa
            from app.tdas.lista_enlazada import ListaEnlazada
            elementos_requeridos = ListaEnlazada()
            elementos_requeridos.insertar_al_final('invernadero')
            elementos_requeridos.insertar_al_final('tiempoTotal')
            elementos_requeridos.insertar_al_final('aguaTotal')
            elementos_requeridos.insertar_al_final('fertilizanteTotal')
            elementos_requeridos.insertar_al_final('resultadosDrones')

            for elemento in elementos_requeridos:
                if root.find(elemento) is None:
                    print(f"Elemento requerido '{elemento}' no encontrado")
                    return False

            invernadero = root.find('invernadero')
            if invernadero.get('nombre') is None:
                print("Atributo 'nombre' del invernadero no encontrado")
                return False

            return True

        except Exception as e:
            print(f"Error validando XML: {e}")
            return False

    def obtener_estadisticas_xml(self, ruta_archivo):
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()

            # Usar resultado en lugar de diccionario
            from app.models.resultado import Resultado
            resultado = Resultado()
            resultado.invernadero_nombre = root.find(
                'invernadero').get('nombre')
            resultado.tiempo_total = float(root.find('tiempoTotal').text)
            resultado.agua_total = float(root.find('aguaTotal').text)
            resultado.fertilizante_total = float(
                root.find('fertilizanteTotal').text)
            resultado.numero_drones = len(
                root.find('resultadosDrones').findall('dron'))

            return resultado

        except Exception as e:
            print(f"Error obteniendo estadisticas XML: {e}")
            return None
