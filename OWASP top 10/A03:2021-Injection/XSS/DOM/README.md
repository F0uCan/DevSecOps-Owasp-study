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
The goal is to exploit a client-side JavaScript flaw. We will pass a malicious payload in the URL's hash fragment (#) which is read by the page's JavaScript and insecurely written into the page, causing it to execute.

1. Visit the Page and Test Normal Function
First, open your web browser and navigate to http://127.0.0.1:8000/.

Test the page's intended feature by navigating to this URL: http://127.0.0.1:8000/#Alice

Expected Response (Normal): The page content will update from "Welcome, Guest!" to Welcome, Alice!. This shows the JavaScript is reading from the URL hash as intended.

2. Perform the Exploit (Use a Malicious URL)
Now, instead of a name, we will provide an HTML payload. We use an <img ...> tag because it's a common way to execute scripts without using the word "script".

Paste the following URL directly into your browser's address bar and press Enter:

http://127.0.0.1:8000/#<img src=x onerror=alert('DOM XSS!')>
3. Analyze the Result
The vulnerable.py script serves the page. The JavaScript on that page then runs:

It reads the malicious string <img src=x onerror=alert('DOM XSS!')> from the URL hash.

It insecurely uses innerHTML to inject this string into the <span> tag.

The browser tries to render this new HTML. It attempts to load an image with an invalid source (src=x).

This triggers the onerror event, which executes our malicious JavaScript.

Successful Exploit Response: An alert box will immediately pop up on your screen with the message "DOM XSS!".

This confirms the exploit was successful, proving a client-side DOM XSS vulnerability that is completely invisible to the server.