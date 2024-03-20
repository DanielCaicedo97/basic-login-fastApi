from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from utils.jwt_manager import  validate_token
from services.api.user_service_api import UserServiceApi
from models.user import User, UserLogin
from models.enums.role_enum import RoleEnum
user_service = UserServiceApi()
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserLogin:
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
        user = UserLogin.model_validate(user, update={"token": token})
        return user

    except Exception as e:
        raise credentials_exception from e
    

def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.role == RoleEnum.SUPERUSER.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_active_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.role <= RoleEnum.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="The user doesn't have enough privileges"
        )
    return current_user