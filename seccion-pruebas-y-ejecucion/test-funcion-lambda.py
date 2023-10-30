# Importar las bibliotecas necesarias
import json
import logging

# Configurar el registro (logger) para mostrar mensajes de registro de depuración
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Definir una clase llamada User para representar un usuario con nombre y edad
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


# Definir la función de controlador Lambda
def lambda_handler(event, context):
    # Registrar el evento de entrada para fines de depuración
    logger.info(event)

    # Obtener el método HTTP del evento
    http_method = event.get("httpMethod")

    # Verificar si el método HTTP es diferente de "POST"
    if http_method != "POST":
        # Si es diferente, devolver una respuesta con un código de estado 405 (Método no permitido)
        return {
            "statusCode": 405,
            "body": "Unsupported method",
            "headers": {"Content-Type": "application/json"},
        }

    # Analizar los datos del cuerpo del evento en un diccionario
    property_dict = json.loads(event.get("body"))

    # Crear una instancia de la clase User utilizando los datos del diccionario
    user = User(**property_dict)

    # Registrar los atributos del objeto User para fines de depuración
    logger.info(user.__dict__)

    # Devolver una respuesta con un código de estado 201 (Creado) y los datos del usuario en el cuerpo
    return {
        "statusCode": 201,
        "statusDescription": "201 CREATED",
        "isBase64Encoded": False,
        "headers": {"Content-Type": "application/json"},
        "body": str(user.__dict__),
    }
