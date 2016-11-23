#!/usr/bin/env python3.5
import time
import datetime
import random
from string import ascii_letters
from functools import wraps

# 1 print, 0 not print
MUTE_PRINTING = 0


def pri(self, message=''):
    if MUTE_PRINTING:
        print("Time: {} {:<10} {}".format(datetime.timedelta(minutes=self.env.now), self.name, message))


def min_to_date(mi):
    return datetime.timedelta(minutes=mi)


def time_to_min(mi=0, h=0, d=0, y=0):
    return mi + h*60 + d*60*24 + y*60*24*365


def time_it(fun):
    @wraps(fun)
    def wrapp_fun(*args, **kwargs):
        start = time.time()
        fun(*args, **kwargs)
        end = time.time()
        print("Function {} executed in {:>3}s".format(fun.__name__, end-start))
    return wrapp_fun


def generate_token():
    random.seed(time.time())
    return ''.join(random.choice(ascii_letters) for _ in range(25))


def any_night(iterable):
    for element in iterable:
        if not element:
            return True
    return False


def sort_hotels(hotels):
    # return sorted(hotels, key=lambda x: x.hotel_popularity, reverse=True)
    if random.choice(range(0, 3)):
        tmp = sorted(hotels, key=lambda x: x.hotel_popularity, reverse=True)
    else:
        # Have some randomness in choosing hotel
        # but still most of them choose by popularity
        tmp = hotels[:]
        random.shuffle(tmp)
    return tmp


def person_walking(self, s):
    self.env.walking_people += s


def check_if_trip_is_over(self, trip_duration):
    return self.env.now >= trip_duration


def check_time(self, start, end):
    day = 24*60
    now = self.env.now
    if now > day:
        now -= (day * (now//day))
    if now <= day:
        if start <= now <= end:
            return True
        if now <= end <= start:
            return True
        if now >= start >= end:
            return True
    return False
