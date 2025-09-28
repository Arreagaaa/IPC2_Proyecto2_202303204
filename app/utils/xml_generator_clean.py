import xml.etree.ElementTree as ET
from xml.dom import minidom


class XMLGenerator:
    def __init__(self):
        pass
    
    def generar_archivo_salida(self, sistema, ruta_salida):
        try:
            root = ET.Element("salida")
            
            if sistema.invernadero_actual is None:
                return False
            
            invernadero_elem = ET.SubElement(root, "invernadero")
            invernadero_elem.set("nombre", sistema.invernadero_actual.nombre)
            
            hileras_elem = ET.SubElement(invernadero_elem, "numeroHileras")
            hileras_elem.text = str(sistema.invernadero_actual.hileras.obtener_tamaño())
            
            plantas_hilera_elem = ET.SubElement(invernadero_elem, "plantasXhilera")
            if sistema.invernadero_actual.hileras.obtener_tamaño() > 0:
                primera_hilera = sistema.invernadero_actual.hileras.obtener(0)
                plantas_hilera_elem.text = str(primera_hilera.plantas.obtener_tamaño())
            else:
                plantas_hilera_elem.text = "0"
            
            if sistema.simulaciones.obtener_tamaño() > 0:
                simulacion = sistema.simulaciones.obtener(sistema.simulaciones.obtener_tamaño() - 1)
                resultados = simulacion.obtener_resultados()
                
                tiempo_elem = ET.SubElement(root, "tiempoTotal")
                tiempo_elem.text = str(resultados.tiempo_total)
                
                agua_elem = ET.SubElement(root, "aguaTotal")
                agua_elem.text = str(resultados.total_agua)
                
                fertilizante_elem = ET.SubElement(root, "fertilizanteTotal")
                fertilizante_elem.text = str(resultados.total_fertilizante)
                
                drones_elem = ET.SubElement(root, "resultadosDrones")
                for i in range(resultados.resultados_drones.obtener_tamaño()):
                    resultado_dron = resultados.resultados_drones.obtener(i)
                    dron_elem = ET.SubElement(drones_elem, "dron")
                    dron_elem.set("id", resultado_dron.id)
                    
                    agua_dron = ET.SubElement(dron_elem, "aguaUtilizada")
                    agua_dron.text = str(resultado_dron.agua_utilizada)
                    
                    fertilizante_dron = ET.SubElement(dron_elem, "fertilizanteUtilizado")
                    fertilizante_dron.text = str(resultado_dron.fertilizante_utilizado)
            
            rough_string = ET.tostring(root, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            
            with open(ruta_salida, 'w', encoding='utf-8') as archivo:
                archivo.write(reparsed.toprettyxml(indent="  "))
            
            return True
            
        except Exception as e:
            print(f"Error generando archivo XML: {e}")
            return False
    
    def validar_estructura_xml(self, ruta_archivo):
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            elementos_requeridos = [
                'invernadero',
                'tiempoTotal',
                'aguaTotal',
                'fertilizanteTotal',
                'resultadosDrones'
            ]
            
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
            
            estadisticas = {
                'invernadero': root.find('invernadero').get('nombre'),
                'tiempo_total': float(root.find('tiempoTotal').text),
                'agua_total': float(root.find('aguaTotal').text),
                'fertilizante_total': float(root.find('fertilizanteTotal').text),
                'numero_drones': len(root.find('resultadosDrones').findall('dron'))
            }
            
            return estadisticas
            
        except Exception as e:
            print(f"Error obteniendo estadisticas XML: {e}")
            return None