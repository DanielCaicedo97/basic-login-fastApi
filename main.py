from fastapi import FastAPI
from middlewares.error_handler import ErrorHandler
from config.db_config import create_db_and_tables
from routes.user import user_router
from routes.login import login_router

app = FastAPI(
    title="Login API - Generic",
    version="0.0.1",
    openapi_url="/api/v1/login.json",  # Especifica la ruta de la documentación OpenAPI
    docs_url="/api/v1/docs",  # Cambia la ruta de la interfaz de documentación
)

create_db_and_tables()
app.add_middleware(ErrorHandler)

@app.get('/api/v1/', tags=["HOME"])
def Home():
    return "Here is Home to API"

# Incluir las rutas del router del usuario bajo /api/v1
app.include_router(login_router, prefix="/api/v1/login", tags=["Login"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])