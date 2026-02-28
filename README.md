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

## OWASP Top 10:2021 mapping

The app includes labs aligned to [OWASP Top 10:2021](https://owasp.org/Top10/). Open **/owasp** in the browser for a full mapping table (A01–A10) with impact and links to each lab.

## Vulnerabilities (intentional)

| # | OWASP | Vulnerability | Route | Notes |
|---|-------|----------------|-------|--------|
| 1 | A03 | SQL Injection | `/sqli` | **Types:** Classic, Error-based, Login bypass, Union, Blind (see hub for code examples) |
| 2 | – | Reflected XSS | `/xss/reflected` | Query echoed without encoding |
| 3 | – | Stored XSS | `/xss/stored` | Comments stored and rendered with `\|safe` |
| 4 | A07 | Broken Authentication | `/auth/login` | Weak check, default creds, no rate limit |
| 5 | A01 | IDOR | `/users/<id>` | No ownership/role check; IDs 1–3 exist |
| 6 | A01 | Path Traversal | `/file` | `name` parameter not sanitized |
| 7 | A03 | Command Injection | `/cmd` | Host passed to `ping` via shell |
| 8 | A01 | CSRF | `/transfer` | No CSRF token on transfer form |
| 9 | A08 | Insecure Deserialization | `/deserialize` | Base64 pickle deserialized with `pickle.loads` |
| 10 | A10 | SSRF | `/ssrf` | Server fetches user-supplied URL (no allowlist) |
| 11 | A02 | Cryptographic Failures | `/crypto` | MD5 “hashing”, plaintext passwords in DB |
| 12 | A02/A05 | Sensitive Data Exposure | `/config`, `/debug` | Config and env leaked; debug raises with secret |
| 13 | A05 | Security Misconfiguration | App-wide | `DEBUG=True`, default credentials in this README |
| 14 | CWE-601 | Open Redirect | `/redirect` | Redirect to user-supplied URL; no allowlist |
| 15 | A03 | XXE | `/xxe` | XML parsing with external entities (code examples) |
| 16 | CWE-1021 | Clickjacking | `/clickjacking` | No X-Frame-Options; victim + attacker demo |

Each lab page includes **exploitation details**, **code examples** (vulnerable vs safe where applicable), OWASP category, impact, example payloads, and remediation.

## Default credentials

| Username | Password |
|----------|----------|
| admin | admin |
| user1 | password1 |
| user2 | password2 |

## Stack

- Python 3.11, Flask, SQLite (stored in `instance/` when run locally or in Docker volume).
