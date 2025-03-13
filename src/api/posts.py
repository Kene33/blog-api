import os
import hashlib

from fastapi import APIRouter
from datetime import datetime

from src.database import posts, user
from src.schemas.posts import Posts, update_Posts
from src.schemas.users import LoginRequest, RegisterRequest

router = APIRouter()


@router.get("/api/posts")
async def get_all_posts():
    all_posts = await posts.get_all_posts()
    return all_posts

@router.post("/api/posts/{user_id}", tags=["POST"], summary="Добавление публикации")
async def add_posts(data: Posts, user_id: int):
    data = data.model_dump()

    current_time = datetime.now()

    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    title = data['title']
    content = data['content']
    category = data['category']
    tags = data['tags']
    createdAt = formatted_time
    updatedAt = formatted_time
    img = data['image_url']

    user_exists = await posts.check_user_exists(user_id)
    if not user_exists:
        await posts.create_database(user_id)
        await posts.add_posts(
            user_id, title, content, category, tags, createdAt, updatedAt, img
            )
    else:
        await posts.add_posts(
            user_id, title, content, category, tags, createdAt, updatedAt, img
            )
        
    return {"ok": True, "info": "Task added successfully"}


@router.put("/api/posts/{user_id}", summary="Обновить публикацию", tags=["PUT"])
async def update_posts(data: update_Posts, user_id: int):
    data = data.model_dump()

    current_time = datetime.now()

    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    id = data['id']
    title = data['title']
    content = data['content']
    category = data['category']
    tags = data['tags']
    updatedAt = formatted_time

    update_info = await posts.update_posts(
        user_id, title, content, category, tags, updatedAt, id
    )
    if update_info == True:
        updated_post = await posts.get_posts(user_id, id)
        return {"ok": True, "info": "Task updated successfully", "posts": updated_post}
    else:
        return {"ok": False, "info": "Some problem with updated posts"}
    

@router.get("/api/posts/{user_id}", tags=["GET"], summary="Получение публикации", description="user_id обязательное поле для получения всех публикаций пользователя.\npost_id выдает публикацию пользователя по его айди.\ntag выдает публикации пользователя по тегам.")
async def get_posts(user_id: int, post_id: int | None = None, tag: str | None = None):
    posts = await posts.get_posts(user_id, post_id, tag)
    return posts


@router.delete("/api/delete_posts/{user_id}", tags=["DELETE"], summary="Удаление публикации", description="post_id айди публикации для удаления.")
async def delete_posts(post_id: int, user_id: int):
    delete_info = await posts.delete_posts(user_id, post_id)

    if delete_info == True:
        return {"ok": True, "info": "Task deleted successfully"}
    else:
        return {"ok": False, "info": "Some problem with deleted posts"}


@router.get("/api/posts/{tag}", tags=["GET"], summary="Получение всех публикаций по тегам")
async def find_posts(tag: str):
    result = await posts.find_posts_by_tag(tag)
    return result