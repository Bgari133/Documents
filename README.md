# VulnLab – Pen-Test Training Site

**For authorized security training only.** Run in an isolated environment (e.g. localhost or lab network). Do not expose to the internet or use for unauthorized testing.

## Run with Docker

```bash
docker-compose up --build
```

Then open **http://localhost:5000**

One-liner with plain Docker:

```bash
docker build -t vulnlab . && docker run -p 5000:5000 vulnlab
```

## Run locally (without Docker)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
python run.py
```

## Vulnerabilities (intentional)

| # | Vulnerability | Route | Notes |
|---|----------------|-------|--------|
| 1 | SQL Injection | `/sqli` | Raw SQL concatenation; try `' OR '1'='1` |
| 2 | Reflected XSS | `/xss/reflected` | Query echoed without encoding |
| 3 | Stored XSS | `/xss/stored` | Comments stored and rendered with `\|safe` |
| 4 | Broken Authentication | `/auth/login` | Weak check, default creds, no rate limit |
| 5 | IDOR | `/users/<id>` | No ownership/role check; IDs 1–3 exist |
| 6 | Path Traversal | `/file` | `name` parameter not sanitized |
| 7 | Command Injection | `/cmd` | Host passed to `ping` via shell |
| 8 | CSRF | `/transfer` | No CSRF token on transfer form |
| 9 | Insecure Deserialization | `/deserialize` | Base64 pickle deserialized with `pickle.loads` |
| 10 | Sensitive Data Exposure | `/config`, `/debug` | Config and env leaked; debug raises with secret |
| 11 | Security Misconfiguration | App-wide | `DEBUG=True`, default credentials in this README |

## Default credentials

| Username | Password |
|----------|----------|
| admin | admin |
| user1 | password1 |
| user2 | password2 |

## Stack

- Python 3.11, Flask, SQLite (stored in `instance/` when run locally or in Docker volume).
