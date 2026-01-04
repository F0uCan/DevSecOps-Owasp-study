import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# Configure internal logging (visible only to the team)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/items/{item_id}")
def read_item(item_id: int):
    items = {"1": "Laptop"}
    # Safe way to access
    if str(item_id) not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    #return {"item": items[str(item_id)]} #Fix string in ID
    return {"item": items[item_id]}  # Include to return only the error.

# SECURE CONFIGURATION:
# Return a generic message to the client, but log the details internally.
@app.exception_handler(Exception)
async def secure_exception_handler(request: Request, exc: Exception):
    # Log the full error so DevOps can fix it
    logger.error(f"Internal error: {exc}", exc_info=True)
    
    # THE FIX: Return a generic, safe response
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please contact support if the problem persists."}
    )