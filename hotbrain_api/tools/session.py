import jwt
from functools import wraps
from flask import request, redirect, g, session
from flask_json import FlaskJSON, JsonError, json_response, as_json

from tools.logging import logger

from tools.get_aws_secrets import get_secrets


def start_session(f):
    @wraps(f)
    def _start(*args, **kwargs):
        if 'username' not in session:
            session['username'] = g.jwt_data['sub']
    
        return f(*args, **kwargs)

    return _start

