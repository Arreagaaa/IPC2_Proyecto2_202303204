import xml.etree.ElementTree as ET
from app.models.invernadero import Invernadero
from app.models.hilera import Hilera
from app.models.planta import Planta
from app.models.dron import Dron
from app.models.plan_riego import PlanRiego
from app.tdas.lista_enlazada import ListaEnlazada


class XMLParser:
    def __init__(self):
        self.drones_disponibles = ListaEnlazada()
        self.invernaderos = ListaEnlazada()

    def cargar_archivo(self, ruta_archivo):
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()

            # Limpiar datos anteriores
            self.drones_disponibles = ListaEnlazada()
            self.invernaderos = ListaEnlazada()

            # Parsear lista de drones
            lista_drones = root.find('listaDrones')
            if lista_drones is not None:
                for dron_xml in lista_drones.findall('dron'):
                    id_dron = int(dron_xml.get('id'))
                    nombre_dron = dron_xml.get('nombre')
                    dron = Dron(id_dron)
                    dron.nombre = nombre_dron
                    self.drones_disponibles.insertar_al_final(dron)

            # Parsear lista de invernaderos
            lista_invernaderos = root.find('listaInvernaderos')
            if lista_invernaderos is not None:
                for inv_xml in lista_invernaderos.findall('invernadero'):
                    nombre = inv_xml.get('nombre')
                    invernadero = Invernadero(nombre)

                    # Obtener configuracion basica
                    num_hileras_elem = inv_xml.find('numeroHileras')
                    plantas_x_hilera_elem = inv_xml.find('plantasXhilera')

                    if num_hileras_elem is not None:
                        num_hileras = int(num_hileras_elem.text.strip())
                    if plantas_x_hilera_elem is not None:
                        plantas_x_hilera = int(
                            plantas_x_hilera_elem.text.strip())

                    # Crear estructura de hileras
                    for i in range(1, num_hileras + 1):
                        hilera = Hilera(i)
                        invernadero.hileras.insertar_al_final(hilera)

                    # Parsear plantas
                    lista_plantas = inv_xml.find('listaPlantas')
                    if lista_plantas is not None:
                        for planta_xml in lista_plantas.findall('planta'):
                            hilera_num = int(planta_xml.get('hilera'))
                            posicion = int(planta_xml.get('posicion'))
                            litros_agua = float(planta_xml.get('litrosAgua'))
                            gramos_fertilizante = float(
                                planta_xml.get('gramosFertilizante'))
                            nombre_planta = planta_xml.text.strip() if planta_xml.text else "Planta"

                            planta = Planta(nombre_planta, posicion)
                            planta.agua_requerida = litros_agua
                            planta.fertilizante_requerido = gramos_fertilizante

                            # Buscar hilera correspondiente
                            for hilera in invernadero.hileras:
                                if hilera.numero == hilera_num:
                                    hilera.plantas.insertar_al_final(planta)
                                    break

                    # Parsear asignacion de drones
                    asignacion_drones = inv_xml.find('asignacionDrones')
                    if asignacion_drones is not None:
                        for dron_xml in asignacion_drones.findall('dron'):
                            id_dron = int(dron_xml.get('id'))
                            hilera_num = int(dron_xml.get('hilera'))

                            # Buscar dron en la lista de drones disponibles
                            for dron_disponible in self.drones_disponibles:
                                if dron_disponible.id == id_dron:
                                    # Crear copia del dron para este invernadero
                                    dron_copia = Dron(dron_disponible.nombre)
                                    dron_copia.id = id_dron
                                    dron_copia.nombre = dron_disponible.nombre
                                    dron_copia.posicion_actual = 0  # Inicio de hilera
                                    
                                    # Buscar y asignar la hilera correspondiente
                                    for hilera in invernadero.hileras:
                                        if hilera.numero == hilera_num:
                                            dron_copia.asignar_hilera(hilera)
                                            hilera.asignar_dron(dron_copia)
                                            break
                                    
                                    invernadero.drones.insertar_al_final(dron_copia)
                                    break

                    # Parsear planes de riego
                    planes_riego = inv_xml.find('planesRiego')
                    if planes_riego is not None:
                        for plan_xml in planes_riego.findall('plan'):
                            nombre_plan = plan_xml.get('nombre')
                            secuencia_plan = plan_xml.text.strip() if plan_xml.text else ""

                            # Configurar plan de riego en el invernadero
                            invernadero.configurar_plan_riego(secuencia_plan)
                            # El plan se guarda en plan_riego del invernadero

                    self.invernaderos.insertar_al_final(invernadero)

            return self._crear_resultado_exitoso("Archivo cargado correctamente")

        except Exception as e:
            return self._crear_resultado_error(f"Error parseando XML: {e}")

    def obtener_invernaderos(self):
        return self.invernaderos

    def obtener_drones(self):
        return self.drones_disponibles

    def generar_resumen_carga(self):
        resumen = f"Drones cargados: {self.drones_disponibles.obtener_tamaño()}\n"
        resumen += f"Invernaderos cargados: {self.invernaderos.obtener_tamaño()}\n"
        return resumen

    def validar_configuracion(self):
        errores = ListaEnlazada()

        if self.drones_disponibles.obtener_tamaño() == 0:
            errores.insertar_al_final("No se cargaron drones")

        if self.invernaderos.obtener_tamaño() == 0:
            errores.insertar_al_final("No se cargaron invernaderos")

        return errores

    def _crear_resultado_exitoso(self, mensaje):
        class Resultado:
            def __init__(self, exito, mensaje):
                self.exito = exito
                self.mensaje = mensaje

            def es_exitoso(self):
                return self.exito

            def obtener_mensaje(self):
                return self.mensaje
        return Resultado(True, mensaje)

    def _crear_resultado_error(self, mensaje):
        class Resultado:
            def __init__(self, exito, mensaje):
                self.exito = exito
                self.mensaje = mensaje

            def es_exitoso(self):
                return self.exito

            def obtener_mensaje(self):
                return self.mensaje
        return Resultado(False, mensaje)
