import httpx
import ipaddress
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI()

# THE FIX: Allowlist of permitted domains/URLs
ALLOWED_DOMAINS = {"api.github.com", "httpbin.org", "jsonplaceholder.typicode.com"}

def is_safe_url(url: str) -> bool:
    """
    Validate that the URL is safe to fetch:
    1. Only allow http/https schemes
    2. Block private/internal IP ranges
    3. Only allow whitelisted domains
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    # Only allow http/https
    if parsed.scheme not in ("http", "https"):
        return False

    hostname = parsed.hostname
    if not hostname:
        return False

    # Block IP addresses (prevent direct access to internal IPs)
    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except ValueError:
        pass  # It's a domain name, not an IP

    # Block common cloud metadata endpoints
    blocked_hostnames = {"169.254.169.254", "metadata.google.internal", "100.100.100.200"}
    if hostname in blocked_hostnames:
        return False

    # Only allow whitelisted domains
    if hostname not in ALLOWED_DOMAINS:
        return False

    return True

@app.get("/api/fetch-url", response_class=PlainTextResponse)
def fetch_url(url: str):
    """
    SECURE VERSION:
    - Validates URL scheme (http/https only)
    - Blocks private/internal IPs
    - Uses domain allowlist
    - Blocks cloud metadata endpoints
    """
    if not is_safe_url(url):
        raise HTTPException(
            status_code=400,
            detail="URL not allowed. Only whitelisted external domains are permitted."
        )

    try:
        response = httpx.get(url, timeout=5.0, follow_redirects=False)  # Don't follow redirects!
        return f"Status: {response.status_code}\n\n{response.text[:2000]}"
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch: {e}")

@app.get("/api/webhook-test", response_class=PlainTextResponse)
def webhook_test(callback_url: str):
    """SECURE: Validates callback URL before making the request."""
    if not is_safe_url(callback_url):
        raise HTTPException(status_code=400, detail="Callback URL not allowed.")

    try:
        response = httpx.post(callback_url, json={"event": "test"}, timeout=5.0, follow_redirects=False)
        return f"Webhook delivered! Status: {response.status_code}"
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Webhook failed: {e}")
