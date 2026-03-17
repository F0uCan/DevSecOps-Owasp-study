from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users_db = {"admin": "SuperSecret!", "john": "password123"}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    """
    VULNERABLE: No logging at all!
    Failed login attempts, suspicious activity, and successful logins
    are completely invisible. An attacker can brute-force passwords
    and nobody will ever know.
    """
    if users_db.get(data.username) != data.password:
        # No log of the failed attempt — the attacker is invisible
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # No log of successful login — no audit trail
    return {"message": "Login successful", "token": f"token_{data.username}"}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    """
    VULNERABLE: A destructive action with ZERO logging.
    If an attacker gains access and deletes all users,
    there's no way to know what happened, when, or by whom.
    """
    # No log of this critical action
    return {"message": f"User {user_id} deleted"}

@app.get("/api/admin/export-database")
def export_database():
    """
    VULNERABLE: Sensitive data export with no audit log.
    A data breach can happen and go undetected for months.
    """
    # No log of who exported the data
    return {"data": "All user records exported", "records": 15000}
