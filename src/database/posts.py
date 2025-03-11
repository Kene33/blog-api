import aiosqlite
import json

async def create_database(user_id: int) -> None:
    async with aiosqlite.connect('app/database/database.db') as db:
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS posts_{user_id} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT NOT NULL,
        tags JSON,
        createdAt TEXT NOT NULL,
        updatedAt TEXT NOT NULL
        )
        '''

        await db.execute(create_table_query)
        await db.commit()

async def check_user_exists(user_id: int) -> bool:
    table_name = f"posts_{user_id}"

    async with aiosqlite.connect('app/database/database.db') as db:
        async with db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)) as cursor:
            result = await cursor.fetchone()
            if result:
                return True
            
            return False

async def get_posts(user_id: int, posts_id: int = None, tag: str = None) -> dict:
    table_name = f"posts_{user_id}"

    async with aiosqlite.connect('app/database/database.db') as db:

        if posts_id:
            async with db.execute(f'SELECT * FROM {table_name} WHERE id = ?', (posts_id,)) as cursor:
                rows = await cursor.fetchone()
                return rows
        elif tag:
            async with db.execute(f'SELECT * FROM {table_name} WHERE tags LIKE ?', (tag,)) as cursor:
                rows = await cursor.fetchone()
                return rows
        else:
            async with db.execute(f'SELECT * FROM {table_name}') as cursor:
                rows = await cursor.fetchall()
                return rows
            
async def add_posts(user_id: int, title: str, content: str, category: str, tags: list, createdAt: int, updatedAt: int) -> bool:
    table_name = f"posts_{user_id}"
    try:
        async with aiosqlite.connect('app/database/database.db') as db:
            tags_json = json.dumps(tags)

            await db.execute(f'''
            INSERT INTO {table_name} (title, content, category, tags, createdAt, updatedAt) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, content, category, tags_json, createdAt, updatedAt))

            await db.commit()
        
            return True
    except:
        return False
    
async def update_posts(user_id: int, title: str, content: str, category: str, tags: list, updatedAt: int, post_id: int) -> dict:
    table_name = f"posts_{user_id}"

    try:
        async with aiosqlite.connect('app/database/database.db') as db:
            tags_json = json.dumps(tags)

            await db.execute(f'''
            UPDATE {table_name}
            SET title = ?, content = ?, category = ?, tags = ?, updatedAt = ?
            WHERE id = ?
            ''', (title, content, category, tags_json, updatedAt, post_id))

            await db.commit()

            return True
    except:
        return False

async def delete_posts(user_id: int, post_id: int) -> bool:
    table_name = f"posts_{user_id}"
    try:
        async with aiosqlite.connect('app/database/database.db') as db:
            await db.execute(f"DELETE FROM {table_name} WHERE id = ?", (post_id,))
            await db.commit()

            return True
    except:
        return False

async def find_posts_by_tag(tag: str, user_id: int = None) -> dict:
    async with aiosqlite.connect('app/database/database.db') as db:
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        async with db.execute(tables_query) as cursor:
            tables = await cursor.fetchall()
        
        results = []
        
        for table in tables:
            table_name = table[0]
            
            columns_query = f"PRAGMA table_info({table_name});"
            async with db.execute(columns_query) as col_cursor:
                columns = await col_cursor.fetchall()
                if any(col[1] == 'tags' for col in columns):
                    
                    query = f"SELECT * FROM {table_name} WHERE tags LIKE ?"
                    like_pattern = f'%{tag}%'
                    async with db.execute(query, (like_pattern,)) as search_cursor:
                        rows = await search_cursor.fetchall()
                        if rows:
                            results.extend(rows)

        return results
    


