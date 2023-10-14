from werkzeug.exceptions import Unauthorized
from models.db import get_db


class User:
    def __init__(self, **kwargs):
        if "id" not in kwargs:
            raise ValueError()

        self.id = kwargs["id"]

        _, cur = get_db()
        cur.execute("SELECT Username FROM Users WHERE UserID = %s", (self.id,))

        (self.username,) = cur.fetchone()
        self.role = "admin"  # TODO: User roles

    @staticmethod
    def login(**kwargs):
        _, cur = get_db()
        cur.execute(
            "SELECT UserID FROM Users WHERE Username = %s", (kwargs["username"],)
        )

        if cur.rowcount != 1:  # User enters a username that doesn't exist
            raise Unauthorized("Account matching our records not found.")

        # TODO: Password Authentication

        user_id = cur.fetchone()
        return User(id=user_id)

    @staticmethod
    def register(**kwargs):
        db, cur = get_db()
        cur.execute(
            "INSERT INTO Users (Username) VALUES (%s) RETURNING UserID",
            (kwargs["username"],),
        )

        if cur.rowcount != 1:  # Operation failed for some reason
            raise Unauthorized("Account matching our records not found.")

        # TODO: Password Authentication

        db.commit()

        user_id = cur.fetchone()[0]
        return User(id=user_id)