import os
import csv
from datetime import datetime


def _rectify(data, offset):
    elapsed_time = offset.get('elapsed_time', 0.0)
    total_distance = offset.get('distance', 0.0)
    data['elapsed_time'] -= elapsed_time
    data['distance'] -= total_distance


def export_csv(serial_list, csv_columns, save_path="."):
    csv_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    try:
        csv_filename = os.path.join(save_path, csv_filename)
        with open(f'{csv_filename}.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            offset = serial_list[0].copy()
            for data in serial_list:
                data.pop('status', None)
                _rectify(data, offset)
                writer.writerow(data)
        print(f"[INFO] {csv_filename} has been saved.")
    except Exception:
        return