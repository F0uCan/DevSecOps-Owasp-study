import base64
import json
import hmac
import hashlib
import os
from fastapi import FastAPI, Response, Cookie, HTTPException

app = FastAPI()

SECRET_KEY = os.getenv("COOKIE_SECRET", "change-me-in-production")
users_db = {"admin": "admin123", "john": "pass456"}

def create_signed_cookie(data: dict) -> str:
    """Create a cookie with HMAC signature to prevent tampering."""
    payload = base64.b64encode(json.dumps(data).encode()).decode()
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{signature}"

def verify_signed_cookie(cookie: str) -> dict:
    """Verify the cookie signature and return the data if valid."""
    try:
        payload, signature = cookie.rsplit(".", 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Malformed cookie")

    expected = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=403, detail="Cookie tampered! Signature mismatch.")

    return json.loads(base64.b64decode(payload))

@app.post("/login")
def login(username: str, password: str, response: Response):
    """SECURE: Sets a signed cookie that cannot be tampered with."""
    if users_db.get(username) != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    cookie_value = create_signed_cookie({"user": username, "role": "viewer"})
    response.set_cookie(key="session", value=cookie_value, httponly=True, samesite="strict")
    return {"message": "Logged in"}

@app.get("/dashboard")
def dashboard(session: str = Cookie(None)):
    """SECURE: Verifies signature before trusting cookie data."""
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    data = verify_signed_cookie(session)

    if data.get("role") == "admin":
        return {"message": "Welcome Admin!", "secret": "Database password: Pr0d_S3cret!"}

    return {"message": f"Welcome {data.get('user')}! You have '{data.get('role')}' access."}
