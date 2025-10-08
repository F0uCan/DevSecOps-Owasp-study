from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict
from passlib.context import CryptContext

# --- 1. SETUP: Configure passlib to use bcrypt ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- In-memory "database" ---
db_users: Dict[str, dict] = {}

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str

app = FastAPI()

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
    """
    FIXED: This endpoint now uses a strong hashing algorithm.
    """
    if user.username in db_users:
        raise HTTPException(status_code=400, detail="Username already exists")

    # --- 2. FIX: Replace weak MD5 with strong bcrypt hashing ---
    hashed_password = pwd_context.hash(user.password)
    
    db_users[user.username] = {
        "password_hash": hashed_password,
        "full_name": user.full_name
    }
    return {"message": f"User {user.username} registered successfully."}

@app.get("/admin/users/all")
def get_all_users_data():
    return db_users