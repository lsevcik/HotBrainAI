from flask import Blueprint, redirect, url_for, session


api_user = Blueprint("api_user", __name__)

@api_user.route("/logout")
def handle_logout():
    session.clear()
    return redirect(url_for("index"))
