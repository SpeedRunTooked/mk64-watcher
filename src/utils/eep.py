import time
from pathlib import Path
from src.TrackRecord import TrackRecord
from src.utils.mk64 import compare_records, get_tracklist
from src.utils.config import get_config


def read_directly():
    '''Open .eep file'''
    # Get eep file
    #eepath = Path(config_dict)
    cfg = get_config()
    eepath = Path(cfg['eep-path'] + cfg['eep-file'])
    tracks = get_tracklist('names')

    #time_bin = binlist[5]+binlist[2],binlist[3],binlist[0],binlist[1]
    f = open(eepath, 'rb')
    return [{'name': track, 'track-record': TrackRecord(f.read(24))} for track in tracks]


def watch_eep():
    '''Watch the eep file for changes'''
    orig = read_directly()

    while True:
        time.sleep(5)
        neep = read_directly()
        compare_records(orig, neep)
        orig = neep
