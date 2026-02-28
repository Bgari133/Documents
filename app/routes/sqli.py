from flask import Blueprint, render_template, request, g

bp = Blueprint("sqli", __name__)


@bp.route("/")
def index():
    """Hub: code examples and links to each SQLi type."""
    return render_template("sqli.html")


@bp.route("/search", methods=["GET", "POST"])
def search():
    """Classic / in-band: vulnerable search with concatenation."""
    results = []
    search_error = None
    if request.method == "POST":
        q = request.form.get("q", "")
        cur = g.db.cursor()
        sql = "SELECT id, username, email FROM users WHERE username = '" + q + "'"
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            results = [dict(row) for row in rows]
        except Exception as e:
            search_error = str(e)
            results = []
    return render_template("sqli_search.html", results=results, search_error=search_error)


@bp.route("/login", methods=["GET", "POST"])
def login_bypass():
    """Login bypass: username/password concatenated into SQL."""
    user = None
    if request.method == "POST":
        u = request.form.get("username", "")
        p = request.form.get("password", "")
        cur = g.db.cursor()
        sql = "SELECT id, username, email FROM users WHERE username = '" + u + "' AND password = '" + p + "'"
        try:
            cur.execute(sql)
            row = cur.fetchone()
            if row:
                user = dict(row)
        except Exception:
            pass
    return render_template("sqli_login.html", user=user)


@bp.route("/union", methods=["GET", "POST"])
def union():
    """Union-based: same vulnerable search; show all columns including password for UNION payloads."""
    results = []
    if request.method == "POST":
        q = request.form.get("q", "")
        cur = g.db.cursor()
        sql = "SELECT id, username, email FROM users WHERE username = '" + q + "'"
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            results = [dict(row) for row in rows]
        except Exception:
            results = []
    return render_template("sqli_union.html", results=results)


@bp.route("/error", methods=["GET", "POST"])
def error_based():
    """Error-based: trigger SQL errors and show message so attacker can extract data from error content."""
    err_msg = None
    if request.method == "POST":
        q = request.form.get("q", "")
        cur = g.db.cursor()
        sql = "SELECT id, username, email FROM users WHERE username = '" + q + "'"
        try:
            cur.execute(sql)
            cur.fetchall()
        except Exception as e:
            err_msg = str(e)
    return render_template("sqli_error.html", search_error=err_msg)


@bp.route("/blind", methods=["GET", "POST"])
def blind():
    """Boolean blind: only returns exists / not exists; no data in response."""
    exists = None
    if request.method == "POST":
        q = request.form.get("q", "")
        cur = g.db.cursor()
        sql = "SELECT 1 FROM users WHERE username = '" + q + "' LIMIT 1"
        try:
            cur.execute(sql)
            exists = cur.fetchone() is not None
        except Exception:
            exists = False
    return render_template("sqli_blind.html", exists=exists)
