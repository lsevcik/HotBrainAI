from flask import request, g, current_app
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.db_con import get_db


def handle_request():
    # User submits form without username or password
    if not request.form["username"] and not request.form["password"]:
        return json_response(status_=400, message="Bad request", authenticated=False)

    db, cur = get_db()
    cur.execute("SELECT * FROM Users WHERE Username = %s", (request.form["username"],))
    if cur.rowcount != 1:  # User enters a username that doesn't exist
        return json_response(
            status_=401, message="Invalid credentials", authenticated=False
        )
    user_id, username = cur.fetchone()

    # TODO: Password Authentication

    # TODO: Get user's role (user or admin)
    role = "admin"

    # Create JWT
    jwt = {"sub": username, "role": role}

    # Return JWT to authenticated user
    return json_response(token=create_token(jwt), authenticated=True)
