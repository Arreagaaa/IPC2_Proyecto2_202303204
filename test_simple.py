#!/usr/bin/env python3
"""
Script de prueba simple para verificar que las importaciones funcionen correctamente
"""

def test_importaciones():
    """Prueba que todas las importaciones funcionen"""
    print("Probando importaciones...")
    
    try:
        # Probar TDAs
        from app.tdas.lista_enlazada import ListaEnlazada
        from app.tdas.cola import Cola
        from app.tdas.pila import Pila
        print("✓ TDAs importados correctamente")
        
        # Probar modelos básicos
        from app.models.planta import Planta
        from app.models.dron import Dron
        from app.models.hilera import Hilera
        print("✓ Modelos básicos importados correctamente")
        
        # Probar modelos avanzados
        from app.models.invernadero import Invernadero
        from app.models.plan_riego import PlanRiego
        from app.models.simulacion import Simulacion
        print("✓ Modelos avanzados importados correctamente")
        
        # Probar utils
        from app.utils.xml_parser import XMLParser
        from app.utils.xml_generator import XMLGenerator
        print("✓ Utils importados correctamente")
        
        # Probar controlador
        from app.controllers.sistema_riego import SistemaRiego
        print("✓ Controlador importado correctamente")
        
        return True
        
    except ImportError as e:
        print(f"✗ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return False

def test_tdas_basicos():
    """Prueba funcionalidad básica de TDAs"""
    print("\nProbando TDAs...")
    
    try:
        from app.tdas.lista_enlazada import ListaEnlazada
        from app.tdas.cola import Cola
        from app.tdas.pila import Pila
        
        # Test Lista Enlazada
        lista = ListaEnlazada()
        lista.insertar_al_final("Elemento 1")
        lista.insertar_al_final("Elemento 2")
        assert lista.obtener_tamaño() == 2
        assert lista.obtener(0) == "Elemento 1"
        print("✓ Lista Enlazada funciona correctamente")
        
        # Test Cola
        cola = Cola()
        cola.encolar("Primero")
        cola.encolar("Segundo")
        assert cola.obtener_tamaño() == 2
        assert cola.desencolar() == "Primero"
        print("✓ Cola funciona correctamente")
        
        # Test Pila
        pila = Pila()
        pila.apilar("Fondo")
        pila.apilar("Cima")
        assert pila.obtener_tamaño() == 2
        assert pila.desapilar() == "Cima"
        print("✓ Pila funciona correctamente")
        
        return True
        
    except Exception as e:
        print(f"✗ Error en TDAs: {e}")
        return False

def test_modelos_basicos():
    """Prueba funcionalidad básica de modelos"""
    print("\nProbando modelos...")
    
    try:
        from app.models.planta import Planta
        from app.models.dron import Dron
        from app.models.hilera import Hilera
        from app.models.invernadero import Invernadero
        from app.models.plan_riego import PlanRiego
        
        # Test Planta
        planta = Planta(1, 2.5, 150)
        assert planta.posicion == 1
        assert planta.litros_agua == 2.5
        print("✓ Planta funciona correctamente")
        
        # Test Dron
        dron = Dron("DR01")
        assert dron.id == "DR01"
        assert dron.posicion_actual == 0
        print("✓ Dron funciona correctamente")
        
        # Test Hilera
        hilera = Hilera(1)
        planta = Planta(1, 1.0, 100)
        hilera.agregar_planta(1.0, 100)
        assert hilera.numero == 1
        print("✓ Hilera funciona correctamente")
        
        # Test Invernadero
        invernadero = Invernadero("Test")
        assert invernadero.nombre == "Test"
        print("✓ Invernadero funciona correctamente")
        
        # Test Plan de Riego
        plan = PlanRiego()
        plan.agregar_paso(1, 2)
        assert plan.hay_pasos_pendientes()
        print("✓ Plan de Riego funciona correctamente")
        
        return True
        
    except Exception as e:
        print(f"✗ Error en modelos: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("="*50)
    print("PRUEBA DE SISTEMA DE RIEGO ROBÓTICO")
    print("="*50)
    
    # Ejecutar pruebas
    tests_passed = 0
    total_tests = 3
    
    if test_importaciones():
        tests_passed += 1
        
    if test_tdas_basicos():
        tests_passed += 1
        
    if test_modelos_basicos():
        tests_passed += 1
    
    print(f"\n{'='*50}")
    print(f"RESULTADO: {tests_passed}/{total_tests} pruebas pasaron")
    
    if tests_passed == total_tests:
        print("✓ Todas las pruebas fueron exitosas")
        return True
    else:
        print("✗ Algunas pruebas fallaron")
        return False

if __name__ == "__main__":
    main()