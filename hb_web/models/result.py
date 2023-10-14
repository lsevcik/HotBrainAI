from models.db import get_db


class Result:
    def __init__(self, **kwargs):
        if "id" not in kwargs:
            raise ValueError()

        self.id = kwargs["id"]

        _, cur = get_db()
        cur.execute("SELECT user_id, url FROM results WHERE id = %s", (self.id,))

        self.user_id, self.url = cur.fetchone()

    # TODO: get and create methods
