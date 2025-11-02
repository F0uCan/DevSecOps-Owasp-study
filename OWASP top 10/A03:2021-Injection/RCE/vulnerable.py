import os
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/ping", response_class=PlainTextResponse)
def ping_host(host: str):
    """
    VULNERABLE ENDPOINT!
    It takes user input 'host' and builds an OS command with it.
    """
    
    # VULNERABILITY: The 'host' string is pasted directly into the command.
    # An attacker can add a ';' to inject a new command.
    command = f"ping -c 3 {host}"
    
    # Run the (potentially malicious) command on the server
    try:
        output = os.popen(command).read()
    except Exception as e:
        output = f"An error occurred: {e}"

    return output