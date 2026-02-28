from flask import Blueprint, render_template, request, g

bp = Blueprint("sqli", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        q = request.form.get("q", "")
        # Intentionally vulnerable: raw SQL concatenation
        cur = g.db.cursor()
        cur.execute("SELECT id, username, email FROM users WHERE username = '" + q + "'")
        rows = cur.fetchall()
        results = [dict(row) for row in rows]
    return render_template("sqli.html", results=results)
