from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Simulated database
users_db = {"admin@example.com": "secret", "devops@example.com": "password123"}

class ResetRequest(BaseModel):
    email: str

@app.post("/reset-password")
def reset_password(request: ResetRequest):
    """
    SECURE DESIGN: Generic response to prevent user enumeration.
    """
    # We check the DB quietly
    if request.email in users_db:
        # Logic to send the real email goes here (background task)
        pass
    
    # THE FIX: Always return the same message.
    # The attacker cannot tell if the email was valid or not.
    return {"message": "If this email is registered, you will receive a reset link shortly."}