#!/usr/bin/env python3.5
import time
import datetime
import random
import math
from string import ascii_letters
from functools import wraps

# 1 print/write to file,     0 no print/no write
MUTE_PRINTING = 0
MUTE_WRITING = 1


def init_text_to_write_receiver(options):
    with open('sim_agents_log.txt', 'w') as file:

        file.write(options)
        file.write("\n")

        while 1:
            item = yield
            file.write(item)


def pri(self, message=''):
    if MUTE_PRINTING:
        print("Time: {} {:<10} {}".format(datetime.timedelta(minutes=self.env.now), self.name, message))
    if MUTE_WRITING:
        self.receiver.send("Time: {} {:<10} {} \n".format(datetime.timedelta(minutes=self.env.now), self.name, message))


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


def sort_city_objects_by_popularity(objs):
    # if random.choice(range(0, 2)):
    #     tmp = sorted(objs, key=lambda x: x.popularity, reverse=True)
    # else:
    #     # Have some randomness in choosing obj
    #     # but still most of them choose by popularity
    #     tmp = objs[:]
    #     random.shuffle(tmp)
    # return tmp
    return objs


def person_walking(self, s):
    self.env.walking_people += s


def check_if_trip_is_over(self, trip_duration):
    return self.env.now >= trip_duration


def check_time_alg(now, start, end):
    day = 24 * 60
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


def check_time(self, start, end):
    now = self.env.now
    return check_time_alg(now, start, end)


def check_time_2(env, start, end):
    now = env.now
    return check_time_alg(now, start, end)


def calculate_distance(from_pos, to_pos):
    return math.sqrt((to_pos[0]-from_pos[0])**2 + (to_pos[1]-from_pos[1])**2)


def calculate_walking_time(from_pos, to_pos, avg_meters_in_min):
    distance = calculate_distance(from_pos, to_pos)
    # print("Distance "+str(int(distance)))
    return distance//avg_meters_in_min + 1


def sort_city_objects_by_nearest_pos(objs, from_pos):
    if random.choice(range(0, 2)):
        tmp = sorted(objs, key=lambda x: calculate_distance(from_pos, x.position))
    else:
        # Have some randomness in choosing object
        # but still most of them choose by position
        tmp = objs[:]
        random.shuffle(tmp)
    return tmp


def convert_time_to_min(time_):
    h, m = time_.split(':')
    return time_to_min(h=int(h), mi=int(m))


def get_opened_places(place, env):
    return [p for p in place if p.is_opened(env)]


def get_new_location_based_on_walking_time(current_loc, walking_time, meters_in_min, env):
    # radius of the circle
    circle_r = walking_time * meters_in_min
    if abs(circle_r) > env.map_size_x or abs(circle_r) > env.map_size_y:
        circle_r = env.map_size_x if env.map_size_x > env.map_size_y else env.map_size_y
        circle_r *= 2
    # center of the circle (x, y)
    circle_x = current_loc[0]
    circle_y = current_loc[1]

    # random angle
    alpha = 2 * math.pi * random.random()
    # random radius
    r = circle_r * random.random()
    # calculating coordinates
    x = r * math.cos(alpha) + circle_x
    y = r * math.sin(alpha) + circle_y
    return int(x), int(y)
