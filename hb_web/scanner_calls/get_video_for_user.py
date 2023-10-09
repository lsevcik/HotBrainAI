from flask import request, g, session, current_app
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token


def handle_request():
    if g.jwt['role'] is not "scanner":
        return json_response(status_=401)

    return json_response(token=create_token(g.jwt_data), books=session["books"])
