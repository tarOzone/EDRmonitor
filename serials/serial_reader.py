import csv
import json
from time import sleep
from datetime import datetime

from serial import Serial
from serial.serialutil import SerialException, SerialTimeoutException


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
        self.connecting = False
        self.serial_lists = []
        self.csv_columns = csv_columns

        self.curr_status = False
        self.prev_status = False

    # connect to the arduino according to the port
    def connect(self):
        while not self.connect_serial():
            sleep(1)
        self.connecting = True
        print("[SUCCESS] Connection DONE!!!")

    def run(self):
        if self.connecting:
            while True:
                line = self.ser.readline()
                if self.curr_status:
                    print(line)
                    if not self.prev_status:
                        self.serial_lists.clear()
                    self.serial_lists.append(line)
                else:
                    if self.prev_status:
                        self.export_csv()
                self.prev_status = self.curr_status

    def readline(self):
        try:
            line = self.ser.readline()
            line = line.decode('utf-8').rstrip()
            line = json.loads(line)
            self.curr_status = line['status']
            return line
        except json.JSONDecodeError:
            return {}
        except SerialException as e:
            self.close()
            self.connecting = False

    def connect_serial(self):
        try:
            self.ser = Serial(self.port, self.baud_rate)
            return True
        except SerialException as e:
            return False

    def rectify(self, data, offset):
        elapsed_time = offset.get('elapsed_time', 0.0)
        total_distance = offset.get('total_distance', 0.0)
        data['elapsed_time'] -= elapsed_time
        data['total_distance'] -= total_distance

    def export_csv(self):
        csv_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f'{csv_filename}.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
            writer.writeheader()
            offset = self.serial_lists[0].copy()
            for data in self.serial_lists:
                data.pop('status', None)
                self.rectify(data, offset)
                writer.writerow(data)
        print(f"[INFO] {csv_filename} has been saved.")

    def close(self):
        try:
            print("CLOSING...")
            self.ser.close()
            self.connecting = False
        except AttributeError:
            pass
        

if __name__ == "__main__":
    port, columns, baud_rate = read_config("config.json")
    ser = SerialArduino(port, baud_rate, columns)
    while True:
        ser.connect()
        print("============================= CONNECTED ===============================")
        ser.run()
        print("============================ DISCONNECTED =============================")
