from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from services.api.user_service_api import UserServiceApi
from models.user import User, UserCreate, UserUpdate, UserUpdateMe
from models.token import Token
from models.enums.role_enum import RoleEnum
from utils.jwt_manager import create_token

user_service = UserServiceApi()

def register_user(user_create: UserCreate):

    result = user_service.get_one_by_email(user_create.email)
    if result != None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User Already exist"})
    
    user = User.model_validate(user_create, update= {"role": RoleEnum.OPERATOR})
    user_service.save(user)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created"})

def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends())-> Token:
    
    user = user_service.get_one_by_email(form_data.username)
    if not user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Incorrect username or password"})
    
    if(User.check_password(user,form_data.password)):
        user_data = {
                "id":  user.id,
                "name": user.name,
                "email": user.email,
            }
        data = Token(
            access_token = create_token(user_data),
            )
        data = jsonable_encoder(data)
        return JSONResponse(status_code=status.HTTP_200_OK, content=data)

    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Incorrect password"})

def delete_user(id: int):
    user = user_service.get_one_by_id(id)
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})
    user_service.delete(id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"id": id, "message": "User deleted successfully"})

def update_user(id: int, user_update: UserUpdate):
    user = user_service.get_one_by_id(id)
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})
    user_data =  user_update.model_dump(exclude_unset=True)
    return user_data

def update_me(user_update: UserUpdateMe):
    return user_update