#!/usr/bin/env python3.5
import simpy
import simplejson
import random

from ._own_functions import time_to_min, init_text_to_write_receiver, min_to_date
from .city_config import get_city_config
from .person_class import Person
from .person_config import get_person_config


def set_interuptions(env, options, person, when_starts, when_stops):
    # Rain ?
    if options["whats_the_weather"] == 'rainy':
        yield env.timeout(when_starts)
        env.is_raining = True
        try:
            if person.is_sightseeing:
                person.action.interrupt()
        except RuntimeError:
            pass
        yield env.timeout(when_stops - when_starts)
        env.is_raining = False


# @time_it # <- dont use when fun is yielding
def run_simulation(options):

    # Create an Environment
    env = simpy.Environment()
    city_config = get_city_config(env)

    # How big is the map
    env.map_size_x = options["map_size_x"]
    env.map_size_y = options["map_size_y"]

    # How many people are currently walking
    env.walking_people = 0

    # How many people are currently in the hotel outside the area
    env.at_outside_hotel = 0

    # How many people are currently in the hotel outside the area
    env.walked_meters = 0

    # Which month is it? To set statistics properly.
    env.month = options["month"]

    # Init sim_agents_log file
    hotels_sum_of_capacity = restaurants_sum_of_capacity = museum_sum_of_capacity = 0

    for h in city_config["hotels"]:
        hotels_sum_of_capacity += h.capacity
    for r in city_config["restaurants"]:
        restaurants_sum_of_capacity += r.capacity
    for m in city_config["museums"]:
        if m.capacity < 9999:
            museum_sum_of_capacity += m.capacity

    places_capacity = """
        sum of capacity of:
        hotels          {}
        restaurants     {}
        museums         {}
        """.format(hotels_sum_of_capacity, restaurants_sum_of_capacity, museum_sum_of_capacity)

    env.receiver = init_text_to_write_receiver(simplejson.dumps(options, indent=4 * ' ') + places_capacity)
    next(env.receiver)

    min_rain = 30
    rain_at = random.randint(0, options["how_long"]-min_rain)
    rain_to = random.randint(rain_at+min_rain, options["how_long"])
    env.is_raining = False
    # Create People using individual configuration
    for i in range(options["how_many_people"]):
        person_config = get_person_config(env, i)
        person = Person(env, city_config, person_config)
        env.process(set_interuptions(env, options, person, rain_at, rain_to))

    # Init variables for report
    hotels_report = {}
    restaurants_report = {}
    museums_report = {}

    # Start Simulation
    last_env_time = None
    until = options["how_long"]
    while env.peek() < until:
        env.step()
        env_time = env.now

        if last_env_time is None:
            last_env_time = env_time

        # Check if something new has happend
        delay = 5
        if env_time % delay == 0 and last_env_time != env_time:

            # Get city's attractions to prepare simulation's state report
            for h in city_config["hotels"]:
                hotels_report[h.hotel_name] = h.count
            for r in city_config["restaurants"]:
                restaurants_report[r.restaurant_name] = (r.count, int(r.is_opened(env)))
            for m in city_config["museums"]:
                museums_report[m.museum_name] = (m.count, int(m.is_opened(env)))

            # Creating simulations state report
            report = {
                "TT": str(min_to_date(env_time)),
                "T": env_time,
                "W": env.walking_people,
                "R": env.is_raining,
                "H": hotels_report,
                "OH": env.at_outside_hotel,
                "RR": restaurants_report,
                "M": museums_report,
                "ME": int(env.walked_meters),
            }

            # Sending/Printing/Whatever connected with report
            yield report

        last_env_time = env_time


def dict_options():
    return {'map_size_x': None,
            'map_size_y': None,
            'how_long': None,
            'how_many_people': None,
            'whats_the_weather': None,
            'when_it_happens': None,
            'month': None}


def get_default_options():
    default_options = dict_options()
    default_options["map_size_x"] = 2000*590//1000  # px * 590//1000
    default_options["map_size_y"] = 2844*590//1000
    default_options["how_long"] = time_to_min(d=3)  # mi, h, d, y
    default_options["how_many_people"] = 5000
    default_options["whats_the_weather"] = 'rainy'  # 'sunny', 'rainy'
    default_options["when_it_happens"] = 'weekday'  # 'weekday', 'weekend', 'vacation'
    default_options["month"] = 2
    return default_options


def main_sim():
    # for r in run_simulation(get_default_options()):
    #     print(r)
    #     pass

    import cProfile
    cProfile.run('for r in run_simulation(get_default_options()):\n\tpass')


if __name__ == "__main__":
    main_sim()
