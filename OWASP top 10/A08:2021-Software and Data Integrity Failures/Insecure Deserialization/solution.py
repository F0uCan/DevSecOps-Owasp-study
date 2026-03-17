import json
import base64
import hmac
import hashlib
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI()

# THE FIX: Use JSON (safe, no code execution) + HMAC signature for integrity.
SECRET_KEY = os.getenv("SESSION_SECRET", "dev-secret-change-in-prod")

def sign_data(data: str) -> str:
    """Create an HMAC signature for the data."""
    return hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()

def verify_signature(data: str, signature: str) -> bool:
    """Verify the HMAC signature matches."""
    expected = sign_data(data)
    return hmac.compare_digest(expected, signature)

@app.post("/api/import-session", response_class=PlainTextResponse)
def import_session(data: str, signature: str):
    """
    SECURE VERSION:
    1. Uses JSON instead of pickle (no code execution possible)
    2. Verifies HMAC signature to prevent tampering
    """
    # Verify integrity — reject tampered data
    if not verify_signature(data, signature):
        raise HTTPException(status_code=400, detail="Invalid signature — data was tampered!")

    try:
        raw = base64.b64decode(data)
        session = json.loads(raw)  # SAFE: JSON cannot execute code
        return f"Session loaded: {session}"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {e}")

@app.get("/api/export-session", response_class=PlainTextResponse)
def export_session():
    session = {"user": "john", "role": "viewer", "theme": "dark"}
    data = base64.b64encode(json.dumps(session).encode()).decode()
    sig = sign_data(data)
    return f"{data}|{sig}"
