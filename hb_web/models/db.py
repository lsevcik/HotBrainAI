import psycopg2
from flask import current_app, g


def connect_to_database():
    connection = psycopg2.connect(
        host=current_app.config["POSTGRES_HOST"],
        dbname=current_app.config["POSTGRES_DB"],
        user=current_app.config["POSTGRES_USERNAME"],
        password=current_app.config["POSTGRES_PASSWORD"],
    )
    cursor = connection.cursor()
    return (connection, cursor)


def get_db():
    if "db" not in g:
        g.db = {}
        g.db["connection"], g.db["cursor"] = connect_to_database()

    return (g.db["connection"], g.db["cursor"])
