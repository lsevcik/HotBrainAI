import csv
from flask import g, request


def handle_request():
    csv.reader(request.data)
    if g.jwt["role"] != "scanner":
        return {}, 401

    return {}, 200
