from flask import Blueprint, redirect, request

bp = Blueprint("redirect_open", __name__)

# Open Redirect: redirect to user-supplied URL without allowlist (CWE-601)


@bp.route("/")
def index():
    from flask import render_template
    return render_template("redirect_open.html")


@bp.route("/go")
def go():
    url = request.args.get("url", "/")
    # Intentionally vulnerable: no allowlist; redirect to any URL
    return redirect(url)
