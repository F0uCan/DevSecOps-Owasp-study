import pickle
import base64
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.post("/api/import-session", response_class=PlainTextResponse)
def import_session(data: str):
    """
    VULNERABLE ENDPOINT!
    Accepts a base64-encoded Python pickle object from the user
    and deserializes it. pickle.loads() can execute ARBITRARY CODE
    during deserialization.
    """
    try:
        # VULNERABILITY: pickle.loads() executes any Python code
        # embedded in the serialized object. An attacker can craft
        # a malicious pickle that runs os.system(), subprocess, etc.
        raw = base64.b64decode(data)
        session = pickle.loads(raw)  # DANGER: Arbitrary Code Execution!
        return f"Session loaded: {session}"
    except Exception as e:
        return f"Error: {e}"

@app.get("/api/export-session", response_class=PlainTextResponse)
def export_session():
    """Creates a legitimate serialized session object."""
    session = {"user": "john", "role": "viewer", "theme": "dark"}
    serialized = base64.b64encode(pickle.dumps(session)).decode()
    return serialized
