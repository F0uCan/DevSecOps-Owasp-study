## Prerequisites
First, ensure you have the necessary libraries installed:

```Bash
pip install fastapi "uvicorn[standard]" python-multipart
```

Next, ensure the vulnerable server (vulnerable.py) is running.

```Bash
uvicorn vulnerable:app --reload
```

## Exploitation Steps
The goal is to inject a malicious JavaScript payload into the guestbook. This "stored" script will then execute in the browser of any user who visits the page, including the attacker, to simulate the effect.

1. Open the Vulnerable Page
Open your web browser and navigate to the running application, which is at http://127.0.0.1:8000. You will see the guestbook page and the (safe) first comment.

2. Craft the Malicious Payload
Instead of a normal comment, the attacker crafts a comment containing an HTML <script> tag. The simplest payload to test for XSS is one that creates a pop-up alert box.

Payload: <script>alert('XSS Attack!');</script>

3. Perform the Exploit (Inject the Payload)
In the "Post a new comment:" form on the webpage, paste the malicious payload into the text box and click the "Post" button.

The server will insecurely save this string to its "database" and then redirect you. Click the "Go back to the guestbook" link.

4. Analyze the Result
As soon as your browser loads the main page, it will read the list of comments. When it tries to render the malicious comment, it won't display the text. Instead, it will execute the JavaScript inside the <script> tag.

Successful Exploit Response: You will immediately see a JavaScript alert box pop up on your screen with the message "XSS Attack!".

This confirms the exploit was successful. An attacker has successfully stored a malicious script on the server, which now attacks every user who views the page. A real attacker would use a script to steal cookies, session tokens, or redirect users to a malicious website.