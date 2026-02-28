from flask import Blueprint, render_template, g

bp = Blueprint("idor", __name__)

# IDOR: no check that requester owns this user_id or has permission


@bp.route("/<int:user_id>")
def user_profile(user_id):
    cur = g.db.cursor()
    cur.execute("SELECT id, username, email, role, password FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        return "User not found", 404
    user = dict(row)
    return render_template("idor_profile.html", user=user)
