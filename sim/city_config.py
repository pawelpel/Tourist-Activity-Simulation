#!/usr/bin/env python3.5
from simpy import Resource
import simplejson

from ._own_functions import check_time_2, convert_time_to_min


class Hotel(Resource):
    """
        Each Hotel has own position, name, rooms(with beds capacity), popularity.
    """

    def __init__(self, env, position, name, rooms, popularity):
        super().__init__(env, capacity=rooms)
        self.position = position
        self.hotel_name = name
        self.popularity = popularity

    def get_empty_rooms(self):
        return self.capacity - self.count


class Restaurant(Resource):
    """
        Each Restaurant has own position, name, chairs(capacity of people who can be eat there at the
        same time), queue, popularity, time when it is opened and statistical visit time.
    """

    def __init__(self, env, position, name, chairs, popularity, open_from, open_to, visit_time):
        super().__init__(env, capacity=chairs)
        self.position = position
        self.restaurant_name = name
        self.popularity = popularity
        self.open_from = open_from
        self.open_to = open_to
        self.visit_time = visit_time

    def is_opened(self, env):
        return check_time_2(env, self.open_from, self.open_to)

    def is_crowded(self):
        return (self.capacity - self.count) < self.capacity * 0.1


class Musuem(Resource):
    """
        Each Museum has own position, name, capacity of people who can be eat there at the
        same time, queue, popularity, time when it is opened and statistical visit time.
    """

    def __init__(self, env, position, name, capacity, popularity, open_from, open_to, visit_time):
        super().__init__(env, capacity=capacity)
        self.position = position
        self.museum_name = name
        self.popularity = popularity
        self.open_from = open_from
        self.open_to = open_to
        self.visit_time = visit_time

    def is_opened(self, env):
        return check_time_2(env, self.open_from, self.open_to)

    def is_crowded(self):
        return (self.capacity - self.count) < self.capacity * 0.1


def get_city_config(env):
    """
    Returns dictionary with city config created from city_config.json
    or not.

    It contains lists of instances of hotels, restaurants, cinema, places
    which can be visited by tourists.

    :param env:  simpy.Environment
    :return: dictionary
    """

    hotels = []
    restaurants = []
    museums = []

    # Create Hotels (name, list of beds in rooms, stars, popularity in %)
    try:
        # todo change path to be more elastic
        file = open('city_config.json', 'rb')
        print('City config has been read!')
        city_from_file = simplejson.load(file)

        for place in city_from_file:
            if place["type"] == "hotel":
                hotels.append(Hotel(env,
                                    (place["x_m"], place["y_m"]),
                                    place["name"],
                                    int(place["capacity"]),
                                    int(place["popularity"])))

            elif place["type"] == "restaurant":
                restaurants.append(Restaurant(env,
                                              (place["x_m"], place["y_m"]),
                                              place["name"],
                                              int(place["capacity"]),
                                              int(place["popularity"]),
                                              convert_time_to_min(place["open_from"]),
                                              convert_time_to_min(place["open_to"]),
                                              convert_time_to_min(place["visittime"])))

            elif place["type"] == "museum":
                museums.append(Musuem(env,
                                      (place["x_m"], place["y_m"]),
                                      place["name"],
                                      int(place["capacity"]),
                                      int(place["popularity"]),
                                      convert_time_to_min(place["open_from"]),
                                      convert_time_to_min(place["open_to"]),
                                      convert_time_to_min(place["visittime"])))

    except FileNotFoundError:
        hotels.append(Hotel(env, (10, 0), "Blach Hotel", 230, 90))
        hotels.append(Hotel(env, (0, 10), "Duda Hotel", 145, 50))
        hotels.append(Hotel(env, (0, 0), "Gawrys Hotel", 145, 50))
        hotels.append(Hotel(env, (10, 10), "Najder Hotel", 145, 50))

    # Make The City!
    city = {
        "hotels": hotels,
        "hotels_number": len(hotels),
        "restaurants": restaurants,
        "museums": museums,
    }

    return city
