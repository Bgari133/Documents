import os
from flask import Blueprint, request, send_file, current_app

bp = Blueprint("path_traversal", __name__)

# Base directory for "files" (we'll create a safe folder with sample files)
FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "files")


@bp.route("/")
def index():
    from flask import render_template
    return render_template("path_traversal.html")


@bp.route("/read")
def read():
    # Intentionally vulnerable: user-controlled filename, no sanitization
    name = request.args.get("name", "welcome.txt")
    path = os.path.join(FILES_DIR, name)
    # Path is not normalized or validated - allows ../ escape
    if os.path.isfile(path):
        return send_file(path, as_attachment=False, download_name=os.path.basename(name))
    return "File not found", 404
