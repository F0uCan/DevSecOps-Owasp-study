# DevSecOps OWASP Top 10 Study

## 🎯 About This Repository

This repository is an educational project dedicated to studying and understanding the **OWASP Top 10** vulnerabilities.

The primary goal is to provide clear, practical, and hands-on examples for **DevOps/DevSecOps teams and Software Engineers**. By demonstrating both the vulnerable code and the secure solution side-by-side, this project aims to help engineers:
* **Identify** common security flaws in code reviews.
* **Understand** how these vulnerabilities are exploited in practice.
* **Learn** the correct patterns and libraries to prevent and fix them.

## ⚠️ Security Disclaimer

**This repository contains code that is *intentionally* vulnerable.**
* **DO NOT** run this code in a production environment.
* **DO NOT** use any of the vulnerable patterns (`vulnerable.py`) in your own applications.
* All examples are for educational, training, and demonstration purposes only.

---

## 🏛️ Repository Structure

This project is organized by the official OWASP Top 10 categories. Each sub-directory contains a specific, self-contained example of a vulnerability.
```text
. 
└── OWASP top 10 
    └── A0X:2021-Category_Name 
        └── App vulnerable 
            └── Specific_Vulnerability_Name 
                ├── vulnerable.py (The insecure, vulnerable code) 
                ├── solution.py (The secure, patched code) 
                └── README.md (A step-by-step guide to exploit the vulnerability)
```


**Current Vulnerabilities Covered:**
* **A01: Broken Access Control**
    * Broken Access Control (Function-Level)
    * Insecure Direct Object Reference (IDOR)
    * Mass Assignment
* **A02: Cryptographic Failures**
    * Cleartext Storage of Sensitive Data
    * Weak Hashing Algorithm (MD5)
    * Weak/Leaked JWT Secret Key
* **A03: Injection**
    * SQL Injection (SQLi)
    * OS Command Injection (RCE)
    * Local File Inclusion (LFI)
    * Cross-Site Scripting (Stored XSS)
    * Cross-Site Scripting (Reflected XSS)
    * Cross-Site Scripting (DOM-based XSS)

---

## 🚀 Getting Started

### Requirements

All examples are built using Python 3 and FastAPI. You will need:

1.  **Python 3.8+**
2.  A Python virtual environment (highly recommended).
3.  The libraries listed in `requirements.txt`.

#### `requirements.txt`
You can create a `requirements.txt` file in the root of this project with the content below.

Core web framework
fastapi uvicorn[standard]

For A02: Cryptographic Failures
passlib[bcrypt] python-jose[cryptography] PyJWT

For A03: Injection (XSS form)
python-multipart


Install all dependencies by running:
```bash
pip install -r requirements.txt
```
How to Use This Repository
The best way to learn is to exploit the code yourself.

Navigate to a specific vulnerability directory:

```Bash
cd "OWASP top 10/A01:2021-Broken Access Control/App vulnerable/IDOR"
```

Start the vulnerable server:

```Bash
uvicorn vulnerable:app --reload
```
Open the README.md file within that same directory.

Follow the step-by-step guide in the README.md to perform the exploit yourself using tools like curl or your browser.

Stop the server (Ctrl+C).

Review the solution.py file to see how the vulnerability is fixed by comparing it to vulnerable.py.