from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import event
from utils.generate_id import generate_id
import bcrypt

from models.enums.role_enum import RoleEnum
class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)
    
    def check_password(user, password_from_form: str) -> bool:
        hashed_password = bcrypt.hashpw(password_from_form.encode('utf-8'), user.salt.encode('utf-8')).decode('utf-8')
        return hashed_password == user.password

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    password: str
    token: str = Field(default=generate_id())
    salt: Optional[str] = Field(default=None)
    role: Optional[int] = Field(default=RoleEnum.OPERATOR.value)
    
# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Test Name",
                "email": "test@email.com",
                "password": "secret_Password"
            }
        }

class UserCreateOpen(SQLModel):
    email: str
    password: str
    full_name: str

# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int

# Properties to receive via API on Login
class UserLogin(SQLModel,table=False):
    id: int
    email: str
    name: str
    token: str
    role: int = RoleEnum
    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@email.com",
                "password": "secret_Password"
            }
        }

class UserUpdate(UserBase):
    email: Optional[str] 
    password: Optional[str]
    role: Optional[str] 
    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@email.com",
                "password": "secret_Password_updated",
                "role": RoleEnum.ADMIN
            }
        }

class UserUpdateMe(SQLModel):
    full_name: Optional[str]
    email: Optional[str]


def hash_password_listener(mapper, connection, target):
    if target.password:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(target.password.encode("utf-8"), salt)
        target.password = hashed_password.decode("utf-8")  # Almacena el hash como una cadena
        target.salt = salt.decode("utf-8")  # Almacena el salt como una cadena

# Escucha el evento before_insert en la clase User
event.listen(User, 'before_insert', hash_password_listener)