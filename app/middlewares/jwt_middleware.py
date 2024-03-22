from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer

from utils.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data == None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"Error validating token"})
