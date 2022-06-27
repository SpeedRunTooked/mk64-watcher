import yaml
from pathlib import Path


FILENAME = 'config.yml'


def get_config():
    '''return yaml config file'''
    # Open yaml config
    with open(Path(FILENAME), 'r') as f:
        config_dict = yaml.safe_load(f)

    return config_dict
