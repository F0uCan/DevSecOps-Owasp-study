## No Logging on Critical Security Events

### What is it?
When an application has no logging for critical events (failed logins, data exports, destructive actions), attackers operate invisibly. Brute-force attacks, data breaches, and unauthorized access can go undetected for **months or years**. According to IBM's 2024 report, the average time to detect a breach is **194 days** — often because of insufficient logging.

### Prerequisites
Start the vulnerable server:

```Bash
uvicorn vulnerable:app --reload
```

### Exploitation Steps

**1. Perform a Brute-Force Attack (Invisible)**

Send multiple failed login attempts:

```Bash
for pwd in 123456 password admin qwerty letmein; do
  curl -s -X POST http://127.0.0.1:8000/login \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"admin\", \"password\": \"$pwd\"}"
  echo ""
done
```

Now check the server logs — there is **nothing there** about these failed attempts. No alert was triggered, no IP was recorded.

**2. Exfiltrate All Data (Undetected)**

```Bash
curl http://127.0.0.1:8000/api/admin/export-database
```

Expected Response:
```JSON
{"data": "All user records exported", "records": 15000}
```

15,000 records just got exported and there's **zero evidence** in the logs.

**3. Delete Users (No Audit Trail)**

```Bash
curl -X DELETE http://127.0.0.1:8000/api/users/1
curl -X DELETE http://127.0.0.1:8000/api/users/2
curl -X DELETE http://127.0.0.1:8000/api/users/3
```

Users were deleted and nobody knows who did it, when, or from where.

**4. Compare with the Secure Version**

Stop and start the secure version:
```Bash
uvicorn solution:app --reload
```

Repeat the brute-force attack, then check `security_audit.log`:
```Bash
cat security_audit.log
```

You'll see structured logs like:
```
2026-02-21 20:30:00 | WARNING | FAILED_LOGIN | user=admin | ip=127.0.0.1 | reason=invalid_credentials
```

**Result:** Without logging, incident response is impossible — you can't investigate what you can't see. Proper logging enables detection, alerting, and forensic analysis.
