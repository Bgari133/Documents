from flask import Blueprint, render_template, request, session

bp = Blueprint("csrf", __name__)

# No CSRF token on state-changing form
BALANCES = {1: 1000, 2: 500, 3: 250}  # user_id -> balance


@bp.route("/", methods=["GET", "POST"])
def index():
    msg = ""
    if request.method == "POST":
        to_user = request.form.get("to_user", type=int)
        amount = request.form.get("amount", type=int, default=0)
        from_user = session.get("user_id", 1)
        if from_user and to_user and amount > 0:
            BALANCES[from_user] = BALANCES.get(from_user, 0) - amount
            BALANCES[to_user] = BALANCES.get(to_user, 0) + amount
            msg = f"Transferred {amount} to user {to_user}"
        else:
            msg = "Invalid transfer"
    uid = session.get("user_id", 1)
    balance = BALANCES.get(uid, 0)
    return render_template("csrf_transfer.html", balance=balance, msg=msg)
