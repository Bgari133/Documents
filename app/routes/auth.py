from flask import Blueprint, render_template, request, session, redirect, url_for

bp = Blueprint("auth", __name__)

# Intentional: default creds, no rate limit, weak password check


@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == "admin" and password == "admin":
            session["user_id"] = 1
            session["username"] = "admin"
            return redirect(url_for("misc.index"))
        # Weak check: compare with other known users (no hashing)
        if username == "user1" and password == "password1":
            session["user_id"] = 2
            session["username"] = "user1"
            return redirect(url_for("misc.index"))
        if username == "user2" and password == "password2":
            session["user_id"] = 3
            session["username"] = "user2"
            return redirect(url_for("misc.index"))
        error = "Invalid credentials"
    return render_template("auth_login.html", error=error)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("misc.index"))
