from fastapi import APIRouter
from datetime import datetime

from src.database import db
from src.schemas.posts import Posts, update_Posts

router = APIRouter()

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

    user_exists = await db.check_user_exists(user_id)
    if not user_exists:
        await db.create_database(user_id)
        await db.add_posts(
            user_id, title, content, category, tags, createdAt, updatedAt
            )
    else:
        await db.add_posts(
            user_id, title, content, category, tags, createdAt, updatedAt
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

    update_info = await db.update_posts(
        user_id, title, content, category, tags, updatedAt, id
    )
    if update_info == True:
        updated_post = await db.get_posts(user_id, id)
        return {"ok": True, "info": "Task updated successfully", "posts": updated_post}
    else:
        return {"ok": False, "info": "Some problem with updated posts"}
    

@router.get("/api/posts/{user_id}", tags=["GET"], summary="Получение публикации", description="user_id обязательное поле для получения всех публикаций пользователя.\npost_id выдает публикацию пользователя по его айди.\ntag выдает публикации пользователя по тегам.")
async def get_posts(user_id: int, post_id: int | None = None, tag: str | None = None):
    posts = await db.get_posts(user_id, post_id, tag)
    return posts


@router.delete("/api/delete_posts/{user_id}", tags=["DELETE"], summary="Удаление публикации", description="post_id айди публикации для удаления.")
async def delete_posts(post_id: int, user_id: int):
    delete_info = await db.delete_posts(user_id, post_id)

    if delete_info == True:
        return {"ok": True, "info": "Task deleted successfully"}
    else:
        return {"ok": False, "info": "Some problem with deleted posts"}


@router.get("/api/posts/{tag}", tags=["GET"], summary="Получение всех публикаций по тегам")
async def find_posts(tag: str):
    result = await db.find_posts_by_tag(tag)
    return result