from app.tdas.lista_enlazada import ListaEnlazada

class GraphvizGenerator:
    def __init__(self):
        pass
    
    def generar_grafico_plan_riego(self, plan_riego):
        lineas = ListaEnlazada()
        lineas.insertar_al_final("digraph PlanRiego {")
        lineas.insertar_al_final("    rankdir=TB;")
        lineas.insertar_al_final("    node [shape=record];")
        lineas.insertar_al_final("}")
        return self._convertir_lista_a_string(lineas)
    
    def generar_grafico_cola_riego(self, cola_riego):
        lineas = ListaEnlazada()
        lineas.insertar_al_final("digraph ColaRiego {")
        lineas.insertar_al_final("    rankdir=LR;")
        lineas.insertar_al_final("    node [shape=box];")
        lineas.insertar_al_final("}")
        return self._convertir_lista_a_string(lineas)
    
    def generar_grafico_drones(self, drones):
        lineas = ListaEnlazada()
        lineas.insertar_al_final("digraph Drones {")
        lineas.insertar_al_final("    rankdir=TB;")
        lineas.insertar_al_final("    node [shape=ellipse];")
        lineas.insertar_al_final("}")
        return self._convertir_lista_a_string(lineas)
    
    def _convertir_lista_a_string(self, lista):
        resultado = ""
        for elemento in lista:
            resultado += str(elemento) + "\n"
        return resultado
    
    def generar_archivo_dot(self, contenido_dot, ruta_archivo):
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_dot)
            return True
        except Exception:
            return False
