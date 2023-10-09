from flask import request, g, session, current_app
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token


def handle_request():
    if "books" not in session:
        session["books"] = []

    if "book_id" in request.args:
        session["books"].append(request.args["book_id"])
        current_app.logger.debug(session["books"])
    return json_response(token=create_token(g.jwt_data), books=session["books"])
