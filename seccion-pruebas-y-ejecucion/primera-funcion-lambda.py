# Importar las bibliotecas necesarias
import json
from dataclasses import asdict

# Importar la clase User del módulo user_class
from user_class import User

# Definir una constante PATH que representa el segmento de la ruta esperado
PATH: str = "users"

# Crear un diccionario simulado (fake_db) para almacenar objetos User con identificadores (claves)
fake_db: dict = dict(
    [(0, User("Peter", 31)), (1, User("Tom", 22)), (2, User("Ana", 28))]
)


# Definir la función de controlador Lambda
def lambda_handler(event, context):
    # Obtener el segmento de la ruta desde el evento
    path: str = event.get("requestContext").get("http").get("path")

    # Verificar si el segmento de la ruta no coincide con PATH
    if path.split("/")[1] != PATH:
        return {"statusCode": 404, "body": json.dumps(f"Path not found")}

    # Obtener el método HTTP desde el evento
    method: str = event.get("requestContext").get("http").get("method")

    if method == "GET":
        # Procesar una solicitud GET
        id_to_get: int = int(path.split("/")[-1])
        user = fake_db.get(id_to_get)
        if not user:
            return {"statusCode": 204, "body": f"User {id_to_get} doesn't exist"}
        return {"statusCode": 200, "body": asdict(user)}

    elif method == "POST":
        # Procesar una solicitud POST
        id_to_create: int = int(path.split("/")[-1])
        user = fake_db.get(id_to_create)
        if user:
            return {"statusCode": 409, "body": f"User {id_to_create} already exists"}
        body: dict = json.loads(event.get("body"))
        user = User(body.get("name"), body.get("age"))
        fake_db[id_to_create]: User = user
        return {"statusCode": 201, "body": asdict(user)}

    elif method == "PUT":
        # Procesar una solicitud PUT
        id_to_update: int = int(path.split("/")[-1])
        user = fake_db.get(id_to_update)

        if not user:
            return {"statusCode": 409, "body": f"User {id_to_update} doesn't exist"}
        body: dict = json.loads(event.get("body"))
        user = User(body.get("name"), body.get("age"))
        fake_db[id_to_update]: User = user
        return {"statusCode": 201, "body": asdict(user)}

    elif method == "DELETE":
        # Procesar una solicitud DELETE
        id_to_delete: int = int(path.split("/")[-1])
        user = fake_db.get(id_to_delete)

        if not user:
            return {"statusCode": 204, "body": f"User {id_to_delete} doesn't exist"}
        user: User = fake_db.pop(id_to_delete)
        return {"statusCode": 200, "body": asdict(user)}
    else:
        # Devolver una respuesta si se recibe un método HTTP no compatible
        return {"statusCode": 405, "body": "Unsupported method"}
