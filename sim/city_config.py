#!/usr/bin/env python3.5
from simpy import Resource
import simplejson


class Hotel(Resource):
    """
        Each Hotel has own position, name, rooms(with beds capacity), popularity.
    """
    def __init__(self, env, position, name, rooms, stars, popularity):
        super().__init__(env, capacity=rooms)
        self.position = position
        self.hotel_name = name
        self.hotel_stars = stars
        self.popularity = popularity

    def get_empty_rooms(self):
        return self.capacity-self.count


class Restaurant(Resource):
    """
        Each Restaurant has own position, name, chairs(capacity of people who can be eat there at the
        same time), queue, popularity.
    """
    def __init__(self, env, position, name, chairs, popularity):
        super().__init__(env, capacity=chairs)
        self.position = position
        self.restaurat_name = name
        self.popularity = popularity


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

    # Create Hotels (name, list of beds in rooms, stars, popularity in %)
    try:
        # todo change path to be more elastic
        file = open('city_config.json', 'rb')
        print('City config has been read!')
        city_from_file = simplejson.load(file)

        for h in city_from_file["hotels"]:
            hotels.append(Hotel(env, (h[0], h[1]), *h[2:6]))

        for r in city_from_file["restaurants"]:
            restaurants.append(Restaurant(env, *r))

    except FileNotFoundError:
        hotels.append(Hotel(env, (10, 0), "Hilton", 230, 5, 90))
        hotels.append(Hotel(env, (0, 10), "Puro Hotel", 145, 4, 50))
        hotels.append(Hotel(env, (0, 0), "Majkel Hotel", 145, 4, 50))
        hotels.append(Hotel(env, (10, 10), "Dupcio Hotel", 145, 4, 50))

    # Make The City!
    city = {
        "hotels": hotels,
        "restaurants": restaurants,
    }

    return city
