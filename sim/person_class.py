#!/usr/bin/env python3.5
import random as ra

from ._own_functions import *


class Person(object):

    def __init__(self, env, city_config, person_config):
        self.env = env
        # # Start the run process everytime an instance is created.
        self.action = env.process(self.run())

        self.person_config = person_config

        # # Set person profile
        self.name = self.person_config["name"]

        # trip
        self.janusz_arriving_time = self.person_config["arriving_time"]
        self.janusz_trip_duration = self.person_config["trip_duration"]
        self.janusz_actual_trip_duration = self.janusz_arriving_time + self.janusz_trip_duration

        # hotel
        self.janusz_goes_to_sleep_at_h = ra.randint(21, 24)
        self.janusz_goes_to_sleep_at_min = time_to_min(h=self.janusz_goes_to_sleep_at_h)
        self.janusz_cant_go_to_sleep_at_min = time_to_min(h=(24 - self.janusz_goes_to_sleep_at_h + ra.randint(1, 4)))

        self.janusz_nights_at_hotel = [False for _ in range(self.janusz_trip_duration // time_to_min(d=1))]
        self.janusz_sleeps_for_about_h = ra.randint(6, 8)
        self.janusz_sleeps_for_about_min = time_to_min(h=self.janusz_sleeps_for_about_h)

        # walking
        self.janusz_avg_siqghtseeing_time = time_to_min(h=ra.randint(3, 5))
        self.janusz_avg_walking_time = time_to_min(mi=ra.randint(3, 15))

        # global actions
        self.janusz_avg_organization_time = time_to_min(mi=ra.randint(5, 15))

        # # Handle the city
        self.hotels = sort_hotels(city_config["hotels"])

    def run(self):
        """
            Main loop to handle person behaviour.
        """

        # Janusz arriving to the city
        yield self.env.timeout(self.janusz_arriving_time)
        pri(self, "Arrived")

        while True:
            # Is that the end of his trip?
            if check_if_trip_is_over(self, self.janusz_actual_trip_duration):
                break

            # Sleeping time ?
            if check_time(self, self.janusz_goes_to_sleep_at_min, self.janusz_cant_go_to_sleep_at_min):

                # Have need to sleep that night at hotel?
                if any_night(self.janusz_nights_at_hotel):

                    # Yes, so he is looking for a hotel
                    for hotel in self.hotels:

                        # Found one, so he is going to that hotel
                        pri(self, "Going to hotel: {}".format(hotel.hotel_name))
                        person_walking(self, 1)
                        yield self.env.timeout(self.janusz_avg_walking_time)
                        person_walking(self, -1)

                        # Is there place for him to sleep there?
                        if hotel.get_empty_rooms() > 0:
                            with hotel.request() as req:

                                # There is a bed for him
                                pri(self, "Booking time at: {}".format(hotel.hotel_name))
                                yield req
                                yield self.env.timeout(self.janusz_avg_organization_time)

                                # Janusz goes to bed
                                pri(self, "Sleeping for next {}h".format(self.janusz_sleeps_for_about_h))
                                yield self.env.timeout(self.janusz_sleeps_for_about_min)
                                self.janusz_nights_at_hotel.pop()

                                # Janusz wake up
                                pri(self, "Time to wake up")
                                yield self.env.timeout(self.janusz_avg_organization_time)

                                # Leeaving the hotel
                                pri(self, "Leaving {}".format(hotel.hotel_name))
                                break

                        # No there is not any bed for him
                        else:
                            pri(self, "No place to sleep at {}".format(hotel.hotel_name))

            # No, its not sleeping time
            pri(self, "Walking")
            person_walking(self, 1)
            yield self.env.timeout(self.janusz_avg_siqghtseeing_time)
            person_walking(self, -1)

            # TODO eating, sightseeing, museums, other atractions
