import time
from pathlib import Path
from src.TrackRecord import TrackRecord
from src.utils.mk64 import mk64
from src.utils.config import get_config


def get_hexmap(config_dict):
    '''Open .eep file, convert to hexmap'''
    # Get eep file
    eeppath = Path(config_dict['eep-path'] + config_dict['eep-file'])

    with open(eeppath, 'rb') as f:
        hx = f.read().hex()

    # Convert to hexmap list
    hexmap = [hx[i:i+2] for i in range(0, len(hx), 2)]
    return(hexmap)


def read_directly():
    '''Open .eep file'''
    # Get eep file
    #eepath = Path(config_dict)
    cfg = get_config()
    eepath = Path(cfg['eep-path'] + cfg['eep-file'])
    tracks = mk64.get_tracklist('names')

    #time_bin = binlist[5]+binlist[2],binlist[3],binlist[0],binlist[1]
    f = open(eepath, 'rb')
    return [{'name': track, 'track-record': TrackRecord(f.read(24))} for track in tracks]


def watch_eep():
    '''Watch the eep file for changes'''
    orig = read_directly()

    while True:
        time.sleep(5)
        neep = read_directly()
        mk64.compare_records(orig, neep)
        orig = neep
