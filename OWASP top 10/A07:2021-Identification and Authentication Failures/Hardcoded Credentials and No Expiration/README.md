## Hardcoded Credentials & Tokens That Never Expire

### What is it?
Two critical authentication failures combined:
1. **Hardcoded credentials** in source code — anyone with repo access (including leaked .git folders) can authenticate
2. **JWT tokens without expiration** — once a token is stolen, it works **forever**

### Prerequisites
Start the vulnerable server:

```Bash
uvicorn vulnerable:app --reload
```

### Exploitation Steps

**1. Use Hardcoded Credentials**

If an attacker finds the source code (via a leaked `.git` folder, public repo, or insider threat), they can see the credentials directly:

```Bash
# Credentials found in vulnerable.py: admin / SuperSecret123!
curl -X POST http://127.0.0.1:8000/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "SuperSecret123!"}'
```

Expected Response:
```JSON
{"access_token": "eyJhbGciOiJIUzI1NiIs..."}
```

**2. Verify the Token Never Expires**

Save the token and decode it at [jwt.io](https://jwt.io):

```Bash
# Use the token from step 1
TOKEN="eyJhbGciOiJIUzI1NiIs..."

curl http://127.0.0.1:8000/protected/data \
     -H "Authorization: Bearer $TOKEN"
```

Notice: The JWT payload has **no `exp` claim**. This means:
- If the token is stolen, the attacker has **permanent access**
- Even if the password is changed, old tokens remain valid
- There is no way to revoke access without changing the secret key (which invalidates ALL tokens)

**3. Decode the Token Payload**

```Bash
# Decode the JWT payload (base64)
echo "$TOKEN" | cut -d'.' -f2 | base64 -d 2>/dev/null
```

Expected output:
```JSON
{"sub": "admin", "role": "admin"}
```

No `exp` field — the token lives forever.

**Result:** Hardcoded credentials eliminate the security benefit of passwords entirely, and tokens without expiration mean a single token leak compromises the system permanently.
