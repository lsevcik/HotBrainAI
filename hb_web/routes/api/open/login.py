from flask import request, abort, current_app
from flask_json import json_response
from tools.token_tools import create_token
from models.user import User


def handle_request():
    # User submits form without username or password
    if list(request.form.keys()) != ["username", "password"]:
        current_app.logger.debug(request.form.keys())
        abort(401)

    # Log the user in
    loginUser = User.login(username=request.form["username"])

    # Create JWT
    jwt = {"sub": loginUser.username, "role": loginUser.role}

    # Return JWT to authenticated user
    return json_response(token=create_token(jwt), authenticated=True)
