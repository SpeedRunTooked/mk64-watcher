from src.utils import uploader
from src.data.game import RACER_IDS, TRACK_SLUGS


def compare_records(original, newrecords):

    for j, (old_times, new_times) in enumerate(zip(original, newrecords)):
        for i, (or_re, nr_re) in enumerate(zip(old_times['track-record'].records, new_times['track-record'].records)):
            if i > 4:
                break
            # If the new record (nr_re) is `None`, this means that the user
            # clear their game memory. If the old record is `None`, we don't
            # care, we still want to upload the new time.
            if or_re != nr_re and nr_re != None:
                # Commented these out because not being used atm
                # track_name = old_times['name']
                # racer_name = racer_ids[nr_re['character']]
                new_time = nr_re['time']
                uploader.send_to_gus(new_time, TRACK_SLUGS[j], rtype="3lap")
                print('New top 5 race time!')
                break

        best_lap_record = new_times['track-record'].records[5]
        if old_times['track-record'].records[5] != best_lap_record and best_lap_record != None:
            # Commented these out because not being used atm
            # track_name = old_times['name']
            # racer_name = racer_ids[nr_re['character']]
            new_time = best_lap_record['time']
            uploader.send_to_gus(new_time, TRACK_SLUGS[j], rtype='flap')
            print('New lap record!')
