from flask import redirect, request, current_app, abort, url_for

from models.user import User

from psycopg2.errors import UniqueViolation


def handle_request():
    # User submits form without username or password
    if list(request.form.keys()) != ["username", "password"]:
        current_app.logger.debug(request.form.keys())
        abort(401)

    # Create the user's account
    try:
        User.register(
            username=request.form["username"], password=request.form["password"]
        )
    except UniqueViolation:  # Username already taken
        abort(409)

    # Return JWT to authenticated user
    return redirect(url_for("login"))
