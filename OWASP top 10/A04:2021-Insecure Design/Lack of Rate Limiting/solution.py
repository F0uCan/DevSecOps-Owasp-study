from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

app = FastAPI()

users_db = {"admin": "secure123"}

# In-memory store for failed attempts (Use Redis in production!)
failed_attempts = {}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(data: LoginRequest, request: Request):
    """
    SECURE DESIGN: Implements a basic rate limiter/lockout.
    """
    client_ip = request.client.host
    
    # THE FIX: Check if this IP is currently "locked out"
    if failed_attempts.get(client_ip, 0) >= 3:
        raise HTTPException(
            status_code=429, 
            detail="Too many failed attempts. Please try again later."
            
        )

    if users_db.get(data.username) == data.password:
        failed_attempts[client_ip] = 0  # Reset counter on success
        return {"message": "Login successful"}
    
    # Increment the failure counter for this IP
    failed_attempts[client_ip] = failed_attempts.get(client_ip, 0) + 1
    
    raise HTTPException(status_code=401, detail="Invalid credentials")