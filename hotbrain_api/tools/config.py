import yaml
import os

def get_config():
    with open(os.path.join(os.path.dirname(__file__), '..', 'config.yml')) as yml_file:
        return yaml.safe_load(yml_file)

if __name__ == "__main__":
    print(get_config())