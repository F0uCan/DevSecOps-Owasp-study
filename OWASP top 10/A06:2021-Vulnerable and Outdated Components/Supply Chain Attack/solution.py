from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

# THE FIX: Use a trusted, verified function instead of a third-party one.
# In production, you should also:
#
# 1. Pin exact versions: package==1.2.3 (not package>=1.2.0)
# 2. Use hash verification: pip install --require-hashes -r requirements.txt
# 3. Run dependency scanners: pip-audit, safety, Snyk, Dependabot
# 4. Use a private package index for internal packages
# 5. Review dependency changelogs before updating
# 6. Use lockfiles (pip-tools, poetry.lock, pipenv.lock)

def format_user_data(data: dict) -> str:
    """
    SECURE: This is our own implementation with no hidden behavior.
    No external dependencies that could be compromised.
    """
    name = data.get("name", "N/A")
    email = data.get("email", "N/A")
    # Notice: SSN is intentionally excluded from output (data minimization)
    return f"User: {name}, Email: {email}"

@app.get("/api/user/{user_id}", response_class=PlainTextResponse)
def get_user(user_id: int):
    users = {
        1: {"name": "Alice", "email": "alice@company.com", "ssn": "123-45-6789"},
        2: {"name": "Bob", "email": "bob@company.com", "ssn": "987-65-4321"},
    }
    user = users.get(user_id, {"name": "Unknown", "email": "N/A"})
    return format_user_data(user)

# To audit dependencies for known vulnerabilities, run:
# pip install pip-audit
# pip-audit
