import xml.etree.ElementTree as ET
from app.models.dron import Dron
from app.models.invernadero import Invernadero
from app.models.hilera import Hilera
from app.models.planta import Planta
from app.models.plan_riego import PlanRiego
from app.tdas.lista_enlazada import ListaEnlazada


class XMLParser:
    def __init__(self):
        self.drones = ListaEnlazada()
        self.invernaderos = ListaEnlazada()

    def cargar_archivo(self, ruta_archivo):
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()

            # Limpiar datos anteriores
            self.drones.limpiar()
            self.invernaderos.limpiar()

            # Parsear drones
            self._parsear_drones(root)

            # Parsear invernaderos
            self._parsear_invernaderos(root)

            return True, "Archivo cargado exitosamente"

        except ET.ParseError as e:
            return False, f"Error de formato XML: {str(e)}"
        except FileNotFoundError:
            return False, f"Archivo no encontrado: {ruta_archivo}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

    def _parsear_drones(self, root):
        lista_drones = root.find('listaDrones')
        if lista_drones is not None:
            for dron_elem in lista_drones.findall('dron'):
                nombre_dron = dron_elem.get('nombre')

                dron = Dron(nombre_dron)
                self.drones.insertar_al_final(dron)

    def _parsear_invernaderos(self, root):
        lista_invernaderos = root.find('listaInvernaderos')
        if lista_invernaderos is not None:
            for invernadero_elem in lista_invernaderos.findall('invernadero'):
                nombre = invernadero_elem.get('nombre')

                # Crear invernadero
                invernadero = Invernadero(nombre)

                # Parsear configuración básica
                self._parsear_configuracion_invernadero(
                    invernadero_elem, invernadero)

                # Parsear plantas
                self._parsear_plantas(invernadero_elem, invernadero)

                # Parsear asignación de drones
                self._parsear_asignacion_drones(invernadero_elem, invernadero)

                # Parsear planes de riego
                self._parsear_planes_riego(invernadero_elem, invernadero)

                self.invernaderos.insertar_al_final(invernadero)

    def _parsear_configuracion_invernadero(self, invernadero_elem, invernadero):
        num_hileras_elem = invernadero_elem.find('numeroHileras')
        plantas_por_hilera_elem = invernadero_elem.find('plantasXhilera')

        if num_hileras_elem is not None and plantas_por_hilera_elem is not None:
            num_hileras = int(num_hileras_elem.text.strip())
            plantas_por_hilera = int(plantas_por_hilera_elem.text.strip())

            # Crear hileras
            for i in range(1, num_hileras + 1):
                invernadero.agregar_hilera(i)

    def _parsear_plantas(self, invernadero_elem, invernadero):
        lista_plantas = invernadero_elem.find('listaPlantas')
        if lista_plantas is not None:
            for planta_elem in lista_plantas.findall('planta'):
                hilera_num = int(planta_elem.get('hilera'))
                posicion = int(planta_elem.get('posicion'))
                litros_agua = float(planta_elem.get('litrosAgua'))
                gramos_fertilizante = float(
                    planta_elem.get('gramosFertilizante'))
                tipo_planta = planta_elem.text.strip() if planta_elem.text else ""

                # Buscar la hilera correspondiente
                hilera = invernadero.obtener_hilera(hilera_num)
                if hilera:
                    planta = Planta(tipo_planta, litros_agua,
                                    gramos_fertilizante)
                    hilera.establecer_planta_en_posicion(posicion, planta)

    def _parsear_asignacion_drones(self, invernadero_elem, invernadero):
        asignacion_drones = invernadero_elem.find('asignacionDrones')
        if asignacion_drones is not None:
            for dron_elem in asignacion_drones.findall('dron'):
                id_dron = int(dron_elem.get('id'))
                hilera_num = int(dron_elem.get('hilera'))

                # Buscar el dron en la lista de drones
                dron = self._buscar_dron_por_id(id_dron)
                hilera = invernadero.obtener_hilera(hilera_num)

                if dron and hilera:
                    # Crear una copia del dron para este invernadero
                    dron_asignado = Dron(dron.id)
                    dron_asignado.asignar_hilera(hilera)
                    # Asignar dron a la hilera también
                    hilera.asignar_dron(dron_asignado)
                    invernadero.agregar_dron(dron_asignado)

    def _parsear_planes_riego(self, invernadero_elem, invernadero):
        planes_riego = invernadero_elem.find('planesRiego')
        if planes_riego is not None:
            for plan_elem in planes_riego.findall('plan'):
                nombre_plan = plan_elem.get('nombre')
                secuencia = plan_elem.text.strip() if plan_elem.text else ""

                plan = PlanRiego()
                plan.parsear_plan_desde_cadena(secuencia)

                # Establecer el plan de riego (por simplicidad, usar el último)
                invernadero.plan_riego = plan

    def _buscar_dron_por_id(self, id_dron_numerico):
        # Mapear ID numérico a nombre de dron
        nombre_dron = f"DR{id_dron_numerico:02d}"

        for i in range(self.drones.obtener_tamaño()):
            dron = self.drones.obtener(i)
            if dron.id == nombre_dron:
                return dron
        return None

    def obtener_drones(self):
        return self.drones

    def obtener_invernaderos(self):
        return self.invernaderos

    def generar_resumen_carga(self):
        resumen = ListaEnlazada()

        resumen.insertar_al_final("=== RESUMEN DE CARGA ===")
        resumen.insertar_al_final(
            f"Drones cargados: {self.drones.obtener_tamaño()}")

        for i in range(self.drones.obtener_tamaño()):
            dron = self.drones.obtener(i)
            resumen.insertar_al_final(f"  - {dron.nombre} (ID: {dron.id})")

        resumen.insertar_al_final(
            f"\nInvernaderos cargados: {self.invernaderos.obtener_tamaño()}")

        for i in range(self.invernaderos.obtener_tamaño()):
            invernadero = self.invernaderos.obtener(i)
            resumen.insertar_al_final(f"  - {invernadero.nombre}")
            resumen.insertar_al_final(
                f"    Hileras: {invernadero.hileras.obtener_tamaño()}")
            resumen.insertar_al_final(
                f"    Drones asignados: {invernadero.drones.obtener_tamaño()}")

            # Contar plantas
            total_plantas = 0
            for j in range(invernadero.hileras.obtener_tamaño()):
                hilera = invernadero.hileras.obtener(j)
                total_plantas += hilera.plantas.obtener_tamaño()
            resumen.insertar_al_final(f"    Total plantas: {total_plantas}")

        # Convertir a string
        resultado = ""
        for i in range(resumen.obtener_tamaño()):
            if i > 0:
                resultado += "\n"
            resultado += resumen.obtener(i)

        return resultado

    def validar_configuracion(self):
        errores = ListaEnlazada()

        # Validar que hay drones
        if self.drones.obtener_tamaño() == 0:
            errores.insertar_al_final("No se cargaron drones")

        # Validar que hay invernaderos
        if self.invernaderos.obtener_tamaño() == 0:
            errores.insertar_al_final("No se cargaron invernaderos")

        # Validar cada invernadero
        for i in range(self.invernaderos.obtener_tamaño()):
            invernadero = self.invernaderos.obtener(i)
            errores_inv = invernadero.validar_configuracion()

            # Agregar errores del invernadero
            for j in range(errores_inv.obtener_tamaño()):
                errores.insertar_al_final(
                    f"{invernadero.nombre}: {errores_inv.obtener(j)}")

        return errores
