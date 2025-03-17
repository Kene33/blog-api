import hashlib
import aiosqlite

DATABASE = "src/database/users.db"


async def create_database() -> None:
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            createdAt TEXT NOT NULL,
            posts_count INT DEFAULT 0,
            avatar_url TEXT
        )
        ''')
        await db.commit()

async def get_user(username: str) -> bool:
        async with aiosqlite.connect(DATABASE) as db:
            async with db.execute("SELECT * FROM users WHERE username = ?", (username,)) as cursor:
                result = await cursor.fetchone()
                if result: return {"ok": True, "user_info": result}

                return {"ok": False, "message": "Cant find user"}

async def add_user(username: str, password: str, createdAt: str = None, posts_count: int = 0, avatar_url: str = None):
    async with aiosqlite.connect(DATABASE) as db:
        try:
            await db.execute("""
                INSERT INTO users (username, password, createdAt, posts_count, avatar_url) VALUES (?, ?, ?, ?, ?)
            """, (username, password, createdAt, posts_count, avatar_url))
            await db.commit()
            return {"ok": True, "message": "User added successfully"}
        except aiosqlite.IntegrityError:
            return {"ok": False, "message": "Username is already exists"}

async def posts_counter(username: str):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("UPDATE users SET posts_count = posts_count + 1 WHERE username = ?", (username,))
        await db.commit()
