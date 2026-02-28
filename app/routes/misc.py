from flask import Blueprint, render_template, current_app
import os

bp = Blueprint("misc", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/config")
def config():
    # Sensitive data exposure: leak config and env
    config_items = {k: str(v) for k, v in current_app.config.items()}
    env_items = dict(os.environ)
    return render_template("config.html", config=config_items, env=env_items)


@bp.route("/debug")
def debug():
    # Verbose error / debug info exposure
    raise ValueError("Intentional debug exception: SECRET_KEY=" + current_app.config.get("SECRET_KEY", ""))
