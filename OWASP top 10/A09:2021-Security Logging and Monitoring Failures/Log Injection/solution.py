import logging
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("auth")

app = FastAPI()

users_db = {"admin": "SuperSecret!"}

def sanitize_for_log(value: str) -> str:
    """
    THE FIX: Sanitize user input before placing it in log messages.
    - Remove newlines and carriage returns (prevents log forging)
    - Truncate to prevent log flooding
    - Remove control characters
    """
    # Remove newlines, carriage returns, and other control characters
    sanitized = re.sub(r'[\n\r\t\x00-\x1f\x7f-\x9f]', '', value)
    # Truncate to reasonable length
    return sanitized[:100]

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    """SECURE: User input is sanitized before logging."""
    safe_username = sanitize_for_log(data.username)

    if users_db.get(data.username) != data.password:
        logger.warning(f"Failed login attempt for user: {safe_username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logger.info(f"Successful login for user: {safe_username}")
    return {"message": "Login successful"}
