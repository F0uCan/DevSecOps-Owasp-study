from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
import sys

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    # Intentional bug to trigger an error
    items = {"1": "Laptop"}
    return {"item": items[item_id]} # This will crash because item_id is int, but key is str

# VULNERABLE MISCONFIGURATION:
# A global error handler that returns the full stack trace to the user.
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "debug_info": {
                "exception": str(exc),
                "stacktrace": traceback.format_exc(), # LEAKS CODE AND PATHS
                "python_version": sys.version,        # LEAKS VERSION
            }
        },
    )