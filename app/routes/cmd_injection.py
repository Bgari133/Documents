import os
import subprocess
from flask import Blueprint, render_template, request

bp = Blueprint("cmd_injection", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        host = request.form.get("host", "127.0.0.1")
        # Intentionally vulnerable: user input passed to shell
        ping_cmd = "ping -n 2 " if os.name == "nt" else "ping -c 2 "
        output = subprocess.getoutput(ping_cmd + host)
    return render_template("cmd_injection.html", output=output)
