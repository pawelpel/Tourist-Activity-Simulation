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
        self.person_arriving_time = self.person_config["arriving_time"]
        self.person_trip_duration = self.person_config["trip_duration"]
        self.person_actual_trip_duration = self.person_arriving_time + self.person_trip_duration

        # hotel
        self.person_goes_to_sleep_at_h = ra.randint(21, 24)
        self.person_goes_to_sleep_at_min = time_to_min(h=self.person_goes_to_sleep_at_h)
        self.person_cant_go_to_sleep_at_min = time_to_min(h=(24 - self.person_goes_to_sleep_at_h + ra.randint(1, 4)))

        self.person_nights_at_hotel = [1 for _ in range(self.person_trip_duration // time_to_min(d=1))]
        self.person_sleeps_for_about_h = ra.randint(6, 8)
        self.person_sleeps_for_about_min = time_to_min(h=self.person_sleeps_for_about_h)

        # walking
        self.person_avg_sightseeing_time = time_to_min(h=ra.randint(3, 5))
        self.person_avg_meters_in_min = ra.randint(3, 6)*1000//60

        # global actions
        self.person_avg_organization_time = time_to_min(mi=ra.randint(5, 15))
        self.person_last_position = self.person_config["first_position"]

        # # Handle the city
        self.hotels = sort_city_objects_by_popularity(city_config["hotels"])
        self.restaurants = sort_city_objects_by_popularity(city_config["restaurants"])

    def run(self):
        """
            Main loop to handle person behaviour.
        """
        # Janusz arriving to the city
        yield self.env.timeout(self.person_arriving_time)
        pri(self, "Arrived")

        while True:
            # Is that the end of his trip?
            if check_if_trip_is_over(self, self.person_actual_trip_duration):
                break

            # Sleeping time ?
            if check_time(self, self.person_goes_to_sleep_at_min, self.person_cant_go_to_sleep_at_min):
                # Have need to sleep that night at hotel?
                if any(self.person_nights_at_hotel):

                    # Yes, so he is looking for a hotel
                    self.hotels = sort_city_objects_by_nearest_pos(self.hotels, self.person_last_position)
                    for hotel in self.hotels:

                        # Found one, so he is going to that hotel
                        how_long_going_to_hotel = calculate_walking_time(self.person_last_position, hotel.position,
                                                                         self.person_avg_meters_in_min)
                        pri(self, "Going to hotel: {}, from {}, to {}, in time: {}".format(hotel.hotel_name,
                                                                                           self.person_last_position,
                                                                                           hotel.position,
                                                                                           how_long_going_to_hotel))
                        person_walking(self, 1)
                        yield self.env.timeout(how_long_going_to_hotel)
                        person_walking(self, -1)

                        # Update position
                        self.person_last_position = hotel.position

                        # Is there place for him to sleep there?
                        if hotel.get_empty_rooms() > 0:
                            with hotel.request() as req:

                                # There is a bed for him
                                pri(self, "Booking time at: {}".format(hotel.hotel_name))
                                yield req
                                yield self.env.timeout(self.person_avg_organization_time)

                                # Janusz goes to bed
                                pri(self, "Sleeping for next {}h".format(self.person_sleeps_for_about_h))
                                yield self.env.timeout(self.person_sleeps_for_about_min)

                                # Janusz wake up
                                pri(self, "Time to wake up")
                                yield self.env.timeout(self.person_avg_organization_time)

                                # Leeaving the hotel
                                pri(self, "Leaving {}".format(hotel.hotel_name))
                                break

                        # No there is not any bed for him
                        else:
                            pri(self, "No place to sleep at {}".format(hotel.hotel_name))

                    # Night is over
                    self.person_nights_at_hotel.pop()

            # No, its not sleeping time
            pri(self, "Walking")
            person_walking(self, 1)
            yield self.env.timeout(self.person_avg_sightseeing_time)
            person_walking(self, -1)

            # TODO eating, sightseeing, museums, other atractions
