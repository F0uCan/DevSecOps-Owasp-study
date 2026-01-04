from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def get_homepage():
    """
    Serves a page with a client-side (DOM) vulnerability.
    The server itself is not vulnerable, the JavaScript it serves is.
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
                        // SINK: Insecurely write data directly into the page's HTML
                        // The browser will parse this string as HTML, not text.
                        document.getElementById('username').innerHTML = name;
                    }
                }
                
                // Run the function when the page loads
                window.onload = loadName;
            </script>
        </body>
    </html>
    """
    return html_content