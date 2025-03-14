from datetime import timedelta
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

@router.post("/login")
async def login(creds: UserLoginSchema, response: Response):
    user_exist = await users_db.user_exists(creds.username)

    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="136474", expiry=timedelta(hours=12))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token, samesite="lax", httponly=True)
        return {"access_token": token}
    
    return {"ok": False, "message": "Username is already exists"}

### dependencies=[Depends(security.access_token_required)]

@router.post("/register")
async def register(creds: UserLoginSchema): # file: UploadFile
    #avatar_url = f"{creds.username}:{file.filename}"
    user_exists = await users_db.user_exists(creds.username)
    createdAt = "01.01.25"
    if user_exists: return {"ok": False, "message": "Username already exists"}

    user = await users_db.add_user(creds.username, creds.password, createdAt)
    return user
