# 🛡️ DevSecOps — OWASP Top 10 (2021) Study Lab

> **A hands-on educational lab** for studying, exploiting, and preventing the 10 most critical web application vulnerabilities according to OWASP.

## 🎯 About This Repository

This repository is an educational project dedicated to studying and understanding the **OWASP Top 10 (2021)**. The primary goal is to provide clear, practical, and hands-on examples for **DevOps/DevSecOps teams and Software Engineers**.

Each vulnerability is demonstrated side-by-side: the vulnerable code and the secure solution, allowing engineers to:
* 🔍 **Identify** common security flaws in code reviews
* 💥 **Exploit** how these vulnerabilities are attacked in practice (with ready-to-use `curl` commands)
* ✅ **Learn** the correct patterns and libraries to prevent and fix each flaw

---

## ⚠️ Security Disclaimer

> **This repository contains code that is *intentionally* vulnerable.**
> * **DO NOT** run this code in a production environment
> * **DO NOT** use any of the vulnerable patterns (`vulnerable.py`) in your own applications
> * All examples are for educational, training, and demonstration purposes only

---

## 🚀 Getting Started

### Requirements
* **Python 3.8+**
* A Python virtual environment (highly recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/F0uCan/DevSecOps-Owasp-study.git
cd DevSecOps-Owasp-study

# Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install all dependencies
pip install -r requirements.txt
```

### How to Use

The best way to learn is to **exploit the code yourself**:

```bash
# 1. Navigate to a specific vulnerability directory
cd "OWASP top 10/A03:2021-Injection/SQLinjection"

# 2. Start the vulnerable server
uvicorn vulnerable:app --reload

# 3. Open the local README.md and follow the step-by-step exploitation guide

# 4. Stop the server (Ctrl+C) and compare with the secure solution
uvicorn solution:app --reload
```

---

## 🏛️ Repository Structure

```text
.
└── OWASP top 10/
    └── A0X:2021-Category_Name/
        └── Vulnerability_Name/
            ├── vulnerable.py    ← Insecure, vulnerable code
            ├── solution.py      ← Secure, patched code
            └── README.md        ← Step-by-step exploitation guide
```

---

## 📋 Full Coverage — OWASP Top 10 (2021)

### A01: Broken Access Control
> Failures that allow users to act outside of their intended permissions.

| Vulnerability | Description |
|---|---|
| **Broken Access Control** | Accessing admin functions without proper role verification |
| **IDOR** (Insecure Direct Object Reference) | Accessing other users' resources by changing IDs in the URL |
| **Mass Assignment** | Sending extra fields (e.g., `role: admin`) to escalate privileges |

---

### A02: Cryptographic Failures
> Failures related to cryptography — or the lack thereof — that expose sensitive data.

| Vulnerability | Description |
|---|---|
| **Cleartext Storage** | Passwords stored in plaintext in the database |
| **Weak Hashing (MD5)** | MD5 hash crackable with rainbow tables |
| **Weak/Leaked JWT Secret** | JWT signed with a weak secret (`"secret"`) — attacker forges tokens |

---

### A03: Injection
> Untrusted data sent as part of a command or query.

| Vulnerability | Description |
|---|---|
| **SQL Injection** | SQL injection via user input that manipulates database queries |
| **OS Command Injection (RCE)** | Remote command execution on the server via `ping` |
| **Local File Inclusion (LFI)** | Reading internal files via path traversal |
| **Stored XSS** | Malicious JavaScript persisted in the database |
| **Reflected XSS** | XSS payload reflected via query parameter |
| **DOM-based XSS** | DOM manipulation via URL fragment |

---

### A04: Insecure Design
> Business logic flaws that no perfect implementation can fix.

| Vulnerability | Description |
|---|---|
| **Lack of Rate Limiting** | Brute-force with no attempt limit |
| **Trusting the Client** | Product price sent by the client (modifiable) |
| **User Enumeration** | Different responses reveal which users exist |

---

### A05: Security Misconfiguration
> Insecure default configurations, incomplete or ad hoc setups.

| Vulnerability | Description |
|---|---|
| **Verbose Error Messages** | Stack traces and version info leaked in error responses |
| **Exposed Technical Metadata** | `/metrics` endpoint exposes credentials and API keys |
| **CORS Misconfiguration** | Wildcard `*` in CORS allows any website to read API data |
| **Default Credentials** | Default credentials (admin/admin) + exposed Swagger + verbose health endpoint |

---

### A06: Vulnerable & Outdated Components
> Use of components with known vulnerabilities or insecure configurations.

| Vulnerability | Description |
|---|---|
| **Insecure YAML Deserialization** | `yaml.load()` with unsafe Loader allows code execution |
| **Supply Chain Attack** | Compromised dependency silently exfiltrates data |

---

### A07: Identification & Authentication Failures
> Failures that allow compromise of accounts, passwords, or session tokens.

| Vulnerability | Description |
|---|---|
| **Weak Password Policy** | Registration accepts 1-character passwords with no validation |
| **Hardcoded Credentials & No Expiration** | Credentials in source code + JWT tokens that never expire |

---

### A08: Software & Data Integrity Failures
> Code and infrastructure that fail to protect against integrity violations.

| Vulnerability | Description |
|---|---|
| **Insecure Deserialization (Pickle)** | `pickle.loads()` on user input = RCE |
| **Unsigned Cookies** | Base64 cookies without signature — privilege escalation possible |

---

### A09: Security Logging & Monitoring Failures
> Without proper logging, attacks go undetected for months.

| Vulnerability | Description |
|---|---|
| **No Logging on Critical Events** | Login attempts, data exports, and deletions with zero logging |
| **Log Injection** | User input in log messages allows forging fake entries |

---

### A10: Server-Side Request Forgery (SSRF)
> Server makes requests to URLs controlled by the attacker.

| Vulnerability | Description |
|---|---|
| **Basic SSRF** | Fetching internal URLs, cloud metadata, and port scanning via the server |

---

## 📊 Statistics

| Metric | Value |
|---|---|
| OWASP categories covered | **10/10** ✅ |
| Total vulnerabilities | **27 examples** |
| Python files | **55+** |
| Exploitation guides | **27 READMEs with curl commands** |

---

## 🛠️ Technologies Used

* **Python 3** — Primary language
* **FastAPI** — Web framework (high performance, async)
* **SQLite** — Database (for SQL Injection examples)
* **PyJWT** — JWT token handling
* **PyYAML** — For deserialization examples
* **httpx** — HTTP client (for SSRF examples)

---

## 📚 References

* [OWASP Top 10 (2021)](https://owasp.org/www-project-top-ten/)
* [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
* [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
* [PortSwigger Web Security Academy](https://portswigger.net/web-security)