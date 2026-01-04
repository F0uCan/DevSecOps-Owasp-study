import os
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

# SECURE CONFIGURATION:
# 1. We define a specific user/pass for the scraper (e.g., Prometheus)
# 2. In production, these would be in a Secret Manager, not hardcoded.
SCRAPER_USER = "prometheus_internal"
SCRAPER_PASS = "a-very-strong-unique-password"

def authenticate_scraper(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != SCRAPER_USER or credentials.password != SCRAPER_PASS:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

@app.get("/metrics", dependencies=[Depends(authenticate_scraper)])
def get_metrics():
    """
    SECURE CONFIGURATION:
    Now, only the authorized monitoring service can access this data.
    """
    return "system_metrics_here 1.0"