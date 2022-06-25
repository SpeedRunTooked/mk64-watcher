from src.utils import uploader
from src.data.game import racer_ids, track_slugs


def compare_records(original, newrecords):
    # Commented this out because not being used atm

    for j, (old_times, new_times) in enumerate(zip(original, newrecords)):
        for i, (or_re, nr_re) in enumerate(zip(old_times['track-record'].records, new_times['track-record'].records)):
            if i > 4:
                break
            if or_re != nr_re:
                # Commented these out because not being used atm
                # track_name = old_times['name']
                # racer_name = racer_ids[nr_re['character']]
                new_time = nr_re['time']
                uploader.send_to_gus(new_time, track_slugs[j], rtype="3lap")
                break

        if old_times['track-record'].records[5] != new_times['track-record'].records[5]:
            # Commented these out because not being used atm
            # track_name = old_times['name']
            # racer_name = racer_ids[nr_re['character']]
            new_time = new_times['track-record'].records[5]['time']
            uploader.send_to_gus(new_time, track_slugs[j], rtype='flap')
