from flask import request, g, session, current_app
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.db_con import get_db

def handle_request():
    db, cur = get_db()

    # TODO: get logged in user's matches, return as a JSON array

    return json_response(token=create_token(g.jwt_data), matches=[])
