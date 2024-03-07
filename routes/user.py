from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
from controllers.user_controller import register_user, authenticate_user, get_current_user, delete_user

user_router = APIRouter()

#Public Routes
@user_router.post("/register") 
def register(user: User):
    return register_user(user)

@user_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return authenticate_user(form_data)
    
#Private Routes with JWT
@user_router.get("/profile")
async def profile(current_user: User = Depends(get_current_user)):
    return current_user

#Private Routes with JWT
@user_router.delete("/delete")
def delete():
    return delete_user()