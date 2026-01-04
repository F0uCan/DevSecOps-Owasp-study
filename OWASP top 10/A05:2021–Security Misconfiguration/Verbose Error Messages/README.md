## Prerequisites
First, ensure the vulnerable Python server is running:

```Bash
uvicorn vulnerable:app --reload
```

Exploitation Steps
The goal is to trigger an error and use the verbose debug output to map the server's internal file structure and software versions.

1. Trigger the Error
Send a request that you know will cause a crash (in this case, requesting a valid ID that triggers a type mismatch in our vulnerable code).

```Bash
curl http://127.0.0.1:8000/items/1
```

2. Analyze the Leaked Information
Observe the response. Instead of a simple "Server Error," you receive a wealth of information.

Expected Response (Leaked Data):

```JSON
{
  "message": "Internal Server Error",
  "debug_info": {
    "exception": "1",
    "stacktrace": "Traceback (most recent call last):\n  File \"/Users/devops/study/vulnerable.py\", line 10...\n",
    "python_version": "3.13.0 (main, Oct 2025...)"
  }
}
```
3. Identify the Risk
By reading the stacktrace, the attacker now knows:

The Internal Username of the developer (devops).

The Absolute Path of the application (/Users/devops/study/).

The Exact Python Version, which can be checked for known CVEs.

Result: This is a Security Misconfiguration. Detailed error messages intended for development were left active in a public-facing API, providing an attacker with a roadmap for further attacks.