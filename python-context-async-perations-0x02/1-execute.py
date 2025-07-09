import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.connection = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Example usage
if __name__ == "__main__":
    db_file = "my_database.db"  # Make sure this DB exists

    # Ensure the table and data exists
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
        """)
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
                ("Alice", 30),
                ("Bob", 20),
                ("Charlie", 35),
            ])
            conn.commit()

    # Use the ExecuteQuery context manager
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(db_file, query, params) as results:
        for row in results:
            print(row)
