import aiosqlite
import json

from src.schemas.users import LoginRequest, RegisterRequest

DATABASE = "src/database/users.db"

async def create_database() -> None:
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        createdAt TEXT NOT NULL,
        avatar_url TEXT
        )
        ''')
        await db.commit()

async def get_user_count():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            return row[0]
    
async def user_exists(username: str) -> bool:
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT 1 FROM users WHERE username = ?", (username,)) as cursor:
            return await cursor.fetchone() is not None

async def get_user(login: LoginRequest, hashed_pass):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute(
            f"SELECT id, username, avatar_url FROM users WHERE username = ? AND password = ?",
            (login.username, hashed_pass)
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return {"status": "false", "message": "Invalid credentials"}
            user = {"id": row[0], "username": row[1], "avatar_url": row[2]}
    
    return {"status": "true", "user": user}

async def get_user_all(username: str):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute(
            f"SELECT * FROM users WHERE username = ?",
            (username, )
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return {"status": "false", "message": "Invalid credentials"}
        return {"status": "true", "data": row}


async def add_user(reg: RegisterRequest, hashed_pass: str, id: int):
    username = reg.username
    async with aiosqlite.connect(DATABASE) as db:
        user_exist = await user_exists(username)
        if user_exist:
            return {"status": "false", "message": "User already exists"}

        await db.execute(
            f"INSERT INTO users (id, name, email, username, password, createdAt, avatar_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (id, reg.name, reg.email, reg.username, hashed_pass, reg.createdAt, reg.image_url)
        )
        await db.commit()

    return {"status": "ok", "message": "User registered successfully"}