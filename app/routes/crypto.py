import hashlib
from flask import Blueprint, request, render_template, g

bp = Blueprint("crypto", __name__)

# A02:2021 Cryptographic Failures - weak hashing (MD5), plaintext storage


@bp.route("/", methods=["GET", "POST"])
def index():
    hash_result = ""
    if request.method == "POST":
        password = request.form.get("password", "")
        # Intentionally weak: MD5 is broken (collisions, fast to brute-force)
        hash_result = hashlib.md5(password.encode()).hexdigest() if password else ""
    # Show that users table stores plaintext (we'll display a note from DB)
    cur = g.db.cursor()
    cur.execute("SELECT username, password FROM users LIMIT 3")
    users_plain = [dict(row) for row in cur.fetchall()]
    return render_template("crypto.html", hash_result=hash_result, users_plain=users_plain)
