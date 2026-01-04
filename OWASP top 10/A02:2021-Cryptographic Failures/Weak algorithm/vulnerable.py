import hashlib
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict

# --- In-memory "database" ---
db_users: Dict[str, dict] = {}

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str

app = FastAPI()

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
    if user.username in db_users:
        raise HTTPException(status_code=400, detail="Username already exists")

    password_hash = hashlib.md5(user.password.encode()).hexdigest()
    
    db_users[user.username] = {
        "password_hash": password_hash,
        "full_name": user.full_name
    }
    return {"message": f"User {user.username} registered successfully."}

@app.get("/admin/users/all")
def get_all_users_data():
    return db_users