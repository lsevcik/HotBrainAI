import jwt
import datetime
from flask import current_app


def create_token(token_data):
    token_data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
        days=0, minutes=30
    )
    token_data["iat"] = datetime.datetime.utcnow()

    return jwt.encode(
        token_data, current_app.config["JWT_SECRET"], algorithm="HS256"
    )
