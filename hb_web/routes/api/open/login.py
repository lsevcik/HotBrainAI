from flask import request, abort, current_app, redirect, url_for, session
from models.user import User


def handle_request():
    # User submits form without username or password
    if list(request.form.keys()) != ["username", "password"]:
        current_app.logger.debug(request.form.keys())
        abort(401)

    # Log the user in
    loginUser = User.login(username=request.form["username"])

    session["logged_in"] = True
    session["user_userid"] = loginUser.id
    session["user_username"] = loginUser.username

    # Return to user
    return redirect(location=url_for("index"))
