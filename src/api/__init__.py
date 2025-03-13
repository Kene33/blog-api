from fastapi import APIRouter
from src.api.posts_2 import router as posts_router
from src.api.users import router as users_router

api_router = APIRouter()

api_router.include_router(posts_router)
api_router.include_router(users_router)