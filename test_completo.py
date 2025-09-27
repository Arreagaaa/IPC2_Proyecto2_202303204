"""
Script de prueba completo para el Sistema de Riego Robótico
Release 3: Simulación + XML de salida + Reporte HTML + Gráficos TDAs
"""

from app.controllers.sistema_riego import SistemaRiego


def main():
    print("=" * 70)
    print("SISTEMA DE RIEGO ROBÓTICO - PRUEBA COMPLETA")
    print("Release 3: Simulación + XML + HTML + Graphviz")
    print("=" * 70)

    # Crear sistema
    sistema = SistemaRiego()

    # 1. Cargar configuración
    print("\n1. Cargando archivo de entrada: input/entrada.xml")
    print("   - Parseando XML...")
    if not sistema.cargar_configuracion("input/entrada.xml"):
        print("   ✗ Error al cargar configuración")
        return

    print("   ✓ Configuración cargada exitosamente")

    # 2. Seleccionar invernadero
    print("\n2. Seleccionando primer invernadero...")
    if not sistema.seleccionar_invernadero(0):
        print("   ✗ Error al seleccionar invernadero")
        return

    print("   ✓ Invernadero seleccionado")

    # 3. Ejecutar simulación
    print("\n3. Ejecutando simulación...")
    print("   - Aplicando restricciones de un solo dron regando")
    print("   - Calculando tiempos y movimientos...")
    if not sistema.ejecutar_simulacion():
        print("   ✗ Error en la simulación")
        return

    print("   ✓ Simulación ejecutada exitosamente")

    # 4. Generar archivo XML de salida
    print("\n4. Generando archivo de salida XML...")
    if not sistema.generar_archivo_salida("output/salida.xml"):
        print("   ✗ Error al generar archivo XML")
        return

    print("   ✓ Archivo XML generado: output/salida.xml")

    # 5. Generar reporte HTML
    print("\n5. Generando reporte HTML...")
    if not sistema.generar_reporte_html():
        print("   ✗ Error al generar reporte HTML")
        return

    print("   ✓ Reporte HTML generado")

    # 6. Generar gráficos de TDAs
    print("\n6. Generando gráficos de TDAs con Graphviz...")
    if not sistema.generar_grafos_tdas():
        print("   ✗ Error al generar gráficos")
        return

    print("   ✓ Gráficos Graphviz generados")

    # 7. Mostrar reporte detallado en consola
    print("\n7. Mostrando reporte detallado:")
    print("-" * 50)
    sistema.mostrar_reporte_detallado()

    # 8. Mostrar estado final del sistema
    print("\n8. Estado final del sistema:")
    print("-" * 30)
    print(sistema.obtener_estado_sistema())

    print("\n" + "=" * 70)
    print("PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 70)

    print("\nArchivos generados:")
    print("  📄 output/salida.xml - XML con resultados de simulación")
    print("  🌐 ReporteInvernadero_*.html - Reporte HTML interactivo")
    print("  📊 grafo_plan_riego.dot - Gráfico del plan de riego")
    print("  📊 grafo_cola_riego.dot - Gráfico de la cola de riego")
    print("  📊 grafo_drones.dot - Gráfico del estado de drones")

    print("\nPara ver los gráficos, use:")
    print("  dot -Tpng grafo_plan_riego.dot -o grafo_plan_riego.png")
    print("  dot -Tpng grafo_cola_riego.dot -o grafo_cola_riego.png")
    print("  dot -Tpng grafo_drones.dot -o grafo_drones.png")

    print("\n¡Sistema completamente funcional! 🎉")


if __name__ == "__main__":
    main()
