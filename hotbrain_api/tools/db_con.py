import psycopg2
from tools.config import get_config


def get_db():
    config = get_config()
    return psycopg2.connect(host=config['database']['host'], dbname=config['database']['name'], user=config['database']['username'], password=config['database']['password'])

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor()

    return db, cur

if __name__ == "__main__":
    config = get_config()
    db, cur = get_db_instance()

    cur.execute("DROP TABLE IF EXISTS Users;")
    cur.execute("CREATE TABLE Users (UserID SERIAL PRIMARY KEY, Username VARCHAR(32));")
    cur.execute("INSERT INTO Users (Username) VALUES ('admin');")

    db.commit()