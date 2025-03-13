from fastapi import APIRouter, Depends, HTTPException, Response
from authx import AuthX, AuthXConfig

from src.database.posts import *
from src.schemas.users import UserLoginSchema

router = APIRouter()
config = AuthXConfig()
config.JWT_SECRET_KEY = "secret_12345_key"
config.JWT_ACCESS_COOKIE_NAME = "jwt_key"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

@router.post("/login")
async def login(creds: UserLoginSchema, response: Response):
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401)

### dependencies=[Depends(security.access_token_required)]

