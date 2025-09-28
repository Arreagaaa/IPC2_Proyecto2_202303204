import os
from datetime import datetime
from app.tdas.lista_enlazada import ListaEnlazada

class HTMLGenerator:
    def __init__(self):
        pass
    
    def generar_reporte_invernadero(self, invernadero, resultados=None, instrucciones=None):
        html = ListaEnlazada()
        html.insertar_al_final("<!DOCTYPE html>")
        html.insertar_al_final("<html><head><title>Reporte</title></head><body>")
        html.insertar_al_final(f"<h1>{invernadero.nombre}</h1>")
        html.insertar_al_final("</body></html>")
        return self._convertir_lista_a_string(html)
    
    def _convertir_lista_a_string(self, lista):
        resultado = ""
        for elemento in lista:
            resultado += str(elemento) + "\n"
        return resultado
    
    def guardar_reporte(self, contenido_html, ruta_archivo):
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_html)
            return True
        except Exception:
            return False
