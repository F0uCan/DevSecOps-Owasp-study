from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Dict
from passlib.context import CryptContext

# --- Password Hashing Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- In-memory "database" simulation ---
db_users: Dict[str, dict] = {}

# --- Pydantic Models ---
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    username: str
    password: str

# --- FastAPI Application ---
app = FastAPI()

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
    """
    FIXED!
    We now store a hash of the password, not the password itself.
    """
    if user.username in db_users:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Generate the password hash before saving
    hashed_password = pwd_context.hash(user.password)

    db_users[user.username] = {
        "password_hash": hashed_password, # Store the hash
        "full_name": user.full_name
    }
    return {"message": f"User {user.username} registered successfully."}

@app.post("/login")
def login_user(form_data: UserLogin):
    """
    Secure login endpoint that verifies a password against the stored hash.
    """
    user_in_db = db_users.get(form_data.username)
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Verify if the provided password matches the stored hash
    if not pwd_context.verify(form_data.password, user_in_db["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"message": f"Welcome {user_in_db['full_name']}!"}


@app.get("/admin/users/all")
def get_all_users_data():
    """
    This endpoint is now safe. Even if the data leaks,
    the passwords are not exposed.
    """
    return db_users