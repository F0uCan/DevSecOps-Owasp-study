from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

# In-memory "database" to store comments
db_comments: List[str] = ["This is the first (safe) comment."]

@app.get("/", response_class=HTMLResponse)
def get_homepage():
    """
    Displays the main page with comments and a form.
    VULNERABILITY IS HERE.
    """
    # Build the HTML for the comments
    comments_html = ""
    for comment in db_comments:
        # VULNERABILITY: The comment is rendered directly into the HTML.
        # An attacker's <script> tag will be treated as real HTML.
        comments_html += f"<li>{comment}</li>"

    # The full page HTML
    return f"""
    <html>
        <head><title>Guestbook</title></head>
        <body>
            <h1>Vulnerable Guestbook</h1>
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
    """Saves the new comment to the database and shows a confirmation."""
    db_comments.append(comment_text)
    return """
    <h1>Comment Posted!</h1>
    <a href="/">Go back to the guestbook</a>
    """