from flask import flash, redirect, request, current_app, abort, url_for, session

from models.user import register
from models.user import login

from psycopg2.errors import UniqueViolation


def handle_request():
    # User submits form without username or password
    if list(request.form.keys()) != ["username", "password"]:
        current_app.logger.debug(request.form.keys())
        abort(401)

    # Create the user's account
    try:
        register(
            username=request.form["username"], password=request.form["password"]
        )
    except UniqueViolation:  # Username already taken
        flash("Username already in use.")
        return redirect(url_for("login"))

    # Log the user in
    user = login(request.form["username"], password=request.form["password"])
    if not user:
        abort(401)

    session["logged_in"] = True
    session["user_userid"] = user.id
    session["user_username"] = user.username

    return redirect(url_for("survey"))
