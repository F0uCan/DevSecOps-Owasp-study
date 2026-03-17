import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import hashlib
import secrets

# THE FIX 1: In production, disable documentation endpoints.
is_production = os.getenv("ENVIRONMENT", "production") == "production"

app = FastAPI(
    title="Internal Admin Panel",
    docs_url=None if is_production else "/docs",       # SECURE: Disabled in prod
    redoc_url=None if is_production else "/redoc",     # SECURE: Disabled in prod
    openapi_url=None if is_production else "/openapi.json"  # SECURE: Disabled in prod
)

security = HTTPBasic()

# THE FIX 2: Credentials from environment variables, never hardcoded.
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH", "")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare password securely using SHA-256 (use bcrypt in real apps)."""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

@app.get("/admin/dashboard")
def admin_dashboard(credentials: HTTPBasicCredentials = Depends(security)):
    """
    SECURE VERSION:
    - Credentials are loaded from environment variables
    - No default passwords
    - Docs are disabled in production
    """
    if not ADMIN_USERNAME or not ADMIN_PASSWORD_HASH:
        raise HTTPException(status_code=500, detail="Server not configured")
    
    if not secrets.compare_digest(credentials.username, ADMIN_USERNAME):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(credentials.password, ADMIN_PASSWORD_HASH):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Welcome to the Admin Dashboard"}

@app.get("/health")
def health_check():
    """SECURE: Only minimal information is exposed."""
    return {"status": "healthy"}
