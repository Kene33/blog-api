from datetime import datetime
import os
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.staticfiles import StaticFiles
from src.database import posts as db_posts
from src.schemas.posts import Posts

from src.api.users import security

router = APIRouter()

UPLOAD_DIR = "src/database/images/posts"
os.makedirs(UPLOAD_DIR, exist_ok=True)


router.mount("/media", StaticFiles(directory=UPLOAD_DIR), name="media")

@router.get("/api/posts", tags=["GET"], summary="Получить все посты") # dependencies=[Depends(security.access_token_required)]
async def get_all_posts():
    all_posts = await db_posts.get_posts()
    return all_posts


@router.get("/api/posts/user/{user_id}", tags=["GET"], summary="Получить посты пользователя", dependencies=[Depends(security.access_token_required)])
async def get_posts_by_user(
    user_id: int, 
    post_id: int | None = Query(None, description="ID поста (опционально)"), 
    tag: str | None = Query(None, description="Фильтр по тегу (опционально)")
):
    result = await db_posts.get_posts(user_id, post_id, tag)
    return result

@router.post("/api/posts", tags=["POST"], summary="Создание публикации", dependencies=[Depends(security.access_token_required)])
async def add_post(data: Posts): # file: UploadFile = File(None)
    data = data.model_dump()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    title = data['title']
    content = data['content']
    username = data['username']
    category = data['category']
    tags = data['tags']
    image_url = None
    createdAt = current_time

    await db_posts.create_database()
    added_post = await db_posts.add_posts(username, title, content, category, tags, createdAt, image_url)
    if added_post.get("status"):
        return {"ok": True, "info": "Post added successfully"}
    raise HTTPException(status_code=400, detail="Error adding post")


@router.delete("/api/posts", tags=["DELETE"], summary="Удалить публикацию", dependencies=[Depends(security.access_token_required)])
async def delete_post(post_id: int = Query(...), user_id: int = Query(...)):
    delete_result = await db_posts.delete_posts(user_id, post_id)
    if delete_result is True:
        return {"ok": True, "info": "Post deleted successfully"}
    raise HTTPException(status_code=400, detail="Error deleting post")

@router.get("/api/posts/tag/{tag}", tags=["GET"], summary="Найти посты по тегу")
async def find_posts_by_tag(tag: str):
    result = await db_posts.find_posts_by_tag(tag)
    return result
