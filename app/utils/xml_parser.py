import xml.etree.ElementTree as ET
from app.models.invernadero import Invernadero
from app.models.hilera import Hilera
from app.models.planta import Planta
from app.models.dron import Dron
from app.models.plan_riego import PlanRiego
from app.tdas.lista_enlazada import ListaEnlazada

class XMLParser:
    @staticmethod
    def parsear_configuracion(ruta_archivo):
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            invernaderos = ListaEnlazada()
            
            for inv_xml in root.findall('invernadero'):
                nombre = inv_xml.get('nombre')
                invernadero = Invernadero(nombre)
                
                for hilera_xml in inv_xml.findall('hilera'):
                    numero = int(hilera_xml.get('numero'))
                    hilera = Hilera(numero)
                    
                    for planta_xml in hilera_xml.findall('planta'):
                        nombre_planta = planta_xml.get('nombre')
                        posicion = int(planta_xml.get('posicion'))
                        planta = Planta(nombre_planta, posicion)
                        
                        if planta_xml.find('riego') is not None:
                            agua_elem = planta_xml.find('riego/agua')
                            fertilizante_elem = planta_xml.find('riego/fertilizante')
                            
                            if agua_elem is not None:
                                planta.agua_requerida = float(agua_elem.text)
                            if fertilizante_elem is not None:
                                planta.fertilizante_requerido = float(fertilizante_elem.text)
                        
                        hilera.plantas.insertar_al_final(planta)
                    
                    invernadero.hileras.insertar_al_final(hilera)
                
                for dron_xml in inv_xml.findall('dron'):
                    id_dron = int(dron_xml.get('id'))
                    dron = Dron(id_dron)
                    
                    posicion_elem = dron_xml.find('posicion')
                    if posicion_elem is not None:
                        dron.posicion_x = int(posicion_elem.get('x'))
                        dron.posicion_y = int(posicion_elem.get('y'))
                    
                    capacidad_elem = dron_xml.find('capacidad')
                    if capacidad_elem is not None:
                        agua_elem = capacidad_elem.find('agua')
                        fertilizante_elem = capacidad_elem.find('fertilizante')
                        
                        if agua_elem is not None:
                            dron.capacidad_agua = float(agua_elem.text)
                        if fertilizante_elem is not None:
                            dron.capacidad_fertilizante = float(fertilizante_elem.text)
                    
                    invernadero.drones.insertar_al_final(dron)
                
                invernaderos.insertar_al_final(invernadero)
            
            return invernaderos
            
        except Exception as e:
            print(f"Error parseando XML: {e}")
            return ListaEnlazada()
