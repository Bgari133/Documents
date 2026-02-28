from flask import Blueprint, render_template

bp = Blueprint("clickjacking", __name__)

# Clickjacking: no X-Frame-Options; page can be embedded in iframe


@bp.route("/")
def index():
    return render_template("clickjacking.html")


@bp.route("/victim")
def victim():
    """Page that looks safe but can be iframed (no X-Frame-Options)."""
    r = render_template("clickjacking_victim.html")
    from flask import make_response
    resp = make_response(r)
    # Intentionally do NOT set X-Frame-Options or Content-Security-Policy frame-ancestors
    return resp


@bp.route("/attacker")
def attacker():
    """Demo: embed victim in iframe to simulate clickjacking."""
    return render_template("clickjacking_attacker.html")
