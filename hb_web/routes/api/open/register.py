from flask import request, g, current_app
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token


def handle_request():
    # User submits form without username or password
    if not request.form["username"] and not request.form["password"]:
        return json_response(status_=400, message="Bad request", authenticated=False)

    db, cur = get_db() # TODO: Insert Password with registration
    cur.execute("INSERT INTO USERS (Username) VALUES (%s)", (request.form["username"],))
    if cur.rowcount != 1:  # User enters a username that doesn't exist
        return json_response(
            status_=409, message="Username conflict", authenticated=False
        )
    user_id, username = (cur.lastrowid, request.form["username"])

    # Create JWT
    jwt = {"sub": username}

    # Return JWT to authenticated user
    return json_response(token=create_token(jwt), authenticated=True)

