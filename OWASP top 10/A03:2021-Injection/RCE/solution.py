import subprocess
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/ping", response_class=PlainTextResponse)
def ping_host(host: str):
    """
    SECURE ENDPOINT!
    It treats all user input as a single, safe argument.
    """
    
    # THE FIX: The command is a list. The 'host' variable
    # is just one item in the list, not part of the command string.
    command_list = ["ping", "-c", "3", host]
    
    # Run the command safely without a shell
    try:
        # 'shell=False' is the default and is secure.
        result = subprocess.run(command_list, 
                                capture_output=True, 
                                text=True, 
                                timeout=10,
                                check=True)
        output = result.stdout
        
    except subprocess.CalledProcessError as e:
        # This catches errors if ping fails (e.g., host not found)
        output = f"Command failed with error:\n{e.stderr}"
    except Exception as e:
        output = f"An error occurred: {e}"

    return output