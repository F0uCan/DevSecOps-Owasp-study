import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# VULNERABILITY 1: Hardcoded credentials in source code
HARDCODED_USERS = {
    "admin": "SuperSecret123!",
    "service_account": "svc_p@ssw0rd_2024",
}

# VULNERABILITY 2: Secret key hardcoded
SECRET_KEY = "my-super-secret-key-12345"

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginRequest):
    """
    VULNERABLE: Hardcoded credentials + JWT tokens that NEVER expire.
    """
    if HARDCODED_USERS.get(data.username) != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # VULNERABILITY 3: Token has NO expiration claim (exp).
    # Once issued, this token is valid FOREVER.
    token = jwt.encode(
        {"sub": data.username, "role": "admin"},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/protected/data")
def get_protected_data(user: dict = Depends(get_current_user)):
    """Protected endpoint — but tokens never expire."""
    return {"message": "Sensitive data", "user": user}
