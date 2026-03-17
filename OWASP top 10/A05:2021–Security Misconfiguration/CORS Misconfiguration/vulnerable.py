from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# VULNERABILITY: CORS is configured to allow ALL origins.
# This means any website on the internet can make authenticated requests
# to this API and read the response, stealing user data.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # INSECURE: Allows ANY website to call this API
    allow_credentials=True,    # CRITICAL: Combined with *, this is devastating
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated user data
users_db = {
    "token_admin": {"username": "admin", "email": "admin@corp.com", "salary": 150000},
    "token_user": {"username": "john", "email": "john@corp.com", "salary": 85000},
}

@app.get("/api/profile")
def get_profile(token: str = ""):
    """
    Returns sensitive user profile data.
    Due to the wildcard CORS policy, a malicious website can fetch this data
    from the victim's browser if they are authenticated.
    """
    user = users_db.get(token)
    if not user:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    return user

@app.get("/api/internal/salaries")
def get_all_salaries(token: str = ""):
    """An internal endpoint that should NEVER be accessible cross-origin."""
    if token != "token_admin":
        return JSONResponse(status_code=403, content={"error": "Admins only"})
    return {"salaries": [u for u in users_db.values()]}
