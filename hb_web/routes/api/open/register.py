from flask import request, current_app, abort
from flask_json import json_response
from tools.token_tools import create_token

from models.user import User

from psycopg2.errors import UniqueViolation

def handle_request():
    # User submits form without username or password
    if list(request.form.keys()) != ["username", "password"]:
        current_app.logger.debug(request.form.keys())
        abort(401)

    # Create the user's account
    try:
        loginUser = User.register(username=request.form["username"], password=request.form["password"])
    except UniqueViolation: # Username already taken
        abort(409)

    # Create JWT
    jwt = {"sub": loginUser.username, "role": loginUser.role}

    # Return JWT to authenticated user
    return json_response(token=create_token(jwt), authenticated=True)

