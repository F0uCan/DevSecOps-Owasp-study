## Weak Password Policy

### What is it?
An application that allows users to register with extremely weak passwords (like `1`, `a`, or `password`) makes it trivial for attackers to brute-force or guess credentials. OWASP recommends minimum length of 8+ characters, complexity rules, and checking against known breached passwords.

### Prerequisites
Start the vulnerable server:

```Bash
uvicorn vulnerable:app --reload
```

### Exploitation Steps

**1. Register with a Ridiculously Weak Password**

```Bash
curl -X POST http://127.0.0.1:8000/register \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "1"}'
```

Expected Response:
```JSON
{"message": "User 'admin' registered successfully"}
```

The server accepted a **1-character password** without any validation!

**2. Register with a Commonly Breached Password**

```Bash
curl -X POST http://127.0.0.1:8000/register \
     -H "Content-Type: application/json" \
     -d '{"username": "ceo", "password": "password123"}'
```

This is one of the top 10 most breached passwords globally, yet the server accepts it.

**3. Brute-Force the Weak Password**

Since the password is just `1`, an attacker can crack it instantly:

```Bash
for pwd in 1 2 3 a b c; do
  result=$(curl -s -X POST http://127.0.0.1:8000/login \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"admin\", \"password\": \"$pwd\"}")
  echo "Trying '$pwd': $result"
done
```

The attacker finds the password on the **first attempt**.

**4. Verify the Fix**

Stop and start the secure version:

```Bash
uvicorn solution:app --reload
```

Try the same weak password:
```Bash
curl -X POST http://127.0.0.1:8000/register \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "1"}'
```

Expected Response:
```JSON
{"detail": [{"msg": "Value error, Password must be at least 10 characters long"}]}
```

**Result:** The lack of a password policy allows trivially guessable passwords, enabling account takeover via brute-force in seconds.
