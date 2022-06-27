from src.utils import uploader
from src.data.game import RACER_IDS, TRACK_SLUGS


def compare_records(original, newrecords):

    for j, (old_times, new_times) in enumerate(zip(original, newrecords)):

        three_lap_record = new_times['track-record'].records[0]
        if old_times['track-record'].records[0] != three_lap_record and three_lap_record != None:
            # Commented these out because not being used atm
            # track_name = old_times['name']
            # racer_name = racer_ids[nr_re['character']]
            new_time = three_lap_record['time']
            uploader.send_to_gus(new_time, TRACK_SLUGS[j], rtype='3lap')
            print('New 3 lap record!')

        best_lap_record = new_times['track-record'].records[5]
        if old_times['track-record'].records[5] != best_lap_record and best_lap_record != None:
            # Commented these out because not being used atm
            # track_name = old_times['name']
            # racer_name = racer_ids[nr_re['character']]
            new_time = best_lap_record['time']
            uploader.send_to_gus(new_time, TRACK_SLUGS[j], rtype='flap')
            print('New lap record!')
