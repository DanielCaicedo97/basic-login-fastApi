from common.base_service_impl import BaseServiceImpl
from models.user import User
from typing import Optional
from config.db_config import get_session
from sqlmodel import select

class UserServiceApi(BaseServiceImpl[User, int]):
    def __init__(self):
        self.model = User  # Añadir esta línea para indicar el modelo que maneja este servicio

    def get_one_by_email(self, email: str):
        with get_session() as db:
            statement = select(self.model).where(self.model.email == email)
            result = db.exec(statement).first()
            if result != None:
                return result
            else:
                return None
