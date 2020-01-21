from flask import request
from datetime import datetime


def read_json_request():
    return request.json


def get_data():
    json_request = read_json_request()

    try:
        latitude = json_request['latitude']
        longitude = json_request['longitude']
        temp = json_request['temp']
        mode = json_request['mode']
        speed = json_request['speed'] * (18./5.)
        distance = json_request['total_distance'] / 1000.
        elapsed_time = json_request['elapsed_time']
        timestamp = datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
    except TypeError:
        return None, None, None, None, None, None, None, None

    return timestamp, latitude, longitude, temp, mode, speed, distance, elapsed_time

