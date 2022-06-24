'''
userId, trackSlug, timeMs, link, note, type
userId = long string gus sent (https://mk64-ad77f-default-rtdb.firebaseio.com/users.json)
trackSlug = slug from track (https://mk64-ad77f-default-rtdb.firebaseio.com/gamedata/cups.json)
link = discord link or comment str() = "Auto uploaded"
note = nopass - created automatically
type = flap OR 3lap
'''
#TODO - Checks for hexmap 512

from pathlib import Path
import json
import yaml
import requests as req
import itertools
import time


global_cfg = None

# It is expected that the payload be a dictionary with the following keys:
#
# * userId
# * trackSlug
# * timeMs
# * link
# * notes
# * type
def post_time(payload):
  url = "https://us-central1-mk64-ad77f.cloudfunctions.net/addTime"
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  # Below we are encoding the payload as form-encoded
  # If it needs to be URL-encoded, change `data` to `params
  return req.post(url, headers=headers, data=payload)



def get_config(filename):
    '''return yaml config file'''
    #Open yaml config
    with open(Path(filename), 'r') as f:
        config_dict = yaml.safe_load(f)

    return config_dict

def get_hexmap(config_dict):
    '''Open .eep file, convert to hexmap'''
    #Get eep file
    eeppath = Path(config_dict['eep-path'] + config_dict['eep-file'])

    with open(eeppath, 'rb') as f:
        hx = f.read().hex()

    #Convert to hexmap list
    hexmap = [hx[i:i+2] for i in range(0, len(hx), 2)]
    return(hexmap)


class TrackRecord():
    def __init__(self, bs):

        self.records = []
        for i in range(0,18,3):
            a = bs[i+0] >> 4
            b = bs[i+0] & 0b00001111
            c = bs[i+1] >> 4
            d = bs[i+1] & 0b00001111
            e = bs[i+2] >> 4
            f = bs[i+2] & 0b00001111
            self.records.append({'character' : e, 
                                'time' : (f * 2 ** 16 + c * 2 ** 12 + d * 2 ** 8 + a * 2 ** 4 + b)*10})

    def __str__(self):
        
        return str([str(record) for record in self.records])

def read_directly():
    '''Open .eep file'''
    #Get eep file
    #eepath = Path(config_dict)
    eepath = Path(global_cfg['eep-path'] + global_cfg['eep-file'])
    tracks = ['Luigi Raceway',
              'Moo Moo Farm',
              'Koopa Troopa Beach',
              'Kalimari Desert',
              'Toad\'s Turnpike',
              'Frappe Snowland',
              'Choco Mountain',
              'Mario Raceway',
              'Wario Stadium',
              'Sherbet Land',
              'Royal Raceway',
              'Bowser\'s Castle',
              'D.K\'s Jungle Parkway',
              'Yoshi Valley',
              'Banshee Boardwalk',
              'Rainbow Road']

    #time_bin = binlist[5]+binlist[2],binlist[3],binlist[0],binlist[1]
    f = open(eepath, 'rb')
    return [{'name': track, 'track-record': TrackRecord(f.read(24))} for track in tracks]

def compare_records(original, newrecords):
    racer_ids = [
        'Mario',
        'Luigi',
        'Yoshi',
        'Toad',
        'DK',
        'Wario',
        'Peach',
        ' Bowser'
    ]

    slugs = [
        "luigiraceway",
        "moomoofarm",
        "koopatroopabeach",
        "kalimaridesert",
        "toadsturnpike",
        "frappesnowland",
        "chocomountain",
        "marioraceway",
        "wariostadium",
        "sherbetland",
        "royalraceway",
        "bowserscastle",
        "dksjungleparkway",
        "yoshivalley",
        "bansheeboardwalk",
        "rainbowroad"
    ]

    for j, (ot, nt) in enumerate(zip(original,newrecords)):
        for i, (or_re,nr_re) in enumerate(zip(ot['track-record'].records, nt['track-record'].records)):
            if i > 4:
                break
            if or_re != nr_re:
                track_name = ot['name']
                racer_name = racer_ids[nr_re['character']]
                slug = slugs[j]
                new_time   = nr_re['time']
                send_to_gus(track_name, racer_name, new_time, slug, rtype="3lap")
                break
        
        if ot['track-record'].records[5] != nt['track-record'].records[5]:
            track_name = ot['name']
            racer_name = racer_ids[nr_re['character']]
            new_time   = nt['track-record'].records[5]['time']
            send_to_gus(track_name, racer_name, new_time, slugs[j], rtype='flap')
            
def send_to_gus(track_name, racer_name, new_time, slug, rtype="NA"):
    payload = {
        'userId'  : global_cfg['userID'],
        'trackSlug': slug,
        'timeMs'  : str(new_time),
        'link'    : "Auto Uploaded",
        'notes'   : "Auto Rekt",
        'type'    : rtype
    }

    r = post_time(payload)
    print(r.text)
    print(r.url)

def watch_eep():
    '''Watch the eep file for changes'''
    orig = read_directly()

    while True:
        time.sleep(5)
        neep = read_directly()
        compare_records(orig, neep)
        orig = neep

if __name__ == '__main__':
    cfg = get_config('config.yml')
    global_cfg = cfg
    watch_eep()

