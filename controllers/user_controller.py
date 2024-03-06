from fastapi import status
from fastapi.responses import JSONResponse

from services.api.user_service_api import UserServiceApi
from models.user import User
from utils.jwt_manager import create_token

user_service = UserServiceApi()

def register_user(user: User):
    result = user_service.get_one_by_email(user.email)
    if result:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User Already exist"})
    
    user_service.save(user)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created"})

def authentication(email: str, password: str):
    
    user = user_service.get_one_by_email(email)
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User does not exist"})
    

    if(User.check_password(user,password)):
        user_data = {
                "id":  user.id,
                "name": user.name,
                "email": user.email,
            }
        data = {
            "message": "User authenticated",
            "user" : user_data,
            "token": create_token(user_data),
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=data)

    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Incorrect password"})

def profile_user():
    pass

def delete_user():
    pass