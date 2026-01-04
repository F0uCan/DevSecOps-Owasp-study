## Prerequisites
First, ensure the vulnerable MD5 server is running with the following command:

```Bash
uvicorn vulnerable_md5_app:app --reload
```

## Exploitation Steps
The goal is to demonstrate that even though a password is hashed, using a weak algorithm like MD5 allows an attacker to easily crack the hash and discover the original password.

1. Register a User and Simulate a Breach
First, an attacker registers a user with a simple password (123). Then, they simulate a data breach by accessing an insecure endpoint that leaks the stored user data, including the password hash.

```Bash
curl -X POST "http://127.0.0.1:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "david", "password": "123", "full_name": "David Banner"}'
```

```Bash
curl http://127.0.0.1:8000/admin/users/all
```

Expected Response:
The API registers the user, and the breach endpoint returns the database contents, showing the MD5 hash of the user's password.

```JSON

{
  "david": {
    "password_hash": "202cb962ac59075b964b07152d234b70",
    "full_name": "David Banner"
  }
}
```
2. Perform the Exploit (Crack the Hash)
The attacker now possesses the hash (202cb962ac59075b964b07152d234b70). Because MD5 is a cryptographically broken and fast algorithm, they can use widely available online tools (like CrackStation.net) or pre-computed rainbow tables to find the original password corresponding to the hash.

This process often takes only a few seconds for simple passwords.

3. Analyze the Result
The online cracking tool instantly finds the original input that produces the stolen hash.

Successful Exploit Response:

```JSON

{
  "hash": "202cb962ac59075b964b07152d234b70",
  "cracked_password": "123"
}
```

This response confirms the exploit was successful. The attacker has recovered the original password, proving that the use of a weak hashing algorithm provided no meaningful security. This is a critical Cryptographic Failure.