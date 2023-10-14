from flask import abort, request


def handle_request():
    if request.method is not "POST":
        abort(405)

    # TODO: parse through survey form resonses here

    return {}
