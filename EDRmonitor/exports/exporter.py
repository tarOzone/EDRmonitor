import os
import csv
from EDRmonitor.utils.time_utils import get_datetime


columns = [
    'elapsed_time', 'mode', 'pedal',
    'temp', 'latitude', 'longitude',
    'altitude', 'speed', 'distance'
]


def _rectify(data, offset):
    elapsed_time = offset.get('elapsed_time', 0.0)
    total_distance = offset.get('distance', 0.0)
    data['elapsed_time'] -= elapsed_time
    data['distance'] -= total_distance


def to_csv(serial_list, csv_filename=""):
    if not csv_filename:
        dt = get_datetime(datetime_sep="_", date_sep="-", time_sep="-")
        csv_filename = os.path.join("logs", f"{dt}.csv")
    try:
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            offset = serial_list[0].copy()
            for data in serial_list:
                data.pop('status', None)
                _rectify(data, offset)
                writer.writerow(data)
        print(f"[INFO] {csv_filename} has been saved.")
        return True
    except FileExistsError:
        print(f"[ERROR] {csv_filename} already exists.")
        return False
