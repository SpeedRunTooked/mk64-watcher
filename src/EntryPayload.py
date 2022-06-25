# It is expected that the payload be a dictionary with the following keys:
#
# * userId
# * trackSlug
# * timeMs
# * link
# * notes
# * type

'''
userId, trackSlug, timeMs, link, note, type
userId = long string gus sent (https://mk64-ad77f-default-rtdb.firebaseio.com/users.json)
trackSlug = slug from track (https://mk64-ad77f-default-rtdb.firebaseio.com/gamedata/cups.json)
link = discord link or comment str() = "Auto uploaded"
note = nopass - created automatically
type = flap OR 3lap
'''


class EntryPayload():

    link = 'Auto Uploaded'
    notes = 'Auto Rekt'

    def __init__(self, userId: str, trackSlug: str, timeMs: int, type: str):
        self.timeMs = str(timeMs)
        self.userId = userId
        self.type = type
        self.trackSlug = trackSlug

    def to_json(self):
        return {
            'link': self.link,
            'timeMs': self.timeMs,
            'userId': self.userId,
            'trackSlug': self.trackSlug,
            'type': self.type,
            'link': self.link,
            'notes': self.notes
        }
