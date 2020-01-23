import csv
import json
from time import sleep
from serial import Serial
from datetime import datetime
from serial.serialutil import SerialException


def read_config(config_file):
    with open(config_file, "r") as f:
        content = f.read()
    json_content = json.loads(content)
    port = json_content["port"]
    columns = json_content["columns"]
    baud_rate = json_content["baud_rate"]
    return port, columns, baud_rate


class SerialArduino:

    def __init__(self, port, baud_rate, csv_columns):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
        self.serial_lists = []
        self.csv_columns = csv_columns
        self.connect()

    def readline(self):
        try:
            line = self.ser.readline()
            line = line.decode('utf-8').rstrip()
            line = json.loads(line)
            self.serial_lists.append(line)
            return line
        except Exception as e:
            return {}

    def connect(self):
        while not self.connect_serial():
            sleep(1)
        print("[SUCCESS] Connection DONE!!!")

    def connect_serial(self):
        try:
            self.ser = Serial(self.port, self.baud_rate)
            return True
        except SerialException:
            return False

    def export_csv(self):
        csv_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f'{csv_filename}.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
            writer.writeheader()
            for data in self.serial_lists:
                writer.writerow(data)

    def __del__(self):
        print("CLOSING...")
        try:
            self.ser.close()
        except AttributeError:
            pass
        self.export_csv()
        

if __name__ == "__main__":
    port, columns, baud_rate = read_config("config.json")
    try:
        ser = SerialArduino(port, baud_rate, columns)
        for i in range(50):
            line = ser.readline()
            print(line)
    finally:
        del ser

