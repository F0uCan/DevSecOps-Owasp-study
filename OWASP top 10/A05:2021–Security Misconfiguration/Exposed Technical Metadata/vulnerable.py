import os
from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse

app = FastAPI()

# Simulated environment variables (In a real app, these are in the OS/K8s)
os.environ["DATABASE_URL"] = "postgres://admin:p@ssword123@10.0.45.2:5432/prod_db"
os.environ["STRIPE_API_KEY"] = "sk_live_51Mzbcdefghijklmnopqrstuvwxyz"

@app.get("/metrics", response_class=PlainTextResponse)
def get_metrics():
    """
    VULNERABLE MISCONFIGURATION:
    This endpoint exposes internal system metrics and environment 
    variables to the public internet without authentication.
    """
    # In a real scenario, this might be a library like prometheus_client
    # but the misconfiguration is the same: exposing it publicly.
    output = "# HELP system_env Internal Environment Variables\n"
    for key, value in os.environ.items():
        # A misconfigured exporter might leak everything
        if "API" in key or "URL" in key:
            output += f'system_env{{name="{key}"}} {value}\n'
    
    return output