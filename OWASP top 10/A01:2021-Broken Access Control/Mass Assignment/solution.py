# vulnerable_mass_assignment.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

# --- In-memory "database" for our example ---
db_users = {
    1: {"id": 1, "username": "alice", "email": "alice@example.com", "bio": "Just a regular user.", "is_admin": False},
    2: {"id": 2, "username": "bob", "email": "bob@example.com", "bio": "Another regular user.", "is_admin": False},
}

# --- Pydantic Models ---
# This is our internal representation of a user. It includes sensitive fields.
class User(BaseModel):
    id: int
    username: str
    email: str
    bio: Optional[str] = None
    is_admin: bool = False

# This is the model used for input. NOTICE it's the SAME as the internal model.
# This is the root cause of the vulnerability.
class UserUpdate(User):
    pass 

# --- A fake authentication dependency ---
def get_current_user():
    # In a real app, this would get the user from a token.
    # We'll pretend we're logged in as Alice (user ID 1).
    return db_users[1]

# --- FastAPI App ---
app = FastAPI()

# --- SECURE Pydantic Models ---

# This model is ONLY for user input and ONLY includes safe fields.
class SecureUserUpdate(BaseModel):
    email: Optional[str] = None
    bio: Optional[str] = None
    # The 'is_admin' field is NOT here!


@app.put("/users/me")
def update_user_me_secure(user_update: SecureUserUpdate, current_user: dict = Depends(get_current_user)):
    """
    SECURE ENDPOINT!
    It only accepts fields defined in the SecureUserUpdate model.
    """
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Now, even if the user sends 'is_admin': true in the JSON,
    # Pydantic will ignore it because it's not in the SecureUserUpdate model.
    # The 'update_data' dictionary will never contain 'is_admin'.
    db_users[current_user["id"]].update(update_data)
    
    return {"message": "Profile updated securely!", "user": db_users[current_user["id"]]}

@app.get("/admin/dashboard")
def get_admin_dashboard(current_user: dict = Depends(get_current_user)):
    """An admin-only endpoint to test our exploit."""
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Forbidden: Admins only!")
    return {"message": "Welcome to the secret admin dashboard!"}