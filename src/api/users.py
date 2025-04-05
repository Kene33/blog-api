from datetime import datetime, timedelta
from fastapi import APIRouter, Response
from authx import AuthX, AuthXConfig

from src.database import users as users_db
from src.schemas.users import UserLoginSchema

router = APIRouter()

config = AuthXConfig()
config.JWT_SECRET_KEY = "secret_12345_key1"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_CSRF_METHODS = []

security = AuthX(config=config)

# dependencies=[Depends(security.access_token_required)]
@router.get("/api/user/{username}")
async def user_page(username: str):
    user_exist = await users_db.get_user(username)
    if user_exist:
        return {"ok": True, "user": user_exist}

    return {"ok": False, "message": "Cant find user"}


@router.post("/api/auth/login")
async def login(creds: UserLoginSchema, response: Response):
    user_exist = await users_db.get_user(creds.username)
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="123456499", expiry=timedelta(hours=12))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token, samesite="lax", httponly=True)
        return {"ok": True, "access_token": token}

    if user_exist:
        token = security.create_access_token(uid=creds.username, expiry=timedelta(hours=12))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token, samesite="lax", httponly=True)
        return {"ok": True, "access_token": token, "username": creds.username}
    
    return {"ok": False, "message": "Wrong password or username"}

@router.post("/api/auth/register")
async def register(creds: UserLoginSchema): # file: UploadFile
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_exists = await users_db.get_user(creds.username)
    if user_exists["ok"]: return {"ok": False, "message": "Username already exists"}

    user = await users_db.add_user(creds.username, creds.password, current_time)
    return user