import aiosqlite
import json

DATABASE = "src/database/database.db"


async def create_database() -> None:
    async with aiosqlite.connect(DATABASE) as db:
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT NOT NULL,
        tags JSON,
        createdAt TEXT NOT NULL,
        updatedAt TEXT NOT NULL,
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

async def get_posts(user_id: int = None, posts_id: int = None, tag: str = None) -> dict:
    async with aiosqlite.connect(DATABASE) as db:
        if posts_id and user_id:
            async with db.execute(f'SELECT * FROM posts WHERE id = ? AND user_id = ?', (posts_id, user_id)) as cursor:
                rows = await cursor.fetchone()
                return rows
        elif tag and user_id:
            async with db.execute(f'SELECT * FROM posts WHERE tags LIKE ? AND user_id = ?', (tag, user_id)) as cursor:
                rows = await cursor.fetchone()
                return rows
        elif user_id:
            async with db.execute(f'SELECT * FROM posts AND user_id = ?') as cursor:
                rows = await cursor.fetchall()
                return rows
        else:
            async with db.execute(f'SELECT * FROM posts') as cursor:
                rows = await cursor.fetchall()
                return rows

async def add_posts(user_id: int, title: str, content: str, category: str, tags: list, createdAt: int, updatedAt: int, image_url: str) -> bool:
    try:
        async with aiosqlite.connect(DATABASE) as db:
            tags_json = json.dumps(tags)

            await db.execute(f'''
            INSERT INTO posts (user_id, title, content, category, tags, createdAt, updatedAt, image_url) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, user_id, content, category, tags_json, createdAt, updatedAt, image_url))

            await db.commit()
        
            return True
    except:
        return False

    
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

    


