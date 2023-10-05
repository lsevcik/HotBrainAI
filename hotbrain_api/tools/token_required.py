import jwt
from functools import wraps
from flask import request, redirect, g, current_app
from flask_json import FlaskJSON, JsonError, json_response, as_json

from tools.get_aws_secrets import get_secrets


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        secrets = get_secrets()
        auth_headers = request.headers.get("Authorization", "").split(":")

        invalid_msg = {
            "message": "Invalid token. Registeration and / or authentication required",
            "authenticated": False,
        }
        expired_msg = {
            "message": "Expired token. Reauthentication required.",
            "authenticated": False,
        }

        if len(auth_headers) != 2:
            return json_response(status_=401, message=invalid_msg)

        try:
            token = auth_headers[1]
            data = jwt.decode(token, secrets["JWT"], algorithms=["HS256"])
            g.jwt_data = data
        except jwt.ExpiredSignatureError:
            return json_response(status_=401, message=expired_msg)
        except (jwt.InvalidTokenError, Exception) as e:
            current_app.logger.debug(e)
            return json_response(status_=401, message=invalid_msg)
        return f(*args, **kwargs)

    return _verify
