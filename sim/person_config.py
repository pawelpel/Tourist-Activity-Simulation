#!/usr/bin/env python3.5
import random

from ._own_functions import time_to_min, min_to_date

# SOURCE
# http://www.mot.krakow.pl/media/badanie-ruchu-turystycznego/badania_ruch_tur_2015.pdf


def get_person_config(env, i):

    # Chance to be PL
    month = env.month
    main_chance = 51.3
    months_chance = [58.9, 61.4, 54.7, 50.4, 50.0, 51.8, 46.0, 45.0, 47.8, 47.4, 59.4, 55.2]
    if month:
        chance_to_pl = months_chance[month-1]
    else:
        chance_to_pl = main_chance
    is_pl = random.randint(0, 100) >= chance_to_pl

    # Trip duration depending on being PL or not
    # in order:    <3h,   24h,   1n,    2-3n, 4-7n,  >7n, bd            n-sleeping night, bd-don't know
    durations_times = [time_to_min(h=3),
                       time_to_min(d=1),
                       time_to_min(d=1.5),
                       time_to_min(d=3),
                       time_to_min(d=7)]
    durations_pl = [5.27, 16.26, 20.78, 28.5, 23.41, 4.9, 0.88]
    durations_not_pl = [0.88, 1.5, 9.35, 32.97, 44.6, 8.32, 2.38]
    durations = durations_pl if is_pl else durations_not_pl
    get_random = random.randint(0, 100)
    duration = None
    for d in range(len(durations)-2):
        if sum(durations[:d]) < get_random < sum(durations[:d+1]):
            duration = durations_times[d]
            break
    if not duration:
        duration = time_to_min(h=random.randint(3, 24 * 7))

    peron_config = {
        "name": "Person {}".format(i+1),
        "is_pl": is_pl,
        "arriving_time": random.randint(0, 12*60),
        "trip_duration": duration,
    }

    return peron_config
