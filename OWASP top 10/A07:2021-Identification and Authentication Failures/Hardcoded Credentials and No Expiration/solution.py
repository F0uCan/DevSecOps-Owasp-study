import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# THE FIX 1: Credentials loaded from environment variables.
# In production, use a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
# Never commit credentials to source code or git.
USERS_DB = {
    os.getenv("ADMIN_USERNAME", ""): os.getenv("ADMIN_PASSWORD_HASH", ""),
}

# THE FIX 2: Secret key from environment variable, never hardcoded.
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
TOKEN_EXPIRY_MINUTES = 15  # Short-lived tokens

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    """SECURE: Uses env-based credentials and short-lived JWT tokens."""
    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="Server misconfigured")
    
    stored_password = USERS_DB.get(data.username)
    if not stored_password or stored_password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # THE FIX 3: Token has an expiration time (exp claim).
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    token = jwt.encode(
        {
            "sub": data.username,
            "role": "admin",
            "exp": expire,            # TOKEN EXPIRES in 15 minutes
            "iat": datetime.now(timezone.utc),  # Issued at
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token, "expires_in": f"{TOKEN_EXPIRY_MINUTES} minutes"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # PyJWT automatically validates the 'exp' claim
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired. Please login again.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/protected/data")
def get_protected_data(user: dict = Depends(get_current_user)):
    return {"message": "Sensitive data", "user": user}
