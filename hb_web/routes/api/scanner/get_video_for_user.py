from flask import g


def handle_request():
    if g.jwt["role"] is not "scanner":
        return {}, 401

    return {"videos": [""]}
