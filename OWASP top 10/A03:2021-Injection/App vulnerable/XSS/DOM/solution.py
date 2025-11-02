from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def get_homepage():
    """
    Serves a secure page.
    The client-side JavaScript now uses a safe sink (textContent).
    """
    
    html_content = """
    <html>
        <head><title>DOM XSS Demo</title></head>
        <body>
            <h1>Welcome, <span id="username">Guest</span>!</h1>
            
            <p>Try appending your name to the URL after a #, like: <code>/#Alice</code></p>

            <script>
                function loadName() {
                    // SOURCE: Read untrusted data from the URL hash
                    var name = window.location.hash.substring(1); 
                    
                    if(name) {
                        // FIX: Use '.textContent' to safely render the data as text.
                        // The browser will not execute any scripts inside 'name'.
                        document.getElementById('username').textContent = name;
                    }
                }
                
                // Run the function when the page loads
                window.onload = loadName;
            </script>
        </body>
    </html>
    """
    return html_content