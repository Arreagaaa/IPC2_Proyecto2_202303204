import xml.etree.ElementTree as ET
from xml.dom import minidom
from app.models.simulacion import ResultadosSimulacion, RegistroTiempo, InstruccionesDron
from app.tdas.lista_enlazada import ListaEnlazada


class XMLGenerator:
    def __init__(self):
        pass

    def generar_archivo_salida(self, invernadero, resultados_simulacion, registro_instrucciones, ruta_salida):
        try:
            # Crear elemento raíz
            root = ET.Element('datosSalida')

            # Crear lista de invernaderos
            lista_invernaderos = ET.SubElement(root, 'listaInvernaderos')

            # Agregar invernadero
            invernadero_elem = ET.SubElement(lista_invernaderos, 'invernadero')
            invernadero_elem.set('nombre', invernadero.nombre)

            # Crear lista de planes
            lista_planes = ET.SubElement(invernadero_elem, 'listaPlanes')

            # Agregar plan (por ahora solo uno)
            plan_elem = ET.SubElement(lista_planes, 'plan')
            plan_elem.set('nombre', 'Plan Principal')

            # Agregar información del plan
            tiempo_elem = ET.SubElement(plan_elem, 'tiempoOptimoSegundos')
            tiempo_elem.text = str(resultados_simulacion.tiempo_total)

            agua_elem = ET.SubElement(plan_elem, 'aguaRequeridaLitros')
            agua_elem.text = str(resultados_simulacion.total_agua)

            fertilizante_elem = ET.SubElement(
                plan_elem, 'fertilizanteRequeridoGramos')
            fertilizante_elem.text = str(
                resultados_simulacion.total_fertilizante)

            # Agregar eficiencia de drones
            eficiencia_elem = ET.SubElement(
                plan_elem, 'eficienciaDronesRegadores')

            for i in range(resultados_simulacion.resultados_drones.obtener_tamaño()):
                resultado_dron = resultados_simulacion.resultados_drones.obtener(
                    i)
                dron_elem = ET.SubElement(eficiencia_elem, 'dron')
                dron_elem.set('nombre', resultado_dron.id)
                dron_elem.set('litrosAgua', str(resultado_dron.agua_utilizada))
                dron_elem.set('gramosFertilizante', str(
                    resultado_dron.fertilizante_utilizado))

            # Agregar instrucciones
            instrucciones_elem = ET.SubElement(plan_elem, 'instrucciones')

            for i in range(registro_instrucciones.obtener_tamaño()):
                registro = registro_instrucciones.obtener(i)
                tiempo_inst_elem = ET.SubElement(instrucciones_elem, 'tiempo')
                tiempo_inst_elem.set('segundos', str(registro.tiempo))

                # Agregar instrucciones de cada dron para este tiempo
                for j in range(registro.instrucciones.instrucciones.obtener_tamaño()):
                    instruccion = registro.instrucciones.instrucciones.obtener(
                        j)
                    dron_inst_elem = ET.SubElement(tiempo_inst_elem, 'dron')
                    dron_inst_elem.set('nombre', instruccion.dron_id)
                    dron_inst_elem.set('accion', instruccion.instruccion)

            # Formatear y guardar XML
            rough_string = ET.tostring(root, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="  ")

            # Remover líneas vacías
            lines = pretty_xml.split('\n')
            non_empty_lines = ListaEnlazada()
            for line in lines:
                if line.strip():
                    non_empty_lines.insertar_al_final(line)

            # Escribir archivo
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                for i in range(non_empty_lines.obtener_tamaño()):
                    if i > 0:
                        f.write('\n')
                    f.write(non_empty_lines.obtener(i))

            return True, "Archivo de salida generado exitosamente"

        except Exception as e:
            return False, f"Error al generar archivo de salida: {str(e)}"

    def generar_resumen_xml(self, invernadero, resultados_simulacion):
        try:
            root = ET.Element('resumen')

            # Información básica
            info_elem = ET.SubElement(root, 'informacion')

            invernadero_elem = ET.SubElement(info_elem, 'invernadero')
            invernadero_elem.text = invernadero.nombre

            tiempo_elem = ET.SubElement(info_elem, 'tiempoTotal')
            tiempo_elem.text = str(resultados_simulacion.tiempo_total)

            agua_elem = ET.SubElement(info_elem, 'aguaTotal')
            agua_elem.text = str(resultados_simulacion.total_agua)

            fertilizante_elem = ET.SubElement(info_elem, 'fertilizanteTotal')
            fertilizante_elem.text = str(
                resultados_simulacion.total_fertilizante)

            plan_elem = ET.SubElement(info_elem, 'planEjecutado')
            plan_elem.text = resultados_simulacion.plan_ejecutado

            # Resultados por dron
            drones_elem = ET.SubElement(root, 'resultadosDrones')

            for i in range(resultados_simulacion.resultados_drones.obtener_tamaño()):
                resultado_dron = resultados_simulacion.resultados_drones.obtener(
                    i)
                dron_elem = ET.SubElement(drones_elem, 'dron')
                dron_elem.set('id', resultado_dron.id)
                dron_elem.set('agua', str(resultado_dron.agua_utilizada))
                dron_elem.set('fertilizante', str(
                    resultado_dron.fertilizante_utilizado))

            # Formatear
            rough_string = ET.tostring(root, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ")

        except Exception as e:
            return f"Error al generar resumen XML: {str(e)}"
