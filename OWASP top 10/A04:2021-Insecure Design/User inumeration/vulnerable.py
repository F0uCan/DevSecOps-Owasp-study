from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Simulated database
users_db = {"admin@example.com": "secret", "devops@example.com": "password123"}

class ResetRequest(BaseModel):
    email: str

@app.post("/reset-password")
def reset_password(request: ResetRequest):
    """
    VULNERABLE DESIGN: This leaks user existence.
    """
    if request.email not in users_db:
        # INSECURE: An attacker now knows this email IS NOT registered.
        raise HTTPException(status_code=404, detail="User not found")
    
    # Logic to send email would go here...
    return {"message": f"Reset link sent to {request.email}"}