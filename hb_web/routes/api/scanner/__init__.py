from flask import Blueprint
from . import get_video_for_user, put_results

api_scanner = Blueprint("api_scanner", __name__)

@api_scanner.get("/video")
def get_video():
    return get_video_for_user.handle_request()

@api_scanner.post("/result")
def post_result():
    return put_results.handle_request()