from src.utils import uploader


def compare_records(original, newrecords):
    racer_ids = get_racer_ids()
    slugs = get_tracklist('slugs')

    for j, (old_times, new_times) in enumerate(zip(original, newrecords)):
        for i, (or_re, nr_re) in enumerate(zip(old_times['track-record'].records, new_times['track-record'].records)):
            if i > 4:
                break
            if or_re != nr_re:
                # Commented these out because not being used atm
                # track_name = old_times['name']
                # racer_name = racer_ids[nr_re['character']]
                slug = slugs[j]
                new_time = nr_re['time']
                uploader.send_to_gus(new_time, slug, rtype="3lap")
                break

        if old_times['track-record'].records[5] != new_times['track-record'].records[5]:
            # Commented these out because not being used atm
            # track_name = old_times['name']
            # racer_name = racer_ids[nr_re['character']]
            new_time = new_times['track-record'].records[5]['time']
            uploader.send_to_gus(new_time, slugs[j], rtype='flap')


def get_racer_ids():
    return [
        'Mario',
        'Luigi',
        'Yoshi',
        'Toad',
        'DK',
        'Wario',
        'Peach',
        ' Bowser'
    ]


def get_tracklist(listType):

    if (listType == 'names'):
        return ['Luigi Raceway',
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

    if (listType == 'slugs'):
        return [
            'luigiraceway',
            'moomoofarm',
            'koopatroopabeach',
            'kalimaridesert',
            'toadsturnpike',
            'frappesnowland',
            'chocomountain',
            'marioraceway',
            'wariostadium',
            'sherbetland',
            'royalraceway',
            'bowserscastle',
            'dksjungleparkway',
            'yoshivalley',
            'bansheeboardwalk',
            'rainbowroad'
        ]

    raise Exception('Tracklist type not specified or incorrect.')
