from typing import Optional
import aiosqlite
import json

DATABASE = "src/database/database.db"


async def create_database() -> None:
    async with aiosqlite.connect(DATABASE) as db:
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT NOT NULL,
        tags TEXT,
        createdAt TEXT NOT NULL,
        image_url TEXT
        )
        '''

        await db.execute(create_table_query)
        await db.commit()


async def check_user_exists(user_id: int) -> bool:
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM posts WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return True

            return False

async def get_posts(user_id: Optional[int] = None, post_id: Optional[int] = None, tag: Optional[str] = None):
    if user_id:
        base_query = "SELECT * FROM posts WHERE user_id = ?"
    else:
        base_query = "SELECT * FROM posts"
        async with aiosqlite.connect(DATABASE) as db:
            async with db.execute(base_query) as cursor:
                rows = await cursor.fetchall()
                return rows
    params = [user_id]

    if post_id is not None:
        base_query += " AND id = ?"
        params.append(post_id)
    if tag is not None:
        base_query += " AND tags LIKE ?"
        params.append(f"%{tag}%")

    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute(base_query, tuple(params)) as cursor:
            rows = await cursor.fetchall()
            return rows

async def add_posts(username: str, title: str, content: str, category: str, tags: list, createdAt: int, image_url: str) -> bool:
    try:
        async with aiosqlite.connect(DATABASE) as db:
            tags_json = json.dumps(tags)

            await db.execute(f'''
            INSERT INTO posts (username, title, content, category, tags, createdAt, image_url) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, title, content, category, tags_json, createdAt, image_url))

            await db.commit()

            return {"status": True}
    except Exception as e:
        return {"status": False, "info": e}


async def update_posts(user_id: int, title: str, content: str, category: str, tags: list, updatedAt: int, post_id: int) -> dict:
    try:
        async with aiosqlite.connect(DATABASE) as db:
            tags_json = json.dumps(tags)

            await db.execute(f'''
            UPDATE posts
            SET title = ?, content = ?, category = ?, tags = ?, updatedAt = ?
            WHERE id = ? AND user_id = ?
            ''', (title, content, category, tags_json, updatedAt, post_id, user_id))

            await db.commit()

            return True
    except:
        return False

async def delete_posts(user_id: int, post_id: int) -> bool:
    try:
        async with aiosqlite.connect(DATABASE) as db:
            await db.execute(f"DELETE FROM posts WHERE id = ? AND user_id = ?", (post_id, user_id))
            await db.commit()

            return True
    except:
        return False

async def find_posts_by_tag(tag: str, user_id: int = None) -> dict:
    async with aiosqlite.connect(DATABASE) as db:
        if user_id:
            query = "SELECT * FROM posts WHERE tags LIKE ? AND user_id = ?"
        else:
            query = "SELECT * FROM posts WHERE tags LIKE ?"
        param = f"%{tag}%"
        async with db.execute(query, (param,)) as cursor:
            rows = await cursor.fetchall()
            return rows

    


