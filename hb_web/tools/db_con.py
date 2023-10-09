import psycopg2
from flask import current_app, g

from tools.config import get_config


def connect_to_database():
    config = get_config()
    connection = psycopg2.connect(
        host=config["database"]["host"],
        dbname=config["database"]["name"],
        user=config["database"]["username"],
        password=config["database"]["password"],
    )
    cursor = connection.cursor()
    return (connection, cursor)


def get_db():
    if "db" not in g:
        g.db = {}
        g.db['connection'], g.db['cursor'] = connect_to_database()

    return (g.db['connection'], g.db['cursor'])


if __name__ == "__main__":
    config = get_config()
    db, cur = get_db()

    cur.execute("DROP TABLE IF EXISTS Users;")
    cur.execute("CREATE TABLE Users (UserID SERIAL PRIMARY KEY, Username VARCHAR(32));")
    cur.execute("INSERT INTO Users (Username) VALUES ('admin');")

    db.commit()
