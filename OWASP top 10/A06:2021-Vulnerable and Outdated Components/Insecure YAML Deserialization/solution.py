import yaml
from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse

app = FastAPI()

sample_config = """
database:
  host: localhost
  port: 5432
  name: myapp
"""

@app.post("/api/config/import", response_class=PlainTextResponse)
def import_config(raw_yaml: str = Body(..., media_type="text/plain")):
    """
    SECURE VERSION: Uses yaml.safe_load() which only allows
    basic Python types (str, int, list, dict, etc.)
    and BLOCKS arbitrary object deserialization.
    """
    try:
        # THE FIX: yaml.safe_load() only deserializes basic Python types.
        # It will reject any !!python/ tags or custom constructors.
        config = yaml.safe_load(raw_yaml)
        return f"Config loaded successfully:\n{config}"
    except yaml.YAMLError as e:
        return f"Error parsing YAML: {e}"

@app.get("/api/config/sample", response_class=PlainTextResponse)
def get_sample_config():
    return sample_config
