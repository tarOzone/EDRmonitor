import json
from time import sleep
from sys import platform
from serial import Serial
from serial.serialutil import SerialException


def read_config(config_file):
    with open(config_file, "r") as f:
        content = f.read()
    json_content = json.loads(content)

    if platform == "linux" or platform == "linux2":
        port = json_content["port_linux"]
    elif platform == "win32":
        port = json_content["port_windows"]

    columns = json_content["columns"]
    baud_rate = json_content["baud_rate"]
    return port, columns, baud_rate


class SerialArduino:

    def __init__(self, port, baud_rate, csv_columns, timeout=0.5):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial_lists = []
        self.csv_columns = csv_columns

    # connect to the arduino according to the port
    def connect(self):
        while not self.connect_serial():
            sleep(1)
        print("[SUCCESS] Connection DONE!!!")

    def readline(self):
        try:
            line = self.ser.readline()
            line = line.decode('utf-8').rstrip()
            line = json.loads(line)
            return line
        except json.decoder.JSONDecodeError:
            return {}
        except SerialException:
            return None

    def connect_serial(self):
        try:
            self.ser = Serial(self.port, self.baud_rate, timeout=self.timeout)
            return True
        except SerialException:
            return False

    def close(self):
        self.ser.close()
