import sqlite3
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# --- Database Setup ---
# (This setup function is identical to the vulnerable one,
#  but it creates a separate 'solution.db' file)
def setup_database():
    conn = sqlite3.connect('solution.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)
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
    setup_database()

@app.get("/users/search")
def search_user(username: str):
    """
    SECURE ENDPOINT!
    It uses query parameters to prevent SQL Injection.
    """
    conn = sqlite3.connect('solution.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # THE FIX: The query string is a template with a '?' placeholder.
    query = "SELECT id, username, role FROM users WHERE username = ?"
    
    # The user input is passed as a separate tuple.
    # The database driver safely sanitizes this input.
    try:
        cursor.execute(query, (username,)) # The (username,) is a tuple
        result = cursor.fetchall()
        users = [dict(row) for row in result]
        return JSONResponse(content=users)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        conn.close()