import os
import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# --- 1. Load environment variables from .env file ---
load_dotenv()

# --- 2. Load the key SECURELY from the environment ---
# This is the fix! The key is no longer in the code.
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# A check to ensure the server doesn't start without a key
if SECRET_KEY is None:
    raise RuntimeError("SECRET_KEY environment variable not set.")

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str

@app.post("/login")
def login_for_access_token(user: User):
    """Issues a standard token signed with the weak key."""
    to_encode = {"sub": user.username, "role": "user"}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    """A secure decode function... that relies on a weak key."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/admin/data")
def get_admin_data(current_user: dict = Depends(get_current_user)):
    """A protected endpoint only for admins."""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only!")
    
    return {"message": "Secret admin data accessed!", "user_data": current_user}