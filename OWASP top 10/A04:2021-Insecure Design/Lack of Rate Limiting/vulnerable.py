from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Simulated DB
users_db = {"admin": "password123"}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    """
    VULNERABLE DESIGN: No Rate Limiting.
    An attacker can call this endpoint infinitely to brute-force the password.
    """
    if users_db.get(data.username) == data.password:
        return {"message": "Login successful"}
    
    # The lack of a delay or lockout is the design flaw
    raise HTTPException(status_code=401, detail="Invalid credentials")