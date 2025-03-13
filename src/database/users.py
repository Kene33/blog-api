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


