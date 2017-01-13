#!/usr/bin/env python3.5
import random

from .own_functions import time_to_min

# SOURCE
# http://www.mot.krakow.pl/media/badanie-ruchu-turystycznego/badania_ruch_tur_2015.pdf


def get_person_config(env, i):
    """
        Returns dict with generated data (from statisticks) about one person.
    """
    name = "Person {}".format(i+1)
    arriving_time = random.randint(0, 12 * 60)

    # Chance to be from PL
    month = env.month
    months_avg_chance = 51.3
    months_chance = [58.9, 61.4, 54.7, 50.4, 50.0, 51.8, 46.0, 45.0, 47.8, 47.4, 59.4, 55.2]
    if 0 < month <= 12:
        chance_to_pl = months_chance[month-1]
    else:
        chance_to_pl = months_avg_chance
    person_is_pl = random.randint(0, 100) >= chance_to_pl

    # Trip duration depending on being from PL or from other country
    # in order:    <3h,   24h,   1n,    2-3n, 4-7n,  >7n, bd            n-sleeping night, bd-don't know
    durations_times = [time_to_min(h=3),
                       time_to_min(d=1),
                       time_to_min(d=2),
                       time_to_min(d=3),
                       time_to_min(d=7)]

    durations_pl = [5.27, 16.26, 20.78, 28.5, 23.41, 4.9, 0.88]
    durations_not_pl = [0.88, 1.5, 9.35, 32.97, 44.6, 8.32, 2.38]

    durations = durations_pl if person_is_pl else durations_not_pl
    duration = None
    # Choose trip duration
    random_number = random.randint(0, 100)
    for d in range(len(durations)-2):
        if sum(durations[:d]) < random_number < sum(durations[:d+1]):
            duration = durations_times[d]
            break
    if not duration:
        duration = time_to_min(h=random.randint(3, 24 * 7))

    # First position
    first_position = (random.randint(0, env.map_size_x), random.randint(0, env.map_size_y))

    # Set personal configuration
    peron_config = {
        "name": name,
        "person_is_pl": person_is_pl,
        "arriving_time": arriving_time,
        "trip_duration": duration,
        "first_position": first_position,
    }

    return peron_config
