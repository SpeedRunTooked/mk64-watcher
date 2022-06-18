'''
userId, trackSlug, timeMs, link, note, type
userId = long string gus sent (https://mk64-ad77f-default-rtdb.firebaseio.com/users.json)
trackSlug = slug from track (https://mk64-ad77f-default-rtdb.firebaseio.com/gamedata/cups.json)
link = discord link or comment str() = "Auto uploaded"
note = nopass - created automatically
type = flap OR 3lap
'''

from pathlib import Path
import json
import yaml
import requests as req


# It is expected that the payload be a dictionary with the following keys:
#
# * userID
# * tackSlug
# * timeMs
# * link
# * notes
# * type
def postTime(payload):
  url = "https://us-central1-mk64-ad77f.cloudfunctions.net/addTime"
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  # Below we are encoding the payload as form-encoded
  # If it needs to be URL-encoded, change `data` to `params
  req.post(url, headers=headers, data=payload)

#TODO - Checks for hexmap 512
#TODO - Parse into dict
#TODO - add slug

class TimeTrialData():
    course_data = [
        {'name': 'Luigi Raceway', 'id': 0, 'offset': 0, 'slug': 'luigiraceway'},
        {'name': 'Moo Moo Farm', 'id': 1, 'offset': 24, 'slug': 'moomoofarm'},
        {'name': 'Koopa Troopa Beach', 'id': 2, 'offset': 48, 'slug': 'koopatroopabeach'},
        {'name': 'Kalimari Desert', 'id': 3, 'offset': 72, 'slug': 'kalimaridesert'},
        {'name': 'Toad\'s Turnpike', 'id': 4, 'offset': 96, 'slug': 'toadsturnpike'},
        {'name': 'Frappe Snowland', 'id': 5, 'offset': 120, 'slug': 'frappesnowland'},
        {'name': 'Choco Mountain', 'id': 6, 'offset': 144, 'slug': 'chocomountain'},
        {'name': 'Mario Raceway', 'id': 7, 'offset': 168, 'slug': 'marioraceway'},
        {'name': 'Wario Stadium', 'id': 8, 'offset': 192, 'slug': 'wariostadium'},
        {'name': 'Sherbet Land', 'id': 9, 'offset': 216, 'slug': 'sherbetland'},
        {'name': 'Royal Raceway', 'id': 10, 'offset': 240, 'slug': 'royalraceway'},
        {'name': 'Bowser\'s Castle', 'id': 11, 'offset': 264, 'slug': 'bowserscastle'},
        {'name': 'D.K\'s Jungle Parkway', 'id': 12, 'offset': 288, 'slug': 'dksjungleparkway'},
        {'name': 'Yoshi Valley', 'id': 13, 'offset': 312, 'slug': 'yoshivalley'},
        {'name': 'Banshee Boardwalk', 'id': 14, 'offset': 336, 'slug': 'bansheeboardwalk'},
        {'name': 'Rainbow Road', 'id': 15, 'offset': 360, 'slug': 'rainbowroad'},
    ]

    def __init__(self, hexmap):
        self.hexmap = hexmap
        self.courseRecords = []

    def buildCourseRecord(self, course):
        '''Load all records for a single track'''
        C = CourseRecords(course['offset'], course['name'])
        C.parse_hex_data(self.hexmap)
        C.build_data()
        x = C.fetch_data()
        return x

    def buildCourseRecords(self):
        '''Build a list of all track records'''
        for course in TimeTrialData.course_data:
            dt = self.buildCourseRecord(course)
            dt['trackSlug'] = course['slug']
            dt['name'] = course['name']
            self.courseRecords.append(dt)

class CourseRecords():

    racer_ids = {
        0: 'Mario',
        1: 'Luigi',
        2: 'Yoshi',
        3: 'Toad',
        4: 'DK',
        5: 'Wario',
        6: 'Peach',
        7: ' Bowser'
    }

    def __init__(self, starting_index:int, course_name:str):
        self.starting_index = starting_index
        self.course_name = course_name
            
    def parse_hex_data(self, hexmap):
        '''Parse out hex map to extract course data'''
        x = self.starting_index
        self.raw_record_1 = hexmap[x:x+3]
        x+=3
        self.raw_record_2 = hexmap[x:x+3]
        x+=3
        self.raw_record_3 = hexmap[x:x+3]
        x+=3
        self.raw_record_4 = hexmap[x:x+3]
        x+=3
        self.raw_record_5 = hexmap[x:x+3]
        x+=3
        self.raw_record_lap = hexmap[x:x+3]
        x+=3
        self.raw_record_exists = hexmap[x:x+1]
        x+=5
        self.checksum = hexmap[x:x+1]

    def build_data(self):
        '''Convert to readable format'''
        self.record_1 = self.format_race(self.raw_record_1)
        self.record_2 = self.format_race(self.raw_record_2)
        self.record_3 = self.format_race(self.raw_record_3)
        self.record_4 = self.format_race(self.raw_record_4)
        self.record_5 = self.format_race(self.raw_record_5)
        self.record_lap = self.format_race(self.raw_record_lap)

    def format_race(self, rr):
        '''receive len 3 list of hex values, return parsed data'''

        #Convert to list of 4 digit binary
        binlist = [bin(int(y,16))[2:].zfill(4) for x in rr for y in x]

        #Extract Racer, [4]'th element
        racer_id = int(binlist[4],2)
        racer = CourseRecords.racer_ids[racer_id]

        #Extract time in centi-seconds (Append 0 to the end? For Gus' tool?)
        #It's oddly organized, have to untangle
        time_bin = binlist[5]+binlist[2]+binlist[3]+binlist[0]+binlist[1]
        time_ms = int(time_bin,2)*10

        return {'time_ms': time_ms, 'racer': racer}

    def fetch_data(self):
        '''Return a dictionary of readable info'''

        data_dict = {
            'record_1': self.record_1,
            'record_2': self.record_2,
            'record_3': self.record_3,
            'record_4': self.record_4,
            'record_5': self.record_5,
            'record_lap': self.record_lap
        }

        return data_dict

    def __str__(self):
        '''Print course data'''
        a = [
            f"RR1: {self.record_1}",
            f"RR2: {self.record_2}",
            f"RR3: {self.record_3}",
            f"RR4: {self.record_4}",
            f"RR5: {self.record_5}",
            f"RRT: {self.record_lap}",
            f"RR?: {self.raw_record_exists}",
            f"RRC: {self.checksum}"
		]
        return str(a)

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

if __name__ == '__main__':
    cfg = get_config('config.yml')
    hexmap = get_hexmap(cfg)

    TTD = TimeTrialData(hexmap)
    TTD.buildCourseRecords()
    print(TTD.courseRecords)

