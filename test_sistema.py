#!/usr/bin/env python3
"""
Script de prueba para el Sistema de Riego Robótico
Día 2: Carga de XML, almacenamiento en TDAs y simulación básica
"""

import os
from app.controllers.sistema_riego import SistemaRiego


def main():
    print("="*60)
    print("SISTEMA DE RIEGO ROBÓTICO - PRUEBA DE FUNCIONALIDAD")
    print("="*60)
    
    # Inicializar el sistema
    sistema = SistemaRiego()
    
    # Ruta del archivo de entrada
    archivo_entrada = os.path.join("input", "entrada.xml")
    archivo_salida = os.path.join("output", "salida.xml")
    
    try:
        print(f"\n1. Cargando archivo de entrada: {archivo_entrada}")
        
        # Verificar si el archivo existe
        if not os.path.exists(archivo_entrada):
            print(f"ERROR: El archivo {archivo_entrada} no existe.")
            print("Creando archivo de ejemplo...")
            crear_archivo_ejemplo(archivo_entrada)
        
        # Cargar la configuración desde XML
        print("   - Parseando XML...")
        sistema.cargar_configuracion(archivo_entrada)
        print("   ✓ Configuración cargada exitosamente")
        
        print("\n2. Verificando datos cargados:")
        
        # Mostrar drones cargados
        print("   - Drones disponibles:")
        for i in range(sistema.drones.obtener_tamaño()):
            dron = sistema.drones.obtener(i)
            print(f"     * {dron.nombre} (ID: {dron.id})")
        
        # Mostrar invernaderos cargados
        print("   - Invernaderos configurados:")
        for i in range(sistema.invernaderos.obtener_tamaño()):
            invernadero = sistema.invernaderos.obtener(i)
            print(f"     * {invernadero.nombre}")
            print(f"       - Hileras: {invernadero.numero_hileras}")
            print(f"       - Plantas por hilera: {invernadero.plantas_por_hilera}")
            print(f"       - Total plantas: {invernadero.hileras.obtener_tamaño() * invernadero.plantas_por_hilera}")
            
            # Mostrar plan de riego
            print("       - Plan de riego:")
            if hasattr(invernadero.plan_riego, 'obtener_plan_original'):
                plan_original = invernadero.plan_riego.obtener_plan_original()
                print(f"         * Plan: {plan_original}")
            else:
                print("         * Sin plan configurado")
        
        print("\n3. Ejecutando simulación...")
        
        # Intentar simular el primer invernadero
        if sistema.invernaderos.obtener_tamaño() > 0:
            try:
                print("   - Seleccionando primer invernadero...")
                exito = sistema.seleccionar_invernadero(0)
                
                if exito:
                    print("   - Ejecutando simulación...")
                    resultado = sistema.ejecutar_simulacion()
                    
                    if resultado:
                        print("   ✓ Simulación ejecutada exitosamente")
                    else:
                        print("   ✗ Error en la simulación")
                else:
                    print("   ✗ No se pudo seleccionar invernadero")
            except Exception as e:
                print(f"   ✗ Error en simulación: {e}")
        else:
            print("   ✗ No hay invernaderos para simular")
        
        print("\n4. Generando archivo de salida...")
        
        # Generar archivo de salida
        sistema.generar_archivo_salida(archivo_salida)
        print(f"   ✓ Archivo generado: {archivo_salida}")
        
        print("\n" + "="*60)
        print("PRUEBA COMPLETADA EXITOSAMENTE")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR durante la ejecución: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def crear_archivo_ejemplo(ruta_archivo):
    """Crea un archivo de ejemplo si no existe"""
    
    # Crear directorio si no existe
    directorio = os.path.dirname(ruta_archivo)
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    contenido_xml = """<?xml version="1.0" encoding="UTF-8"?>
<configuracion>
    <listaDrones>
        <dron id="1" nombre="DR01"/>
        <dron id="2" nombre="DR02"/>
        <dron id="3" nombre="DR03"/>
    </listaDrones>
    
    <listaInvernaderos>
        <invernadero nombre="Invernadero Zacapa">
            <numeroHileras>3</numeroHileras>
            <plantasXhilera>4</plantasXhilera>
            
            <listaPlantas>
                <planta hilera="1" posicion="1" litrosAgua="1" gramosFertilizante="100">ciprés</planta>
                <planta hilera="1" posicion="2" litrosAgua="1" gramosFertilizante="100">ciprés</planta>
                <planta hilera="1" posicion="3" litrosAgua="1" gramosFertilizante="100">ciprés italiano</planta>
                <planta hilera="1" posicion="4" litrosAgua="1" gramosFertilizante="100">ciprés italiano</planta>
                
                <planta hilera="2" posicion="1" litrosAgua="1" gramosFertilizante="100">ciprés italiano</planta>
                <planta hilera="2" posicion="2" litrosAgua="1" gramosFertilizante="100">ciprés italiano</planta>
                <planta hilera="2" posicion="3" litrosAgua="1" gramosFertilizante="100">ciprés de tarout</planta>
                <planta hilera="2" posicion="4" litrosAgua="1" gramosFertilizante="100">ciprés de tarout</planta>
                
                <planta hilera="3" posicion="1" litrosAgua="1" gramosFertilizante="100">ciprés de tarout</planta>
                <planta hilera="3" posicion="2" litrosAgua="1" gramosFertilizante="100">ciprés italiano</planta>
                <planta hilera="3" posicion="3" litrosAgua="1" gramosFertilizante="100">ciprés</planta>
                <planta hilera="3" posicion="4" litrosAgua="1" gramosFertilizante="100">ciprés</planta>
            </listaPlantas>
            
            <asignacionDrones>
                <dron id="1" hilera="1"/>
                <dron id="2" hilera="2"/>
                <dron id="3" hilera="3"/>
            </asignacionDrones>
            
            <planesRiego>
                <plan nombre="Semana 1">H1-P2, H2-P1, H2-P2, H3-P3, H1-P4</plan>
                <plan nombre="Semana 2">H3-P1, H1-P3, H2-P4, H3-P4, H2-P3, H1-P1, H3-P2</plan>
            </planesRiego>
        </invernadero>
    </listaInvernaderos>
</configuracion>"""
    
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(contenido_xml)
    
    print(f"   ✓ Archivo de ejemplo creado: {ruta_archivo}")


if __name__ == "__main__":
    main()