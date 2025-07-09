import asyncio
import aiosqlite

DB_FILE = "my_database.db"

async def async_fetch_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All users:")
            for row in rows:
                print(row)
            return rows

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)
            return rows

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Setup DB (optional - for testing)
async def setup_database():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )""")
        await db.execute("DELETE FROM users")  # Clear existing data
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 30),
            ("Bob", 45),
            ("Charlie", 50),
            ("Diana", 22),
        ])
        await db.commit()

if __name__ == "__main__":
    # First run DB setup, then fetch concurrently
    asyncio.run(setup_database())        # Remove if not needed
    asyncio.run(fetch_concurrently())
