from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import event
from utils.generate_id import generate_id
import bcrypt

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    email: str
    token: str = Field(default=generate_id())
    password: str
    salt: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Test Name",
                "email": "test@email.com",
                "password": "secret_Password"
            }
        }

    def check_password(user, password_from_form: str) -> bool:
        hashed_password = bcrypt.hashpw(password_from_form.encode('utf-8'), user.salt.encode('utf-8')).decode('utf-8')
        return hashed_password == user.password

# Properties to receive via API on Login
class UserLogin(SQLModel,table=False):
    email: str
    password: str
    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@email.com",
                "password": "secret_Password"
            }
        }


def hash_password_listener(mapper, connection, target):
    if target.password:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(target.password.encode("utf-8"), salt)
        target.password = hashed_password.decode("utf-8")  # Almacena el hash como una cadena
        target.salt = salt.decode("utf-8")  # Almacena el salt como una cadena

# Escucha el evento before_insert en la clase User
event.listen(User, 'before_insert', hash_password_listener)



