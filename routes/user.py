from fastapi import APIRouter, Body, Depends, Request
from models.user import User, UserLogin
from controllers.user_controller import register_user, authentication, profile_user, delete_user
from middlewares.jwt_middleware import JWTBearer
user_router = APIRouter()

#Public Routes
@user_router.post("/register") 
def register(user: User):
    return register_user(user)

@user_router.post("/login")
def login(login: UserLogin):
    return authentication(login.email,login.password)

#Private Routes with JWT
@user_router.get("/profile", dependencies=[Depends(JWTBearer())])
def profile():
    return profile_user()

#Private Routes with JWT
@user_router.delete("/delete", dependencies=[Depends(JWTBearer())])
def delete():
    return delete_user()