from src.data.game import default_record

class TrackRecord:

    def __init__(self, bs):

        if bs == default_record:
          self.records.append(None)
          return
        self.records = []
        for i in range(0, 18, 3):
            a = bs[i+0] >> 4
            b = bs[i+0] & 0b00001111
            c = bs[i+1] >> 4
            d = bs[i+1] & 0b00001111
            e = bs[i+2] >> 4
            f = bs[i+2] & 0b00001111

            record = {'character': e, 'time': (
                f * 2 ** 16 + c * 2 ** 12 + d * 2 ** 8 + a * 2 ** 4 + b)*10}

            self.records.append(record)

    def __str__(self) -> str:

        return str([str(record) for record in self.records])
