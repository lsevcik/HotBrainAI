from flask.config import Config
from os import path


def get_config():
    config = Config(path.join(path.dirname(__file__), ".."))
    try:
        config.from_pyfile(filename="config.cfg")
    except OSError:
        print("Failed to load config.cfg")
    config.from_prefixed_env()
    
    return config


if __name__ == "__main__":
    print(get_config())
