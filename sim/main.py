#!/usr/bin/env python3.5
import simpy

from ._own_functions import time_to_min, time_it
from .city_config import get_city_config
from .person_class import Person
from .person_config import get_person_config


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

    # Which month is it? To set statistics properly.
    env.month = options["month"]

    # Init variables for report
    hotels_report = {}
    restaurants_report = {}

    # Create People using individual configuration
    for i in range(options["how_many_people"]):
        person_config = get_person_config(env, i)
        _ = Person(env, city_config, person_config)

    # Start Simulation
    last_env_time = None
    until = options["how_long"]
    while env.peek() < until:
        env.step()
        env_time = env.now

        # Check if something new has happend
        if last_env_time is not None and env_time != last_env_time:

            # Get city's attractions to prepare simulation's state report
            for k in city_config["hotels"]:
                hotels_report[k.hotel_name] = k.count
            for r in city_config["restaurants"]:
                restaurants_report[r.restaurant_name] = r.count

            # Creating simulations state report
            report = {
                "TIM": env_time,
                "WP": env.walking_people,
                "HR": hotels_report,
                "RR": restaurants_report,
            }

            # Sending/Printing/Whatever connected with report
            yield report

        last_env_time = env_time


def options():
    return {'map_size_x': None,
            'map_size_y': None,
            'how_long': None,
            'how_many_people': None,
            'whats_the_weather': None,
            'when_it_happens': None,
            'month': None}


def get_default_options():
    default_options = options()
    default_options["map_size_x"] = 1000
    default_options["map_size_y"] = 1000
    default_options["how_long"] = time_to_min(d=3)  # mi, h, d, y
    default_options["how_many_people"] = 100
    default_options["whats_the_weather"] = 'sunny'  # 'sunny', 'windy', 'rainy'
    default_options["when_it_happens"] = 'weekday'  # 'weekday', 'weekend', 'vacation'
    default_options["month"] = 2
    return default_options


def main_sim():
    # for r in run_simulation(get_default_options()):
        # print(r)
        # pass

    import cProfile
    cProfile.run('for r in run_simulation(get_default_options()):\n\tpass')


if __name__ == "__main__":
    main_sim()
