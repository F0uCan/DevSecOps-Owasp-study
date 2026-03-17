from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# THE FIX: Only allow specific, trusted origins.
# This is a whitelist approach — only your own frontend can call this API.
ALLOWED_ORIGINS = [
    "https://myapp.example.com",
    "https://admin.example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # SECURE: Only trusted domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],   # SECURE: Only necessary HTTP methods
    allow_headers=["Authorization", "Content-Type"],  # SECURE: Only needed headers
)

# Simulated user data
users_db = {
    "token_admin": {"username": "admin", "email": "admin@corp.com", "salary": 150000},
    "token_user": {"username": "john", "email": "john@corp.com", "salary": 85000},
}

@app.get("/api/profile")
def get_profile(token: str = ""):
    """Now protected by a strict CORS policy."""
    user = users_db.get(token)
    if not user:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    return user

@app.get("/api/internal/salaries")
def get_all_salaries(token: str = ""):
    if token != "token_admin":
        return JSONResponse(status_code=403, content={"error": "Admins only"})
    return {"salaries": [u for u in users_db.values()]}
