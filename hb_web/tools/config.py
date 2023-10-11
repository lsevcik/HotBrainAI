from flask.config import Config
from os import path

def get_config():
    config = Config(path.join(path.dirname(__file__), ".."))
    config.from_pyfile(filename="config.cfg")
    return config

if __name__ == "__main__":
    print(get_config())
