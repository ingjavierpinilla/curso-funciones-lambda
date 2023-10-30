# Importar las bibliotecas necesarias
import json
import os

# Obtener el valor de la clave de la API desde una variable de entorno
API_KEY = os.getenv("api_key")


# Definir la función de controlador Lambda
def lambda_handler(event, context):
    # Obtener el valor de la clave de la API desde el evento de entrada
    api_key = event.get("api_key")

    # Verificar si la clave de la API proporcionada coincide con la clave almacenada
    if api_key != API_KEY:
        # Si no coincide, imprimir un mensaje de no autorizado y devolver una respuesta 401
        print(f"Unauthorized {event}")
        return {"statusCode": 401, "body": json.dumps("Unauthorized")}

    # Si la clave de la API coincide, devolver una respuesta 200 con un saludo
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
