#!/usr/bin/env python3.5
from simpy import Resource


class Hotel(Resource):
    """
        Each Hotel has own name, rooms(with beds capacity),
        stars and popularity.
    """
    def __init__(self, env, name, rooms, stars, popularity):
        super().__init__(env, capacity=sum(r for r in rooms))
        self.hotel_name = name
        self.hotel_stars = stars
        self.hotel_popularity = popularity

    def get_empty_rooms(self):
        return self.capacity-self.count


def get_city_config(env):
    """
    Returns dictionary with city config.

    It contains lists of instances of hotels, restaurants, cinema, places
    which can be visited by tourists.

    :param env:  simpy.Environment
    :return: dictionary
    """
    # Create Hotels  (name, list of beds in rooms, stars, popularity in %)
    hilton = Hotel(env, "Hilton", [300], 5, 90)
    puro_hotel = Hotel(env, "Puro Hotel", [150], 4, 50)

    # Make The City!
    city = {
        "hotels": [hilton, puro_hotel],
        "restaurants": [],
        "cinema": [],
        "museums": [],
        "shops": [],
    }

    return city
