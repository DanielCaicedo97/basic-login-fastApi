import os
from dotenv import load_dotenv
from config.db_config import get_session
from models.user import User
from models.enums.role_enum import RoleEnum

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def init():
    db = get_session()
    # Creamos un nuevo usuario con el rol de superusuario usando variables de entorno
    
    superuser = User(
        name=os.getenv("SUPERUSER_NAME"),
        email=os.getenv("SUPERUSER_EMAIL"),
        password=os.getenv("SUPERUSER_PASSWORD"),
        role=RoleEnum.SUPERUSER.value
    )
    db.add(superuser)
    db.commit()
    db.close()

if __name__ == "__main__":
    init()

