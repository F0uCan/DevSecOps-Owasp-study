"""
EVIL ATTACKER SERVER
Simulates a malicious website on a different origin (port 9000).
It serves attacker.html which uses JavaScript to steal data
from the vulnerable API (port 8000) via CORS misconfiguration.

Usage:
    Terminal 1: uvicorn vulnerable:app --reload          (port 8000)
    Terminal 2: python3 attacker_server.py               (port 9000)
    Browser:    Open http://localhost:9000
"""

import http.server
import os

PORT = 9000
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_GET(self):
        # Serve attacker.html for any request
        html_path = os.path.join(DIR, "attacker.html")
        with open(html_path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        print(f"[ATTACKER] {args[0]}")

if __name__ == "__main__":
    with http.server.HTTPServer(("", PORT), Handler) as httpd:
        print()
        print(f"  Evil Attacker Server running on http://localhost:{PORT}")
        print(f"  Target API: http://localhost:8000")
        print()
        print(f"  Open http://localhost:{PORT} in your browser to start the attack")
        print()
        httpd.serve_forever()
