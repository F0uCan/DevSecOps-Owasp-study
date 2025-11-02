import html  # Import the HTML escaping library
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

# In-memory "database" to store comments
db_comments: List[str] = ["This is the first (safe) comment."]

@app.get("/", response_class=HTMLResponse)
def get_homepage():
    """
    SECURE VERSION.
    Uses HTML escaping to neutralize XSS.
    """
    comments_html = ""
    for comment in db_comments:
        # THE FIX: Escape the comment before rendering it.
        # <script> becomes &lt;script&gt;
        # The browser will display this text, not execute it.
        safe_comment = html.escape(comment)
        comments_html += f"<li>{safe_comment}</li>"

    # The full page HTML (same as before)
    return f"""
    <html>
        <head><title>Guestbook</title></head>
        <body>
            <h1>Secure Guestbook</h1>
            <h3>Comments:</h3>
            <ul>
                {comments_html}
            </ul>
            <hr>
            <h3>Post a new comment:</h3>
            <form action="/comment" method="post">
                <input type="text" name="comment_text" style="width: 300px;">
                <input type="submit" value="Post">
            </form>
        </body>
    </html>
    """

@app.post("/comment", response_class=HTMLResponse)
def post_comment(comment_text: str = Form(...)):
    """Saves the new comment to the database."""
    db_comments.append(comment_text)
    return """
    <h1>Comment Posted!</h1>
    <a href="/">Go back to the guestbook</a>
    """