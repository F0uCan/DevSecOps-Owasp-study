from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict

# --- In-memory "database" simulation ---
# The key is the username, the value is the user's data.
db_users: Dict[str, dict] = {}

# --- Pydantic Models ---
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str

# --- FastAPI Application ---
app = FastAPI()

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
    """
    VULNERABILITY HERE!
    The user's password is saved directly to the database
    in plaintext, without any kind of hashing or encryption.
    """
    if user.username in db_users:
        raise HTTPException(status_code=400, detail="Username already exists")

    # The password is saved exactly as it was received.
    db_users[user.username] = {
        "password": user.password,
        "full_name": user.full_name
    }
    return {"message": f"User {user.username} registered successfully."}


@app.get("/admin/users/all")
def get_all_users_data():
    """
    This is an "admin" endpoint that simulates a data breach.
    It exposes the complete contents of our database.
    """
    return db_users