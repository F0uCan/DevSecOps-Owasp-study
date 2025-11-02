import sqlite3
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# --- Database Setup ---
# This function creates a 'vulnerable.db' file with sample data
def setup_database():
    conn = sqlite3.connect('vulnerable.db')
    cursor = conn.cursor()
    # Drop table if it exists to ensure a clean start
    cursor.execute("DROP TABLE IF EXISTS users")
    # Create a users table
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)
    # Insert some sample data
    users_to_add = [
        (1, 'alice', 'user'),
        (2, 'bob', 'user'),
        (3, 'admin', 'admin')
    ]
    cursor.executemany("INSERT INTO users (id, username, role) VALUES (?, ?, ?)", users_to_add)
    conn.commit()
    conn.close()

# --- FastAPI App ---
app = FastAPI()

@app.on_event("startup")
def on_startup():
    # This function runs when the server starts
    setup_database()

@app.get("/users/search")
def search_user(username: str):
    """
    VULNERABLE ENDPOINT!
    It searches for a user by building a raw SQL query with user input.
    """
    conn = sqlite3.connect('vulnerable.db')
    conn.row_factory = sqlite3.Row # This helps convert rows to dict-like objects
    cursor = conn.cursor()

    # VULNERABILITY: User input is directly formatted into the query string.
    # This is highly insecure.
    query = f"SELECT id, username, role FROM users WHERE username = '{username}'"
    
    try:
        cursor.execute(query) # An attacker's payload is executed here
        result = cursor.fetchall()
        users = [dict(row) for row in result]
        return JSONResponse(content=users)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        conn.close()