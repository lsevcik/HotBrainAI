from flask import request, abort, current_app, redirect, url_for, session

from models.user import login


def handle_request():
    # User is logged in
    if session.get("logged_in", False):
        return redirect("index")

    # User submits form without username or password
    if list(request.form.keys()) != ["username", "password"]:
        current_app.logger.debug(request.form.keys())
        abort(400)

    # Log the user in
    user = login(request.form["username"], password=request.form["password"])
    if not user:
        abort(401)

    session["logged_in"] = True
    session["user_userid"] = user.id
    session["user_username"] = user.username

    # Return to user
    return redirect(url_for("survey"))
