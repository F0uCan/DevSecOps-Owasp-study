import yaml
from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse

app = FastAPI()

# VULNERABILITY: Using yaml.load() without SafeLoader.
# In older versions of PyYAML (< 6.0), yaml.load() defaults to
# FullLoader/Loader which can execute arbitrary Python objects.
# An attacker can exploit this to achieve Remote Code Execution (RCE).

sample_config = """
database:
  host: localhost
  port: 5432
  name: myapp
"""

@app.post("/api/config/import", response_class=PlainTextResponse)
def import_config(raw_yaml: str = Body(..., media_type="text/plain")):
    """
    VULNERABLE ENDPOINT!
    Accepts raw YAML from the user and loads it with the unsafe yaml.load().
    An attacker can craft a YAML payload that executes OS commands.
    """
    try:
        # VULNERABILITY: yaml.load() without specifying Loader=yaml.SafeLoader
        # allows deserialization of arbitrary Python objects.
        # Even with yaml.FullLoader (default in PyYAML >= 5.1), some attacks
        # are still possible. SafeLoader is the ONLY safe option.
        config = yaml.load(raw_yaml, Loader=yaml.FullLoader)
        return f"Config loaded successfully:\n{config}"
    except Exception as e:
        return f"Error parsing YAML: {e}"

@app.get("/api/config/sample", response_class=PlainTextResponse)
def get_sample_config():
    """Returns a sample configuration in YAML format."""
    return sample_config
