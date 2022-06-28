from src.utils import uploader
from src.data.game import RACER_IDS, TRACK_SLUGS


def compare_records(original, newrecords):

    for j, (old_times, new_times) in enumerate(zip(original, newrecords)):

        # Check the top 3-lap record, and the best lap record.
        # If the new record is `None`, this means the user
        # cleared thier game memory. If the old record is `None`
        # that means no record has been set before, so we proceed

        three_lap_record = new_times['track-record'].records[0]
        if old_times['track-record'].records[0] != three_lap_record and three_lap_record != None:
            new_time = three_lap_record['time']
            uploader.send_to_gus(new_time, TRACK_SLUGS[j], rtype='3lap')
            print('New 3 lap record!')

        best_lap_record = new_times['track-record'].records[5]
        if old_times['track-record'].records[5] != best_lap_record and best_lap_record != None:
            new_time = best_lap_record['time']
            uploader.send_to_gus(new_time, TRACK_SLUGS[j], rtype='flap')
            print('New lap record!')
