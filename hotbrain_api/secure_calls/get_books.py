from flask import request, g, session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    if 'books' not in session:
        session.books = []
    session.books.append(request.args)
    logger.debug(session.books)
    return json_response(token = create_token(g.jwt_data), books = session.books)