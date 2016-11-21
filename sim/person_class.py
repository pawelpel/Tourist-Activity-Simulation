#!/usr/bin/env python3.5
import random as rr

from ._own_functions import pri, time_to_min, min_to_date, any_not, sort_hotels, person_walking


class Person(object):
    """
        Each Person has own:
        - name
        - length of stay
        - budget
        - needs
        - trip plan (prefers museums, clubs, sightseeing, ...)
    """

    def __init__(self, env, city_config, person_config):
        self.env = env
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())

        # Set person profile
        self.person_config = person_config
        self.name = self.person_config["name"]

        self.have_been_at_hotel = [False for _ in range(self.person_config["trip_duration"]//time_to_min(d=1))]

        # Handle the city
        self.hotels = set(city_config["hotels"])

    def run(self):
        """
            Main loop to handle person behaviour.
        """
        # Show person options
        # print(self.have_been_at_hotel, self.want_to_be_at_hotel)

        # Janusz arriving to the city
        yield self.env.timeout(self.person_config["arriving_time"])
        pri(self, "Arrived")

        while True:
            # Sleeping time ?
            if (self.env.now % time_to_min(d=1, h=rr.randint(-3, 3))) < time_to_min(h=7):

                # Have need to sleep that night at hotel?
                if any_not(self.have_been_at_hotel):

                    # Yes, so he is looking for a hotel
                    for hotel in sort_hotels(self.hotels):

                        # Found one, so he is going to that hotel
                        pri(self, "Going to hotel: {}".format(hotel.hotel_name))
                        person_walking(self, 1)
                        yield self.env.timeout(time_to_min(mi=rr.randint(3, 15)))
                        person_walking(self, 0)

                        # Is there place for him to sleep there?
                        if hotel.get_empty_rooms() > 0:
                            with hotel.request() as req:

                                # There is a bed for him
                                pri(self, "Booking time at: {}".format(hotel.hotel_name))
                                yield req
                                yield self.env.timeout(time_to_min(mi=rr.randint(1, 8)))

                                # Janusz goes to bed
                                sleep_hours = rr.randint(6, 10)
                                pri(self, "Sleeping for next {}h".format(sleep_hours))
                                yield self.env.timeout(time_to_min(h=sleep_hours))

                                # Janusz wake up
                                pri(self, "Time to wake up")
                                yield self.env.timeout(time_to_min(mi=rr.randint(5, 60)))

                                # Leeaving the hotel
                                pri(self, "Leaving hotel {}".format(hotel.hotel_name))
                                break

                        # No there is not any bed for him
                        else:
                            pri(self, "No place to sleep at {}".format(hotel.hotel_name))

                            # He is going to check other hotel
                            person_walking(self, 1)
                            yield self.env.timeout(time_to_min(mi=rr.randint(1, 3)))
                            person_walking(self, 0)

            # Is that the end of his trip?
            if self.env.now >= self.person_config["arriving_time"] + self.person_config["trip_duration"]:
                pri(self, "End of the trip. GOODBYE!")
                break

            # No, its not sleeping time
            pri(self, "Walking")
            person_walking(self, 1)
            yield self.env.timeout(time_to_min(mi=rr.randint(1, 60*3)))
            person_walking(self, 0)

            # sniadanie

            # zwiedzanie

            # obiad

            # zwiedzanie

            # kolacja

            # zwiedzanie

            # kluby

            # hotel
