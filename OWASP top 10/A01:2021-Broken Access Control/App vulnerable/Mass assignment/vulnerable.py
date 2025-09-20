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

@app.put("/users/me")
def update_user_me(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    """
    VULNERABLE ENDPOINT!
    It takes all data from the UserUpdate model and applies it.
    """
    update_data = user_update.model_dump(exclude_unset=True)
    
    # THE VULNERABLE STEP: The code blindly updates the database object
    # with whatever data the user sent, because the UserUpdate model
    # allows the 'is_admin' field to be passed in.
    db_users[current_user["id"]].update(update_data)
    
    return {"message": "Profile updated!", "user": db_users[current_user["id"]]}

@app.get("/admin/dashboard")
def get_admin_dashboard(current_user: dict = Depends(get_current_user)):
    """An admin-only endpoint to test our exploit."""
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Forbidden: Admins only!")
    return {"message": "Welcome to the secret admin dashboard!"}