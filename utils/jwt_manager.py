import os
from typing import Optional
from fastapi import HTTPException
from jose import  JWTError, jwt

def create_token(data: dict) -> Optional[str]:
    """
    Crea un token JWT utilizando la clave secreta proporcionada en las variables de entorno.

    Args:
        data (dict): Datos que se incluirán en el token.

    Returns:
        Optional[str]: Token JWT generado o None si hay un error.
    """
    try:
        secret_key = os.getenv("SECRET_KEY")
        if secret_key is None:
            raise ValueError("SECRET_KEY not found in environment variables.")

        token: str = jwt.encode(data, key=secret_key, algorithm="HS256")
        return token

    except JWTError as e:
        raise HTTPException(status_code=500, detail=f"Error creating token: {e}")

def validate_token(token: str) -> Optional[dict]:
    """
    Valida un token JWT utilizando la clave secreta proporcionada en las variables de entorno.

    Args:
        token (str): Token JWT a validar.

    Returns:
        Optional[dict]: Datos extraídos del token o None si la validación falla.
    """
    try:
        secret_key = os.getenv("SECRET_KEY")
        if secret_key is None:
            raise ValueError("SECRET_KEY not found in environment variables.")

        data: dict = jwt.decode(token, key=secret_key, algorithms=["HS256"])
        return data

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Error validating token: {e}")
