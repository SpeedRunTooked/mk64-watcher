from src.utils import uploader
from src.data.game import racer_ids, track_slugs, default_record_time


def compare_records(original, newrecords):

    for j, (old_times, new_times) in enumerate(zip(original, newrecords)):
        for i, (or_re, nr_re) in enumerate(zip(old_times['track-record'].records, new_times['track-record'].records)):
            if i > 4:
                break
            if or_re != nr_re:
                # Commented these out because not being used atm
                # track_name = old_times['name']
                # racer_name = racer_ids[nr_re['character']]
                new_time = nr_re['time']
                # We don't need to send the time to the server if it's the
                # default time. This deals with the case where a user deleted
                # their saved game.
                if new_time == default_record_time:
                    continue
                uploader.send_to_gus(new_time, track_slugs[j], rtype="3lap")
                print('New top 5 race time!')
                break

        if old_times['track-record'].records[5] != new_times['track-record'].records[5]:
            # Commented these out because not being used atm
            # track_name = old_times['name']
            # racer_name = racer_ids[nr_re['character']]
            new_time = new_times['track-record'].records[5]['time']
            uploader.send_to_gus(new_time, track_slugs[j], rtype='flap')
            print('New lap record!')
