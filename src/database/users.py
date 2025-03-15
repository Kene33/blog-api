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
        avatar_url TEXT
        )
        ''')
        await db.commit()

async def user_exists(username: str) -> bool:
        async with aiosqlite.connect(DATABASE) as db:
            async with db.execute("SELECT 1 FROM users WHERE username = ?", (username,)) as cursor:
                result = await cursor.fetchone()
                if result:
                    return True
                else:
                    return False


async def add_user(username: str, password: str, createdAt: str = None, avatar_url: str = None):
    async with aiosqlite.connect(DATABASE) as db:
        try:
            await db.execute("""
                INSERT INTO users (username, password, createdAt, avatar_url) VALUES (?, ?, ?, ?)
            """, (username, password, createdAt, avatar_url))
            await db.commit()
            return {"ok": True, "message": "User added successfully"}
        except aiosqlite.IntegrityError:
            return {"ok": False, "message": "Username is already exists"}

