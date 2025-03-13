import os
import hashlib
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from src.database import posts as db_posts
from src.schemas.posts import Posts, update_Posts

router = APIRouter()


@router.get("/api/posts", tags=["GET"], summary="Получить все посты")
async def get_all_posts():
    all_posts = await db_posts.get_posts()
    return all_posts


@router.get("/api/posts/user/{user_id}", tags=["GET"], summary="Получить посты пользователя")
async def get_posts_by_user(
    user_id: int, 
    post_id: int | None = Query(None, description="ID поста (опционально)"), 
    tag: str | None = Query(None, description="Фильтр по тегу (опционально)")
):
    result = await db_posts.get_posts_by_user(user_id, post_id, tag)
    return result

@router.post("/api/posts", tags=["POST"], summary="Создание публикации")
async def add_post(data: Posts):
    data = data.model_dump()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    title = data['title']
    content = data['content']
    username = data['username']
    user_id = data['user_id']
    category = data['category']
    tags = data['tags']
    image_url = data.get('image_url')
    createdAt = current_time

    await db_posts.create_database()
    added_post = await db_posts.add_posts(user_id, username, title, content, category, tags, createdAt, createdAt, image_url)
    if added_post.get("status"):
        return {"ok": True, "info": "Post added successfully"}
    raise HTTPException(status_code=400, detail="Error adding post")


@router.put("/api/posts", tags=["PUT"], summary="Обновить публикацию")
async def update_post(data: update_Posts):
    data = data.model_dump()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    post_id = data['id']
    user_id = data['user_id']
    title = data['title']
    content = data['content']
    category = data['category']
    tags = data['tags']
    updatedAt = current_time

    update_result = await db_posts.update_posts(user_id, title, content, category, tags, updatedAt, post_id)
    if update_result is True:
        updated_post = await db_posts.get_post(user_id, post_id)
        return {"ok": True, "info": "Post updated successfully", "post": updated_post}
    raise HTTPException(status_code=400, detail="Error updating post")


@router.delete("/api/posts", tags=["DELETE"], summary="Удалить публикацию")
async def delete_post(post_id: int = Query(...), user_id: int = Query(...)):
    delete_result = await db_posts.delete_posts(user_id, post_id)
    if delete_result is True:
        return {"ok": True, "info": "Post deleted successfully"}
    raise HTTPException(status_code=400, detail="Error deleting post")

@router.get("/api/posts/tag/{tag}", tags=["GET"], summary="Найти посты по тегу")
async def find_posts_by_tag(tag: str):
    result = await db_posts.find_posts_by_tag(tag)
    return result
