import psycopg2
import yaml
import os


def get_db():
    yml_configs = {}
    with open(os.path.join(os.path.dirname(__file__), '..', 'config.yml')) as yml_file:
        yml_configs = yaml.safe_load(yml_file)
    return psycopg2.connect(host=yml_configs['database']['host'], dbname=yml_configs['database']['name'], user=yml_configs['database']['username'], password=yml_configs['database']['password'])

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor()

    return db, cur

if __name__ == "__main__":
    yml_configs = {}
    with open(os.path.join(os.path.dirname(__file__), '..', 'config.yml')) as yml_file:
        yml_configs = yaml.safe_load(yml_file)
    db, cur = get_db_instance()

    cur.execute("DROP TABLE IF EXISTS Users;")
    cur.execute("CREATE TABLE Users (UserID SERIAL PRIMARY KEY, Username VARCHAR(32));")
    cur.execute("INSERT INTO Users (Username) VALUES ('admin');")

    db.commit()