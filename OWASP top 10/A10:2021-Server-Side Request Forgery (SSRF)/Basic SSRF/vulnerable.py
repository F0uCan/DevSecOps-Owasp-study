import httpx
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/api/fetch-url", response_class=PlainTextResponse)
def fetch_url(url: str):
    """
    VULNERABLE ENDPOINT (SSRF)!
    Accepts a URL from the user and makes a server-side HTTP request.
    An attacker can use this to:
    1. Access internal services (Redis, databases, admin panels)
    2. Read cloud metadata (AWS/GCP/Azure instance credentials)
    3. Port scan internal networks
    4. Bypass firewalls and access controls
    """
    try:
        # VULNERABILITY: No validation on the URL.
        # The server fetches ANY URL the user provides, including internal ones.
        response = httpx.get(url, timeout=5.0)
        return f"Status: {response.status_code}\n\n{response.text[:2000]}"
    except Exception as e:
        return f"Error fetching URL: {e}"

@app.get("/api/webhook-test", response_class=PlainTextResponse)
def webhook_test(callback_url: str):
    """
    VULNERABLE: Another common SSRF vector.
    The 'callback_url' parameter is fetched server-side without validation.
    Common in webhook, preview, and PDF generation features.
    """
    try:
        response = httpx.post(callback_url, json={"event": "test", "status": "ok"}, timeout=5.0)
        return f"Webhook delivered! Status: {response.status_code}"
    except Exception as e:
        return f"Webhook failed: {e}"

# --- Internal service that should NOT be reachable from outside ---
@app.get("/internal/admin", response_class=PlainTextResponse)
def internal_admin():
    """
    This endpoint simulates an internal admin panel.
    It should only be accessible from within the network,
    but SSRF allows an attacker to reach it through the server.
    """
    return "INTERNAL ADMIN PANEL\nDatabase: postgres://admin:s3cret@10.0.1.5/prod\nAPI Key: sk_live_supersecretkey123"
