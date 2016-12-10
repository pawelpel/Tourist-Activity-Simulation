#!/usr/bin/env python3.5
from simpy import Resource


class Hotel(Resource):
    """
        Each Hotel has own position, name, rooms(with beds capacity), popularity.
    """
    def __init__(self, env, position, name, rooms, stars, popularity):
        super().__init__(env, capacity=sum(r for r in rooms))
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
    Returns dictionary with city config.

    It contains lists of instances of hotels, restaurants, cinema, places
    which can be visited by tourists.

    :param env:  simpy.Environment
    :return: dictionary
    """
    # Create Hotels  (name, list of beds in rooms, stars, popularity in %)
    hilton = Hotel(env, (10, 0), "Hilton", [230], 5, 90)
    puro_hotel = Hotel(env, (0, 10), "Puro Hotel", [145], 4, 50)
    majkel_hotel = Hotel(env, (0, 0), "Majkel Hotel", [145], 4, 50)
    dupcio_hotel = Hotel(env, (10, 10), "Dupcio Hotel", [145], 4, 50)

    # Make The City!
    city = {
        "hotels": [hilton, puro_hotel, majkel_hotel, dupcio_hotel],
        "restaurants": [],
        "cinema": [],
        "museums": [],
        "shops": [],
    }

    return city
