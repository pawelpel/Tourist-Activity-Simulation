#!/usr/bin/env python3.5
import random as rr

from ._own_functions import *


class Person(object):

    def __init__(self, env, city_config, person_config):
        self.env = env
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())

        # Set person profile
        self.person_config = person_config
        self.name = self.person_config["name"]

        self.have_been_at_hotel = [False for _ in range(self.person_config["trip_duration"]//time_to_min(d=1))]

        # Initial random variables
        self.have_no_time_to_find_another_hotel = False
        self.random_time_to_sleep = time_to_min(d=1, h=rr.randint(-3, 3))
        self.sleep_hours = rr.randint(6, 8)
        self.random_how_long_sleeps = time_to_min(h=self.sleep_hours)
        self.random_how_fast_he_moves = time_to_min(mi=rr.randint(3, 15))
        self.ranodm_how_fast_he_books = time_to_min(mi=rr.randint(1, 8))
        self.random_wake_up_time = time_to_min(mi=rr.randint(5, 60))
        self.ranodm_how_long_can_walk = time_to_min(h=rr.randint(4, 6))

        # Handle the city
        self.hotels = sort_hotels(city_config["hotels"])

    def run(self):
        """
            Main loop to handle person behaviour.
        """

        # Janusz arriving to the city
        yield self.env.timeout(self.person_config["arriving_time"])
        pri(self, "Arrived")

        while True:
            # Is that the end of his trip?
            if check_if_trip_is_over(self):
                break

            # Sleeping time ?
            if check_time(self, time_to_min(h=21), time_to_min(h=5)):

                # Have need to sleep that night at hotel?
                if any_not(self.have_been_at_hotel):

                    # Yes, so he is looking for a hotel
                    for hotel in self.hotels:

                        # Found one, so he is going to that hotel
                        pri(self, "Going to hotel: {}".format(hotel.hotel_name))
                        person_walking(self, 1)
                        yield self.env.timeout(self.random_how_fast_he_moves)
                        person_walking(self, 0)

                        # Is there place for him to sleep there?
                        if hotel.get_empty_rooms() > 0:
                            with hotel.request() as req:

                                # There is a bed for him
                                pri(self, "Booking time at: {}".format(hotel.hotel_name))
                                yield req
                                yield self.env.timeout(self.ranodm_how_fast_he_books)

                                # Janusz goes to bed
                                pri(self, "Sleeping for next {}h".format(self.sleep_hours))
                                yield self.env.timeout(self.random_how_long_sleeps)
                                self.have_been_at_hotel.pop()

                                # Janusz wake up
                                pri(self, "Time to wake up")
                                yield self.env.timeout(self.random_wake_up_time)

                                # Leeaving the hotel
                                pri(self, "Leaving {}".format(hotel.hotel_name))
                                break

                        # No there is not any bed for him
                        else:
                            pri(self, "No place to sleep at {}".format(hotel.hotel_name))

            # No, its not sleeping time
            pri(self, "Walking")
            person_walking(self, 1)
            yield self.env.timeout(self.ranodm_how_long_can_walk)
            person_walking(self, 0)

            # TODO eating, sightseeing, museums, other atractions
