# clase para reemplazar tuplas en retornos de métodos

class Resultado:
    # clase para manejar resultados de operaciones sin usar tuplas nativas

    def __init__(self, exito, mensaje="", data=None):
        # inicializa un resultado de operación
        self.exito = exito
        self.mensaje = mensaje
        self.data = data

    def es_exitoso(self):
        # retorna si el resultado es exitoso
        return self.exito

    def obtener_mensaje(self):
        # retorna el mensaje del resultado
        return self.mensaje

    def obtener_data(self):
        # retorna los datos del resultado
        return self.data
