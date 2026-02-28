import urllib.request
from flask import Blueprint, request, render_template

bp = Blueprint("ssrf", __name__)

# A10:2021 Server-Side Request Forgery - fetch user-supplied URL without allowlist


@bp.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            try:
                # Intentionally vulnerable: no allowlist, can hit internal services
                req = urllib.request.Request(url, headers={"User-Agent": "VulnLab/1.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    result = resp.read().decode("utf-8", errors="replace")[:2000]
            except Exception as e:
                result = f"Error: {e}"
    return render_template("ssrf.html", result=result)
