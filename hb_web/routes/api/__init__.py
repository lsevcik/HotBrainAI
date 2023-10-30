from flask import Blueprint
from werkzeug.exceptions import HTTPException

from .open import api_open
from .scanner import api_scanner

api = Blueprint("api", __name__)

api.register_blueprint(api_open, url_prefix="/open")
api.register_blueprint(api_scanner, url_prefix="/scanner")


@api.app_errorhandler(HTTPException)
def api_unauthorized(err):
    return {"status": err.code}, err.code