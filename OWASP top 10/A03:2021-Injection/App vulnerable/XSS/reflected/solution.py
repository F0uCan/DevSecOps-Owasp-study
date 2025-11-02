import html
from fastapi import FastAPI, Cookie
from fastapi.responses import HTMLResponse, Response
from typing import Optional

app = FastAPI()

# The homepage function is the same as vulnerable.py
@app.get("/", response_class=HTMLResponse)
def homepage(response: Response, session_id: Optional[str] = Cookie(None)):
    if not session_id:
        response.set_cookie(key="session_id", value="secure_fake_session_xyz789", httponly=True)
    return """
    <html><head><title>Modern Demo</title></head>
    <body>
        <h1>Welcome, User!</h1>
        <p>Your session cookie is HttpOnly. It can't be stolen by document.cookie!</p>
        <h3>Search our site (Vulnerable)</h3>
        <form action="/search" method="get">
            <input type="text" name="q"><input type="submit" value="Search">
        </form>
    </body></html>
    """

@app.get("/search", response_class=HTMLResponse)
def search(q: Optional[str] = None):
    """
    SECURE ENDPOINT!
    It HTML-escapes the query.
    """
    if q:
        # FIX: Escape the 'q' parameter.
        safe_query = html.escape(q)
        search_result = f"<h1>You searched for: {safe_query}</h1><p>...no results found.</p>"
    else:
        search_result = "<h1>Search results will appear here.</h1>"
    
    return f"""
    <html>
        <head><title>Search Results</title></head>
        <body>
            {search_result}
            <a href="/">Go back home</a>
        </body>
    </html>
    """