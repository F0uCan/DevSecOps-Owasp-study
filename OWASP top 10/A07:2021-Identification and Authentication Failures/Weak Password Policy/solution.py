import re
import hashlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI()

users_db = {}

# A small list of the most common breached passwords.
# In production, use the Have I Been Pwned API (https://haveibeenpwned.com/API/v3)
COMMON_PASSWORDS = {"password", "123456", "password123", "admin", "qwerty",
                    "letmein", "welcome", "monkey", "dragon", "master"}

class RegisterRequest(BaseModel):
    username: str
    password: str

    # THE FIX: Enforce password policy at the model level
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 10:
            raise ValueError("Password must be at least 10 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        if v.lower() in COMMON_PASSWORDS:
            raise ValueError("This password is too common and has been found in data breaches")
        return v

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(data: RegisterRequest):
    """SECURE: Password is validated against a strong policy before registration."""
    if data.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # Store a hash, never the plaintext password
    hashed = hashlib.sha256(data.password.encode()).hexdigest()
    users_db[data.username] = hashed

    return {"message": f"User '{data.username}' registered successfully"}

@app.post("/login")
def login(data: LoginRequest):
    hashed = hashlib.sha256(data.password.encode()).hexdigest()
    if users_db.get(data.username) != hashed:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
