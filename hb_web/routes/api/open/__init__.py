from flask import Blueprint, flash, redirect, session, url_for

from . import login, register

api_open = Blueprint("api_open", __name__)


@api_open.post("/login")
def handle_login():
    return login.handle_request()


@api_open.post("/register")
def handle_register():
    return register.handle_request()

@api_open.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("index"))