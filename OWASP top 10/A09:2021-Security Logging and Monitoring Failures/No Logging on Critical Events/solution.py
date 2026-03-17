import logging
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

# THE FIX: Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("security_audit.log"),  # Persist logs to file
    ]
)
logger = logging.getLogger("security")

app = FastAPI()

users_db = {"admin": "SuperSecret!", "john": "password123"}

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(data: LoginRequest, request: Request):
    """
    SECURE: All authentication events are logged with relevant context.
    """
    client_ip = request.client.host
    timestamp = datetime.now(timezone.utc).isoformat()

    if users_db.get(data.username) != data.password:
        # THE FIX: Log failed login attempts with context
        logger.warning(
            f"FAILED_LOGIN | user={data.username} | ip={client_ip} | "
            f"time={timestamp} | reason=invalid_credentials"
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # THE FIX: Log successful logins
    logger.info(
        f"SUCCESSFUL_LOGIN | user={data.username} | ip={client_ip} | "
        f"time={timestamp}"
    )
    return {"message": "Login successful"}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int, request: Request):
    """SECURE: Destructive actions are always logged."""
    client_ip = request.client.host
    logger.critical(
        f"USER_DELETED | target_user_id={user_id} | ip={client_ip} | "
        f"time={datetime.now(timezone.utc).isoformat()}"
    )
    return {"message": f"User {user_id} deleted"}

@app.get("/api/admin/export-database")
async def export_database(request: Request):
    """SECURE: Data exports are logged for audit."""
    client_ip = request.client.host
    logger.warning(
        f"DATABASE_EXPORT | ip={client_ip} | records=15000 | "
        f"time={datetime.now(timezone.utc).isoformat()}"
    )
    return {"data": "All user records exported", "records": 15000}
