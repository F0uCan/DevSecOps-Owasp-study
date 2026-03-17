import base64
import json
from fastapi import FastAPI, Response, Cookie, HTTPException

app = FastAPI()

users_db = {"admin": "admin123", "john": "pass456"}

@app.post("/login")
def login(username: str, password: str, response: Response):
    """
    VULNERABLE: Sets a cookie with user data in plain base64.
    No signature or encryption — the user can tamper with it.
    """
    if users_db.get(username) != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # VULNERABILITY: Cookie data is just base64-encoded JSON.
    # An attacker can decode it, change the role, re-encode it,
    # and send it back — the server has no way to detect tampering.
    session_data = json.dumps({"user": username, "role": "viewer"})
    cookie_value = base64.b64encode(session_data.encode()).decode()

    response.set_cookie(key="session", value=cookie_value)
    return {"message": "Logged in", "cookie_value": cookie_value}

@app.get("/dashboard")
def dashboard(session: str = Cookie(None)):
    """
    VULNERABLE: Trusts the cookie without verifying integrity.
    """
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        data = json.loads(base64.b64decode(session))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session")

    if data.get("role") == "admin":
        return {"message": "Welcome Admin!", "secret": "Database password: Pr0d_S3cret!"}

    return {"message": f"Welcome {data.get('user')}! You have '{data.get('role')}' access."}
