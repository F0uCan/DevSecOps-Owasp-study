from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI(
    title="Internal Admin Panel",
    docs_url="/docs",        # Swagger UI publicly accessible
    redoc_url="/redoc",      # ReDoc publicly accessible
    openapi_url="/openapi.json"
)

security = HTTPBasic()

# VULNERABILITY: Default credentials that were never changed after deployment.
# This is one of the most common misconfigurations found in production systems.
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

@app.get("/admin/dashboard")
def admin_dashboard(credentials: HTTPBasicCredentials = Depends(security)):
    """
    VULNERABLE: Uses default credentials (admin/admin).
    Combined with exposed documentation endpoints, an attacker can
    discover and brute-force this endpoint trivially.
    """
    if credentials.username == ADMIN_USERNAME and credentials.password == ADMIN_PASSWORD:
        return {
            "message": "Welcome to the Admin Dashboard",
            "db_connection": "postgres://prod_user:Pr0d_P@ss!@10.0.1.5:5432/maindb",
            "redis_url": "redis://10.0.1.10:6379",
            "api_keys": {
                "stripe": "sk_live_abc123...",
                "sendgrid": "SG.xyz789..."
            }
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/health")
def health_check():
    """
    Another misconfiguration: a health endpoint that reveals
    too much information about the stack.
    """
    return {
        "status": "healthy",
        "version": "3.2.1-beta",
        "framework": "FastAPI 0.104.1",
        "database": "PostgreSQL 15.4",
        "cache": "Redis 7.2",
        "environment": "production"
    }
