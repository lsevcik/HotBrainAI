from flask import flash, redirect, request, current_app, abort, url_for

from models.user import register

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

    flash("You have successfully registered. You may now log in.")
    return redirect(url_for("login"))
