from pathlib import Path

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
                           'time' : f * 2 ** 16 + c * 2 ** 12 + d * 2 ** 8 + a * 2 ** 4 + b})

def read_directly(config_dict):
    '''Open .eep file'''
    #Get eep file
    #eepath = Path('/mnt/a/Emulators/P64/Save/MARIOKART64-97AC600799CF6EC717D19E5AA5DA8AE8/MARIOKART64.eep')
    eepath = Path(config_dict['eep-path'] + config_dict['eep-file'])
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

if __name__ == '__main__':
  a = read_directly(None)
  for track in a:
    print(track['track-record'].records)