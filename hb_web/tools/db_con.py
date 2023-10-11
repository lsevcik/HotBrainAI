import psycopg2

from config import get_config

def connect_to_database():
    config = get_config()
    connection = psycopg2.connect(
        host=config["POSTGRES_HOST"],
        dbname=config["POSTGRES_DB"],
        user=config["POSTGRES_USERNAME"],
        password=config["POSTGRES_PASSWORD"],
    )
    cursor = connection.cursor()
    return (connection, cursor)

if __name__ == "__main__":
    config = get_config()
    con, cur = connect_to_database()

    cur.execute("DROP TABLE IF EXISTS Users;")
    cur.execute("CREATE TABLE Users (UserID SERIAL PRIMARY KEY, Username VARCHAR(32) UNIQUE);")
    cur.execute("INSERT INTO Users (Username) VALUES ('admin');")

    con.commit()
