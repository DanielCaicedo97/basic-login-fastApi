import os
from fastapi import status, HTTPException
from jwt import encode, decode
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def create_token(data: dict):
    try:
        # Obtener la clave secreta desde las variables de entorno
        secret_key = os.getenv("SECRET_KEY")
        if secret_key is None:
            raise ValueError("SECRET_KEY not found in environment variables.")

        # Convertir la clave a bytes
        secret_key_bytes = secret_key


        # Generar el token
        token: str = encode(payload=data, key=secret_key_bytes, algorithm="HS256")
        return token

    except Exception as e:
        # Manejar cualquier excepción y mostrar un mensaje de error
        print(f"Error creating token: {e}")
        return None


def validate_token(token: str):

    try:
        secret_key = os.getenv("SECRET_KEY")
        if secret_key is None:
            raise ValueError("SECRET_KEY not found in environment variables.")

        # Convertir la clave a bytes
        secret_key_bytes = secret_key
        data: dict = decode(token, key=secret_key_bytes, algorithms=["HS256"])
        return data
    
    except Exception as e:
      # En lugar de lanzar una HTTPException aquí, simplemente devuelve None para indicar que la validación ha fallado
        print(f"Error validating token: {e}")
        return None
        


