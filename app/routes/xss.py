from flask import Blueprint, render_template, request, g

bp = Blueprint("xss", __name__)


@bp.route("/reflected", methods=["GET", "POST"])
def reflected():
    # Reflected XSS: echo user input without encoding
    q = request.args.get("q", "") or (request.form.get("q", "") if request.form else "")
    return render_template("xss_reflected.html", q=q)


@bp.route("/stored", methods=["GET", "POST"])
def stored():
    if request.method == "POST":
        author = request.form.get("author", "Anonymous")
        content = request.form.get("content", "")
        cur = g.db.cursor()
        cur.execute("INSERT INTO comments (author, content) VALUES (?, ?)", (author, content))
        g.db.commit()
    cur = g.db.cursor()
    cur.execute("SELECT author, content, created_at FROM comments ORDER BY id DESC")
    comments = [dict(row) for row in cur.fetchall()]
    return render_template("xss_stored.html", comments=comments)
