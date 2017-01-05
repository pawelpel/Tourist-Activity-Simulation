#!/usr/bin/env python3.5
import simpy
import simplejson

from ._own_functions import time_to_min, init_text_to_write_receiver
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

    env.receiver = init_text_to_write_receiver(simplejson.dumps(options) + places_capacity)
    next(env.receiver)

    # Create People using individual configuration
    for i in range(options["how_many_people"]):
        person_config = get_person_config(env, i)
        _ = Person(env, city_config, person_config)

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

        # Check if something new has happend
        if last_env_time is not None and env_time != last_env_time:

            # Get city's attractions to prepare simulation's state report
            for h in city_config["hotels"]:
                hotels_report[h.hotel_name] = h.count
            for r in city_config["restaurants"]:
                restaurants_report[r.restaurant_name] = (r.count, int(r.is_opened(env)), int(r.is_crowded()))
            for m in city_config["museums"]:
                museums_report[m.museum_name] = (m.count, int(m.is_opened(env)), int(m.is_crowded()))

            # Creating simulations state report
            report = {
                "TIM": env_time,
                "WP": env.walking_people,
                "HR": hotels_report,
                "RR": restaurants_report,
                "MR": museums_report
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
    default_options["map_size_x"] = 2000*590//1000  # px * 590//1000
    default_options["map_size_y"] = 2844*590//1000
    default_options["how_long"] = time_to_min(d=2)  # mi, h, d, y
    default_options["how_many_people"] = 10000
    default_options["whats_the_weather"] = 'sunny'  # 'sunny', 'windy', 'rainy'
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
