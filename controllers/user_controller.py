from fastapi import status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from services.api.user_service_api import UserServiceApi
from models.user import User
from utils.jwt_manager import create_token, validate_token

user_service = UserServiceApi()
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")

def register_user(user: User):
    result = user_service.get_one_by_email(user.email)
    if result:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "User Already exist"})
    
    user_service.save(user)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User created"})

def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = user_service.get_one_by_email(form_data.username)
    if not user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Incorrect username or password"})
    
    if(User.check_password(user,form_data.password)):
        user_data = {
                "id":  user.id,
                "name": user.name,
                "email": user.email,
            }
        data = {
            "message": "User authenticated",
            "user" : user_data,
            "access_token": create_token(user_data),
            "token_type": "bearer"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=data)

    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Incorrect password"})


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        data = validate_token(token)
        if data is None:
            raise credentials_exception

        user = user_service.get_one_by_email(data.get("email"))
        if user is None:
            raise credentials_exception

        return data

    except Exception as e:
        raise credentials_exception from e


def delete_user():
    pass