import xml.etree.ElementTree as ET
from flask import Blueprint, request, render_template

bp = Blueprint("xxe", __name__)

# XXE: parse XML with external entities enabled (no secure parser)


@bp.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        raw = request.form.get("xml", "")
        if raw:
            try:
                # Intentionally vulnerable: ElementTree can resolve entities in some setups
                root = ET.fromstring(raw)
                result = ET.tostring(root, encoding="unicode", method="xml")[:2000]
            except ET.ParseError as e:
                result = "Parse error: " + str(e)
            except Exception as e:
                result = "Error: " + str(e)
    return render_template("xxe.html", result=result)
