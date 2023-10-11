from flask import Blueprint

from . import login, register

api_open = Blueprint('api_open', __name__)

@api_open.post("/login")
def handle_login():
    return login.handle_request()