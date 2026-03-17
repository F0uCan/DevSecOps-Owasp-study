import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("auth")

app = FastAPI()

users_db = {"admin": "SuperSecret!"}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    """
    VULNERABLE TO LOG INJECTION!
    User input is placed directly into log messages without sanitization.
    An attacker can inject newline characters to forge log entries,
    hiding attacks or creating fake evidence.
    """
    if users_db.get(data.username) != data.password:
        # VULNERABILITY: data.username goes directly into the log.
        # An attacker can inject newlines (\n) to create fake log entries.
        logger.warning(f"Failed login attempt for user: {data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logger.info(f"Successful login for user: {data.username}")
    return {"message": "Login successful"}
