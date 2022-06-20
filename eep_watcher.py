'''
Monitor the .eep file for changes,
execute code when a change is detected
'''
import time
from pathlib import Path
import yaml



def watch_eep():
    '''Watch the eep file for changes'''

def get_config(filename):
    '''return yaml config file'''
    #Open yaml config
    with open(Path(filename), 'r') as f:
        config_dict = yaml.safe_load(f)

    return config_dict

if __name__ == '__main__':
    cfg = get_config('config.yml')