from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Simulated database
users_db = {}

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(data: RegisterRequest):
    """
    VULNERABLE: No password policy enforcement.
    Accepts any password, including '1', 'a', or empty-like strings.
    """
    if data.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # VULNERABILITY: No validation on password strength!
    # No minimum length, no complexity requirements, no breach checking.
    users_db[data.username] = data.password

    return {"message": f"User '{data.username}' registered successfully"}

@app.post("/login")
def login(data: LoginRequest):
    """Standard login — the weakness is in registration, not here."""
    if users_db.get(data.username) != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "token": f"fake_token_{data.username}"}

@app.get("/users/count")
def user_count():
    """Utility endpoint to verify registered users."""
    return {"total_users": len(users_db)}
