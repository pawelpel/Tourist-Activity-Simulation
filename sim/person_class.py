#!/usr/bin/env python3.5
import random as ra

from ._own_functions import *


class Person(object):

    def __init__(self, env, city_config, person_config):
        # # Start the run process every time an instance is created.
        self.env = env
        self.action = self.env.process(self.run())

        # For loging file
        self.receiver = env.receiver

        # # Set person profile
        self.person_config = person_config
        self.name = self.person_config["name"]

        # trip
        self.person_arriving_time = self.person_config["arriving_time"]
        self.person_trip_duration = self.person_config["trip_duration"]
        self.person_leaving_time = self.person_arriving_time + self.person_trip_duration

        # hotel
        self.person_goes_to_sleep_at_h = ra.randint(21, 24)
        self.person_goes_to_sleep_at_min = time_to_min(h=self.person_goes_to_sleep_at_h)
        self.person_cant_go_to_sleep_at_min = time_to_min(h=(24 - self.person_goes_to_sleep_at_h + ra.randint(1, 4)))
        self.person_nights_at_hotel = self.person_trip_duration // time_to_min(d=1)
        self.person_sleeps_for_about_h = ra.randint(6, 10)
        self.person_sleeps_for_about_min = time_to_min(h=self.person_sleeps_for_about_h)
        self.person_last_hotel = None
        self.person_add_hours_for_outside_hotel = ra.randint(1, 3)
        self.person_max_number_of_tries_for_hotel = ra.randint(2, 5)

        # restaurant
        self.person_meals_per_day = ra.randint(2, 3)
        self.person_eaten_meals = 0
        self.person_max_number_of_tries_for_restaurant = ra.randint(2, 5)

        # museum
        self.list_of_museums = ra.sample(city_config["museums"], len(city_config["museums"])//ra.randint(1, 4))
        self.list_of_museums = sort_city_objects_by_popularity(self.list_of_museums)
        self.person_want_to_visit_museum = ra.randint(0, 8)
        self.person_max_number_of_tries_for_museum = ra.randint(2, 5)

        # sightseeing
        self.person_start_sightseeing = time_to_min(h=ra.randint(6, 10))
        self.person_stop_sightseeing = time_to_min(h=ra.randint(15, 18))
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

            # Have need to sleep this night at the hotel?
            if self.person_nights_at_hotel > 0:

                # Is that sleeping time
                if check_time(self, self.person_goes_to_sleep_at_min, self.person_cant_go_to_sleep_at_min):

                    # Yes, so he is looking for a hotel
                    self.hotels = sort_city_objects_by_nearest_pos(self.hotels, self.person_last_position)

                    # Was in any hotel before?
                    if self.person_last_hotel:

                        # Yes, so that hotel become his first try
                        self.hotels.remove(self.person_last_hotel)
                        self.hotels = [self.person_last_hotel, *self.hotels]

                    # Let's check hotels
                    hotels_checked = 0
                    for hotel in self.hotels:

                        # Going to the hotel, and it takes him some time
                        how_long_going_to_hotel = calculate_walking_time(self.person_last_position,
                                                                         hotel.position,
                                                                         self.person_avg_meters_in_min)
                        pri(self, "Going to hotel: {}, from {}, to {}, in time: {}".format(hotel.hotel_name,
                                                                                           self.person_last_position,
                                                                                           hotel.position,
                                                                                           how_long_going_to_hotel))
                        person_walking(self, 1)
                        yield self.env.timeout(how_long_going_to_hotel)
                        person_walking(self, -1)

                        # Update his position
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

                                self.person_last_hotel = hotel
                                break

                        # No there is not any bed for him
                        else:
                            pri(self, "No place to sleep at {}".format(hotel.hotel_name))
                            hotels_checked += 1

                    # Janusz didn't find any empty hotel
                    if hotels_checked >= self.person_max_number_of_tries_for_hotel:

                        # So he is leaving the Old Town to find hotel
                        new_pos = ra.choice((
                            (0, 0),
                            (0, self.env.map_size_y),
                            (self.env.map_size_x, 0),
                            (self.env.map_size_x, self.env.map_size_y)
                        ))

                        # And it will take him some time to get there
                        how_long_going_to_outside_hotel = calculate_walking_time(self.person_last_position, new_pos,
                                                                                 self.person_avg_meters_in_min)
                        pri(self, "Going to the hotel outside Old Town")
                        person_walking(self, 1)
                        yield self.env.timeout(how_long_going_to_outside_hotel)
                        person_walking(self, -1)

                        # Janusz is in the hotel outside the Old Town
                        additional_hours = self.person_add_hours_for_outside_hotel
                        pri(self, "Being in anonymous hotel for {}h".format(self.person_sleeps_for_about_h +
                                                                            additional_hours))
                        yield self.env.timeout(self.person_sleeps_for_about_min +
                                               time_to_min(h=additional_hours))

                    # Night is over
                    self.person_nights_at_hotel -= 1

            # Is that the end of his trip?
            if check_if_trip_is_over(self, self.person_leaving_time):
                pri(self, "Leaving the town.")
                break

            # Does he have any meal to eat ?
            if self.person_eaten_meals < self.person_meals_per_day:

                # Yes, so he is looking for nearest opened restaurant
                checked_restaurants = 0
                for restaurant in sort_city_objects_by_nearest_pos(get_opened_places(self.restaurants, self.env),
                                                                   self.person_last_position):

                    # Found one, so he is going to that restaurant, it takes him some time
                    how_long_going_to_restaurant = calculate_walking_time(self.person_last_position,
                                                                          restaurant.position,
                                                                          self.person_avg_meters_in_min)
                    pri(self, "Going to restaurant: {}, f{} to{}, distance {}m, in time: {}".format(
                        restaurant.restaurant_name,
                        self.person_last_position,
                        restaurant.position,
                        int(calculate_distance(self.person_last_position,
                                               restaurant.position)),
                        how_long_going_to_restaurant))

                    person_walking(self, 1)
                    yield self.env.timeout(how_long_going_to_restaurant)
                    person_walking(self, -1)

                    # Update position
                    self.person_last_position = restaurant.position

                    # Is there place for him to eat there and is that restaurant still opened?
                    if not restaurant.is_crowded() and restaurant.min_to_close(self.env)\
                            and restaurant.is_opened(self.env):

                        # There is a chair for him so he is going to eat there
                        with restaurant.request() as req:

                            # Eating takes him some time
                            new_visit_time = ra.randint(restaurant.visit_time//2, restaurant.visit_time)

                            pri(self, "Eating time at: {} for next {}min".format(restaurant.restaurant_name,
                                                                                 new_visit_time))
                            yield req
                            yield self.env.timeout(new_visit_time)

                            # Meal eaten
                            self.person_eaten_meals += 1
                            break
                    else:
                        # Restaurant is closed or will be in short time? Maybe crowded? Check next restaurant!
                        pri(self, "Looking for different restaurant, C:{} CL:{} T:{} P:{}".format(
                            restaurant.is_crowded(),
                            restaurant.is_opened(self.env),
                            restaurant.min_to_close(self.env),
                            restaurant.count
                        ))
                        checked_restaurants += 1

                        # Give up on looking for restaurant
                        if checked_restaurants > self.person_max_number_of_tries_for_restaurant:
                            break

            # Is that the end of his trip?
            if check_if_trip_is_over(self, self.person_leaving_time):
                pri(self, "Leaving the town.")
                break

            # Sightseeing ?
            pri(self, "Sightseeing")
            person_walking(self, 1)
            yield self.env.timeout(self.person_avg_sightseeing_time)
            self.person_last_position = get_new_location_based_on_walking_time(self.person_last_position,
                                                                               self.person_avg_sightseeing_time,
                                                                               self.person_avg_meters_in_min,
                                                                               self.env)
            person_walking(self, -1)

            # Visiting museums ?
            if self.person_want_to_visit_museum:

                # Looking for nearest opened museum
                checked_museums = 0
                for museum in sort_city_objects_by_nearest_pos(get_opened_places(self.list_of_museums, self.env),
                                                               self.person_last_position):

                    # Found one, so he is going to that museum and it takes him some time
                    how_long_going_to_museum = calculate_walking_time(self.person_last_position,
                                                                      museum.position,
                                                                      self.person_avg_meters_in_min)

                    pri(self, "Going to museum: {}, f{} to{}, distance {}m, in time: {}".format(
                        museum.museum_name,
                        self.person_last_position,
                        museum.position,
                        int(calculate_distance(self.person_last_position,
                                               museum.position)),
                        how_long_going_to_museum))

                    person_walking(self, 1)
                    yield self.env.timeout(how_long_going_to_museum)
                    person_walking(self, -1)

                    # Update his position
                    self.person_last_position = museum.position

                    # Is opened? Is not crowded? Can he visit it?
                    if not museum.is_crowded() and museum.min_to_close(self.env) and museum.is_opened(self.env):

                        # Yes, it is!
                        with museum.request() as req:

                            # Visiting takes him some time
                            new_visit_time = ra.randint(museum.visit_time//2, museum.visit_time)

                            pri(self, "Visiting: {} for next {}min".format(museum.museum_name,
                                                                           new_visit_time))
                            yield req
                            yield self.env.timeout(new_visit_time)

                            # Remove that museum from list! He doesn't want to see it again.
                            self.list_of_museums.remove(museum)
                            break
                    else:
                        # Museum is closed or will be in short time? Maybe crowded? Check next museum!
                        pri(self, "Looking for different museum, C:{} CL:{} T:{} P:{}".format(
                            not museum.is_crowded(),
                            museum.is_opened(self.env),
                            museum.min_to_close(self.env),
                            museum.count
                        ))
                        checked_museums += 1

                        # Give up on looking for museum
                        if checked_museums > self.person_max_number_of_tries_for_museum:
                            break

            # Is that the end of his trip?
            if check_if_trip_is_over(self, self.person_leaving_time):
                pri(self, "Leaving the town.")
                break
