import csv
from flask import abort, g, request
from sqlalchemy.orm.session import Session
from models.match import *
from database import engine


def handle_request():
    if not len(request.data):
        abort(400, "No file provided")

    if (
        not request.authorization
        and request.authorization.type != "bearer"
    ):
        return {}, 400

    # Check if user exists here?
    with Session(engine) as session:
        matches = csv.reader(
            [line.decode("UTF-8") for line in request.data.splitlines()]
        )

        i = 0
        for match in matches:
            i = i + 1
            m = Match(
                user1=match[0],
                user2=match[1],
                score=match[3]
                )
            session.add(m)

        session.commit()

    return {}, 200
