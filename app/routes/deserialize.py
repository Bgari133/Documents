import pickle
import base64
from flask import Blueprint, render_template, request

bp = Blueprint("deserialize", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        data = request.form.get("data", "")
        try:
            raw = base64.b64decode(data)
            obj = pickle.loads(raw)  # Intentionally vulnerable
            result = repr(obj)
        except Exception as e:
            result = f"Error: {e}"
    return render_template("deserialize.html", result=result)
