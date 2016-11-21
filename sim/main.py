#!/usr/bin/env python3.5
import simpy
from collections import deque

from ._own_functions import time_to_min, time_it, min_to_date
from .city_config import get_city_config
from .person_class import Person
from .person_config import get_person_config


# @time_it # <- dont use when fun is yielding
def run_simulation(options):

    # Create an Environment
    env = simpy.Environment()
    city_config = get_city_config(env)

    # Who is curently walking
    env.walking_people = deque()

    # Which month is it? To set statistics properly.
    env.month = options["month"]

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

            # Get city's attractions to prepare simulation's state raport
            hotels_raport = {}
            for k in city_config["hotels"]:
                hotels_raport[k.hotel_name] = {"interaction_with": k.count}

            # Creating simulations state raport
            report = {
                "TIM": env_time,
                "TIDF": str(min_to_date(env.now)),
                "WP": len(env.walking_people),
                "HR": hotels_raport,
            }

            # Sending/Printing/Whatever
            yield report

        last_env_time = env_time


def options():
    return {'how_long': None,
            'how_many_people': None,
            'whats_the_weather': None,
            'when_it_happens': None,
            'month': None}


def get_default_options():
    default_options = options()
    default_options["how_long"] = time_to_min(d=5)  # mi, h, d, y
    default_options["how_many_people"] = 1000
    default_options["whats_the_weather"] = 'sunny'  # 'sunny', 'windy', 'rainy'
    default_options["when_it_happens"] = 'weekday'  # 'weekday', 'weekend', 'vacation'
    default_options["month"] = 2
    return default_options


def main_sim():
    for r in run_simulation(get_default_options()):
        print(r)
        pass

if __name__ == "__main__":
    main_sim()
