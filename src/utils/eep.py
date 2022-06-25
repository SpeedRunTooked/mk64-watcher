import time
from pathlib import Path
from src.TrackRecord import TrackRecord
from src.utils.mk64 import compare_records
from src.utils.config import get_config
from src.data.game import track_names


def read_directly():
    '''Open .eep file'''
    # Get eep file
    #eepath = Path(config_dict)
    cfg = get_config()
    eepath = Path(cfg['eep-path'] + cfg['eep-file'])

    #time_bin = binlist[5]+binlist[2],binlist[3],binlist[0],binlist[1]
    f = open(eepath, 'rb')
    return [{'name': track, 'track-record': TrackRecord(f.read(24))} for track in track_names]


def watch_eep():
    '''Watch the eep file for changes'''
    orig = read_directly()
    print('Watching for new records...')

    while True:
        time.sleep(5)
        neep = read_directly()
        compare_records(orig, neep)
        orig = neep
