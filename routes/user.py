from fastapi import APIRouter, Depends
from models.user import  UserLogin, UserUpdate, UserUpdateMe
from controllers.user_controller import delete_user, update_user, update_me
from middlewares.oauth2_deps import get_current_user, get_current_active_admin

user_router = APIRouter()
    
#Private Routes with JWT
@user_router.get("/profile")
async def profile(current_user: UserLogin = Depends(get_current_user)):
    return current_user

# Define la ruta con un parámetro de ruta "id"
@user_router.delete("/delete/{id}", description="Delete or deactivate a user. Requires admin or superuser privileges.")
def delete(id: int, current_user: UserLogin = Depends(get_current_active_admin)):
    return delete_user(id)

# Define la ruta de actualización para el usuario actual
@user_router.put("/update/me", description="Update user's own data. Requires authentication.")
def update_current_user(user_update: UserUpdateMe, current_user: UserLogin = Depends(get_current_user)):
    return update_me(user_update)

# # Define la ruta de actualización para admin/superuser
# @user_router.put("/update/{id}", description="Update role and active/inactive status of another user. Requires admin or superuser privileges.")
# def update_user_by_admin(id: int, user_update: UserUpdate, current_user: UserLogin = Depends(get_current_user)):
#     return update_user(id, user_update)