from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from controllers.user_controller import register_user, authenticate_user
from models.user import UserCreate

login_router = APIRouter()

@login_router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return authenticate_user(form_data)

#Public Routes
@login_router.post("/register") 
def register(user: UserCreate):
    return register_user(user)
